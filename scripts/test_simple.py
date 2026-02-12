import telebot
import os
from dotenv import load_dotenv

base_dir = '/home/ubuntu/fractal-mind'
load_dotenv(os.path.join(base_dir, '.env'))
token = os.getenv('TELEGRAM_TOKEN_FRACTAL')
bot = telebot.TeleBot(token)

print(f'Iniciando Test Simple con token: {token[:10]}...')

@bot.message_handler(func=lambda m: True)
def echo_all(m):
    print(f'Mensaje recibido: {m.text}')
    bot.reply_to(m, f'TEST OK: {m.text}')

bot.infinity_polling()
