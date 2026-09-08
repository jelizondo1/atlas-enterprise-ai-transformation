"""Atlas Day 4: deterministic, single-bundle ROI. Python standard library only.

Money/time inputs are decimal strings; output decimals are strings. No network,
LLM, financial action, posting, or approval execution is performed.
"""
import argparse
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path

PARAMS = {
    'unique_eligible_annual_cases': 'cases/year',
    'baseline_bundle_minutes': 'active minutes/eligible case',
    'intervention_bundle_minutes_including_review': 'active minutes/eligible case',
    'steady_adoption_fraction': 'fraction',
    'year1_adoption_fraction': 'fraction, annual average including ramp',
    'annual_internal_maintenance_hours': 'hours/year',
    'implementation_cash_cost_usd': 'USD, one time',
    'annual_incremental_run_cash_cost_usd': 'USD/year',
    'cash_realization_fraction': 'fraction of positive net capacity value',
}
BASELINE = {'annual_disputes': '180000', 'annual_handling_hours': '71952',
            'productive_hours_per_fte': '1700', 'capacity_rate_usd_per_hour': '50'}
STATUSES = {'UNKNOWN', 'ILLUSTRATIVE', 'PILOT_MEASURED', 'APPROVED_PLANNING'}
GOV_FIELDS = {'unique_cohort_verified', 'bundle_time_nonoverlap_verified',
              'quality_gate_passed', 'control_gate_passed',
              'cash_realization_plan_approved', 'review_ref', 'realization_plan_ref'}

class InputError(ValueError):
    pass

def exact_keys(obj, expected, location):
    if not isinstance(obj, dict) or set(obj) != set(expected):
        raise InputError(location + ': missing or unexpected fields')

def decimal_value(value, name):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{1,13}(\.[0-9]{1,12})?',value):
        raise InputError(name + ': expected a decimal string')
    try:
        d = Decimal(value)
    except InvalidOperation as exc:
        raise InputError(name + ': invalid decimal') from exc
    if not d.is_finite() or d < 0 or d > Decimal('1000000000000'):
        raise InputError(name + ': nonfinite, negative or excessive value')
    return d

def fmt(value):
    return format(value.quantize(Decimal('0.000001')), 'f')

