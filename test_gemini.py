import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API key not found!")
    exit()

# Configure Gemini
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content("Say Hello in one sentence.")

    print("✅ API is working!")
    print("Response:", response.text)

except Exception as e:
    print("❌ Error:")
    print(e)