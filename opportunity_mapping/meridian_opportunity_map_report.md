# Atlas source-backed — AI Opportunity Mapping

**Meridian Retail Group AP disputes · Final design v1.0.0 · File-grounded**

All nine opportunities survive validation against the authoritative diagnosis and source files. The final map preserves Atlas's principle: **use AI where ambiguity exists, deterministic systems where truth can be calculated, and humans where judgment, risk and accountability require them.**

The recommendations form a controlled design, not a production authorization. Calculations and approval routing remain deterministic. Authorized humans approve and own ambiguous/high-risk decisions. Solara's unresolved 2026 freight terms remain with Procurement, with Legal confirmation as required by diagnosis C1.

## Evidence and design basis

The map uses original file references and JSON pointers for diagnosis findings F1–F7, conflict C1 and process step P5. F2 and F5 retain their DERIVED labels. Reopen-associated burden is 7,919 hours. The precise handling baseline is 71,952 hours; the original rounded 72,000-hour headline is retained as context. Intervention savings remain unsized.

Controls address the exact $50,000 threshold overlap, Apex component scope, policy effective dates and supplier-specific evidence exceptions. Clear contractual terms do not require unnecessary specialist escalation. [Provenance](../docs/provenance.json) records the selected authoritative files and public transformations.

## Baseline and burden

| Measure | Source-grounded value | Meaning |
|---|---:|---|
| Annual dispute volume | 180,000 | Declared annualization assumption |
| Sample | 250 cases | Synthetic client-facing dataset |
| Active handling | 71,952 hours; source-backed headline 72,000 | Precise vs rounded input calculation |
| Active-work FTE | 42.3247; source-backed reported 42.4 | 1,700 productive hours/FTE assumption |
| Team | 52 FTE; USD 4.42M/year | Declared 85,000 USD/FTE cost; not all active handling |
| SLA attainment | 62% | Observed sample |
| Missing-evidence SLA | 13.3% vs 68.6% without missing evidence | Association, not causal effect |

Sources: [sizing assumptions and output](../impact_sizing/meridian_annualized_impact_sizing.json), [quantitative baseline](../diagnostics/meridian_quantitative_diagnostics.json).

| Lens | Annualized cases | Associated excess active hours | Opportunity |
|---|---:|---:|---|
| Reopened | 25,200 | 7,919 | O05 |
| Missing evidence | 21,600 | 1,220 | O02 |
| 4+ systems | 89,280 | 7,619 | O01 |
| Recorded resolution ESCALATE | 51,840 | 5,092 | O07 |

These lenses overlap and must not be summed. Associated excess hours compare cohorts; they are not measured avoidable work, intervention eligibility or savings. ESCALATE describes the recorded resolution field, not every case that experienced escalation. Missing evidence also has an 8.6627-day observed resolution gap; days waiting are not interchangeable with active hours.

## Opportunity coverage and classification

All portfolio items combine multiple tasks, so all are HYBRID at opportunity level. Each explicitly assigns its components; O02, O08 and O09 do not require an LLM. The taxonomy and fixtures retain pure task-level examples across all six types.

| Opportunity | Actual diagnosis | Intervention components | Priority |
|---|---|---|---|
| O01 Evidence assembly | F1 | WORKFLOW_AUTOMATION + LLM + HUMAN_JUDGMENT | PILOT_FIRST |
| O02 Missing-evidence intake and follow-up | F2 | PROCESS_POLICY_CHANGE + DETERMINISTIC_LOGIC + WORKFLOW_AUTOMATION + HUMAN_JUDGMENT | PILOT_FIRST |
| O03 Contract applicability support | F3 | LLM + DETERMINISTIC_LOGIC + HUMAN_JUDGMENT + PROCESS_POLICY_CHANGE | CONTROL_PREREQUISITE |
| O04 Precedent controls | F4 | PROCESS_POLICY_CHANGE + DETERMINISTIC_LOGIC + LLM + HUMAN_JUDGMENT | EMBEDDED_CONTROL |
| O05 Closure quality and reopen learning | F5 | DETERMINISTIC_LOGIC + WORKFLOW_AUTOMATION + LLM + HUMAN_JUDGMENT | PILOT_FIRST |
| O06 Component reconciliation and calculations | F6 | LLM + DETERMINISTIC_LOGIC + HUMAN_JUDGMENT | VALIDATE_THEN_PILOT |
| O07 Escalation routing and decision briefs | F7 | DETERMINISTIC_LOGIC + WORKFLOW_AUTOMATION + LLM + HUMAN_JUDGMENT | PILOT_FIRST |
| O08 Resolve Solara 2026 freight authority gap | C1 | HUMAN_JUDGMENT + PROCESS_POLICY_CHANGE | CONTROL_PREREQUISITE |
| O09 Approval eligibility and routing | P5 | DETERMINISTIC_LOGIC + WORKFLOW_AUTOMATION + HUMAN_JUDGMENT | CONTROL_PREREQUISITE |

