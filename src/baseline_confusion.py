import pandas as pd

df = pd.read_csv("data/baseline_results.csv")

wrong = df[df["predicted_intent"] != df["true_intent"]]

print("Total wrong predictions:", len(wrong))
print()

print("Most common wrong predictions:")
print(
    wrong.groupby(["true_intent", "predicted_intent"])
    .size()
    .sort_values(ascending=False)
    .head(10)
)