import pandas as pd


df = pd.read_csv("data/amazon_customer_sample.csv")

eval_set = df.sample(n=200, random_state=123)

eval_set = eval_set[["text"]].copy()

eval_set["true_intent"] = ""

eval_set.to_csv("data/golden_eval.csv", index=False)

print("Golden evaluation set created")
print("Number of messages:", len(eval_set))
print("Saved to: data/golden_eval.csv")