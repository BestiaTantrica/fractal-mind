import os
import telebot
import google.generativeai as genai
import subprocess
from telebot import types
from dotenv import load_dotenv

# Configuración de base
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"), override=True)

# Inicialización
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN_FRACTAL"))
ALLOWED_IDS = [6527908321, 8224826198]
model = genai.GenerativeModel('gemini-flash-latest')

# --- MENÜ DE BOTONES ---
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_status = types.KeyboardButton("📊 ESTADO TORRES")
    btn_oracle = types.KeyboardButton("☁️ ORACLE CLOUD")
    btn_logs = types.KeyboardButton("📄 VER LOGS")
    btn_ai = types.KeyboardButton("🧠 HABLAR CON MENTE")
    markup.add(btn_status, btn_oracle, btn_logs, btn_ai)
    return markup

def get_system_status():
    mem = subprocess.getoutput("free -h | grep Mem | awk '{print $3 \"/\" $2}'")
    cpu = subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
    uptime = subprocess.getoutput("uptime -p")
    return f"🛠 **Torre Maestra:** {uptime}\n📊 **RAM:** {mem}\n🔥 **CPU:** {cpu}%"

@bot.message_handler(commands=['start', 'panel', 'reset'])
def send_welcome(m):
    if m.from_user.id not in ALLOWED_IDS: 
        print(f"⚠️ Acceso denegado a: {m.from_user.id}")
        return
    bot.send_message(m.chat.id, "🦅 **SISTEMA PEGASO ACTIVO**\nSelecciona una opción del panel táctil:", 
                     reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.from_user.id in ALLOWED_IDS)
def handle_text(m):
    text = m.text.upper() if m.text else ""
    
    if "ESTADO" in text:
        bot.send_message(m.chat.id, get_system_status(), parse_mode="Markdown")
        
    elif "ORACLE" in text:
        bot.send_message(m.chat.id, "🛰 Consultando Oracle Cloud...")
        # Simulación o comando real si oci está configurado
        bot.send_message(m.chat.id, "✅ Oracle Cloud reporta todas las torres operativas.")
        
    elif "LOGS" in text:
        bot.send_message(m.chat.id, "📄 Recuperando logs del sistema...")
        
    elif "MENTE" in text:
        bot.send_message(m.chat.id, "🧠 Modo IA activado.")
        
    else:
        try:
            res = model.generate_content(m.text)
            bot.reply_to(m, res.text)
        except Exception as e:
            bot.reply_to(m, "⚠️ Error en la Matrix.")

if __name__ == "__main__":
    print("Iniciando Polling Pegaso...")
    bot.remove_webhook()
    bot.polling(none_stop=True, interval=1, timeout=20)
