# Project Contract App for ERPNext

## Goal

Build a custom Frappe app for ERPNext that manages project-based customer contracts from draft to closure, with approval, billing milestones, retention, and contract change control.

This app should sit between CRM/Sales and Project/Accounts:

- Sales closes the deal.
- Contracts controls the legal/commercial agreement.
- Projects executes against the approved contract.
- Accounts bills according to milestones, recurring schedules, or progress.

## Why a custom app

For a true project contract process, a custom app is better than only adding `Custom Field`s because you will likely need:

- new business objects
- approval workflow
- child tables for milestones and variations
- validation rules
- server-side automation
- role-based permissions
- print formats and reports

Frappe apps and DocTypes are the intended extension model for this kind of workflow.

## Proposed app name

- App name: `project_contract`
- Module name: `Project Contract`

## Version target

- Target platform: ERPNext / Frappe v16
- App dependency: ERPNext is required
- Use standard DocTypes and `doc_events` for lifecycle reactions on `Sales Invoice`
- Prefer v16 extension hooks such as `extend_doctype_class` only when adding methods or properties to standard DocType classes

## Main use cases

1. Create a contract for a customer and link it to a project.
2. Store contract value, dates, terms, retention, and billing method.
3. Track billing milestones and invoice readiness.
4. Manage contract amendments or variation orders.
5. Prevent work or billing against expired or unapproved contracts.
6. Give management a clear view of contract value, billed amount, balance, and exposure.

## Core DocTypes

### 1. Project Contract

Primary transaction DocType.

Suggested fields:

- `contract_number` - naming series
- `customer` - Link to `Customer`
- `project` - Link to `Project`
- `company` - Link to `Company`
- `status` - Draft / Under Review / Approved / Active / Suspended / Closed / Cancelled / Expired
- `contract_type` - Lump Sum / Time and Material / Recurring / Milestone Based
- `start_date`
- `end_date`
- `revised_end_date`
- `currency`
- `contract_value`
- `retention_percentage`
- `retention_amount`
- `billing_frequency` - One Time / Monthly / Quarterly / By Milestone / By Progress
- `payment_terms_template` - Link to `Payment Terms Template`
- `quotation` - optional Link to `Quotation`
- `sales_order` - optional Link to `Sales Order`
- `cost_center`
- `project_manager` - Link to `Employee` or `User`
- `signed_date`
- `signed_by_customer`
- `signed_by_company`
- `document_attachment`
- `terms_and_conditions`
- `internal_notes`

Suggested child tables:

- `milestones`
- `clauses`
- `approvals`
- `linked_variations`

### 2. Project Contract Milestone

Child table under `Project Contract`.

Suggested fields:

- `milestone_name`
- `description`
- `planned_date`
- `amount`
- `percentage`
- `billing_condition`
- `invoice_created`
- `sales_invoice`
- `completion_status`

### 3. Contract Variation

Separate DocType linked to a `Project Contract`.

Purpose:

- change scope
- extend dates
- revise value
- document approved change orders

Suggested fields:

- `project_contract`
- `variation_type` - Scope Change / Value Change / Time Extension / Rate Revision
- `effective_date`
- `description`
- `value_change`
- `days_extension`
- `status` - Draft / Pending Approval / Approved / Rejected / Applied
- `supporting_document`

On approval, this record can update the parent contract totals and dates.

### 4. Contract Invoice Request

Optional DocType for tighter billing control.

Use this if the business wants contract admins to trigger finance instead of allowing direct invoicing from the contract.

Suggested fields:

- `project_contract`
- `milestone`
- `request_date`
- `amount`
- `reason`
- `status` - Draft / Submitted / Approved / Invoiced / Cancelled
- `sales_invoice`

### 5. Contract Clause

Optional child table if you want searchable structured clauses instead of only a rich-text terms field.

Suggested fields:

- `clause_type`
- `title`
- `clause_text`
- `is_mandatory`

## Recommended workflow

### Contract lifecycle

1. Draft
2. Under Review
3. Approved
4. Active
5. Suspended
6. Closed
7. Cancelled
8. Expired

