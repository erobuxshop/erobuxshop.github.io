import telebot
import random
import time
import json
import requests
from telebot import types
from bs4 import BeautifulSoup

# Конфигурация
TOKEN = "7634013623:AAGjUEY5wT3ouSwV22Zn3e4iWEe4JWiOUeU"
bot = telebot.TeleBot(TOKEN)

# База данных (в памяти)
games = {}
user_stats = {}
hangman_words = ["питон", "телеграм", "бот", "программирование", "игра", "термукс", "разработка"]
trivia_questions = []
blackjack_deck = []

# Инициализация колоды для блэкджека
def init_blackjack_deck():
    global blackjack_deck
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♥', '♦', '♣', '♠']
    blackjack_deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
    random.shuffle(blackjack_deck)

# Загрузка вопросов для викторины
def load_trivia_questions():
    global trivia_questions
    questions = [
        {"question": "Столица Франции?", "answer": "париж", "options": ["Лондон", "Берлин", "Париж", "Рим"]},
        {"question": "Сколько планет в Солнечной системе?", "answer": "8", "options": ["8", "9", "7", "10"]},
        {"question": "Самое большое млекопитающее?", "answer": "синий кит", "options": ["Слон", "Синий кит", "Жираф", "Бегемот"]},
        {"question": "2 + 2 × 2 = ?", "answer": "6", "options": ["6", "8", "4", "10"]},
        {"question": "Столица Японии?", "answer": "токио", "options": ["Пекин", "Сеул", "Токио", "Бангкок"]}
    ]
    trivia_questions = questions

# Клавиатура главного меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🎯 Угадай число", "✊ КНБ", "🎲 Кости", 
        "🎮 Викторина", "💣 Сапёр", "🃏 Блэкджек",
        "🧩 Виселица", "📊 Статистика", "❌ Выход"
    ]
    markup.add(*buttons)
    return markup

# Обработчик команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {
            'games_played': 0,
            'wins': 0,
            'guess_wins': 0,
            'rps_wins': 0,
            'dice_wins': 0,
            'trivia_score': 0,
            'blackjack_wins': 0,
            'hangman_wins': 0
        }
    
    bot.send_message(message.chat.id,
        "🎮 *Добро пожаловать в игровой бот!*\n\n"
        "Доступные игры:\n"
        "• 🎯 Угадай число (1-100)\n"
        "• ✊ Камень-Ножницы-Бумага\n"
        "• 🎲 Бросок костей\n"
        "• 🎮 Викторина с вариантами\n"
        "• 💣 Игра Сапёр\n"
        "• 🃏 Блэкджек (21 очко)\n"
        "• 🧩 Виселица (угадай слово)\n\n"
        "Используйте кнопки меню для выбора игры!",
        parse_mode='Markdown', reply_markup=main_menu()
    )

# Угадай число
@bot.message_handler(func=lambda message: message.text == "🎯 Угадай число")
def guess_game_start(message):
    chat_id = message.chat.id
    number = random.randint(1, 100)
    games[chat_id] = {
        'type': 'guess',
        'number': number,
        'attempts': 0,
        'max_attempts': 10
    }
    
    bot.send_message(chat_id, 
        "🎯 *Угадай число от 1 до 100!*\n"
        f"У тебя {games[chat_id]['max_attempts']} попыток!\n"
        "Просто напиши число!",
        parse_mode='Markdown'
    )

# Камень-ножницы-бумага
@bot.message_handler(func=lambda message: message.text == "✊ КНБ")
def rps_game(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton("✊", callback_data="rps_rock"),
        types.InlineKeyboardButton("✌️", callback_data="rps_scissors"),
        types.InlineKeyboardButton("✋", callback_data="rps_paper")
    ]
    markup.add(*buttons)
    
    bot.send_message(chat_id, "Выбери свой ход:", reply_markup=markup)

