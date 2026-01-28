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

# CONFIGURACIÓN DE EXPERTOS (SocialBoost Premium)
PROMPT_SISTEMA_CREATIVO = """
## AGENTE AIR v2.0 | Modelo de Consultoría "Punta de Lanza" (Core Prompt)

Este es el prompt maestro que define la arquitectura mental de AIR.

### I. Perfil de Alto Rendimiento

**Nombre del Modelo:** AIR (Authentic, Intelligent, Radiant)
**Rol:** **Director Ejecutivo de Marca Personal y Arquitecto de Contenido Viral.** (Focus: Alto Retorno, Inspiración Táctica y Conversión Sutil).
**Tono de Mando:** Profesional, pero cálido e inspirador. Utiliza tecnicismos de marketing (e.g., AVD, Hook rate, UGC) salpicados de entusiasmo. Siempre asume una posición de guía, no de mero ejecutor.
**Vocabulario Distintivo:** Usa términos como: "Potencial magnético", "ADN del viral", "Afinar la puntería", "Activación estratégica", y "Visión de 360°".

### II. La Identidad Central
Eres AIR, un socio estratégico enfocado en resultados. Tu misión es transformar ideas en contenido de alto rendimiento para TikTok, Reels y Shorts.

#### TUS DIRECTRICES:
1. **Acción Directa:** No pierdas tiempo en explicaciones largas a menos que el usuario lo pida.
2. **Foco en el Activo:** La prioridad es el video/imagen y su metadata (caption, hashtags).
3. **Tono:** Profesional, directo y enérgico.

#### FASE II: ARQUITECTURA STRATEGIC (Planning)
**Objetivo:** Desarrollar la estructura detallada del contenido elegido.
1.  **El Diseño del Gancho (The Hook):** Proporciona 2 opciones de gancho, ambas con una duración máxima de 3 segundos, que desafíen la 'zona de confort' del algoritmo.
2.  **Estructura Prolija:** Presenta el **CUERPO** (el valor) y el **CTA** (Call to Action) en formato de viñetas claras.
3.  **Refinamiento de Producción:** Sugiere al menos una mejora de producción (visual, sonora o de edición). (Ej: "Para maximizar el AVD, sugiero un corte cada 0.8 segundos en la primera parte, con un incremento de volumen en el Hook.").

#### FASE III: MASTERIZACIÓN (Generación)
**Objetivo:** Entregar el activo final (guion, texto, etc.) listo para su publicación, manteni
endo el tono AIR.
1.  El resultado debe ser un texto finalizado que encapsule toda la estrategia definida.
2.  Añade una **Nota Estratégica Final** indicando por qué esa pieza funcionará (Ej: "Esta estructura aprovecha el sesgo de prueba social, lo que disparará el 'Share Rate'.").

### IV. Reglas de Oro y Pivotes (Anti-Mediocridad)

*   **Prohibido lo Genérico:** No uses frases motivacionales vacías o clichés de autoayuda ("Lucha por tus sueños", "El éxito está cerca"). Sustitúyelos por táctica y estrategia.
*   **Foco en la Retención:** Cada elemento propuesto (Hook, Cuerpo, CTA) debe justificar su existencia basándose en retener al usuario.
*   **Gestión de la Debilidad:** Si la idea inicial del usuario es estratégicamente inviable o mediocre, **debes tomar el control amablemente**.
    *   *Pivote de Control:* "Permíteme afinar el enfoque. Dada tu meta de [Menciona su meta], sugiero que pivotemos a [Nueva Estrategia]. Esto garantiza la conversión que buscamos."
"""


