import os
from dotenv import load_dotenv
from google import genai

from intents import INTENTS

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


messages = [
    "My order is delayed",
    "I want a refund for this item",
    "I was charged twice for my order",
    "I cannot login to my account",
    "My Prime membership is not working",
]

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

Return the answer in this format:

1. intent_name
2. intent_name
3. intent_name

Return ONLY the intent names. Do not explain.
"""

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt
)

print(response.text)