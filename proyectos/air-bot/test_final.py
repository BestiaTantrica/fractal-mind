# -*- coding: utf-8 -*-
"""
Test FINAL para verificar que Imagen 4.0 y Veo 3.1 funcionan correctamente
"""
import os
import sys
from dotenv import load_dotenv

# Configurar encoding
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
print("TEST FINAL - IMAGEN 4.0 Y VEO 3.1")
print("="*70)

# Test 1: Imagen con configuracion corregida
print("\n[1/2] Probando IMAGEN 4.0 (con safety_filter correcto)...")
print("-"*70)
try:
    prompt = "A steaming cup of coffee on rustic wooden table, warm morning light"
    
    response = client.models.generate_images(
        model='imagen-4.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            safety_filter_level="block_low_and_above",  # CORREGIDO
            person_generation="allow_adult"
        )
    )
    
    if response.generated_images:
        img_bytes = response.generated_images[0].image.image_bytes
        print(f"EXITO! Imagen generada ({len(img_bytes)} bytes)")
        
        with open('imagen_final.jpg', 'wb') as f:
            f.write(img_bytes)
        print("Guardada: imagen_final.jpg")
        print("STATUS: IMAGEN 4.0 FUNCIONA CORRECTAMENTE")
    else:
        print("FALLO: Sin imagenes en respuesta")
        
except Exception as e:
    print(f"ERROR: {e}")
    print("STATUS: IMAGEN 4.0 NO FUNCIONA")

# Test 2: Video con configuracion corregida
print("\n[2/2] Probando VEO 3.1 (con person_generation)...")
print("-"*70)
try:
    prompt = "Cinematic close-up of coffee cup with rising steam, golden hour lighting, 8 seconds"
    print("Generando video (esto tarda 30-60 segundos)...")
    
    response = client.models.generate_videos(
        model='veo-3.1-generate-preview',
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            duration_seconds=8,
            person_generation="allow_adult"  # AGREGADO
        )
    )
    
    if hasattr(response, 'generated_videos') and response.generated_videos:
        video = response.generated_videos[0]
        
        video_uri = None
        if hasattr(video.video, 'uri'):
            video_uri = video.video.uri
        elif hasattr(video, 'uri'):
            video_uri = video.uri
            
        if video_uri:
            print(f"EXITO! Video generado")
            print(f"URI: {video_uri}")
            print("STATUS: VEO 3.1 FUNCIONA CORRECTAMENTE")
        else:
            print("ADVERTENCIA: Video sin URI")
            print(f"Atributos: {dir(video)}")
    else:
        print("FALLO: Sin videos en respuesta")
        print(f"Respuesta completa: {response}")
        print("STATUS: VEO 3.1 NO FUNCIONA")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("STATUS: VEO 3.1 NO FUNCIONA")

print("\n" + "="*70)
print("TEST COMPLETADO")
print("="*70)