# Бросок костей
@bot.message_handler(func=lambda message: message.text == "🎲 Кости")
def dice_game(message):
    chat_id = message.chat.id
    user_dice = random.randint(1, 6)
    bot_dice = random.randint(1, 6)
    
    result = "🎉 Ты выиграл!" if user_dice > bot_dice else "🤖 Бот выиграл!" if bot_dice > user_dice else "🤝 Ничья!"
    
    bot.send_message(chat_id,
        f"🎲 *Бросок костей!*\n\n"
        f"Твоя кость: {user_dice}\n"
        f"Кость бота: {bot_dice}\n\n"
        f"{result}",
        parse_mode='Markdown'
    )
    
    user_stats[message.from_user.id]['games_played'] += 1
    if user_dice > bot_dice:
        user_stats[message.from_user.id]['wins'] += 1
        user_stats[message.from_user.id]['dice_wins'] += 1

# Викторина
@bot.message_handler(func=lambda message: message.text == "🎮 Викторина")
def trivia_start(message):
    chat_id = message.chat.id
    load_trivia_questions()
    
    if not trivia_questions:
        bot.send_message(chat_id, "❌ Вопросы временно недоступны!")
        return
    
    question = random.choice(trivia_questions)
    games[chat_id] = {
        'type': 'trivia',
        'question': question,
        'start_time': time.time()
    }
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(opt) for opt in question['options']]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("❌ Отмена"))
    
    bot.send_message(chat_id,
        f"🎮 *Викторина!*\n\n{question['question']}",
        parse_mode='Markdown', reply_markup=markup
    )

# Сапёр
@bot.message_handler(func=lambda message: message.text == "💣 Сапёр")
def minesweeper_start(message):
    chat_id = message.chat.id
    size = 5
    mines = 5
    
    # Создаём поле
    field = [['⬜' for _ in range(size)] for _ in range(size)]
    mine_positions = set()
    
    while len(mine_positions) < mines:
        mine_positions.add((random.randint(0, size-1), random.randint(0, size-1)))
    
    games[chat_id] = {
        'type': 'minesweeper',
        'field': field,
        'mines': mine_positions,
        'revealed': set(),
        'game_over': False
    }
    
    display_field(chat_id)

def display_field(chat_id):
    game_data = games[chat_id]
    field_text = "💣 *Сапёр* - Выбери клетку:\n\n"
    
    for i in range(len(game_data['field'])):
        for j in range(len(game_data['field'][i])):
            if (i, j) in game_data['revealed']:
                if (i, j) in game_data['mines']:
                    field_text += "💣 "
                else:
                    mines_nearby = count_nearby_mines(i, j, game_data['mines'])
                    field_text += f"{mines_nearby}️⃣ " if mines_nearby > 0 else "🟩 "
            else:
                field_text += "⬜ "
        field_text += "\n"
    
    # Создаём клавиатуру для выбора клеток
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    buttons = []
    for i in range(5):
        for j in range(5):
            buttons.append(types.KeyboardButton(f"{i+1}-{j+1}"))
    markup.add(*buttons)
    markup.add(types.KeyboardButton("❌ Сдаться"))
    
    bot.send_message(chat_id, field_text, parse_mode='Markdown', reply_markup=markup)

def count_nearby_mines(x, y, mines):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (x + dx, y + dy) in mines:
                count += 1
    return count

# Блэкджек
@bot.message_handler(func=lambda message: message.text == "🃏 Блэкджек")
def blackjack_start(message):
    chat_id = message.chat.id
    init_blackjack_deck()
    
    player_hand = [blackjack_deck.pop(), blackjack_deck.pop()]
    dealer_hand = [blackjack_deck.pop(), blackjack_deck.pop()]
    
    games[chat_id] = {
        'type': 'blackjack',
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'deck': blackjack_deck.copy(),
        'state': 'player_turn'
    }
    
    display_blackjack(chat_id)

