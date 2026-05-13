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

This is the app scaffold plus the contract design spec. The business DocTypes and
workflow are not implemented yet.

See [project_contract_app_spec.md](project_contract_app_spec.md) for the planned
ERPNext contract model.
