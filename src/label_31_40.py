import pandas as pd

file_path = "data/golden_eval.csv"

df = pd.read_csv(file_path)

labels = [
    "payment_or_billing",
    "other_non_actionable",
    "order_issue",
    "payment_or_billing",
    "order_issue",
    "other_non_actionable",
    "refund_or_return",
    "other_non_actionable",
    "account_or_security",
    "delivery_attempt_issue"
]

df.loc[30:39, "true_intent"] = labels

df.to_csv(file_path, index=False)

print("Messages 31-40 labelled successfully.")