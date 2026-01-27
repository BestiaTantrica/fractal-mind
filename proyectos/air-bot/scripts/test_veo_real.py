import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')
genai.configure(api_key=api_key)

MODEL_NAME = "models/veo-3.1-generate-preview"

print(f"Testing video generation with: {MODEL_NAME}")

try:
    # prompt = "A cinematic drone shot of a futuristic city at sunset, cyberpunk style, 8k resolution"
    prompt = "Un gato volando con una capa de superheroe"
    
    print(f"Prompt: {prompt}")
    print("Sending request... (this might take a while)")
    
    # NOTE: The exact SDK method for Veo might vary. 
    # Based on search results, it seems likely to be under genai.models or successful via verify.
    # We will try a standard pattern first.
    
    # According to search, we might need to look for specific operations.
    # Let's try to find the model and call generate_content or similar if supported, 
    # but Veo usually returns an Operation object.
    
    # Attempt 1: Direct instantiation if available in newer SDKs, 
    # but since we are not sure of the wrapper, let's look at list_models output from before.
    # It supported 'predictLongRunning'. This usually implies client.predict or model.generate_content (async).
    
    # Let's try the modern client approach if possible, or the reliable one.
    # 'google-generativeai' usually wraps this. 
    
    # IMPORTANT: The public SDK documentation for Veo is sparse. 
    # We will try the generic model access.
    model = genai.GenerativeModel(MODEL_NAME)
    
    # For video, we likely need to pass specific parameters.
    # However, 'generate_content' is typically for text/multimodal text.
    # Videos might need a specific 'generate_videos' or similar if exposed, 
    # OR we pass the prompt to generate_content and expect a URI.
    
    # Let's look at what the user's `check_models.py` said: 
    # Supported Actions: ['predictLongRunning']
    
    # If the action is predictLongRunning, it might not be exposed fluently in GenerativeModel yet.
    # We might need to use the lower level client if GenerativeModel doesn't handle it.
    
    # Let's assert we can just call this for now and see the error or success
    # If this fails, we will fallback to investigating the specific call signature.
    
    # NOTE: As of 0.8.6, video generation might be distinct.
    # Let's try to see if there is a specific helper.
    
    operation = model.generate_content(prompt) 
    # Wait, generate_content might not be the right method for 'predictLongRunning' models.
    
    print("Response received:", operation)
    
except Exception as e:
    print(f"\nError during generation: {e}")
    print("\nAttempting alternative method...")
    # Add alternative method here if known, otherwise we rely on the error to guide us.
