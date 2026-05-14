import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("Variation"),
            "fieldtype": "Link",
            "options": "Contract Variation",
            "width": 150,
        },
        {
            "fieldname": "project_contract",
            "label": _("Project Contract"),
            "fieldtype": "Link",
            "options": "Project Contract",
            "width": 150,
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 180,
        },
        {
            "fieldname": "variation_type",
            "label": _("Variation Type"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "fieldname": "effective_date",
            "label": _("Effective Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "days_extension",
            "label": _("Days Extension"),
            "fieldtype": "Int",
            "width": 110,
        },
        {
            "fieldname": "value_change",
            "label": _("Value Change"),
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "fieldname": "revised_end_date",
            "label": _("Revised End Date"),
            "fieldtype": "Date",
            "width": 110,
        },
        {
            "fieldname": "owner",
            "label": _("Owner"),
            "fieldtype": "Data",
            "width": 140,
        },
    ]


def get_data(filters):
    variation_filters = {}

    if filters.get("project_contract"):
        variation_filters["project_contract"] = filters.get("project_contract")
    if filters.get("customer"):
        variation_filters["customer"] = filters.get("customer")
    if filters.get("status"):
        variation_filters["status"] = filters.get("status")
    if filters.get("from_date"):
        variation_filters["effective_date"] = [">=", filters.get("from_date")]
    if filters.get("to_date"):
        if variation_filters.get("effective_date"):
            variation_filters["effective_date"] = ["between", [filters.get("from_date"), filters.get("to_date")]]
        else:
            variation_filters["effective_date"] = ["<=", filters.get("to_date")]

    return frappe.get_all(
        "Contract Variation",
        filters=variation_filters,
        fields=[
            "name",
            "project_contract",
            "customer",
            "variation_type",
            "status",
            "effective_date",
            "days_extension",
            "value_change",
            "revised_end_date",
            "currency",
            "owner",
        ],
        order_by="modified desc",
    )
