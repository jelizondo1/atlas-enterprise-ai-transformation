"""Atlas read-only case workbench. No network, LLM inference or financial execution."""
import argparse,csv,hashlib,json,re,sys
import os
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'roi_operating_model'))
from workflow_guards import assess

class Rejected(ValueError):pass
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def save(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def verify_sources(root=ROOT):
    for x in load(root/'source_manifest.json')['files']:
        p=(root/x['file']).resolve()
        if not p.is_relative_to(root.resolve()) or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:raise Rejected('Source integrity failed: '+x['file'])
def source_record(relative,root=ROOT):
    p=root/relative;text=p.read_text(encoding='utf-8')
    return {'source_id':relative,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':text.splitlines()}
def excerpt(source,start,end):
    return {'source_id':source['source_id'],'source_sha256':source['sha256'],'line_start':start,'line_end':end,'quote':'\n'.join(source['lines'][start-1:end])}
def validate_citation(c,sources):
    try:
        s=sources[c['source_id']];a=c['line_start'];b=c['line_end']
        return type(a) is int and type(b) is int and 1<=a<=b<=len(s['lines']) and c['source_sha256']==s['sha256'] and c['quote']=='\n'.join(s['lines'][a-1:b])
    except (KeyError,TypeError):return False

# Curated design questions from visible case packets, not evaluator answer keys.
QUESTIONS={
'0003':'Verify Phoenix-origin freight amendment applicability and support before disposition.',
'0018':'Obtain current executed surcharge terms; prior paid cases cannot resolve conflicting amendments.',
'0022':'Verify authorized Receiving confirmation and documented outage exception; absence of posted receipt alone is not non-delivery.',
'0026':'Obtain required Facilities Director written confirmation; supplier/store-manager statements do not substitute for the agreement requirement.',
'0139':'Reconcile original disputed scope of $48,088.38 with the $75,000 component listing before calculation/routing.',
'0143':'Verify domestic Mexico scope against the agreement; do not apply cross-border amendment indiscriminately.',
'0147':'Tax must resolve the uncertain cross-border withholding treatment; historical payment is not authority.',
'0159':'Verify NorthStar contractual 120-day window instead of applying the generic 90-day rule.',
'0168':'Verify promotional scope, shipment date, units and disputed-amount relationship before any adjustment.',
'0184':'Procurement / Legal must establish governing 2026 freight terms; do not apply the unsigned 4% draft.',
'0213':'Compare goods, POs, amount and entity; repeated invoice number alone does not establish a duplicate.',
'0215':'Verify Apex consumables tolerance conditions, accepted receipt, unchanged unit price and incremental amount.'}
KNOWN_HOLDS={'0018':('CONTRACT_AMENDMENT_CONFLICT','Procurement / Legal'),'0026':('FACILITIES_DIRECTOR_CONFIRMATION_MISSING','Facilities Director'),'0139':('APEX_DISPUTED_SCOPE_UNRECONCILED','AP Analyst / case owner'),'0147':('TAX_AUTHORITY_REQUIRED','Tax'),'0184':('SOLARA_C1_UNRESOLVED','Procurement / Legal')}
CHECKS=['material_risk','tax_ambiguous','policy_version_verified','evidence_sufficient_human_verified','contract_conflict','disputed_scope_reconciled','usd_basis_verified','northstar_consultation_required','procurement_consultation_recorded','analyst_requests_escalation']
def build_case(case_id,root=ROOT):
    verify_sources(root)
    if not re.fullmatch(r'MRG-2026-\d{4}',case_id):raise Rejected('Invalid case ID')
    packet='source_pack/06_Unstructured_Case_Evidence/'+case_id+'.md'
    if not (root/packet).is_file():raise Rejected('No supplied case packet')
    with (root/'source_pack/meridian_disputes_250.csv').open(encoding='utf-8') as f:rows=[x for x in csv.DictReader(f) if x['case_id']==case_id]
    if len(rows)!=1:raise Rejected('Historical case identity is not unique')
    row=rows[0];suffix=case_id[-4:]
    files=[packet,'source_pack/01_AP_Dispute_Resolution_SOP.md','source_pack/02_Vendor_Commercial_Terms_Policy.md']
    suppliers={'NorthStar Consumer Products':'03_NorthStar_Agreements.md','Apex Industrial Supply':'04_Apex_Agreement.md','Solara Imports':'05_Solara_Agreements_and_Email.md'}
    if row['supplier_name'] in suppliers:files.append('source_pack/'+suppliers[row['supplier_name']])
    sources={p:source_record(p,root) for p in files};s=sources[packet]
    amount=row['disputed_amount_usd'];header=re.search(r'\*\*(?:Total disputed amount|Disputed amount):\*\* \$([0-9,.]+)','\n'.join(s['lines']))
    holds=[]
    if suffix in KNOWN_HOLDS:holds.append({'reason':KNOWN_HOLDS[suffix][0],'owner':KNOWN_HOLDS[suffix][1],'source_ref':packet,'clearing_rule':'Not clearable through reviewer flags; requires new source validation/version in a later controlled release.'})
    if header and Decimal(header.group(1).replace(',',''))!=Decimal(amount):holds.append({'reason':'PACKET_CSV_AMOUNT_CONFLICT','owner':'AP Analyst','source_ref':packet,'clearing_rule':'Reconcile authoritative original disputed amount before further processing.'})
    if Decimal(amount)==50000:holds.append({'reason':'HOLD_FOR_POLICY_CLARIFICATION','owner':'Finance Controls','source_ref':'source_pack/01_AP_Dispute_Resolution_SOP.md','clearing_rule':'Resolve source policy overlap.'})
    # Date comparison is only a review cue: case date is not necessarily the governing transaction date.
    policy_date_gap=row['case_created_date']<'2026-03-01'
    facts={k:row[k] for k in ['case_id','supplier_name','invoice_id','po_id','case_created_date','disputed_amount_usd','system_reason_code']}
    base={'schema_version':'1.0.0','case_id':case_id,'mode':'READ_ONLY_SOURCE_REPLAY','facts':facts,'fact_status':'Historical intake fields, not validated root cause or authority','sources':sources,'source_packet_excerpt':excerpt(s,1,len(s['lines'])),'review_question':QUESTIONS[suffix],'review_question_origin':'Authored design question grounded in supplied packet; not an LLM result or final disposition','source_holds':holds,'policy_date_gap_review_required':policy_date_gap,'review_checks':{k:None for k in CHECKS},'model_draft':None,'measurements':None,'approved':False,'financial_execution_allowed':False,'supplier_sending_allowed':False}
    base['case_version_sha256']=digest(base)
    return base
def review_template(case):
    return {'case_id':case['case_id'],'case_version_sha256':case['case_version_sha256'],'actor_label':None,'note':None,'confirmations':{k:None for k in CHECKS},'citations':[]}
def validate_review(review,case):
    if set(review)!={'case_id','case_version_sha256','actor_label','note','confirmations','citations'}:raise Rejected('Unexpected/missing review fields')
    if review['case_id']!=case['case_id'] or review['case_version_sha256']!=case['case_version_sha256']:raise Rejected('Stale/wrong case version')
    if not isinstance(review['actor_label'],str) or not review['actor_label'].strip():raise Rejected('Reviewer label required; identity remains unverified')
    if not isinstance(review['note'],str) or not review['note'].strip():raise Rejected('Review rationale required')
    if set(review['confirmations'])!=set(CHECKS) or any(v is not None and type(v) is not bool for v in review['confirmations'].values()):raise Rejected('Invalid review confirmations')
    if not review['citations'] or not all(validate_citation(c,case['sources']) for c in review['citations']):raise Rejected('Exact source citations required')
def reviewed_state(case,review=None):
    if review:validate_review(review,case)
    flags=dict(case['review_checks'] if review is None else review['confirmations'])
    flags.update(original_disputed_amount_usd=case['facts']['disputed_amount_usd'],solara_2026_freight=case['case_id'].endswith('0184'),solara_authority_confirmed=False)
    result=assess(flags)
    for h in case['source_holds']:
        if h['reason'] not in result['reasons']:result['reasons'].append(h['reason'])
        if h['owner'] not in result['owners']:result['owners'].append(h['owner'])
    if case['policy_date_gap_review_required']:
        result['reasons'].append('GOVERNING_HISTORICAL_POLICY_VERSION_NOT_SUPPLIED');result['owners'].append('Procurement / Finance Controls')
    if result['reasons']:result['status']='HOLD_AND_ESCALATE'
    result.update(identity_authenticated=False,review_is_approval=False)
    return result
def read_audit(path):
    if not Path(path).exists():return []
    events=[];previous=None
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        event=json.loads(line);stored=event.pop('event_hash')
        if event.get('previous_hash')!=previous or digest(event)!=stored:raise Rejected('Audit chain integrity failed')
        event['event_hash']=stored;events.append(event);previous=stored
    return events
def record_review(review,root=ROOT,output=None):
    case=build_case(review['case_id'],root);state=reviewed_state(case,review)
    output=Path(output or root/'runs');output.mkdir(parents=True,exist_ok=True)
    audit=output/'review_events.jsonl';events=read_audit(audit)
    event={'sequence':len(events)+1,'previous_hash':events[-1]['event_hash'] if events else None,'timestamp_utc':datetime.now(timezone.utc).isoformat(),'review':review,'state':state,'identity_authenticated':False,'event_type':'REVIEW_ANNOTATION_NOT_APPROVAL'}
    event['event_hash']=digest(event)
    with audit.open('a',encoding='utf-8') as f:f.write(json.dumps(event,sort_keys=True)+'\n')
    return event
def validate_model_draft(draft,case):
    if set(draft)!={'case_id','case_version_sha256','generation_label','claims'} or draft['case_id']!=case['case_id'] or draft['case_version_sha256']!=case['case_version_sha256']:raise Rejected('Invalid/stale draft')
    if not isinstance(draft['generation_label'],str) or not draft['generation_label']:raise Rejected('Generation provenance label required')
    if not isinstance(draft['claims'],list) or not draft['claims']:raise Rejected('Draft claims required')
    for claim in draft['claims']:
        if set(claim)!={'text','citations'} or not isinstance(claim['text'],str) or not claim['text'] or not claim['citations'] or not all(validate_citation(c,case['sources']) for c in claim['citations']):raise Rejected('Claim requires exact citations')
    return {'status':'CITATIONS_VALID_HUMAN_SEMANTIC_REVIEW_REQUIRED','approved':False,'note':'Exact quotation validity does not establish entailment or correct interpretation. Draft never sets review flags.'}
def replay(root=ROOT,output=None):
    out=Path(output or root/'runs/replay');out.mkdir(parents=True,exist_ok=True);items=[]
    for p in sorted((root/'source_pack/06_Unstructured_Case_Evidence').glob('*.md')):
        c=build_case(p.stem,root);save(out/(p.stem+'.json'),c);save(out/(p.stem+'.review.template.json'),review_template(c));state=reviewed_state(c)
        dossier='# '+p.stem+' — evidence review packet\n\n**Read-only; not a commercial decision.**\n\n'+c['review_question']+'\n\nStatus: '+state['status']+'\n\nKnown source holds: '+(', '.join(h['reason'] for h in c['source_holds']) or 'None curated; all reviewer checks still require confirmation.')+'\n\nCase version: `'+c['case_version_sha256']+'`\n\n## Intake fields\n\n'
        dossier+='\n'.join('- '+k+': '+v for k,v in c['facts'].items())+'\n\nThese historical intake fields do not establish correctness or authority.\n\n## Supplied case evidence\n\n```text\n'
        dossier+='\n'.join(str(i+1)+' | '+line for i,line in enumerate(c['sources'][next(iter(c['sources']))]['lines']))+'\n```\n\n## Supporting source documents\n\n'
        for sid,s in c['sources'].items():dossier+='- ['+sid+']('+Path(os.path.relpath(root/sid,out)).as_posix()+') · SHA-256 `'+s['sha256']+'`\n'
        dossier+='\n## Review\n\n[Structured review template]('+p.stem+'.review.template.json). Record evidence/triage observations only. Local actor labels are unverified; this cannot approve or release a payment.\n'
        (out/(p.stem+'.md')).write_text(dossier,encoding='utf-8')
        items.append({'case_id':p.stem,'supplier':c['facts']['supplier_name'],'review_question':c['review_question'],'source_holds':[h['reason'] for h in c['source_holds']],'state':state,'case_version_sha256':c['case_version_sha256']})
    save(out/'replay_results.json',{'mode':'DETERMINISTIC_RETRIEVAL_AND_GUARDS_NO_LLM','case_count':len(items),'cases':items,'measured_pilot_benefits':None})
    report='# Meridian case workbench — read-only replay\n\nAll packets are unreviewed. Holds identify outstanding verification, not final commercial outcomes. No LLM inference or measured pilot has run.\n\n'
    for i in items:report+='## '+i['case_id']+' · '+i['supplier']+'\n\n'+i['review_question']+'\n\n[Read evidence packet]('+i['case_id']+'.md) · [Structured dossier]('+i['case_id']+'.json) · [Review template]('+i['case_id']+'.review.template.json)\n\nSource-specific holds: '+(', '.join(i['source_holds']) or 'No curated source-specific hold; reviewer checks remain unset.')+'\n\nState: '+i['state']['status']+'\n\n'
    (out/'case_workbench_report.md').write_text(report,encoding='utf-8');return items
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('replay');a.add_argument('--output')
    a=sub.add_parser('record-review');a.add_argument('review_json');a.add_argument('--output')
    a=sub.add_parser('check-draft');a.add_argument('draft_json')
    args=p.parse_args()
    try:
        if args.command=='replay':print('Built',len(replay(output=args.output)),'read-only dossiers')
        elif args.command=='record-review':print(json.dumps(record_review(load(args.review_json),output=args.output),indent=2))
        else:
            d=load(args.draft_json);print(json.dumps(validate_model_draft(d,build_case(d['case_id'])),indent=2))
    except (Rejected,ValueError,KeyError,TypeError) as e:print('REJECTED:',e);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
