import pandas as pd
from baseline import classify_message


df = pd.read_csv("data/golden_eval.csv")

df["predicted_intent"] = df["text"].apply(classify_message)

df.to_csv("data/baseline_results.csv", index=False)

print("Baseline results saved.")
print("Accuracy:", round(
    (df["predicted_intent"] == df["true_intent"]).mean() * 100, 2
), "%")