import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from project_contract.subcontract_management.utils import get_subcontract_certified_total


class SubcontractClaim(Document):
    def validate(self):
        self.populate_subcontract_context()
        self.validate_dates()
        self.validate_items()
        self.calculate_amounts()
        self.validate_certification_limit()

    def on_update(self):
        self.update_subcontract_rollup()

    def on_trash(self):
        self.update_subcontract_rollup()

    def populate_subcontract_context(self):
        if not self.subcontract:
            return

        subcontract = frappe.get_cached_doc("Subcontract", self.subcontract)
        self.supplier = subcontract.supplier
        self.project = subcontract.project
        self.currency = subcontract.currency

        if subcontract.status not in {"Active", "Completed", "Closed"} and self.status != "Draft":
            frappe.throw(_("Claims can only be submitted against active or completed subcontracts."))

    def validate_dates(self):
        if self.claim_period_from and self.claim_period_to and self.claim_period_to < self.claim_period_from:
            frappe.throw(_("Claim period end date cannot be before start date."))

    def validate_items(self):
        if not self.claim_items:
            frappe.throw(_("At least one claim item is required."))

        for row in self.claim_items:
            row.cumulative_quantity = flt(row.previous_quantity) + flt(row.current_quantity)
            row.current_amount = flt(row.current_quantity) * flt(row.rate)
            row.cumulative_amount = row.cumulative_quantity * flt(row.rate)

            if row.cumulative_quantity > flt(row.contract_quantity):
                frappe.throw(_("Cumulative quantity cannot exceed contract quantity for claim item {0}.").format(row.idx))

    def calculate_amounts(self):
        self.current_certified_amount = sum(flt(row.current_amount) for row in self.claim_items)
        self.cumulative_certified_amount = sum(flt(row.cumulative_amount) for row in self.claim_items)
        subcontract = frappe.get_cached_doc("Subcontract", self.subcontract) if self.subcontract else None
        retention_percentage = flt(subcontract.retention_percentage) if subcontract else 0.0
        self.retention_amount = self.current_certified_amount * retention_percentage / 100
        self.net_certified_amount = self.current_certified_amount - flt(self.retention_amount)

    def validate_certification_limit(self):
        if not self.subcontract or self.status not in {"Certified", "Invoiced", "Paid"}:
            return

        subcontract = frappe.get_cached_doc("Subcontract", self.subcontract)
        existing_total = get_subcontract_certified_total(self.subcontract, exclude_name=self.name)
        if existing_total + flt(self.net_certified_amount) > flt(subcontract.revised_contract_sum) + 0.01:
            frappe.throw(_("Certified claims cannot exceed the revised contract sum."))

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
                "certified_amount": subcontract.certified_amount,
                "retention_held_amount": subcontract.retention_held_amount,
                "remaining_commitment": subcontract.remaining_commitment,
            },
            update_modified=False,
        )
