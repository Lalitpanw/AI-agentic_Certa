import os
import json
from classifier import classify_document
from extractor import extract_document
from risk_flagging import flag_risks
from router import route_document
from report_generator import generate_doc_report, generate_master_summary

DOCS_FOLDER = "./sample_docs"
VENDOR_REGISTRY_PATH = "./vendor_registry.json"
OUTPUT_PATH = "./output_report.json"

def load_vendor_registry():
    with open(VENDOR_REGISTRY_PATH, "r") as f:
        return json.load(f)

def load_documents():
    docs = []
    for filename in sorted(os.listdir(DOCS_FOLDER)):
        if filename.endswith(".txt"):
            with open(os.path.join(DOCS_FOLDER, filename), "r") as f:
                docs.append({"filename": filename, "text": f.read()})
    return docs

def process_document(doc, vendor_registry):
    print(f"\n-> Processing: {doc['filename']}")

    classification = classify_document(doc["text"], doc["filename"])
    print(f"   Classified as: {classification['doc_type']} ({classification['confidence']} confidence)")

    extraction = extract_document(doc["text"], classification["doc_type"])

    flags = flag_risks(extraction, classification["doc_type"], vendor_registry)
    print(f"   Flags: {len(flags)} ({sum(1 for f in flags if f['severity']=='High')} high)")

    routing = route_document(flags)
    print(f"   Decision: {routing['decision']}")

    return generate_doc_report(
        doc["filename"], classification, extraction, flags, routing
    )

def main():
    print("=== Certa Vendor Document Analysis Agent ===\n")

    vendor_registry = load_vendor_registry()
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")

    doc_reports = []
    for doc in documents:
        report = process_document(doc, vendor_registry)
        doc_reports.append(report)

    master = generate_master_summary(doc_reports)

    final_output = {
        "master_summary": master,
        "document_reports": doc_reports
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(final_output, f, indent=2)

    print(f"\n=== Complete ===")
    print(f"Processed:    {master['total_documents']} docs")
    print(f"Auto-approved: {master['auto_approved']}")
    print(f"Human review:  {master['flagged_for_human_review']}")
    print(f"High risk:     {len(master['high_risk_documents'])} docs")
    print(f"\nFull report saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()