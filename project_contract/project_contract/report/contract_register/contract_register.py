import frappe
from frappe import _


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
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "fieldname": "contract_type",
            "label": _("Contract Type"),
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "fieldname": "start_date",
            "label": _("Start Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "end_date",
            "label": _("End Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "contract_value",
            "label": _("Contract Value"),
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "fieldname": "total_variation_amount",
            "label": _("Variation Value"),
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "fieldname": "revised_contract_value",
            "label": _("Revised Value"),
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "fieldname": "total_billed_amount",
            "label": _("Billed"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "remaining_contract_value",
            "label": _("Remaining"),
            "fieldtype": "Currency",
            "width": 120,
        },
    ]


def get_data(filters):
    contract_filters = {}

    if filters.get("company"):
        contract_filters["company"] = filters.get("company")
    if filters.get("customer"):
        contract_filters["customer"] = filters.get("customer")
    if filters.get("status"):
        contract_filters["status"] = filters.get("status")
    if filters.get("from_date"):
        contract_filters["start_date"] = [">=", filters.get("from_date")]
    if filters.get("to_date"):
        if contract_filters.get("start_date"):
            contract_filters["start_date"] = ["between", [filters.get("from_date"), filters.get("to_date")]]
        else:
            contract_filters["start_date"] = ["<=", filters.get("to_date")]

    return frappe.get_all(
        "Project Contract",
        filters=contract_filters,
        fields=[
            "name",
            "contract_title",
            "customer",
            "project",
            "company",
            "status",
            "contract_type",
            "start_date",
            "end_date",
            "contract_value",
            "total_variation_amount",
            "revised_contract_value",
            "total_billed_amount",
            "remaining_contract_value",
            "currency",
        ],
        order_by="modified desc",
    )
