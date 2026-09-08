# Atlas source-backed — Intervention taxonomy and classification rules

Version 1.0.0. This taxonomy classifies tasks, not whole departments. A hybrid classification must name each component and its responsibility; it is not an excuse to add AI everywhere.

**Principle:** Use AI where ambiguity exists, deterministic systems where truth can be calculated, and humans where judgment, risk and accountability require them.

| Type | Use when | Suitable AP task | Boundary / unsuitable use |
|---|---|---|---|
| LLM | Language varies and a useful output can be verified against evidence | Cited draft summary or proposed document classification | Cannot establish contractual authority, calculate authoritative amounts, approve or execute payment |
| DETERMINISTIC_LOGIC | Verified inputs and an approved rule produce a reproducible answer | Component arithmetic, reconciliation, date comparison, approval-role eligibility | Missing or conflicting inputs cause a hold; do not guess values or policy |
| WORKFLOW_AUTOMATION | A known event triggers a stable sequence of actions | Assign owner, request known missing item, reminder, status synchronization | Does not resolve unclear commercial meaning or grant authority |
| HUMAN_JUDGMENT | Interpretation, material risk, exception authority or accountability is required | Conflicting amendments, tax ambiguity, commercial exception, authenticated approval | Human review must include evidence, authority, ability to reject, and an audit record |
| PROCESS_POLICY_CHANGE | The root cause is missing ownership, standards, documentation or policy | Executed-contract registry; evidence checklist; clarified authority matrix | Software cannot manufacture a missing agreement or an accountable owner |
| HYBRID | The task decomposes into two or more necessary intervention types | AI draft + deterministic reconciliation + human decision + workflow routing | Enumerate components, handoffs and stop conditions. An LLM is optional |

## Classification sequence

1. Identify the diagnosed problem and source evidence. Separate the observed problem from the proposed remedy (normally INFERRED).
2. Decompose retrieval, interpretation, calculation, routing, approval and execution into separate tasks.
3. Check whether missing policy, evidence or ownership causes the problem. Assign process/policy remediation before encoding a rule.
4. If authoritative inputs plus an approved rule determine the answer, choose deterministic logic. If only coordination is needed, choose workflow automation.
5. If bounded language interpretation adds value, propose LLM assistance with citations and review. Exact lookup alone does not establish an AI need.
6. If authority, material risk or unresolved ambiguity remains, assign a named human decision owner. AI may prepare a brief but cannot resolve the ambiguity by confidence.
7. Choose HYBRID only when multiple components are necessary. Name an alternative without AI and explain why AI adds value, or omit it.
8. Apply hard boundaries before prioritization or economic scoring. No benefit estimate may override a boundary.

## Mandatory handoffs

| Task | Executor | Acceptance / stop rule |
|---|---|---|
| Evidence retrieval | Authorized connector or human | Preserve stable IDs, versions, permissions and timestamps; inaccessible record means missing evidence |
| Semantic extraction | LLM candidate output | Cite exact passage; label uncertainty; human validates financially material inputs |
| Applicable terms | Authorized specialist when disputed | Confirm execution status, effective date, scope and hierarchy; unresolved conflict stays open |
| Amount computation | Deterministic service | Validated inputs, explicit currency/units, approved rounding, reproducible reconciliation |
| Approval routing | Versioned rule engine | Original disputed amount, role/identity and exception precedence; undefined equality/FX rules cause hold |
| Approval decision | Authorized human | Authenticated, current delegation, evidence reviewed; no model approval |
| Posting and communication | Controlled workflow after approvals | Revalidate state, idempotency and authority; audit result and reconcile failures |

The authoritative SOP section 8 overlaps at exactly $50,000: both the Team Lead and AP Manager ranges name that endpoint. source-backed deliberately does not invent a deployable authority table. Finance Controls must confirm exact equality treatment, currencies, FX basis and exception precedence from authoritative documents before implementation. Splitting components must not lower authority requirements based on the original dispute.

## Evidence and confidence

DIRECT = explicitly present in the cited available evidence; DERIVED = computed from identified inputs with formula; INFERRED = hypothesis or recommendation. Preserve the original diagnosis evidence type: F2 and F5 are DERIVED; the other F findings are DIRECT. Recommendations remain INFERRED.

Do not fabricate numeric confidence scores. Record source strength and missing evidence. Historical decisions are context, not proof of correct treatment. Supplier priority may affect urgency, never unsupported authority or evidence waivers.

## Prioritization

Sequence control and policy prerequisites first, then reversible shadow pilots, then measured deployment proposals. Compare measured net benefit, decision error, reviewer burden, coverage and implementation cost. Do not prioritize on theoretical case volume alone, and do not target fewer escalations without measuring missed risks.


## Source-validated refinements

AP may apply clear terms under commercial policy section 10; specialist review is triggered by conflict, ambiguity, challenge or precedent. Validate governing dates before applying policy. For NorthStar, supplier-specific 120-day window and defined Procurement consultation override generic simplifications. For Apex, accepted service confirmation is valid without a goods receipt for installation, and disputed components must be reconciled to original scope before routing. C1 requires Procurement / Legal confirmation; no model-selected fallback settles Solara 2026 freight. See source_reconciliation.md for exact file references.
