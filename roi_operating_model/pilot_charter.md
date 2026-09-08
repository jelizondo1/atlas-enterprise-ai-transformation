# Atlas source-backed — Pilot charter and operating ownership

**Proposed pilot:** O01 evidence assembly + O02 missing-evidence intake/follow-up + O05 closure quality. **Status:** design ready; measurement parameters and owner sign-off pending. No live deployment is authorized.

## Why this pilot

O01 and O05 address the largest observed associated-hour lenses; O02 addresses the substantial evidence-delay/SLA gap. The bundle can be tested as read-only/review assistance. It also exercises evidence, language interpretation, deterministic completeness checks and human decisions without launching autonomous dispute resolution. Source basis: [source-backed opportunities O01/O02/O05](../opportunity_mapping/meridian_opportunity_map_final.json).

O03's governing-term registry and O04's precedent discipline are embedded prerequisites. O08's unresolved Solara authority and O09's $50,000 ambiguity are held out of decision automation; they may appear as deliberate abstention tests. O06 and O07 support reconciliation and escalation without becoming additive benefit claims.

## Entry and exclusion rules

Include cases only with known identity, permitted source access, observable task boundaries and an applicable policy version. Stratify by supplier, reason code, missing evidence and complexity. Keep a registry of every screened case, eligibility, assignment and exclusion reason; do not silently drop difficult or failed cases from performance reporting.

For initial read-only tests, unresolved Solara freight, unreconciled Apex MRG-2026-0139, exact $50,000 authority, tax ambiguity and material-risk cases must demonstrate the correct hold/escalation. They are not candidates for automated substantive decisions. Missing evidence may remain in scope for O02's request/coordination support, while final disposition remains held.

## Phases and exit gates

| Phase | Work | Gate |
|---|---|---|
| Readiness | Confirm policies, owners, access, checklist exceptions, measurement boundary, quality thresholds and privacy controls | Authorized owners record approval; unresolved quality thresholds block launch |
| Offline replay | Read-only evidence packets, drafts and guard tests on historical source material | Correct holds; no use of hidden answers as model inputs; adjudicated reference decisions use governing evidence |
| Shadow pilot | Parallel support alongside current process; no automated posting/sending | Human-reviewed outputs; logged corrections/time; immediate stop for control breach |
| Controlled assisted pilot | Only separately authorized assistance; current human authority unchanged | Predeclared quality/noninferiority and net-time criteria met with complete observation |
| Business-case decision | Supply measured coverage/time and approved cost/adoption/realization inputs to ROI engine | Finance reviews conditional cash/capacity views; production decision is separate |

No calendar dates or sample sizes are invented. AP Analytics sets sample size using expected variability and agreed precision/noninferiority requirements before results are observed. Approve these fields in [pilot_acceptance_parameters.json](pilot_acceptance_parameters.json).

## Measurement design

Use randomized case assignment where operationally feasible; otherwise predefine matched controls by supplier, reason, complexity and evidence availability, document residual confounding and avoid causal overclaiming. Record assignment before treatment. Analyze all assigned cases, including failures and crossovers; report adoption separately so it is not counted twice in both treatment effect and the ROI adoption factor.

The engine expects Bâˆ’T conditional on actual intervention use; A accounts for uptake separately. An intention-to-treat time difference already contains uptake: either recover a justified per-used-case effect or set A=1 for the assigned eligible population with the exact definition documented. Never multiply an uptake-adjusted effect by adoption again.

Track active task intervals without overlapping timers. Review and correction minutes are included in bundle totals and recorded separately only for diagnosis. Track pending business days, SLA, decision accuracy, citation errors, missed escalations, approval bypasses and reopen rework. Keep elapsed waiting separate from labor minutes. Close an observation window for every case; incomplete reopen windows are censored/flagged, not treated as no reopen.

Freeze sample strata, observation window, confidence level, error limits and minimum net-time improvement before pilot results. Report sample sizes, exclusions and uncertainty. Good performance in a synthetic set is not evidence of live operational gains.

## Ownership and handoffs

| Activity | Accountable | Responsible / consulted |
|---|---|---|
| Pilot scope and workflow | AP Operations | AP Analyst, Analytics, IT |
| Evidence adequacy and case interpretation | AP Analyst within authority | Receiving, Facilities, Logistics, Procurement |
| Ambiguous commercial terms / Solara C1 | Procurement | Legal confirms where needed |
| Tax ambiguity | Tax | AP supplies evidence brief |
| Authority matrix / cash realization | Finance Controls / Finance | AP management; no LLM authority |
| Rule implementation and integrations | IT / ERP owner | Finance Controls approves rule meaning |
| Decision and monetary approval | Currently authorized role | Required specialist consultation remains separate |
| Quality and measurement adjudication | AP Quality | Procurement/Tax/Finance for disputed assessments |
| Change adoption and training | AP Operations | Team Leads and analysts |

Teach analysts how to verify citations, distinguish missing from invalid evidence, challenge AI drafts, request escalation and report failures. Publish a simple feedback channel and retain corrections for review; no automatic training on historical paid/rejected labels.

## Stop and recovery

Stop the relevant capability immediately on unauthorized action, approval bypass, hidden-answer leakage, forced resolution of a known hold or lost auditability. Return work to the current human process and preserve logs. Suspend on quality deterioration beyond the preapproved bound. Record incident owner and corrective action before restarting.

Future production execution must recheck current case hash, approval, delegated authority and specialist decisions. A stale approval returns to review. An unknown posting result is reconciled before retry; use idempotency to prevent duplicates. Changed facts or reopened decisions require fresh applicable approvals.
