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
    logging.warning("google-genai no está instalado.")

from .utils import detectar_red_social

logger = logging.getLogger(__name__)

# CONFIGURACIÓN DE EXPERTOS
PROMPT_SISTEMA_CREATIVO = """
## AGENTE AIR v2.0
Eres AIR, experto en marketing. 

Instrucciones:
- Si el usuario quiere varias imágenes, usa "tipo": "secuencia" y fija "cantidad".
- Genera prompts en inglés detallados en "prompt_ia".

Responde SIEMPRE en este formato JSON:
{
  "tipo": "chat" | "imagen" | "video" | "secuencia",
  "respuesta": "Texto para el usuario",
  "prompt_ia": "Detailed English prompt for AI",
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
            # Limpiar el mensaje de basura técnica previa
            mensaje_limpio = re.sub(r'✅|❌|📊|🎨|🎬|Prompt:.*|Cuota:.*', '', mensaje_actual).strip()

            shortcut_words = ["imagen", "foto", "crea", "genera", "dibuj", "secuencia"]
            if any(w in mensaje_limpio.lower() for w in shortcut_words):
                # Extraer cantidad si existe
                nums = re.findall(r'\d+', mensaje_limpio)
                cantidad = int(nums[0]) if nums and int(nums[0]) <= 5 else (3 if "secuencia" in mensaje_limpio.lower() else 1)
                return {
                    "tipo": "imagen" if cantidad == 1 else "secuencia",
                    "respuesta": f"¡Entendido! Preparando {'esa secuencia de ' + str(cantidad) + ' imágenes' if cantidad > 1 else 'tu imagen'}. 🚀",
                    "prompt_ia": mensaje_limpio,
                    "cantidad": cantidad
                }

            contents = []
            for h in historial:
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
                        system_instruction=PROMPT_SISTEMA_CREATIVO
                    )
                )
            )
            
            raw_text = response.text.strip()
            clean_text = re.sub(r'```json\s*|\s*```', '', raw_text)
            
            try:
                return json.loads(clean_text)
            except:
                return {"tipo": "chat", "respuesta": raw_text, "prompt_ia": mensaje_limpio, "cantidad": 1}
                
        except Exception as e:
            logger.error(f"Error procesando intención: {e}")
            return {"tipo": "chat", "respuesta": "Sigo aquí, ¿qué quieres hacer?", "prompt_ia": mensaje_actual, "cantidad": 1}

    async def mejorar_prompt_marketing(self, instruccion_basica: str, tipo: str = "imagen") -> str:
        """Mejora prompts usando Gemini (ASÍNCRONO)"""
        try:
            prompt_mejora = f"Transform this into a hyper-realistic, high-impact English prompt for {tipo}: {instruccion_basica}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.models.generate_content(model=self.text_model_name, contents=prompt_mejora)
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error mejorando prompt: {e}")
            return instruccion_basica

    async def generar_imagen_free(self, prompt: str, red_social: str = "tiktok", seed: Optional[int] = None) -> bytes:
        """Genera imagen gratis via Pollinations.ai con Retries y mayor Timeout"""
        try:
            # Limpiar prompt
            prompt_clean = re.sub(r'✅|❌|📊|🎨|🎬', '', prompt).strip()
            
            if len(prompt_clean) < 15:
                prompt_pro = await self.mejorar_prompt_marketing(prompt_clean, "imagen")
            else:
                prompt_pro = prompt_clean
                
            width, height = 1080, 1080
            if red_social in ["tiktok", "instagram", "youtube"]:
                width, height = 1080, 1920
                
            final_seed = seed if seed is not None else random.randint(1, 1000000)
            prompt_encoded = requests.utils.quote(prompt_pro)
            url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={width}&height={height}&seed={final_seed}&nologo=true&model=flux"
            
            loop = asyncio.get_event_loop()
            
            for intento in range(2): # Reintento automático
                try:
                    response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=60)) # Timeout de 60s
                    if response.status_code == 200:
                        return response.content
                    logger.warning(f"Intento {intento+1} fallido ({response.status_code})")
                except Exception as e:
                    logger.warning(f"Intento {intento+1} error: {e}")
                
                if intento == 0: await asyncio.sleepEx(2) # Esperar antes de reintentar
            
            raise Exception("El servidor de imágenes está muy lento ahora. Prueba en un minuto.")
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
                raise Exception("Google no devolvió imagen editada.")
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
                poll = 20
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
                metadata['error'] = f"Excepción: {str(e)}"
                
            return metadata
        except Exception as e:
            logger.error(f"Error video: {e}")
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
