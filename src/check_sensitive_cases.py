import pandas as pd

df = pd.read_csv("data/decision_results.csv")

sensitive = [
    "payment_or_billing",
    "account_or_security",
    "refund_or_return"
]

cases = df[
    df["true_intent"].isin(sensitive)
    & (df["decision"] == "auto_handle")
]

print("Sensitive cases auto-handled:", len(cases))
print()

print(
    cases[
        [
            "text",
            "true_intent",
            "predicted_intent",
            "retrieval_score",
            "decision"
        ]
    ].to_string(index=False)
)