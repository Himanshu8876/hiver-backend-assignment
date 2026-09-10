import pandas as pd
from baseline import classify_message


df = pd.read_csv("data/golden_eval.csv")

df["predicted_intent"] = df["text"].apply(classify_message)

accuracy = (df["predicted_intent"] == df["true_intent"]).mean()

print("Baseline accuracy:", round(accuracy * 100, 2), "%")