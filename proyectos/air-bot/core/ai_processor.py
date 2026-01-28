"""
AIR-Bot - Procesador de IA
Integración con Google Generative AI (SDK v1), Pollinations y Pexels.
"""

import os
import time
import asyncio
import logging
import requests
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

from .utils import detectar_red_social, calcular_horario_optimo

logger = logging.getLogger(__name__)

# CONFIGURACIÓN DE EXPERTOS
PROMPT_SISTEMA_CREATIVO = """
## AGENTE AIR v2.0 | Modelo de Consultoría "Punta de Lanza"
Eres AIR, un socio estratégico enfocado en resultados virales (TikTok, Reels, Shorts).
Directrices: Acción directa, tono profesional inspirado, vocabulario distintivo marketing.
"""

class AIProcessor:
    """Procesador principal de IA con fallback gratuito"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if GOOGLE_AI_AVAILABLE:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
            
        self.text_model_name = os.getenv('TEXT_MODEL', 'gemini-flash-latest')
        self.video_model_name = os.getenv('VIDEO_MODEL', 'veo-3.1-generate-preview')
        self.image_model_name = os.getenv('IMAGE_MODEL', 'imagen-4.0-fast-generate-001')
        
        logger.info(f"AIProcessor inicializado (Texto: {self.text_model_name})")

    def mejorar_prompt_marketing(self, instruccion_basica: str, tipo: str = "imagen") -> str:
        """Mejora prompts usando Gemini"""
        try:
            prompt_mejora = f"{PROMPT_SISTEMA_CREATIVO}\nMejora este prompt para {tipo} en INGLÉS: {instruccion_basica}"
            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt_mejora
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error mejorando prompt: {e}")
            return instruccion_basica

    def generar_imagen_free(self, prompt: str, red_social: str = "tiktok") -> bytes:
        """Genera imagen gratis via Pollinations.ai"""
        try:
            prompt_pro = self.mejorar_prompt_marketing(prompt, "imagen")
            width, height = 1080, 1080
            if red_social in ["tiktok", "instagram", "youtube"]:
                width, height = 1080, 1920
                
            seed = int(time.time())
            # Usamos FLUX en Pollinations para máxima calidad
            url = f"https://image.pollinations.ai/prompt/{prompt_pro}?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
            
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Pollinations error: {response.status_code}")
        except Exception as e:
            logger.error(f"Error en generar_imagen_free: {e}")
            raise e

    async def generar_video(self, prompt_usuario: str, red_social: str = "tiktok") -> Dict:
        """Genera video asíncrono via Veo 3.1"""
        try:
            prompt_pro = self.mejorar_prompt_marketing(prompt_usuario, "video")
            prompt_optimizado = f"{prompt_pro}. Cinematic, high quality, 8k."
            metadata = self._generar_metadata_completo(prompt_pro, red_social)
            
            try:
                aspect_ratio = "9:16" if red_social in ["tiktok", "instagram", "youtube"] else "16:9"
                operation = self.client.models.generate_videos(
                    model=self.video_model_name,
                    prompt=prompt_optimizado,
                    config=types.GenerateVideosConfig(
                        number_of_videos=1,
                        aspect_ratio=aspect_ratio,
                        duration_seconds=8
                    )
                )
                
                max_wait = 600
                poll = 10
                waited = 0
                while not operation.done and waited < max_wait:
                    await asyncio.sleep(poll)
                    waited += poll
                    operation = self.client.operations.get(name=operation.name)
                
                if operation.done and not operation.error:
                    result = operation.result
                    if result.generated_videos:
                        video = result.generated_videos[0]
                        metadata['video_url'] = video.video.uri if hasattr(video.video, 'uri') else video.uri
                else:
                    metadata['error'] = f"Error en video: {operation.error or 'Timeout'}"
            except Exception as e:
                metadata['error'] = f"Excepción Video: {str(e)}"
                
            return metadata
        except Exception as e:
            logger.error(f"Error global video: {e}")
            raise

    def generar_guiones(self, tema: str, red_social: str = "tiktok") -> Dict:
        """Genera guiones profesionales"""
        try:
            prompt = f"{PROMPT_SISTEMA_CREATIVO}\nGenera 3 guiones para {red_social} sobre: {tema}. Formato Markdown."
            response = self.client.models.generate_content(model=self.text_model_name, contents=prompt)
            return {
                "guiones": [{"titulo": "Estrategia AIR", "script": response.text, "duracion_estimada": "15-30s"}],
                "hashtags": ["#Viral", f"#{red_social}"],
                "red_social": red_social,
                "horario_optimo": calculate_horario_optimo(red_social) if 'calculate_horario_optimo' in globals() else {"dias_semana": "18:00", "fin_semana": "11:00"}
            }
        except Exception as e:
            logger.error(f"Error guiones: {e}")
            raise

    def _generar_metadata_completo(self, prompt: str, red_social: str) -> Dict:
        return {
            "caption": f"Video sobre {prompt[:30]}...",
            "descripcion": f"Contenido viral generado para {red_social}.",
            "cta": "¡Síguenos para más!",
            "hashtags": ["#AI", f"#{red_social}"],
            "horario_optimo": {"dias_semana": "19:00", "fin_semana": "12:00"},
            "formato": "9:16" if red_social != "facebook" else "1:1",
            "duracion": 8
        }

def crear_ai_processor(api_key: str) -> AIProcessor:
    return AIProcessor(api_key)
