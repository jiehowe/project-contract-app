PRINT_FORMATS = [
    {
        "name": "Project Contract Summary",
        "doc_type": "Project Contract",
        "module": "Project Contract",
        "standard": "Yes",
        "custom_format": 1,
        "disabled": 0,
        "print_format_type": "Jinja",
        "raw_printing": 0,
        "html": """
<style>
  .contract-print {
    font-size: 11px;
    color: #1f2937;
    line-height: 1.45;
  }
  .contract-print .header-table,
  .contract-print .meta-table,
  .contract-print .amount-table,
  .contract-print .milestone-table {
    width: 100%;
    border-collapse: collapse;
  }
  .contract-print .header-table td {
    vertical-align: top;
    padding-bottom: 12px;
  }
  .contract-print .eyebrow {
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 10px;
    color: #6b7280;
  }
  .contract-print h1 {
    margin: 0;
    font-size: 24px;
    color: #111827;
  }
  .contract-print h3 {
    margin: 18px 0 8px;
    font-size: 13px;
    text-transform: uppercase;
    color: #374151;
  }
  .contract-print .meta-table td,
  .contract-print .amount-table td {
    padding: 4px 0;
  }
  .contract-print .label {
    color: #6b7280;
    width: 34%;
  }
  .contract-print .value-strong {
    font-weight: 600;
  }
  .contract-print .summary-band {
    margin: 12px 0 18px;
    padding: 10px 12px;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
  }
  .contract-print .milestone-table th,
  .contract-print .milestone-table td {
    border: 1px solid #d1d5db;
    padding: 8px;
    text-align: left;
    vertical-align: top;
  }
  .contract-print .milestone-table th {
    background: #f9fafb;
    color: #374151;
    font-weight: 600;
  }
  .contract-print .text-right {
    text-align: right;
  }
  .contract-print .muted {
    color: #6b7280;
  }
</style>

<div class="contract-print">
  <table class="header-table">
    <tr>
      <td>
        <div class="eyebrow">Project Contract</div>
        <h1>{{ doc.name }}</h1>
        <div class="muted">{{ doc.contract_title or "" }}</div>
      </td>
      <td class="text-right">
        <div><strong>Status:</strong> {{ doc.status or "" }}</div>
        <div><strong>Type:</strong> {{ doc.contract_type or "" }}</div>
        <div><strong>Signed:</strong> {{ doc.get_formatted("signed_date") or "Pending" }}</div>
      </td>
    </tr>
  </table>

  <div class="summary-band">
    <table class="amount-table">
      <tr>
        <td class="label">Contract Value</td>
        <td class="value-strong">{{ doc.get_formatted("contract_value") or "" }}</td>
        <td class="label">Revised Value</td>
        <td class="value-strong">{{ doc.get_formatted("revised_contract_value") or "" }}</td>
      </tr>
      <tr>
        <td class="label">Billed</td>
        <td>{{ doc.get_formatted("total_billed_amount") or "" }}</td>
        <td class="label">Remaining</td>
        <td>{{ doc.get_formatted("remaining_contract_value") or "" }}</td>
      </tr>
    </table>
  </div>

  <table class="meta-table">
    <tr>
      <td class="label">Customer</td>
      <td>{{ doc.customer or "" }}</td>
      <td class="label">Project</td>
      <td>{{ doc.project or "" }}</td>
    </tr>
    <tr>
      <td class="label">Company</td>
      <td>{{ doc.company or "" }}</td>
      <td class="label">Project Manager</td>
      <td>{{ doc.project_manager or "" }}</td>
    </tr>
    <tr>
      <td class="label">Start Date</td>
      <td>{{ doc.get_formatted("start_date") or "" }}</td>
      <td class="label">End Date</td>
      <td>{{ doc.get_formatted("end_date") or "" }}</td>
    </tr>
    <tr>
      <td class="label">Billing Frequency</td>
      <td>{{ doc.billing_frequency or "" }}</td>
      <td class="label">Payment Terms</td>
      <td>{{ doc.payment_terms_template or "" }}</td>
    </tr>
  </table>

  {% if doc.milestones %}
  <h3>Milestones</h3>
  <table class="milestone-table">
    <thead>
      <tr>
        <th>Milestone</th>
        <th>Planned Date</th>
        <th class="text-right">Percentage</th>
        <th class="text-right">Amount</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      {% for row in doc.milestones %}
      <tr>
        <td>
          <div class="value-strong">{{ row.milestone_name or "" }}</div>
          {% if row.description %}
          <div class="muted">{{ row.description }}</div>
          {% endif %}
        </td>
        <td>{{ row.get_formatted("planned_date") or "" }}</td>
        <td class="text-right">{{ row.percentage or "" }}</td>
        <td class="text-right">{{ row.get_formatted("amount") or "" }}</td>
        <td>{{ row.completion_status or "" }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  {% endif %}

  {% if doc.terms_and_conditions %}
  <h3>Terms and Conditions</h3>
  <div>{{ doc.terms_and_conditions }}</div>
  {% endif %}

  {% if doc.internal_notes %}
  <h3>Internal Notes</h3>
  <div>{{ doc.internal_notes }}</div>
  {% endif %}
</div>
""",
    }
]
