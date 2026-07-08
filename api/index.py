import asyncio
import random
from aiogram import Bot

# --- ВАШИ НАСТРОЙКИ ---
API_TOKEN = '8775675496:AAHTF75MjKlX1Grkv9a6CfUI5lEWESf7g4w'
GROUP_ID = '-5461372297'  # Должен быть строкой, например: '-100123456789'
# ---------------------

bot = Bot(token=API_TOKEN)


def get_quotes():
    with open('quotes.txt', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


async def send_quotes():
    quotes = get_quotes()
    random.shuffle(quotes)  # Перемешиваем, чтобы шли в случайном порядке

    for quote in quotes:
        try:
            await bot.send_message(GROUP_ID, quote)
            print(f"Цитата отправлена: {quote[:30]}...")
        except Exception as e:
            print(f"Ошибка при отправке: {e}")

        # Пауза 4 часа (4 часа * 60 минут * 60 секунд = 14400 секунд)
        await asyncio.sleep(14400)


async def main():
    print("Бот запущен и готов к работе!")
    await send_quotes()


if __name__ == '__main__':
    asyncio.run(main())