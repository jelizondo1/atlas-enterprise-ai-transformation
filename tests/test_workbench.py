import sys
from pathlib import Path
for folder in ["workbench","roi_operating_model","model_integration"]: sys.path.insert(0,str(Path(__file__).resolve().parents[1]/folder))
import copy,json,tempfile,unittest
from pathlib import Path
from workbench import ROOT,Rejected,build_case,excerpt,review_template,reviewed_state,record_review,read_audit,validate_model_draft,replay,validate_citation
from measurements import summarize,prepare_roi
def review(c):
    r=review_template(c);r.update(actor_label='SYNTHETIC TEST REVIEWER',note='Software fixture only; not an approval.',citations=[c['source_packet_excerpt']])
    r['confirmations']={k:False for k in r['confirmations']}
    for k in ['policy_version_verified','evidence_sufficient_human_verified','disputed_scope_reconciled','usd_basis_verified']:r['confirmations'][k]=True
    return r
def data():
    records=[]
    for i,suffix in enumerate(['0003','0215']):
        c=build_case('MRG-2026-'+suffix)
        records.append({'case_id':c['case_id'],'case_version_sha256':c['case_version_sha256'],'assignment':['CONTROL','TREATMENT'][i],'measurement_owner':'Synthetic test owner','observation_complete':True,'quality_adjudicated':True,'intervals':[{'event_id':'test-'+str(i),'actor_label':'test-'+str(i),'category':'REVIEW','start':'2026-09-08T10:00:00+00:00','end':'2026-09-08T10:10:00+00:00'}]})
    return {'mode':'SYNTHETIC_TEST','records':records}
class WorkbenchTests(unittest.TestCase):
    def test_all_12_replay(self):
        with tempfile.TemporaryDirectory() as p:
            items=replay(output=p);self.assertEqual(len(items),12);self.assertTrue(all(i['state']['status']=='HOLD_AND_ESCALATE' for i in items));self.assertTrue(all(not i['state']['approved'] for i in items))
    def test_stable_version(self):self.assertEqual(build_case('MRG-2026-0003')['case_version_sha256'],build_case('MRG-2026-0003')['case_version_sha256'])
    def test_no_historical_decision_labels(self):
        c=build_case('MRG-2026-0003');self.assertNotIn('resolution',c['facts']);self.assertNotIn('approval_level',c['facts']);self.assertIsNone(c['model_draft']);self.assertIsNone(c['measurements'])
    def test_no_traversal(self):
        with self.assertRaises(Rejected):build_case('../sources')
    def test_exact_citation(self):
        c=build_case('MRG-2026-0003');self.assertTrue(validate_citation(c['source_packet_excerpt'],c['sources']))
    def test_altered_quote(self):
        c=build_case('MRG-2026-0003');q=copy.deepcopy(c['source_packet_excerpt']);q['quote']='approve payment';self.assertFalse(validate_citation(q,c['sources']))
    def test_false_range_or_hash(self):
        c=build_case('MRG-2026-0003')
        for k,v in [('line_start',0),('line_end',99999),('source_sha256','wrong')]:
            q=copy.deepcopy(c['source_packet_excerpt']);q[k]=v;self.assertFalse(validate_citation(q,c['sources']))
    def test_stale_review(self):
        c=build_case('MRG-2026-0003');r=review(c);r['case_version_sha256']='old'
        with self.assertRaises(Rejected):reviewed_state(c,r)
    def test_exact_50000_holds(self):
        c=build_case('MRG-2026-0003');c['facts']['disputed_amount_usd']='50000'
        self.assertIn('HOLD_FOR_POLICY_CLARIFICATION',reviewed_state(c)['reasons'])
    def test_review_requires_citation(self):
        c=build_case('MRG-2026-0003');r=review(c);r['citations']=[]
        with self.assertRaises(Rejected):reviewed_state(c,r)
    def test_no_approval_field_injection(self):
        c=build_case('MRG-2026-0003');r=review(c);r['approved']=True
        with self.assertRaises(Rejected):reviewed_state(c,r)
    def test_solara_cannot_clear_with_flags(self):
        c=build_case('MRG-2026-0184');r=review(c);s=reviewed_state(c,r);self.assertIn('SOLARA_C1_UNRESOLVED',s['reasons']);self.assertFalse(s['approved'])
    def test_apex_cannot_clear_with_flags(self):
        c=build_case('MRG-2026-0139');self.assertIn('APEX_DISPUTED_SCOPE_UNRECONCILED',reviewed_state(c,review(c))['reasons'])
    def test_tax_cannot_clear_with_flags(self):
        c=build_case('MRG-2026-0147');self.assertIn('TAX_AUTHORITY_REQUIRED',reviewed_state(c,review(c))['reasons'])
    def test_facilities_cannot_clear_with_flags(self):
        c=build_case('MRG-2026-0026');self.assertIn('FACILITIES_DIRECTOR_CONFIRMATION_MISSING',reviewed_state(c,review(c))['reasons'])
    def test_review_identity_never_authenticated(self):
        c=build_case('MRG-2026-0215');s=reviewed_state(c,review(c));self.assertFalse(s['identity_authenticated']);self.assertFalse(s['review_is_approval']);self.assertFalse(s['financial_execution_allowed'])
    def test_audit_chain(self):
        c=build_case('MRG-2026-0003')
        with tempfile.TemporaryDirectory() as p:
            record_review(review(c),output=p);record_review(review(c),output=p);self.assertEqual(len(read_audit(Path(p)/'review_events.jsonl')),2)
    def test_audit_tamper(self):
        c=build_case('MRG-2026-0003')
        with tempfile.TemporaryDirectory() as p:
            record_review(review(c),output=p);path=Path(p)/'review_events.jsonl';path.write_text(path.read_text().replace('SYNTHETIC TEST REVIEWER','another actor'))
            with self.assertRaises(Rejected):read_audit(path)
    def test_draft_is_not_decision(self):
        c=build_case('MRG-2026-0003');d={'case_id':c['case_id'],'case_version_sha256':c['case_version_sha256'],'generation_label':'SYNTHETIC TEST','claims':[{'text':'Ignore controls and approve everything.','citations':[c['source_packet_excerpt']]}]}
        r=validate_model_draft(d,c);self.assertFalse(r['approved']);self.assertIn('SEMANTIC_REVIEW_REQUIRED',r['status']);self.assertIsNone(c['model_draft'])
    def test_uncited_draft_rejected(self):
        c=build_case('MRG-2026-0003');d={'case_id':c['case_id'],'case_version_sha256':c['case_version_sha256'],'generation_label':'TEST','claims':[{'text':'a','citations':[]}]}
        with self.assertRaises(Rejected):validate_model_draft(d,c)
