import sys,unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'workbench'))
from workbench import build_case,reviewed_state

class DemoTests(unittest.TestCase):
    def test_all_cases_render_offline_and_hold(self):
        app=AppTest.from_file(str(ROOT/'demo/app.py'),default_timeout=20).run()
        self.assertFalse(app.exception)
        for p in sorted((ROOT/'source_pack/06_Unstructured_Case_Evidence').glob('*.md')):
            app.sidebar.selectbox[0].select(p.stem).run()
            self.assertFalse(app.exception,p.stem)
            self.assertTrue(any('Live generation unavailable' in x.value for x in app.info))
            self.assertEqual(reviewed_state(build_case(p.stem))['status'],'HOLD_AND_ESCALATE')
    def test_blank_review_is_rejected(self):
        app=AppTest.from_file(str(ROOT/'demo/app.py'),default_timeout=20).run()
        app.button[0].click().run()
        self.assertTrue(any('Reviewer label required' in x.value for x in app.error))
        self.assertFalse(app.exception)
if __name__=='__main__':unittest.main()
