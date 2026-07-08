import os
import random
import asyncio
from http.server import BaseHTTPRequestHandler
from aiogram import Bot

# ================= НАСТРОЙКИ БОТА =================
BOT_TOKEN = "8775675496:AAHTF75MjKlX1Grkv9a6CfUI5lEWESf7g4w"
GROUP_ID = "-1001902195458"
FILE_NAME = "quotes.txt"
# ==================================================

def get_random_quote():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            quotes = [line.strip() for line in file if line.strip()]
        return random.choice(quotes) if quotes else "Файл с цитатами пуст!"
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

async def send_quote():
    bot = Bot(token=BOT_TOKEN)
    quote = get_random_quote()
    try:
        await bot.send_message(chat_id=GROUP_ID, text=quote)
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
    finally:
        await bot.session.close()

# Класс-обработчик для Vercel (строго с маленькой буквы 'handler')
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        asyncio.run(send_quote())
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Джейсон Стэтхем выполнил работу!".encode('utf-8'))
