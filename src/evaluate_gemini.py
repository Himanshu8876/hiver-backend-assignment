import pandas as pd
from gemini_classifier import classify_messages

df = pd.read_csv("data/golden_eval.csv")

test_df = df.head(5).copy()

messages = test_df["text"].tolist()

predictions = classify_messages(messages)

for i, (_, row) in enumerate(test_df.iterrows()):
    print("Message:", row["text"])
    print("Actual:", row["true_intent"])
    print("Predicted:", predictions[i])
    print()