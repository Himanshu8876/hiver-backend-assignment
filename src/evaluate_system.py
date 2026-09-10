import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report

from baseline import classify_message


df = pd.read_csv("data/golden_eval.csv")

df["predicted_intent"] = df["text"].apply(
    classify_message
)

accuracy = accuracy_score(
    df["true_intent"],
    df["predicted_intent"]
)

macro_f1 = f1_score(
    df["true_intent"],
    df["predicted_intent"],
    average="macro"
)

print("Accuracy:", round(accuracy, 4))
print("Macro F1:", round(macro_f1, 4))

print("\nPer-intent results:")
print(
    classification_report(
        df["true_intent"],
        df["predicted_intent"],
        zero_division=0
    )
)