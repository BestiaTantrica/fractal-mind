import os
import telebot
import google.generativeai as genai
import subprocess
import sys
from telebot import types
from dotenv import load_dotenv

# Configuración de base
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"), override=True)

print("--- DEBUG PEGASO START ---")
print(f"Base Dir: {base_dir}")
print(f"Token: {os.getenv('TELEGRAM_TOKEN_FRACTAL')[:5]}...")

# Inicialización
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN_FRACTAL"))
ALLOWED_IDS = [6527908321, 8224826198]
model = genai.GenerativeModel('gemini-flash-latest')

print(f"IDs Permitidos: {ALLOWED_IDS}")

# --- MENÚ DE BOTONES ---
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_status = types.KeyboardButton("📊 ESTADO TORRES")
    btn_oracle = types.KeyboardButton("☁️ ORACLE CLOUD")
    btn_logs = types.KeyboardButton("📄 VER LOGS")
    btn_ai = types.KeyboardButton("🧠 HABLAR CON MENTE")
    markup.add(btn_status, btn_oracle, btn_logs, btn_ai)
    return markup

# --- HANDLERS ---
@bot.message_handler(func=lambda m: True)
def debug_all(m):
    print(f"DEBUG: Mensaje recibido de {m.from_user.id}: {m.text}")
    
    if m.from_user.id not in ALLOWED_IDS:
        print(f"⚠️ ID {m.from_user.id} NO AUTORIZADO")
        return

    text = m.text.upper() if m.text else ""
    
    if "ESTADO" in text:
        bot.send_message(m.chat.id, "📊 RAM: OK | CPU: OK (Debug Mode)")
        
    elif "MENTE" in text:
        bot.send_message(m.chat.id, "🧠 Modo IA activo.")
        
    else:
        try:
            print("Enviando a Gemini...")
            res = model.generate_content(m.text)
            bot.reply_to(m, res.text)
            print("Respuesta enviada.")
        except Exception as e:
            print(f"❌ Error Gemini: {e}")
            bot.reply_to(m, "⚠️ Error procesando pensamiento.")

print("Bot en Polling (Debug Mode)...")
try:
    bot.remove_webhook()
    bot.polling(none_stop=True)
except Exception as e:
    print(f"FATAL ERROR: {e}")
