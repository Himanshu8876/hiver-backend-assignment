import pandas as pd
from intents import INTENTS


df = pd.read_csv("data/golden_eval.csv")

valid_intents = set(INTENTS.keys())

missing_labels = df["true_intent"].isna() | (df["true_intent"].str.strip() == "")
invalid_labels = ~df["true_intent"].isin(valid_intents)

print("Total examples:", len(df))
print("Missing labels:", missing_labels.sum())
print("Invalid labels:", invalid_labels.sum())

if missing_labels.sum() == 0 and invalid_labels.sum() == 0:
    print("Golden evaluation set is valid.")
else:
    print("Please fix the labels.")