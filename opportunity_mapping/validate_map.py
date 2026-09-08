"""Source-grounded artifact validation. Does not execute an LLM benchmark."""
import copy,csv,hashlib,json,math,statistics
from pathlib import Path
from datetime import datetime,timezone
from jsonschema import Draft202012Validator
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
schema=read('opportunity_mapping/atlas_opportunity_map.schema.json');Draft202012Validator.check_schema(schema)
diag=read('reasoning/meridian_atlas_v0_diagnosis.json')
impact=read('impact_sizing/meridian_annualized_impact_sizing.json')
quant=read('diagnostics/meridian_quantitative_diagnostics.json')
rows=list(csv.DictReader((R/'source_pack/meridian_disputes_250.csv').open(encoding='utf-8')))
def pointer(obj,p):
    for token in p.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~');obj=obj[int(token)] if isinstance(obj,list) else obj[token]
    return obj
def validate(m):
    errors=[e.message for e in Draft202012Validator(schema).iter_errors(m)]
    if errors:return errors
    def check(ok,msg):
        if not ok:errors.append(msg)
    sources={s['id']:s for s in m['sources']};ds={d['id']:d for d in m['diagnoses']};ops={o['id']:o for o in m['opportunities']}
    check(len(sources)==len(m['sources']),'Duplicate source ID');check(len(ds)==len(m['diagnoses']),'Duplicate diagnosis ID');check(len(ops)==len(m['opportunities']),'Duplicate opportunity ID')
    allowed=set(x['file'] for x in read('source_manifest.json')['files']) | {'source_pack/README.md','reasoning/meridian_atlas_v0_diagnosis.json','impact_sizing/meridian_annualized_impact_sizing.json','diagnostics/meridian_quantitative_diagnostics.json'}
    for s in sources.values():
        check(s['file'] in allowed,'Evidence outside allowlist')
        check(not any(x in s['file'] for x in ['_Evaluation','evaluation_only','recovered']),'Forbidden mapping evidence')
        try:
            p=(R/s['file']).resolve();check(p.is_relative_to(R.resolve()),'Unsafe source path')
            check(hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],'Source hash mismatch')
            if s['json_pointer']:pointer(json.loads(p.read_text(encoding='utf-8')),s['json_pointer'])
        except (OSError,ValueError,KeyError,IndexError):errors.append('Unresolvable evidence locator')
    expected_ids={f['finding_id'] for f in diag['diagnostic_findings']}|{'C1','P5'}
    check(set(ds)==expected_ids,'Diagnosis set mismatch')
    for f in diag['diagnostic_findings']:
        d=ds.get(f['finding_id'],{});check(d.get('finding')==f['finding'] and d.get('evidence_type')==f['evidence_type'],'Original finding/type altered')
    for d in ds.values():check(set(d['source_refs'])<=set(sources),'Broken diagnosis source')
    expected_refs=dict(zip(['O01','O02','O03','O04','O05','O06','O07','O08','O09'],['F1','F2','F3','F4','F5','F6','F7','C1','P5']))
    check(set(ops)==set(expected_refs),'Opportunity coverage mismatch')
    lens_op={'O01':2,'O02':1,'O05':0,'O07':3}
    for o in ops.values():
        check(o['diagnosis_refs']==[expected_refs.get(o['id'])],'Wrong opportunity-to-diagnosis link')
        for refs in [o['source_refs'],o['affected_cohort']['source_refs'],o['impact']['burden_source_refs']]:check(set(refs)<=set(sources),'Broken opportunity citation')
        check(o['recommendation_evidence_type']=='INFERRED','Recommendation presented as observed fact')
        c=o['components'];check(len(c)==len(set(c)),'Duplicate component')
        check(len(c)>=2 and 'HYBRID' not in c if o['primary_type']=='HYBRID' else c==[o['primary_type']],'Invalid decomposition')
        idx=lens_op.get(o['id']);lens=impact['diagnostic_lenses'][idx] if idx is not None else None
        check(o['affected_cohort']['annual_cases']==(lens['annualized_cases'] if lens else None),'Incorrect annualized exposure')
        check(o['impact']['associated_burden_hours']==(lens['associated_extra_active_hours'] if lens else None),'Incorrect associated burden')
        check(o['impact']['status']=='UNSIZED' and o['impact']['annual_savings_hours'] is None and o['impact']['annual_savings_currency'] is None,'Unmeasured savings')
        check(o['impact']['overlap_group']=='AP_DISPUTE_UNIVERSE','Missing overlap control')
    check(set(x for o in ops.values() for x in o['diagnosis_refs'])==expected_ids,'Incomplete diagnosis coverage')
    b=m['baseline'];a=impact['assumptions'];n=len(rows);annual=a['annual_disputes'];mean=statistics.mean(float(x['handling_minutes']) for x in rows)
    check(b['annual_cases']==annual and b['sample_cases']==n,'Incorrect annualization assumptions')
    check(b['annual_handling_hours_precise']==annual*mean/60==71952,'Incorrect precise baseline')
    check(b['annual_handling_hours_day2_reported']==impact['overall_current_state']['annual_active_handling_hours'],'Source headline not preserved')
    check(b['productive_hours_per_fte']==a['productive_hours_per_fte'],'Incorrect FTE assumption')
    check(math.isclose(b['fte_precise'],71952/1700),'Incorrect FTE calculation')
    check(b['team_fte']==52 and b['fully_loaded_cost_per_fte_usd']==85000 and b['annual_team_cost_usd']==52*85000 and b['cost_per_productive_hour_usd']==85000/1700,'Incorrect cost assumptions')
    predicates=[lambda x:x['reopened']=='Yes',lambda x:x['missing_evidence']=='Yes',lambda x:int(x['systems_accessed_count'])>=4,lambda x:x['resolution']=='ESCALATE']
    for i,pred in enumerate(predicates):
        yes=[x for x in rows if pred(x)];no=[x for x in rows if not pred(x)]
        cases=annual*len(yes)/n;gap=statistics.mean(float(x['handling_minutes']) for x in yes)-statistics.mean(float(x['handling_minutes']) for x in no)
        lens=m['burden_lenses'][i];check(lens['annualized_cases']==cases and math.isclose(lens['associated_hours_unrounded'],cases*gap/60) and lens['associated_hours_rounded']==round(cases*gap/60)==impact['diagnostic_lenses'][i]['associated_extra_active_hours'],'Burden lens not reproducible')
    check('LLM' not in ops['O08']['components'] and ops['O08']['accountable_owner']=='Procurement' and 'until authority exists' in ops['O08']['proposed_intervention'] and 'Legal' in ops['O08']['proposed_intervention'],'Solara authority breach')
    check('original disputed amount' in ops['O09']['proposed_intervention'],'Partial-amount routing breach')
    check('HOLD_FOR_POLICY_CLARIFICATION' in ops['O09']['prohibited_action'],'Threshold ambiguity omitted')
    check('$48088.38' in ops['O06']['prohibited_action'] and 'reconciliation' in ops['O06']['prohibited_action'],'Unreconciled Apex scope ignored')
    check('not labels for correctness' in ops['O04']['classification_reason'],'History-as-truth breach')
    check('AP may apply clear contractual terms' in ops['O03']['proposed_intervention'],'Unnecessary specialist routing')
    check(m['status']=='FILE_GROUNDED_FINAL_DESIGN','Wrong evidence status')
    return errors

