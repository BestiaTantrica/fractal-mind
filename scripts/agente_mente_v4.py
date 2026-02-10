import os
import datetime
import telebot
import google.generativeai as genai
import subprocess
from telebot import types
from dotenv import load_dotenv

# Carga limpia de configuración
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"), override=True)

# Configuración de IA y Bot
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN_FRACTAL"))
ALLOWED_IDS = [6527908321, 8224826198]
model = genai.GenerativeModel('gemini-flash-latest')

# --- MENÚ DE BOTONES ---
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Fila 1: Monitor Unificado y Radar Remoto
    btn_monitor = types.KeyboardButton("📊 MONITOR PEGASO")
    btn_radar = types.KeyboardButton("🔭 RADAR CAZADOR")
    # Fila 2: IA y Oracle (Respaldo)
    btn_ai = types.KeyboardButton("🧠 MENTE")
    btn_oracle = types.KeyboardButton("☁️ ORACLE CLOUD")
    markup.add(btn_monitor, btn_radar, btn_ai, btn_oracle)
    return markup

# --- FUNCIONES DE MONITOR ---
def get_monitor_status():
    # 1. Estado Local (Torre Maestra)
    uptime = subprocess.getoutput("uptime -p").replace("up ", "")
    mem = subprocess.getoutput("free -h | grep Mem | awk '{print $3 \"/\" $2}'")
    
    # 2. Logs Reales (Journalctl)
    logs = subprocess.getoutput("sudo journalctl -u bot-fractal -n 10 --no-pager")
    
    return f"""🦅 **MONITOR PEGASO - TORRE MAESTRA**
⏱ **Uptime:** {uptime}
RUNNING 🟢 | RAM: {mem}

**📝 ÚLTIMOS LOGS:**
```
{logs}
```"""

def get_radar_cazador():
    # Intenta conectar a Torre Cazadora (129.80.32.115) usando final.key
    target_ip = "129.80.32.115"
    key_path = "/home/ubuntu/fractal-mind/final.key"
    try:
        # Timeout corto para no congelar el bot. Tail de los ultimos 10 logs de caceria.
        cmd = f"ssh -i {key_path} -o ConnectTimeout=8 -o StrictHostKeyChecking=no ubuntu@{target_ip} 'tail -n 12 /home/ubuntu/caceria.log'"
        result = subprocess.getoutput(cmd)
        
        if "Permission denied" in result or "timed out" in result:
            return f"🔭 **RADAR CAZADOR (129.80...)**\n⚠️ **ENLACE INTERRUMPIDO**\n\nError de conexión SSH: `{result.splitlines()[0]}`"
            
        if not result:
            return f"🔭 **RADAR CAZADOR (129.80...)**\n💤 **SIN ACTIVIDAD EN LOG**\n\nEl archivo caceria.log está vacío o no existe."
            
        return f"🔭 **RADAR CAZADOR (129.80...)**\n🟢 **ENLACE ACTIVO - ÚLTIMA ACTIVIDAD:**\n```\n{result}\n```"
    except Exception as e:
        return f"⚠️ Error interno en Radar: {e}"

def save_to_inbox(content):
    inbox_dir = os.path.join(base_dir, "inbox")
    if not os.path.exists(inbox_dir):
        os.makedirs(inbox_dir)
    
    existing_files = [f for f in os.listdir(inbox_dir) if f.startswith("idea_") and f.endswith(".md")]
    numbers = [int(f.replace("idea_", "").replace(".md", "")) for f in existing_files if f.replace("idea_", "").replace(".md", "").isdigit()]
    next_num = max(numbers) + 1 if numbers else 1
    
    file_path = os.path.join(inbox_dir, f"idea_{next_num}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Sync silenciosa
    try:
        subprocess.Popen(
            f"cd '{base_dir}' && git add inbox/ && git commit -m 'Auto-sync idea {next_num}' && git push origin main",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    except: pass
    return file_path

# --- HANDLERS ---
@bot.message_handler(commands=['start', 'panel', 'reset'])
def send_welcome(m):
    if m.from_user.id not in ALLOWED_IDS: return
    bot.send_message(m.chat.id, "🦅 **SISTEMA PEGASO V4**\nInterfaz táctil desplegada:", 
                     reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.from_user.id in ALLOWED_IDS, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text'])
def handle_all(m):
    user_input = m.text or m.caption or ""
    text_upper = user_input.upper()

    # 1. Comandos de Monitor
    if "MONITOR" in text_upper:
        bot.send_message(m.chat.id, get_monitor_status(), parse_mode="Markdown")
        
    elif "RADAR" in text_upper:
        bot.send_message(m.chat.id, "🔭 Escaneando sector 129.80... (Puede tardar uns segundos)")
        bot.send_message(m.chat.id, get_radar_cazador(), parse_mode="Markdown")
        
    elif "MENTE" in text_upper:
        bot.send_message(m.chat.id, "🧠 Modo IA activado. Decime qué tenés en mente.")
        
    elif "ORACLE" in text_upper:
        # Fallback a comando OCI si está configurado
        cmd = "/home/ubuntu/bin/oci compute instance list --compartment-id ocid1.tenancy.oc1..aaaaaaaa7xczcsz7xf3qa22n3c6zmn2iy76xkfnqe45yix532hlgyovi3c3a --query \"data[*].{Name:\\\"display-name\\\", State:\\\"lifecycle-state\\\"}\" --output table"
        res = subprocess.getoutput(cmd)
        if "not found" in res: res = "⚠️ OCI CLI no configurado o sin permisos."
        bot.send_message(m.chat.id, f"☁️ **ESTADO ORACLE:**\n```\n{res}\n```", parse_mode="Markdown")
    
    # 2. IA General
    else:
        try:
            res = model.generate_content(user_input)
            txt = res.text
            
            # Guardar siempre
            save_to_inbox(txt)
            
            # Respuesta paginada
            for i in range(0, len(txt), 4000):
                bot.send_message(m.chat.id, txt[i:i+4000])
        except Exception as e:
            bot.reply_to(m, f"❌ Error: {e}")

if __name__ == "__main__":
    print("Pegaso V4 Engine Activo.")
    bot.remove_webhook()
    bot.polling(none_stop=True)
