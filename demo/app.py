"""Local, read-only Atlas demonstration. No provider calls or financial actions."""
import sys,json
from pathlib import Path
from decimal import Decimal
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
for folder in ['workbench','model_integration']:sys.path.insert(0,str(ROOT/folder))
from workbench import build_case,reviewed_state,review_template,excerpt,Rejected
from evaluate_run import evaluate
from model_runner import load

st.set_page_config(page_title='Atlas | Evidence & authority',page_icon='◈',layout='wide')
st.markdown('''<style>
.block-container{max-width:1280px;padding-top:4rem}h1{letter-spacing:-1.3px}
[data-testid="stMetric"]{background:white;border:1px solid #dde5e9;border-radius:8px;padding:14px}
[data-testid="stSidebar"]{border-right:1px solid #dce5e7}
.eyebrow{color:#16766a;font-size:12px;font-weight:700;letter-spacing:2px}
</style>''',unsafe_allow_html=True)
curated={'MRG-2026-0018':'01 · Conflicting amendments','MRG-2026-0139':'02 · Disputed scope mismatch','MRG-2026-0184':'03 · Unsigned freight terms'}
ids=list(curated)+[p.stem for p in sorted((ROOT/'source_pack/06_Unstructured_Case_Evidence').glob('*.md')) if p.stem not in curated]
requested=st.query_params.get('case',ids[0])
with st.sidebar:
    st.title('Atlas')
    st.caption('ENTERPRISE AI TRANSFORMATION')
    chosen=st.selectbox('Meridian case',ids,index=ids.index(requested) if requested in ids else 0,format_func=lambda x:curated.get(x,x))
    st.divider()
    st.markdown('**Evidence first. Authority preserved.**')
    st.caption('Fictional Meridian Retail Group · synthetic source evidence')
    st.info('Read-only / shadow\n\nNo payments, approvals or supplier messages.')
    st.markdown('**Three responsibilities**\n\nAI drafts interpretations.\n\nRules validate and route.\n\nPeople own judgment and decisions.')
