# Subcontract Management App for ERPNext

## Goal

Build a custom Frappe app that manages subcontract agreements from tendering to final settlement, with control over scope, values, progress claims, retention, variations, and supplier performance.

This app should sit between Projects, Buying, and Accounts:

- Projects defines the package of work to outsource.
- Procurement appoints the subcontractor.
- Contract administrators manage the commercial agreement.
- Site teams certify progress.
- Accounts pays only against approved claims.

## Recommended app name

- App name: `subcontract_management`
- Module name: `Subcontract Management`

## Core use cases

1. Create subcontract packages linked to a project and cost code.
2. Compare supplier quotations and award a subcontract.
3. Store subcontract sum, dates, scope, retention, and payment terms.
4. Track work items, progress claims, certified values, and retention.
5. Manage variation orders and extensions of time.
6. Link approved claims to purchase invoices for payment control.
7. Monitor committed cost, revised cost, certified cost, paid cost, and remaining exposure.

## Scope boundary

Use standard ERPNext documents where they already fit:

- `Supplier`
- `Project`
- `Supplier Quotation`
- `Purchase Order`
- `Purchase Invoice`
- `Payment Terms Template`
- `Cost Center`
- `Item`

Add custom DocTypes only for construction-style subcontract control that standard buying transactions do not model cleanly:

- subcontract package / award
- bill of quantities style scope lines
- progress claim certification
- subcontract variation control
- retention release

## Core DocTypes

### 1. Subcontract

Primary transaction DocType for the awarded supplier agreement.

Suggested fields:

- `naming_series`
- `subcontract_title`
- `status` - Draft / Under Review / Approved / Active / Suspended / Completed / Closed / Cancelled / Expired
- `project`
- `company`
- `supplier`
- `supplier_quotation`
- `purchase_order`
- `cost_center`
- `contract_type` - Lump Sum / Unit Rate / Reimbursable / Framework
- `trade_package`
- `currency`
- `original_contract_sum`
- `approved_variation_amount`
- `revised_contract_sum`
- `certified_amount`
- `invoiced_amount`
- `paid_amount`
- `remaining_commitment`
- `retention_percentage`
- `retention_cap_percentage`
- `retention_held_amount`
- `advance_payment_amount`
- `start_date`
- `completion_date`
- `revised_completion_date`
- `defects_liability_end_date`
- `payment_terms_template`
- `project_manager`
- `contract_administrator`
- `signed_date`
- `signed_by_company`
- `signed_by_supplier`
- `scope_summary`
- `terms_and_conditions`
- `document_attachment`

Suggested child tables:

- `scope_items`
- `payment_milestones`
- `linked_variations`
- `insurance_requirements`
- `performance_securities`

### 2. Subcontract Scope Item

Child table under `Subcontract`.

Suggested fields:

- `item_code`
- `description`
- `uom`
- `quantity`
- `rate`
- `amount`
- `cost_code`
- `work_section`
- `is_provisional_sum`
- `is_daywork`

Purpose:

- Works like a lightweight BOQ / schedule of rates.
- Supports both lump-sum and measured work subcontracts.

### 3. Subcontract Claim

Separate DocType for monthly or milestone-based progress claims.

Suggested fields:

- `subcontract`
- `claim_period_from`
- `claim_period_to`
- `claim_date`
- `status` - Draft / Submitted / Under Review / Certified / Rejected / Invoiced / Paid
- `claimed_amount`
- `previously_certified_amount`
- `current_certified_amount`
- `cumulative_certified_amount`
- `retention_amount`
- `less_advance_recovery`
- `net_certified_amount`
- `purchase_invoice`
- `supporting_document`
- `certified_by`
- `certified_on`

Suggested child table:

- `claim_items`

### 4. Subcontract Claim Item

Child table under `Subcontract Claim`.

Suggested fields:

- `scope_item`
- `description`
- `contract_quantity`
- `previous_quantity`
- `current_quantity`
- `cumulative_quantity`
- `rate`
- `current_amount`
- `cumulative_amount`
- `remarks`

### 5. Subcontract Variation

Separate DocType linked to a `Subcontract`.

Suggested fields:

- `subcontract`
- `variation_type` - Addition / Omission / Rate Revision / Provisional Sum Adjustment / Time Extension
- `status` - Draft / Pending Approval / Approved / Applied / Rejected
- `instruction_date`
- `effective_date`
- `description`
- `value_change`
- `days_extension`
- `revised_completion_date`
- `supporting_document`
- `approved_by`
- `approved_on`

### 6. Retention Release

Separate DocType for controlled release of retained sums.

Suggested fields:

- `subcontract`
- `release_type` - Practical Completion / Final Completion / Manual
- `release_date`
- `eligible_amount`
- `released_amount`
- `status` - Draft / Approved / Paid / Cancelled
- `purchase_invoice`
- `remarks`

## Recommended workflow

### Subcontract lifecycle

1. Draft
2. Under Review
3. Approved
4. Active
5. Suspended
6. Completed
7. Closed
8. Cancelled
9. Expired

### Claim lifecycle

1. Draft
2. Submitted
3. Under Review
4. Certified
5. Invoiced
6. Paid
7. Rejected

