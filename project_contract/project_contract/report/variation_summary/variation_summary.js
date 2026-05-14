frappe.query_reports["Variation Summary"] = {
  filters: [
    {
      fieldname: "project_contract",
      label: __("Project Contract"),
      fieldtype: "Link",
      options: "Project Contract"
    },
    {
      fieldname: "customer",
      label: __("Customer"),
      fieldtype: "Link",
      options: "Customer"
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: "\nDraft\nPending Approval\nApproved\nApplied\nRejected"
    },
    {
      fieldname: "from_date",
      label: __("Effective Date From"),
      fieldtype: "Date"
    },
    {
      fieldname: "to_date",
      label: __("Effective Date To"),
      fieldtype: "Date"
    }
  ]
};
