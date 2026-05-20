import frappe
from frappe import _
from frappe.model.document import Document


class ProjectDocument(Document):
    def validate(self):
        self.validate_direction_dates()
        self.validate_counterparty()
        self.validate_reply_document()
        self.populate_root_document()

    def after_insert(self):
        if not self.root_document:
            frappe.db.set_value(
                "Project Document",
                self.name,
                "root_document",
                self.name,
                update_modified=False,
            )

    def validate_direction_dates(self):
        if self.direction == "Incoming" and self.status == "Received" and not self.received_date:
            frappe.throw(_("Received date is required for received incoming documents."))

        if self.direction == "Outgoing" and self.status == "Issued" and not self.sent_date:
            frappe.throw(_("Sent date is required for issued outgoing documents."))

    def validate_counterparty(self):
        if self.customer and self.supplier:
            frappe.throw(_("Choose either a customer or a supplier, not both."))

    def validate_reply_document(self):
        if not self.reply_to_document:
            return

        if self.reply_to_document == self.name:
            frappe.throw(_("A document cannot reply to itself."))

        reply_project = frappe.db.get_value("Project Document", self.reply_to_document, "project")
        if self.project and reply_project and self.project != reply_project:
            frappe.throw(_("Reply documents must belong to the same project."))

    def populate_root_document(self):
        if not self.reply_to_document:
            return

        root_document = frappe.db.get_value("Project Document", self.reply_to_document, "root_document")
        self.root_document = root_document or self.reply_to_document
