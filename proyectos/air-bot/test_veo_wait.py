# -*- coding: utf-8 -*-
"""
Test definitivo con WAIT para operaciones async de Veo
"""
import os
import sys
from dotenv import load_dotenv

if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
client = genai.Client(api_key=api_key)

print("="*70)
print("TEST VEO 3.1 CON WAIT (operacion asincrona)")
print("="*70)

try:
    prompt = "Cinematic close-up of steaming coffee cup on wooden table, warm morning light"
    print(f"Prompt: {prompt}")
    print("Iniciando generacion...")
    
    operation = client.models.generate_videos(
        model='veo-3.1-generate-preview',
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            duration_seconds=8
        )
    )
    
    print(f"\nOperacion iniciada: {operation.name}")
    print("Esperando a que la operacion termine (30-90 segundos)...")
    
    # ESTO ES LO QUE FALTABA: ESPERAR A QUE TERMINE
    result = operation.result()
    
    print(f"\nOperacion completada!")
    print(f"Resultado tipo: {type(result)}")
    print(f"Resultado atributos: {dir(result)}")
    
    # Ahora SI deberia tener los videos
    if hasattr(result, 'generated_videos') and result.generated_videos:
        print(f"\nNumero de videos: {len(result.generated_videos)}")
        video = result.generated_videos[0]
        
        # Extraer URI
        video_uri = None
        if hasattr(video.video, 'uri'):
            video_uri = video.video.uri
        elif hasattr(video, 'uri'):
            video_uri = video.uri
            
        if video_uri:
            print(f"\nEXITO TOTAL! Video generado correctamente")
            print(f"URI: {video_uri}")
            print("\n" + "="*70)
            print("STATUS: VEO 3.1 FUNCIONA CORRECTAMENTE")
            print("="*70)
        else:
            print("\nERROR: Video sin URI")
            print(f"Video object: {video}")
    else:
        print("\nERROR: Sin videos en resultado")
        print(f"Resultado: {result}")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
