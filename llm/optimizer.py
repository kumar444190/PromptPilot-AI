import os

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def optimize_prompt(prompt):
    """
    Improve the user's prompt using Gemini.
    """

    optimization_prompt = f"""
You are an expert Prompt Engineer.

Improve the following prompt.

Rules:
- Keep the original meaning.
- Make it clearer.
- Add useful details.
- Make it more specific.
- Return ONLY the improved prompt.

Prompt:
{prompt}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=optimization_prompt
    )

    return response.text