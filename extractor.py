from groq import Groq
import json
from prompts import EXTRACTION_PROMPT
from schemas import SCHEMAS

client = Groq()

def extract_document(doc_text, doc_type):
    schema = SCHEMAS.get(doc_type, SCHEMAS["unknown"])
    fields = schema["required_fields"]

    if not fields:
        return {"error": "Unknown document type — no schema available"}

    prompt = EXTRACTION_PROMPT.format(
        doc_type=doc_type.replace("_", " "),
        fields=", ".join(fields),
        document_text=doc_text
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )

    try:
        text = response.choices[0].message.content
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Extraction failed — malformed response"}
