def route_document(flags):
    if not flags:
        return {
            "decision": "AUTO_APPROVE",
            "reason": "No risk flags detected",
            "queue": None
        }

    severities = [f["severity"] for f in flags]

    if "High" in severities:
        return {
            "decision": "HUMAN_REVIEW",
            "reason": str(severities.count("High")) + " high-severity flag(s) require review",
            "queue": "compliance_team"
        }
    elif "Medium" in severities:
        return {
            "decision": "HUMAN_REVIEW",
            "reason": str(severities.count("Medium")) + " medium-severity flag(s) need attention",
            "queue": "vendor_ops_team"
        }
    else:
        return {
            "decision": "AUTO_APPROVE",
            "reason": "Only low-severity flags — logged for audit",
            "queue": None
        }