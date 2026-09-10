import pandas as pd

from sklearn.metrics import accuracy_score, f1_score

from baseline import classify_message


df = pd.read_csv("data/golden_eval.csv")


# -------------------------
# Keyword baseline
# -------------------------

keyword_predictions = [
    classify_message(text)
    for text in df["text"]
]

keyword_accuracy = accuracy_score(
    df["true_intent"],
    keyword_predictions
)

keyword_f1 = f1_score(
    df["true_intent"],
    keyword_predictions,
    average="macro"
)


# -------------------------
# Trivial baseline
# -------------------------

most_common_intent = df["true_intent"].value_counts().idxmax()

trivial_predictions = [
    most_common_intent
    for _ in range(len(df))
]

trivial_accuracy = accuracy_score(
    df["true_intent"],
    trivial_predictions
)

trivial_f1 = f1_score(
    df["true_intent"],
    trivial_predictions,
    average="macro"
)


# -------------------------
# Results
# -------------------------

print("Evaluation results")
print("------------------")

print(
    f"Keyword baseline accuracy: {keyword_accuracy:.4f}"
)

print(
    f"Keyword baseline macro F1: {keyword_f1:.4f}"
)

print()

print(
    f"Trivial baseline accuracy: {trivial_accuracy:.4f}"
)

print(
    f"Trivial baseline macro F1: {trivial_f1:.4f}"
)