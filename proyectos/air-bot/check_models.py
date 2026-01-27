import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')
if not api_key:
    print("Error: No se encontró GOOGLE_AI_API_KEY en el .env")
else:
    genai.configure(api_key=api_key)

    print("--- MODELOS DISPONIBLES (Buscando vision/image/veo) ---")
    found = False
    try:
        for m in genai.list_models():
            if any(term in m.name.lower() for term in ['vision', 'image', 'imagen', 'veo']):
                print(f"Name: {m.name}, Supported Actions: {m.supported_generation_methods}")
                found = True
        
        if not found:
            print("No se encontraron modelos específicos. Listando todos los modelos disponibles:")
            for m in genai.list_models():
                print(f"Name: {m.name}")
    except Exception as e:
        print(f"Error al listar modelos: {e}")