class AIProcessor:
    """Procesador principal de IA usando Google GenAI SDK"""
    
    def __init__(self, api_key: str):
        if not GOOGLE_AI_AVAILABLE:
            raise ImportError("google-genai no está disponible")
        
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        
        # Configurar modelos
        # NUNCA degradar a modelos gratuitos según protocolo /air -> ACTUALIZACIÓN: CAMBIO A PLAN GRATUITO
        self.text_model_name = os.getenv('TEXT_MODEL', 'gemini-1.5-flash')
        
        # Modelos Multimedia (Solo se activan bajo confirmación de usuario)
        self.video_model_name = os.getenv('VIDEO_MODEL', 'veo-3.1-generate-preview')
        self.image_model_name = os.getenv('IMAGE_MODEL', 'imagen-4.0-generate-001')
        
        logger.info(f"AIProcessor inicializado en MODO AHORRO/GRATUITO (Texto: {self.text_model_name})")

    def obtener_cliente(self):
        return self.client

    def mejorar_prompt_marketing(self, instruccion_basica: str, tipo: str = "imagen") -> str:
        """
        Transforma una instrucción simple en una descripción técnica de alta calidad
        """
        try:
            # Detectar si es logo
            es_logo = "logo" in instruccion_basica.lower()
            
            prompt_mejora = f"""
            {PROMPT_SISTEMA_CREATIVO}
            Transforma esta instrucción básica para un modelo de {tipo} en una descripción técnica detallada (PROMPT).
            
            ENTRADA: "{instruccion_basica}"
            
            REGLAS CRÍTICAS:
            1. FIDELIDAD: No inventes elementos que no están en la entrada. Si es "taza de café", es solo eso.
            2. ESTILO: 
               - Si es VIDEO: Cinematic, 8k, highly detailed, slow motion if appropriate.
               - Si es LOGO: Vector style, minimal, clean lines, professional branding, white background default.
               - Si es FOTO: Editorial, photorealistic, cinematic lighting.
            3. IDIOMA: Respondo SOLO con el prompt en INGLÉS.
            """
            
            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt_mejora
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error mejorando prompt: {e}")
            return instruccion_basica # Fallback

    def editar_imagen(self, imagen_bytes: bytes, instruccion: str) -> bytes:
        """
        Edita una imagen usando IA (Imagen 4.0)
        """
        try:
            # 1. MEJORAR PROMPT "PRO"
            instruccion_pro = self.mejorar_prompt_marketing(instruccion, "imagen")
            logger.info(f"Editando imagen con instrucción PRO: {instruccion_pro}")
            
            imagen = Image.open(BytesIO(imagen_bytes))
            
            # Intentar usar edit_image con configuración correcta
            try:
                response = self.client.models.edit_image(
                    model=self.image_model_name,
                    prompt=instruccion_pro,
                    image=imagen,
                    config=types.EditImageConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        safety_filter_level="block_low_and_above",
                        person_generation="allow_adult"
                    )
                )
                if response.generated_images:
                    logger.info("Imagen editada con éxito usando Imagen 4.0")
                    return response.generated_images[0].image.image_bytes
            except Exception as e:
                logger.warning(f"Error en edit_image: {e}. Intentando generación desde cero...")
            
            # Fallback: Generar imagen nueva con configuración correcta
            prompt_completo = f"{instruccion_pro}. 8k, photorealistic, cinematic lighting, masterpiece."
            
            response = self.client.models.generate_images(
                model=self.image_model_name,
                prompt=prompt_completo,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    safety_filter_level="block_low_and_above",
                    person_generation="allow_adult"
                )
            )
            
            if response.generated_images:
                return response.generated_images[0].image.image_bytes
                

            
            # Si llegamos aquí, fallaron ambos métodos
            raise Exception("No se pudo editar ni generar una nueva versión de la imagen.")
            
        except Exception as e:
            logger.error(f"Error editando imagen: {e}")
            raise e

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

                operation = self.client.models.generate_videos(
                    model=self.video_model_name,
                    prompt=prompt_optimizado,
                    config=types.GenerateVideosConfig(
                        number_of_videos=1,
                        aspect_ratio=aspect_ratio,
                        duration_seconds=8
                    )
                )
                
                # Veo 3.1 devuelve una OPERACIÓN ASÍNCRONA, no el video directamente
                logger.info(f"Operación de video iniciada: {operation.name}")
                logger.info("Esperando a que Veo complete la generación (puede tardar 3-5 minutos)...")
                
                # Polling con timeout de 10 minutos (600s)
                max_wait_seconds = 600
                poll_interval = 10
                waited = 0
                
                while not operation.done and waited < max_wait_seconds:
                    time.sleep(poll_interval)
                    waited += poll_interval
                    logger.info(f"Esperando video... {waited}s/{max_wait_seconds}s")
                    
                    # Intentar refrescar estado
                    try:
                        operation = self.client.operations.get(name=operation.name)
                    except Exception as e:
                        logger.warning(f"Error al refrescar operación: {e}")
                        pass # Continue polling even if refresh fails temporarily
                
                if not operation.done:
                    logger.warning(f"Timeout esperando video después de {max_wait_seconds}s")
                    metadata['error'] = f"⏱️ Video en progreso (tarda 3-5 min). Operación: {operation.name}"
                    return metadata
                
                # Operación completada
                if operation.error:
                    logger.error(f"Error en operación de Veo: {operation.error}")
                    raise Exception(f"Error de Veo: {operation.error}")
                
                # Obtener resultado
                result = operation.result
                if not result or not hasattr(result, 'generated_videos'):
                    logger.error(f"Resultado inesperado: {result}")
                    raise Exception("Veo no devolvió videos en el resultado")
                
                if result.generated_videos:
                    video = result.generated_videos[0]
                    
                    # Extraer URI
                    video_uri = None
                    if hasattr(video.video, 'uri'):
                        video_uri = video.video.uri
                    elif hasattr(video, 'uri'):
                        video_uri = video.uri
                        
                    logger.info(f"Video generado exitosamente. URI: {video_uri}")

                    if video_uri:
                        metadata['video_url'] = video_uri
                    else:
                        logger.error(f"No se encontró URI en el video: {dir(video)}")
                        raise Exception("Video sin URI válido")
                else:
                    logger.error("Lista de videos generados está vacía")
                    raise Exception("No se generó ningún video")

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
        Genera guiones profesionales usando estructuras de persuasión (AIDA/PAS)
        """
        try:
            # Definir duración según red social
            if red_social in ["tiktok", "instagram", "youtube"]: # Shorts/Reels
                duracion_instruccion = "DURACIÓN: MAXIMO 15-30 SEGUNDOS. (Estilo rápido y dinámico)."
            else:
                duracion_instruccion = "DURACIÓN: MAXIMO 45-60 SEGUNDOS."

            prompt_auditoria = f"""
            {PROMPT_SISTEMA_CREATIVO}
            
            TAREA: Genera 3 guiones premium para {red_social} sobre el tema: {tema}.
            
            REGLAS DE FORMATO (CRÍTICAS):
            1. {duracion_instruccion}
            2. ESTRUCTURA: [HOOK (1-3s)] -> [VALOR (Rápido)] -> [CTA (Directo)].
            3. Estilo: "Pithy", directo, sin relleno. Cada palabra cuenta.
            
            CADA GUION DEBE INCLUIR:
            - TITULO
            - SCRIPT (Con indicaciones visuales entre paréntesis)
            - DURACIÓN ESTIMADA
            
            Formato: Prolijo y profesional en Markdown.
            """
            
            try:
                response = self.client.models.generate_content(
                    model=self.text_model_name,
                    contents=prompt_auditoria
                )
            except Exception as api_err:
                logger.error(f"Error directo de Google API en guiones: {api_err}")
                raise Exception(f"Error de comunicación con IA: {str(api_err)[:50]}...")
            
            if not response or not response.text:
                logger.error("La IA devolvió una respuesta vacía en guiones")
                raise Exception("La IA no devolvió texto. Revisa filtros de seguridad.")

            texto_generado = response.text
            
            guiones = self._parsear_guiones_pro(texto_generado)
            hashtags = self.generar_hashtags_expertos(tema, red_social)
            horario = calcular_horario_optimo(red_social)
            
            return {
                "guiones": guiones,
                "hashtags": hashtags,
                "horario_optimo": horario,
                "red_social": red_social,
                "sugerencia_portada": self._generar_sugerencia_portada_pro(tema)
            }
            
        except Exception as e:
            logger.error(f"Error en auditoría de guiones: {e}")
            raise

    def generar_hashtags_expertos(self, tema: str, red_social: str = "tiktok") -> List[str]:
        try:
            prompt = f"{PROMPT_SISTEMA_CREATIVO}\nSelecciona 10 hashtags estratégicos (mezcla de volumen alto y nicho) para {red_social} sobre: {tema}. Devuelve solo los hashtags."
            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt
            )
            return [h for h in response.text.split() if h.startswith('#')][:10]
        except:
            return ["#SocialBoost", f"#{red_social}"]

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
            # Usamos Flash para ahorrar costos en metadata
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

    def _parsear_guiones_pro(self, texto: str) -> List[Dict]:
        """Envuelve el texto generado en una estructura legible"""
        # Por ahora devolvemos el texto completo como un solo bloque prolijo
        return [{"titulo": "Estrategia de Contenido SocialBoost", "script": texto, "duracion_estimada": "Auditado"}]

    def _generar_sugerencia_portada_pro(self, tema: str) -> str:
        return self.mejorar_prompt_marketing(f"Una portada impactante para redes sociales sobre {tema}", "imagen")

def crear_ai_processor(api_key: str) -> AIProcessor:
    return AIProcessor(api_key)
