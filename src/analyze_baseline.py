import pandas as pd
from baseline import classify_message


df = pd.read_csv("data/golden_eval.csv")

df["predicted_intent"] = df["text"].apply(classify_message)

wrong = df[df["predicted_intent"] != df["true_intent"]]

print("Total examples:", len(df))
print("Wrong predictions:", len(wrong))
print("\nFirst 20 mistakes:\n")

for i, row in wrong.head(20).iterrows():
    print(f"\nExample {i + 1}")
    print("Message:", row["text"])
    print("Actual:", row["true_intent"])
    print("Predicted:", row["predicted_intent"])