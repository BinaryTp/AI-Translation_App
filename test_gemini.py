from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""
Translate the following text into Hindi.
Return ONLY the translated text.
Do not explain anything.

Text:
Hello, how are you?
"""
)

print(response.text)