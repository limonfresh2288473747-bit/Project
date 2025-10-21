import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN', "8245368424:AAF04bbNF2KUsKfaA0Aqk7ZP5gZXLiMEsqg")

# Проверка токена
if not BOT_TOKEN or BOT_TOKEN == "ваш_токен_здесь":
    logger.error("❌ Токен бота не настроен!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="🎯 Крестики-нолики"), KeyboardButton(text="ℹ️ Помощь")],
        [KeyboardButton(text="🚀 Статус")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"🤖 Привет, {user_name}!\n\n"
        "🎉 Я работаю на Render.com 24/7!\n"
        "🚀 Бот всегда онлайн и готов к работе!\n\n"
        "📅 Сервер: Render.com\n"
        "⏰ Аптайм: 99.9%\n"
        "⚡ Статус: Активен",
        reply_markup=keyboard
    )
    logger.info(f"Пользователь {user_name} запустил бота")

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("✅ Бот работает стабильно на Render.com!\n📊 Все системы в норме")

@dp.message(F.text == "🎮 Игры")
async def show_games(message: types.Message):
    await message.answer(
        "🎮 Игровой центр:\n\n"
        "🎯 Крестики-нолики\n"
        "🧩 Викторина\n"
        "🔍 Загадки\n"
        "🎲 Случайная игра\n\n"
        "Выбери игру из меню!"
    )

@dp.message(F.text == "📊 Статистика")
async def show_stats(message: types.Message):
    await message.answer(
        "📊 Статистика сервера:\n\n"
        "• Хостинг: Render.com\n"
        "• Регион: Европа\n"
        "• Python: 3.11\n"
        "• Библиотека: Aiogram\n"
        "• Статус: 🔥 Активен"
    )

@dp.message(F.text == "🎯 Крестики-нолики")
async def tic_tac_toe(message: types.Message):
    await message.answer(
        "🎯 Крестики-нолики\n\n"
        "Игра скоро будет доступна!\n"
        "Следи за обновлениями 🚀"
    )

@dp.message(F.text == "ℹ️ Помощь")
async def show_help(message: types.Message):
    await message.answer(
        "ℹ️ Помощь по боту:\n\n"
        "• /start - запустить бота\n"
        "• /status - статус сервера\n"
        "• 🎮 Игры - игровое меню\n"
        "• 📊 Статистика - информация\n\n"
        "📞 Техподдержка: @limonfresh2288473747"
    )

@dp.message(F.text == "🚀 Статус")
async def show_server_status(message: types.Message):
    await message.answer("🟢 СЕРВЕР РАБОТАЕТ\n\n📍 Хостинг: Render.com\n⚡ Статус: Активен\n🔧 Техобслуживание: Не требуется")

@dp.message()
async def echo_message(message: types.Message):
    responses = [
        "Отличное сообщение! 👍",
        "Продолжаем общение! 💬",
        "Интересно! Расскажи больше 🤔",
        "Бот работает стабильно! 🚀",
        "Сервер Render отвечает быстро! ⚡"
    ]
    import random
    await message.answer(random.choice(responses))

async def main():
    try:
        # Проверяем подключение
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот @{bot_info.username} запущен на Render!")
        logger.info("🚀 Сервер работает 24/7")
        
        # Запускаем опрос
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TELEGRAM BOT - RENDER.COM")
    print("=" * 50)
    print("🚀 Запуск на облачном сервере...")
    print("📡 Режим: 24/7")
    print("⚡ Статус: Запускается")
    print("=" * 50)
    
    asyncio.run(main())