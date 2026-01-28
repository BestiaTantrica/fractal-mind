"""
AIR-Bot - Procesador de IA (Versión Simplificada y Robusta)
Integración con Google Generative AI y Pollinations.
"""

import os
import time
import asyncio
import logging
import requests
import re
import random
from io import BytesIO
from typing import Dict, List, Optional
from PIL import Image

try:
    from google import genai
    from google.genai import types
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

from .utils import detectar_red_social

logger = logging.getLogger(__name__)

class AIProcessor:
    """Procesador simplificado sin dependencias de JSON parsing"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if GOOGLE_AI_AVAILABLE:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
            
        self.text_model = os.getenv('TEXT_MODEL', 'gemini-1.5-flash')
        self.image_model = os.getenv('IMAGE_MODEL', 'imagen-4.0-fast-generate-001')
        logger.info("AIProcessor SIMPLE v5.0 inicializado")

    async def mejorar_prompt(self, texto: str) -> str:
        """
        Traduce y mejora el prompt al inglés técnico.
        Si falla, devuelve el original + directivas de calidad.
        """
        try:
            instruccion = (
                f"Transform this Spanish description into a professional English AI image prompt. "
                f"Add 'perfect anatomy, no extra limbs, highly detailed, 8k, cinematic lighting'. "
                f"Description: {texto}"
            )
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.text_model,
                    contents=instruccion
                )
            )
            resultado = response.text.strip()
            logger.info(f"Prompt mejorado: {resultado[:100]}...")
            return resultado
            
        except Exception as e:
            logger.warning(f"Fallo al mejorar prompt: {e}. Usando original con mejoras básicas.")
            return f"{texto}, perfect anatomy, highly detailed, no extra limbs, 8k quality"

    async def generar_imagen_free(self, prompt: str, red_social: str = "tiktok", seed: Optional[int] = None) -> bytes:
        """
        Genera imagen gratis via Pollinations con reintentos.
        """
        try:
            # Mejora el prompt si es muy corto o español
            if len(prompt) < 20 or not any(x in prompt.lower() for x in ["the", "detailed", "quality"]):
                prompt_final = await self.mejorar_prompt(prompt)
            else:
                prompt_final = prompt
            
            # Dimensiones según red social
            width, height = 1080, 1080
            if red_social in ["tiktok", "instagram", "youtube"]:
                width, height = 1080, 1920
            
            # Semilla aleatoria si no viene especificada
            final_seed = seed if seed is not None else random.randint(1, 999999)
            
            # URL encoding
            prompt_encoded = requests.utils.quote(prompt_final)
            url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={width}&height={height}&seed={final_seed}&nologo=true&model=flux"
            
            logger.info(f"Generando imagen (seed={final_seed}): {prompt_final[:60]}...")
            
            # Reintentos con timeout amplio
            loop = asyncio.get_event_loop()
            for intento in range(2):
                try:
                    response = await loop.run_in_executor(
                        None,
                        lambda: requests.get(url, timeout=45)
                    )
                    
                    if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                        logger.info(f"✅ Imagen generada exitosamente (intento {intento+1})")
                        return response.content
                    
                    logger.warning(f"Intento {intento+1} falló: {response.status_code}")
                except Exception as e:
                    logger.warning(f"Error en intento {intento+1}: {e}")
                
                if intento == 0:
                    await asyncio.sleep(3)  # Esperar antes del reintento
            
            raise Exception("Servidor de imágenes saturado. Intenta de nuevo en unos segundos.")
            
        except Exception as e:
            logger.error(f"Error crítico en generación de imagen: {e}")
            raise

    async def editar_imagen(self, imagen_bytes: bytes, instruccion: str) -> bytes:
        """Edita imagen usando Google Imagen 4.0 (Premium)"""
        try:
            prompt_mejorado = await self.mejorar_prompt(instruccion)
            img = Image.open(BytesIO(imagen_bytes))
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_images(
                    model=self.image_model,
                    prompt=prompt_mejorado,
                    config=types.GenerateImagesConfig(
                        reference_images=[img],
                        number_of_images=1,
                        safety_filter_level="block_low_and_above"
                    )
                )
            )
            
            if response.generated_images:
                return response.generated_images[0].image.image_bytes
            raise Exception("Google no devolvió imagen editada")
            
        except Exception as e:
            logger.error(f"Error editando imagen: {e}")
            raise

    async def generar_video(self, prompt: str, red_social: str = "tiktok") -> Dict:
        """Genera video asíncrono vía Veo 3.1"""
        try:
            prompt_mejorado = await self.mejorar_prompt(prompt)
            
            aspect_ratio = "9:16" if red_social in ["tiktok", "instagram", "youtube"] else "16:9"
            
            loop = asyncio.get_event_loop()
            operation = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_videos(
                    model="veo-3.1-generate-preview",
                    prompt=prompt_mejorado,
                    config=types.GenerateVideosConfig(
                        aspect_ratio=aspect_ratio,
                        duration_seconds=8
                    )
                )
            )
            
            # Polling
            waited = 0
            while not operation.done and waited < 600:
                await asyncio.sleep(20)
                waited += 20
                operation = await loop.run_in_executor(
                    None,
                    lambda: self.client.operations.get(name=operation.name)
                )
            
            metadata = {
                "caption": f"Video: {prompt[:30]}...",
                "hashtags": ["#AI", f"#{red_social}"]
            }
            
            if operation.done and not operation.error:
                result = operation.result
                if result.generated_videos:
                    metadata['video_url'] = result.generated_videos[0].video.uri
            else:
                metadata['error'] = "Timeout o error en generación"
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error en video: {e}")
            raise

    async def generar_guiones(self, tema: str, red_social: str = "tiktok") -> Dict:
        """Genera guiones profesionales"""
        try:
            prompt = f"Genera 3 guiones virales para {red_social} sobre: {tema}. Formato Markdown con estructura clara."
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.text_model,
                    contents=prompt
                )
            )
            
            return {
                "guiones": [{"titulo": "Estrategia AIR", "script": response.text, "duracion_estimada": "15-30s"}],
                "hashtags": ["#Viral", f"#{red_social}"],
                "red_social": red_social,
                "horario_optimo": {"dias_semana": "18:00", "fin_semana": "11:00"}
            }
        except Exception as e:
            logger.error(f"Error generando guiones: {e}")
            raise

def crear_ai_processor(api_key: str) -> AIProcessor:
    return AIProcessor(api_key)
