"""
Script de prueba para verificar generación de imágenes y videos con la API corregida
"""
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
if not api_key:
    print("❌ Error: No se encontró GOOGLE_AI_API_KEY")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# Test 1: Generación de Imagen
print("="*60)
print("TEST 1: GENERACIÓN DE IMAGEN CON IMAGEN 4.0")
print("="*60)

try:
    prompt_imagen = "A professional coffee cup on wooden table, cinematic lighting, 8k, photorealistic"
    print(f"Prompt: {prompt_imagen}")
    
    response = client.models.generate_images(
        model='imagen-4.0-generate-001',
        prompt=prompt_imagen,
        config=types.GenerateImagesConfig(
            number_of_images=1
        )
    )
    
    if response.generated_images:
        img_bytes = response.generated_images[0].image.image_bytes
        print(f"✅ Imagen generada correctamente! Tamaño: {len(img_bytes)} bytes")
        
        # Guardar para verificación
        with open('test_imagen.jpg', 'wb') as f:
            f.write(img_bytes)
        print("📁 Guardada como 'test_imagen.jpg'")
    else:
        print("❌ No se generó ninguna imagen")
        
except Exception as e:
    print(f"❌ Error en generación de imagen: {e}")

# Test 2: Generación de Video
print("\n" + "="*60)
print("TEST 2: GENERACIÓN DE VIDEO CON VEO 3.1")
print("="*60)

try:
    prompt_video = "A steaming cup of coffee on a wooden table, slow motion cinematic"
    print(f"Prompt: {prompt_video}")
    print("⏳ Generando video... (esto puede tomar 30-60 segundos)")
    
    response = client.models.generate_videos(
        model='veo-3.1-generate-preview',
        prompt=prompt_video,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            duration_seconds=8
        )
    )
    
    if hasattr(response, 'generated_videos') and response.generated_videos:
        video = response.generated_videos[0]
        
        # Extraer URI
        video_uri = None
        if hasattr(video.video, 'uri'):
            video_uri = video.video.uri
        elif hasattr(video, 'uri'):
            video_uri = video.uri
            
        if video_uri:
            print(f"✅ Video generado correctamente!")
            print(f"📹 URI del video: {video_uri}")
        else:
            print("❌ No se encontró URI del video")
            print(f"Estructura del objeto: {dir(video)}")
    else:
        print("❌ No se generó ningún video")
        print(f"Respuesta: {response}")
        
except Exception as e:
    print(f"❌ Error en generación de video: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("PRUEBAS COMPLETADAS")
print("="*60)
