import os
import telebot
from google import genai
from dotenv import load_dotenv

# Configuración de rutas y variables
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

# Inicializar Clientes
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
AUTHORIZED_USER = int(os.getenv("MY_USER_ID"))

@bot.message_handler(func=lambda message: message.from_user.id == AUTHORIZED_USER)
def handle_message(message):
    try:
        # Nueva forma de llamar al modelo 1.5 Flash
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message.text
        )
        
        full_text = response.text
        
        # Paginación para Telegram (evita error 400)
        for i in range(0, len(full_text), 4000):
            bot.send_message(message.chat.id, full_text[i:i+4000])
            
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

print("Mente Activa con SDK Google-GenAI v1...")
bot.polling()
