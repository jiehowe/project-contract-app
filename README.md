# Project Contract App

Installable Frappe app scaffold for ERPNext project contract management.

This repository now contains the base app structure needed for `bench get-app`
and `bench --site <site> install-app project_contract`.

## Install

From your bench directory:

```bash
bench get-app https://github.com/jiehowe/project-contract-app.git
bench --site your-site-name install-app project_contract
bench migrate
```

## Current scope

The app now includes the first working DocType layer:

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

Status control currently includes:

- guarded contract transitions for Draft, Review, Approval, Active, Suspended, Closed, Cancelled, and Expired

Daily automation currently includes:

- automatic move to `Expired` when end date has passed

Printing currently includes:

- `Project Contract Summary` print format synced on install and migrate

See [project_contract_app_spec.md](project_contract_app_spec.md) for the planned
ERPNext contract model.
