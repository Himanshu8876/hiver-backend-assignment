def make_decision(intent, retrieval_score, message=""):

    text = message.lower()

    sensitive_terms = [
        "payment",
        "charged",
        "billing",
        "bank",
        "card",
        "cashback",
        "touch id",
        "login",
        "password",
        "account",
        "refund",
        "return"
    ]

    if intent in [
        "payment_or_billing",
        "account_or_security",
        "refund_or_return"
    ]:
        return {
            "decision": "escalate",
            "reason": "This issue may require account-specific or transaction-specific investigation."
        }

    if any(term in text for term in sensitive_terms):
        return {
            "decision": "escalate",
            "reason": "The message contains a sensitive payment, account, or refund signal."
        }

    if retrieval_score < 0.30:
        return {
            "decision": "escalate",
            "reason": "No sufficiently similar historical resolution was found."
        }

    return {
        "decision": "auto_handle",
        "reason": "A sufficiently similar historical resolution was found."
    }