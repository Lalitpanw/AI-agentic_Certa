# AI-Agentic Vendor Document Analysis Agent

An AI agent that autonomously processes vendor compliance documents, 
extracts structured data, flags risks, and routes documents for human review.

Built as a take-home case study for Certa — a third-party risk management platform.

## What It Does

Takes raw vendor documents as input and makes autonomous decisions at every stage:

1. **Classifies** document type (COI, Contract, W9, NDA, SOC2)
2. **Selects schema** based on doc type — different fields for different documents
3. **Extracts** structured data using LLM
4. **Flags risks** using hybrid approach: rule engine + LLM judgment
5. **Routes** documents: auto-approve (low risk) vs human review queue

## Sample Output
```json
{
  "master_summary": {
    "total_documents": 7,
    "auto_approved": 0,
    "flagged_for_human_review": 7,
    "high_risk_documents": [
      "doc2_coi_expired.txt",
      "doc4_w9_name_mismatch.txt"
    ]
  }
}
```

## Document Types Supported

| Type | Key Fields Extracted | Risk Rules |
|---|---|---|
| Certificate of Insurance | Insurer, coverage, expiry | Expired dates, coverage gaps |
| Vendor Contract | Parties, liability cap, terms | Missing clauses, unsigned |
| W-9 Tax Form | Legal name, TIN, entity type | Name mismatch vs registry |
| NDA | Parties, scope, governing law | Missing fields |
| SOC 2 Report | Audit period, opinion, exceptions | Qualified opinion, expired audit |

## Architecture
```
Raw Document
     ↓
Stage 1: Classification (LLM)
     ↓
Stage 2: Schema Selection (rule-based)
     ↓
Stage 3: Field Extraction (LLM)
     ↓
Stage 4: Risk Flagging (Rules + LLM hybrid)
     ↓
Stage 5: Routing Decision (rule-based)
     ↓
Structured JSON Output
```

## Tech Stack

- Python 3.14
- Groq API (llama-3.3-70b-versatile)
- Zero external dependencies beyond `groq`

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install groq
set GROQ_API_KEY=your-key-here
python main.py
```

## Key Design Decisions

**Why chained prompts over one big prompt:**
Each stage is independently testable and debuggable. 
Classification, extraction, and risk judgment are three 
different cognitive tasks — collapsing them causes hallucination 
and makes failures hard to diagnose.

**Why hybrid risk flagging:**
Deterministic rules handle clear cases (expired dates, missing fields).
LLM handles judgment calls (unusual clauses, ambiguous terms).
This is how you build something trustworthy in a compliance context.

**Known limitation:**
Current version has high false-positive rate on medium-severity flags.
Next iteration would add confidence thresholds and feedback loop 
from human reviewers to tune flagging precision.