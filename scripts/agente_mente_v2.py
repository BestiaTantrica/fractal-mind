import os
import datetime
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
ADMIN_ID = ALLOWED_IDS[0] if ALLOWED_IDS else None
model = genai.GenerativeModel('gemini-flash-latest')

# --- FUNCIONES DE APOYO ---
def get_system_status():
    mem = subprocess.getoutput("free -h | grep Mem | awk '{print $3 \"/\" $2}'")
    cpu = subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
    uptime = subprocess.getoutput("uptime -p")
    return f"🛠 **Maestra:** {uptime}\n📊 **RAM:** {mem}\n🔥 **CPU:** {cpu}%"

def get_oracle_instances():
    # Usamos la ruta absoluta al oci solo por si acaso
    cmd = "/home/ubuntu/bin/oci compute instance list --compartment-id ocid1.tenancy.oc1..aaaaaaaa7xczcsz7xf3qa22n3c6zmn2iy76xkfnqe45yix532hlgyovi3c3a --query \"data[*].{Name:\\\"display-name\\\", State:\\\"lifecycle-state\\\"}\" --output table"
    return subprocess.getoutput(cmd)

# --- HANDLERS DE COMANDOS ---
@bot.message_handler(commands=['panel', 'status', 'start'])
def send_panel(m):
    if m.from_user.id not in ALLOWED_IDS: return
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_status = types.InlineKeyboardButton("📊 Estado Sistemas", callback_data="status")
    btn_oracle = types.InlineKeyboardButton("☁️ Oracle Cloud", callback_data="oracle")
    btn_logs = types.InlineKeyboardButton("📄 Ver Logs", callback_data="logs")
    markup.add(btn_status, btn_oracle, btn_logs)
    
    msg = "🦅 **PEGASO CONSERJE v2.0**\nSistemas listos. ¿Qué quieres monitorear?"
    bot.send_message(m.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.from_user.id not in ALLOWED_IDS: return
    
    if call.data == "status":
        bot.answer_callback_query(call.id, "Consultando Maestra...")
        bot.send_message(call.message.chat.id, get_system_status(), parse_mode="Markdown")
        
    elif call.data == "oracle":
        bot.answer_callback_query(call.id, "Hablando con Oracle...")
        instances = get_oracle_instances()
        bot.send_message(call.message.chat.id, f"☁️ **INSTANCIAS ORACLE:**\n```\n{instances}\n```", parse_mode="Markdown")
        
    elif call.data == "logs":
        bot.answer_callback_query(call.id, "Leyendo bitácora...")
        logs = subprocess.getoutput(f"tail -n 15 {base_dir}/mente.log")
        bot.send_message(call.message.chat.id, f"📄 **ÚLTIMOS LOGS:**\n```\n{logs}\n```", parse_mode="Markdown")

# --- MANTENER FUNCIONES ORIGINALES ---
@bot.message_handler(func=lambda m: m.from_user.id in ALLOWED_IDS, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def handle_ai(m):
    try:
        user_input = m.text or m.caption or "[Media]"
        res = model.generate_content(user_input)
        bot.reply_to(m, res.text)
    except Exception as e:
        bot.reply_to(m, f"❌ Error IA: {e}")

print("Conserje PEGASO Activo.")
bot.polling(none_stop=True)
