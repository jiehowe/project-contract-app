def get_custom_fields():
    return {
        "Project": [
            {
                "fieldname": "project_contract_section",
                "fieldtype": "Section Break",
                "label": "Project Contract",
                "insert_after": "status",
            },
            {
                "fieldname": "project_contract",
                "fieldtype": "Link",
                "label": "Primary Project Contract",
                "options": "Project Contract",
                "insert_after": "project_contract_section",
            },
        ],
        "Sales Invoice": [
            {
                "fieldname": "project_contract_section",
                "fieldtype": "Section Break",
                "label": "Project Contract",
                "insert_after": "project",
            },
            {
                "fieldname": "project_contract",
                "fieldtype": "Link",
                "label": "Project Contract",
                "options": "Project Contract",
                "insert_after": "project_contract_section",
                "fetch_from": "project.project_contract",
                "fetch_if_empty": 1,
                "in_standard_filter": 1,
            },
        ],
        "Purchase Invoice": [
            {
                "fieldname": "subcontract_section",
                "fieldtype": "Section Break",
                "label": "Subcontract",
                "insert_after": "project",
            },
            {
                "fieldname": "subcontract",
                "fieldtype": "Link",
                "label": "Subcontract",
                "options": "Subcontract",
                "insert_after": "subcontract_section",
                "in_standard_filter": 1,
            },
            {
                "fieldname": "subcontract_claim",
                "fieldtype": "Link",
                "label": "Subcontract Claim",
                "options": "Subcontract Claim",
                "insert_after": "subcontract",
                "in_standard_filter": 1,
            },
        ],
    }
