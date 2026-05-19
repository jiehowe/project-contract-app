import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, flt

from project_contract.project_contract.utils import get_project_contract_variation_total


class ContractVariation(Document):
    def validate(self):
        self.populate_contract_context()
        self.validate_effective_date()
        self.validate_days_extension()
        self.calculate_revised_end_date()
        self.validate_contract_value_floor()

    def on_update(self):
        self.update_contract_rollup()

    def on_trash(self):
        self.update_contract_rollup()

    def populate_contract_context(self):
        if not self.project_contract:
            return

        contract = frappe.get_cached_doc("Project Contract", self.project_contract)
        self.customer = contract.customer
        self.currency = contract.currency

        if contract.status in {"Cancelled", "Closed"} and self.status in {"Approved", "Applied"}:
            frappe.throw(_("Variations cannot be approved or applied against closed or cancelled contracts."))

    def validate_effective_date(self):
        if self.status in {"Approved", "Applied"} and not self.effective_date:
            frappe.throw(_("Effective date is required before a variation can be approved or applied."))

    def validate_days_extension(self):
        if flt(self.days_extension) < 0:
            frappe.throw(_("Days extension cannot be negative."))

    def calculate_revised_end_date(self):
        self.revised_end_date = None
        if not self.project_contract:
            return

        contract_end_date = frappe.db.get_value("Project Contract", self.project_contract, "end_date")
        if contract_end_date:
            self.revised_end_date = add_days(contract_end_date, flt(self.days_extension))

    def validate_contract_value_floor(self):
        if not self.project_contract or self.status not in {"Approved", "Applied"}:
            return

        contract_value = flt(frappe.db.get_value("Project Contract", self.project_contract, "contract_value"))
        existing_variations = get_project_contract_variation_total(self.project_contract, exclude_name=self.name)
        revised_value = contract_value + existing_variations + flt(self.value_change)

        if revised_value < 0:
            frappe.throw(_("Applied variations cannot reduce the revised contract value below zero."))

    def update_contract_rollup(self):
        if not self.project_contract:
            return

        contract = frappe.get_doc("Project Contract", self.project_contract)
        contract.calculate_financials()

        frappe.db.set_value(
            "Project Contract",
            contract.name,
            {
                "total_variation_amount": contract.total_variation_amount,
                "revised_contract_value": contract.revised_contract_value,
                "revised_end_date": contract.revised_end_date,
                "remaining_contract_value": contract.remaining_contract_value,
            },
            update_modified=False,
        )
