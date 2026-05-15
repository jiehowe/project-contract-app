import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from project_contract.subcontract_management.utils import (
    get_subcontract_certified_total,
    get_subcontract_revised_completion_date,
    get_subcontract_variation_total,
)


class Subcontract(Document):
    ALLOWED_STATUS_TRANSITIONS = {
        "Draft": {"Draft", "Under Review", "Cancelled"},
        "Under Review": {"Under Review", "Approved", "Draft", "Cancelled"},
        "Approved": {"Approved", "Active", "Under Review", "Cancelled"},
        "Active": {"Active", "Suspended", "Completed", "Expired", "Cancelled"},
        "Suspended": {"Suspended", "Active", "Completed", "Cancelled"},
        "Completed": {"Completed", "Closed"},
        "Closed": {"Closed"},
        "Cancelled": {"Cancelled"},
        "Expired": {"Expired", "Active", "Closed"},
    }

    def validate(self):
        self.validate_status_transition()
        self.validate_dates()
        self.validate_contract_sum()
        self.validate_linked_documents()
        self.validate_activation_requirements()
        self.validate_scope_items()
        self.calculate_financials()

    def validate_status_transition(self):
        previous_status = None
        if not self.is_new():
            previous_status = frappe.db.get_value("Subcontract", self.name, "status")

        if not previous_status:
            return

        allowed = self.ALLOWED_STATUS_TRANSITIONS.get(previous_status, {previous_status})
        if self.status not in allowed:
            frappe.throw(_("Subcontract cannot move from status {0} to {1}.").format(previous_status, self.status))

    def validate_dates(self):
        if self.start_date and self.completion_date and self.completion_date < self.start_date:
            frappe.throw(_("Completion date cannot be before start date."))

    def validate_contract_sum(self):
        if flt(self.original_contract_sum) <= 0:
            frappe.throw(_("Original contract sum must be greater than zero."))

    def validate_linked_documents(self):
        if self.supplier_quotation:
            quotation_supplier = frappe.db.get_value("Supplier Quotation", self.supplier_quotation, "supplier")
            if quotation_supplier and self.supplier and quotation_supplier != self.supplier:
                frappe.throw(_("Supplier Quotation supplier must match the subcontract supplier."))

        if self.purchase_order:
            purchase_order_supplier = frappe.db.get_value("Purchase Order", self.purchase_order, "supplier")
            if purchase_order_supplier and self.supplier and purchase_order_supplier != self.supplier:
                frappe.throw(_("Purchase Order supplier must match the subcontract supplier."))

    def validate_activation_requirements(self):
        if self.status != "Active":
            return

        if not self.signed_date:
            frappe.throw(_("Signed date is required before a subcontract can be activated."))

        if not self.signed_by_company or not self.signed_by_supplier:
            frappe.throw(_("Both company and supplier signatures are required before activation."))

    def validate_scope_items(self):
        if not self.scope_items:
            frappe.throw(_("At least one scope item is required."))

        if self.contract_type not in {"Unit Rate", "Lump Sum"}:
            return

        total_scope_amount = sum(flt(row.amount) for row in self.scope_items)
        if abs(total_scope_amount - flt(self.original_contract_sum)) > 0.01:
            frappe.throw(_("Scope item amounts must equal the original contract sum."))

    def calculate_financials(self):
        original_sum = flt(self.original_contract_sum)
        retention_percentage = flt(self.retention_percentage)

        self.approved_variation_amount = (
            get_subcontract_variation_total(self.name) if self.name and not self.is_new() else 0.0
        )
        self.revised_contract_sum = original_sum + flt(self.approved_variation_amount)
        self.revised_completion_date = (
            get_subcontract_revised_completion_date(self.name) if self.name and not self.is_new() else None
        )
        self.certified_amount = (
            get_subcontract_certified_total(self.name) if self.name and not self.is_new() else 0.0
        )
        retention_base = min(self.certified_amount, self.revised_contract_sum)
        self.retention_held_amount = retention_base * retention_percentage / 100
        self.remaining_commitment = self.revised_contract_sum - flt(self.certified_amount)
