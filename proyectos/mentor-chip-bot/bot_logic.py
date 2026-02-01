import os
import logging
import asyncio
import edge_tts
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, InternalServerError

# --- PROJECT DEPENDENCIES (Conceptual List) ---
# google-genai
# python-dotenv
# requests
# Pillow
# edge-tts
# tenacity
# ---------------------------------------------

logger = logging.getLogger(__name__)

class MentorChipLogic:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.model_id = os.getenv('TEXT_MODEL', 'gemini-1.5-flash')
        
        # Cargar el prompt del sistema basado en la Idea 52
        self.system_instruction = """
Eres el Mentor Chip (C.H.I.P. - Consejero de Hardware e Inversión Práctica).
Especialidad: Diagnóstico de Hardware Móvil y PC, Reparación con Recursos Limitados, y Estrategias de Ahorro para Inversión.

FILOSOFÍA CENTRAL:
"El mejor diagnóstico se hace con la mente y el multímetro más barato. Antes de comprar una herramienta, asegúrate de que el trabajo lo pague."

OBJETIVO PRINCIPAL:
Guiar a un usuario de 15 años (Luca) desde cero hasta realizar su primera reparación rentable, enseñándole a documentar, diagnosticar y ahorrar para herramientas esenciales.

ROL Y ESTILO:
1. Eres paciente, práctico, enfocado en SEGURIDAD y AHORRO.
2. NUNCA recomiendes herramientas costosas al inicio.
3. Siempre acompaña explicaciones con referencias de búsqueda (ej. "Busca en YouTube: Tutorial Multímetro básico").
4. Prioridad: Gasto cero en cursos, inversión solo si el aprendizaje lo justifica.
5. Seguridad y ESD: Cada sesión debe recordar la importancia de la descarga electrostática.
6. Clasifica herramientas: Nivel 0 (Gratis), Nivel 1 (Inversión Inicial), Nivel 2 (Profesional).

ESTILO DE RESPUESTA:
- Empatía con el aprendizaje.
- Pasos numerados si es un proceso técnico.
- Siempre una "Tarea de Ahorro" o "Reto de Diagnóstico" opcional.
"""

    @retry(
        retry=retry_if_exception_type((ResourceExhausted, ServiceUnavailable, InternalServerError)),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    def _call_gemini_api(self, contents):
        """Llamada a la API separada para poder decorarla con reintentos"""
        return self.client.models.generate_content(
            model=self.model_id,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.7,
            )
        )

    async def get_response(self, user_id: str, message: str, history: list = None) -> str:
        try:
            # Convertir historial al formato de Gemini si existe
            contents = []
            if history:
                for msg in history:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(types.Content(parts=[types.Part(text=msg["content"])], role=role))
            
            # Agregar el nuevo mensaje
            contents.append(types.Content(parts=[types.Part(text=message)], role="user"))

            loop = asyncio.get_event_loop()
            
            # Ejecutar la llamada con reintentos dentro del executor
            response = await loop.run_in_executor(
                None,
                lambda: self._call_gemini_api(contents)
            )
            return response.text
        except ResourceExhausted:
            logger.error("Error 429: Cuota excedida incluso tras reintentos.")
            return "🔋 Mi batería cerebral necesita un descanso. (Límite de API alcanzado, probá en un ratito)."
        except Exception as e:
            logger.error(f"Error en MentorChipLogic: {e}")
            return f"Lo siento, tuve un pequeño corto circuito. Revisa mi cableado (error: {str(e)[:50]}...)"

    async def generate_voice(self, text: str, output_path: str):
        """Genera audio a partir de texto usando Edge-TTS (Neuromórfico)"""
        try:
            # Limpiar un poco el texto para el audio (quitar markdown)
            clean_text = text.replace("**", "").replace("#", "").replace("`", "").replace("_", "")
            
            voice = "es-AR-ElenaNeural" # Voz neutra/argentina de calidad
            communicate = edge_tts.Communicate(clean_text, voice)
            await communicate.save(output_path)
            return True
        except Exception as e:
            logger.error(f"Error generando voz: {e}")
            return False
