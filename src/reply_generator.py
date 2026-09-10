import os
from dotenv import load_dotenv
from google import genai

from src.reply_context import build_reply_context
from src.reply_prompt import build_reply_prompt

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_reply(customer_message, top_k=3):
    context = build_reply_context(customer_message, top_k)

    prompt = build_reply_prompt(
        customer_message,
        context
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception:
        # Fallback to the most relevant historical reply
        if context:
            return context[0]["historical_reply"]

        return "Please contact Amazon Customer Support for further assistance."