# -*- coding: utf-8 -*-
"""
Script de diagnostico para verificar Plan PRO y Configuración
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

# ----------------------------------------------------------------------
# PASO 1: IMAGEN
# ----------------------------------------------------------------------
print("PASO 1: Probando Imagen (Modelo del .env)...")
print("-"*70)
try:
    prompt = "A professional coffee cup on wooden table, cinematic lighting"
    model_env = os.getenv('IMAGE_MODEL', 'imagen-3.0-generate-001')
    print(f"Modelo: {model_env}")
    
    response = client.models.generate_images(
        model=model_env,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            safety_filter_level="block_low_and_above",
            person_generation="allow_adult"
        )
    )
    
    if response.generated_images:
        img_bytes = response.generated_images[0].image.image_bytes
        print(f"EXITO! Imagen generada - Tamano: {len(img_bytes)} bytes")
        with open('test_imagen_pro.jpg', 'wb') as f:
            f.write(img_bytes)
    else:
        print("FALLO: La respuesta no contiene imagenes")
        
except Exception as e:
    error_msg = str(e)
    if "billed users" in error_msg:
        print(f"PROBLEMA: El modelo requerie Billing.")
    elif "PERMISSION_DENIED" in error_msg:
         print("PROBLEMA: API Key rechazada.")
    else:
        print(f"ERROR: {error_msg}")
print("")

# ----------------------------------------------------------------------
# PASO 2: VIDEO
# ----------------------------------------------------------------------
print("PASO 2: Probando Veo (Modelo del .env)...")
print("-"*70)
try:
    prompt = "Coffee steam rising from cup, cinematic, 8 seconds"
    video_model = os.getenv('VIDEO_MODEL', 'veo-3.1-generate-preview')
    print(f"Modelo: {video_model}")
    print("Esperando respuesta (puede tardar)...")
    
    operation = client.models.generate_videos(
        model=video_model,
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            duration_seconds=8
        )
    )
    
    if hasattr(operation, 'error') and operation.error:
         print(f"ERROR VEO: {operation.error}")
    else:
         print("Operacion iniciada (OK / Polling required).")

except Exception as e:
    error_msg = str(e)
    if "RESOURCE_EXHAUSTED" in error_msg:
         print("PROBLEMA: Cuota de Video excedida (Vuelve a intentar más tarde).")
    elif "billed users" in error_msg:
         print("PROBLEMA: Video requiere Billing.")
    else:
         print(f"ERROR: {error_msg}")
print("")

# ----------------------------------------------------------------------
# PASO 3: TEXTO
# ----------------------------------------------------------------------
print("PASO 3: Probando Texto (Guiones)...")
print("-"*70)
try:
    text_model = os.getenv('TEXT_MODEL', 'gemini-2.0-flash')
    print(f"Modelo: {text_model}")
    response = client.models.generate_content(
        model=text_model,
        contents="Hola, response 'OK SYSTEM ACTIVE'."
    )
    print(f"RESPUESTA: {response.text.strip()}")
    print("EXITO! Texto funciona GRATIS.")
except Exception as e:
    print(f"ERROR TEXTO: {e}")
    
print("")
print("="*70)
print("DIAGNOSTICO COMPLETADO")
print("="*70)
