import re
from llm.gemini import client


def evaluate_response(prompt, response):
    evaluation_prompt = f"""
You are an AI evaluator.

Evaluate the AI response.

Prompt:
{prompt}

Response:
{response}

Score it out of 100 using:

- Relevance (30)
- Clarity (20)
- Completeness (25)
- Accuracy (25)

Return ONLY the score.

Example:
92
"""

    result = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=evaluation_prompt
    )

    text = result.text.strip()

    match = re.search(r"\d+", text)

    if match:
        return int(match.group())

    return 0