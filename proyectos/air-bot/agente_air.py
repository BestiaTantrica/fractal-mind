"""
AIR-Bot - Agente Integral Reis
Bot de Telegram para generación de contenido con IA

Funcionalidades:
1. Edición de imágenes con IA
2. Generación de videos completos (Veo 3.1)
3. Creación de guiones y sugerencias para redes sociales
"""

import os
import sys
import logging
import codecs
from io import BytesIO
from pathlib import Path

# Forzar codificación UTF-8 en la salida de consola (solución para Windows)
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
)

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Módulos propios
from core.ai_processor import crear_ai_processor
from core.utils import quota_manager, log_manager, detectar_red_social

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variables de configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_AIR') or os.getenv('TELEGRAM_TOKEN') or os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_AI_API_KEY')
QUOTA_LIMIT_IMAGES = int(os.getenv('QUOTA_LIMIT_IMAGES', '100'))
QUOTA_LIMIT_VIDEOS = int(os.getenv('QUOTA_LIMIT_VIDEOS', '50'))
ADMIN_USER_ID = os.getenv('MY_USER_ID') or os.getenv('ADMIN_USER_ID')

# Inicializar procesador de IA
try:
    if GOOGLE_API_KEY:
        ai_processor = crear_ai_processor(GOOGLE_API_KEY)
        logger.info("Procesador de IA inicializado correctamente")
    else:
        logger.error("GOOGLE_AI_API_KEY / GEMINI_API_KEY no configurado")
        ai_processor = None
except Exception as e:
    logger.error(f"Error inicializando procesador de IA: {e}")
    ai_processor = None

# ========== MIDDLEWARE / FILTROS ==========

async def debug_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Loguea cada vez que llega algo al bot"""
    if update.effective_user:
        logger.info(f"RECIBIDO: Mensaje de {update.effective_user.id} (@{update.effective_user.username}): {update.message.text if update.message else 'no-text'}")
    
    # Si hay ADMIN_USER_ID, filtrar todo lo que no sea del admin
    if ADMIN_USER_ID and update.effective_user:
        if str(update.effective_user.id) != str(ADMIN_USER_ID):
            logger.warning(f"ACCESO DENEGADO: Usuario {update.effective_user.id} intentó usar el bot")
            # Opcional: enviar mensaje de acceso denegado una sola vez
            return False
    return True


# ========== HANDLERS DE COMANDOS ==========

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler del comando /start"""
    mensaje_bienvenida = """
🤖 ¡Hola! Soy **AIR-Bot** - tu Agente Integral para Redes Sociales

 🎯 **¿Qué puedo hacer por ti?**

🖼️ **1. EDITAR IMÁGENES**
Envíame una imagen con lo que quieres cambiar.

🎬 **2. GENERAR VIDEOS PREMIUM**
Escribe "video" + descripción (Ej: "Video de zumba para TikTok").
⏱️ *Espera:* ~10 minutos.

✍️ **3. CREAR GUIONES**
Escribe un tema y te daré ideas virales.

¡Pruébame ahora! 🚀
"""
    await update.message.reply_text(mensaje_bienvenida, parse_mode='Markdown')
    logger.info(f"Usuario {update.effective_user.id} inició el bot")


async def ayuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler del comando /ayuda"""
    mensaje_ayuda = """
📚 **GUÍA DE USO - AIR-Bot**

**🖼️ Para editar imágenes:**
1. Envía una imagen
2. En el caption, describe los cambios
3. ¡Listo! Recibirás la imagen editada

**🎬 Para generar videos:**
1. Escribe "video" o "genera video"
2. Describe el contenido
3. Menciona la red social (TikTok, Instagram, etc.)
Ejemplo: "Video de café humeante para TikTok"

**✍️ Para generar guiones:**
1. Describe tu tema o idea
2. Menciona la red social (opcional)
Ejemplo: "Ideas para Reels de fitness"

