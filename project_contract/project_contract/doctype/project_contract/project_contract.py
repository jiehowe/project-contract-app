import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from project_contract.project_contract.utils import get_project_contract_variation_total


class ProjectContract(Document):
    ALLOWED_STATUS_TRANSITIONS = {
        "Draft": {"Draft", "Under Review", "Cancelled"},
        "Under Review": {"Under Review", "Approved", "Draft", "Cancelled"},
        "Approved": {"Approved", "Active", "Under Review", "Cancelled"},
        "Active": {"Active", "Suspended", "Closed", "Expired", "Cancelled"},
        "Suspended": {"Suspended", "Active", "Closed", "Cancelled"},
        "Closed": {"Closed"},
        "Cancelled": {"Cancelled"},
        "Expired": {"Expired", "Active", "Closed"},
    }

    def validate(self):
        self.validate_status_transition()
        self.validate_dates()
        self.validate_contract_value()
        self.validate_linked_documents()
        self.validate_activation_requirements()
        self.validate_milestones()
        self.calculate_financials()

    def validate_status_transition(self):
        previous_status = None
        if not self.is_new():
            previous_status = frappe.db.get_value("Project Contract", self.name, "status")

        if not previous_status:
            return

        allowed = self.ALLOWED_STATUS_TRANSITIONS.get(previous_status, {previous_status})
        if self.status not in allowed:
            frappe.throw(
                _("Project Contract cannot move from status {0} to {1}.").format(previous_status, self.status)
            )

    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            frappe.throw(_("End date cannot be before start date."))

    def validate_contract_value(self):
        if self.contract_type != "Time and Material" and flt(self.contract_value) <= 0:
            frappe.throw(_("Contract value must be greater than zero for this contract type."))

    def validate_activation_requirements(self):
        if self.status != "Active":
            return

        if not self.signed_date:
            frappe.throw(_("Signed date is required before a contract can be activated."))

        if not self.signed_by_customer or not self.signed_by_company:
            frappe.throw(_("Both customer and company signatures are required before activation."))

    def validate_linked_documents(self):
        if self.project:
            project_customer = frappe.db.get_value("Project", self.project, "customer")
            if project_customer and self.customer and project_customer != self.customer:
                frappe.throw(_("Project customer must match the contract customer."))

        if self.sales_order:
            sales_order_customer = frappe.db.get_value("Sales Order", self.sales_order, "customer")
            if sales_order_customer and self.customer and sales_order_customer != self.customer:
                frappe.throw(_("Sales Order customer must match the contract customer."))

        if self.quotation:
            quotation_party = frappe.db.get_value("Quotation", self.quotation, "party_name")
            if quotation_party and self.customer and quotation_party != self.customer:
                frappe.throw(_("Quotation party must match the contract customer."))

    def validate_milestones(self):
        if self.contract_type != "Milestone Based":
            return

        if not self.milestones:
            frappe.throw(_("At least one milestone is required for milestone-based contracts."))

        percentages = [flt(row.percentage) for row in self.milestones if flt(row.percentage)]
        if percentages:
            if len(percentages) != len(self.milestones):
                frappe.throw(_("Enter a percentage for every milestone or leave all milestone percentages blank."))

            total_percentage = sum(percentages)
            if abs(total_percentage - 100) > 0.001:
                frappe.throw(_("Milestone percentages must total 100%."))

        amounts = [flt(row.amount) for row in self.milestones if flt(row.amount)]
        if amounts:
            if len(amounts) != len(self.milestones):
                frappe.throw(_("Enter an amount for every milestone or leave all milestone amounts blank."))

            if flt(self.contract_value) and abs(sum(amounts) - flt(self.contract_value)) > 0.01:
                frappe.throw(_("Milestone amounts must equal the contract value."))

    def calculate_financials(self):
        contract_value = flt(self.contract_value)
        retention_percentage = flt(self.retention_percentage)
        billed_amount = flt(self.total_billed_amount)

        self.retention_amount = contract_value * retention_percentage / 100
        self.total_variation_amount = (
            get_project_contract_variation_total(self.name) if self.name and not self.is_new() else 0.0
        )
        self.revised_contract_value = contract_value + flt(self.total_variation_amount)
        self.remaining_contract_value = self.revised_contract_value - billed_amount
