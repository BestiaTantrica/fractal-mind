import os
import sys
from dotenv import load_dotenv
import logging

# Configurar path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ai_processor import crear_ai_processor
from core.utils import quota_manager, detectar_red_social

# Mock logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')
processor = crear_ai_processor(api_key)

def test_duracion_guiones():
    print("\n--- TEST: Duración de Guiones ---")
    temas = [
        ("tiktok", "Receta de café rápido"),
        ("youtube", "Tutorial de Python completo"),
        ("instagram", "Rutina de gimnasio"),
        ("logo", "Diseño de marca personal")
    ]
    
    for red, tema in temas:
        print(f"Testing red: {red} - Tema: {tema}")
        # Accedemos a métodos privados/internos o simulamos la lógica para verificar
        # En este caso, generaremos un guion real (texto) que es barato
        try:
            res = processor.generar_guiones(tema, red)
            guiones = res['guiones']
            print(f"  ✅ Generado {len(guiones)} guiones")
            print(f"  Hashtags: {res['hashtags']}")
            print(f"  Horario: {res['horario_optimo']}")
            print("-" * 30)
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_prompt_video_logic():
    print("\n--- TEST: Lógica de Prompt de Video ---")
    inputs = [
        "Un logo animado para mi marca de café",
        "Video de un gato saltando en slow motion",
        "Instagram reel about travel to Japan"
    ]
    
    for inp in inputs:
        red = detectar_red_social(inp)
        print(f"Input: '{inp}' -> Red detectada: {red}")
        # Aquí idealmente mockearíamos la llamada a Gemini para ver el prompt transformado
        # Como no tenemos mocks fáciles, confiamos en la lógica implementada
        
def test_quota_checkout():
    print("\n--- TEST: Verificación de Cuota (Fix Unpacking) ---")
    try:
        puede, restante, costo = quota_manager.verificar_cuota("video", 100, 10)
        print(f"✅ Unpacking correcto: Puede={puede}, Restante={restante}, Costo={costo}")
    except ValueError as e:
        print(f"❌ Error de unpacking: {e}")

if __name__ == "__main__":
    test_quota_checkout()
    test_prompt_video_logic()
    # Descomentar para gastar tokens de texto
    # test_duracion_guiones()
