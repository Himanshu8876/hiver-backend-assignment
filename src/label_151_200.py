import pandas as pd


file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "delivery_not_received",
    "other_non_actionable",
    "refund_or_return",
    "delivery_delay",
    "account_or_security",
    "delivery_attempt_issue",
    "delivery_delay",
    "prime_subscription",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_delay",
    "product_or_digital_issue",
    "other_non_actionable",
    "product_or_digital_issue",
    "delivery_delay",
    "delivery_attempt_issue",
    "other_non_actionable",
    "delivery_delay",
    "product_or_digital_issue",
    "delivery_delay",
    "seller_or_product_complaint",
    "refund_or_return",
    "delivery_not_received",
    "delivery_attempt_issue",
    "delivery_delay",
    "delivery_delay",
    "delivery_attempt_issue",
    "delivery_delay",
    "delivery_not_received",
    "product_or_digital_issue",
    "delivery_delay",
    "product_or_digital_issue",
    "product_or_digital_issue",
    "other_non_actionable",
    "seller_or_product_complaint",
    "delivery_attempt_issue",
    "delivery_attempt_issue",
    "seller_or_product_complaint",
    "delivery_delay",
    "order_issue",
    "delivery_attempt_issue",
    "other_non_actionable",
    "delivery_delay",
    "payment_or_billing",
    "other_non_actionable",
    "prime_subscription",
    "delivery_not_received",
    "delivery_attempt_issue",
    "other_non_actionable",
    "other_non_actionable"
]

df.loc[150:199, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("Messages 151-200 labelled successfully.")