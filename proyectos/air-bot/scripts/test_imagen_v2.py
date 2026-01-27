import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')
client = genai.Client(api_key=api_key)

MODEL_NAME = os.getenv('IMAGE_MODEL', 'imagen-4.0-generate-001')

print(f"Testing image generation with NEW SDK: {MODEL_NAME}")

try:
    prompt = "A futuristic city with flying cars, cyberpunk style"
    print(f"Prompt: {prompt}")
    
    response = client.models.generate_images(
        model=MODEL_NAME,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        )
    )
    
    print("Response received!")
    if hasattr(response, 'generated_images'):
        img = response.generated_images[0]
        print(f"Image generated! URI: {img.image.uri[:50]}...")
        # Optional: Save to file to verify
        # with open("test_image.png", "wb") as f:
        #     f.write(img.image.image_bytes)
    else:
        print("Check structure:", dir(response))

except Exception as e:
    print(f"\nError: {e}")