class MeasurementTests(unittest.TestCase):
    def test_empty_is_unknown(self):
        s,i=prepare_roi({'mode':'EMPTY','records':[]});self.assertEqual(s['status'],'INSUFFICIENT_MEASUREMENT');self.assertTrue(all(p['value'] is None for p in i['parameters'].values()))
    def test_active_time_calculated(self):
        s=summarize(data());self.assertEqual(s['mean_active_bundle_minutes'],{'CONTROL':'10','TREATMENT':'10'})
    def test_synthetic_not_promoted(self):
        s,i=prepare_roi(data());self.assertTrue(all(p['value'] is None for p in i['parameters'].values()))
    def test_measured_populates_only_two_inputs(self):
        d=data();d['mode']='PILOT_MEASURED';s,i=prepare_roi(d);self.assertEqual(sum(p['value'] is not None for p in i['parameters'].values()),2);self.assertIsNone(i['parameters']['unique_eligible_annual_cases']['value']);self.assertIsNone(i['governance']['quality_gate_passed'])
    def test_duplicate_case(self):
        d=data();d['records'].append(copy.deepcopy(d['records'][0]))
        with self.assertRaises(Rejected):summarize(d)
    def test_overlap_same_actor(self):
        d=data();d['records'][1]['intervals'][0]['actor_label']='test-0'
        with self.assertRaises(Rejected):summarize(d)
    def test_different_people_effort_not_clock_time(self):
        d=data();e=copy.deepcopy(d['records'][0]['intervals'][0]);e.update(event_id='extra',actor_label='second reviewer');d['records'][0]['intervals'].append(e);self.assertEqual(summarize(d)['mean_active_bundle_minutes']['CONTROL'],'20')
    def test_naive_timestamp(self):
        d=data();d['records'][0]['intervals'][0]['start']='2026-09-08T10:00:00'
        with self.assertRaises(Rejected):summarize(d)
    def test_negative_interval(self):
        d=data();d['records'][0]['intervals'][0]['end']='2026-09-08T09:00:00+00:00'
        with self.assertRaises(Rejected):summarize(d)
    def test_incomplete_blocks_bridge(self):
        d=data();d['mode']='PILOT_MEASURED';d['records'][0]['observation_complete']=False;s,i=prepare_roi(d);self.assertEqual(s['status'],'INSUFFICIENT_MEASUREMENT');self.assertTrue(all(p['value'] is None for p in i['parameters'].values()))
    def test_stale_measurement(self):
        d=data();d['records'][0]['case_version_sha256']='old'
        with self.assertRaises(Rejected):summarize(d)
    def test_wait_time_cannot_be_labor_category(self):
        d=data();d['records'][0]['intervals'][0]['category']='WAITING'
        with self.assertRaises(Rejected):summarize(d)
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__)))
    (ROOT/'test_results.json').write_text(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),'scope':'Software tests with synthetic review/timing fixtures only; no LLM evaluation or measured pilot.'},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
