import os
from dotenv import load_dotenv
from google import genai

from intents import INTENTS
from baseline import classify_message as baseline_classify

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_message(message):
    intent_list = "\n".join(
        f"- {name}: {description}"
        for name, description in INTENTS.items()
    )

    prompt = f"""
You are a customer support intent classifier.

Classify the customer message into exactly ONE of the following intents:

{intent_list}

Customer message:
{message}

Important:
- If the message says the package/order was marked as delivered but the customer did not receive it, classify it as delivery_not_received.
- If the message says the order is late or delayed, classify it as delivery_delay.
- If the customer wants a refund or return, classify it as refund_or_return.
- Choose the closest intent from the list.
- Return ONLY the exact intent name.
- Do not explain your answer.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        predicted_intent = response.text.strip()

        if predicted_intent not in INTENTS:
            return "other_non_actionable"

        return predicted_intent

    except Exception:
        # Fallback to the keyword baseline if Gemini is unavailable
        return baseline_classify(message)

def classify_messages(messages):
    intent_list = "\n".join(
        f"- {name}: {description}"
        for name, description in INTENTS.items()
    )

    customer_messages = "\n".join(
        f"{i + 1}. {message}"
        for i, message in enumerate(messages)
    )

    prompt = f"""
You are a customer support intent classifier.

Classify each customer message into exactly ONE of these intents:

{intent_list}

Customer messages:

{customer_messages}

Return exactly one intent for each message, in the same order.

Format:
1. intent_name
2. intent_name
3. intent_name

Return ONLY the numbered intent names.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        lines = response.text.strip().splitlines()

        predictions = []

        for line in lines:
            if ". " in line:
                prediction = line.split(". ", 1)[1].strip()

                if prediction in INTENTS:
                    predictions.append(prediction)
                else:
                    predictions.append("other_non_actionable")

        return predictions

    except Exception:
    # Fallback to the keyword baseline if Gemini is unavailable
        return [baseline_classify(message) for message in messages]