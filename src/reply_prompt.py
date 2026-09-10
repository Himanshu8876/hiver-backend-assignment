def build_reply_prompt(customer_message, context):
    examples = []

    for item in context:
        examples.append(
            f"""Customer:
{item['similar_customer_message']}

Historical AmazonHelp reply:
{item['historical_reply']}
"""
        )

    historical_examples = "\n---\n".join(examples)

    prompt = f"""
You are a customer support agent for Amazon.

Write a helpful reply to the customer using the historical AmazonHelp replies below as evidence.

Customer message:
{customer_message}

Historical examples:
{historical_examples}

Rules:
- Use the historical examples to guide the resolution.
- Do not invent policies, refunds, delivery dates, or actions that are not supported by the examples.
- Be concise and professional.
- Do not mention that you used historical examples.
- Return only the customer-facing reply.
"""

    return prompt