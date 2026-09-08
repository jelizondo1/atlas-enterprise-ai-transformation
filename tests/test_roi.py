import sys
from pathlib import Path
for folder in ["workbench","roi_operating_model","model_integration"]: sys.path.insert(0,str(Path(__file__).resolve().parents[1]/folder))
"""Deterministic unit and control tests. All numeric scenarios are invented fixtures,
not Meridian pilot measurements, assumptions or benefit forecasts."""
import copy,json,unittest
from pathlib import Path
from decimal import Decimal
from roi_engine import calculate,InputError
from workflow_guards import assess
R=Path(__file__).resolve().parents[1]/"roi_operating_model"
def fixture():
    d=json.loads((R/'meridian_roi_inputs.json').read_text())
    d.update(scenario_id='SYNTHETIC_TEST_NOT_MERIDIAN_FORECAST',mode='ILLUSTRATIVE')
    d['evidence_registry'] += [{'id':'FIXTURE','kind':'ILLUSTRATIVE','description':'Invented arithmetic fixture only.'},{'id':'TEST_GATE','kind':'GATE_REVIEW','description':'Simulated gate attestation for software testing only.'},{'id':'TEST_PLAN','kind':'APPROVED_PLAN','description':'Simulated cash plan for software testing only.'}]
    vals=['12000','10','4','0.5','0.25','100','10000','5000','0.4']
    for p,value in zip(d['parameters'].values(),vals):p.update(value=value,status='ILLUSTRATIVE',source_ref='FIXTURE',owner='Test fixture author')
    d['governance']={k:True for k in d['governance']};d['governance'].update(review_ref='TEST_GATE',realization_plan_ref='TEST_PLAN')
    return d
def case():
    return {'material_risk':False,'tax_ambiguous':False,'policy_version_verified':True,'evidence_sufficient_human_verified':True,'contract_conflict':False,'solara_2026_freight':False,'solara_authority_confirmed':False,'disputed_scope_reconciled':True,'original_disputed_amount_usd':'12000','usd_basis_verified':True,'northstar_consultation_required':False,'procurement_consultation_recorded':False,'analyst_requests_escalation':False}
