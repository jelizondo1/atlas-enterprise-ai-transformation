"""Aggregate only LIVE_API attempts; mocks and configuration-only records are excluded."""
import argparse
from pathlib import Path
from collections import Counter
from model_runner import load,save
def summarize(directory):
    records=[load(p) for p in Path(directory).rglob('run.json')]
    live=[r for r in records if r.get('execution_mode')=='LIVE_API' and r.get('provider_attempted') is True]
    ids=[r['run_id'] for r in live]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate run IDs; do not double-count copied results')
    evaluations={}
    for p in Path(directory).rglob('evaluation.json'):
        e=load(p)
        if e['run_id'] in evaluations:raise ValueError('Duplicate evaluation IDs')
        evaluations[e['run_id']]=e
    reviewed=[r for r in live if evaluations.get(r['run_id'],{}).get('status') in {'REVIEW_ACCEPTED','REVIEW_REJECTED'}]
    accepted=[r for r in reviewed if evaluations[r['run_id']]['status']=='REVIEW_ACCEPTED']
    measured_usage=[r['usage'] for r in live if isinstance(r.get('usage'),dict)]
    return {'status':'LIVE_RUNS_RECORDED' if live else 'LIVE_BENCHMARK_NOT_RUN','live_attempts':len(live),
            'excluded_nonlive_or_unsent_records':len(records)-len(live),'status_counts':dict(Counter(r['status'] for r in live)),
            'semantic_reviews_recorded':len(reviewed),'review_coverage':len(reviewed)/len(live) if live else None,
            'accepted_runs':len(accepted),'accepted_over_attempted':len(accepted)/len(live) if live and reviewed else None,
            'accepted_over_reviewed':len(accepted)/len(reviewed) if reviewed else None,
            'runs_with_usage':len(measured_usage),'input_tokens_recorded':sum(u.get('input_tokens',0) for u in measured_usage) if measured_usage else None,
            'output_tokens_recorded':sum(u.get('output_tokens',0) for u in measured_usage) if measured_usage else None,
            'cost_usd':None,'note':'Rates describe recorded local reviewer attestations. Unreviewed/failed attempts are not silently excluded. No dollar pricing or production guarantee inferred.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('runs_directory');p.add_argument('--output',required=True);a=p.parse_args();r=summarize(a.runs_directory);save(a.output,r);print(r['status'])
if __name__=='__main__':main()
