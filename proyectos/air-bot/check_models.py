import os
import sys
from dotenv import load_dotenv

# Importar nueva SDK
try:
    from google import genai
except ImportError:
    print("ERROR: google-genai no instalado")
    sys.exit(1)

load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')

if not api_key:
    print("Error: No se encontró GOOGLE_AI_API_KEY en el .env")
else:
    print(f"Usando API Key: ...{api_key[-6:]}")
    client = genai.Client(api_key=api_key)

    print("--- MODELOS DISPONIBLES (Nuevo SDK) ---")
    try:
        # Paginator for list_models
        for m in client.models.list():
            name = m.name # models/name
            # Filtrar solo relevantes
            if any(k in name for k in ['gemini', 'imagen', 'veo']):
                print(f"Model: {name}")
                print(f"  - Display: {m.display_name}")
                # print(f"  - Methods: {m.supported_generation_methods}") 
                print("-" * 30)
                
    except Exception as e:
        print(f"Error al listar modelos: {e}")
