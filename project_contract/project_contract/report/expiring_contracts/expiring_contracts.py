from frappe import _

from project_contract.tasks.daily import get_upcoming_expiry_contracts


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("Contract"),
            "fieldtype": "Link",
            "options": "Project Contract",
            "width": 150,
        },
        {
            "fieldname": "contract_title",
            "label": _("Title"),
            "fieldtype": "Data",
            "width": 220,
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 180,
        },
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 150,
        },
        {
            "fieldname": "company",
            "label": _("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "width": 150,
        },
        {
            "fieldname": "project_manager",
            "label": _("Project Manager"),
            "fieldtype": "Link",
            "options": "User",
            "width": 160,
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "end_date",
            "label": _("End Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "remaining_contract_value",
            "label": _("Remaining Value"),
            "fieldtype": "Currency",
            "width": 130,
        },
    ]


def get_data(filters):
    days = int(filters.get("days") or 30)
    rows = get_upcoming_expiry_contracts(days=days)

    if filters.get("company"):
        rows = [row for row in rows if row.company == filters.get("company")]
    if filters.get("customer"):
        rows = [row for row in rows if row.customer == filters.get("customer")]

    return rows
