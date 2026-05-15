import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, flt

from project_contract.subcontract_management.utils import get_subcontract_variation_total


class SubcontractVariation(Document):
    def validate(self):
        self.populate_subcontract_context()
        self.validate_effective_date()
        self.validate_days_extension()
        self.calculate_revised_completion_date()
        self.validate_contract_sum_floor()

    def on_update(self):
        self.update_subcontract_rollup()

    def on_trash(self):
        self.update_subcontract_rollup()

    def populate_subcontract_context(self):
        if not self.subcontract:
            return

        subcontract = frappe.get_cached_doc("Subcontract", self.subcontract)
        self.supplier = subcontract.supplier
        self.currency = subcontract.currency

        if subcontract.status in {"Cancelled", "Closed"} and self.status in {"Approved", "Applied"}:
            frappe.throw(_("Variations cannot be approved or applied against closed or cancelled subcontracts."))

    def validate_effective_date(self):
        if self.status in {"Approved", "Applied"} and not self.effective_date:
            frappe.throw(_("Effective date is required before a variation can be approved or applied."))

    def validate_days_extension(self):
        if flt(self.days_extension) < 0:
            frappe.throw(_("Days extension cannot be negative."))

    def calculate_revised_completion_date(self):
        self.revised_completion_date = None
        if not self.subcontract:
            return

        completion_date = frappe.db.get_value("Subcontract", self.subcontract, "completion_date")
        if completion_date:
            self.revised_completion_date = add_days(completion_date, flt(self.days_extension))

    def validate_contract_sum_floor(self):
        if not self.subcontract or self.status not in {"Approved", "Applied"}:
            return

        original_sum = flt(frappe.db.get_value("Subcontract", self.subcontract, "original_contract_sum"))
        existing_variations = get_subcontract_variation_total(self.subcontract, exclude_name=self.name)
        if original_sum + existing_variations + flt(self.value_change) < 0:
            frappe.throw(_("Applied variations cannot reduce the revised contract sum below zero."))

    def update_subcontract_rollup(self):
        if not self.subcontract:
            return

        subcontract = frappe.get_doc("Subcontract", self.subcontract)
        subcontract.calculate_financials()
        frappe.db.set_value(
            "Subcontract",
            subcontract.name,
            {
                "approved_variation_amount": subcontract.approved_variation_amount,
                "revised_contract_sum": subcontract.revised_contract_sum,
                "revised_completion_date": subcontract.revised_completion_date,
                "retention_held_amount": subcontract.retention_held_amount,
                "remaining_commitment": subcontract.remaining_commitment,
            },
            update_modified=False,
        )