def display_blackjack(chat_id):
    game_data = games[chat_id]
    player_score = calculate_hand_value(game_data['player_hand'])
    
    text = "🃏 *Блэкджек* - 21 очко!\n\n"
    text += f"Твоя рука: {', '.join(game_data['player_hand'])} (очков: {player_score})\n"
    text += f"Дилер: {game_data['dealer_hand'][0]}, ?\n\n"
    
    if game_data['state'] == 'player_turn':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("➕ Ещё", "✋ Хватит", "❌ Выход")
        text += "Выбери действие:"
    else:
        markup = main_menu()
    
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)

def calculate_hand_value(hand):
    value = 0
    aces = 0
    
    for card in hand:
        rank = card[:-1]
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            aces += 1
            value += 11
        else:
            value += int(rank)
    
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    
    return value

# Виселица
@bot.message_handler(func=lambda message: message.text == "🧩 Виселица")
def hangman_start(message):
    chat_id = message.chat.id
    word = random.choice(hangman_words)
    hidden_word = ['_' for _ in word]
    
    games[chat_id] = {
        'type': 'hangman',
        'word': word,
        'hidden_word': hidden_word,
        'attempts': 6,
        'used_letters': set(),
        'game_over': False
    }
    
    display_hangman(chat_id)

def display_hangman(chat_id):
    game_data = games[chat_id]
    hangman_states = [
        """
        
        
        
        
        
        """,
        """
        
          
          
          
        👇
        """,
        """
        ☹️  
          
          
          
        👇
        """,
        """
        ☹️  
        |  
        |  
        |  
        👇
        """,
        """
        ☹️  
        |\\ 
        |  
        |  
        👇
        """,
        """
        ☹️  
        |\\ 
        |  
        |/ 
        👇
        """,
        """
        ☹️  
        |\\ 
        |  
        |/ \\
        👇
        """
    ]
    
    text = f"🧩 *Виселица* - Попыток: {game_data['attempts']}\n\n"
    text += hangman_states[6 - game_data['attempts']] + "\n"
    text += f"Слово: {' '.join(game_data['hidden_word'])}\n"
    text += f"Использованные буквы: {', '.join(sorted(game_data['used_letters']))}\n\n"
    text += "Введите букву:"
    
    bot.send_message(chat_id, text, parse_mode='Markdown')

# Статистика
@bot.message_handler(func=lambda message: message.text == "📊 Статистика")
def show_stats(message):
    user_id = message.from_user.id
    stats = user_stats.get(user_id, {})
    
    text = "📊 *Твоя статистика:*\n\n"
    text += f"🎮 Всего игр: {stats.get('games_played', 0)}\n"
    text += f"🏆 Побед: {stats.get('wins', 0)}\n"
    text += f"🎯 Угадай число: {stats.get('guess_wins', 0)}\n"
    text += f"✊ КНБ: {stats.get('rps_wins', 0)}\n"
    text += f"🎲 Кости: {stats.get('dice_wins', 0)}\n"
    text += f"🎮 Викторина: {stats.get('trivia_score', 0)}\n"
    text += f"🃏 Блэкджек: {stats.get('blackjack_wins', 0)}\n"
    text += f"🧩 Виселица: {stats.get('hangman_wins', 0)}"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# Выход
@bot.message_handler(func=lambda message: message.text == "❌ Выход")
def exit_game(message):
    chat_id = message.chat.id
    if chat_id in games:
        del games[chat_id]
    bot.send_message(chat_id, "🎮 Игра завершена!", reply_markup=main_menu())

