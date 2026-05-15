import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {"fieldname":"name","label":_("Subcontract"),"fieldtype":"Link","options":"Subcontract","width":150},
        {"fieldname":"subcontract_title","label":_("Title"),"fieldtype":"Data","width":220},
        {"fieldname":"project","label":_("Project"),"fieldtype":"Link","options":"Project","width":150},
        {"fieldname":"supplier","label":_("Supplier"),"fieldtype":"Link","options":"Supplier","width":180},
        {"fieldname":"status","label":_("Status"),"fieldtype":"Data","width":110},
        {"fieldname":"contract_type","label":_("Contract Type"),"fieldtype":"Data","width":130},
        {"fieldname":"original_contract_sum","label":_("Original Sum"),"fieldtype":"Currency","width":130},
        {"fieldname":"approved_variation_amount","label":_("Variations"),"fieldtype":"Currency","width":120},
        {"fieldname":"revised_contract_sum","label":_("Revised Sum"),"fieldtype":"Currency","width":130},
        {"fieldname":"certified_amount","label":_("Certified"),"fieldtype":"Currency","width":120},
        {"fieldname":"invoiced_amount","label":_("Invoiced"),"fieldtype":"Currency","width":120},
        {"fieldname":"remaining_commitment","label":_("Remaining"),"fieldtype":"Currency","width":120},
    ]


def get_data(filters):
    subcontract_filters = {}
    for fieldname in ("project", "supplier", "status"):
        if filters.get(fieldname):
            subcontract_filters[fieldname] = filters.get(fieldname)

    return frappe.get_all(
        "Subcontract",
        filters=subcontract_filters,
        fields=[
            "name", "subcontract_title", "project", "supplier", "status", "contract_type",
            "original_contract_sum", "approved_variation_amount", "revised_contract_sum",
            "certified_amount", "invoiced_amount", "remaining_commitment", "currency",
        ],
        order_by="modified desc",
    )
