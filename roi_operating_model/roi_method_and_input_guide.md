# Atlas source-backed — Deterministic ROI method

The model evaluates the **joint O01/O02/O05 workflow once**, using unique eligible annual cases and total measured bundle time. It does not add opportunity-level savings or source-backed burden lenses. If separate pilot cohorts are later combined, first reconcile case IDs, time boundaries and shared costs in a consolidated input; do not sum this engine's outputs.

## Source baseline

[source-backed /baseline](../opportunity_mapping/meridian_opportunity_map_final.json): 180,000 annual disputes (assumption), 71,952 precise active handling hours, 1,700 productive hours/FTE and USD 50/productive hour (85,000 / 1,700). The rounded source-backed 72,000-hour headline and approximately 42.3 precise active FTE remain context. The 52-FTE team is not assumed reducible to active handling FTE.

## Parameters and evidence required

| Parameter | Required definition | Owner / evidence |
|---|---|---|
| Unique eligible annual cases | Unique cases meeting the agreed pilot scope, with annualization method; not sum of exposure lenses | AP Analytics; measured coverage and eligibility ledger |
| Baseline bundle minutes | Active evidence assembly + information follow-up + closure/QA task minutes on eligible cases; no overlapping timer intervals | AP Operations; control cohort measurement |
| Intervention bundle minutes including review | Same boundary, including AI review/corrections, manual exceptions, follow-up and observed reopen rework | AP Operations; treatment measurement |
| Steady adoption | Fraction of eligible cases actually using the intervention, not model success rate | AP Operations; observed adoption or approved plan |
| Year-one adoption | Annual average including launch/ramp; must not exceed steady adoption in this model | AP Operations; approved ramp plan |
| Annual internal maintenance hours | Incremental internal support, QA monitoring and upkeep not already in case handling time | IT/AP; task ledger |
| Implementation cash cost | One-time incremental implementation cash outlay | Finance/IT; approved budget |
| Annual incremental run cash cost | Incremental infrastructure, model/API, licensing, external support, overtime/backfill or other actual cash cost | Finance/IT; measured bill or approved plan |
| Cash realization fraction | Portion of positive net released-capacity value that becomes a documented labor cash reduction/avoided spend | Finance; specific realization plan |

Every parameter carries its value, unit, status, owner and evidence reference. Unknown values remain null. Decimal values are strings to avoid binary floating-point artifacts. Known source assumptions do not make pilot effects known.

Input modes: UNSIZED (incomplete actual Meridian inputs), ILLUSTRATIVE (explicit counterfactual only), MEASURED_INPUTS (coverage/time must carry pilot-measurement provenance; adoption/costs can be approved plans). Even MEASURED_INPUTS produces a **conditional scenario**, not automatically a verified outcome.

Evidence references and boolean gate attestations are an interface contract. The engine checks their structure and declared provenance; an authorized reviewer must verify the underlying measurement, plan and gate record. A user-supplied true flag is not authentication or independent evidence validation.

## Formulas

Let N = unique eligible annual cases; A = adoption; B = baseline bundle minutes; T = intervention minutes including review; M = annual internal maintenance hours; R = capacity rate; F = cash realization fraction; C = annual incremental run cash cost; I = implementation cash cost.

- Gross released hours = N × A × (B − T) / 60.
- Net capacity hours = gross released hours âˆ’ M. Negative values remain negative.
- Net capacity value = net capacity hours × R. This is a capacity valuation, not a cash benefit.
- Realizable labor cash benefit = max(net capacity hours, 0) × R × F.
- Remaining noncash capacity value = max(net capacity value, 0) âˆ’ realizable labor cash benefit.
- Steady net cash benefit = realizable labor cash benefit âˆ’ C.
- Year-one net cash benefit = labor cash benefit at year-one adoption âˆ’ C âˆ’ I.
- Cash ROI fraction = net cash benefit / incremental cash costs for that period; null when denominator is zero.
- Steady cash break-even improvement minutes = [M + C / (R × F)] × 60 / (N × A), when N × A and F are positive. Compare with B − T; a threshold above feasible time is not achievable under those inputs.
- Steady-run-rate payback proxy = I / positive steady net cash benefit × 12. This is explicitly not ramp-adjusted payback; actual payback remains null until dated cash flows exist.

Implementation cost is included in year one, not repeatedly each year. Annual maintenance and run costs are charged in full in both views, even with zero adoption; provide a conservative annual budget or a separately approved prorated year-one extension later. Year-one adoption is the only ramp term implemented here.

Internal maintenance consumes released capacity. Run cash cost contains incremental cash spending, not an automatic second monetization of the same internal hours. If paid overtime/backfill genuinely adds cash cost, document that separately. The capacity-minus-cash-cost view is a planning comparison, not a financial ROI; do not add it to the cash view.

No automatic benefit is assigned to better SLA, lower escalations, prevented loss, working capital, invoice face value or the observed 7,919/1,220/7,619/5,092 burden lenses. These require separately evidenced causal/financial models. Accuracy is a gate, not a savings multiplier. Reopens enter matched observed task time, not a second benefit stream.

## Guardrails and interpretation

The engine rejects extra benefit fields, bad units, nonfinite/negative values, fractional case counts, volumes above 180,000, duplicate bundle definitions, year-one adoption above steady state, and eligible baseline time exceeding 71,952 hours. It blocks complete scenarios when unique-cohort/nonoverlap or quality/control gates fail or remain unknown. Cash realization above zero requires an approved-plan flag and reference.

These caps are plausibility checks, not proof of no overlap. The measurement ledger and review must establish unique cases, compatible task boundaries and complete observation. Negative returns are valid outputs; they must not be edited away.

The synthetic arithmetic fixture in tests/ exists only to verify the software. Its numbers are invented test values and are not Meridian assumptions or a recommended scenario. The real Meridian input/result files remain NOT_ESTIMABLE.