### O01 · Evidence assembly

**Evidence:** [F1](../reasoning/meridian_atlas_v0_diagnosis.json) `/diagnostic_findings/0`; [DOC:01_AP_Dispute_Resolution_SOP.md](../source_pack/01_AP_Dispute_Resolution_SOP.md); [DOC:03_NorthStar_Agreements.md](../source_pack/03_NorthStar_Agreements.md); [DOC:04_Apex_Agreement.md](../source_pack/04_Apex_Agreement.md); [DOC:05_Solara_Agreements_and_Email.md](../source_pack/05_Solara_Agreements_and_Email.md); [L3](../impact_sizing/meridian_annualized_impact_sizing.json) `/diagnostic_lenses/2`.

**Intervention:** Retrieve authorized records by stable identifiers; summarize and link relevant passages; analyst verifies sufficiency.

**Why:** An LLM can interpret varied documents; connectors should perform exact retrieval. A unified evidence checklist may solve part of the problem without AI.

**Boundary:** LLM must not invent missing receipts, silently select conflicting terms, or certify evidence as authoritative.

**Owner:** AP Operations (proposed accountable role). **Next:** Read-only connector pilot and analyst-reviewed evidence packet.

**Measure:** Time spent locating and reading evidence; citation accuracy; analyst correction rate. Savings remain null/UNSIZED.

### O02 · Missing-evidence intake and follow-up

**Evidence:** [F2](../reasoning/meridian_atlas_v0_diagnosis.json) `/diagnostic_findings/1`; [QUANT:missing_evidence_impact](../diagnostics/meridian_quantitative_diagnostics.json) `/missing_evidence_impact`; [L2](../impact_sizing/meridian_annualized_impact_sizing.json) `/diagnostic_lenses/1`.

**Intervention:** Define required evidence by case type; check presence; route requests and reminders; human assesses substantive adequacy. Use case-specific evidence requirements: an approved Apex service confirmation can substitute for a goods receipt on installation; documented receiving/system-error exceptions need authorized Receiving confirmation. Keep PENDING INFORMATION time visible.

**Why:** Requirements, timers and assignments are explicit. LLM is unnecessary for checklist presence checks.

**Boundary:** Presence is not validity; lack of a receipt must not become proof of non-delivery or automatic rejection.

**Owner:** AP Operations with Receiving (proposed accountable role). **Next:** Agree evidence owners and checklist; pilot reminder workflow.

**Measure:** Time waiting for evidence; completeness at intake; SLA by cohort. Savings remain null/UNSIZED.

### O03 · Contract applicability support

**Evidence:** [F3](../reasoning/meridian_atlas_v0_diagnosis.json) `/diagnostic_findings/2`; [DOC:03_NorthStar_Agreements.md](../source_pack/03_NorthStar_Agreements.md); [DOC:04_Apex_Agreement.md](../source_pack/04_Apex_Agreement.md); [DOC:05_Solara_Agreements_and_Email.md](../source_pack/05_Solara_Agreements_and_Email.md).

**Intervention:** Extract candidate clauses with citations and dates; deterministic filters enforce verified supplier, SKU, shipment/geography, scope and effective periods. AP may apply clear contractual terms; Procurement resolves conflict, uncertain authority, disputed interpretation or material precedent. Approved rules enter a versioned registry.

**Why:** Language interpretation benefits from AI support. Only approved, unambiguous rules may enter a versioned rule registry. Do not route every clear term to Procurement: commercial policy section 10 permits AP to apply clear terms. Historical cases must use the policy effective for their dates; do not retroactively apply the March 2026 policy.

**Boundary:** No model-selected binding interpretation when execution status, applicability, or amendments conflict.

**Owner:** Procurement (proposed accountable role). **Next:** Validate the supplier-rule registry and effective-date handling; use contract-term cases as a high-complexity pilot stratum, not as all eligible cases.

**Measure:** Clause citation correctness; unresolved-conflict detection; reviewer time. Savings remain null/UNSIZED.

### O04 · Precedent controls

**Evidence:** [F4](../reasoning/meridian_atlas_v0_diagnosis.json) `/diagnostic_findings/3`; [DOC:02_Vendor_Commercial_Terms_Policy.md](../source_pack/02_Vendor_Commercial_Terms_Policy.md); [CASE:MRG-2026-0018](../source_pack/06_Unstructured_Case_Evidence/MRG-2026-0018.md).

