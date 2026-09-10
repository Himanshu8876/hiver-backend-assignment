import pandas as pd


file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "payment_or_billing",
    "delivery_delay",
    "seller_or_product_complaint",
    "seller_or_product_complaint",
    "order_issue",
    "other_non_actionable",
    "product_or_digital_issue",
    "other_non_actionable",
    "delivery_delay",
    "refund_or_return"
]

df.loc[:9, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("First 10 messages labelled successfully.")