import pandas as pd


file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "seller_or_product_complaint",
    "other_non_actionable",
    "other_non_actionable",
    "delivery_not_received",
    "other_non_actionable",
    "prime_subscription",
    "product_or_digital_issue",
    "order_issue",
    "other_non_actionable",
    "delivery_attempt_issue"
]

df.loc[10:19, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("Messages 11-20 labelled successfully.")