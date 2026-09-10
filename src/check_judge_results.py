import pandas as pd

df = pd.read_csv("data/reply_judge_results.csv")

usable = df[
    ~df["judge_result"].fillna("").str.startswith("Judge unavailable:")
]

failed = df[
    df["judge_result"].fillna("").str.startswith("Judge unavailable:")
]

print("Total replies:", len(df))
print("Usable judge results:", len(usable))
print("Judge failures:", len(failed))