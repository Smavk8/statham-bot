import os
import random
import json
import urllib.request
from http.server import BaseHTTPRequestHandler

# ================= НАСТРОЙКИ БОТА =================
BOT_TOKEN = "8775675496:AAHTF75MjKlX1Grkv9a6CfUI5lEWESf7g4w"
GROUP_ID = "-1001902195458"
FILE_NAME = "quotes.txt"
# ==================================================

def get_random_quote():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, FILE_NAME)
        
        if not os.path.exists(file_path):
            return f"Джейсон Стэтхем говорит: файл {FILE_NAME} не найден!"
            
        with open(file_path, "r", encoding="utf-8") as file:
            quotes = [line.strip() for line in file if line.strip()]
        return random.choice(quotes) if quotes else "Файл с цитатами пуст!"
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": GROUP_ID,
        "text": text
    }
    headers = {"Content-Type": "application/json"}
    
    # Отправляем стандартный POST-запрос напрямую в Telegram без aiogram
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    with urllib.request.urlopen(req) as response:
        return response.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Получаем цитату
        quote = get_random_quote()
        
        # 2. Отправляем в Telegram
        try:
            send_telegram_message(quote)
            status_text = "Джейсон Стэтхем успешно выдал базу в чат!"
            response_code = 200
        except Exception as e:
            status_text = f"Ошибка при отправке в Telegram: {e}"
            response_code = 500
        
        # 3. Отдаем ответ серверу Vercel
        self.send_response(response_code)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(status_text.encode('utf-8'))
