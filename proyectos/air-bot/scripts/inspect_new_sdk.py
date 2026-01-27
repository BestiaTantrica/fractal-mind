from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')
client = genai.Client(api_key=api_key)

print("--- CLIENT MODELS METHODS ---")
for attr in dir(client.models):
    if not attr.startswith("_"):
        print(attr)
