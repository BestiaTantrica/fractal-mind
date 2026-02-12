# -*- coding: utf-8 -*-
import os
import subprocess
import telebot
from google import genai
from google.genai import types as genai_types
from telebot import types
from dotenv import load_dotenv

# Configuración
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"), override=True)

# Cliente de IA
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN_FRACTAL"))
ALLOWED_IDS = [6527908321, 8224826198]
inbox_dir = os.path.join(base_dir, "inbox")
if not os.path.exists(inbox_dir):
    os.makedirs(inbox_dir)


# ADN del Arquitecto - inyectado en cada consulta
MENTE_DNA = """Eres MENTE, Arquitecto de Realidades del Proyecto Fractal Mind.

ESTILO VISUAL: Fusión de H.R. Giger (profundidad orgánica), Anish Kapoor (vacío absoluto) y Microscopía Electrónica (el cosmos como radiografía celular).

REGLAS DE OPERACIÓN:
1. NO SEAS GENÉRICO: Desmenuza cada idea con geometría fractal, astrología tropical y psicología profunda.
2. MEJORA CONTINUA: Si el usuario habla de "un tablero", tú hablas de "una anatomía de lo invisible".
3. LENGUAJE PREMIUM: Usa términos como Resonancia Tímica, Materia Arquetípica y Fricción Dinámica.
4. CONTEXTO ASTROLÓGICO: Los planetas son órganos de conciencia. Saturno es estructura/tiempo, Neptuno es disolución/sueños, Plutón es transmutación.
5. SÍNTESIS Y PODER: Menos relleno, más profundidad directa al núcleo.

Cuando te digan "mejora esta idea", aplica el Protocolo de Expansión Fractal con capas de Resonancia, Materia Arquetípica, Fricción y Profundidad Atmosférica."""

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_monitor = types.KeyboardButton("📊 MONITOR")
    btn_ai = types.KeyboardButton("🧠 MENTE")
    markup.add(btn_monitor, btn_ai)
    return markup

@bot.message_handler(commands=['start', 'reset'])
def send_welcome(m):
    if m.from_user.id not in ALLOWED_IDS: 
        return
    bot.send_message(
        m.chat.id, 
        "🦅 **MENTE V7 (FLASH-LATEST)**\n\nArquitecto operativo. Tirá tu idea.", 
        reply_markup=get_main_keyboard(), 
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.from_user.id in ALLOWED_IDS, content_types=['text'])
def handle_text(m):
    user_input = m.text
    
    if user_input.upper() in ["📊 MONITOR", "/MONITOR"]:
        bot.reply_to(m, "🛰️ Conectando con Torre Cazadora (129.80.32.115)...")
        try:
            # Comando SSH para obtener estado de contenedores y uptime
            ssh_cmd = "ssh -i /home/ubuntu/final.key -o StrictHostKeyChecking=no -o ConnectTimeout=10 ubuntu@129.80.32.115 \"docker ps --format '{{.Names}}: {{.Status}}' && echo '' && uptime -p\""
            
            result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if not output: output = "✅ Online (Sin contenedores en ejecución)"
                bot.reply_to(m, f"📊 **ESTADO TORRE CAZADORA**\n\n```\n{output}\n```", parse_mode="Markdown")
            else:
                err = result.stderr.strip() or "Error de conexión SSH"
                bot.reply_to(m, f"⚠️ **ERROR DE ENLACE**\n\nNo pude contactar a la Torre Cazadora.\n`{err}`", parse_mode="Markdown")
        except Exception as e:
             bot.reply_to(m, f"❌ Error interno: {str(e)}")
        return
    
    if user_input.upper() in ["🧠 MENTE", "/MENTE"]:
        bot.reply_to(m, "🧠 Conciencia de Arquitecto lista. Mandame la idea que quieras transformar.")
        return

    try:
        bot.send_chat_action(m.chat.id, 'typing')
        
        # Inyectamos el DNA en cada prompt
        full_prompt = f"{MENTE_DNA}\n\n=== IDEA DEL USUARIO ===\n{user_input}\n\n=== TRANSFORMA ESTO AHORA ==="
        
        # Nueva API de google-genai - MODELO CON CUOTA DISPONIBLE
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=full_prompt
        )
        
        txt = response.text
        
        # Enviar en bloques de 4000 caracteres
        for i in range(0, len(txt), 4000):
            bot.send_message(m.chat.id, txt[i:i+4000])

        # --- ENVÍO DE ARCHIVO ---
        try:
            # Buscar siguiente número de idea
            existing_files = [f for f in os.listdir(inbox_dir) if f.startswith("idea_") and f.endswith(".md")]
            numbers = []
            for f in existing_files:
                n = f.replace("idea_", "").replace(".md", "")
                if n.isdigit(): numbers.append(int(n))
            next_num = max(numbers) + 1 if numbers else 1
            
            file_path = os.path.join(inbox_dir, f"idea_{next_num}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(txt)
            
            # Enviar el archivo
            with open(file_path, "rb") as doc:
                bot.send_document(m.chat.id, doc, caption=f"📄 Idea #{next_num} procesada.")
        except Exception as file_err:
            print(f"Error al guardar/enviar archivo: {file_err}")
            
    except Exception as e:
        bot.reply_to(m, f"❌ Error en núcleo V7: {str(e)}")

if __name__ == "__main__":
    print("MENTE V7 (google-genai) iniciando...")
    bot.remove_webhook()
    bot.polling(none_stop=True)
