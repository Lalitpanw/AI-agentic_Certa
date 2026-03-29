from groq import Groq
import json
from prompts import CLASSIFICATION_PROMPT

client = Groq()

def classify_document(doc_text, filename):
    prompt = CLASSIFICATION_PROMPT.format(document_text=doc_text)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    try:
        text = response.choices[0].message.content
        result = json.loads(text)
        result["filename"] = filename
        return result
    except json.JSONDecodeError:
        return {
            "filename": filename,
            "doc_type": "unknown",
            "confidence": "low",
            "reasoning": "Classification failed"
        }
