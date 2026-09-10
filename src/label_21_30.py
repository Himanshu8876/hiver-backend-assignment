import pandas as pd

file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "seller_or_product_complaint",
    "payment_or_billing",
    "other_non_actionable",
    "payment_or_billing",
    "other_non_actionable",
    "payment_or_billing",
    "delivery_not_received",
    "refund_or_return",
    "prime_subscription",
    "other_non_actionable"
]

df.loc[20:29, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("Messages 21-30 labelled successfully.")