"""Authored-map validator regression tests; no model benchmark or hidden labels."""
import unittest,copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'opportunity_mapping'))
from validate_map import validate
BASE=json.loads((R/'opportunity_mapping/meridian_opportunity_map_final.json').read_text(encoding='utf-8'))
mutations=[
('llm_financial_execution',lambda x:x['opportunities'][0]['controls'].update(llm_can_execute_financial_action=True)),
('llm_calculation',lambda x:x['opportunities'][5]['controls'].update(calculation_executor='LLM')),
('model_approval',lambda x:x['opportunities'][8]['controls'].update(approval_decision_owner='LLM')),
('no_human_hold',lambda x:x['opportunities'][7]['controls'].update(ambiguous_or_high_risk_action='AUTO_RESOLVE')),
('invented_savings',lambda x:x['opportunities'][0]['impact'].update(annual_savings_hours=9000)),
('broken_reference',lambda x:x['opportunities'][0].update(source_refs=['INVENTED'])),
('no_hybrid_decomposition',lambda x:x['opportunities'][0].update(components=['LLM'])),
('rounded_reopen_error',lambda x:x['burden_lenses'][0].update(associated_hours_unrounded=7938)),
('solara_model_decision',lambda x:x['opportunities'][7]['components'].append('LLM')),
('partial_amount_authority',lambda x:x['opportunities'][8].update(proposed_intervention='Route on accepted portion.')),
('false_production_status',lambda x:x.update(status='PRODUCTION_APPROVED')),
('duplicate_opportunity',lambda x:x['opportunities'].append(copy.deepcopy(x['opportunities'][0]))),
('broken_json_pointer',lambda x:x['sources'][4].update(json_pointer='/nonexistent')),
('wrong_evidence_type',lambda x:x['diagnoses'][1].update(evidence_type='DIRECT')),
('wrong_precise_baseline',lambda x:x['baseline'].update(annual_handling_hours_precise=72000)),
('no_threshold_hold',lambda x:x['opportunities'][8].update(prohibited_action='Resolve threshold by confidence.')),
('no_apex_reconciliation',lambda x:x['opportunities'][5].update(prohibited_action='Pay supported components.')),
('source_tamper',lambda x:x['sources'][0].update(sha256='0'*64)),
('wrong_diagnosis_link',lambda x:x['opportunities'][0].update(diagnosis_refs=['F2'])),
('evaluation_leakage',lambda x:x['sources'][0].update(file='evaluation_only/private_expected_answers.json'))]

class MappingTests(unittest.TestCase):
    def test_authoritative_map_validates(self):self.assertEqual(validate(BASE),[])
def make_test(mutation):
    def test(self):
        candidate=copy.deepcopy(BASE);mutation(candidate);self.assertTrue(validate(candidate))
    return test
for name,mutation in mutations:setattr(MappingTests,'test_reject_'+name,make_test(mutation))
if __name__=='__main__':unittest.main()
