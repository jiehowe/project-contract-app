# Project Contract and Document Management Apps

Installable Frappe app scaffold for ERPNext project contract, subcontract, and
document management.

This repository contains two installable Frappe apps:

- `project_contract` - project contract and subcontract commercial control
- `document_management` - separate document-control app that can link back to contracts and subcontracts

## Install

From your bench directory:

```bash
bench get-app https://github.com/jiehowe/project-contract-app.git
bench --site your-site-name install-app project_contract
python3 - <<'PY'
from pathlib import Path

apps_txt = Path("sites/apps.txt")
apps = apps_txt.read_text().splitlines()
if "document_management" not in apps:
    apps.append("document_management")
apps_txt.write_text("\n".join(apps) + "\n")
PY
bench --site your-site-name install-app document_management
bench migrate
```

`document_management` is a second Frappe app shipped in the same repository.
Bench may register only `project_contract` in `sites/apps.txt` after
`bench get-app`, so add `document_management` to `sites/apps.txt` before
installing it. Keep it on its own line; a malformed line such as
`project_contractdocument_management` will prevent Frappe from importing either
app name correctly.

## Current scope

The `project_contract` app includes the first working DocType layer:

- `Project Contract`
- `Project Contract Milestone`
- `Contract Variation`

Server-side validation currently covers:

- contract date validation
- activation signature checks
- milestone percentage and amount rollups
- variation rollups into revised contract value

ERPNext integration currently includes:

- custom `project_contract` link on `Project`
- custom `project_contract` link on `Sales Invoice`
- billed amount rollup from submitted Sales Invoices back to the contract

Reporting currently includes:

- `Contract Register` script report for contract pipeline and value tracking
- `Expiring Contracts` script report for near-term expiry monitoring
- `Variation Summary` script report for commercial change tracking

The `project_contract` app also includes the first subcontract-management slice:

- `Subcontract`
- `Subcontract Scope Item`
- `Subcontract Claim`
- `Subcontract Claim Item`
- `Subcontract Variation`

Subcontract support currently includes:

- supplier-side contract validation and financial rollups
- approved variation rollups into revised subcontract value
- certified claim rollups into subcontract commitment tracking
- `Purchase Invoice` links for subcontract and subcontract claim
- `Subcontract Register` and `Claims Awaiting Certification` reports

The repository also includes a separate document-management app:

- `Project Document`
- `Project Document Link`

Document support currently includes:

- one register for incoming, outgoing, and internal project documents
- correspondence threading through reply and root document links
- generic links from a document to contracts, subcontracts, claims, invoices, and future records
- validation for reply chains, counterparty selection, and issued / received movement dates

This is intentionally not mixed into the `project_contract` app. It remains
interlinked through `Project Document Link`, which can point to `Project
Contract`, `Contract Variation`, `Subcontract`, `Subcontract Variation`,
`Subcontract Claim`, ERPNext invoices, and future records.

Status control currently includes:

- guarded contract transitions for Draft, Review, Approval, Active, Suspended, Closed, Cancelled, and Expired

Daily automation currently includes:

- automatic move to `Expired` when end date has passed

Printing currently includes:

- `Project Contract Summary` print format synced on install and migrate

See [project_contract_app_spec.md](project_contract_app_spec.md) for the planned
ERPNext contract model.

See [subcontract_app_spec.md](subcontract_app_spec.md) for the subcontract
management design.

See [document_management_spec.md](document_management_spec.md) for the document
management design.
