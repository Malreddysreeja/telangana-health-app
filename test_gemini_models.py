import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("\n✅ Listing available Gemini models for your API key:\n")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print("➡️", m.name)
