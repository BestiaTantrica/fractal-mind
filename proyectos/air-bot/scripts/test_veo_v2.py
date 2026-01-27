import os
import time
from dotenv import load_dotenv

# Try importing the new SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed yet.")
    exit(1)

load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')
if not api_key:
    print("API Key not found")
    exit(1)

client = genai.Client(api_key=api_key)

MODEL_NAME = "veo-3.1-generate-preview"

print(f"Testing video generation with NEW SDK: {MODEL_NAME}")

try:
    prompt = "Un gato volando con una capa de superheroe, estilo cinematico, 8k"
    print(f"Prompt: {prompt}")
    print("Sending request...")
    
    # The new SDK typically uses client.models.generate_videos or something similar.
    # We will try the most standard pattern for video generation.
    
    response = client.models.generate_videos(
        model=MODEL_NAME,
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9", # or 9:16
            duration_seconds=8
        )
    )
    
    print("Response received!")
    print(response)
    
    # Start operation poll if it returns an operation
    # Usually the new SDK handles this, but let's see what we get.
    if hasattr(response, 'generated_videos'):
         video = response.generated_videos[0]
         print(f"Video generated! URI: {video.video.uri}")
    else:
         print("Check response structure:", dir(response))

except Exception as e:
    print(f"\nError: {e}")