**Intervention:** Require current governing evidence; flag unsupported precedent; optionally summarize similar cases as context.

**Why:** Governance fixes authority; an LLM may aid comparison but past outcomes are not labels for correctness.

**Boundary:** Do not train an automatic pay/reject decision on historical dispositions as truth.

**Owner:** AP Quality and Procurement (proposed accountable role). **Next:** Introduce source-and-authority field in closure checklist.

**Measure:** Unsupported-precedent rate in sampled decisions. Savings remain null/UNSIZED.

### O05 · Closure quality and reopen learning

**Evidence:** [F5](../reasoning/meridian_atlas_v0_diagnosis.json) `/diagnostic_findings/4`; [QUANT:reopened_case_profile](../diagnostics/meridian_quantitative_diagnostics.json) `/reopened_case_profile`; [L1](../impact_sizing/meridian_annualized_impact_sizing.json) `/diagnostic_lenses/0`.

**Intervention:** Check required evidence, calculation and approval references; draft cited closure notes; human reviews reasoning; log reopen causes.

**Why:** Structured checks catch missing fields; semantic review can help explain a decision but cannot certify correctness.

**Boundary:** A complete note does not prove a correct outcome; new evidence must still permit reopening.

**Owner:** AP Quality (proposed accountable role). **Next:** Pilot closure checklist and reviewed note drafts.

**Measure:** Reopen causes; reviewed decision accuracy; total handling including review. Savings remain null/UNSIZED.

### O06 · Component reconciliation and calculations

**Evidence:** [F6](../reasoning/meridian_atlas_v0_diagnosis.json) `/diagnostic_findings/5`; [DOC:04_Apex_Agreement.md](../source_pack/04_Apex_Agreement.md); [CASE:MRG-2026-0139](../source_pack/06_Unstructured_Case_Evidence/MRG-2026-0139.md).

**Intervention:** Propose line/component extraction; human confirms disputed components and governing terms; deterministic service calculates supported/unsupported totals.

**Why:** Ambiguous component interpretation differs from arithmetic. Calculations require fixed precision, units, currency and reproducible inputs.

**Boundary:** No LLM arithmetic as system-of-record amount; no splitting the original dispute to reduce approval authority. In MRG-2026-0139, invoice components total $75000 while the header states $48088.38 disputed; supported items total $69000 and freight $6000. The scope relationship is not explained. Require case-owner reconciliation before computing a disputed adjustment or approval route; do not overwrite the original amount with either total.

**Owner:** AP Operations and Finance Controls (proposed accountable role). **Next:** Validate inputs and reconcile components to original dispute before calculation.

**Measure:** Reconciliation errors; component review time; amount traceability. Savings remain null/UNSIZED.

### O07 · Escalation routing and decision briefs

**Evidence:** [F7](../reasoning/meridian_atlas_v0_diagnosis.json) `/diagnostic_findings/6`; [DOC:01_AP_Dispute_Resolution_SOP.md](../source_pack/01_AP_Dispute_Resolution_SOP.md); [DOC:02_Vendor_Commercial_Terms_Policy.md](../source_pack/02_Vendor_Commercial_Terms_Policy.md); [CASE:MRG-2026-0184](../source_pack/06_Unstructured_Case_Evidence/MRG-2026-0184.md); [CASE:MRG-2026-0147](../source_pack/06_Unstructured_Case_Evidence/MRG-2026-0147.md); [L4](../impact_sizing/meridian_annualized_impact_sizing.json) `/diagnostic_lenses/3`; [DOC:03_NorthStar_Agreements.md](../source_pack/03_NorthStar_Agreements.md).

**Intervention:** Rules route known triggers; AI drafts the evidence brief; analysts can escalate any risk; accountable specialists decide.

**Why:** Routing can be mechanized while risk assessment remains with people. Escalation frequency alone does not show waste.

**Boundary:** Never suppress an escalation because the model is confident; never optimize escalation count as the sole KPI. NorthStar requires Procurement consultation before final communication for rejection above $100000, material historical-treatment change, or disputed promotion interpretation. Fraud/sanctions/litigation/regulatory concerns route immediately to Finance/Legal/Compliance; tax ambiguity routes to Tax.

**Owner:** AP Team Lead with specialist owners (proposed accountable role). **Next:** Agree escalation matrix and pilot structured briefs.

**Measure:** Routing accuracy; time to accountable owner; missed-risk rate. Savings remain null/UNSIZED.

