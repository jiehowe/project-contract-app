import frappe
from frappe import _
from frappe.utils import flt


def validate_purchase_invoice(doc, method=None):
    subcontract_name = getattr(doc, "subcontract", None)
    claim_name = getattr(doc, "subcontract_claim", None)

    if not subcontract_name and not claim_name:
        return

    if claim_name:
        claim = frappe.get_cached_doc("Subcontract Claim", claim_name)
        if claim.status not in {"Certified", "Invoiced", "Paid"}:
            frappe.throw(_("Only certified subcontract claims can be linked to Purchase Invoices."))

        if subcontract_name and claim.subcontract != subcontract_name:
            frappe.throw(_("Subcontract Claim must belong to the linked subcontract."))

        subcontract_name = claim.subcontract
        doc.subcontract = subcontract_name

    subcontract = frappe.get_cached_doc("Subcontract", subcontract_name)
    if subcontract.status not in {"Active", "Completed", "Closed"}:
        frappe.throw(_("Only active or completed subcontracts can be used on Purchase Invoices."))

    if subcontract.supplier and doc.supplier and subcontract.supplier != doc.supplier:
        frappe.throw(_("Purchase Invoice supplier must match the linked subcontract supplier."))

    if subcontract.project and doc.project and subcontract.project != doc.project:
        frappe.throw(_("Purchase Invoice project must match the linked subcontract project."))

    if subcontract.currency and doc.currency and subcontract.currency != doc.currency:
        frappe.throw(_("Purchase Invoice currency must match the linked subcontract currency."))


def update_subcontract_invoiced_amount(doc, method=None):
    subcontract_name = getattr(doc, "subcontract", None)
    if subcontract_name:
        refresh_subcontract_invoiced_amount(subcontract_name)

    claim_name = getattr(doc, "subcontract_claim", None)
    if claim_name:
        update_claim_invoice_status(claim_name)


def refresh_subcontract_invoiced_amount(subcontract_name: str):
    totals = frappe.get_all(
        "Purchase Invoice",
        filters={"subcontract": subcontract_name, "docstatus": 1},
        fields=["sum(grand_total) as invoiced_amount"],
    )
    invoiced_amount = flt(totals[0].get("invoiced_amount")) if totals else 0.0

    subcontract = frappe.get_doc("Subcontract", subcontract_name)
    subcontract.invoiced_amount = invoiced_amount
    subcontract.calculate_financials()

    frappe.db.set_value(
        "Subcontract",
        subcontract_name,
        {
            "approved_variation_amount": subcontract.approved_variation_amount,
            "revised_contract_sum": subcontract.revised_contract_sum,
            "certified_amount": subcontract.certified_amount,
            "invoiced_amount": subcontract.invoiced_amount,
            "retention_held_amount": subcontract.retention_held_amount,
            "remaining_commitment": subcontract.remaining_commitment,
        },
        update_modified=False,
    )


def update_claim_invoice_status(claim_name: str):
    claim = frappe.get_doc("Subcontract Claim", claim_name)
    submitted_invoice_exists = frappe.db.exists(
        "Purchase Invoice",
        {"subcontract_claim": claim_name, "docstatus": 1},
    )
    next_status = "Invoiced" if submitted_invoice_exists else "Certified"

    if claim.status in {"Certified", "Invoiced"} and claim.status != next_status:
        frappe.db.set_value("Subcontract Claim", claim.name, "status", next_status, update_modified=False)
