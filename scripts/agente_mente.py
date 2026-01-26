import os
import telebot
import google.generativeai as genai
from dotenv import load_dotenv

# Carga limpia
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

# Configuración
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
USER_ID = int(os.getenv("MY_USER_ID"))

# Usamos el nombre exacto de tu lista
model = genai.GenerativeModel('gemini-flash-latest')

@bot.message_handler(func=lambda m: m.from_user.id == USER_ID)
def handle(m):
    try:
        # Generación directa
        res = model.generate_content(m.text)
        txt = res.text
        
        # Paginación para Telegram
        for i in range(0, len(txt), 4000):
            bot.send_message(m.chat.id, txt[i:i+4000])
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

print("Bot activo con gemini-flash-latest...")
bot.polling()
