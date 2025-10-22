import os
import asyncio
import logging
import random
import datetime
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен
BOT_TOKEN = "8245368424:AAF04bbNF2KUsKfaA0Aqk7ZP5gZXLiMEsqg"

# ID администратора (ваш ID в Telegram)
ADMIN_ID =  7233513048  # Замените на ваш реальный ID

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Файл для сохранения данных
DATA_FILE = "users_data.json"

# Загрузка данных
def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}, "stats": {}, "support_sessions": {}}

# Сохранение данных
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({"users": users_data, "stats": user_stats, "support_sessions": support_sessions}, f, ensure_ascii=False, indent=2)

# Загружаем данные
data = load_data()
users_data = data.get("users", {})
user_stats = data.get("stats", {})
support_sessions = data.get("support_sessions", {})
active_games = {}

def get_user(user_id):
    return users_data.get(str(user_id))

def get_user_stats(user_id):
    return user_stats.get(str(user_id), {'games_played': 0, 'games_won': 0, 'total_earned': 0})

def register_user(user_id, username, first_name):
    user_id_str = str(user_id)
    if user_id_str not in users_data:
        users_data[user_id_str] = {
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'balance': 100,
            'level': 1,
            'experience': 0,
            'registered_date': datetime.datetime.now().isoformat(),
            'last_bonus_date': None
        }
        save_data()
    
    if user_id_str not in user_stats:
        user_stats[user_id_str] = {
            'games_played': 0,
            'games_won': 0,
            'total_earned': 0
        }
        save_data()

def update_balance(user_id, amount):
    user_id_str = str(user_id)
    if user_id_str in users_data:
        users_data[user_id_str]['balance'] += amount
        if amount > 0:
            user_stats[user_id_str]['total_earned'] += amount
        save_data()
        return users_data[user_id_str]['balance']
    return 0

def update_stats(user_id, won=False):
    user_id_str = str(user_id)
    if user_id_str in user_stats:
        user_stats[user_id_str]['games_played'] += 1
        if won:
            user_stats[user_id_str]['games_won'] += 1
        save_data()

# Основная клавиатура
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="💰 Баланс")],
            [KeyboardButton(text="📊 Профиль"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="🏆 Топ игроков"), KeyboardButton(text="📞 Поддержка")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )

# Игровая клавиатура
def get_games_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Крестики-нолики"), KeyboardButton(text="🎰 Казино")],
            [KeyboardButton(text="🎲 Кости"), KeyboardButton(text="✂️ Камень-ножницы")],
            [KeyboardButton(text="🔢 Угадай число"), KeyboardButton(text="🎮 Случайная игра")],
            [KeyboardButton(text="🔙 Назад в меню")]
        ],
        resize_keyboard=True
    )

# Клавиатура поддержки
def get_support_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛑 Завершить обращение")],
            [KeyboardButton(text="🔙 Назад в меню")]
        ],
        resize_keyboard=True
    )

# Класс для игры в крестики-нолики
class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_id = f"ttt_{random.randint(1000, 9999)}"
        
    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        if all(cell != ' ' for row in self.board for cell in row):
            return 'Draw'
        
        return None
    
    def get_board_display(self):
        symbols = {'X': '❌', 'O': '⭕', ' ': '⬜'}
        board_text = ""
        for row in self.board:
            for cell in row:
                board_text += symbols[cell]
            board_text += "\n"
        return board_text

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    register_user(user_id, message.from_user.username, message.from_user.first_name)
    
    welcome_text = f"""
🎉 Добро пожаловать, {message.from_user.first_name}!

🤖 Я - продвинутый игровой бот с экономикой!

🎮 **Доступные игры:**
• 🎯 Крестики-нолики
• 🎰 Казино  
• 🎲 Кости
• ✂️ Камень-ножницы
• 🔢 Угадай число
• 🎮 Случайная игра

💰 **Экономическая система:**
• Стартовый баланс: 100 монет
• Ежедневные бонусы: 15-50 монет
• Заработок в играх
• Уровневая система

📞 **Поддержка:**
• Онлайн-чат с администратором
• Быстрые ответы на вопросы

Выбери раздел из меню ниже! 🚀
    """
    
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

