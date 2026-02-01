import os
import logging
import asyncio
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
        return

    if update.message.voice:
        await update.message.reply_text("🎤 Escuchando tu nota de voz...")
        # Nota: Por ahora Luca debe escribir, pero ya detectamos el audio.
        text = "He recibido un audio tuyo (Luca), pero mi procesador de audio está en mantenimiento. ¿Podrías escribirme lo mismo por texto? ¡Gracias!"
        await update.message.reply_text(text)
        return

    if not text:
        return

    if not mentor_logic:
        await update.message.reply_text("❌ Error: Mentor Logic no inicializado.")
        return

    # Mostrar que el bot está "escribiendo"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Obtener historial
    history = USER_HISTORY.get(user_id, [])[-10:] # Últimos 10 mensajes

    # Obtener respuesta de la IA
    response = await mentor_logic.get_response(user_id, text, history)

    # Guardar en historial
    if user_id not in USER_HISTORY:
        USER_HISTORY[user_id] = []
    
    USER_HISTORY[user_id].append({"role": "user", "content": text})
    USER_HISTORY[user_id].append({"role": "assistant", "content": response})

    # Enviar respuesta de texto
    await update.message.reply_text(response, parse_mode='Markdown')

    # Enviar respuesta de voz (Audio)
    audio_path = os.path.join(TEMP_DIR, f"response_{user_id}.mp3")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="record_voice")
    
    if await mentor_logic.generate_voice(response, audio_path):
        with open(audio_path, 'rb') as audio:
            await update.message.reply_voice(voice=audio)
        if os.path.exists(audio_path):
            os.remove(audio_path)

def main():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN no encontrado en .env")
        return

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
