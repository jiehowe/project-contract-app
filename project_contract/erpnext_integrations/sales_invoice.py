import frappe
from frappe import _
from frappe.utils import flt


def validate_sales_invoice(doc, method=None):
    project_contract = getattr(doc, "project_contract", None)
    if not project_contract:
        return

    contract = frappe.get_cached_doc("Project Contract", project_contract)

    if contract.status != "Active":
        frappe.throw(_("Only active project contracts can be used on Sales Invoices."))

    if contract.customer and doc.customer and contract.customer != doc.customer:
        frappe.throw(_("Sales Invoice customer must match the linked project contract customer."))

    if contract.project and doc.project and contract.project != doc.project:
        frappe.throw(_("Sales Invoice project must match the linked project contract project."))

    if contract.currency and doc.currency and contract.currency != doc.currency:
        frappe.throw(_("Sales Invoice currency must match the linked project contract currency."))


def update_contract_billed_amount(doc, method=None):
    project_contract = getattr(doc, "project_contract", None)
    if not project_contract:
        return

    refresh_contract_billed_amount(project_contract)


def refresh_contract_billed_amount(project_contract: str):
    totals = frappe.get_all(
        "Sales Invoice",
        filters={"project_contract": project_contract, "docstatus": 1},
        fields=["sum(grand_total) as total_billed_amount"],
    )
    total_billed_amount = flt(totals[0].get("total_billed_amount")) if totals else 0.0

    contract = frappe.get_doc("Project Contract", project_contract)
    contract.total_billed_amount = total_billed_amount
    contract.calculate_financials()

    frappe.db.set_value(
        "Project Contract",
        project_contract,
        {
            "total_billed_amount": contract.total_billed_amount,
            "retention_amount": contract.retention_amount,
            "total_variation_amount": contract.total_variation_amount,
            "revised_contract_value": contract.revised_contract_value,
            "remaining_contract_value": contract.remaining_contract_value,
        },
        update_modified=False,
    )
