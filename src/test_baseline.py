import pandas as pd
from baseline import classify_message


df = pd.read_csv("data/amazon_customer_sample.csv")

df["predicted_intent"] = df["text"].apply(classify_message)

print(df[["text", "predicted_intent"]].head(20).to_string(index=False))

print("\nTotal messages:", len(df))
print("Predictions completed:", df["predicted_intent"].notna().sum())