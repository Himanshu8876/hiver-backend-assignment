import pandas as pd

df = pd.read_csv("data/golden_eval.csv")

print(df["true_intent"].value_counts())