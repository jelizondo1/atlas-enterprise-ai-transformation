"""Reproducible public package checks; read-only unless --report is supplied."""
import argparse,csv,hashlib,json,re,sys
from pathlib import Path
from decimal import Decimal
from urllib.parse import unquote
from jsonschema import Draft202012Validator
R=Path(__file__).resolve().parents[1]
for folder in ['workbench','model_integration','roi_operating_model']:sys.path.insert(0,str(R/folder))
from workbench import build_case,reviewed_state
from model_runner import request_payload,clean_context

def checks():
    results=[]
    def check(name,ok):results.append({'check':name,'pass':bool(ok)})
    load=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
    for x in load('docs/provenance.json'):
        p=R/x['public_file']
        check('Public lineage '+x['public_file'],p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==x['public_sha256'])
        if x['public_file'].startswith('source_pack/') and not x['public_file'].endswith('/README.md'):
            check('Original source bytes '+x['public_file'],x['original_sha256']==x['public_sha256'])
    for x in load('source_manifest.json')['files']:
        p=(R/x['file']).resolve()
        check('Source integrity '+x['file'],p.is_relative_to(R) and p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'])
    m=load('opportunity_mapping/meridian_opportunity_map_final.json')
    check('Opportunity map schema',not list(Draft202012Validator(load('opportunity_mapping/atlas_opportunity_map.schema.json')).iter_errors(m)))
    for s in m['sources']:
        p=R/s['file'];ok=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256']
        if ok and s.get('json_pointer'):
            try:
                v=json.loads(p.read_text(encoding='utf-8'))
                for bit in s['json_pointer'].strip('/').split('/'):
                    bit=bit.replace('~1','/').replace('~0','~');v=v[int(bit)] if isinstance(v,list) else v[bit]
            except (KeyError,IndexError,ValueError):ok=False
        check('Opportunity source '+s['id'],ok)
    for schema,data in [('roi_input.schema.json','meridian_roi_inputs.json'),('roi_output.schema.json','meridian_roi_results.json')]:
        check('ROI schema '+data,not list(Draft202012Validator(load('roi_operating_model/'+schema)).iter_errors(load('roi_operating_model/'+data))))
    for p in sorted((R/'source_pack/06_Unstructured_Case_Evidence').glob('*.md')):
        c=build_case(p.stem);payload=request_payload(c,'PACKAGE_TEST_NO_NETWORK');context=clean_context(c)
        check('Isolated context '+p.stem,set(context)=={'case_id','case_version_sha256','sources'} and all(set(s)=={'source_id','sha256','numbered_lines'} for s in context['sources']))
        check('Safe request '+p.stem,payload['tools']==[] and payload['store'] is False and payload['max_output_tokens']==4096)
        check('Fail closed '+p.stem,reviewed_state(c)['status']=='HOLD_AND_ESCALATE' and c['model_draft'] is None and not c['financial_execution_allowed'])
    rows=list(csv.DictReader((R/'source_pack/meridian_disputes_250.csv').open(encoding='utf-8')))
    q=load('diagnostics/meridian_quantitative_diagnostics.json')['overall']
    mean=sum(Decimal(x['handling_minutes']) for x in rows)/len(rows)
    check('250 rows and exact handling mean',len(rows)==250 and mean==Decimal(str(q['avg_handling_minutes'])))
    check('Exact annualized active hours',mean*180000/60==71952)
    check('Team cost is context',load('impact_sizing/meridian_annualized_impact_sizing.json')['overall_current_state']['annual_dispute_team_cost_usd']==4420000)
    check('Actual ROI remains unknown',all(v['value'] is None for v in load('roi_operating_model/meridian_roi_inputs.json')['parameters'].values()))
    check('Featured case supplier source match',build_case('MRG-2026-0018')['facts']['supplier_name']=='Apex Industrial Supply' and build_case('MRG-2026-0139')['facts']['supplier_name']=='Apex Industrial Supply' and build_case('MRG-2026-0184')['facts']['supplier_name']=='Solara Imports')
    cfg=load('model_integration/runner_config.json')
    check('Bounded timeout and batch',cfg['timeout_seconds']==60 and cfg['max_cases_per_run']==3)
    for p in R.rglob('*.md'):
        s=p.read_text(encoding='utf-8')
        for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
            if target.startswith(('http:','https:','#','mailto:')):continue
            target=unquote(target.split('#')[0])
            check('Local link '+p.relative_to(R).as_posix()+' -> '+target,(p.parent/target).exists())
    prohibited=[]
    files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['__pycache__','runs','.venv','.git'])]
    for p in files:
        if p.suffix in ['.zip','.log','.pyc','.xlsx'] or p.name in ['.env','secrets.toml'] or 'evaluation_only' in p.parts:prohibited.append(p.relative_to(R).as_posix())
        if p.suffix in ['.py','.md','.json','.csv','.txt','.toml']:
            s=p.read_text(encoding='utf-8')
            # Literal patterns are assembled to avoid matching this scanner's own source.
            pats=[r'[A-Za-z]:'+r'[\\/](?:Users|home|Windows)[\\/]',r'/(?:home|mnt/data|Users)/',r'\bsk'+r'-[A-Za-z0-9_-]{20,}',r'-----BEGIN '+r'(?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
            if any(re.search(pattern,s) for pattern in pats):prohibited.append(p.relative_to(R).as_posix())
    check('Secret and machine-path scan',not prohibited)
    check('No generated runtime files selected',not any(p.name in ['run.json','provider_response.json','request.json','test_results.json'] for p in files))
    return {'checks':results,'checks_run':len(results),'passed':all(x['pass'] for x in results),'failed':[x for x in results if not x['pass']],'scrub_findings':prohibited,'scope':'Static public package, source lineage, schemas, arithmetic, offline boundaries and local documentation links; no live model claims.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--report');a=p.parse_args();r=checks()
    if a.report:Path(a.report).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in r.items() if k!='checks'},indent=2));return 0 if r['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
