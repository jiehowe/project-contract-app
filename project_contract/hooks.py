app_name = "project_contract"
app_title = "Project Contract"
app_publisher = "Jie Howe"
app_description = "Project contract management app for ERPNext"
app_email = "support@example.com"
app_license = "MIT"
app_version = "0.0.1"

# Modules
# -------

fixtures = []

# Install hooks
# -------------

after_install = "project_contract.install.after_install"
after_migrate = "project_contract.install.after_migrate"

doc_events = {
    "Sales Invoice": {
        "validate": "project_contract.erpnext_integrations.sales_invoice.validate_sales_invoice",
        "on_submit": "project_contract.erpnext_integrations.sales_invoice.update_contract_billed_amount",
        "on_cancel": "project_contract.erpnext_integrations.sales_invoice.update_contract_billed_amount",
        "on_update_after_submit": "project_contract.erpnext_integrations.sales_invoice.update_contract_billed_amount",
    },
    "Purchase Invoice": {
        "validate": "project_contract.erpnext_integrations.purchase_invoice.validate_purchase_invoice",
        "on_submit": "project_contract.erpnext_integrations.purchase_invoice.update_subcontract_invoiced_amount",
        "on_cancel": "project_contract.erpnext_integrations.purchase_invoice.update_subcontract_invoiced_amount",
        "on_update_after_submit": "project_contract.erpnext_integrations.purchase_invoice.update_subcontract_invoiced_amount",
    },
}

scheduler_events = {
    "daily": [
        "project_contract.tasks.daily.run_daily_contract_maintenance",
    ]
}
