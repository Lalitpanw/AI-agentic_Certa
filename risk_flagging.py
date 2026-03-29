from groq import Groq
import json
from datetime import date
from prompts import RISK_ANALYSIS_PROMPT
from schemas import SCHEMAS

client = Groq()

def run_rule_based_flags(extracted_data, doc_type, vendor_registry):
    flags = []
    today = date.today()

    for field in ["expiry_date", "audit_period_end"]:
        val = extracted_data.get(field)
        if val:
            try:
                doc_date = date.fromisoformat(val)
                if doc_date < today:
                    flags.append({
                        "field": field,
                        "issue": "Date has expired (" + val + ")",
                        "severity": "High",
                        "type": "rule",
                        "recommendation": "Request updated document from vendor"
                    })
            except ValueError:
                flags.append({
                    "field": field,
                    "issue": "Date format invalid: " + val,
                    "severity": "Medium",
                    "type": "rule",
                    "recommendation": "Verify date manually"
                })

    required = SCHEMAS.get(doc_type, {}).get("required_fields", [])
    for field in required:
        if extracted_data.get(field) is None:
            flags.append({
                "field": field,
                "issue": "Required field missing",
                "severity": "Medium",
                "type": "rule",
                "recommendation": "Request this information from vendor"
            })

    name_field = (extracted_data.get("insured_name") or
                  extracted_data.get("legal_name") or
                  extracted_data.get("party_b"))
    if name_field and vendor_registry:
        registered_names = [v["legal_name"].lower()
                            for v in vendor_registry.get("vendors", [])]
        if name_field.lower() not in registered_names:
            flags.append({
                "field": "entity_name",
                "issue": "'" + name_field + "' not found in vendor registry",
                "severity": "High",
                "type": "rule",
                "recommendation": "Verify vendor identity before proceeding"
            })

    return flags


def run_llm_flags(extracted_data, doc_type):
    prompt = RISK_ANALYSIS_PROMPT.format(
        doc_type=doc_type,
        extracted_data=json.dumps(extracted_data, indent=2)
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )

    try:
        text = response.choices[0].message.content
        result = json.loads(text)
        for flag in result.get("ai_flags", []):
            flag["type"] = "ai"
        return result.get("ai_flags", [])
    except json.JSONDecodeError:
        return []


def flag_risks(extracted_data, doc_type, vendor_registry):
    rule_flags = run_rule_based_flags(extracted_data, doc_type, vendor_registry)
    ai_flags = run_llm_flags(extracted_data, doc_type)
    return rule_flags + ai_flags
