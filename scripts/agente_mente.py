import os
import telebot
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
AUTHORIZED_USER = int(os.getenv("MY_USER_ID"))

model = genai.GenerativeModel('gemini-flash-latest')

SYSTEM_PROMPT = """
Eres la 'Mente' de Tomás Reis. Técnico, experto en Trading y Tarot.
Tu objetivo es procesar sus 'vómitos' de ideas:
- Si envía código: Optimízalo y documéntalo.
- Si envía una idea: Transfórmala en un 'Prompt de Ingeniería'.
- Estilo: Directo y técnico.
"""

@bot.message_handler(func=lambda message: message.from_user.id == AUTHORIZED_USER)
def procesar_idea(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        prompt_final = f"{SYSTEM_PROMPT}\n\nENTRADA DE TOMÁS:\n{message.text}"
        response = model.generate_content(prompt_final)
        
        filename = f"inbox/idea_{message.message_id}.md"
        os.makedirs("inbox", exist_ok=True)
        with open(filename, "w") as f:
            f.write(f"# Idea de Tomás\n\n## Entrada:\n{message.text}\n\n## Respuesta Mente:\n{response.text}")
        
        bot.reply_to(message, response.text)
        bot.send_message(message.chat.id, f"✅ Guardado en `{filename}`")
    except Exception as e:
        bot.reply_to(message, f"Che, se rompió algo: {e}")

print("Mente Activa con gemini-flash-latest...")
bot.polling()
