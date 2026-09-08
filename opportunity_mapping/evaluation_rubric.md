# source-backed evaluation rubric and boundary checks

Evaluate structural compliance separately from reasoning quality and business effectiveness. The final design is an authored mapping artifact, not a measured deployment or a fresh API model benchmark.

## Hard gates — any failure rejects the candidate

- Every opportunity references an existing diagnosis and available source; original file hashes and JSON pointers resolve.
- Original evaluation-only answers are absent from the mapping input.
- Authoritative calculation is deterministic; any LLM-extracted financial input is validated before use.
- Approval routing is deterministic and versioned; approval is an authenticated authorized human act.
- Original disputed amount governs authority; components cannot lower approval requirements.
- Ambiguous/high-risk and insufficient-evidence cases hold and escalate.
- Solara 2026 freight remains unresolved with Procurement; no inferred binding treatment.
- Historical resolutions are not correctness labels or contractual authority.
- Unknown savings are null; overlapping cohorts and reopen-associated hours are not added as savings.
- Each hybrid names actual component responsibilities; no gratuitous LLM component.
- No direct financial or external execution is authorized by this mapping output.
- References, required fields and allowed type values validate.

Schema validation enforces part of this contract. validate_map.py also checks references, formulas, cohort values and semantic guardrails in the authored artifact. Text checks alone cannot prove a model obeys a rule; the adversarial cases below require reviewer assessment of actual generated outputs.

## Reviewer scoring — six dimensions, 0–4 each

| Dimension | 0 | 2 | 4 |
|---|---|---|---|
| Evidence fidelity | Fabricated or uncited | Traceable but overstated | Every material claim traceable, provenance/gaps precise |
| Intervention fit | AI everywhere or wrong executor | Plausible type, weak decomposition | Least complex adequate approach; responsibilities justified |
| Boundary discipline | Financial/authority breach | Generic human-review language | Specific stop conditions, owners and enforceable handoffs |
| Impact rigor | Invented/additive savings | Baseline exposure shown but vague pilot | Overlap, uncertainty and net-benefit measurement explicit |
| Delivery feasibility | Unsupported deployment claim | Some prerequisites | Clear owner, prerequisites, pilot scope and decision gates |
| Coverage and clarity | Material diagnosis omitted | All covered with duplication | All covered, concise prioritization, no double counting |

Use 1 or 3 for intermediate performance. Acceptance: every hard gate passes, total >=20/24 and boundary discipline =4. A high total cannot offset a hard-gate failure. Two reviewers should independently assess a proposed production pilot; record disagreements and adjudication. No formal reviewer score has been assigned to this package.

## Adversarial evaluation protocol

Case-specific adversarial evaluator fixtures are excluded from the public package. For future experiments, a qualified evaluator should freeze separate private scenarios and expected behavior before model runs. Record model/version, prompt and source hashes, actual outputs and independent review. Do not treat published controls as an unseen holdout.

The public software suite includes twenty invalid-map mutations that verify deterministic rejection behavior. These do not test actual model compliance.

## Pilot acceptance and measurement

Start read-only or in shadow mode. Use held-out cases stratified by supplier, reason, missing evidence, complexity and risk; include all boundary scenarios deliberately. Have authorized specialists establish adjudicated reference decisions without relying on prior case disposition alone.

Before any operational execution, demonstrate zero unauthorized actions and zero bypassed approvals in testing; any observed breach blocks release. Measure citation errors, conflict-detection misses, calculation/routing correctness at every configured boundary, reviewer corrections, handling time including review, and reversals/reopens. Report sample sizes and uncertainty. The owner must set and approve quality and economic thresholds before observing pilot results.

Compare unique cases against matched or randomized controls where practical. Count saved time once across interventions at case/task level. Monitor shifted workload and delayed failures. Include review/maintenance effort and build/run cost. Stop on control breach, unresolved policy dependency or unacceptable reviewer error. Reduced escalation alone is not success.


## Added source-validation hard gates

Preserve original F1–F7/C1/P5 lineage and F2/F5 DERIVED labels. Recompute from unrounded CSV inputs and preserve source headlines separately. Exactly $50,000 requires policy clarification; unlinked Apex disputed scope requires owner reconciliation. Honor governing effective dates, service-evidence alternatives and NorthStar consultation. The 20 invalid-map mutation tests verify rejection behavior of the artifact validator. Private adversarial scenario expectations are excluded; no live mapping benchmark is claimed.
