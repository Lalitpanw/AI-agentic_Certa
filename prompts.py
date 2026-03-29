CLASSIFICATION_PROMPT = """
You are a document classification system for a vendor risk management platform.

Analyze the document below and identify its type.

Choose ONLY from these types:
- certificate_of_insurance
- vendor_contract
- w9_tax_form
- nda
- soc2_report
- unknown

Respond in this exact JSON format:
{{
  "doc_type": "<type>",
  "confidence": "<high|medium|low>",
  "reasoning": "<one sentence>"
}}

Document:
{document_text}
"""

EXTRACTION_PROMPT = """
You are a data extraction system for vendor compliance documents.

Extract the following fields from this {doc_type} document.

Fields to extract: {fields}

Rules:
- If a field is present, extract its exact value
- If a field is missing or unclear, return null
- Dates must be in YYYY-MM-DD format
- Do not infer or guess values

Respond ONLY in valid JSON with field names as keys.

Document:
{document_text}
"""

RISK_ANALYSIS_PROMPT = """
You are a compliance risk analyst reviewing a vendor document.

Document type: {doc_type}
Extracted data: {extracted_data}

Identify any risk signals that require human attention beyond the rule-based flags already caught.
Focus on: unusual clauses, ambiguous terms, missing context, or anything a compliance officer would flag.

Respond in this JSON format:
{{
  "ai_flags": [
    {{
      "field": "<field or area>",
      "issue": "<what the issue is>",
      "severity": "<High|Medium|Low>",
      "recommendation": "<what reviewer should do>"
    }}
  ]
}}

If no additional issues found, return {{"ai_flags": []}}
"""