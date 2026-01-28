# -*- coding: utf-8 -*-
"""
Test VEO con manejo correcto de la operacion
"""
import os
import sys
import time
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
print("TEST VEO 3.1 - Manejo de Operacion Async")
print("="*70)

try:
    prompt = "Close-up of steaming coffee cup, cinematic morning light"
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
    
    print(f"\nOperacion: {operation.name}")
    print(f"Tipo: {type(operation)}")
    
    # Esperar con polling manual
    print("Esperando (polling cada 5 segundos)...")
    max_wait = 180  # 3 minutos
    waited = 0
    
    while not operation.done and waited < max_wait:
        time.sleep(5)
        waited += 5
        print(f"  ... {waited}s ...")
        
        # Refrescar estado
        try:
            # Intentar obtener estado actualizado
            operation = client.operations.get(name=operation.name)
        except:
            pass
    
    if operation.done:
        print(f"\nOperacion completada en {waited}s")
        
        # Ahora usar .result (atributo, no metodo)
        if operation.result:
            result = operation.result
            
            print(f"Result tipo: {type(result)}")
            print(f"Result atributos: {dir(result)}")
            
            # Buscar videos
            if hasattr(result, 'generated_videos'):
                videos = result.generated_videos
                print(f"\nVideos generados: {len(videos)}")
                
                if videos:
                    video = videos[0]
                    
                    # Extraer URI
                    uri = None
                    if hasattr(video.video, 'uri'):
                        uri = video.video.uri
                    elif hasattr(video, 'uri'):
                        uri = video.uri
                        
                    if uri:
                        print(f"\nEXITO! Video generado")
                        print(f"URI: {uri}")
                        print("\n" + "="*70)
                        print("VEO 3.1 FUNCIONA CORRECTAMENTE")
                        print("="*70)
                    else:
                        print(f"\nERROR: Sin URI en video")
                else:
                    print("\nERROR: Lista de videos vacia")
            else:
                print(f"\nERROR: result no tiene 'generated_videos'")
                print(f"Result: {result}")
        else:
            print("\nERROR: operation.result es None")
            if operation.error:
                print(f"Error de operacion: {operation.error}")
    else:
        print(f"\nTIMEOUT: Operacion no completo en {max_wait}s")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