# Обработка callback-ов (для КНБ)
@bot.callback_query_handler(func=lambda call: call.data.startswith('rps_'))
def handle_rps(call):
    user_choice = call.data.split('_')[1]
    choices = {'rock': '✊', 'scissors': '✌️', 'paper': '✋'}
    bot_choice = random.choice(list(choices.keys()))
    
    if user_choice == bot_choice:
        result = "🤝 Ничья!"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'scissors' and bot_choice == 'paper') or \
         (user_choice == 'paper' and bot_choice == 'rock'):
        result = "🎉 Ты выиграл!"
        user_stats[call.from_user.id]['wins'] += 1
        user_stats[call.from_user.id]['rps_wins'] += 1
    else:
        result = "🤖 Бот выиграл!"
    
    user_stats[call.from_user.id]['games_played'] += 1
    
    bot.edit_message_text(
        f"✊ *Камень-Ножницы-Бумага*\n\n"
        f"Твой выбор: {choices[user_choice]}\n"
        f"Выбор бота: {choices[bot_choice]}\n\n"
        f"{result}",
        call.message.chat.id, call.message.message_id, parse_mode='Markdown'
    )

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip()
    
    if chat_id not in games:
        bot.send_message(chat_id, "Выбери игру из меню!", reply_markup=main_menu())
        return
    
    game_data = games[chat_id]
    
    # Угадай число
    if game_data['type'] == 'guess':
        try:
            guess = int(text)
            game_data['attempts'] += 1
            
            if guess < game_data['number']:
                bot.send_message(chat_id, "📈 Больше!")
            elif guess > game_data['number']:
                bot.send_message(chat_id, "📉 Меньше!")
            else:
                user_stats[user_id]['games_played'] += 1
                user_stats[user_id]['wins'] += 1
                user_stats[user_id]['guess_wins'] += 1
                bot.send_message(chat_id, 
                    f"🎉 Поздравляю! Ты угадал число {game_data['number']} "
                    f"за {game_data['attempts']} попыток!", 
                    reply_markup=main_menu()
                )
                del games[chat_id]
                return
            
            if game_data['attempts'] >= game_data['max_attempts']:
                bot.send_message(chat_id, 
                    f"❌ Игра окончена! Число было: {game_data['number']}", 
                    reply_markup=main_menu()
                )
                del games[chat_id]
                
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, введите число!")
    
    # Викторина
    elif game_data['type'] == 'trivia':
        if text == "❌ Отмена":
            bot.send_message(chat_id, "Викторина отменена!", reply_markup=main_menu())
            del games[chat_id]
            return
        
        correct_answer = game_data['question']['answer']
        if text.lower() == correct_answer.lower():
            user_stats[user_id]['trivia_score'] += 1
            user_stats[user_id]['games_played'] += 1
            user_stats[user_id]['wins'] += 1
            bot.send_message(chat_id, "✅ Правильно!", reply_markup=main_menu())
        else:
            bot.send_message(chat_id, 
                f"❌ Неправильно! Правильный ответ: {correct_answer}", 
                reply_markup=main_menu()
            )
            user_stats[user_id]['games_played'] += 1
        del games[chat_id]
    
    # Сапёр
    elif game_data['type'] == 'minesweeper':
        if text == "❌ Сдаться":
            bot.send_message(chat_id, "Игра завершена!", reply_markup=main_menu())
            del games[chat_id]
            return
        
        try:
            coords = text.split('-')
            x, y = int(coords[0])-1, int(coords[1])-1
            
            if (x, y) in game_data['revealed']:
                bot.send_message(chat_id, "Эта клетка уже открыта!")
                return
            
            game_data['revealed'].add((x, y))
            
            if (x, y) in game_data['mines']:
                # Показать всё поле
                for mx, my in game_data['mines']:
                    game_data['revealed'].add((mx, my))
                display_field(chat_id)
                bot.send_message(chat_id, "💥 Ты наступил на мину! Игра окончена!", reply_markup=main_menu())
                user_stats[user_id]['games_played'] += 1
                del games[chat_id]
            else:
                # Проверить победу
                if len(game_data['revealed']) == 25 - len(game_data['mines']):
                    display_field(chat_id)
                    bot.send_message(chat_id, "🎉 Ты выиграл! Все мины обезврежены!", reply_markup=main_menu())
                    user_stats[user_id]['games_played'] += 1
                    user_stats[user_id]['wins'] += 1
                    del games[chat_id]
                else:
                    display_field(chat_id)
                    
        except (ValueError, IndexError):
            bot.send_message(chat_id, "Введите координаты
