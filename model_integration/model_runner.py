"""Atlas Responses API integration. Dry-run is default; never approves or executes."""
import argparse,hashlib,json,os,sys,time,urllib.request,urllib.error,uuid
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'workbench'))
from workbench import build_case,validate_citation,Rejected
ENDPOINT='https://api.openai.com/v1/responses'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def fingerprint(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def clean_context(case):
    # Deliberately omit curated Day 5 questions, source_holds, reviewer flags and historical decisions.
    return {'case_id':case['case_id'],'case_version_sha256':case['case_version_sha256'],
            'sources':[{'source_id':s['source_id'],'sha256':s['sha256'],'numbered_lines':[{'line':i+1,'text':line} for i,line in enumerate(s['lines'])]} for s in case['sources'].values()]}
def request_payload(case,model,config=None):
    config=config or load(ROOT/'runner_config.json')
    if not isinstance(model,str) or not model.strip():raise Rejected('A model ID must be explicitly configured')
    context=clean_context(case);text=json.dumps(context,ensure_ascii=False)
    if len(text)>config['max_input_characters']:raise Rejected('Input exceeds configured character cap; no silent truncation')
    return {'model':model,'instructions':(ROOT/'generation_prompt.md').read_text(encoding='utf-8'),
            'input':[{'role':'user','content':[{'type':'input_text','text':text}]}],
            'text':{'format':{'type':'json_schema','name':'atlas_evidence_draft','strict':True,'schema':load(ROOT/'draft.schema.json')}},
            'max_output_tokens':config['max_output_tokens'],'store':False,'tools':[]}
def validate_draft(d,case):
    errors=[]
    if not isinstance(d,dict) or set(d)!={'case_id','case_version_sha256','claims','recommended_next_step','suggested_review_owner','uncertainties'}:return ['Draft fields do not match contract']
    if d['case_id']!=case['case_id'] or d['case_version_sha256']!=case['case_version_sha256']:errors.append('Wrong/stale case identity')
    if d['recommended_next_step'] not in {'HUMAN_EVIDENCE_REVIEW','REQUEST_INFORMATION','SPECIALIST_REVIEW'}:errors.append('Invalid next step')
    if not isinstance(d['suggested_review_owner'],str) or not d['suggested_review_owner'].strip():errors.append('Review owner missing')
    if not isinstance(d['uncertainties'],list) or any(not isinstance(x,str) for x in d['uncertainties']):errors.append('Invalid uncertainties')
    if not isinstance(d['claims'],list) or not d['claims']:return errors+['At least one cited claim required']
    if len(d['claims'])>20:errors.append('Too many claims for bounded draft')
    citation_fields={'source_id','source_sha256','line_start','line_end','quote'}
    for claim in d['claims']:
        if not isinstance(claim,dict) or set(claim)!={'kind','text','citations'}:errors.append('Invalid claim fields');continue
        if claim['kind'] not in {'FACT','UNCERTAINTY','REVIEW_QUESTION'} or not isinstance(claim['text'],str) or not claim['text'].strip():errors.append('Invalid claim kind/text')
        citations=claim['citations']
        if not isinstance(citations,list) or not citations:errors.append('Claim lacks citations');continue
        for c in citations:
            if not isinstance(c,dict) or set(c)!=citation_fields or not validate_citation(c,case['sources']):errors.append('Citation source/hash/range/quote invalid')
    return errors
def parse_response(response,case):
    if not isinstance(response,dict):return {'status':'INVALID_PROVIDER_RESPONSE','draft':None,'errors':['Non-object response']}
    if response.get('status')!='completed':return {'status':'PROVIDER_'+str(response.get('status','UNKNOWN')).upper(),'draft':None,'errors':['No completed response; partial output not admitted']}
    texts=[]
    if not isinstance(response.get('output'),list):return {'status':'INVALID_PROVIDER_RESPONSE','draft':None,'errors':['Invalid output collection']}
    for item in response['output']:
        if not isinstance(item,dict) or not isinstance(item.get('content',[]),list):return {'status':'INVALID_PROVIDER_RESPONSE','draft':None,'errors':['Invalid output item']}
        if item.get('type')!='message':continue
        for content in item.get('content',[]):
            if not isinstance(content,dict):return {'status':'INVALID_PROVIDER_RESPONSE','draft':None,'errors':['Invalid content item']}
            if content.get('type')=='refusal':return {'status':'MODEL_REFUSAL','draft':None,'errors':['Refusal; no draft admitted']}
            if content.get('type')=='output_text':texts.append(content.get('text',''))
    if not texts:return {'status':'NO_OUTPUT_TEXT','draft':None,'errors':['No output text']}
    try:draft=json.loads(''.join(texts))
    except (json.JSONDecodeError,TypeError):return {'status':'INVALID_DRAFT_JSON','draft':None,'errors':['Output is not a single JSON draft']}
    errors=validate_draft(draft,case)
    return {'status':'STRUCTURAL_REJECTION' if errors else 'DRAFT_PENDING_SEMANTIC_REVIEW','draft':draft,'errors':errors}
def http_transport(payload,key,timeout):
    request=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
    # A fixed HTTPS endpoint; credentials are never included in saved requests or errors.
    with urllib.request.urlopen(request,timeout=timeout) as response:
        raw=response.read(2_000_001)
        if len(raw)>2_000_000:raise Rejected('Provider response exceeds local size cap')
        return json.loads(raw),response.headers.get('x-request-id')
def run_case(case_id,output,model=None,live=False,transport=None):
    config=load(ROOT/'runner_config.json');case=build_case(case_id)
    model=model or os.environ.get('OPENAI_MODEL') or config['model']
    output=Path(output)
    if output.exists():raise Rejected('Run output already exists; choose a new path to preserve provenance')
    result={'run_id':str(uuid.uuid4()),'case_id':case_id,'case_version_sha256':case['case_version_sha256'],
            'execution_mode':'TEST_TRANSPORT' if transport else 'LIVE_API' if live else 'DRY_RUN',
            'model_requested':model,'model_returned':None,'started_at_utc':datetime.now(timezone.utc).isoformat(),
            'status':None,'request_sha256':None,'prompt_sha256':hashlib.sha256((ROOT/'generation_prompt.md').read_bytes()).hexdigest(),
            'schema_sha256':hashlib.sha256((ROOT/'draft.schema.json').read_bytes()).hexdigest(),
            'context_sha256':fingerprint(clean_context(case)),'latency_seconds':None,'usage':None,
            'response_id':None,'request_id':None,'provider_attempted':False,'errors':[],'draft':None,'approved':False,'financial_execution_allowed':False,'semantic_evaluation_status':'NOT_REVIEWED'}
    if not model:
        result.update(status='CONFIGURATION_REQUIRED',errors=['Set a model ID; no request sent']);save(output/'run.json',result);return result
    payload=request_payload(case,model,config);result['request_sha256']=fingerprint(payload)
    if not live:
        result['status']='DRY_RUN_REQUEST_READY';save(output/'request.json',payload);save(output/'run.json',result);return result
    key=os.environ.get('OPENAI_API_KEY')
    if transport is None and not key:
        result.update(status='CREDENTIAL_REQUIRED',errors=['OPENAI_API_KEY unavailable; no request sent']);save(output/'request.json',payload);save(output/'run.json',result);return result
    save(output/'request.json',payload);started=time.monotonic()
    result['provider_attempted']=True
    try:
        response,request_id=(transport or http_transport)(payload,key,config['timeout_seconds'])
        result.update(parse_response(response,case));result.update(model_returned=response.get('model'),usage=response.get('usage'),response_id=response.get('id'),request_id=request_id)
        save(output/'provider_response.json',response)
    except urllib.error.HTTPError as e:
        result.update(status='HTTP_ERROR',errors=['HTTP '+str(e.code)+'; no automatic retry; response body not logged'])
    except (urllib.error.URLError,TimeoutError,OSError) as e:
        result.update(status='TRANSPORT_ERROR',errors=[type(e).__name__+'; result may be uncertain; no automatic retry'])
    except (Rejected,ValueError,KeyError,TypeError,AttributeError):
        result.update(status='INVALID_PROVIDER_RESPONSE',errors=['Response could not be admitted; no automatic retry'])
    result['latency_seconds']=round(time.monotonic()-started,6)
    save(output/'run.json',result)
    if result['status']=='DRAFT_PENDING_SEMANTIC_REVIEW':
        d=result['draft'];legacy={'case_id':d['case_id'],'case_version_sha256':d['case_version_sha256'],
                'generation_label':result['execution_mode']+' '+str(result['model_returned'] or model)+' '+result['run_id'],
                'claims':[{'text':c['text'],'citations':c['citations']} for c in d['claims']]}
        save(output/'workbench_draft.json',legacy)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cases',nargs='+',required=True);p.add_argument('--model');p.add_argument('--live',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
    cfg=load(ROOT/'runner_config.json')
    if len(a.cases)>cfg['max_cases_per_run'] or len(set(a.cases))!=len(a.cases):p.error('Use at most three distinct cases per bounded run')
    try:
        for c in a.cases:
            r=run_case(c,Path(a.output)/c,a.model,a.live);print(c,r['status'])
            if r['status'] in {'CREDENTIAL_REQUIRED','CONFIGURATION_REQUIRED','HTTP_ERROR','TRANSPORT_ERROR'}:break
    except (Rejected,ValueError) as e:print('REJECTED:',e);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
