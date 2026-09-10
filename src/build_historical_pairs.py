import pandas as pd

INPUT_FILE = r"C:\Users\admin\Desktop\Hiver\archive\twcs\twcs.csv"
OUTPUT_FILE = "data/amazon_historical_pairs.csv"

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

# AmazonHelp tweets
amazon_replies = df[
    (df["author_id"] == "AmazonHelp") &
    (df["inbound"] == False)
].copy()

# Customer tweets that mention AmazonHelp
customers = df[
    (df["inbound"] == True) &
    (df["text"].str.contains("@AmazonHelp", case=False, na=False))
].copy()

# Create lookup: AmazonHelp tweet ID -> reply text
reply_lookup = dict(
    zip(
        amazon_replies["tweet_id"].astype(str),
        amazon_replies["text"]
    )
)

pairs = []

for _, row in customers.iterrows():
    response_ids = str(row["response_tweet_id"]).split(",")

    for response_id in response_ids:
        response_id = response_id.strip()

        if response_id in reply_lookup:
            pairs.append({
                "customer_tweet_id": row["tweet_id"],
                "customer_text": row["text"],
                "reply_tweet_id": response_id,
                "amazon_reply": reply_lookup[response_id]
            })

pairs_df = pd.DataFrame(pairs)

pairs_df.to_csv(OUTPUT_FILE, index=False)

print("Historical pairs:", len(pairs_df))
print("Saved to:", OUTPUT_FILE)

print("\nSample:")
print(pairs_df.head(5).to_string(index=False))