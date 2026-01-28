# -*- coding: utf-8 -*-
"""
Script de diagnostico para verificar Plan PRO
"""
import os
import sys
from dotenv import load_dotenv

# Configurar encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

# Usar SDK correcto
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai no instalado")
    sys.exit(1)

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
if not api_key:
    print("ERROR: No se encontro GOOGLE_AI_API_KEY")
    sys.exit(1)

print("="*70)
print("DIAGNOSTICO DEL PLAN PRO - AIR BOT")
print("="*70)
print(f"API Key (ultimos 6): ...{api_key[-6:]}")
print("")

client = genai.Client(api_key=api_key)

# Test Imagen
print("PASO 1: Probando Imagen 4.0...")
print("-"*70)
try:
    prompt = "A professional coffee cup on wooden table, cinematic lighting"
    print(f"Prompt: {prompt}")
    
    response = client.models.generate_images(
        model='imagen-4.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            safety_filter_level="block_only_high",
            person_generation="allow_adult"
        )
    )
    
    if response.generated_images:
        img_bytes = response.generated_images[0].image.image_bytes
        print(f"EXITO! Imagen generada - Tamano: {len(img_bytes)} bytes")
        
        with open('test_imagen_pro.jpg', 'wb') as f:
            f.write(img_bytes)
        print("Guardada como: test_imagen_pro.jpg")
    else:
        print("FALLO: La respuesta no contiene imagenes")
        
except Exception as e:
    error_msg = str(e)
    print(f"ERROR: {error_msg}")
    
    if "billed users" in error_msg or "PERMISSION_DENIED" in error_msg:
        print("")
        print("PROBLEMA: Billing no habilitado o API key incorrecta")
        print("SOLUCION:")
        print("1. Ir a https://console.cloud.google.com/")
        print("2. Seleccionar el proyecto con Plan PRO")
        print("3. Habilitar 'Vertex AI API'")
        print("4. Generar API key DEL PROYECTO CORRECTO")
        print("5. Actualizar .env con la nueva API key")
    
print("")

# Test Video
print("PASO 2: Probando Veo 3.1...")
print("-"*70)
try:
    prompt = "Coffee steam rising from cup, cinematic, 8 seconds"
    print(f"Prompt: {prompt}")
    print("Esperando respuesta (30-60 segundos)...")
    
    response = client.models.generate_videos(
        model='veo-3.1-generate-preview',
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            duration_seconds=8
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
        else:
            print("ADVERTENCIA: Video generado pero sin URI")
    else:
        print("FALLO: No se genero video")
        
except Exception as e:
    error_msg = str(e)
    print(f"ERROR: {error_msg}")
    
    if "billed users" in error_msg or "PERMISSION_DENIED" in error_msg:
        print("")
        print("PROBLEMA: Billing no habilitado para Veo")

print("")
print("="*70)
print("DIAGNOSTICO COMPLETADO")
print("="*70)
