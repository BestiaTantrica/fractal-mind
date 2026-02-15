import os
import sys
import asyncio
from dotenv import load_dotenv
from google.genai import types

# Añadimos la ruta de air-bot al path para importar su core
AIR_BOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../proyectos/air-bot"))
sys.path.append(AIR_BOT_PATH)

# Cargamos el .env de air-bot
load_dotenv(os.path.join(AIR_BOT_PATH, ".env"))

from core.ai_processor import AIProcessor

async def bridge_air_image(prompt, output_path, red_social="tiktok"):
    print(f"AIR Bridge: Solicitando imagen para '{prompt}'")
    
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_AI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: No se encontró GEMINI_API_KEY, GOOGLE_AI_API_KEY o GOOGLE_API_KEY en el .env de air-bot")
        return False
        
    p = AIProcessor(api_key)
    content = None
    
    try:
        # FASE 1: Intento Premium (Google Imagen)
        if p.client and hasattr(p.client.models, 'generate_images'):
            try:
                print("AIR Bridge: Intentando motor Premium (Google Imagen)...")
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: p.client.models.generate_images(
                        model=p.image_model,
                        prompt=prompt,
                        config=types.GenerateImagesConfig(number_of_images=1)
                    )
                )
                if response.generated_images:
                    content = response.generated_images[0].image.image_bytes
                    print("[OK] Imagen generada con motor Premium.")
            except Exception as premium_err:
                print(f"[WARN] Motor Premium no disponible o error: {premium_err}")
                print("[RETRY] Saltando a motor Gratuito (Failsafe)...")
        
        # FASE 2: Intento Gratuito (Pollinations con reintentos agresivos)
        if not content:
            print("AIR Bridge: Usando motor Gratuito (Pollinations)...")
            retries = 3
            for i in range(retries):
                try:
                    content = await p.generar_imagen_free(prompt, red_social=red_social)
                    if content:
                        print(f"[OK] Imagen generada con motor Gratuito (Intento {i+1}).")
                        break
                except Exception as free_err:
                    print(f"[WARN] Intento {i+1} fallido: {free_err}")
                    if i < retries - 1:
                        wait_time = (i + 1) * 5
                        print(f"Esperando {wait_time}s antes de reintentar...")
                        await asyncio.sleep(wait_time)
            
        if not content:
            print("Error: No se pudo obtener contenido de ningún motor.")
            return False
            
        with open(output_path, 'wb') as f:
            f.write(content)
        print(f"Imagen guardada con éxito en {output_path}")
        return True
    except Exception as e:
        print(f"Error crítico en AIR Bridge: {e}")
        return False
    except Exception as e:
        print(f"Error en AIR Bridge execution: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python main.py <prompt> <output_path>")
        sys.exit(1)
        
    prompt_arg = sys.argv[1]
    out_arg = sys.argv[2]
    
    success = asyncio.run(bridge_air_image(prompt_arg, out_arg))
    sys.exit(0) if success else sys.exit(1)
