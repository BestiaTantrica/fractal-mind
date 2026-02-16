import telebot
import json
import os
from datetime import datetime

BOT_TOKEN = "8509893705:AAF6ycIJ4TswQkiguZWzTOa6knHmB5hgnIU"
AUTHORIZED_CHAT_ID = 6527908321  # Solo el usuario puede consultar
STATUS_FILE = "/home/ubuntu/cazador_status.json"
LOG_FILE = "/home/ubuntu/cazador.log"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['cazador'])
def cazador_status(message):
    """Lee el estado del cazador y lo reporta"""
    # Verificar autorización
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "⛔ No autorizado.")
        return
    
    try:
        if not os.path.exists(STATUS_FILE):
            bot.reply_to(message, "⚠️ El cazador aún no ha iniciado o no está corriendo.")
            return
        
        with open(STATUS_FILE, "r") as f:
            data = json.load(f)
        
        timestamp = data.get("timestamp", "N/A")
        intentos = data.get("intentos", 0)
        zona = data.get("zona_actual", "N/A")
        estado = data.get("estado", "DESCONOCIDO")
        detalle = data.get("detalle", "")
        
        # Calcular tiempo desde última actualización
        try:
            ts = datetime.fromisoformat(timestamp)
            ahora = datetime.now()
            diff = (ahora - ts).total_seconds()
            tiempo_desde = f"{int(diff)}s" if diff < 600 else f"{int(diff/60)} min"
        except:
            tiempo_desde = "N/A"
        
        # Emojis según estado
        emoji_map = {
            "CAZANDO": "🏹",
            "ÉXITO": "✅",
            "PÁNICO": "🚨",
            "ERROR": "❌",
            "INICIANDO": "🔄"
        }
        emoji = emoji_map.get(estado, "🔍")
        
        msg = f"{emoji} **ESTADO DEL CAZADOR**\n\n"
        msg += f"📊 Intentos: {intentos}\n"
        msg += f"📍 Zona actual: {zona}\n"
        msg += f"⏱️ Última actualización: {tiempo_desde} atrás\n"
        msg += f"🎯 Estado: {estado}\n"
        
        if detalle:
            msg += f"\n💬 {detalle}"
        
        bot.reply_to(message, msg, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error leyendo estado: {str(e)}")

@bot.message_handler(commands=['logs'])
def ver_logs(message):
    """Muestra las últimas 15 líneas del log del cazador"""
    # Verificar autorización
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "⛔ No autorizado.")
        return
    
    try:
        if not os.path.exists(LOG_FILE):
            bot.reply_to(message, "⚠️ Aún no hay logs disponibles.")
            return
        
        # Leer últimas 15 líneas
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        
        ultimas = lines[-15:] if len(lines) > 15 else lines
        log_text = "```\n" + "".join(ultimas) + "```"
        
        bot.reply_to(message, f"📜 **ÚLTIMAS ACCIONES DEL CAZADOR:**\n\n{log_text}", parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error leyendo logs: {str(e)}")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
        "🎯 **Cazadora de Instancias ARM 24GB**\n\n"
        "Comandos disponibles:\n"
        "/cazador - Ver estado actual del cazador\n"
        "/logs - Ver últimas 15 líneas de actividad\n"
        "/help - Este mensaje",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, "Usá /cazador para ver el estado del cazador 🏹")

if __name__ == "__main__":
    print("🤖 Bot Cazadora iniciado...")
    bot.polling(none_stop=True)
