# Document Management System for ERPNext

## Goal

Build a project-centered document-control module for ERPNext that records all
incoming and outgoing correspondence, preserves the relationship between
letters, and keeps non-letter documents in the same searchable register.

This should be a separate Frappe app named `document_management`, not a module
inside the `project_contract` app. It should still connect to the commercial
records already managed by the contract and subcontract app:

- award letters received from clients
- award letters issued to subcontractors
- contract correspondence
- subcontract correspondence
- claims, certificates, notices, drawings, minutes, and supporting documents

## Design principle

Use one primary DocType, `Project Document`, for every controlled document.
Letters are not split into separate incoming and outgoing DocTypes because they
share the same metadata, filing rules, attachments, and downstream links.
Instead, use:

- `document_type` to classify the record
- `direction` to distinguish incoming, outgoing, and internal documents
- `reply_to_document` and `root_document` to preserve correspondence chains
- child-table links to attach one document to many business records

This gives one register, one search surface, and one correspondence timeline.

## App boundary

- App name: `document_management`
- Module name: `Document Management`
- Required app: `erpnext`
- Optional companion app: `project_contract`

Do not make `document_management` depend directly on `project_contract`. The
interlink should remain data-driven through Dynamic Link rows in `Project
Document Link`, so the document app can be installed independently and can still
link to `Project Contract` or `Subcontract` when those DocTypes exist on the
site.

## Core use cases

1. Register an incoming letter from a client.
2. Issue an outgoing reply and link it back to the incoming letter.
3. See all correspondence in the same thread.
4. Store general project documents such as awards, contracts, claims, drawings,
   certificates, meeting minutes, and photos.
5. Link the same document to a `Project Contract`, `Subcontract`, variation,
   claim, invoice, or any future project record without redesigning the schema.
6. Track whether a document is draft, issued, received, superseded, archived,
   or cancelled.

## Core DocTypes

### 1. Project Document

Primary transaction DocType and document register.

Suggested fields:

- `naming_series`
- `document_title`
- `document_type`
- `direction` - Incoming / Outgoing / Internal
- `status` - Draft / Registered / Received / Issued / Superseded / Archived / Cancelled
- `project`
- `company`
- `document_date`
- `received_date`
- `sent_date`
- `reference_number`
- `customer`
- `supplier`
- `counterparty_name`
- `reply_to_document`
- `root_document`
- `subject`
- `summary`
- `attachment`
- `related_records`

Recommended document types:

- Letter
- Award Letter
- Contract
- Subcontract
- Variation
- Claim
- Certificate
- Drawing
- Report
- Meeting Minutes
- Notice
- Photo
- Other

### 2. Project Document Link

Child table under `Project Document`.

Suggested fields:

- `reference_doctype`
- `reference_name`
- `relationship_type`
- `remarks`

Purpose:

- attach one controlled document to many operational records
- support both current records and future app modules through Dynamic Link

Recommended relationship types:

- Supports
- Relates To
- Awards
- Replies To
- Supersedes
- Evidence For

## Correspondence model

Example:

1. Client sends award letter.
   - `document_type = Award Letter`
   - `direction = Incoming`
   - linked to `Project Contract`
2. Company sends acceptance / clarification letter.
   - `document_type = Letter`
   - `direction = Outgoing`
   - `reply_to_document = <client award letter>`
   - `root_document = <client award letter>`
3. Later replies continue the same thread by pointing to the most recent letter.

This allows:

- one-click traceability from reply to original letter
- a full thread view by filtering on `root_document`
- mixed incoming/outgoing exchanges in one chain

## Links to current app

Use `Project Document Link` rows to connect documents to:

- `Project Contract`
- `Contract Variation`
- `Subcontract`
- `Subcontract Variation`
- `Subcontract Claim`
- `Sales Invoice`
- `Purchase Invoice`

Examples:

- client award letter linked to a `Project Contract` with relationship `Awards`
- subcontract award letter linked to a `Subcontract` with relationship `Awards`
- subcontractor claim attachment linked to `Subcontract Claim` with relationship `Supports`

## Business rules

1. `received_date` is required for incoming documents once marked `Received`.
2. `sent_date` is required for outgoing documents once marked `Issued`.
3. A document cannot be both customer-facing and supplier-facing at the same
   time unless it is explicitly filed only by free-text `counterparty_name`.
4. `reply_to_document` must belong to the same project when both records have a
   project.
5. A document cannot reply to itself.
6. Reply documents inherit the root thread document from the referenced record.
7. `root_document` should be set to self for the first document in a thread.

## Recommended workflow

### Incoming document

1. Draft
2. Registered
3. Received
4. Archived

### Outgoing document

1. Draft
2. Registered
3. Issued
4. Archived

### Exceptional states

- Superseded
- Cancelled

## Reporting ideas

- Incoming Correspondence Register
- Outgoing Correspondence Register
- Open Correspondence Awaiting Reply
- Documents by Project
- Documents by Linked Contract / Subcontract
- Superseded Documents

## Future enhancements

- document numbering by project and document type
- review / approval workflow before issue
- distribution list and acknowledgement tracking
- reminders for correspondence requiring response
- revision control for drawings and reports
- barcode / QR labels for physical filing
- workspace dashboard and thread view
