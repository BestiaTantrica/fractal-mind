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

# CONFIGURACIÓN DE EXPERTOS - MÁS ESTRICTO
PROMPT_SISTEMA_CREATIVO = """
## AGENTE AIR v2.5 | EXPERTO EN MARKETING VIRAL
Tu tarea es traducir y mejorar las ideas del usuario para transformarlas en PROMPTS TÉCNICOS DE IA (en inglés).

REGLAS:
1. Si el usuario pide una imagen o secuencia, extrae el DETALLE visual (colores, acciones, estilo).
2. Genera un prompt en INGLÉS detallado y profesional.
3. NO ignores ningún detalle del usuario (ropa, clima, cantidad de gente).

Responde SIEMPRE en este formato JSON:
{
  "tipo": "chat" | "imagen" | "video" | "secuencia",
  "respuesta": "Texto corto y motivador para el usuario",
  "prompt_ia": "THE DETAILED ENGLISH PROMPT HERE",
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
        
        logger.info(f"AIProcessor v4.5 inicializado")

    async def procesar_intencion(self, historial: List[Dict], mensaje_actual: str) -> Dict:
        """Usa Gemini para entender y TRADUCIR la intención del usuario"""
        try:
            # Limpiar rastro de mensajes anteriores del bot para no confundir a Gemini
            mensaje_limpio = re.sub(r'✅|❌|📊|🎨|🎬|Prompt:.*|Cuota:.*|Imagen \d/\d.*|¿Quieres cambiar algo.*', '', mensaje_actual, flags=re.IGNORECASE | re.DOTALL).strip()

            contents = []
            # Solo pasar los últimos 4 mensajes del historial para no marear a la IA
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
            
            return json.loads(response.text.strip())
                
        except Exception as e:
            logger.error(f"Error procesando intención: {e}")
            # Fallback simple
            tipo = "imagen" if any(x in mensaje_actual.lower() for x in ["imagen", "foto", "hace", "crea"]) else "chat"
            return {"tipo": tipo, "respuesta": "¡Claro! Trabajando en eso.", "prompt_ia": mensaje_actual, "cantidad": 1}

    async def mejorar_prompt_marketing(self, instruccion: str, tipo: str = "imagen") -> str:
        """Asegura que el prompt esté en inglés y sea profesional antes de ir a Pollinations"""
        try:
            prompt_mejora = f"Act as a professional prompt engineer. Convert this description into a high-quality technical prompt in ENGLISH for AI {tipo} generation. Include lighting, composition and textures. Desc: {instruccion}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.models.generate_content(model=self.text_model_name, contents=prompt_mejora)
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error en mejora de prompt: {e}")
            return instruccion

    async def generar_imagen_free(self, prompt: str, red_social: str = "tiktok", seed: Optional[int] = None) -> bytes:
        """Genera imagen gratis via Pollinations.ai (FLUX) con validación de tipo de contenido"""
        try:
            # SIEMPRE mejorar/traducir el prompt si no parece inglés técnico
            if not prompt.lower().startswith(("a portrait", "cinematic", "high quality", "photo of")):
                 prompt_pro = await self.mejorar_prompt_marketing(prompt, "image")
            else:
                 prompt_pro = prompt

            width, height = 1080, 1080
            if red_social in ["tiktok", "instagram", "youtube"]:
                width, height = 1080, 1920
                
            final_seed = seed if seed is not None else random.randint(1, 999999)
            prompt_encoded = requests.utils.quote(prompt_pro)
            url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={width}&height={height}&seed={final_seed}&nologo=true&model=flux"
            
            loop = asyncio.get_event_loop()
            
            for intento in range(2):
                try:
                    response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=45))
                    # Verificar que recibimos una imagen y no un error JSON
                    if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                        return response.content
                    logger.warning(f"Intento {intento+1} fallido: {response.status_code} - {response.headers.get('Content-Type')}")
                except Exception as e:
                    logger.warning(f"Error de red intento {intento+1}: {e}")
                
                await asyncio.sleep(2)
            
            raise Exception("El servidor de imágenes está saturado. Reintenta con un prompt más simple.")
        except Exception as e:
            logger.error(f"Error grave en imagen free: {e}")
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
            
            # (Lógica de video simplificada para estabilidad)
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
            
            # Polling simplificado
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

def crear_ai_processor(api_key: str) -> AIProcessor:
    return AIProcessor(api_key)
