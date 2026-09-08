# ATLAS — Meridian Quantitative Diagnostic

## 1. Deterministic baseline

- Historical cases analyzed: **250**
- Total disputed value represented: **$8,352,523**
- Average active handling time: **24.0 min**
- Average final resolution time: **6.8 business days**
- SLA attainment: **62.0%**
- Reopen rate: **14.0%**
- Missing-evidence rate: **12.0%**
- Average systems accessed per case: **3.3**
- Average evidence types reviewed per case: **3.0**
- Cases coded OTHER at intake: **15.6%**
- Historical cases ending in ESCALATE: **28.8%**

## 2. Performance by system reason code

| Reason code | Cases | Share | Avg handling | Avg resolution | SLA | Reopen | Missing evidence |
|---|---:|---:|---:|---:|---:|---:|---:|
| PRICE_MISMATCH | 48 | 19.2% | 17.0 min | 3.7 d | 87.5% | 12.5% | 6.2% |
| QUANTITY_MISMATCH | 41 | 16.4% | 20.6 min | 3.1 d | 90.2% | 12.2% | 7.3% |
| OTHER | 39 | 15.6% | 31.8 min | 8.4 d | 48.7% | 15.4% | 10.3% |
| MISSING_RECEIPT | 34 | 13.6% | 24.4 min | 10.1 d | 35.3% | 8.8% | 32.4% |
| DUPLICATE | 31 | 12.4% | 11.1 min | 3.6 d | 83.9% | 9.7% | 9.7% |
| FREIGHT | 25 | 10.0% | 28.2 min | 7.3 d | 60.0% | 28.0% | 4.0% |
| CONTRACT_TERM | 20 | 8.0% | 42.9 min | 12.9 d | 15.0% | 15.0% | 25.0% |
| TAX | 12 | 4.8% | 30.2 min | 14.5 d | 8.3% | 16.7% | 0.0% |

## 3. Supplier profile

| Supplier | Cases | Avg handling | Avg resolution | SLA | Reopen | Avg systems |
|---|---:|---:|---:|---:|---:|---:|
| NorthStar Consumer Products | 59 | 24.5 min | 5.3 d | 71.2% | 5.1% | 3.4 |
| Apex Industrial Supply | 48 | 24.7 min | 5.8 d | 70.8% | 12.5% | 3.3 |
| Solara Imports | 46 | 23.2 min | 8.6 d | 45.7% | 26.1% | 3.3 |
| BluePeak Logistics | 28 | 24.0 min | 7.1 d | 60.7% | 10.7% | 3.4 |
| Harbor Home Goods | 28 | 27.6 min | 7.2 d | 64.3% | 21.4% | 3.6 |
| Pinnacle Packaging | 21 | 20.0 min | 7.2 d | 57.1% | 9.5% | 3.4 |
| Evergreen Facilities | 20 | 21.9 min | 8.3 d | 55.0% | 15.0% | 3.0 |

## 4. Observable complexity effects

### Missing evidence
- Cases with missing evidence: **30**
- Avg resolution with missing evidence: **14.4 days** vs **5.8 days** without it.
- SLA attainment with missing evidence: **13.3%** vs **68.6%** without it.

### Reopened cases
- Reopened cases: **35**
- Avg handling when reopened: **40.2 min** vs **21.3 min** otherwise.
- Avg resolution when reopened: **10.2 days** vs **6.3 days** otherwise.

### Systems touched

| Systems accessed | Cases | Avg handling | Avg resolution | SLA | Reopen |
|---|---:|---:|---:|---:|---:|
| 2 systems | 46 | 14.1 min | 5.7 d | 69.6% | 15.2% |
| 3 systems | 80 | 25.7 min | 6.8 d | 61.3% | 12.5% |
| 4 systems | 116 | 25.8 min | 7.1 d | 60.3% | 13.8% |
| 5+ systems | 8 | 37.2 min | 9.2 d | 50.0% | 25.0% |

## 5. Correlations (descriptive, not causal)

- Systems accessed vs handling time: **0.30**
- Systems accessed vs resolution time: **0.09**
- Evidence types reviewed vs handling time: **0.06**
- Evidence types reviewed vs resolution time: **0.15**
- Handling time vs resolution time: **0.33**

These are descriptive relationships only. Atlas should not infer causality from them without additional evidence.

## 6. Data-boundary notes

- This analysis uses only client-facing historical case fields.
- It does **not** use the `_evaluation_only_DO_NOT_INGEST` ground-truth folder.
- It does **not** determine whether historical resolutions were correct.
- It does **not** recommend AI, automation, or target-state solutions.
- System reason codes are analyzed as recorded operational data; this layer cannot independently determine classification accuracy.

This report is intended to be fed into Atlas' reasoning layer as deterministic quantitative evidence.