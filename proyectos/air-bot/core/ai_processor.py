"""
AIR-Bot - Procesador de IA
Integración con Google Generative AI (SDK v1), Pollinations y Pexels.
"""

import os
import time
import asyncio
import logging
import requests
import json
import re
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
    logging.warning("google-genai no está instalado.")

from .utils import detectar_red_social

logger = logging.getLogger(__name__)

# CONFIGURACIÓN DE EXPERTOS
PROMPT_SISTEMA_CREATIVO = """
## AGENTE AIR v2.0 | SOCIO ESTRATÉGICO
Eres AIR, experto en marketing. Tu misión es entender qué necesita el usuario.

Responde SIEMPRE en este formato JSON:
{
  "tipo": "chat" | "imagen" | "video" | "secuencia",
  "respuesta": "Texto para el usuario",
  "prompt_ia": "Prompt descriptivo en inglés",
  "cantidad": 1-5
}
"""

class AIProcessor:
    """Procesador principal de IA con inteligencia de intención"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if GOOGLE_AI_AVAILABLE:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
            
        self.text_model_name = os.getenv('TEXT_MODEL', 'gemini-1.5-flash')
        self.video_model_name = os.getenv('VIDEO_MODEL', 'veo-3.1-generate-preview')
        self.image_model_name = os.getenv('IMAGE_MODEL', 'imagen-4.0-fast-generate-001')
        
        logger.info(f"AIProcessor inicializado (Texto: {self.text_model_name})")

    async def procesar_intencion(self, historial: List[Dict], mensaje_actual: str) -> Dict:
        """Usa Gemini para entender qué quiere hacer el usuario realmente"""
        try:
            contents = []
            for h in historial:
                role = "user" if h['role'] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": h['content']}]})
            
            contents.append({"role": "user", "parts": [{"text": mensaje_actual}]})
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.text_model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=PROMPT_SISTEMA_CREATIVO
                    )
                )
            )
            
            # Limpieza robusta de JSON
            raw_text = response.text.strip()
            # Eliminar bloques de código markdown si existen
            clean_text = re.sub(r'```json\s*|\s*```', '', raw_text)
            
            try:
                data = json.loads(clean_text)
            except:
                # Fallback: Detección manual de tipo
                tipo = "chat"
                if any(x in mensaje_actual.lower() for x in ["imagen", "foto", "secuencia"]):
                    tipo = "imagen"
                data = {"tipo": tipo, "respuesta": raw_text, "prompt_ia": mensaje_actual, "cantidad": 1}
                
            return data
        except Exception as e:
            logger.error(f"Error procesando intención: {e}")
            return {"tipo": "chat", "respuesta": "Sigo aquí, ¿qué quieres hacer?", "prompt_ia": mensaje_actual, "cantidad": 1}

    async def mejorar_prompt_marketing(self, instruccion_basica: str, tipo: str = "imagen") -> str:
        """Mejora prompts usando Gemini (ASÍNCRONO)"""
        try:
            prompt_mejora = f"Transform this into a high-impact English prompt for {tipo}: {instruccion_basica}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.models.generate_content(model=self.text_model_name, contents=prompt_mejora)
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error mejorando prompt: {e}")
            return instruccion_basica

    async def generar_imagen_free(self, prompt: str, red_social: str = "tiktok") -> bytes:
        """Genera imagen gratis via Pollinations.ai"""
        try:
            # Asegurar que el prompt esté en inglés y sea descriptivo
            if len(prompt) < 10 or not any(x in prompt.lower() for x in ["the", "in", "a"]):
                prompt_pro = await self.mejorar_prompt_marketing(prompt, "imagen")
            else:
                prompt_pro = prompt
                
            width, height = 1080, 1080
            if red_social in ["tiktok", "instagram", "youtube"]:
                width, height = 1080, 1920
                
            seed = int(time.time())
            # Encodear caracteres especiales en la URL
            prompt_encoded = requests.utils.quote(prompt_pro)
            url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=30))
            
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Pollinations error: {response.status_code}")
        except Exception as e:
            logger.error(f"Error en generar_imagen_free: {e}")
            raise e

    async def editar_imagen(self, imagen_bytes: bytes, instruccion: str) -> bytes:
        """Edita imagen usando Google Image 4.0 (PREMIUM)"""
        try:
            prompt_pro = await self.mejorar_prompt_marketing(instruccion, "image editing")
            img = Image.open(BytesIO(imagen_bytes))
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_images(
                    model=self.image_model_name,
                    prompt=prompt_pro,
                    config=types.GenerateImagesConfig(
                        reference_images=[img],
                        number_of_images=1,
                        safety_filter_level="block_low_and_above",
                        person_generation="allow_adult"
                    )
                )
            )
            
            if response.generated_images:
                return response.generated_images[0].image.image_bytes
            else:
                raise Exception("Sin respuesta de Google.")
        except Exception as e:
            logger.error(f"Error en editar_imagen: {e}")
            raise e

    async def generar_video(self, prompt_usuario: str, red_social: str = "tiktok") -> Dict:
        """Genera video asíncrono via Veo 3.1"""
        try:
            prompt_pro = await self.mejorar_prompt_marketing(prompt_usuario, "video")
            metadata = self._generar_metadata_completo(prompt_pro, red_social)
            
            try:
                aspect_ratio = "9:16" if red_social in ["tiktok", "instagram", "youtube"] else "16:9"
                loop = asyncio.get_event_loop()
                operation = await loop.run_in_executor(
                    None,
                    lambda: self.client.models.generate_videos(
                        model=self.video_model_name,
                        prompt=prompt_pro,
                        config=types.GenerateVideosConfig(
                            number_of_videos=1,
                            aspect_ratio=aspect_ratio,
                            duration_seconds=8
                        )
                    )
                )
                
                max_wait = 600
                poll = 15
                waited = 0
                while not operation.done and waited < max_wait:
                    await asyncio.sleep(poll)
                    waited += poll
                    operation = await loop.run_in_executor(None, lambda: self.client.operations.get(name=operation.name))
                
                if operation.done and not operation.error:
                    result = operation.result
                    if result.generated_videos:
                        video = result.generated_videos[0]
                        metadata['video_url'] = video.video.uri if hasattr(video.video, 'uri') else video.uri
                else:
                    metadata['error'] = f"Error: {operation.error or 'Timeout'}"
            except Exception as e:
                metadata['error'] = f"Error: {str(e)}"
                
            return metadata
        except Exception as e:
            logger.error(f"Error video: {e}")
            raise

    async def generar_guiones(self, tema: str, red_social: str = "tiktok") -> Dict:
        """Genera guiones profesionales (ASÍNCRONO)"""
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

    def _generar_metadata_completo(self, prompt: str, red_social: str) -> Dict:
        return {
            "caption": f"Video sobre {prompt[:30]}...",
            "descripcion": f"Contenido viral para {red_social}.",
            "cta": "¡Síguenos!",
            "hashtags": ["#AI", f"#{red_social}"],
            "horario_optimo": {"dias_semana": "19:00", "fin_semana": "12:00"},
            "formato": "9:16" if red_social != "facebook" else "1:1",
            "duracion": 8
        }

def crear_ai_processor(api_key: str) -> AIProcessor:
    return AIProcessor(api_key)
