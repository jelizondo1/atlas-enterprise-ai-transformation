"""Read-only reference guard simulation; never approves, posts or sends anything.

Inputs represent verified facts for design tests, not authenticated production evidence.
"""
from decimal import Decimal,InvalidOperation

def assess(case):
    reasons=[];owners=[]
    def hold(reason,owner):
        reasons.append(reason)
        if owner not in owners:owners.append(owner)
    if case.get('material_risk') is not False:
        hold('RISK_REVIEW_REQUIRED','Finance / Legal / Compliance')
    if case.get('tax_ambiguous') is not False:
        hold('TAX_REVIEW_REQUIRED','Tax')
    if case.get('policy_version_verified') is not True:
        hold('GOVERNING_POLICY_UNVERIFIED','Procurement / Finance Controls')
    if case.get('evidence_sufficient_human_verified') is not True:
        hold('EVIDENCE_REVIEW_OR_REQUEST','AP Analyst / evidence owner')
    if case.get('contract_conflict') is not False:
        hold('CONTRACT_AUTHORITY_REQUIRED','Procurement / Legal')
    if case.get('solara_2026_freight') is True and case.get('solara_authority_confirmed') is not True:
        hold('SOLARA_C1_UNRESOLVED','Procurement / Legal')
    if case.get('disputed_scope_reconciled') is not True:
        hold('DISPUTED_COMPONENT_SCOPE_UNRECONCILED','AP Analyst / case owner')
    amount=None
    try:
        if type(case.get('original_disputed_amount_usd')) is not str:raise InvalidOperation
        amount=Decimal(case['original_disputed_amount_usd'])
        if not amount.is_finite() or amount<0:raise InvalidOperation
    except InvalidOperation:
        hold('INVALID_OR_MISSING_ORIGINAL_AMOUNT','AP Analyst')
    if case.get('usd_basis_verified') is not True:
        hold('CURRENCY_BASIS_UNVERIFIED','Finance Controls')
    role=None
    if amount is not None and amount.is_finite() and amount>=0:
        if amount==50000:hold('HOLD_FOR_POLICY_CLARIFICATION','Finance Controls')
        elif amount<10000:role='AP Analyst'
        elif amount<50000:role='AP Team Lead'
        elif amount<=250000:role='AP Manager'
        else:role='Finance Director'
    if case.get('northstar_consultation_required') is not False and case.get('procurement_consultation_recorded') is not True:
        hold('NORTHSTAR_CONSULTATION_REQUIRED','Procurement')
    if case.get('analyst_requests_escalation') is not False:
        hold('ANALYST_ESCALATION_PRESERVED','AP Team Lead / appropriate specialist')
    return {'status':'HOLD_AND_ESCALATE' if reasons else 'READY_FOR_AUTHORIZED_HUMAN_DECISION',
            'reasons':reasons,'owners':owners,'candidate_monetary_approval_role':role,
            'candidate_role_is_authorization':False,'approved':False,'financial_execution_allowed':False,
            'note':'Design simulation only. Candidate role does not supersede unresolved holds, specialist rules or authenticated authority.'}
