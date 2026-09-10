import os
from dotenv import load_dotenv
from google import genai

from src.judge_prompt import build_judge_prompt


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def judge_reply(
    customer_message,
    generated_reply,
    historical_examples
):
    prompt = build_judge_prompt(
        customer_message,
        generated_reply,
        historical_examples
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Judge unavailable: {e}"