**📊 Cuotas diarias:**
- Imágenes: {}/día
- Videos: {}/día (según tu plan Google AI)

¿Necesitas más ayuda? Escríbeme /start
    """.format(QUOTA_LIMIT_IMAGES, QUOTA_LIMIT_VIDEOS)
    
    await update.message.reply_text(mensaje_ayuda, parse_mode='Markdown')


async def cuota_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el estado de las cuotas"""
    try:
        tiene_img, restante_img = quota_manager.verificar_cuota("imagen", QUOTA_LIMIT_IMAGES, QUOTA_LIMIT_VIDEOS)
        tiene_vid, restante_vid = quota_manager.verificar_cuota("video", QUOTA_LIMIT_IMAGES, QUOTA_LIMIT_VIDEOS)
        
        mensaje = f"""
📊 **ESTADO DE CUOTAS**

🖼️ **Imágenes:**
Disponibles: {restante_img}/{QUOTA_LIMIT_IMAGES}

🎬 **Videos:**
Disponibles: {restante_vid}/{QUOTA_LIMIT_VIDEOS}

Las cuotas se resetean diariamente a medianoche UTC.
"""
        await update.message.reply_text(mensaje, parse_mode='Markdown')
        

    except Exception as e:
        logger.error(f"Error mostrando cuotas: {e}")
        await update.message.reply_text("❌ Error al obtener información de cuotas.")


