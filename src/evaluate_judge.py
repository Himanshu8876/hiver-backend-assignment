import pandas as pd
from src.judge import judge_reply
from src.reply_context import build_reply_context

df = pd.read_csv("data/reply_eval_results.csv")

results = []

for _, row in df.iterrows():
    print("Judging reply...")

    context = build_reply_context(row["text"], top_k=3)

    score = judge_reply(
        row["text"],
        row["generated_reply"],
        context
    )

    results.append(score)

df["judge_result"] = results

df.to_csv("data/reply_judge_results.csv", index=False)

print("\nJudge evaluation file created.")
print("Examples:", len(df))