import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# If running on Streamlit Cloud, read from Secrets
if not api_key:
    api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)

def generate_response(prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1024
    )

    return completion.choices[0].message.content