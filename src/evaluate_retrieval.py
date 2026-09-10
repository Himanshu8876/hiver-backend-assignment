import pandas as pd

from retriever import HistoricalRetriever


df = pd.read_csv("data/golden_eval.csv")

retriever = HistoricalRetriever()

scores = []

for _, row in df.iterrows():
    results = retriever.search(
        row["text"],
        top_k=3
    )

    if len(results) > 0:
        scores.append(float(results.iloc[0]["similarity"]))
    else:
        scores.append(0.0)

df["retrieval_score"] = scores

df.to_csv(
    "data/golden_with_retrieval.csv",
    index=False
)

print("Retrieval evaluation complete.")
print()
print("Average similarity:", round(df["retrieval_score"].mean(), 4))
print("Minimum similarity:", round(df["retrieval_score"].min(), 4))
print("Maximum similarity:", round(df["retrieval_score"].max(), 4))

print("\nExamples with lowest similarity:")
print(
    df[
        ["text", "true_intent", "retrieval_score"]
    ]
    .sort_values("retrieval_score")
    .head(10)
    .to_string(index=False)
)