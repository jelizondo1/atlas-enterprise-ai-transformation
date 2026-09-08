"""Run only the three approved development cases; prepare structural and semantic artifacts."""
import argparse,os
from datetime import datetime,timezone
from pathlib import Path
from model_runner import run_case,save
from evaluate_run import evaluate,review_template
from summarize_benchmark import summarize

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model',default=os.environ.get('OPENAI_MODEL'));a=p.parse_args()
    if not os.environ.get('OPENAI_API_KEY'):p.error('OPENAI_API_KEY unavailable. Integration ready; live benchmark pending. No requests sent.')
    if not a.model:p.error('Supply --model with an available model ID, or set OPENAI_MODEL. No requests sent.')
    root=Path(__file__).resolve().parents[1]/'runs/live'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    for suffix in ['0018','0139','0184']:
        cid='MRG-2026-'+suffix;d=root/cid;r=run_case(cid,d,a.model,True)
        save(d/'evaluation.json',evaluate(d))
        if r.get('draft') is not None and r['status']=='DRAFT_PENDING_SEMANTIC_REVIEW':save(d/'semantic_review.template.json',review_template(r))
        print(cid,r['status'])
        if r['status'] in {'CREDENTIAL_REQUIRED','CONFIGURATION_REQUIRED','HTTP_ERROR','TRANSPORT_ERROR'}:break
    save(root/'benchmark_summary.json',summarize(root))
    print('Run folder:',root)
if __name__=='__main__':main()
