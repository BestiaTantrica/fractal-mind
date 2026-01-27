"""
AIR-Bot - Procesador de IA
Integración con Google Generative AI (SDK v1) para edición de imágenes,
generación de videos y creación de contenido.
"""

import os
import time
import logging
from io import BytesIO
from typing import Dict, List, Optional, Union

# Importar nueva SDK
try:
    from google import genai
    from google.genai import types
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    logging.warning("google-genai no está instalado. Ejecute: pip install google-genai")

from PIL import Image
from .utils import detectar_red_social, calcular_horario_optimo

logger = logging.getLogger(__name__)


class AIProcessor:
    """Procesador principal de IA usando Google GenAI SDK"""
    
    def __init__(self, api_key: str):
        if not GOOGLE_AI_AVAILABLE:
            raise ImportError("google-genai no está disponible")
        
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        
        # Configurar modelos
        self.text_model_name = os.getenv('TEXT_MODEL', 'gemini-2.0-flash-exp')
        # Veo 3.1
        self.video_model_name = os.getenv('VIDEO_MODEL', 'veo-3.1-generate-preview')
        # Imagen 4.0
        self.image_model_name = os.getenv('IMAGE_MODEL', 'imagen-4.0-generate-001')
        
        logger.info(f"AIProcessor inicializado. Video: {self.video_model_name}")

    def editar_imagen(self, imagen_bytes: bytes, instruccion: str) -> bytes:
        """
        Edita una imagen usando IA (Imagen 3)
        """
        try:
            # 1. MEJORAR PROMPT "PRO"
            instruccion_pro = self.mejorar_prompt_marketing(instruccion, "imagen")
            logger.info(f"Editando imagen con instrucción PRO: {instruccion_pro}")
            
            imagen = Image.open(BytesIO(imagen_bytes))
            
            # Intentar usar edit_image
            try:
                response = self.client.models.edit_image(
                    model=self.image_model_name,
                    prompt=instruccion_pro,
                    image=imagen,
                    config=types.EditImageConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg"
                    )
                )
                if response.generated_images:
                    logger.info("Imagen editada con éxito usando Imagen 4.0")
                    return response.generated_images[0].image.image_bytes
            except Exception as e:
                logger.warning(f"Error en edit_image: {e}. Intentando generación desde cero...")
            
            # Fallback: Generar imagen nueva basada en el prompt mejorado
            # Agregamos keywords por si acaso el prompt mejorado perdió fuerza
            prompt_completo = f"{instruccion_pro}. 8k, photorealistic, cinematic lighting, masterpiece."
            
            response = self.client.models.generate_images(
                model=self.image_model_name,
                prompt=prompt_completo,
                config=types.GenerateImagesConfig(
                    number_of_images=1
                )
            )
            
            if response.generated_images:
                return response.generated_images[0].image.image_bytes
                
            return imagen_bytes # Return original on failure
            
        except Exception as e:
            logger.error(f"Error editando imagen: {e}")
            return imagen_bytes

    def generar_video(self, prompt_usuario: str, red_social: str = "tiktok") -> Dict:
        """
        Genera un video completo con Google Veo 3.1
        """
        try:
            # Detectar red social
            if red_social == "tiktok" and "instagram" in prompt_usuario.lower():
                red_social = detectar_red_social(prompt_usuario)
            
            # 1. MEJORAR PROMPT VIDEO
            prompt_pro = self.mejorar_prompt_marketing(prompt_usuario, "video")
            
            # Prompt optimizado (con estilo técnico)
            prompt_optimizado = self._optimizar_prompt_video(prompt_pro, red_social)
            
            logger.info(f"Generando video ({self.video_model_name}): {prompt_optimizado[:50]}...")
            
            # Generar Metadata
            metadata = self._generar_metadata_completo(prompt_pro, red_social)
            
            # LLAMADA REAL A VEO
            try:
                # Configurar aspecto
                aspect_ratio = "9:16" if red_social in ["tiktok", "instagram", "youtube"] else "16:9"
                if red_social in ["facebook", "whatsapp"]:
                    aspect_ratio = "1:1" # Si soportado, sino default
                
                # Veo 3.1 solo soporta ciertos ratios.
                if aspect_ratio not in ["16:9", "9:16"]:
                    aspect_ratio = "16:9"

                response = self.client.models.generate_videos(
                    model=self.video_model_name,
                    prompt=prompt_optimizado,
                    config=types.GenerateVideosConfig(
                        number_of_videos=1,
                        aspect_ratio=aspect_ratio,
                        duration_seconds=8
                    )
                )
                
                # La respuesta suele contener el video generado o una operación
                # SDK v1 simplifica esto y devuelve el objeto con generated_videos
                
                if hasattr(response, 'generated_videos') and response.generated_videos:
                     video = response.generated_videos[0]
                     # Descargar bytes del URI si es necesario o si ya vienen
                     # NOTA: En la versión actual, video.video.uri es lo que tenemos.
                     # Necesitamos descargar el contenido del URI si no viene en bytes.
                     # Pero a veces video.video.video_bytes existe?
                     # Asumiremos que requests puede bajarlo si es una URL publica,
                     # o usamos client.requests?
                     
                     video_bytes = None
                     if hasattr(video.video, 'video_bytes') and video.video.video_bytes:
                         video_bytes = video.video.video_bytes
                     elif hasattr(video, 'video_bytes') and video.video_bytes:
                         video_bytes = video.video_bytes
                     elif hasattr(video.video, 'uri') and video.video.uri:
                         import requests
                         logger.info(f"Descargando video de URI: {video.video.uri}")
                         try:
                             r = requests.get(video.video.uri, timeout=30)
                             if r.status_code == 200:
                                 video_bytes = r.content
                             else:
                                 logger.error(f"Error descargando video: Status {r.status_code}")
                         except Exception as e:
                             logger.error(f"Excepción descargando video de URI: {e}")
                
                     if video_bytes:
                         metadata['video_bytes'] = video_bytes
                         metadata['video_url'] = video.video.uri if hasattr(video.video, 'uri') else None
                     else:
                        raise Exception("No se obtuvieron los bytes del video generado")
                else:
                    raise Exception("Respuesta de video vacía o estructura desconocida")

            except Exception as e:
                logger.error(f"Error en llamada a Veo: {e}")
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    metadata['error'] = "⚠️ Cuota de Veo excedida. Intenta más tarde."
                else:
                    metadata['error'] = f"⚠️ Error generando video: {str(e)[:100]}"
                
                # Placeholder para no romper flujo
                metadata['video_bytes'] = None 

            return metadata
            
        except Exception as e:
            logger.error(f"Error generando video global: {e}")
            raise

    def generar_guiones(self, tema: str, red_social: str = "tiktok") -> Dict:
        """
        Genera guiones usando generate_content
        """
        try:
            prompt = self._crear_prompt_guiones(tema, red_social)
            
            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt
            )
            
            texto_generado = response.text
            
            guiones = self._parsear_guiones(texto_generado)
            hashtags = self.generar_hashtags(tema, red_social)
            horario = calcular_horario_optimo(red_social)
            
            resultado = {
                "guiones": guiones,
                "hashtags": hashtags,
                "horario_optimo": horario,
                "red_social": red_social,
                "sugerencia_portada": self._generar_sugerencia_portada(tema)
            }
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error generando guiones: {e}")
            raise

    def generar_hashtags(self, tema: str, red_social: str = "tiktok") -> List[str]:
        try:
            prompt = f"Generate 10 hashtags for {red_social} about {tema}. Return only hashtags separated by spaces."
            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt
            )
            texto = response.text
            return [h for h in texto.split() if h.startswith('#')][:10]
        except:
            return ["#Viral", f"#{red_social}"]

    def _optimizar_prompt_video(self, prompt_usuario: str, red_social: str) -> str:
        estilos = {
            "tiktok": "dynamic, energetic, fast-paced, viral style",
            "instagram": "aesthetic, high quality, polished, cinematic",
            "youtube": "informative, clear, professional",
        }
        estilo = estilos.get(red_social, "cinematic, high quality")
        return f"{prompt_usuario}. Style: {estilo}. 8k resolution, highly detailed."

    def _generar_metadata_completo(self, prompt: str, red_social: str) -> Dict:
        # Reutilizar lógica existente o llamara a generate_content
        # Por brevedad, simplificamos:
        try:
            p = f"Generate JSON metadata for a {red_social} video about '{prompt}': caption, description, cta."
            res = self.client.models.generate_content(model=self.text_model_name, contents=p)
            # Parsear JSON idealmente, aqui simulamos:
            return {
                "caption": f"Video sobre {prompt} ✨",
                "descripcion": f"Increíble video generado con IA sobre {prompt}. ¡Mira esto!",
                "cta": "Dale like y comparte ❤️",
                "hashtags": ["#AI", "#Veo", f"#{red_social}"],
                "horario_optimo": calcular_horario_optimo(red_social),
                "formato": "9:16",
                "duracion": 8
            }
        except Exception as e:
            logger.error(f"Error generando metadata: {e}")
            return {
                "caption": f"Video sobre {prompt} ✨",
                "descripcion": f"Video generado con IA sobre {prompt}.",
                "cta": "Dale like ❤️",
                "hashtags": ["#AI", "#Video", f"#{red_social}"],
                "horario_optimo": {"dias_semana": "18:00", "fin_semana": "11:00"},
                "formato": "9:16",
                "duracion": 8
            }

    def _crear_prompt_guiones(self, tema: str, red_social: str) -> str:
        return f"Escribe 3 guiones cortos para {red_social} sobre: {tema}"

    def _parsear_guiones(self, texto: str) -> List[Dict]:
        # Implementación simple
        return [{"titulo": "Guión Generado", "script": texto[:500], "duracion_estimada": "30s"}]

    def _generar_sugerencia_portada(self, tema: str) -> str:
        return f"Imagen colorida sobre {tema}"

def crear_ai_processor(api_key: str) -> AIProcessor:
    return AIProcessor(api_key)
