import frappe
from frappe.utils import flt


APPROVED_VARIATION_STATUSES = ("Approved", "Applied")


def get_project_contract_variation_total(project_contract: str, exclude_name: str | None = None) -> float:
    if not project_contract:
        return 0.0

    filters = {
        "project_contract": project_contract,
        "status": ["in", APPROVED_VARIATION_STATUSES],
    }
    if exclude_name:
        filters["name"] = ["!=", exclude_name]

    result = frappe.get_all(
        "Contract Variation",
        filters=filters,
        fields=["sum(value_change) as total_value_change"],
    )
    if not result:
        return 0.0

    return flt(result[0].get("total_value_change"))
