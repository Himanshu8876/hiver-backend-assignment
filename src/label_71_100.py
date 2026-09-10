import pandas as pd


file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "delivery_attempt_issue",
    "delivery_delay",
    "seller_or_product_complaint",
    "delivery_delay",
    "delivery_not_received",
    "payment_or_billing",
    "other_non_actionable",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_not_received",
    "seller_or_product_complaint",
    "other_non_actionable",
    "delivery_delay",
    "product_or_digital_issue",
    "payment_or_billing",
    "other_non_actionable",
    "other_non_actionable",
    "product_or_digital_issue",
    "delivery_attempt_issue",
    "other_non_actionable",
    "product_or_digital_issue",
    "delivery_delay",
    "prime_subscription",
    "other_non_actionable",
    "delivery_delay",
    "order_issue",
    "delivery_not_received",
    "other_non_actionable",
    "delivery_delay",
    "other_non_actionable"
]

df.loc[70:99, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("Messages 71-100 labelled successfully.")