### Variation lifecycle

1. Draft
2. Pending Approval
3. Approved
4. Applied
5. Rejected

## ERPNext links

Keep the app connected to standard ERPNext masters and transactions:

- `Customer`
- `Project`
- `Quotation`
- `Sales Order`
- `Sales Invoice`
- `Company`
- `Cost Center`
- `Payment Terms Template`
- `File`

Recommended behavior:

- A contract should optionally be created from a `Quotation` or `Sales Order`.
- A project can reference one primary active contract.
- Sales invoices should carry a `project_contract` link for reporting.

## Business rules

Suggested first-pass validations:

1. `end_date` must be after `start_date`.
2. `contract_value` must be positive for fixed-value contracts.
3. Milestone percentages should total 100 percent for milestone-based contracts.
4. No activation without required approval and signed date.
5. No invoicing when contract status is not `Active`.
6. Variation cannot be applied unless approved.
7. Total billed amount must not exceed contract value plus approved variations unless explicitly allowed.

## Automation ideas

Server-side hooks or DocType methods:

- On contract approval, set status to `Active` if signature conditions are met.
- On variation apply, update contract value and end date.
- On approved or applied variations, roll the latest revised end date back to the parent contract.
- On invoice creation, update billed amount on the contract.
- Daily scheduled job:
  - mark contracts as `Expired` when end date passes
  - notify project manager 30 days before expiry
  - notify finance for upcoming billable milestones

## Dashboard and reports

### Workspace / module view

Create a `Project Contract` workspace with shortcuts for:

- Contracts
- Variations
- Invoice Requests
- Expiring Contracts
- Pending Approvals
- Billing Due This Month

### Useful reports

- Contract Register
- Expiring Contracts
- Contract vs Billed Value
- Milestone Billing Status
- Variation Summary
- Retention Outstanding

## Roles and permissions

Suggested roles:

- `Contract Manager`
- `Project Manager`
- `Accounts User`
- `Sales User`
- `Legal Reviewer`

Suggested permission logic:

- Sales can create draft contracts from quotations.
- Contract Manager can submit and amend.
- Legal Reviewer can review and approve.
- Project Manager can view active contracts and update milestone completion.
- Accounts User can create invoices from approved billing requests or approved milestones.

## Minimal MVP

If you want to keep phase 1 lean, build only:

1. `Project Contract`
2. `Project Contract Milestone`
3. `Contract Variation`
4. workflow
5. basic dashboard fields:
   - total variations
   - total billed
   - remaining contract value
6. one print format
7. two reports:
   - Contract Register
   - Expiring Contracts

## Suggested technical build sequence

1. Create app scaffold:

```bash
bench new-app project_contract
```

2. Install app on the site:

```bash
bench --site your-site-name install-app project_contract
```

3. Enable developer mode if needed for tracked DocType files.

4. Create DocTypes in this order:

- Project Contract
- Project Contract Milestone
- Contract Variation
- Contract Invoice Request

5. Add workflow and permissions.

6. Add custom link field on `Sales Invoice` and optionally on `Project`.

7. Add server scripts or app Python methods for validations and rollups.

8. Build print format and reports.

9. Add notifications for expiry and billing due dates.

## Implementation notes

- Use a custom app, not only site-level customization, if this will be reused across sites or environments.
- Keep milestone and variation logic in Python methods, not only client-side scripts.
- Start with standard Desk forms before building a custom front-end.
- Use naming series for `Project Contract` such as `PC-.YYYY.-`.

## Recommended first version

The best first version for most companies is:

- one contract per project
- milestone-based billing
- approval workflow
- variation handling
- invoice linkage
- expiry reminders

That gives you strong operational control without making the app too heavy.

## References

- Frappe app creation: https://docs.frappe.io/framework/user/en/tutorial/create-an-app
- Frappe DocType tutorial: https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype
- Frappe apps overview: https://docs.frappe.io/framework/user/en/basics/apps
- ERPNext customization overview: https://docs.frappe.io/erpnext/user/manual/en/customize-erpnext