# Профиль пользователя
@dp.message(F.text == "📊 Профиль")
async def show_profile(message: types.Message):
    user = get_user(message.from_user.id)
    stats = get_user_stats(message.from_user.id)
    
    if user:
        win_rate = (stats['games_won'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
        
        profile_text = f"""
📊 **ПРОФИЛЬ ИГРОКА**

👤 Имя: {user['first_name']}
🎮 Уровень: {user['level']}
⭐ Опыт: {user['experience']}/100
💰 Баланс: {user['balance']} монет

📈 **Статистика:**
• Игр сыграно: {stats['games_played']}
• Побед: {stats['games_won']}
• Процент побед: {win_rate:.1f}%
• Всего заработано: {stats['total_earned']} монет

📅 Регистрация: {user['registered_date'][:10]}
        """
        await message.answer(profile_text)
    else:
        await message.answer("❌ Профиль не найден. Напишите /start")

# Баланс
@dp.message(F.text == "💰 Баланс")
async def show_balance(message: types.Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer(f"💎 Ваш баланс: {user['balance']} монет")
    else:
        await message.answer("❌ Профиль не найден")

# Игры
@dp.message(F.text == "🎮 Игры")
async def games_center(message: types.Message):
    await message.answer("🎮 Выберите игру:", reply_markup=get_games_keyboard())

# Случайная игра
@dp.message(F.text == "🎮 Случайная игра")
async def random_game(message: types.Message):
    games = [
        "🎯 Крестики-нолики",
        "🎰 Казино", 
        "🎲 Кости",
        "✂️ Камень-ножницы",
        "🔢 Угадай число"
    ]
    selected_game = random.choice(games)
    
    await message.answer(f"🎲 Случайная игра выбрала: {selected_game}!")
    
    # Перенаправляем на выбранную игру
    if selected_game == "🎯 Крестики-нолики":
        await start_tic_tac_toe(message)
    elif selected_game == "🎰 Казино":
        await casino_game(message)
    elif selected_game == "🎲 Кости":
        await dice_game(message)
    elif selected_game == "✂️ Камень-ножницы":
        await rps_game(message)
    elif selected_game == "🔢 Угадай число":
        await guess_number(message)

# Назад в главное меню
@dp.message(F.text == "🔙 Назад в меню")
async def back_to_main(message: types.Message):
    user_id = str(message.from_user.id)
    
    # Завершаем сессию поддержки если активна
    if user_id in support_sessions and support_sessions[user_id]['active']:
        support_sessions[user_id]['active'] = False
        save_data()
        await message.answer("📞 Обращение в поддержку завершено.", reply_markup=get_main_keyboard())
    else:
        await message.answer("🔙 Возвращаемся в главное меню", reply_markup=get_main_keyboard())

# Поддержка
@dp.message(F.text == "📞 Поддержка")
async def support_start(message: types.Message):
    user_id = str(message.from_user.id)
    
    # Создаем сессию поддержки
    support_sessions[user_id] = {
        'active': True,
        'start_time': datetime.datetime.now().isoformat(),
        'message_count': 0
    }
    save_data()
    
    support_text = f"""
📞 **СЛУЖБА ПОДДЕРЖКИ**

👤 Пользователь: {message.from_user.first_name}
🆔 ID: {message.from_user.id}

💬 Теперь все ваши сообщения будут пересылаться администратору.
✍️ Напишите ваш вопрос или проблему.

🛑 Чтобы завершить обращение, нажмите кнопку ниже.
⏰ Время начала: {datetime.datetime.now().strftime('%H:%M')}
    """
    
    # Уведомляем администратора
    admin_notification = f"""
🆕 НОВОЕ ОБРАЩЕНИЕ В ПОДДЕРЖКУ

👤 Пользователь: {message.from_user.first_name}
🆔 ID: {message.from_user.id}
📛 Username: @{message.from_user.username}
⏰ Время: {datetime.datetime.now().strftime('%H:%M')}

💬 Ожидаем сообщение от пользователя...
    """
    
    try:
        await bot.send_message(ADMIN_ID, admin_notification)
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления админу: {e}")
    
    await message.answer(support_text, reply_markup=get_support_keyboard())

# Завершение обращения
@dp.message(F.text == "🛑 Завершить обращение")
async def support_end(message: types.Message):
    user_id = str(message.from_user.id)
    
    if user_id in support_sessions and support_sessions[user_id]['active']:
        support_sessions[user_id]['active'] = False
        save_data()
        
        end_text = f"""
📞 **ОБРАЩЕНИЕ ЗАВЕРШЕНО**

✅ Вы завершили обращение в поддержку.
🕐 Время обращения: {datetime.datetime.now().strftime('%H:%M')}

💫 Если у вас остались вопросы - вы всегда можете написать снова!
        """
        
        # Уведомляем администратора
        admin_notification = f"""
🔚 ОБРАЩЕНИЕ ЗАВЕРШЕНО

👤 Пользователь: {message.from_user.first_name}
🆔 ID: {message.from_user.id}
⏰ Время завершения: {datetime.datetime.now().strftime('%H:%M')}
        """
        
        try:
            await bot.send_message(ADMIN_ID, admin_notification)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления админу: {e}")
        
        await message.answer(end_text, reply_markup=get_main_keyboard())
    else:
        await message.answer("❌ У вас нет активных обращений в поддержку.")

# Обработка сообщений в режиме поддержки
@dp.message(F.text & ~F.command)
async def handle_support_messages(message: types.Message):
    user_id = str(message.from_user.id)
    
    # Проверяем активна ли сессия поддержки
    if user_id in support_sessions and support_sessions[user_id]['active']:
        # Увеличиваем счетчик сообщений
        support_sessions[user_id]['message_count'] += 1
        save_data()
        
        # Формируем сообщение для администратора
        admin_message = f"""
📩 СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ

👤 Имя: {message.from_user.first_name}
🆔 ID: {message.from_user.id}
📛 Username: @{message.from_user.username}
🔢 Сообщение №{support_sessions[user_id]['message_count']}

💬 Текст:
{message.text}

⏰ Время: {datetime.datetime.now().strftime('%H:%M:%S')}
        """
        
        # Клавиатура для ответа администратору
        admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Ответить пользователю", callback_data=f"reply_{user_id}")],
            [InlineKeyboardButton(text="🛑 Завершить обращение", callback_data=f"close_support_{user_id}")]
        ])
        
        try:
            await bot.send_message(ADMIN_ID, admin_message, reply_markup=admin_keyboard)
            await message.answer("✅ Ваше сообщение отправлено администратору!")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения админу: {e}")
            await message.answer("❌ Ошибка отправки сообщения. Попробуйте позже.")
        
        return
    
    # Если не в режиме поддержки, обрабатываем как обычное сообщение
    responses = [
        "Выбери действие из меню! 📱",
        "Интересно! Расскажи больше 🤔",
        "Бот работает стабильно! 🚀",
        "Попробуй сыграть в игры! 🎮",
        "Проверь свой профиль! 📊",
        "Не забудь про ежедневный бонус! 🎁",
        "Нужна помощь? Напиши в поддержку! 📞"
    ]
    await message.answer(random.choice(responses))

# Обработчик ответов администратора
@dp.callback_query(F.data.startswith("reply_"))
async def handle_admin_reply(callback: types.CallbackQuery):
    user_id = callback.data.split("_")[1]
    
    await callback.message.answer(f"💬 Введите ответ для пользователя (ID: {user_id}):")
    # Здесь можно добавить логику для ответа пользователю
    await callback.answer("Функция ответа в разработке")

# Обработчик завершения поддержки администратором
@dp.callback_query(F.data.startswith("close_support_"))
async def handle_admin_close_support(callback: types.CallbackQuery):
    user_id = callback.data.split("_")[2]
    
    if user_id in support_sessions:
        support_sessions[user_id]['active'] = False
        save_data()
        
        # Уведомляем пользователя
        try:
            user_info = users_data.get(user_id, {})
            user_name = user_info.get('first_name', 'Пользователь')
            await bot.send_message(
                int(user_id), 
                f"📞 Администратор завершил ваше обращение в поддержку.\n\nСпасибо за обращение, {user_name}! 💫",
                reply_markup=get_main_keyboard()
            )
        except Exception as e:
            logger.error(f"Ошибка уведомления пользователя: {e}")
        
        await callback.message.edit_text(f"✅ Обращение пользователя {user_id} завершено.")
    else:
        await callback.answer("❌ Сессия поддержки не найдена")

# Крестики-нолики (остальной код игр остается таким же)
@dp.message(F.text == "🎯 Крестики-нолики")
async def start_tic_tac_toe(message: types.Message):
    game = TicTacToe()
    active_games[game.game_id] = game
    
    keyboard = InlineKeyboardBuilder()
    for i in range(3):
        for j in range(3):
            keyboard.button(text="⬜", callback_data=f"ttt_{game.game_id}_{i}_{j}")
    keyboard.button(text="🔚 Завершить игру", callback_data=f"ttt_exit_{game.game_id}")
    keyboard.adjust(3, 3, 1)
    
    await message.answer(
        f"🎯 Крестики-нолики\n\nИгрок: ❌\nБот: ⭕\n\n{game.get_board_display()}",
        reply_markup=keyboard.as_markup()
    )

# Обработчик ходов в крестики-нолики
@dp.callback_query(F.data.startswith("ttt_"))
async def handle_tic_tac_toe(callback: types.CallbackQuery):
    data = callback.data.split("_")
    game_id = data[1]
    
    if data[2] == "exit":
        if game_id in active_games:
            del active_games[game_id]
        await callback.message.edit_text("🎯 Игра завершена")
        await callback.answer()
        return
    
    if game_id not in active_games:
        await callback.answer("Игра не найдена")
        return
    
    game = active_games[game_id]
    row, col = int(data[2]), int(data[3])
    
    if game.make_move(row, col):
        winner = game.check_winner()
        
        if not winner:
            empty_cells = [(i, j) for i in range(3) for j in range(3) if game.board[i][j] == ' ']
            if empty_cells:
                bot_row, bot_col = random.choice(empty_cells)
                game.make_move(bot_row, bot_col)
                winner = game.check_winner()
        
        keyboard = InlineKeyboardBuilder()
        for i in range(3):
            for j in range(3):
                symbol = "❌" if game.board[i][j] == 'X' else "⭕" if game.board[i][j] == 'O' else "⬜"
                keyboard.button(text=symbol, callback_data=f"ttt_{game_id}_{i}_{j}")
        keyboard.button(text="🔚 Завершить игру", callback_data=f"ttt_{game_id}_exit")
        keyboard.adjust(3, 3, 1)
        
        status_text = ""
        if winner:
            if winner == 'X':
                status_text = "🎉 Вы победили! +10 монет"
                new_balance = update_balance(callback.from_user.id, 10)
                update_stats(callback.from_user.id, won=True)
            elif winner == 'O':
                status_text = "🤖 Бот победил!"
                update_stats(callback.from_user.id, won=False)
            else:
                status_text = "🤝 Ничья! +5 монет"
                new_balance = update_balance(callback.from_user.id, 5)
                update_stats(callback.from_user.id, won=False)
            
            if winner != 'O':
                status_text += f"\n💎 Новый баланс: {new_balance} монет"
            
            del active_games[game_id]
        
        await callback.message.edit_text(
            f"🎯 Крестики-нолики\n\n{game.get_board_display()}\n{status_text}",
            reply_markup=keyboard.as_markup() if not winner else None
        )
    
    await callback.answer()

# Казино (сокращенный код для примера)
@dp.message(F.text == "🎰 Казино")
async def casino_game(message: types.Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Сначала напишите /start")
        return
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Крутить (10 монет)", callback_data="casino_spin")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_games")]
    ])
    
    await message.answer(
        "🎰 **КАЗИНО**\n\nСтавка: 10 монет\nВыигрыши:\n• 3 одинаковых = x5\n• 2 одинаковых = x2\n\n"
        f"💎 Баланс: {user['balance']} монет",
        reply_markup=keyboard
    )

