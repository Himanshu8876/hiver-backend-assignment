import pandas as pd
from sklearn.metrics import accuracy_score, f1_score


df = pd.read_csv("data/golden_eval.csv")

most_common_intent = df["true_intent"].value_counts().idxmax()

predictions = [most_common_intent] * len(df)

accuracy = accuracy_score(
    df["true_intent"],
    predictions
)

macro_f1 = f1_score(
    df["true_intent"],
    predictions,
    average="macro"
)

print("Most common intent:", most_common_intent)
print("Accuracy:", round(accuracy, 4))
print("Macro F1:", round(macro_f1, 4))