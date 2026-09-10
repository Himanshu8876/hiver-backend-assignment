import pandas as pd


file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "delivery_delay",
    "account_or_security",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_attempt_issue",
    "delivery_not_received",
    "delivery_delay",
    "seller_or_product_complaint",
    "other_non_actionable",
    "seller_or_product_complaint",
    "product_or_digital_issue",
    "delivery_delay",
    "account_or_security",
    "order_issue",
    "other_non_actionable",
    "delivery_delay",
    "other_non_actionable",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_delay",
    "seller_or_product_complaint",
    "product_or_digital_issue",
    "prime_subscription",
    "payment_or_billing",
    "delivery_attempt_issue",
    "seller_or_product_complaint",
    "other_non_actionable",
    "order_issue",
    "delivery_not_received",
    "account_or_security",
    "product_or_digital_issue",
    "delivery_delay",
    "other_non_actionable",
    "delivery_not_received",
    "prime_subscription",
    "seller_or_product_complaint",
    "prime_subscription",
    "seller_or_product_complaint",
    "seller_or_product_complaint",
    "product_or_digital_issue",
    "delivery_not_received",
    "delivery_attempt_issue",
    "seller_or_product_complaint",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_attempt_issue",
    "product_or_digital_issue",
    "prime_subscription",
    "delivery_delay",
    "delivery_delay"
]

df.loc[100:149, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("Messages 101-150 labelled successfully.")