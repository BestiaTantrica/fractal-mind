# -*- coding: utf-8 -*-
"""
Test VERIFICACION FINAL - Sin person_generation en Veo
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
print("VERIFICACION FINAL - VEO 3.1 (sin person_generation)")
print("="*70)

try:
    prompt = "Cinematic close-up of steaming coffee cup, morning light, 8 seconds"
    print(f"Prompt: {prompt}")
    print("Generando video (30-60 segundos)...")
    
    response = client.models.generate_videos(
        model='veo-3.1-generate-preview',
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            duration_seconds=8
            # SIN person_generation - no soportado
        )
    )
    
    print(f"\nRespuesta tipo: {type(response)}")
    print(f"Atributos: {dir(response)}")
    
    if hasattr(response, 'generated_videos') and response.generated_videos:
        print(f"\nNumero de videos: {len(response.generated_videos)}")
        video = response.generated_videos[0]
        
        print(f"Video tipo: {type(video)}")
        print(f"Video atributos: {dir(video)}")
        
        # Intentar múltiples formas de extraer URI
        video_uri = None
        
        if hasattr(video, 'video'):
            print(f"video.video tipo: {type(video.video)}")
            print(f"video.video atributos: {dir(video.video)}")
            
            if hasattr(video.video, 'uri'):
                video_uri = video.video.uri
        
        if not video_uri and hasattr(video, 'uri'):
            video_uri = video.uri
            
        if video_uri:
            print(f"\nEXITO! Video generado")
            print(f"URI del video: {video_uri}")
            print("\nSTATUS: VEO 3.1 FUNCIONA CORRECTAMENTE")
        else:
            print("\nADVERTENCIA: Video generado pero sin URI accesible")
            print("Revisa los atributos arriba para debugging")
    else:
        print("\nFALLO: Sin videos en respuesta")
        print(f"Respuesta completa: {response}")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
