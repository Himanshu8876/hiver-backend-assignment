import pandas as pd
from src.reply_generator import generate_reply

df = pd.read_csv("data/reply_eval.csv")

replies = []

for _, row in df.iterrows():
    print("Generating reply...")
    reply = generate_reply(row["text"], top_k=3)
    replies.append(reply)

df["generated_reply"] = replies

df.to_csv("data/reply_eval_results.csv", index=False)

print("\nReply evaluation file created.")
print("Examples:", len(df))

print(
    df[
        [
            "text",
            "true_intent",
            "generated_reply"
        ]
    ].to_string(index=False)
)