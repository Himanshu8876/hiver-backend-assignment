from intents import INTENTS

def classify_message(message):
    text = message.lower()

    if "refund" in text or "return" in text:
        return "refund_or_return"

    if "prime" in text:
        return "prime_subscription"

    if (
    "delivered but" in text
    or "delivered when" in text
    or "marked" in text and "delivered" in text
    or "still no package" in text
    or "no sign of it" in text
    or "never received" in text
    or "didn't receive" in text
    or "didn't get" in text
    or "never got" in text
    or "not there" in text
    or "lost package" in text
    or "lost packages" in text
    or "stole my" in text and "package" in text
    or "stolen" in text and "package" in text
):
        return "delivery_not_received"
    if (
    "where is my package" in text
    or "where is my parcel" in text
    or "still no package" in text
    or "never got my package" in text
    or "never got my order" in text
):
        return "delivery_not_received"

    if "late" in text or "delayed" in text:
        return "delivery_delay"

    if "delivery" in text or "shipping" in text:
        return "delivery_attempt_issue"

    if "payment" in text or "charged" in text or "billing" in text:
        return "payment_or_billing"

    if "login" in text or "password" in text or "account" in text:
        return "account_or_security"

    if "seller" in text:
        return "seller_or_product_complaint"

    if "product" in text or "device" in text:
        return "product_or_digital_issue"

    if "order" in text:
        return "order_issue"

    return "other_non_actionable"


if __name__ == "__main__":
    examples = [
        "My order is delayed",
        "I want a refund",
        "I was charged twice",
        "I cannot login to my account",
        "My Prime subscription has a problem",
    ]

    for message in examples:
        print(message)
        print(" ->", classify_message(message))
        print()