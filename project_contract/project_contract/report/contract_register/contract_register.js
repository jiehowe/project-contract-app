frappe.query_reports["Contract Register"] = {
  filters: [
    {
      fieldname: "company",
      label: __("Company"),
      fieldtype: "Link",
      options: "Company"
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
      options: "\nDraft\nUnder Review\nApproved\nActive\nSuspended\nClosed\nCancelled\nExpired"
    },
    {
      fieldname: "from_date",
      label: __("Start Date From"),
      fieldtype: "Date"
    },
    {
      fieldname: "to_date",
      label: __("Start Date To"),
      fieldtype: "Date"
    }
  ]
};
