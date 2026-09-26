import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("✅ Gemini API key loaded successfully!")
    print("Key detected:", api_key[:6] + "******")
else:
    print("❌ Gemini API key was not found.")