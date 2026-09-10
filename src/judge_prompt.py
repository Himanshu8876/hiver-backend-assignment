def build_judge_prompt(
    customer_message,
    generated_reply,
    historical_examples
):
    examples = []

    for item in historical_examples:
        examples.append(
            f"""Customer:
{item['similar_customer_message']}

Historical reply:
{item['historical_reply']}
"""
        )

    evidence = "\n---\n".join(examples)

    prompt = f"""
You are evaluating a customer support agent's reply.

Customer message:
{customer_message}

Generated reply:
{generated_reply}

Historical examples used as evidence:
{evidence}

Evaluate the generated reply on these criteria:

1. Groundedness:
Does the reply stay consistent with the historical examples and avoid unsupported claims?

2. Helpfulness:
Does the reply provide a useful next step or resolution for the customer's issue?

3. Professionalism:
Is the reply clear, concise, polite, and appropriate for customer support?

Give each criterion a score from 1 to 5.

Return ONLY this format:

Groundedness: <1-5>
Helpfulness: <1-5>
Professionalism: <1-5>
Overall: <1-5>
Reason: <one short sentence>
"""

    return prompt