"""
Script CORREGIDO para verificar que el Plan PRO funciona correctamente
Importante: Si falla con "billed users", puede ser:
1. La API key no está asociada al proyecto con billing
2. Hay que habilitar las APIs en Google Cloud Console
"""
import os
import sys
from dotenv import load_dotenv

# Usar SDK correcto
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ Error: google-genai no instalado. Ejecutar: pip install google-genai")
    sys.exit(1)

from PIL import Image
from io import BytesIO

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
if not api_key:
    print("❌ Error: No se encontró GOOGLE_AI_API_KEY")
    sys.exit(1)

print("="*70)
print("🔍 DIAGNÓSTICO DEL PLAN PRO - AIR BOT")
print("="*70)
print(f"API Key (últimos 6): ...{api_key[-6:]}")
print("")

client = genai.Client(api_key=api_key)

# Test 1: Verificar modelos disponibles
print("📋 PASO 1: Verificando modelos disponibles...")
print("-"*70)
try:
    modelos_imagen = []
    modelos_video = []
    
    for m in client.models.list():
        nombre = m.name
        if 'imagen' in nombre.lower():
            modelos_imagen.append(nombre)
        if 'veo' in nombre.lower():
            modelos_video.append(nombre)
    
    print(f"✅ Modelos Imagen encontrados: {len(modelos_imagen)}")
    for m in modelos_imagen[:3]:
        print(f"   - {m}")
    
    print(f"✅ Modelos Veo encontrados: {len(modelos_video)}")
    for m in modelos_video[:3]:
        print(f"   - {m}")
    print("")
except Exception as e:
    print(f"❌ Error listando modelos: {e}")
    print("")

# Test 2: Generación de Imagen con Imagen 4.0
print("📋 PASO 2: Probando Imagen 4.0 (imagen-4.0-generate-001)...")
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
        print(f"✅ ¡IMAGEN GENERADA! Tamaño: {len(img_bytes)} bytes")
        
        with open('test_imagen_pro.jpg', 'wb') as f:
            f.write(img_bytes)
        print("📁 Guardada como: test_imagen_pro.jpg")
    else:
        print("⚠️ La respuesta no contiene imágenes")
        
except Exception as e:
    error_msg = str(e)
    print(f"❌ ERROR: {error_msg}")
    
    if "billed users" in error_msg:
        print("")
        print("🔴 PROBLEMA DETECTADO: Billing no habilitado")
        print("   Posibles causas:")
        print("   1. La API key no está asociada al proyecto con billing")
        print("   2. Imagen API no está habilitada en Google Cloud Console")
        print("   3. El plan PRO no está activo en AI Studio")
        print("")
        print("📌 SOLUCIÓN:")
        print("   1. Ir a https://aistudio.google.com/")
        print("   2. Verificar que el plan PRO esté activo")
        print("   3. Ir a Google Cloud Console del proyecto")
        print("   4. Habilitar 'Vertex AI API' y 'Imagen API'")
        print("   5. Generar una NUEVA API key del proyecto correcto")
    
print("")

# Test 3: Generación de Video con Veo 3.1
print("📋 PASO 3: Probando Veo 3.1 (veo-3.1-generate-preview)...")
print("-"*70)
try:
    prompt = "Coffee steam rising from cup, cinematic"
    print(f"Prompt: {prompt}")
    print("⏳ Esto puede tardar 30-60 segundos...")
    
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
            print(f"✅ ¡VIDEO GENERADO!")
            print(f"📹 URI: {video_uri}")
        else:
            print("⚠️ Video generado pero sin URI")
            print(f"Estructura: {dir(video)}")
    else:
        print("⚠️ No se generó video")
        
except Exception as e:
    error_msg = str(e)
    print(f"❌ ERROR: {error_msg}")
    
    if "billed users" in error_msg:
        print("")
        print("🔴 PROBLEMA: Billing no habilitado para Veo")
        print("   Ver solución en PASO 2")

print("")
print("="*70)
print("🏁 DIAGNÓSTICO COMPLETADO")
print("="*70)