async def sync_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fuerza una sincronización con Git"""
    user_id = str(update.effective_user.id)
    if not ADMIN_USER_ID or user_id != str(ADMIN_USER_ID):
        return
        
    msg = await update.message.reply_text("🔄 Sincronizando repositorio con Git...")
    success, detail = log_manager.sync_manual()
    
    if success:
        await msg.edit_text("✅ Sincronización completada con éxito.")
    else:
        await msg.edit_text(f"❌ Error en la sincronización: {detail}")


async def update_server_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin-only command to update and restart the server"""
    user_id = str(update.effective_user.id)
    if not ADMIN_USER_ID or user_id != str(ADMIN_USER_ID):
        logger.warning(f"Intento de update no autorizado de {user_id}")
        return
        
    await update.message.reply_text("🚀 Iniciando actualización automática del servidor...")
    
    try:
        import subprocess
        # Get base directory
        base_dir = Path(__file__).parent.parent.parent
        
        # Script de actualización que se ejecuta en segundo plano
        update_script = f"""#!/bin/bash
cd "{base_dir}"
git pull
sudo systemctl restart bot-fractal bot-air
"""
        
        # Crear archivo temporal con el script
        script_path = base_dir / "update_temp.sh"
        with open(script_path, 'w') as f:
            f.write(update_script)
        
        # Dar permisos de ejecución
        os.chmod(script_path, 0o755)
        
        # Ejecutar en segundo plano
        subprocess.Popen(
            ["/bin/bash", str(script_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        await update.message.reply_text(
            "✅ Actualización iniciada.\n\n"
            "📥 Git pull ejecutándose...\n"
            "🔄 Servicios reiniciándose...\n\n"
            "El bot podría desconectarse brevemente."
        )
        logger.info(f"Update server iniciado por admin {user_id}")
        
    except Exception as e:
        logger.error(f"Error en update_server: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las interacciones con botones inline"""
    query = update.callback_query
    await query.answer()

    data = query.data
    
    try:
        if data == "cancel":
            await query.edit_message_text(text="❌ Operación cancelada.")
            # Limpiar datos de usuario si es necesario
            context.user_data.clear()
            return

        if data == "confirm_video":
            await generar_video_confirmado(update, context)
        
        elif data == "confirm_imagen":
            await editar_imagen_confirmada(update, context)
            
        elif data == "video_from_script":
            await generar_video_desde_guion(update, context)
            
    except Exception as e:
        logger.error(f"Error en callback: {e}")
        await query.edit_message_text(text=f"⚠️ Ocurrió un error: {e}")


# ========== HANDLERS DE MENSAJES ==========

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensajes con imágenes"""
    try:
        user_id = update.effective_user.id
        caption = update.message.caption or "Edita esta imagen"
        
        # Verificar cuota
        tiene_cuota, restante, costo = quota_manager.verificar_cuota("imagen", QUOTA_LIMIT_IMAGES, QUOTA_LIMIT_VIDEOS)
        
        if not tiene_cuota:
            await update.message.reply_text(
                "❌ **Cuota diaria de imágenes agotada**\n\n"
                "Vuelve mañana o contacta para aumentar tu límite.",
                parse_mode='Markdown'
            )
            return
        
        # Guardar en contexto para confirmar
        context.user_data['pending_image_file_id'] = update.message.photo[-1].file_id
        context.user_data['pending_image_caption'] = caption
        
        # Crear teclado de confirmación
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirmar Edición (PRO)", callback_data="confirm_imagen"),
                InlineKeyboardButton("❌ Cancelar", callback_data="cancel")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🖼️ **Solicitud de Edición (PRO)**\n\n"
            f"📝 Instrucción: {caption}\n"
            f"💰 Precio: {costo} crédito(s)\n"
            f"💳 Saldo restante hoy: {restante} imágenes\n\n"
            f"¿Deseas proceder?",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

        
        # Registrar en log
        log_manager.registrar_interaccion(
            user_id=user_id,
            tipo="IMAGEN_EDICION",
            input_texto=caption,
            output_info={"caption": "Imagen editada"},
            cuota_actual=nueva_cuota
        )
        
        # Enviar resultado
        await update.message.reply_photo(
            photo=BytesIO(imagen_editada),
            caption=f"✅ Imagen editada\n\n📊 Cuota: {nueva_cuota}/{QUOTA_LIMIT_IMAGES}"
        )
        
        # Borrar mensaje de procesamiento
        await msg_procesando.delete()
        
        logger.info(f"Imagen procesada para usuario {user_id}")
        
    except Exception as e:
        logger.error(f"Error procesando imagen: {e}")
        await update.message.reply_text("❌ Error procesando la imagen. Intenta de nuevo.")


async def editar_imagen_confirmada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ejecuta la edición de imagen después de confirmación"""
    query = update.callback_query
    user_id = query.from_user.id
    
    try:
        # Recuperar datos
        file_id = context.user_data.get('pending_image_file_id')
        caption = context.user_data.get('pending_image_caption')
        
        if not file_id:
            await query.edit_message_text("⚠️ Sesión expirada. Por favor envía la imagen de nuevo.")
            return

        await query.edit_message_text("🎨 Procesando imagen con IA... ⏳")
        
        # Descargar imagen
        new_file = await context.bot.get_file(file_id)
        imagen_bytes = await new_file.download_as_bytearray()
        
        # Procesar con IA
        if ai_processor:
            imagen_editada = ai_processor.editar_imagen(bytes(imagen_bytes), caption)
        else:
            raise Exception("Procesador IA no disponible")
            
        # Incrementar cuota
        quota_manager.incrementar_cuota("imagen")
        _, restante, _ = quota_manager.verificar_cuota("imagen", QUOTA_LIMIT_IMAGES, QUOTA_LIMIT_VIDEOS)
        nueva_cuota = QUOTA_LIMIT_IMAGES - restante
        
        # Enviar
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=BytesIO(imagen_editada),
            caption=f"✅ Imagen editada\n\n📊 Cuota: {nueva_cuota}/{QUOTA_LIMIT_IMAGES}"
        )

        # Registrar en log y obtener path
        saved_path = log_manager.registrar_interaccion(
            user_id=user_id,
            tipo="IMAGEN_EDICION",
            input_texto=caption,
            output_info={"caption": "Imagen editada"},
            cuota_actual=nueva_cuota
        )
        
        # FAILSAFE: Enviar archivo de log
        if saved_path and os.path.exists(saved_path):
            with open(saved_path, 'rb') as f:
                 await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=f,
                    caption="📂 Backup de Log (Inbox)"
                )
        
        # Limpiar
        context.user_data.clear()
        
    except Exception as e:
        logger.error(f"Error en edición confirmada: {e}")
        await query.message.reply_text(f"❌ Error: {e}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensajes de texto"""
    try:
        user_id = update.effective_user.id
        texto = update.message.text
        
        # Detectar si es solicitud de video
        es_video = any(palabra in texto.lower() for palabra in ['video', 'genera', 'crea un video', 'quiero un video'])
        
        if es_video:
            await handle_video_request(update, context, texto)
        else:
            await handle_guion_request(update, context, texto)
            
    except Exception as e:
        logger.error(f"Error procesando texto: {e}")
        await update.message.reply_text("❌ Error procesando tu solicitud. Intenta de nuevo.")

async def handle_guion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para el comando explícito /guion"""
    texto = " ".join(context.args) if context.args else ""
    if not texto:
        await update.message.reply_text("💡 Uso: `/guion [tema del contenido]`\nEjemplo: `/guion Ideas para reels de café`", parse_mode='Markdown')
        return
    await handle_guion_request(update, context, texto)

async def handle_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para el comando explícito /video"""
    texto = " ".join(context.args) if context.args else ""
    if not texto:
        await update.message.reply_text("💡 Uso: `/video [descripción del video]`\nEjemplo: `/video Un atardecer cinemático en la playa`", parse_mode='Markdown')
        return
    await handle_video_request(update, context, texto)


async def handle_video_request(update: Update, context: ContextTypes.DEFAULT_TYPE, texto: str):
    """Procesa solicitud de generación de video"""
    try:
        user_id = update.effective_user.id
        
        # Verificar cuota
        tiene_cuota, restante, costo = quota_manager.verificar_cuota("video", QUOTA_LIMIT_IMAGES, QUOTA_LIMIT_VIDEOS)
        
        if not tiene_cuota:
            await update.message.reply_text(
                "❌ **Cuota diaria de videos agotada**\n\n"
                "Vuelve mañana o contacta para aumentar tu límite.",
                parse_mode='Markdown'
            )
            return
        
        # Guardar contexto
        context.user_data['pending_video_prompt'] = texto
        
        # Crear teclado
        keyboard = [
            [
                InlineKeyboardButton("🚀 Generar Video (1 Crédito)", callback_data="confirm_video"),
                InlineKeyboardButton("❌ Cancelar", callback_data="cancel")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🎬 **PREPARANDO VIDEO PREMIUM**\n\n"
            f"📝 **Idea:** {texto}\n"
            f"💰 **Costo:** 1 Crédito (Te quedan {restante} hoy)\n"
            f"⏱️ **Espera estimada:** 5-10 minutos (Veo 3.1)\n\n"
            f"¿Confirmo la generación?",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
        
        # Registrar en log
        log_manager.registrar_interaccion(
            user_id=user_id,
            tipo="VIDEO_GENERACION",
            input_texto=texto,
            output_info=resultado,
            cuota_actual=nueva_cuota
        )
        
        # Formatear respuesta
        mensaje_resultado = f"""
✅ **VIDEO GENERADO** - {red_social.upper()}

📝 **Caption:**
{resultado['caption']}

📄 **Descripción:**
{resultado['descripcion']}

🏷️ **Hashtags:**
{' '.join(resultado['hashtags'])}

⏰ **Mejor horario:**
Lunes-Viernes: {resultado['horario_optimo']['dias_semana']}
Fin de semana: {resultado['horario_optimo']['fin_semana']}

👆 **CTA:**
{resultado['cta']}

📊 Cuota: {nueva_cuota}/{QUOTA_LIMIT_VIDEOS}

📱 Formato: {resultado['formato']} • Duración: {resultado['duracion']}s
"""
        
        # Enviar respuesta
        await update.message.reply_text(mensaje_resultado, parse_mode='Markdown')
        
        # Enviar video real si existe
        if resultado.get('video_bytes'):
            await update.message.reply_video(
                video=BytesIO(resultado['video_bytes']),
                caption=f"🎬 {resultado['caption']}"
            )
        elif resultado.get('video_url'):
            await update.message.reply_text(f"🎬 Video generado: {resultado['video_url']}")
        else:
            msg_error = resultado.get('error', 'No se pudo generar el video.')
            await update.message.reply_text(f"⚠️ {msg_error}")

        # Mensaje final con metadata
        await update.message.reply_text(
            "✅ **METADATA GENERADO**\n"
            "Usa esta información para publicar tu video manualmente si hubo algún error con el archivo.",
            parse_mode='Markdown'
        )
        
        # Borrar mensaje de procesamiento
        await msg_procesando.delete()
        
        logger.info(f"Video generado para usuario {user_id}")
        
    except Exception as e:
        logger.error(f"Error generando video: {e}")
        await update.message.reply_text("❌ Error generando el video. Intenta de nuevo.")


async def generar_video_confirmado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ejecuta la generación de video después de confirmación"""
    query = update.callback_query
    
    try:
        texto = context.user_data.get('pending_video_prompt')
        user_id = query.from_user.id
        
        if not texto:
            await query.edit_message_text("⚠️ Sesión expirada. Por favor envía el comando de nuevo.")
            return

        await query.edit_message_text(
            "🎬 **Generando Video Premium...**\n\n"
            "El modelo Veo 3.1 está creando tu video pixel por pixel.\n"
            "Esto tomará entre **5 y 10 minutos**. \n\n"
            "⚠️ No cierres el chat, te avisaré cuando esté listo. ⏳"
        )
        
        # Detectar red social
        red_social = detectar_red_social(texto)
        
        # Generar video
        resultado = ai_processor.generar_video(texto, red_social)
        
        # Incrementar cuota
        quota_manager.incrementar_cuota("video")
        # FIX: unpacking 3 values
        _, restante, _ = quota_manager.verificar_cuota("video", QUOTA_LIMIT_IMAGES, QUOTA_LIMIT_VIDEOS)
        nueva_cuota = QUOTA_LIMIT_VIDEOS - restante

        # Verificar errores antes de cantar victoria
        if resultado.get('error'):
             await context.bot.send_message(
                 chat_id=query.message.chat_id,
                 text=f"⚠️ **Atención:** {resultado['error']}",
                 parse_mode='Markdown'
             )
             # No retornamos aquí para permitir que se guarde el log, pero evitamos el mensaje de ÉXITO
             mensaje_resultado = None
        else:
            # Enviar resultado solo si no hubo error
            import html
            caption = html.escape(resultado.get('caption', 'Sin caption'))
            desc = html.escape(resultado.get('descripcion', 'Sin descripción'))
            cta = html.escape(resultado.get('cta', 'Sin CTA'))
            tags = html.escape(' '.join(resultado.get('hashtags', [])))
            
            mensaje_resultado = f"""
<b>✅ VIDEO GENERADO - {red_social.upper()}</b>

📝 <b>Caption:</b>
{caption}

📄 <b>Descripción:</b>
{desc}

🏷️ <b>Hashtags:</b>
{tags}

⏰ <b>Mejor horario:</b>
Lunes-Viernes: {resultado.get('horario_optimo', {}).get('dias_semana', 'N/A')}
Fin de semana: {resultado.get('horario_optimo', {}).get('fin_semana', 'N/A')}

👆 <b>CTA:</b>
{cta}

📊 Cuota: {nueva_cuota}/{QUOTA_LIMIT_VIDEOS}
"""
            await context.bot.send_message(chat_id=query.message.chat_id, text=mensaje_resultado, parse_mode='HTML')
        
        # Registrar en log
        saved_path = log_manager.registrar_interaccion(
            user_id=user_id,
            tipo="VIDEO_GENERACION",
            input_texto=texto,
            output_info=resultado,
            cuota_actual=nueva_cuota
        )
        
        # FAILSAFE: Enviar backup
        if saved_path and os.path.exists(saved_path):
             with open(saved_path, 'rb') as f:
                 await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=f,
                    caption="📂 Backup de Log (Inbox)"
                )
        
        # Intentar enviar por URL primero (Telegram soporta envío directo por URL)
        video_url = resultado.get('video_url')
        video_bytes = resultado.get('video_bytes')
        caption_text = f"🎬 {resultado.get('caption', 'Video generado')}"

        enviado = False
        
        if video_url:
            try:
                logger.info(f"Intentando enviar video por URL: {video_url}")
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=video_url,
                    caption=caption_text
                )
                enviado = True
            except Exception as e:
                logger.warning(f"Fallo envío por URL: {e}. Intentando fallback...")
        
        if not enviado and video_bytes:
            try:
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=BytesIO(video_bytes),
                    caption=caption_text
                )
                enviado = True
            except Exception as e:
                logger.error(f"Fallo envío por bytes: {e}")

        if not enviado:
             if video_url:
                 try:
                     import requests
                     logger.info(f"Descargando video para envío manual: {video_url}")
                     resp = requests.get(video_url, timeout=60)
                     if resp.status_code == 200:
                         await context.bot.send_video(
                             chat_id=query.message.chat_id,
                             video=BytesIO(resp.content),
                             caption=caption_text
                         )
                         enviado = True
                 except Exception as download_err:
                     logger.error(f"Error descargando video: {download_err}")

             if not enviado:
                 if video_url:
                     await context.bot.send_message(
                         chat_id=query.message.chat_id, 
                         text=f"🎬 **Video Listo**\n\nNo pude procesar el archivo directo en Telegram, pero puedes descargarlo aquí:\n{video_url}"
                     )
                 elif not resultado.get('error'): 
                     msg_error = resultado.get('error', 'No se pudo generar el video.')
                     await context.bot.send_message(chat_id=query.message.chat_id, text=f"⚠️ {msg_error}")

        # Limpiar
        context.user_data.clear()

    except Exception as e:
        logger.error(f"Error en video confirmado: {e}")
        await query.message.reply_text(f"❌ Error crítico: {e}")


async def handle_guion_request(update: Update, context: ContextTypes.DEFAULT_TYPE, texto: str):
    """Procesa solicitud de generación de guiones"""
    try:
        user_id = update.effective_user.id
        
        # Notificar procesamiento
        msg_procesando = await update.message.reply_text("✍️ Generando guiones creativos... ⏳")
        
        # Detectar red social
        red_social = detectar_red_social(texto)
        
        # Generar guiones con IA
        if ai_processor:
            resultado = ai_processor.generar_guiones(texto, red_social)
        else:
            raise Exception("Procesador de IA no disponible")
        
        # Registrar en log (NO gasta cuota)
        saved_path = log_manager.registrar_interaccion(
            user_id=user_id,
            tipo="GUION_GENERACION",
            input_texto=texto,
            output_info=resultado,
            cuota_actual=None
        )
        
        # FAILSAFE: Enviar archivo de log
        if saved_path and os.path.exists(saved_path):
            with open(saved_path, 'rb') as f:
                 await update.message.reply_document(
                    document=f,
                    caption="📂 Guion Guardado (Inbox)"
                )
        
        # Formatear guiones
        guiones_texto = "\n\n".join([
            f"**{g['titulo']}**\n{g['script']}\n⏱️ {g['duracion_estimada']}"
            for g in resultado['guiones']])
        
        mensaje_resultado = f"""
✅ **GUIONES GENERADOS** - {red_social.upper()}

{guiones_texto}

🖼️ **Sugerencia de portada:**
{resultado['sugerencia_portada']}

🏷️ **Hashtags:**
{' '.join(resultado['hashtags'])}

⏰ **Mejor horario:**
Lunes-Viernes: {resultado['horario_optimo']['dias_semana']}
Fin de semana: {resultado['horario_optimo']['fin_semana']}

💡 **Tip:** Usa estos guiones como base y personalízalos con tu estilo único
"""
        
        # Enviar respuesta - Quitamos Markdown para evitar errores de parseo con caracteres especiales
        try:
            await update.message.reply_text(mensaje_resultado)
        except Exception as telegram_err:
            logger.warning(f"Error con mensaje formateado, enviando crudo: {telegram_err}")
            # Si falla el formateado, enviamos el script pelado
            await update.message.reply_text(f"✅ GUIONES (Modo Simple):\n\n{guiones_texto[:3000]}")
        
        # Guardar tema en contexto para el botón
        context.user_data['last_script_topic'] = texto
        
        # Botón para generar video
        keyboard = [[InlineKeyboardButton("🎬 Generar Video de esto", callback_data="video_from_script")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "¿Quieres convertir este tema en un video ahora?",
            reply_markup=reply_markup
        )
        
        # Borrar mensaje de procesamiento
        try:
            await msg_procesando.delete()
        except:
            pass
        
        logger.info(f"Guiones generados para usuario {user_id}")
        
    except Exception as e:
        logger.error(f"Error generando guiones: {e}")
        await update.message.reply_text("❌ Error generando los guiones. Intenta de nuevo.")

async def generar_video_desde_guion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback para generar video desde un guion previo"""
    query = update.callback_query
    
    # Recuperar tema del contexto
    tema = context.user_data.get('last_script_topic')
    if not tema:
        await query.edit_message_text("⚠️ Sesión expirada. Por favor genera el guion de nuevo.")
        return
        
    # Simular comando de video
    # Guardamos el prompt como si el usuario lo hubiera escrito
    context.user_data['pending_video_prompt'] = f"Video sobre {tema}"
    
    # Llamamos directamente a la confirmación
    await generar_video_confirmado(update, context)


# ========== FUNCIÓN PRINCIPAL ==========

def main():
    """Función principal del bot"""
    
    # Verificar configuración
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN / TELEGRAM_BOT_TOKEN no configurado")
        sys.exit(1)
    
    if not GOOGLE_API_KEY:
        logger.error("GEMINI_API_KEY / GOOGLE_AI_API_KEY no configurado")
        sys.exit(1)
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Registrar handlers de comandos (con verificación de middleware)
    application.add_handler(MessageHandler(filters.ALL, debug_middleware), group=-1)
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ayuda", ayuda_command))
    application.add_handler(CommandHandler("cuota", cuota_command))
    application.add_handler(CommandHandler("sync", sync_command))
    application.add_handler(CommandHandler("update_server", update_server_command))
    application.add_handler(CommandHandler("guion", handle_guion_command))
    application.add_handler(CommandHandler("video", handle_video_command))
    
    # Callback Query Handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Registrar handlers de mensajes
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Iniciar bot
    logger.info("AIR-Bot iniciado. Escuchando mensajes...")
    print("\n" + "="*50)
    print("AIR-BOT - AGENTE INTEGRAL REIS")
    print("="*50)
    print("OK: Bot iniciado correctamente")
    print(f"Cuota imagenes: {QUOTA_LIMIT_IMAGES}/dia")
    print(f"Cuota videos: {QUOTA_LIMIT_VIDEOS}/dia")
    print("Escuchando mensajes...")
    print("="*50 + "\n")
    
    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico en el bot: {e}")
        # Aquí se podría implementar un reinicio automático si fuera un servicio
        sys.exit(1)