class ROITests(unittest.TestCase):
    def test_meridian_unknown_not_zero(self):
        r=calculate(json.loads((R/'meridian_roi_inputs.json').read_text()));self.assertEqual(r['status'],'NOT_ESTIMABLE');self.assertEqual(len(r['missing_parameters']),9);self.assertIsNone(r['steady_state'])
    def test_known_arithmetic(self):
        r=calculate(fixture());self.assertEqual(r['status'],'ILLUSTRATIVE_ONLY')
        expected={'gross_released_hours':'600.000000','net_capacity_hours':'500.000000','net_capacity_value_usd':'25000.000000','realizable_labor_cash_benefit_usd':'10000.000000','remaining_noncash_capacity_value_usd':'15000.000000','net_cash_benefit_usd':'5000.000000','cash_roi_fraction':'1.000000'}
        for k,v in expected.items():self.assertEqual(r['steady_state'][k],v,k)
        self.assertEqual(r['year_one']['net_cash_benefit_usd'],'-11000.000000');self.assertEqual(r['break_even']['steady_run_rate_payback_proxy_months'],'24.000000');self.assertEqual(r['break_even']['steady_state_cash_break_even_minutes_per_adopted_case'],'3.500000')
    def test_zero_realization_no_cash_savings(self):
        d=fixture();d['parameters']['cash_realization_fraction']['value']='0';d['governance'].update(cash_realization_plan_approved=False,realization_plan_ref=None)
        r=calculate(d);self.assertEqual(r['steady_state']['realizable_labor_cash_benefit_usd'],'0.000000');self.assertEqual(r['steady_state']['net_cash_benefit_usd'],'-5000.000000');self.assertIsNone(r['break_even']['steady_run_rate_payback_proxy_months'])
    def test_no_cash_plan_blocks(self):
        d=fixture();d['governance']['cash_realization_plan_approved']=False;self.assertEqual(calculate(d)['status'],'BLOCKED')
    def test_negative_capacity_not_clamped(self):
        d=fixture();d['parameters']['intervention_bundle_minutes_including_review']['value']='12';r=calculate(d);self.assertEqual(r['steady_state']['net_capacity_hours'],'-300.000000');self.assertEqual(r['steady_state']['net_capacity_value_usd'],'-15000.000000');self.assertEqual(r['steady_state']['realizable_labor_cash_benefit_usd'],'0.000000')
    def test_zero_adoption_keeps_maintenance_and_cost(self):
        d=fixture()
        for k in ['steady_adoption_fraction','year1_adoption_fraction']:d['parameters'][k]['value']='0'
        r=calculate(d);self.assertEqual(r['steady_state']['net_capacity_hours'],'-100.000000');self.assertIsNone(r['break_even']['steady_state_cash_break_even_minutes_per_adopted_case'])
    def test_zero_cost_roi_undefined(self):
        d=fixture()
        for k in ['implementation_cash_cost_usd','annual_incremental_run_cash_cost_usd']:d['parameters'][k]['value']='0'
        r=calculate(d);self.assertIsNone(r['year_one']['cash_roi_fraction']);self.assertEqual(r['break_even']['steady_run_rate_payback_proxy_months'],'0.000000')
    def test_quality_and_control_fail_closed(self):
        for k in ['quality_gate_passed','control_gate_passed','unique_cohort_verified','bundle_time_nonoverlap_verified']:
            for val in [False,None]:
                with self.subTest(k=k,val=val):
                    d=fixture();d['governance'][k]=val;self.assertEqual(calculate(d)['status'],'BLOCKED')
    def test_invalid_fraction(self):
        d=fixture();d['parameters']['steady_adoption_fraction']['value']='1.01'
        with self.assertRaises(InputError):calculate(d)
    def test_invalid_volume(self):
        for value in ['180001','1.5']:
            d=fixture();d['parameters']['unique_eligible_annual_cases']['value']=value
            with self.assertRaises(InputError):calculate(d)
    def test_population_burden_cap(self):
        d=fixture();d['parameters']['baseline_bundle_minutes']['value']='1000'
        with self.assertRaises(InputError):calculate(d)
    def test_nonfinite_negative_float_and_malformed(self):
        for value in ['NaN','Infinity','-1','1e2',1.2,True,{},'']:
            d=fixture();d['parameters']['baseline_bundle_minutes']['value']=value
            with self.subTest(value=value),self.assertRaises(InputError):calculate(d)
    def test_unknown_value_must_be_null(self):
        d=fixture();d['parameters']['baseline_bundle_minutes']['status']='UNKNOWN'
        with self.assertRaises(InputError):calculate(d)
    def test_year_one_cannot_exceed_steady(self):
        d=fixture();d['parameters']['year1_adoption_fraction']['value']='0.6'
        with self.assertRaises(InputError):calculate(d)
    def test_wrong_unit(self):
        d=fixture();d['parameters']['baseline_bundle_minutes']['unit']='business days'
        with self.assertRaises(InputError):calculate(d)
    def test_extra_benefit_or_duplicate_bundle_rejected(self):
        for key,val in [('invented_soft_savings','10000'),('bundle_opportunity_ids',['O01','O01','O05'])]:
            d=fixture();d[key]=val
            with self.assertRaises(InputError):calculate(d)
    def test_measured_mode_rejects_illustrative(self):
        d=fixture();d['mode']='MEASURED_INPUTS'
        with self.assertRaises(InputError):calculate(d)
    def test_unverifiable_provenance_rejected(self):
        for ref in ['NO_SOURCE',{}]:
            d=fixture();d['parameters']['baseline_bundle_minutes']['source_ref']=ref
            with self.assertRaises(InputError):calculate(d)
    def test_review_reference_required(self):
        d=fixture();d['governance']['review_ref']=None;self.assertEqual(calculate(d)['status'],'BLOCKED')
    def test_measured_inputs_still_conditional(self):
        d=fixture();d['mode']='MEASURED_INPUTS';d['evidence_registry'].append({'id':'SIMULATED_MEASURED','kind':'PILOT_MEASUREMENT','description':'Test of acceptance contract, no actual pilot data.'})
        for p in d['parameters'].values():p.update(status='PILOT_MEASURED',source_ref='SIMULATED_MEASURED')
        self.assertEqual(calculate(d)['status'],'CONDITIONAL_SCENARIO')
    def test_output_deterministic(self):self.assertEqual(calculate(fixture()),calculate(fixture()))
    def test_cash_and_capacity_not_added(self):
        r=calculate(fixture())['steady_state'];self.assertEqual(Decimal(r['realizable_labor_cash_benefit_usd'])+Decimal(r['remaining_noncash_capacity_value_usd']),Decimal(r['net_capacity_value_usd']))