### O08 · Resolve Solara 2026 freight authority gap

**Evidence:** [C1](../reasoning/meridian_atlas_v0_diagnosis.json) `/source_conflicts/0`; [DOC:05_Solara_Agreements_and_Email.md](../source_pack/05_Solara_Agreements_and_Email.md).

**Intervention:** Procurement owns obtaining executed documentation or an authorized documented decision, with Legal confirmation as required by C1; records scope and effective date; keeps case pending until authority exists.

**Why:** This is missing commercial authority, not a text-generation problem. No LLM is necessary to decide treatment.

**Boundary:** No extrapolation from old agreements, informal email, generic policy or prior payments to settle 2026 freight. Do not silently revert to FCA or apply the unsigned 4% fee/$1000 threshold; the expiry clause, continuation email and unsigned draft require Procurement / Legal confirmation together.

**Owner:** Procurement (proposed accountable role). **Next:** Owner-led document and authority remediation.

**Measure:** Documented authoritative resolution; zero unsupported freight decisions. Savings remain null/UNSIZED.

### O09 · Approval eligibility and routing

**Evidence:** [P5](../reasoning/meridian_atlas_v0_diagnosis.json) `/process_steps/4`; [DOC:01_AP_Dispute_Resolution_SOP.md](../source_pack/01_AP_Dispute_Resolution_SOP.md); [DOC:02_Vendor_Commercial_Terms_Policy.md](../source_pack/02_Vendor_Commercial_Terms_Policy.md); [DOC:03_NorthStar_Agreements.md](../source_pack/03_NorthStar_Agreements.md); [DOC:04_Apex_Agreement.md](../source_pack/04_Apex_Agreement.md).

**Intervention:** Versioned approved authority matrix computes required role from original disputed amount and exceptions; workflow obtains authenticated human approval.

**Why:** Threshold evaluation is deterministic; exercising delegated approval authority is an accountable human action.

**Boundary:** LLM cannot set thresholds, grant approval, substitute model confidence for authority, or route on the accepted portion only. At exactly $50000, overlapping source ranges must produce HOLD_FOR_POLICY_CLARIFICATION. Do not manufacture an inclusive/exclusive convention.

**Owner:** Finance Controls (proposed accountable role). **Next:** Finance Controls resolves the exact $50000 overlap, confirms currency/FX basis and encodes specialist exceptions; then test the versioned matrix.

**Measure:** Unauthorized closure rate; routing accuracy at boundaries. Savings remain null/UNSIZED.

## Priority and implementation sequence

1. **Control prerequisites:** Procurement addresses O08 and O03's governing-document registry, with Legal for C1; Finance Controls resolves O09's exact $50,000 overlap and currency/exception rules. Apply O04 precedent safeguards throughout.
2. **First read-only/shadow pilots:** O05 closure quality and O01 evidence assembly have the largest associated-hour lenses (7,919 and 7,619). These are workload signals, not additive benefit forecasts. O02 remains a first-wave candidate because missing evidence has a large observed delay/SLA gap despite lower associated active hours. Keep normal human decisions intact.
3. **Escalation support:** O07 improves routing and decision briefs while protecting necessary escalation. Do not reward fewer escalations without measuring missed risks. Include NorthStar consultation and Tax/Legal exceptions in the pilot.
4. **Higher-complexity support:** O03 clause comparison and O06 component extraction follow verified terms and reconciled inputs. Contract-term cases show 42.9 minutes and 15% SLA in the sizing output, useful for pilot stratification; intake reason codes are not verified root causes or eligibility counts. Apex scope clarification is a prerequisite for using MRG-2026-0139 as a numerical decision fixture.

No classification was changed merely to increase AI use. Control ownership and task boundaries were refined where the files support a more precise design. Dependencies outrank exposure size; no financial ranking is asserted.

## Impact measurement

Net annual hours = unique eligible annual cases × adoption × (baseline task minutes − intervention minutes including review) / 60 − annual maintenance hours.

Use unique case/task identifiers to avoid counting the same benefit across O01/O02/O05/O07. Validate causal effects with a controlled pilot and include corrections, reviewer work, maintenance and shifted workload. The sizing's USD 85,000/1,700 = USD 50 per productive hour is an explicit planning assumption; a capacity-value scenario is not cash savings. Implementation cost, eligible task time, effects and realization remain unknown. No monetary benefits are invented.

## Public-package verification

See the [final validation report](../docs/validation_report.md). This is a source-grounded design map, not a live model benchmark or an operational approval.
## Public-package verification

See the [final validation report](../docs/validation_report.md). This is a source-grounded design map, not a live model benchmark or an operational approval.
