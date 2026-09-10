import pandas as pd


file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "seller_or_product_complaint",
    "other_non_actionable",
    "delivery_delay",
    "delivery_not_received",
    "other_non_actionable",
    "refund_or_return",
    "delivery_not_received",
    "seller_or_product_complaint",
    "account_or_security",
    "delivery_not_received",
    "other_non_actionable",
    "product_or_digital_issue",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_delay",
    "payment_or_billing",
    "delivery_delay",
    "other_non_actionable",
    "account_or_security",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_not_received",
    "delivery_delay",
    "refund_or_return",
    "delivery_delay",
    "other_non_actionable",
    "delivery_delay",
    "order_issue",
    "delivery_delay",
    "other_non_actionable"
]

df.loc[40:69, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("Messages 41-70 labelled successfully.")