import os
import random
import asyncio
from http.server import BaseHTTPRequestHandler
from aiogram import Bot

# ================= НАСТРОЙКИ БОТА =================
BOT_TOKEN = "8775675496:AAHTF75MjKlX1Grkv9a6CfUI5lEWESf7g4w"
GROUP_ID = "-1001902195458"
# ==================================================

def get_random_quote():
    try:
        # Вычисляем точный путь к файлу quotes.txt, который лежит в корне проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "quotes.txt")
        
        if not os.path.exists(file_path):
            return f"Ошибка: Файл не найден по пути {file_path}"
            
        with open(file_path, "r", encoding="utf-8") as file:
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Запускаем асинхронную задачу отправки
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_quote())
        loop.close()
        
        # Возвращаем успешный ответ серверу
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Джейсон Стэтхем выполнил работу!".encode('utf-8'))
