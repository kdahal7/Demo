def decide(parsed_query, context_chunks):
    for text in context_chunks:
        if parsed_query['procedure'] in text.lower() and "covered" in text.lower():
            if parsed_query['policy_duration'] >= 3:
                return {
                    "decision": "Approved",
                    "amount": "₹1,00,000",
                    "justification": f"Procedure '{parsed_query['procedure']}' is covered as per clause mentioning waiting period is 3 months."
                }
    return {
        "decision": "Rejected",
        "amount": "₹0",
        "justification": "No clause found indicating coverage for the procedure within 3-month policy."
    }
