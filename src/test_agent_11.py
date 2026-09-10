import pandas as pd
from agent import run_agent

df = pd.read_csv("data/golden_eval.csv")

# One example from each intent
test_df = (
    df.groupby("true_intent", group_keys=False)
    .head(1)
    .reset_index(drop=True)
)

for _, row in test_df.iterrows():

    print("=" * 80)
    print("Customer:", row["text"])
    print("Expected intent:", row["true_intent"])

    try:
        result = run_agent(row["text"])

        print("Predicted intent:", result["intent"])
        print("Decision:", result["decision"])
        print("Reason:", result["reason"])
        print("Reply:", result["reply"])

        if result["evidence"]:
            print(
                "Top similarity:",
                round(result["evidence"][0]["similarity"], 4)
            )

    except Exception as e:
        print("ERROR:", e)