import frappe
from frappe.utils import add_days, getdate, nowdate


def run_daily_contract_maintenance():
    expire_due_contracts()


def expire_due_contracts(today=None):
    today = getdate(today or nowdate())

    contracts = frappe.get_all(
        "Project Contract",
        filters={
            "status": ["in", ["Approved", "Active", "Suspended"]],
            "end_date": ["<", today],
        },
        fields=["name"],
    )

    for contract in contracts:
        frappe.db.set_value("Project Contract", contract.name, "status", "Expired", update_modified=False)

    return len(contracts)


def get_upcoming_expiry_contracts(days=30, today=None):
    today = getdate(today or nowdate())
    cutoff_date = add_days(today, days)

    return frappe.get_all(
        "Project Contract",
        filters={
            "status": ["in", ["Approved", "Active", "Suspended"]],
            "end_date": ["between", [today, cutoff_date]],
        },
        fields=[
            "name",
            "contract_title",
            "customer",
            "project",
            "company",
            "project_manager",
            "status",
            "end_date",
            "remaining_contract_value",
        ],
        order_by="end_date asc",
    )