def calculate(data):
    exact_keys(data, {'schema_version','scenario_id','mode','bundle_opportunity_ids',
                     'baseline','parameters','governance','evidence_registry'}, 'input')
    if data['schema_version'] != '1.0.0' or data['mode'] not in {'UNSIZED','ILLUSTRATIVE','MEASURED_INPUTS'}:
        raise InputError('Unsupported version/mode')
    if not isinstance(data['scenario_id'], str) or not data['scenario_id']:
        raise InputError('scenario_id required')
    if data['bundle_opportunity_ids'] != ['O01','O02','O05']:
        raise InputError('This model evaluates the joint O01/O02/O05 bundle once')
    if data['baseline'] != BASELINE:
        raise InputError('Meridian baseline must match the reconciled Day 3 source')
    exact_keys(data['parameters'], PARAMS, 'parameters')
    registry = {}
    if not isinstance(data['evidence_registry'], list):
        raise InputError('Evidence registry must be a list')
    for e in data['evidence_registry']:
        exact_keys(e, {'id','kind','description'}, 'evidence record')
        if not all(isinstance(e[k],str) and e[k] for k in e):
            raise InputError('Evidence fields must be nonempty strings')
        if e['id'] in registry or e['kind'] not in {'SOURCE_ASSUMPTION','ILLUSTRATIVE','PILOT_MEASUREMENT','APPROVED_PLAN','GATE_REVIEW'}:
            raise InputError('Duplicate/invalid evidence record')
        registry[e['id']] = e
    values, missing = {}, []
    expected_kind = {'ILLUSTRATIVE':'ILLUSTRATIVE','PILOT_MEASURED':'PILOT_MEASUREMENT','APPROVED_PLANNING':'APPROVED_PLAN'}
    for key, unit in PARAMS.items():
        p=data['parameters'][key]
        exact_keys(p, {'value','unit','status','source_ref','owner'}, key)
        if p['unit'] != unit or p['status'] not in STATUSES:
            raise InputError(key + ': unit/status mismatch')
        if p['status']=='UNKNOWN':
            if p['value'] is not None or p['source_ref'] is not None:
                raise InputError(key + ': unknown must have null value/reference')
            missing.append(key)
            continue
        if p['value'] is None:
            raise InputError(key + ': known value cannot be null')
        if not isinstance(p['owner'],str) or not p['owner']:
            raise InputError(key + ': accountable input owner required')
        if not isinstance(p['source_ref'],str):
            raise InputError(key + ': reference must be a string')
        ref=registry.get(p['source_ref'])
        if not ref or ref['kind']!=expected_kind[p['status']]:
            raise InputError(key + ': invalid evidence provenance')
        if data['mode']=='MEASURED_INPUTS' and p['status']=='ILLUSTRATIVE':
            raise InputError('Illustrative assumptions cannot masquerade as measured inputs')
        values[key]=decimal_value(p['value'], key)
        if key.endswith('_fraction') and values[key]>1:
            raise InputError(key + ': fraction exceeds one')
    g=data['governance'];exact_keys(g,GOV_FIELDS,'governance')
    for key in GOV_FIELDS-{'review_ref','realization_plan_ref'}:
        if g[key] is not None and type(g[key]) is not bool:
            raise InputError(key+': expected boolean or null')
    for key,kind in [('review_ref','GATE_REVIEW'),('realization_plan_ref','APPROVED_PLAN')]:
        if g[key] is not None and (not isinstance(g[key],str) or g[key] not in registry or registry[g[key]]['kind']!=kind):
            raise InputError(key+': invalid review/plan reference')
    n=values.get('unique_eligible_annual_cases')
    if n is not None and (n!=n.to_integral_value() or n>Decimal(BASELINE['annual_disputes'])):
        raise InputError('Eligible volume must be whole unique cases within annual population')
    if n is not None and 'baseline_bundle_minutes' in values:
        if n*values['baseline_bundle_minutes']/60>Decimal(BASELINE['annual_handling_hours']):
            raise InputError('Eligible bundle baseline exceeds total active handling; check overlap/units')
    if {'steady_adoption_fraction','year1_adoption_fraction'} <= values.keys():
        if values['year1_adoption_fraction']>values['steady_adoption_fraction']:
            raise InputError('Year-one adoption must not exceed the steady state in this ramp model')
    encoded=json.dumps(data,sort_keys=True,separators=(',',':')).encode()
    result={'schema_version':'1.0.0','scenario_id':data['scenario_id'],'mode':data['mode'],
            'input_sha256':hashlib.sha256(encoded).hexdigest(),'status':None,'missing_parameters':missing,
            'blocked_reasons':[],'steady_state':None,'year_one':None,'break_even':None,
            'claim_boundary':'Scenario calculation only. Capacity value is not cash savings; no deployment or payment authority.',
            'rounding':'Decimal arithmetic; six decimal places serialized, rounding only at output.'}
    if missing:
        result['status']='NOT_ESTIMABLE';return result
    if data['mode']=='UNSIZED':
        raise InputError('Complete inputs require explicit illustrative or measured mode')
    for key in ['unique_cohort_verified','bundle_time_nonoverlap_verified','quality_gate_passed','control_gate_passed']:
        if g[key] is not True:result['blocked_reasons'].append(key)
    if g['review_ref'] is None:result['blocked_reasons'].append('review_ref')
    if values['cash_realization_fraction']>0 and (g['cash_realization_plan_approved'] is not True or g['realization_plan_ref'] is None):
        result['blocked_reasons'].append('cash realization needs approved plan and reference')
    if data['mode']=='MEASURED_INPUTS':
        for key in ['unique_eligible_annual_cases','baseline_bundle_minutes','intervention_bundle_minutes_including_review']:
            if data['parameters'][key]['status']!='PILOT_MEASURED':
                result['blocked_reasons'].append(key+': measured coverage/time evidence required')
    if result['blocked_reasons']:
        result['status']='BLOCKED';return result
    with localcontext() as context:
        context.prec=32
        minutes=values['baseline_bundle_minutes']-values['intervention_bundle_minutes_including_review']
        rate=Decimal(BASELINE['capacity_rate_usd_per_hour']);fte=Decimal(BASELINE['productive_hours_per_fte'])
        maintenance=values['annual_internal_maintenance_hours'];run=values['annual_incremental_run_cash_cost_usd'];build=values['implementation_cash_cost_usd'];real=values['cash_realization_fraction']
        def period(adoption,implementation):
            gross=n*adoption*minutes/60
            net=gross-maintenance
            capacity=net*rate
            cash=max(net,Decimal(0))*rate*real
            cost=run+implementation
            cash_net=cash-cost
            noncash=max(capacity,Decimal(0))-cash
            return {'adopted_annual_cases':fmt(n*adoption),'gross_released_hours':fmt(gross),'net_capacity_hours':fmt(net),
                    'net_capacity_fte_equivalent':fmt(net/fte),'net_capacity_value_usd':fmt(capacity),
                    'realizable_labor_cash_benefit_usd':fmt(cash),'remaining_noncash_capacity_value_usd':fmt(noncash),
                    'incremental_cash_cost_usd':fmt(cost),'net_cash_benefit_usd':fmt(cash_net),
                    'cash_roi_fraction':fmt(cash_net/cost) if cost>0 else None,
                    'capacity_minus_incremental_cash_cost_usd':fmt(capacity-cost),
                    'warning':'Capacity and cash views are alternatives, not additive benefits. Negative net capacity is retained.'}
        steady=period(values['steady_adoption_fraction'],Decimal(0));year1=period(values['year1_adoption_fraction'],build)
        margin=max(n*values['steady_adoption_fraction']*minutes/60-maintenance,Decimal(0))*rate*real-run
        # This is explicitly a steady-run-rate proxy, not a ramp-adjusted cash-flow payback.
        proxy=Decimal(0) if build==0 and margin>0 else build/margin*12 if margin>0 else None
        divisor=n*values['steady_adoption_fraction']
        threshold=(maintenance+(run/(rate*real) if real>0 else Decimal(0)))*60/divisor if divisor>0 and real>0 else None
        result.update(status='ILLUSTRATIVE_ONLY' if data['mode']=='ILLUSTRATIVE' else 'CONDITIONAL_SCENARIO',steady_state=steady,year_one=year1,
                      break_even={'steady_state_cash_break_even_minutes_per_adopted_case':fmt(threshold) if threshold is not None else None,
                                  'steady_run_rate_payback_proxy_months':fmt(proxy) if proxy is not None else None,
                                  'actual_ramp_adjusted_payback_months':None,
                                  'note':'Proxy assumes steady benefit/run cost from start and excludes ramp; actual payback requires dated cash flows. Zero realization or nonpositive cash margin has no cash payback.'})
        return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input');parser.add_argument('--output',required=True);args=parser.parse_args()
    try:
        result=calculate(json.loads(Path(args.input).read_text(encoding='utf-8')))
    except (InputError,json.JSONDecodeError) as exc:
        result={'status':'INVALID_INPUT','error':str(exc)}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    return 1 if result['status']=='INVALID_INPUT' else 0

if __name__=='__main__':raise SystemExit(main())
