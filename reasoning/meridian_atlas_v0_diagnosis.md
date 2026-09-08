# ATLAS v0 — Meridian Current-State Diagnosis

## Executive summary

1. Meridian's dispute-resolution workflow is a **multi-system evidence-reconstruction process**, not merely an invoice-matching exception queue. Analysts must combine transactional data, supplier documentation, operational records, and supplier-specific commercial terms before resolving many cases.

2. Deterministic baseline performance is weak relative to Meridian's stated service levels: **62% SLA attainment**, **6.8 business days** average resolution time, and a **14% reopen rate**.

3. Evidence completeness is a major diagnostic signal. Cases marked as missing evidence achieved only **13.3% SLA attainment**, compared with **68.6%** when evidence was available.

4. Supplier-specific agreements materially alter standard handling rules. NorthStar, Apex, and Solara each contain exceptions that can change the correct treatment of pricing, freight, dispute windows, quantities, services, and escalation.

5. The current process relies heavily on analyst judgment to distinguish clear cases from those requiring Procurement, Tax, Receiving, Logistics, or management authority.

## Current-state process

**P1. Invoice validation & exception creation**  
SAP creates an exception when standard validation fails and assigns a reason code where possible.

**P2. Reason verification & evidence collection**  
AP validates the issue and searches SAP, Coupa, SharePoint, Outlook, TMS, receiving records, and supplier documents as required.

**P3. Root-cause & policy determination**  
The analyst identifies the governing rule, including supplier-specific amendments and document precedence.

**P4. Information request / escalation**  
If evidence is missing or authority/interpretation is insufficient, the case is routed to the supplier or an internal specialist function.

**P5. Resolution & approval**  
A disposition is selected and approved according to disputed amount and special policy requirements.

**P6. System update, communication & closure**  
SAP is updated, case notes are entered, suppliers are notified when required, and the case is closed.

**P7. Quality review / reopening**  
Cases may be reopened if new evidence, an internal challenge, or a prior processing error emerges.

## Quantitative baseline

| Metric | Current state |
|---|---:|
| Cases analyzed | 250 |
| Avg handling time | 24.0 min |
| Avg resolution time | 6.8 days |
| SLA attainment | 62.0% |
| Reopen rate | 14.0% |
| Missing-evidence rate | 12.0% |
| Avg systems accessed | 3.3 |

## Key diagnostic findings

### 1. Information fragmentation
Analysts must assemble evidence from several systems and repositories. This creates search effort, context switching, and dependence on evidence completeness.

### 2. Missing evidence materially degrades performance
Missing-evidence cases have **13.3% SLA attainment** versus **68.6%** otherwise.

### 3. Supplier-specific terms create policy complexity
Generic AP policy is insufficient for many cases because supplier-specific executed terms can supersede it.

### 4. Historical precedent is a weak control
Prior case treatment may be outdated, erroneous, or explicitly one-time, yet weak notes can make precedent look authoritative.

### 5. Reopened disputes represent significant rework
Reopened cases require **40.2 minutes** average handling versus **21.3 minutes** for non-reopened cases.

### 6. Some cases require component-level resolution
Mixed invoices can contain simultaneously valid and invalid components; the process cannot always be treated as a binary invoice-level decision.

### 7. Specialist escalation is part of the operating model
Correct handling depends on analysts recognizing when Procurement, Tax, Logistics, Receiving, or higher approval authority is required.

## Material source conflict

**Solara 2026 freight terms:** executed amendments expired at the end of 2025, a Procurement email says to continue the arrangement into 2026, and an unsigned draft proposes new terms. The source material is insufficient for AP to establish the governing 2026 commercial term independently.

## Diagnostic hypotheses to test next

1. **Evidence retrieval/completeness is a material driver of cycle time.**
2. **Contract/policy interpretation contributes disproportionately to high-complexity cases.**
3. **Analyst variation may partly reflect uneven institutional knowledge and escalation judgment rather than productivity alone.**

## Boundary

This diagnosis intentionally makes **no recommendation about AI, automation, software, organization design, or target-state workflow**.
