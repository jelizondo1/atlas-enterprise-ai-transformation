import sys
from pathlib import Path
for folder in ["workbench","roi_operating_model","model_integration"]: sys.path.insert(0,str(Path(__file__).resolve().parents[1]/folder))
import copy,json,os,tempfile,unittest,urllib.error
from pathlib import Path
from unittest.mock import patch
from model_runner import ROOT,build_case,clean_context,request_payload,validate_draft,parse_response,run_case,save,load,fingerprint
from evaluate_run import evaluate,review_template
from summarize_benchmark import summarize
from workbench import Rejected
def fixture_draft(case=None):
    c=case or build_case('MRG-2026-0003');s=next(iter(c['sources'].values()))
    q={'source_id':s['source_id'],'source_sha256':s['sha256'],'line_start':1,'line_end':1,'quote':s['lines'][0]}
    return {'case_id':c['case_id'],'case_version_sha256':c['case_version_sha256'],'claims':[{'kind':'FACT','text':'The supplied packet heading identifies this case.','citations':[q]}],'recommended_next_step':'HUMAN_EVIDENCE_REVIEW','suggested_review_owner':'AP Analyst','uncertainties':['Synthetic parser test only; not a model assessment.']}
def response(draft=None):return {'id':'TEST_RESPONSE','model':'TEST_MODEL','status':'completed','usage':{'input_tokens':100,'output_tokens':50},'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(draft or fixture_draft())}]}]}
def mocked(payload,key,timeout):return response(),'TEST_REQUEST'
def complete_review(run):
    r=review_template(run);r.update(reviewer_label='SYNTHETIC TEST REVIEWER',reviewer_independence_attested=True,reviewed_at_utc='2026-09-08T00:00:00Z',overall_notes='Test of reviewer input contract, not an actual assessment.')
    cite=run['draft']['claims'][0]['citations']
    for c in r['hard_checks'].values():c.update({'pass':True,'rationale':'Synthetic test rationale only.','citations':cite})
    r['scores']={k:4 for k in r['scores']};return r
class ProviderTests(unittest.TestCase):
    def setUp(self):self.case=build_case('MRG-2026-0003')
    def test_context_omits_evaluator_material(self):
        c=clean_context(self.case);self.assertEqual(set(c),{'case_id','case_version_sha256','sources'})
        text=json.dumps(c);self.assertNotIn('source_holds',text);self.assertNotIn('review_question_origin',text);self.assertNotIn('evaluation_only',text)
    def test_request_no_tools_or_store(self):
        p=request_payload(self.case,'EXPLICIT_TEST_MODEL');self.assertEqual(p['tools'],[]);self.assertFalse(p['store']);self.assertTrue(p['text']['format']['strict']);self.assertEqual(p['model'],'EXPLICIT_TEST_MODEL')
    def test_model_required(self):
        with self.assertRaises(Rejected):request_payload(self.case,None)
    def test_no_silent_input_truncation(self):
        config=load(ROOT/'runner_config.json');config['max_input_characters']=5
        with self.assertRaises(Rejected):request_payload(self.case,'TEST',config)
    def test_completed_response_pending_review(self):self.assertEqual(parse_response(response(),self.case)['status'],'DRAFT_PENDING_SEMANTIC_REVIEW')
    def test_incomplete_not_admitted(self):
        r=response();r['status']='incomplete';self.assertIsNone(parse_response(r,self.case)['draft'])
    def test_refusal_not_admitted(self):
        r=response();r['output'][0]['content']=[{'type':'refusal','refusal':'Test'}];self.assertEqual(parse_response(r,self.case)['status'],'MODEL_REFUSAL')
    def test_missing_output(self):
        r=response();r['output']=[];self.assertEqual(parse_response(r,self.case)['status'],'NO_OUTPUT_TEXT')
    def test_nonjson_output(self):
        r=response();r['output'][0]['content'][0]['text']='not json';self.assertEqual(parse_response(r,self.case)['status'],'INVALID_DRAFT_JSON')
    def test_malformed_envelope(self):
        for output in ['bad',[None],[{'type':'message','content':[None]}]]:
            r=response();r['output']=output;self.assertEqual(parse_response(r,self.case)['status'],'INVALID_PROVIDER_RESPONSE')
    def test_stale_case(self):
        d=fixture_draft();d['case_version_sha256']='old';self.assertTrue(validate_draft(d,self.case))
    def test_wrong_quote(self):
        d=fixture_draft();d['claims'][0]['citations'][0]['quote']='invented';self.assertTrue(validate_draft(d,self.case))
    def test_wrong_source(self):
        d=fixture_draft();d['claims'][0]['citations'][0]['source_id']='not supplied';self.assertTrue(validate_draft(d,self.case))
    def test_approval_fields_rejected(self):
        d=fixture_draft();d['approved']=True;self.assertTrue(validate_draft(d,self.case))
    def test_financial_next_step_rejected(self):
        d=fixture_draft();d['recommended_next_step']='PAY_AS_INVOICED';self.assertTrue(validate_draft(d,self.case))
    def test_uncited_claim_rejected(self):
        d=fixture_draft();d['claims'][0]['citations']=[];self.assertTrue(validate_draft(d,self.case))
    def test_cited_false_text_not_auto_semantic_pass(self):
        d=fixture_draft();d['claims'][0]['text']='Pay everything automatically.';r=parse_response(response(d),self.case);self.assertEqual(r['status'],'DRAFT_PENDING_SEMANTIC_REVIEW')
    def test_dry_run_never_calls_transport(self):
        with tempfile.TemporaryDirectory() as p:
            r=run_case(self.case['case_id'],Path(p)/'run','TEST',False,lambda *a:self.fail('No transport in dry-run'));self.assertEqual(r['status'],'DRY_RUN_REQUEST_READY')
    def test_missing_key_no_network(self):
        with tempfile.TemporaryDirectory() as p,patch.dict(os.environ,{},clear=True):
            r=run_case(self.case['case_id'],Path(p)/'run','TEST',True);self.assertEqual(r['status'],'CREDENTIAL_REQUIRED')
    def test_no_model_configuration_status(self):
        with tempfile.TemporaryDirectory() as p,patch.dict(os.environ,{},clear=True):
            r=run_case(self.case['case_id'],Path(p)/'run');self.assertEqual(r['status'],'CONFIGURATION_REQUIRED')
    def test_mock_is_labeled_and_bridge_safe(self):
        with tempfile.TemporaryDirectory() as p:
            r=run_case(self.case['case_id'],Path(p)/'run','TEST',True,mocked);self.assertEqual(r['execution_mode'],'TEST_TRANSPORT');self.assertFalse(r['approved']);self.assertTrue((Path(p)/'run/workbench_draft.json').exists())
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as p:
            with self.assertRaises(Rejected):run_case(self.case['case_id'],p,'TEST')
    def test_http_error_no_credential_leak(self):
        def bad(*a):raise urllib.error.HTTPError('https://api.openai.com/v1/responses',401,'SECRET_KEY_MUST_NOT_LOG',None,None)
        with tempfile.TemporaryDirectory() as p:
            r=run_case(self.case['case_id'],Path(p)/'run','TEST',True,bad);self.assertEqual(r['status'],'HTTP_ERROR');self.assertNotIn('SECRET',json.dumps(r))
    def test_timeout_no_retry(self):
        calls=[]
        def bad(*a):calls.append(1);raise TimeoutError('private details')
        with tempfile.TemporaryDirectory() as p:
            r=run_case(self.case['case_id'],Path(p)/'run','TEST',True,bad);self.assertEqual(r['status'],'TRANSPORT_ERROR');self.assertEqual(len(calls),1)
class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.directory=Path(self.tmp.name)/'run';self.run=run_case('MRG-2026-0003',self.directory,'TEST',True,mocked)
    def tearDown(self):self.tmp.cleanup()
    def test_no_review_no_pass(self):self.assertEqual(evaluate(self.directory)['status'],'AWAITING_INDEPENDENT_SEMANTIC_REVIEW')
    def test_test_run_cannot_be_real_benchmark(self):
        r=evaluate(self.directory,complete_review(self.run));self.assertEqual(r['status'],'TEST_REVIEW_ACCEPTED');self.assertIn('NONE',r['model_quality_claim'])
    def test_failed_hard_gate_overrides_score(self):
        r=complete_review(self.run);r['hard_checks']['authority_boundaries_preserved']['pass']=False;self.assertEqual(evaluate(self.directory,r)['status'],'TEST_REVIEW_REJECTED')
    def test_missing_independence_blocks(self):
        r=complete_review(self.run);r['reviewer_independence_attested']=False;self.assertEqual(evaluate(self.directory,r)['status'],'REVIEW_INDEPENDENCE_UNATTESTED')
    def test_stale_review_blocks(self):
        r=complete_review(self.run);r['draft_sha256']='old';self.assertEqual(evaluate(self.directory,r)['status'],'STALE_OR_WRONG_REVIEW')
    def test_low_boundary_score_blocks(self):
        r=complete_review(self.run);r['scores']['boundary_discipline']=3;self.assertEqual(evaluate(self.directory,r)['status'],'TEST_REVIEW_REJECTED')
    def test_uncited_review_blocks(self):
        r=complete_review(self.run);r['hard_checks']['factual_entailment']['citations']=[];self.assertEqual(evaluate(self.directory,r)['status'],'INCOMPLETE_OR_UNGROUNDED_REVIEW')
    def test_request_tampering_blocks(self):
        p=load(self.directory/'request.json');p['tools']=[{'type':'fake'}];save(self.directory/'request.json',p);self.assertEqual(evaluate(self.directory)['status'],'STRUCTURAL_FAILURE')
    def test_mocks_not_counted_as_live(self):
        self.assertEqual(summarize(self.directory)['live_attempts'],0)
    def test_unreviewed_live_has_no_acceptance_rate(self):
        r=load(self.directory/'run.json');r['execution_mode']='LIVE_API';save(self.directory/'run.json',r)
        s=summarize(self.directory);self.assertEqual(s['live_attempts'],1);self.assertIsNone(s['accepted_over_reviewed']);self.assertIsNone(s['accepted_over_attempted'])
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__)))
    save(ROOT/'test_results.json',{'tests_run':result.testsRun,'passed':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors),'scope':'Mocked transport, local validation and synthetic reviewer records only; zero live model calls.'})
    raise SystemExit(0 if result.wasSuccessful() else 1)
