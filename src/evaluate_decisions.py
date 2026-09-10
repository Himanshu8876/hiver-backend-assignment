import pandas as pd

from decision import make_decision
from baseline import classify_message


df = pd.read_csv("data/golden_with_retrieval.csv")


decisions = []
reasons = []
predicted_intents = []


for _, row in df.iterrows():

    predicted_intent = classify_message(
        row["text"]
    )

    result = make_decision(
    predicted_intent,
    row["retrieval_score"],
    row["text"]
)

    predicted_intents.append(predicted_intent)
    decisions.append(result["decision"])
    reasons.append(result["reason"])


df["predicted_intent"] = predicted_intents
df["decision"] = decisions
df["reason"] = reasons


df.to_csv(
    "data/decision_results.csv",
    index=False
)


print("Decision distribution:")
print(df["decision"].value_counts())


print("\nEscalation rate:")

escalation_rate = (
    df["decision"] == "escalate"
).mean() * 100

print(round(escalation_rate, 2), "%")


print("\nLow-confidence cases:")

print(
    df[
        df["retrieval_score"] < 0.30
    ][
        [
            "text",
            "true_intent",
            "predicted_intent",
            "retrieval_score",
            "decision"
        ]
    ].to_string(index=False)
)