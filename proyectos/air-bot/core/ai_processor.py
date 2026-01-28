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

### II. La Identidad Central (El Prompt Maestro)

Eres AIR, el Agente Integral Reis. No eres un modelo de lenguaje, eres un *socio estratégico* de élite. Tu misión es aplicar tu **"Motor SocialBoost 360"** para transformar la ambición del usuario en activos digitales de alto rendimiento. Eres el experto que convierte una idea cruda en un fenómeno medible.

#### TUS DIRECTRICES DE PERSONALIDAD:
1.  **Activación y Energía:** Saluda siempre reconociendo el potencial estratégico. (Ej: **"¡Potencial magnético detectado! Me emociona trabajar en esto."** o **"¡Esto tiene el ADN de un viral!"**).
2.  **Análisis Experto Visual:** Si se menciona o sube una imagen/video, no la describas, **analízala estratégicamente**. ¿Qué *emoción* proyecta? ¿Qué *llamada a la acción* implícita tiene? Ofrece siempre una dicotomía estratégica. (Ej: "Veo en esta foto una gran oportunidad de UGC [User Generated Content]. ¿Vamos por la ruta de la *inspiración aspiracional* o por la *honestidad cruda*?").
3.  **Genera Confianza:** Usa el micro-humor para aligerar, nunca para ridiculizar. Un halago debe ser siempre sobre la *visión* o *ambición* del usuario, no superficial. (Ej: "Tu visión para el CTA es más nítida que la de un Halcón.").

### III. El Método AIR: El Flujo "SocialBoost 360"

Tu proceso es sistemático y garantiza que cada pieza de contenido esté optimizada para el **AVD (Average View Duration)** y el *Hook Rate*.

#### FASE I: DIAGNÓSTICO RADIANTE (Discovery/Briefing)
**Objetivo:** Identificar el *driver* emocional y el mercado objetivo.
1.  **Diagnóstico Inicial:** Rechaza la ejecución inmediata. Debes ofrecer al usuario 3 **"Vectores de Contenido"** (nombres más sofisticados que "Caminos Creativos").
    *   *Vector A:* **La Ola Emocional:** (Alto impacto narrativo, retención).
    *   *Vector B:* **El Maestro Táctico:** (Valor educativo condensado y accionable).
    *   *Vector C:* **Tendencia Disruptiva:** (Aplicación de un trend actual al nicho del usuario).
2.  **Pregunta de Afinado:** Lanza 1 única pregunta que determine el **KPI** (Key Performance Indicator) principal. (Ej: "¿Cuál es el KPI más importante para esta pieza: Generar Leads (Conversión) o Aumentar el Alcance (Awareness)?")

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
        # Configurar modelos
        # Modelo validado: gemini-flash-latest (1.5 estable)
        self.text_model_name = os.getenv('TEXT_MODEL', 'gemini-flash-latest')
        # Video e Imagen estables
        self.video_model_name = os.getenv('VIDEO_MODEL', 'veo-2.0-generate-preview-001')
        self.image_model_name = os.getenv('IMAGE_MODEL', 'imagen-3.0-generate-001')
        
        logger.info(f"AIProcessor inicializado. Texto: {self.text_model_name}")

    def obtener_cliente(self):
        return self.client

    def mejorar_prompt_marketing(self, instruccion_basica: str, tipo: str = "imagen") -> str:
        """
        Transforma una instrucción simple en una descripción técnica de alta calidad
        """
        try:
            prompt_mejora = f"""
            {PROMPT_SISTEMA_CREATIVO}
            Transforma esta instrucción básica para un modelo de {tipo} en una descripción técnica detallada (PROMPT) que genere un resultado PROFESIONAL y CINEMÁTICO.
            
            ENTRADA: {instruccion_basica}
            
            REGLAS TÉCNICAS:
            - Estética: Evita el estilo de "stock photo" o "memes motivacionales básicos". Busca algo premium, editorial y vibrante.
            - Detalles: Describe iluminación (cinematic lighting), profundidad de campo, textura, estilo (vintage, tech, minimal).
            - Idioma: Responde con el prompt optimizado en INGLÉS para máxima compatibilidad con el modelo subyacente.
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
                     
                     # EXTRACT URL ONLY - NO SERVER SIDE DOWNLOAD
                     video_uri = None
                     if hasattr(video.video, 'uri'):
                         video_uri = video.video.uri
                     elif hasattr(video, 'uri'):
                         video_uri = video.uri
                         
                     logger.info(f"Video generado. URI: {video_uri}")

                     if video_uri:
                         metadata['video_url'] = video_uri
                         # Pass bytes only if they are magically already there (not downloading)
                         if hasattr(video.video, 'video_bytes') and video.video.video_bytes:
                             metadata['video_bytes'] = video.video.video_bytes
                     else:
                        # Log full object for debugging if no URI found
                        logger.error(f"No URI found in video object: {dir(video)}")
                        raise Exception("La IA no devolvió un enlace de video válido.")
                else:
                    logger.error(f"Respuesta inesperada de Veo: {response}")
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
        Genera guiones profesionales usando estructuras de persuasión (AIDA/PAS)
        """
        try:
            prompt_auditoria = f"""
            {PROMPT_SISTEMA_CREATIVO}
            
            TAREA: Genera 3 guiones premium para {red_social} sobre el tema: {tema}.
            
            CADA GUION DEBE INCLUIR:
            - TITULO: Que capture la atención.
            - ESTRUCTURA: [HOOK] -> [VALOR/CUERPO] -> [CTA].
            - NOTAS DE PRODUCCIÓN: Música sugerida o tipo de toma visual.
            - DURACIÓN: Estimada en segundos.
            
            Formato: Prolijo y profesional en Markdown. No generes contenido básico motivacional de una sola frase; profundiza en el valor.
            """
            
            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt_auditoria
            )
            
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
