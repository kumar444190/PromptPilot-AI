import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)

def optimize_prompt(prompt):
    """
    Improve the user's prompt using Groq.
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

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": optimization_prompt
            }
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return completion.choices[0].message.content