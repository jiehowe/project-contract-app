import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {"fieldname":"name","label":_("Claim"),"fieldtype":"Link","options":"Subcontract Claim","width":150},
        {"fieldname":"subcontract","label":_("Subcontract"),"fieldtype":"Link","options":"Subcontract","width":150},
        {"fieldname":"supplier","label":_("Supplier"),"fieldtype":"Link","options":"Supplier","width":180},
        {"fieldname":"project","label":_("Project"),"fieldtype":"Link","options":"Project","width":150},
        {"fieldname":"claim_date","label":_("Claim Date"),"fieldtype":"Date","width":110},
        {"fieldname":"status","label":_("Status"),"fieldtype":"Data","width":120},
        {"fieldname":"current_certified_amount","label":_("Current Amount"),"fieldtype":"Currency","width":130},
        {"fieldname":"net_certified_amount","label":_("Net Amount"),"fieldtype":"Currency","width":130},
    ]


def get_data(filters):
    claim_filters = {"status": ["in", ["Submitted", "Under Review"]]}
    for fieldname in ("project", "supplier", "subcontract"):
        if filters.get(fieldname):
            claim_filters[fieldname] = filters.get(fieldname)

    return frappe.get_all(
        "Subcontract Claim",
        filters=claim_filters,
        fields=[
            "name", "subcontract", "supplier", "project", "claim_date", "status",
            "current_certified_amount", "net_certified_amount", "currency",
        ],
        order_by="claim_date asc",
    )
