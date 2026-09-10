from intents import INTENTS


test_predictions = [
    "delivery_delay",
    "refund_or_return",
    "payment_or_billing",
    "account_or_security",
    "prime_subscription",
    "wrong_intent"
]


for prediction in test_predictions:
    if prediction in INTENTS:
        print(prediction, "-> valid")
    else:
        print(prediction, "-> invalid")