"""
AIR-Bot - Procesador de IA
Integración con Google Generative AI (SDK v1) y Pollinations.
"""

import os
import time
import asyncio
import logging
import requests
import json
import re
import random
from io import BytesIO
from typing import Dict, List, Optional, Union
from PIL import Image

# Importar nueva SDK
try:
    from google import genai
    from google.genai import types
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

from .utils import detectar_red_social

logger = logging.getLogger(__name__)

# CONFIGURACIÓN DE EXPERTOS
PROMPT_SISTEMA_CREATIVO = """
## AGENTE AIR v2.6 | SOCIO ESTRATÉGICO
Eres AIR, experto en marketing viral. Tu misión es transformar las ideas del usuario en contenido de impacto.

REGLAS CRÍTICAS:
1. Si el usuario pide varias imágenes, una secuencia, o un número específico de fotos, fija "tipo": "secuencia" y "cantidad" al número solicitado (máximo 5).
2. Para imágenes, genera un "prompt_ia" en INGLÉS extremadamente detallado.
3. Incluye siempre directivas de calidad: "perfect anatomy, hyper-realistic, 8k, highly detailed".

Responde SIEMPRE en este formato JSON:
{
  "tipo": "chat" | "imagen" | "video" | "secuencia",
  "respuesta": "Mensaje motivador en español",
  "prompt_ia": "THE DETAILED ENGLISH PROMPT",
  "cantidad": 1-5
}
"""

class AIProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if GOOGLE_AI_AVAILABLE:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
            
        self.text_model_name = os.getenv('TEXT_MODEL', 'gemini-1.5-flash')
        self.image_model_name = os.getenv('IMAGE_MODEL', 'imagen-4.0-fast-generate-001')
        
        logger.info(f"AIProcessor v2.6 inicializado")

    async def procesar_intencion(self, historial: List[Dict], mensaje_actual: str) -> Dict:
        """Usa Gemini para entender la intención con fallback manual para secuencias"""
        try:
            # Limpiar rastro de etiquetas del bot
            mensaje_limpio = re.sub(r'✅|❌|📊|🎨|🎬|Prompt:.*|Cuota:.*|Imagen \d/\d.*|¿Quieres cambiar algo.*', '', mensaje_actual, flags=re.IGNORECASE | re.DOTALL).strip()

            contents = []
            for h in historial[-4:]:
                role = "user" if h['role'] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": h['content']}]})
            
            contents.append({"role": "user", "parts": [{"text": mensaje_limpio}]})
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.text_model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=PROMPT_SISTEMA_CREATIVO,
                        response_mime_type="application/json"
                    )
                )
            )
            
            data = json.loads(response.text.strip())
            
            # REFUERZO MANUAL: Si el usuario dijo "3" o "secuencia" y Gemini devolvió 1, lo corregimos
            low_text = mensaje_limpio.lower()
            if any(x in low_text for x in ["secuencia", " 3 ", " tres ", "varias"]):
                if data.get("cantidad", 1) == 1:
                    data["tipo"] = "secuencia"
                    data["cantidad"] = 3
                    logger.info("Corrigiendo intención: Detectada secuencia manualmente")
            
            return data
                
        except Exception as e:
            logger.error(f"Error procesando intención: {e}")
            return {"tipo": "chat", "respuesta": "Sigo aquí, cuéntame más.", "prompt_ia": mensaje_actual, "cantidad": 1}

    async def mejorar_prompt_marketing(self, instruccion: str, tipo: str = "imagen") -> str:
        """Mejora prompts agregando directivas de anatomía y calidad"""
        try:
            prompt_mejora = f"Act as a pro prompt engineer. Convert this into an English technical prompt for {tipo}. IMPORTANT: Include 'perfect anatomy, high quality, no extra limbs, no deformed hands, cinematic lighting'. Original desc: {instruccion}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.models.generate_content(model=self.text_model_name, contents=prompt_mejora)
            )
            # Asegurar que las palabras clave de calidad estén presentes
            final_prompt = response.text.strip()
            if "anatomy" not in final_prompt.lower():
                final_prompt += ", perfect anatomy, highly detailed, 8k resolution"
            return final_prompt
        except Exception as e:
            logger.error(f"Error en mejora: {e}")
            return f"{instruccion}, perfect anatomy, high quality"

    async def generar_imagen_free(self, prompt: str, red_social: str = "tiktok", seed: Optional[int] = None) -> bytes:
        """Genera imagen gratis con reintentos y validación de calidad"""
        try:
            # Si el prompt no es técnico, mejorarlo
            if len(prompt) < 20 or not any(x in prompt.lower() for x in ["the", "lighting", "detailed"]):
                prompt_pro = await self.mejorar_prompt_marketing(prompt)
            else:
                prompt_pro = prompt

            width, height = 1080, 1080
            if red_social in ["tiktok", "instagram", "youtube"]:
                width, height = 1080, 1920
                
            # Semilla aleatoria para variedad si no viene una fija
            final_seed = seed if seed is not None else random.randint(1, 999999)
            prompt_encoded = requests.utils.quote(prompt_pro)
            url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={width}&height={height}&seed={final_seed}&nologo=true&model=flux"
            
            loop = asyncio.get_event_loop()
            for intento in range(2):
                try:
                    response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=40))
                    if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                        return response.content
                except:
                    continue
                await asyncio.sleep(2)
            
            raise Exception("Servidor de imágenes ocupado. Intenta de nuevo.")
        except Exception as e:
            logger.error(f"Error imagen free: {e}")
            raise e

    async def editar_imagen(self, imagen_bytes: bytes, instruccion: str) -> bytes:
        """Edita imagen usando Google Image 4.0 (PREMIUM)"""
        try:
            prompt_pro = await self.mejorar_prompt_marketing(instruccion, "editing")
            img = Image.open(BytesIO(imagen_bytes))
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_images(
                    model=self.image_model_name,
                    prompt=prompt_pro,
                    config=types.GenerateImagesConfig(reference_images=[img], number_of_images=1)
                )
            )
            
            if response.generated_images:
                return response.generated_images[0].image.image_bytes
            raise Exception("Google no respondió.")
        except Exception as e:
            logger.error(f"Error editar: {e}")
            raise e

    async def generar_video(self, prompt: str, red_social: str = "tiktok") -> Dict:
        """Genera video asíncrono via Veo 3.1"""
        try:
            prompt_pro = await self.mejorar_prompt_marketing(prompt, "video")
            metadata = {"caption": f"Video: {prompt[:30]}...", "hashtags": ["#AI", f"#{red_social}"]}
            
            aspect_ratio = "9:16" if red_social in ["tiktok", "instagram", "youtube"] else "16:9"
            loop = asyncio.get_event_loop()
            operation = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_videos(
                    model="veo-3.1-generate-preview",
                    prompt=prompt_pro,
                    config=types.GenerateVideosConfig(aspect_ratio=aspect_ratio)
                )
            )
            
            waited = 0
            while not operation.done and waited < 300:
                await asyncio.sleep(15)
                waited += 15
                operation = await loop.run_in_executor(None, lambda: self.client.operations.get(name=operation.name))
            
            if operation.done and not operation.error:
                metadata['video_url'] = operation.result.generated_videos[0].video.uri
            else:
                metadata['error'] = "Timeout en video."
            return metadata
        except Exception as e:
            logger.error(f"Error video: {e}")
            raise

    async def generar_guiones(self, tema: str, red_social: str = "tiktok") -> Dict:
        """Genera guiones profesionales"""
        try:
            prompt = f"Genera 3 guiones para {red_social} sobre: {tema}. Formato Markdown."
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(model=self.text_model_name, contents=prompt)
            )
            return {
                "guiones": [{"titulo": "Estrategia AIR", "script": response.text, "duracion_estimada": "15-30s"}],
                "hashtags": ["#Viral", f"#{red_social}"],
                "red_social": red_social,
                "horario_optimo": {"dias_semana": "18:00", "fin_semana": "11:00"}
            }
        except Exception as e:
            logger.error(f"Error guiones: {e}")
            raise

def crear_ai_processor(api_key: str) -> AIProcessor:
    return AIProcessor(api_key)
