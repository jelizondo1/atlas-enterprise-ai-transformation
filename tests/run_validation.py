"""Run the public software suite and write a compact local verification record."""
from pathlib import Path
import argparse,io,json,sys,unittest
R=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='runs/software_checks.json');a=p.parse_args()
    result=unittest.TextTestRunner(stream=io.StringIO(),verbosity=2).run(unittest.defaultTestLoader.discover(str(R/'tests'),pattern='test_*.py'))
    record={'tests_run':result.testsRun,'passed':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors),'scope':'Deterministic mapping/ROI/authority, read-only workbench, mocked model integration, semantic gating and offline Streamlit tests. No live benchmark.'}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))
    if not result.wasSuccessful():
        for test,error in result.failures+result.errors:print(test,error,file=sys.stderr)
    return 0 if result.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
