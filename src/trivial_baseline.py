import pandas as pd

df = pd.read_csv("data/golden_eval.csv")

most_common_intent = df["true_intent"].value_counts().idxmax()

df["predicted_intent"] = most_common_intent

accuracy = (
    df["predicted_intent"] == df["true_intent"]
).mean()

print("Most common intent:", most_common_intent)
print("Trivial baseline accuracy:", round(accuracy * 100, 2), "%")
