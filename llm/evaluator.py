import re
from llm.gemini import client


def evaluate_response(prompt, response):
    evaluation_prompt = f"""
You are an expert AI evaluator.

Evaluate the following AI response based on the given prompt.

Prompt:
{prompt}

Response:
{response}

Give marks out of 100 using:

- Relevance (30)
- Clarity (20)
- Completeness (25)
- Accuracy (25)

Return ONLY a number.

Example:
92
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0,
        max_tokens=20
    )

    text = completion.choices[0].message.content.strip()

    match = re.search(r"\d+", text)

    if match:
        return int(match.group())

    return 0