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
    }
