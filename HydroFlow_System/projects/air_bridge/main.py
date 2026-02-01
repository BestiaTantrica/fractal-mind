import os
import sys
import asyncio
from dotenv import load_dotenv

# Añadimos la ruta de air-bot al path para importar su core
AIR_BOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../proyectos/air-bot"))
sys.path.append(AIR_BOT_PATH)

# Cargamos el .env de air-bot
load_dotenv(os.path.join(AIR_BOT_PATH, ".env"))

from core.ai_processor import AIProcessor

async def bridge_air_image(prompt, output_path, red_social="tiktok"):
    print(f"AIR Bridge: Solicitando imagen para '{prompt}'")
    
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        print("Error: No se encontró GEMINI_API_KEY en el .env de air-bot")
        return False
        
    p = AIProcessor(api_key)
    
    try:
        content = await p.generar_imagen_free(prompt, red_social=red_social)
        if not content:
            print("Error: El procesador de AIR devolvió contenido vacío.")
            return False
            
        with open(output_path, 'wb') as f:
            f.write(content)
        print(f"Imagen de AIR guardada en {output_path}")
        return True
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
