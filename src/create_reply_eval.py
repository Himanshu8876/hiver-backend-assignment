import pandas as pd

df = pd.read_csv("data/golden_eval.csv")

sample = df.sample(n=10, random_state=42)

sample.to_csv("data/reply_eval.csv", index=False)

print("Reply evaluation set created.")
print("Examples:", len(sample))
print(sample[["text", "true_intent"]].to_string(index=False))