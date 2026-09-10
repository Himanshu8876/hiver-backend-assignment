import pandas as pd

df = pd.read_csv("data/golden_eval.csv")

from baseline import classify_message

df["predicted_intent"] = df["text"].apply(classify_message)

failure_pairs = [
    ("product_or_digital_issue", "other_non_actionable"),
    ("delivery_attempt_issue", "other_non_actionable"),
    ("delivery_not_received", "other_non_actionable"),
    ("delivery_delay", "delivery_attempt_issue"),
    ("seller_or_product_complaint", "other_non_actionable"),
]

rows = []

for true_intent, predicted_intent in failure_pairs:
    examples = df[
        (df["true_intent"] == true_intent)
        & (df["predicted_intent"] == predicted_intent)
    ].head(3)

    for _, row in examples.iterrows():
        rows.append({
            "true_intent": true_intent,
            "predicted_intent": predicted_intent,
            "text": row["text"]
        })

result = pd.DataFrame(rows)

result.to_csv("data/top_failure_examples.csv", index=False)

print("Failure examples saved.")
print("Examples:", len(result))