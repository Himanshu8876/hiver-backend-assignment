import pandas as pd

df = pd.read_csv("data/baseline_results.csv")

examples = df[
    (df["true_intent"] == "seller_or_product_complaint") &
    (df["predicted_intent"] == "other_non_actionable")
]

print("Number of examples:", len(examples))
print()

for i, (_, row) in enumerate(examples.head(5).iterrows(), 1):
    print(f"Example {i}:")
    print("Message:", row["text"])
    print("Actual:", row["true_intent"])
    print("Predicted:", row["predicted_intent"])
    print()