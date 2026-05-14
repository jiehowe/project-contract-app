import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from project_contract.custom_fields import get_custom_fields
from project_contract.print_formats import PRINT_FORMATS


def after_install():
    create_custom_fields(get_custom_fields())
    sync_print_formats()


def after_migrate():
    create_custom_fields(get_custom_fields())
    sync_print_formats()


def sync_print_formats():
    for print_format in PRINT_FORMATS:
        upsert_print_format(print_format)


def upsert_print_format(data):
    existing_name = frappe.db.exists("Print Format", data["name"])

    if existing_name:
        doc = frappe.get_doc("Print Format", existing_name)
        for key, value in data.items():
            setattr(doc, key, value)
        doc.save(ignore_permissions=True)
        return

    doc = frappe.get_doc({"doctype": "Print Format", **data})
    doc.insert(ignore_permissions=True)
