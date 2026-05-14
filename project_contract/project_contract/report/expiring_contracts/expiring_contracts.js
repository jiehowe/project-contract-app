frappe.query_reports["Expiring Contracts"] = {
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
      fieldname: "days",
      label: __("Expiring Within (Days)"),
      fieldtype: "Int",
      default: 30,
      reqd: 1
    }
  ]
};
