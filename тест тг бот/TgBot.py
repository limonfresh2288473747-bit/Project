import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN', "8245368424:AAF04bbNF2KUsKfaA0Aqk7ZP5gZXLiMEsqg")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="🎯 Крестики-нолики"), KeyboardButton(text="ℹ️ Помощь")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"🤖 Привет, {message.from_user.first_name}!\n\n"
        "🎉 Я работаю на Render.com 24/7!\n"
        "🚀 Бот всегда онлайн и готов к работе!",
        reply_markup=keyboard
    )

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("✅ Бот работает стабильно на Render!")

@dp.message(F.text == "🎮 Игры")
async def show_games(message: types.Message):
    await message.answer("🎯 Доступные игры:\n• Крестики-нолики\n• Викторина\n• Загадки")

@dp.message(F.text == "📊 Статистика")
async def show_stats(message: types.Message):
    await message.answer("📈 Статистика:\n• Сервер: Render.com\n• Аптайм: 99.9%\n• Статус: Активен")

@dp.message(F.text == "🎯 Крестики-нолики")
async def tic_tac_toe(message: types.Message):
    await message.answer("🎮 Крестики-нолики скоро будут доступны!")

@dp.message(F.text == "ℹ️ Помощь")
async def show_help(message: types.Message):
    await message.answer("📞 Помощь:\n• Бот работает на Render\n• 24/7 доступность\n• Быстрые ответы")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы сказали: {message.text}")

async def main():
    logger.info("🚀 Бот запущен на Render.com!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())