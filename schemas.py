SCHEMAS = {
    "certificate_of_insurance": {
        "required_fields": [
            "insured_name", "insurer_name", "policy_number",
            "coverage_type", "coverage_amount", "effective_date",
            "expiry_date", "certificate_holder"
        ],
        "risk_rules": ["expiry_date", "coverage_amount", "insured_name"]
    },
    "vendor_contract": {
        "required_fields": [
            "party_a", "party_b", "effective_date", "term_length",
            "governing_law", "liability_cap", "termination_clause",
            "payment_terms"
        ],
        "risk_rules": ["liability_cap", "termination_clause", "expiry_date"]
    },
    "w9_tax_form": {
        "required_fields": [
            "legal_name", "business_name", "entity_type",
            "tin", "tin_type", "address", "signature_date"
        ],
        "risk_rules": ["legal_name", "tin"]
    },
    "nda": {
        "required_fields": [
            "disclosing_party", "receiving_party", "effective_date",
            "confidentiality_period", "governing_law", "scope"
        ],
        "risk_rules": ["confidentiality_period", "governing_law"]
    },
    "soc2_report": {
        "required_fields": [
            "organization_name", "audit_period_start", "audit_period_end",
            "trust_service_criteria", "auditor_name", "opinion_type",
            "exceptions_noted"
        ],
        "risk_rules": ["opinion_type", "exceptions_noted", "audit_period_end"]
    },
    "unknown": {
        "required_fields": [],
        "risk_rules": []
    }
}