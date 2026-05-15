frappe.query_reports["Claims Awaiting Certification"] = {
  filters: [
    { fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
    { fieldname: "supplier", label: __("Supplier"), fieldtype: "Link", options: "Supplier" },
    { fieldname: "subcontract", label: __("Subcontract"), fieldtype: "Link", options: "Subcontract" }
  ]
};
