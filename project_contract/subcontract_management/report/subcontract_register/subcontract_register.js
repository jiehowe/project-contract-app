frappe.query_reports["Subcontract Register"] = {
  filters: [
    { fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
    { fieldname: "supplier", label: __("Supplier"), fieldtype: "Link", options: "Supplier" },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: "\nDraft\nUnder Review\nApproved\nActive\nSuspended\nCompleted\nClosed\nCancelled\nExpired"
    }
  ]
};
