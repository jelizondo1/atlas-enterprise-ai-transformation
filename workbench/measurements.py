"""Active labor measurement and conservative Day 4 input preparation. No savings inference."""
import argparse,json
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from workbench import ROOT,Rejected,build_case,save,load
CATEGORIES={'EVIDENCE','FOLLOWUP','REVIEW','CLOSURE','REOPEN_REWORK'}
def instant(value):
    try:d=datetime.fromisoformat(value.replace('Z','+00:00'))
    except (ValueError,TypeError,AttributeError) as e:raise Rejected('Invalid timestamp') from e
    if d.tzinfo is None or d.utcoffset() is None:raise Rejected('Timestamp needs UTC offset')
    return d
def summarize(dataset,root=ROOT):
    if set(dataset)!={'mode','records'} or dataset['mode'] not in {'EMPTY','PILOT_MEASURED','SYNTHETIC_TEST'} or not isinstance(dataset['records'],list):raise Rejected('Invalid measurement dataset')
    if dataset['mode']=='EMPTY' and dataset['records']:raise Rejected('Empty mode cannot contain observations')
    ids=set();events=set();actor_intervals={};totals={'CONTROL':[],'TREATMENT':[]};incomplete=[]
    for r in dataset['records']:
        if set(r)!={'case_id','case_version_sha256','assignment','measurement_owner','observation_complete','quality_adjudicated','intervals'}:raise Rejected('Invalid measurement record')
        if r['case_id'] in ids:raise Rejected('Duplicate case; cannot count in both arms')
        ids.add(r['case_id']);case=build_case(r['case_id'],root)
        if r['case_version_sha256']!=case['case_version_sha256']:raise Rejected('Stale measurement case version')
        if r['assignment'] not in totals or not isinstance(r['measurement_owner'],str) or not r['measurement_owner']:raise Rejected('Assignment/owner required')
        if any(type(r[k]) is not bool for k in ['observation_complete','quality_adjudicated']):raise Rejected('Observation/quality state must be explicit')
        if not r['observation_complete'] or not r['quality_adjudicated']:incomplete.append(r['case_id'])
        if not isinstance(r['intervals'],list) or not r['intervals']:raise Rejected('Active-time observations missing; do not substitute zero')
        seconds=Decimal(0)
        for e in r['intervals']:
            if set(e)!={'event_id','actor_label','category','start','end'}:raise Rejected('Invalid timing interval')
            if not isinstance(e['event_id'],str) or not e['event_id'] or e['event_id'] in events:raise Rejected('Duplicate/invalid event ID')
            events.add(e['event_id'])
            if e['category'] not in CATEGORIES or not isinstance(e['actor_label'],str) or not e['actor_label']:raise Rejected('Invalid actor/category')
            start,end=instant(e['start']),instant(e['end'])
            if end<=start:raise Rejected('Interval must have positive duration')
            for a,b in actor_intervals.setdefault(e['actor_label'],[]):
                if start<b and end>a:raise Rejected('Overlapping active intervals for one person')
            actor_intervals[e['actor_label']].append((start,end));delta=end-start
            seconds+=Decimal(delta.days*86400+delta.seconds)+Decimal(delta.microseconds)/1000000
        totals[r['assignment']].append(seconds/60)
    means={k:str(sum(v)/len(v)) if v else None for k,v in totals.items()}
    ready=bool(totals['CONTROL'] and totals['TREATMENT']) and not incomplete
    return {'mode':dataset['mode'],'status':'READY_FOR_MEASUREMENT_REVIEW' if ready else 'INSUFFICIENT_MEASUREMENT','unique_cases':len(ids),'cases_by_arm':{k:len(v) for k,v in totals.items()},'mean_active_bundle_minutes':means,'incomplete_or_unadjudicated_cases':incomplete,'annual_eligible_cases':None,'statistical_causal_effect_established':False,'note':'Time is summed labor effort, including review/followup/rework. Concurrent different people contribute separate effort; one person cannot double-count time. Waiting is not active effort. Arm comparison is descriptive, not proof of causal effect.'}
def prepare_roi(dataset,root=ROOT):
    summary=summarize(dataset,root);inputs=load(root/'roi_operating_model/meridian_roi_inputs.json')
    if dataset['mode']=='PILOT_MEASURED' and summary['status']=='READY_FOR_MEASUREMENT_REVIEW':
        inputs['evidence_registry'].append({'id':'DAY5_MEASUREMENT','kind':'PILOT_MEASUREMENT','description':'User-supplied timing observations summarized by Day 5; design comparability, completeness and causal interpretation require independent owner review.'})
        for key,arm in [('baseline_bundle_minutes','CONTROL'),('intervention_bundle_minutes_including_review','TREATMENT')]:
            # Match Day 4's decimal precision contract; round only the exported mean.
            value=format(Decimal(summary['mean_active_bundle_minutes'][arm]).quantize(Decimal('0.000000000001')),'f')
            inputs['parameters'][key].update(value=value,status='PILOT_MEASURED',source_ref='DAY5_MEASUREMENT',owner='AP Analytics / measurement owner review required')
    return summary,inputs
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('dataset');p.add_argument('--output',required=True);a=p.parse_args()
    try:s,i=prepare_roi(load(a.dataset));save(Path(a.output)/'measurement_summary.json',s);save(Path(a.output)/'roi_inputs_prepared.json',i);print(s['status'])
    except (Rejected,ValueError,KeyError,TypeError) as e:print('REJECTED:',e);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
