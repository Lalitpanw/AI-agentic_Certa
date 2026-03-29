from datetime import datetime

def generate_doc_report(filename, classification, extraction, flags, routing) -> dict:
    return {
        "filename": filename,
        "doc_type": classification["doc_type"],
        "classification_confidence": classification["confidence"],
        "extracted_fields": extraction,
        "risk_flags": flags,
        "flag_count": {
            "high": sum(1 for f in flags if f["severity"] == "High"),
            "medium": sum(1 for f in flags if f["severity"] == "Medium"),
            "low": sum(1 for f in flags if f["severity"] == "Low")
        },
        "routing_decision": routing["decision"],
        "routing_queue": routing.get("queue"),
        "routing_reason": routing["reason"]
    }

def generate_master_summary(doc_reports: list) -> dict:
    total = len(doc_reports)
    auto_approved = sum(1 for d in doc_reports
                       if d["routing_decision"] == "AUTO_APPROVE")
    human_review = total - auto_approved

    high_risk_docs = [
        d["filename"] for d in doc_reports
        if d["flag_count"]["high"] > 0
    ]

    return {
        "run_timestamp": datetime.now().isoformat(),
        "total_documents": total,
        "auto_approved": auto_approved,
        "flagged_for_human_review": human_review,
        "high_risk_documents": high_risk_docs,
        "summary_by_doc": [
            {
                "file": d["filename"],
                "type": d["doc_type"],
                "decision": d["routing_decision"],
                "flags": d["flag_count"]
            }
            for d in doc_reports
        ]
    }