case=build_case(chosen)
stored=st.session_state.get('review_'+chosen)
state=reviewed_state(case,stored)
st.markdown('<div class="eyebrow">CASE WORKBENCH / GOVERNED REVIEW</div>',unsafe_allow_html=True)
st.title(curated.get(chosen,'Evidence review').split(' · ')[-1])
st.caption(chosen+' · '+case['facts']['supplier_name'])
a,b,c=st.columns([1,1,1.4])
a.metric('Original disputed amount',f"${Decimal(case['facts']['disputed_amount_usd']):,.2f}")
b.metric('Source documents',len(case['sources']))
c.metric('Workflow state','On hold' if state['reasons'] else 'Human decision required')
st.warning(case['review_question'].replace('$',r'\$'))
st.caption('Source-grounded design guidance · authored control, not an AI-generated result.')
overview,evidence,review=st.tabs(['Review overview','Evidence & source lines','Human review'])
with overview:
    left,right=st.columns([1.15,1])
    with left:
        st.subheader('AI · evidence draft')
        admitted=[]
        for p in (ROOT/'runs/live').glob('*/'+chosen+'/run.json'):
            try:
                r=load(p)
                e=evaluate(p.parent)
                if r['execution_mode']=='LIVE_API' and r['provider_attempted'] and e['status']=='AWAITING_INDEPENDENT_SEMANTIC_REVIEW':admitted.append((p,r))
            except (ValueError,KeyError,OSError):pass
        if not admitted:
            st.info('Live generation unavailable until API configured. No model draft is available for this case.')
            st.caption('Integration is mock-tested. Live benchmark and independent semantic review are pending.')
        else:
            p,r=sorted(admitted,key=lambda x:x[1]['started_at_utc'])[-1]
            st.warning('Live model draft · structurally valid · independent semantic review required')
            st.caption('Model: '+str(r['model_returned'])+' · Run: '+r['run_id'])
            review_path=p.parent/'semantic_review.template.json'
            if review_path.is_file():
                try:st.caption('Recorded review check: '+evaluate(p.parent,load(review_path))['status']+' · identity and independence remain self-attested; no operational approval.')
                except (ValueError,KeyError,OSError):st.caption('Stored review cannot be validated; independent review remains pending.')
            st.write('Model-suggested next step: '+r['draft']['recommended_next_step'].replace('_',' ').lower())
            st.write('Suggested reviewer: '+r['draft']['suggested_review_owner'])
            for uncertainty in r['draft']['uncertainties']:st.write('Uncertainty: '+uncertainty.replace('$',r'\$'))
            for claim in r['draft']['claims']:
                st.write(claim['text'].replace('$',r'\$'))
                for cite in claim['citations']:
                    with st.expander(cite['source_id']+f" · lines {cite['line_start']}–{cite['line_end']}"):
                        st.text(cite['quote'])
        st.subheader('Structured intake facts')
        st.table({'Field':list(case['facts']),'Value':list(case['facts'].values())})
        st.caption(case['fact_status'])
    with right:
        st.subheader('Rules · deterministic checks')
        st.success('Source hashes verified · current source version bound to this case')
        if chosen.endswith('0139'):
            total=sum(map(Decimal,['42000','27000','6000']))
            st.write(f'Listed components: $42,000 + $27,000 + $6,000 = ${total:,.2f}'.replace('$',r'\$'))
            st.write(f"Difference from disputed scope: ${total-Decimal(case['facts']['disputed_amount_usd']):,.2f}")
            st.caption('Arithmetic comparison only. The packet supplies these components; reconciliation is unresolved. This is not an approved adjustment or routing basis.')
        st.write('Candidate monetary role: **'+str(state['candidate_monetary_approval_role'] or 'Unresolved')+'**')
        st.caption('Amount-band indication only. It grants no authority and cannot override any hold. Exact $50,000 remains a policy-clarification hold.')
        st.subheader('People · unresolved holds')
        for h in case['source_holds']:st.error(h['reason'].replace('_',' ').capitalize()+' → '+h['owner'])
        with st.expander(f"All {len(state['reasons'])} outstanding checks",expanded=False):
            for reason in state['reasons']:st.write('• '+reason.replace('_',' ').capitalize())
        st.write('**Next step:** '+case['review_question'].replace('$',r'\$'))
        st.caption('Model confidence cannot suppress escalation. Historical payment is not contractual authority.')
with evidence:
    sid=st.selectbox('Evidence document',list(case['sources']),format_func=lambda x:Path(x).name)
    source=case['sources'][sid]
    st.caption('SHA-256 '+source['sha256'])
    st.code('\n'.join(f'{i+1:03} | {line}' for i,line in enumerate(source['lines'])),language=None)
with review:
    st.subheader('Human-controlled evidence review')
    st.write('Record an evidence assessment for this local session. This form does not authenticate identity, approve a disposition or clear a source-level hold.')
    with st.form('review_form_'+chosen):
        actor=st.text_input('Reviewer label (self-reported)')
        note=st.text_area('Evidence assessment and rationale')
        flags={}
        cols=st.columns(2)
        for i,k in enumerate(case['review_checks']):
            with cols[i%2]:
                value=st.selectbox(k.replace('_',' ').capitalize(),['Not assessed','Yes','No'],key=chosen+k)
                flags[k]={'Not assessed':None,'Yes':True,'No':False}[value]
        rsid=st.selectbox('Cited source',list(case['sources']),key='review_source_'+chosen)
        start=st.number_input('First cited line',min_value=1,value=1,step=1)
        end=st.number_input('Last cited line',min_value=1,value=1,step=1)
        submitted=st.form_submit_button('Record session assessment')
    if submitted:
        r=review_template(case);r.update(actor_label=actor,note=note,confirmations=flags,citations=[excerpt(case['sources'][rsid],int(start),int(end))])
        try:
            reviewed_state(case,r)
            st.session_state['review_'+chosen]=r
            st.rerun()
        except Rejected as e:st.error(str(e))
    if stored:
        st.success('Session assessment recorded. No approval issued.')
        st.download_button('Download assessment',json.dumps(stored,indent=2),chosen+'.review.json',mime='application/json')
    st.write('**Current state:** '+state['status'])
    st.caption('Source-level holds require new validated evidence and a controlled version update. Production identity, authorization and audit services are outside this demonstration.')