# Остальные игры (кости, камень-ножницы, угадай число) остаются без изменений
# ...

# Ежедневный бонус
@dp.message(F.text == "🎁 Бонус")
async def daily_bonus(message: types.Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Сначала напишите /start")
        return
        
    today = datetime.datetime.now().date().isoformat()
    
    if user['last_bonus_date'] == today:
        await message.answer("❌ Вы уже получали бонус сегодня! Возвращайся завтра.")
        return
    
    bonus = random.randint(15, 50)
    new_balance = update_balance(message.from_user.id, bonus)
    
    users_data[str(message.from_user.id)]['last_bonus_date'] = today
    save_data()
    
    await message.answer(
        f"🎁 **ЕЖЕДНЕВНЫЙ БОНУС**\n\n💰 +{bonus} монет!\n💎 Баланс: {new_balance} монет\n\n🔄 Возвращайся завтра!"
    )

# Топ игроков
@dp.message(F.text == "🏆 Топ игроков")
async def top_players(message: types.Message):
    sorted_users = sorted(users_data.values(), key=lambda x: x['balance'], reverse=True)[:10]
    
    top_text = "🏆 **ТОП ИГРОКОВ**\n\n"
    for i, user in enumerate(sorted_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        stats = get_user_stats(user['user_id'])
        win_rate = (stats['games_won'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
        top_text += f"{medal} {user['first_name']} - {user['balance']} монет\n"
    
    await message.answer(top_text)

# Помощь
@dp.message(F.text == "❓ Помощь")
async def help_command(message: types.Message):
    help_text = """
❓ **ПОМОЩЬ ПО БОТУ**

🎮 **Игры:**
• Крестики-нолики, Казино, Кости
• Камень-ножницы, Угадай число
• Случайная игра

💰 **Экономика:**
• Баланс: 100 монет
• Бонусы: 15-50 монет
• Заработок в играх

📞 **Поддержка:**
• Онлайн-чат с админом
• Быстрые ответы
• Кнопка завершения

⚡ **Хостинг: Replit.com**
🔄 **24/7 работа**
    """
    await message.answer(help_text)

# Настройки
@dp.message(F.text == "⚙️ Настройки")
async def settings(message: types.Message):
    await message.answer(
        "⚙️ **НАСТРОЙКИ**\n\n"
        "🔔 Уведомления: Вкл\n"
        "🌐 Язык: Русский\n"
        "💾 Данные: JSON файл\n"
        "📞 Поддержка: Активна\n"
        "⚡ Хостинг: Replit.com"
    )

# Обработчики назад для игр
@dp.callback_query(F.data == "back_games")
async def back_to_games(callback: types.CallbackQuery):
    await callback.message.edit_text("🔙 Возвращаемся в игры")
    await games_center(callback.message)

# Запуск бота
async def main():
    logger.info("🚀 Запуск бота с системой поддержки...")
    try:
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот @{bot_info.username} запущен!")
        logger.info(f"👑 Администратор: {ADMIN_ID}")
        
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 TELEGRAM BOT С СИСТЕМОЙ ПОДДЕРЖКИ")
    print("=" * 60)
    print("🎮 6 игр с экономикой")
    print("📞 Онлайн-поддержка")
    print("💰 Баланс и бонусы")
    print("👑 Админ панель")
    print("🚀 Запуск...")
    print("=" * 60)
    
    asyncio.run(main())