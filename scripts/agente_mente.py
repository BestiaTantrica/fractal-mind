import os
import datetime
import telebot
import google.generativeai as genai
from dotenv import load_dotenv

# Carga limpia
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

# Configuración
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN_FRACTAL"))
USER_ID = int(os.getenv("MY_USER_ID"))

# Usamos el nombre exacto de tu lista
model = genai.GenerativeModel('gemini-flash-latest')

def save_to_inbox(content):
    inbox_dir = os.path.join(base_dir, "inbox")
    if not os.path.exists(inbox_dir):
        os.makedirs(inbox_dir)
    
    # FULL STORAGE: Guardamos todo el contenido como pidió el usuario
    lean_content = content
    
    # Buscar el siguiente número disponible
    existing_files = [f for f in os.listdir(inbox_dir) if f.startswith("idea_") and f.endswith(".md")]
    numbers = []
    for f in existing_files:
        try:
            num = int(f.replace("idea_", "").replace(".md", ""))
            numbers.append(num)
        except ValueError:
            continue
    
    next_num = max(numbers) + 1 if numbers else 1
    file_name = f"idea_{next_num}.md"
    file_path = os.path.join(inbox_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(lean_content)
    
    # Sincronización automática (Git Push) - NO BLOQUEANTE
    try:
        os.system(f"cd \"{base_dir}\" && git add \"{file_path}\" && git commit -m 'Auto-save (lean): {file_name}' && git push origin main &")
    except Exception as e:
        print(f"Error en sincronización Git: {e}")
        
    return file_path

@bot.message_handler(commands=['update_server'])
def update_server(m):
    if m.from_user.id != USER_ID:
        return
    bot.reply_to(m, "🚀 Iniciando actualización del servidor...")
    try:
        # Comando para actualizar y reiniciar
        # Nota: requiere que el usuario tenga permisos de sudo sin pass para systemctl
        cmd = f"cd \"{base_dir}\" && git pull && sudo systemctl restart bot-fractal bot-air"
        os.system(f"{cmd} &")
        bot.send_message(m.chat.id, "✅ Comando enviado. El servidor se reiniciará en unos segundos.")
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}")

@bot.message_handler(func=lambda m: m.from_user.id == USER_ID)
def handle(m):
    try:
        # Generación directa
        res = model.generate_content(m.text)
        txt = res.text
        
        # Guardar en inbox
        file_path = None
        try:
            file_path = save_to_inbox(txt)
            # FAILSAFE: Enviar también el archivo generado por Telegram
            if file_path and os.path.exists(file_path):
                with open(file_path, 'rb') as doc:
                    bot.send_document(m.chat.id, doc, caption="📂 Copia de seguridad del archivo generado")
        except Exception as e:
            print(f"Error guardando/enviando: {e}")
        
        # Paginación para Telegram
        for i in range(0, len(txt), 4000):
            bot.send_message(m.chat.id, txt[i:i+4000])
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

print("Bot activo con gemini-flash-latest y guardado en inbox...")
bot.polling()
