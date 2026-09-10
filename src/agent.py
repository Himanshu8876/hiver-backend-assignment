from gemini_classifier import classify_message
from reply_context import build_reply_context
from reply_generator import generate_reply
from decision import make_decision

def run_agent(customer_message):

    # 1. Classify intent
    intent = classify_message(customer_message)

    # 2. Retrieve historical examples
    context = build_reply_context(
        customer_message,
        top_k=3
    )

    # 3. Best retrieval score
    retrieval_score = 0.0

    if context:
        retrieval_score = context[0]["similarity"]

    # 4. Decide whether to auto-handle or escalate
    decision = make_decision(intent, retrieval_score, customer_message)

    # 5. Generate customer reply
    reply = generate_reply(
        customer_message,
        top_k=3
    )

    return {
        "intent": intent,
        "reply": reply,
        "decision": decision["decision"],
        "reason": decision["reason"],
        "evidence": context
    }