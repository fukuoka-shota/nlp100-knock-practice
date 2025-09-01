import google.generativeai as genai
import os

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = """
感謝というテーマについて、川柳の案を10個作成してください。
"""

response = model.generate_content(prompt)

print("解答:")
print(response.text)