import pandas as pd

df = pd.read_csv("data/golden_eval.csv")

for i, row in df.iloc[150:200].iterrows():
    print(f"\n{i + 1}. {row['text']}")