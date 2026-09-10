import pandas as pd

file_path = r"C:\Users\admin\Desktop\Hiver\archive\twcs\twcs.csv"
output_path = "data/amazon_conversations.csv"

df = pd.read_csv(file_path)

# AmazonHelp replies
amazon = df[df["author_id"] == "AmazonHelp"]

# Get customer tweet IDs
customer_ids = (
    amazon["in_response_to_tweet_id"]
    .dropna()
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
)

# Convert IDs into a consistent format
customer_ids = pd.to_numeric(
    customer_ids,
    errors="coerce"
).dropna().astype("int64")

customer_ids = set(customer_ids)

print("Customer tweet IDs:", len(customer_ids))

# Find customer tweets
customers = df[
    df["tweet_id"].isin(customer_ids)
    & (df["inbound"] == True)
].copy()

print("Customer messages:", len(customers))

customers.to_csv(output_path, index=False)

print("Saved to:", output_path)