class WorkflowTests(unittest.TestCase):
    def test_thresholds(self):
        for amount,role in [('9999.99','AP Analyst'),('10000','AP Team Lead'),('49999.99','AP Team Lead'),('50000.01','AP Manager'),('250000','AP Manager'),('250000.01','Finance Director')]:
            c=case();c['original_disputed_amount_usd']=amount;r=assess(c);self.assertEqual(r['candidate_monetary_approval_role'],role);self.assertFalse(r['approved']);self.assertFalse(r['financial_execution_allowed'])
    def test_50000_holds(self):
        c=case();c['original_disputed_amount_usd']='50000';r=assess(c);self.assertIn('HOLD_FOR_POLICY_CLARIFICATION',r['reasons']);self.assertIsNone(r['candidate_monetary_approval_role'])
    def test_solara_holds(self):
        c=case();c['solara_2026_freight']=True;r=assess(c);self.assertIn('SOLARA_C1_UNRESOLVED',r['reasons']);self.assertIn('Procurement / Legal',r['owners'])
    def test_apex_scope_holds(self):
        c=case();c.update(original_disputed_amount_usd='48088.38',disputed_scope_reconciled=False);self.assertIn('DISPUTED_COMPONENT_SCOPE_UNRECONCILED',assess(c)['reasons'])
    def test_partial_amount_does_not_lower_role(self):
        c=case();c.update(original_disputed_amount_usd='60000',accepted_amount='9000');self.assertEqual(assess(c)['candidate_monetary_approval_role'],'AP Manager')
    def test_unknowns_hold(self):self.assertEqual(assess({})['status'],'HOLD_AND_ESCALATE')
    def test_risk_tax_and_analyst_override(self):
        c=case();c.update(material_risk=True,tax_ambiguous=True,analyst_requests_escalation=True);r=assess(c);self.assertEqual(len(r['reasons']),3);self.assertFalse(r['approved'])
    def test_northstar_consultation(self):
        c=case();c['northstar_consultation_required']=True;self.assertIn('NORTHSTAR_CONSULTATION_REQUIRED',assess(c)['reasons'])
    def test_policy_and_currency_hold(self):
        c=case();c.update(policy_version_verified=False,usd_basis_verified=False);self.assertEqual(len(assess(c)['reasons']),2)
    def test_no_human_decision_granted(self):self.assertEqual(assess(case())['status'],'READY_FOR_AUTHORIZED_HUMAN_DECISION');self.assertFalse(assess(case())['approved'])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    output={'scope':'Deterministic software tests and read-only guard simulation; invented test inputs are not business assumptions.','tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),'llm_benchmark_run':False,'pilot_run':False}
    (R/'test_results.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    demo=calculate(fixture());(R/'tests').mkdir(exist_ok=True)
    (R/'tests/synthetic_arithmetic_fixture.json').write_text(json.dumps(fixture(),indent=2)+'\n',encoding='utf-8')
    (R/'tests/synthetic_arithmetic_expected_output.json').write_text(json.dumps(demo,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
