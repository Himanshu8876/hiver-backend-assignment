import time
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

from gemini_classifier import classify_messages

df = pd.read_csv("data/golden_eval.csv")

batch_size = 10
predictions = []

for start in range(0, len(df), batch_size):

    batch = df["text"].iloc[start:start + batch_size].tolist()

    print(
        f"Processing {start + 1}-{min(start + batch_size, len(df))} "
        f"of {len(df)}"
    )

    batch_predictions = classify_messages(batch)

    if len(batch_predictions) != len(batch):
        print("Batch failed. Using baseline fallback.")

        from src.baseline import classify_message

        batch_predictions = [
            classify_message(message)
            for message in batch
        ]

    predictions.extend(batch_predictions)

    time.sleep(2)


df["predicted_intent"] = predictions

df.to_csv(
    "data/gemini_predictions.csv",
    index=False
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

print("\nFinal Gemini results")
print("--------------------")
print("Accuracy:", round(accuracy, 4))
print("Macro F1:", round(macro_f1, 4))