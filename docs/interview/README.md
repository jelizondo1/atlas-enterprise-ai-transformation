# Interview materials

## 90-second explanation

Atlas is a working enterprise AI transformation POC around a fictional retailer's supplier invoice disputes. I started with policies, agreements, historical cases and evidence packets, then connected process diagnosis to intervention choices, workload sizing and a proposed operating model.

The central design choice is to use AI where evidence is ambiguous, deterministic systems where an answer can be calculated, and people where risk and accountability require judgment. For example, Atlas can organize conflicting contract evidence, but it cannot decide which unsigned terms are binding. It can calculate that Apex's listed components total $75,000, but it keeps the mismatch with the $48,088.38 disputed scope unresolved until the case owner reconciles it.

The local workbench exposes evidence, checks and review responsibilities. The model adapter requires cited structured output and separates structural validation from independent semantic review. Live model validation is pending; I do not present mocks as benchmark results. The ROI engine also leaves benefits unestimated until intervention measurements exist.

Atlas demonstrates how I connect enterprise problem framing to a working, governed POC and an honest production handoff.

## Three-minute technical walkthrough

Start with the source pack: five policy/agreement documents, 250 historical synthetic cases and 12 richer packets. The deterministic diagnostic analyzer measures the baseline. A separate diagnosis records evidence-backed findings, conflicts and uncertainty. The opportunity map assigns work across AI, rules, workflow, people and policy change, with explicit prerequisites.

Next show the case workbench. It assembles a source-version-bound dossier with numbered source lines and historical intake fields; historical outcomes are excluded as decision authority. The demo distinguishes an authored review question from a model output. Select Apex 0018 to show a contract conflict and why precedent cannot override current terms. Select Apex 0139 to show deterministic arithmetic without inventing disputed scope. Select Solara 0184 to show Procurement / Legal ownership of the unsigned 2026 terms.

Then explain the adapter. Only the allowlisted source context reaches the model. The request has strict JSON output, no tools, bounded tokens and timeout, and no retry. The validator checks identity, version, source hash, line range and exact quote. A cited false interpretation can still pass that gate, so independent semantic review remains mandatory. Failed hard gates override a high score. Local tests exercise malformed output, refusal, timeout, stale citations and attempts to introduce financial actions; they do not demonstrate live model quality.

Finally show measurement and ROI. Count unique eligible cases and include review/rework and maintenance effort. Reject overlapping labor intervals and stale case versions. Distinguish reclaimed capacity from realized cash. Unknown inputs remain null. End with production requirements: authenticated identity and approval, access-scoped integrations, durable audit, security, observability and controlled rollout.

## Working POC versus production ownership

“I can independently scope and build a working POC far enough to validate the workflow, business value, and technical feasibility. For production hardening and enterprise-scale deployment, I would partner closely with engineering.”

The portfolio demonstrates problem framing, source analysis, intervention boundaries, a working local interface, deterministic controls, model integration and evaluation/measurement design. It does not establish a measured business result. Describe the actual tools and AI assistance used when asked; do not imply unaided authorship or operational deployment.

Production engineering would partner on identity, authorization, secrets, resilient ERP/document connections, audit storage, monitoring, security and deployment. Operations, Finance, Procurement, Legal and domain reviewers retain ownership of policy, authority and acceptance decisions.

## Key tradeoffs

- Fail closed on uncertainty: more human work initially, lower risk of unsupported action.
- Explicit rules for known authority gaps: inspectable and testable, but source/version governance is required as policies change.
- Separate semantic review: slower than automatically scoring citations, but quote accuracy alone cannot establish correct interpretation.
- Read-only pilot: operationally limited, but it can measure evidence/review effort before introducing execution risk.
- Conservative ROI: fewer headline claims, stronger distinction between observed workload, causal improvement and realized cash.

## Five likely questions

**Why use an LLM at all?** Policies and correspondence contain ambiguity that exact rules cannot reliably interpret. An LLM can compare and organize evidence for review; arithmetic and authority checks remain explicit code.

**How do you prevent hallucinations?** Constrain the source context and output, require exact citations, reject unsupported structure and preserve uncertainty. These reduce risk; they do not eliminate it. Human semantic review checks entailment and authority.

**How would you prove ROI?** Measure a unique, controlled eligible cohort, active effort including review and rework, quality and maintenance. Estimate net capacity separately from cash realization. The current baseline is synthetic and no intervention benefit has been measured.

**What happens when the model is wrong or unavailable?** Refusals, timeouts and malformed output produce no admitted draft. A structurally valid wrong interpretation still needs semantic review. Existing rules and source holds are independent of the draft.

**What would block production?** Unresolved source authority, failed quality/control gates, absent authenticated approval/audit, unproven integrations and security, or an unsupported benefit case. A strong development score alone is insufficient.

## FinPago versus Atlas

FinPago proves I can build a bounded AI system. Atlas proves I can determine what an enterprise should automate, how to govern it, how to measure it, and how to deploy it safely. This comparison makes no additional claims about FinPago's features, results or production status.
