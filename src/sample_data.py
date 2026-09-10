import pandas as pd

file_path = "data/amazon_conversations.csv"
output_path = "data/amazon_customer_sample.csv"

df = pd.read_csv(file_path)

sample = df.sample(n=500, random_state=42)

sample.to_csv(output_path, index=False)

print("Total customer messages:", len(df))
print("Sample messages:", len(sample))
print("Saved to:", output_path)