### Variation lifecycle

1. Draft
2. Pending Approval
3. Approved
4. Applied
5. Rejected

### Retention release lifecycle

1. Draft
2. Approved
3. Paid
4. Cancelled

## ERPNext integrations

### Buying

- Link `Supplier Quotation` to preserve the commercial comparison trail.
- Link or generate `Purchase Order` from the approved subcontract.
- Link approved claims to `Purchase Invoice`.

### Projects

- Link every subcontract to a `Project`.
- Use `Cost Center` and optional cost code fields for package-level reporting.
- Roll subcontract commitment and certified cost into project commercial dashboards.

### Accounts

- Use `Purchase Invoice` for actual vendor billing.
- Keep payment status sourced from ERPNext accounting documents rather than duplicating ledger logic.

### Optional manufacturing subcontracting coexistence

- If the company also uses ERPNext's manufacturing subcontracting flow, keep this app scoped to commercial subcontract agreements for project work.
- Avoid overloading the standard manufacturing subcontracting records with construction-style claims, retention, and variation logic.

## Business rules

Suggested first-pass validations:

1. `completion_date` must be on or after `start_date`.
2. `original_contract_sum` must be positive before approval.
3. Scope item totals must equal the subcontract sum for measured or schedule-of-rates contracts.
4. No activation without approval, signed date, and both signature flags.
5. No claim submission unless the subcontract is `Active`.
6. Current cumulative certified quantity must not exceed contract quantity unless an approved variation exists.
7. Claim certification must not exceed revised contract sum.
8. Retention held must follow the configured percentage and cap.
9. A variation cannot be applied unless approved.
10. No final closeout while open claims, unpaid certified amounts, or unresolved variations remain.

## Automation ideas

- On approval, calculate revised contract sum and create the linked `Purchase Order` if desired.
- On approved variation application, update revised contract sum and revised completion date.
- On claim certification, update certified amount, retention held amount, and remaining commitment.
- On purchase invoice submission, update invoiced amount.
- On payment posting, update paid amount.
- Daily scheduled job:
  - flag overdue completion dates
  - notify contract administrators of pending claims
  - warn when retention release dates become due
  - surface subcontractors with expiring insurance or securities

## Workspace and dashboards

Create a `Subcontract Management` workspace with shortcuts for:

- Subcontracts
- Claims Awaiting Review
- Approved Variations
- Retention Releases
- Overdue Completion Dates
- Supplier Performance

Recommended dashboard fields on `Subcontract`:

- original contract sum
- approved variations
- revised contract sum
- certified amount
- invoiced amount
- paid amount
- retention held
- remaining commitment

## Reports

- Subcontract Register
- Commitment vs Certified vs Paid
- Claims Awaiting Certification
- Variation Summary
- Retention Outstanding
- Subcontractor Performance
- Overdue Subcontracts
- Project Package Cost Summary

## Roles and permissions

Suggested roles:

- `Subcontract Manager`
- `Project Manager`
- `Quantity Surveyor`
- `Procurement User`
- `Accounts User`
- `Approver`

Suggested permission model:

- Procurement can create draft subcontracts from supplier quotations.
- Quantity Surveyors can prepare claims and variations.
- Project Managers can review progress and completion.
- Approvers can approve awards, variations, and retention releases.
- Accounts Users can create invoices only from certified claims.
- General project users can view but not alter commercial values.

## Minimal MVP

Phase 1 should include only:

1. `Subcontract`
2. `Subcontract Scope Item`
3. `Subcontract Claim`
4. `Subcontract Claim Item`
5. `Subcontract Variation`
6. workflow and permissions
7. rollup fields on `Subcontract`
8. two reports:
   - Subcontract Register
   - Claims Awaiting Certification

Defer `Retention Release`, supplier scorecards, and advanced notifications to phase 2 unless they are immediately needed.

## Suggested technical build sequence

1. Create the `subcontract_management` app and module.
2. Build `Subcontract` and `Subcontract Scope Item`.
3. Add ERPNext links to `Supplier`, `Project`, `Supplier Quotation`, `Purchase Order`, and `Purchase Invoice`.
4. Build `Subcontract Variation` and revise-value rollups.
5. Build `Subcontract Claim` and `Subcontract Claim Item`.
6. Add workflow, permissions, and status guards.
7. Add print format for subcontract summary.
8. Add the first two operational reports.
9. Add scheduled reminders and retention release in a second pass.

## Recommended first version

The best first version for most project businesses is:

- one subcontract per awarded work package
- scope item schedule
- certified monthly claims
- approved variations
- retention tracking
- ERPNext purchase invoice linkage

That gives commercial control without rebuilding ERPNext's purchasing or accounting stack.

## Relationship to the existing Project Contract app

The existing `project_contract` app manages the customer-facing revenue contract.

This subcontract app would manage the supplier-facing cost contract.

Together they support a simple commercial chain:

1. `Project Contract` defines what the customer will pay.
2. `Subcontract` defines what the company commits to suppliers.
3. Project reporting compares revenue, committed cost, certified cost, billed revenue, and margin exposure.
