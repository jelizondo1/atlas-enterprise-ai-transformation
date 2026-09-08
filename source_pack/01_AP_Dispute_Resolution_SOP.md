# MERIDIAN RETAIL GROUP
## Accounts Payable — Supplier Invoice Dispute Resolution SOP

**Document ID:** AP-OPS-104  
**Version:** 3.4  
**Owner:** Director, Accounts Payable Operations  
**Effective date:** January 15, 2026  
**Applies to:** U.S. and Mexico shared-services AP operations

### 1. Purpose
This SOP defines the standard process for investigating and resolving supplier invoice exceptions that cannot be processed through Meridian Retail Group’s standard automated invoice-matching workflow.

The objective is to ensure supplier disputes are resolved accurately, consistently, and within applicable service-level requirements while protecting Meridian from duplicate, incorrect, unsupported, or unauthorized payments.

### 2. Scope
This procedure applies to supplier invoice exceptions originating from merchandise, logistics, facilities, marketing, and indirect-procurement spend.

Invoices successfully matched through standard three-way matching are outside scope.

Cases involving suspected fraud, sanctions issues, litigation, or material regulatory concerns must be escalated immediately to Finance, Legal, or Compliance.

### 3. Systems used
**SAP S/4HANA** is the system of record for purchase orders, invoices, goods receipts, payment status, and vendor master data.

**Coupa Supplier Portal** is used for supplier submissions, supporting documentation, and selected dispute communications.

**Microsoft Outlook** is used for communication with suppliers and internal stakeholders when the required party does not interact directly through Coupa.

**SharePoint** contains supplier contracts, amendments, promotional agreements, freight agreements, and other commercial documentation.

The **Transportation Management System (TMS)** must be referenced for freight, carrier, shipment, and delivery-related disputes.

Analysts are responsible for documenting final case disposition in SAP regardless of where supporting information was obtained.

### 4. Initial exception review
When an invoice fails automated validation, SAP creates an invoice exception and assigns an exception reason code when sufficient information is available.

Standard reason codes include PRICE_MISMATCH, QUANTITY_MISMATCH, MISSING_RECEIPT, DUPLICATE, FREIGHT, TAX, CONTRACT_TERM, and OTHER.

The assigned analyst must confirm that the system-generated reason code reflects the actual issue before proceeding.

### 5. Investigation requirements
The analyst must establish the factual basis of the dispute before making a resolution decision.

At minimum, the analyst should review the invoice, purchase order, goods receipt when applicable, prior payment history when relevant, supplier-provided documentation, and commercial terms necessary to determine the correct amount.

Additional evidence may include buyer correspondence, receiving records, freight records, contract amendments, promotional agreements, or previous disputes involving the same supplier.

Analysts should avoid requesting documentation already available in Meridian systems.

Where commercial terms are unclear, the analyst should first review available supplier agreements before contacting Procurement.

### 6. Supplier and internal follow-up
If required information cannot be located, the analyst must request missing evidence from the appropriate party.

Cases awaiting external information should remain open with status **PENDING INFORMATION**. The analyst is responsible for monitoring pending cases and following up when responses are overdue.

### 7. Resolution options
**PAY_AS_INVOICED** — evidence supports the full supplier invoice amount.  
**PAY_PO_AMOUNT** — purchase-order amount governs and no approved exception supports the higher amount.  
**PARTIAL_ADJUSTMENT** — only part of the disputed amount is valid.  
**REQUEST_CREDIT_NOTE** — supplier must issue a corrected invoice or credit.  
**REJECT_DISPUTE** — supplier claim is unsupported.  
**ESCALATE** — analyst lacks sufficient authority, evidence, or clarity.

An escalation must include a summary, evidence reviewed, disputed amount, analyst recommendation when available, and the specific decision required.

### 8. Approval authority
Resolution authority is based on the disputed amount, not total invoice value.

- Below $10,000: AP Analyst
- $10,000–$50,000: AP Team Lead
- $50,000–$250,000: AP Manager
- Above $250,000: Finance Director; Procurement should be included when commercial terms or supplier relationships are material

Analysts must not split disputes to remain below an approval threshold.

### 9. Service levels
Standard disputes: **5 business days**.  
Priority suppliers: **3 business days**.  
Disputes above $250,000: **initial review within 2 business days**.

Time spent PENDING INFORMATION remains visible in overall resolution-time reporting.

### 10. Case documentation
Before closure, the analyst must enter sufficient SAP notes for another qualified employee to understand the cause, evidence reviewed, applicable commercial terms, calculations, final decision, approvals, and required supplier communication.

Notes such as “fixed,” “per buyer,” “supplier issue,” or “approved” without context are insufficient.

### 11. Supplier communication
Suppliers must be notified when a dispute results in rejection, partial adjustment, credit-note request, or payment different from the submitted invoice.

### 12. Escalation guidance
Escalate when documents conflict, contract language is ambiguous, the supplier disputes interpretation, required evidence cannot be obtained, the case involves unusual precedent, authority is exceeded, or material supplier/financial/legal/operational risk exists.

Escalation should not be used solely because a case is time-consuming.

### 13. Quality review
AP Team Leads periodically review decision accuracy, documentation quality, approval compliance, and supplier communication.

### 14. Reopened disputes
A case may be reopened if the supplier provides new evidence, Meridian identifies a processing error, or an internal stakeholder challenges the resolution. The reason must be documented.
