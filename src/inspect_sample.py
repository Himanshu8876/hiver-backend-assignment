import pandas as pd

df = pd.read_csv("data/amazon_customer_sample.csv")

for i, (_, row) in enumerate(df.iloc[130:180].iterrows(), start=131):
    print("=" * 80)
    print(f"Example {i}")
    print(row["text"])