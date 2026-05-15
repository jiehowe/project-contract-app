import frappe
from frappe.utils import flt


APPROVED_VARIATION_STATUSES = ("Approved", "Applied")
CERTIFIED_CLAIM_STATUSES = ("Certified", "Invoiced", "Paid")


def get_subcontract_variation_total(subcontract: str, exclude_name: str | None = None) -> float:
    if not subcontract:
        return 0.0

    filters = {"subcontract": subcontract, "status": ["in", APPROVED_VARIATION_STATUSES]}
    if exclude_name:
        filters["name"] = ["!=", exclude_name]

    result = frappe.get_all(
        "Subcontract Variation",
        filters=filters,
        fields=["sum(value_change) as total_value_change"],
    )
    return flt(result[0].get("total_value_change")) if result else 0.0


def get_subcontract_certified_total(subcontract: str, exclude_name: str | None = None) -> float:
    if not subcontract:
        return 0.0

    filters = {"subcontract": subcontract, "status": ["in", CERTIFIED_CLAIM_STATUSES]}
    if exclude_name:
        filters["name"] = ["!=", exclude_name]

    result = frappe.get_all(
        "Subcontract Claim",
        filters=filters,
        fields=["sum(net_certified_amount) as total_certified_amount"],
    )
    return flt(result[0].get("total_certified_amount")) if result else 0.0


def get_subcontract_revised_completion_date(subcontract: str):
    if not subcontract:
        return None

    result = frappe.get_all(
        "Subcontract Variation",
        filters={"subcontract": subcontract, "status": ["in", APPROVED_VARIATION_STATUSES]},
        fields=["max(revised_completion_date) as revised_completion_date"],
    )
    return result[0].get("revised_completion_date") if result else None
