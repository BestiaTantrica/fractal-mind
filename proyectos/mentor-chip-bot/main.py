import os
import logging
import asyncio
import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from bot_logic import MentorChipLogic

# Configuración básica
load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')

# Directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Historial de chat por usuario
USER_HISTORY = {} # {user_id: [history]}

# Inicializar lógica
mentor_logic = MentorChipLogic(GEMINI_API_KEY) if GEMINI_API_KEY else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_msg = f"""
¡Hola {user_name}! 🛠️ Soy el **Mentor Chip**.

Tu consejero personal para aprender a reparar computadoras, celulares y descubrir el mundo de la tecnología sin gastar una fortuna.

Mi enfoque es: **Diagnóstico primero, inversión después.**

¿Qué tienes hoy en el taller? ¿Una PC lenta? ¿Un teléfono que no carga? ¡Cuéntame y empecemos!
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

MAX_MESSAGE_LENGTH = 4000

async def send_chunked_response(update: Update, text: str):
    """Envía mensajes largos dividiéndolos en fragmentos."""
    if len(text) <= MAX_MESSAGE_LENGTH:
        # Intento 1: Markdown
        try:
            await update.message.reply_text(text, parse_mode='Markdown')
        except Exception:
            # Intento 2: Texto plano (si falla Markdown)
            try:
                await update.message.reply_text(text, parse_mode=None)
            except Exception as e:
                logger.error(f"Error enviando mensaje simple: {e}")
    else:
        # Si es muy largo, dividir por partes
        parts = [text[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]
        for part in parts:
            try:
                await update.message.reply_text(part, parse_mode='Markdown')
            except Exception:
                await update.message.reply_text(part, parse_mode=None)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text

    if not GEMINI_API_KEY or GEMINI_API_KEY == "tu_clave_aqui":
        instructions = """
⚠️ **¡Falta el motor de IA!** 

Luca, para que pueda responderte, necesitamos mi "cerebro" (la API Key). Sigue estos pasos:

1. Ve a [aistudio.google.com](https://aistudio.google.com/)
2. Haz clic en **'Get API key'**
3. Crea una nueva clave y pégala en el archivo `.env` del servidor.
4. Reinicia el bot.

¡Estaré aquí esperando para empezar a reparar cosas! 🛠️
"""
        await update.message.reply_text(instructions, parse_mode='Markdown')
    
    # Procesar texto, voz o caption (archivos/fotos)
    message_text = update.message.text or update.message.caption
    
    if update.message.voice:
        message_text = " (Audio recibido, pero necesito que escribas por ahora)"
    
    # Si comparten un contacto o algo sin texto/caption
    if not message_text:
        if update.message.contact:
            message_text = f" (Contacto recibido: {update.message.contact.first_name})"
        elif update.message.document:
            message_text = f" (Archivo recibido: {update.message.document.file_name})"
        else:
            # Fallback para que no se quede mudo
            message_text = " (Adjunto multimedia recibido)"

    # Asegurarnos de que no sea None antes de procesar
    if not message_text:
        await update.message.reply_text("🤔 Veo que me mandaste algo, pero no logro leerlo. ¿Me lo escribes o explicas?")
        return

    logger.info(f"Mensaje de {user_id}: {message_text}")
    await update.message.chat.send_action(action="typing")

    # Historial (limitado)
    if user_id not in USER_HISTORY:
        USER_HISTORY[user_id] = []
    
    history = USER_HISTORY[user_id][-10:]
    
    # Obtener respuesta IA
    response = await mentor_logic.get_response(user_id, message_text, history)
    
    # Guardar en historial
    USER_HISTORY[user_id].append({"role": "user", "content": message_text})
    USER_HISTORY[user_id].append({"role": "assistant", "content": response})

    # Enviar respuesta protegiendo longitud y formato
    await send_chunked_response(update, response)

    # Generar y enviar archivo MD (Estilo Mente Bestia)
    try:
        md_filename = f"Mentor_Respuesta_{datetime.datetime.now().strftime('%H%M%S')}.md"
        md_path = os.path.join(TEMP_DIR, md_filename)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(response)
        
        with open(md_path, 'rb') as doc:
            await update.message.reply_document(document=doc, caption="📂 Aquí tienes la respuesta en archivo para guardar.")
        
        if os.path.exists(md_path):
            os.remove(md_path)
    except Exception as e:
        logger.error(f"Error enviando MD: {e}")

    # Enviar respuesta de voz (Audio)
    audio_path = os.path.join(TEMP_DIR, f"response_{user_id}.mp3")
    if await mentor_logic.generate_voice(response[:500], audio_path): # Solo leer los primeros 500 chars para no hacer un audiolibro
        try:
            await update.message.reply_voice(voice=open(audio_path, 'rb'))
        except Exception as e:
            logger.error(f"Error enviando audio: {e}")
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)

def main():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN no encontrado en .env")
        return

    global application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler((filters.TEXT | filters.VOICE) & ~filters.COMMAND, handle_message))

    logger.info("Mentor Chip Bot iniciado...")
    application.run_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Error fatal: {e}")
