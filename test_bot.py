import os
import telebot
from dotenv import load_dotenv

# Configuración de base
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")
load_dotenv(env_path)

token = os.getenv("TELEGRAM_TOKEN_FRACTAL")
print(f"DEBUG: Token encontrado (primeros 5): {token[:5] if token else 'None'}")

try:
    bot = telebot.TeleBot(token)
    me = bot.get_me()
    print(f"BOT_STATUS: ONLINE")
    print(f"BOT_NAME: {me.first_name}")
    print(f"BOT_ID: {me.id}")
except Exception as e:
    print(f"BOT_STATUS: ERROR")
    print(f"ERROR: {e}")
