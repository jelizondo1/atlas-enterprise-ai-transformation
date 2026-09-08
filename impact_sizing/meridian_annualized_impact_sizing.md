# ATLAS — Meridian Annualized Impact Sizing

## Purpose

This layer translates the 250-case diagnostic sample into **annualized current-state burden estimates** using Meridian's assumed annual dispute volume of **180,000 cases**.

It does **not** estimate savings yet.

The diagnostic lenses overlap. They must **not** be added together.

## Current-state scale

- Annual invoices: **1,000,000**
- Annual disputes: **180,000**
- Exception rate: **18%**
- Average active handling: **24.0 minutes/case**
- Annual active dispute-handling requirement: **72,000 hours**
- Active-handling capacity equivalent: **42.4 FTE**
- Stated dispute-team size: **52 FTE**
- Approximate annual fully loaded team cost: **$4.42M**

The gap between 52 team FTE and 42.4 active-handling FTE is **not assumed to be waste**. It can include supervision, QA, follow-up, waiting, administration, leave, meetings, and other responsibilities.

## Diagnostic impact lenses

| Lens | Annualized cases | Avg handling | Comparator | Associated gap | Annualized associated hours | FTE equiv. |
|---|---:|---:|---:|---:|---:|---:|
| Reopened cases | 25,200 | 40.2 min | 21.3 min | 18.9 min | 7,919 | 4.7 |
| Missing evidence | 21,600 | 27.0 min | 23.6 min | 3.4 min | 1,220 | 0.7 |
| 4+ systems accessed | 89,280 | 26.6 min | 21.4 min | 5.1 min | 7,619 | 4.5 |
| Escalated cases | 51,840 | 28.2 min | 22.3 min | 5.9 min | 5,092 | 3.0 |

### Reopened cases
Approximately **25,200 cases/year** are reopened at the observed 14% rate. Reopened cases consume about **40.2 minutes** of active handling versus **21.3 minutes** for non-reopened cases, an associated burden of roughly **7,919 active hours/year**.

This is not yet a savings claim: some reopened cases may be inherently more complex.

### Missing evidence
Approximately **21,600 cases/year** are marked as missing material evidence in the sample. Those cases take about **14.4 days** to resolve versus **5.8 days** without missing evidence, a gap of **8.7 days**.

The handling-time association is approximately **1,220 active hours/year**.

### High system complexity
Approximately **89,280 cases/year** touch four or more systems in the sample. These cases average **26.6 minutes** of handling versus **21.4 minutes** for cases touching fewer systems.

Again, this is descriptive: complex cases may require more systems because they are complex.

### Escalated cases
Approximately **51,840 cases/year** end in ESCALATE at the observed rate. Their workload should not automatically be considered avoidable because escalation is often an appropriate control.

## Why this matters for source-backed

Atlas can now enter opportunity mapping with a ranked understanding of **scale and burden**, rather than treating every pain point as equally important.

The next stage can ask:

> For each material problem, is the appropriate intervention AI, deterministic logic, workflow automation, human judgment, policy/process change, or a hybrid?

Only after that classification will Atlas estimate a realizable business case.
