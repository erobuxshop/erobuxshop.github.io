import telebot
import random
import time
import logging
from telebot import types

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "7634013623:AAGjUEY5wT3ouSwV22Zn3e4iWEe4JWiOUeU"
bot = telebot.TeleBot(TOKEN)

# Остальной код без изменений...

# База данных
games = {}
user_stats = {}
waiting_players = {}
active_matches = {}

# Словари для игр
hangman_words = ["питон", "телеграм", "бот", "программирование", "игра", "чат", "группа", "мультиплеер"]
trivia_questions = []

# Загрузка вопросов для викторины
def load_trivia_questions():
    global trivia_questions
    questions = [
        {"question": "Столица Франции?", "answer": "париж", "options": ["Лондон", "Берлин", "Париж", "Рим"]},
        {"question": "Сколько планет в Солнечной системе?", "answer": "8", "options": ["8", "9", "7", "10"]},
        {"question": "2 + 2 × 2 = ?", "answer": "6", "options": ["6", "8", "4", "10"]}
    ]
    trivia_questions = questions

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🎯 Угадай число", "✊ КНБ", "🎲 Кости", 
        "🎮 Викторина", "💣 Сапёр", "🃏 Блэкджек",
        "🧩 Виселица", "⚔️ КНБ с игроком", "🎯 Дартс",
        "🏆 Статистика", "❌ Выход"
    ]
    markup.add(*buttons)
    return markup

# Меню для КНБ с игроком
def rps_multiplayer_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = ["✊", "✌️", "✋", "❌ Отмена"]
    markup.add(*buttons)
    return markup

# Меню для дартса
def darts_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = ["🎯 Бросить дротик", "🏆 Результаты", "❌ Выход"]
    markup.add(*buttons)
    return markup

# Инициализация пользователя
def init_user(user_id, username):
    if user_id not in user_stats:
        user_stats[user_id] = {
            'username': username,
            'games_played': 0,
            'wins': 0,
            'rps_wins': 0,
            'rps_multi_wins': 0,
            'darts_score': 0,
            'darts_games': 0
        }

# Команды бота
@bot.message_handler(commands=['start', 'help', 'games'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    init_user(user_id, username)
    
    welcome_text = (
        "🎮 *Добро пожаловать в multiplayer игровой бот!*\n\n"
        "🌟 *Одиночные игры:*\n"
        "• 🎯 Угадай число (1-100)\n"
        "• ✊ Камень-Ножницы-Бумага vs Бот\n"
        "• 🎲 Бросок костей\n"
        "• 🎮 Викторина\n"
        "• 💣 Сапёр\n"
        "• 🃏 Блэкджек\n"
        "• 🧩 Виселица\n\n"
        "🎭 *Multiplayer игры:*\n"
        "• ⚔️ КНБ с другим игроком\n"
        "• 🎯 Дартс (соревнование)\n\n"
        "Используйте кнопки меню для выбора игры!"
    )
    
    bot.send_message(chat_id, welcome_text, parse_mode='Markdown', reply_markup=main_menu())

# Угадай число
@bot.message_handler(func=lambda message: message.text == "🎯 Угадай число")
def guess_game_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    number = random.randint(1, 100)
    games[chat_id] = {
        'type': 'guess',
        'number': number,
        'attempts': 0,
        'max_attempts': 8,
        'player_id': user_id
    }
    
    bot.send_message(chat_id, 
        f"🎯 *Угадай число от 1 до 100!*\n"
        f"У тебя {games[chat_id]['max_attempts']} попыток!\n"
        "Просто напиши число в чат!",
        parse_mode='Markdown'
    )

# КНБ с ботом
@bot.message_handler(func=lambda message: message.text == "✊ КНБ")
def rps_vs_bot(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton("✊", callback_data="rps_bot_rock"),
        types.InlineKeyboardButton("✌️", callback_data="rps_bot_scissors"),
        types.InlineKeyboardButton("✋", callback_data="rps_bot_paper")
    ]
    markup.add(*buttons)
    
    bot.send_message(chat_id, "Выбери свой ход против бота:", reply_markup=markup)

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
        'question': question
    }
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(opt) for opt in question['options']]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("❌ Отмена"))
    
    bot.send_message(chat_id, f"🎮 *Викторина!*\n\n{question['question']}", parse_mode='Markdown', reply_markup=markup)

# КНБ с другим игроком
@bot.message_handler(func=lambda message: message.text == "⚔️ КНБ с игроком")
def rps_multiplayer_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    if chat_id in waiting_players:
        # Найден второй игрок
        player1_id = waiting_players[chat_id]['player_id']
        player1_name = waiting_players[chat_id]['player_name']
        
        # Создаем матч
        active_matches[chat_id] = {
            'player1': {'id': player1_id, 'name': player1_name, 'choice': None},
            'player2': {'id': user_id, 'name': username, 'choice': None},
            'status': 'waiting_choices'
        }
        
        del waiting_players[chat_id]
        
        # Отправляем сообщения обоим игрокам
        bot.send_message(chat_id, 
            f"🎮 *Матч начался!*\n"
            f"⚔️ {player1_name} vs {username}\n\n"
            f"Выберите свой ход!",
            parse_mode='Markdown', reply_markup=rps_multiplayer_menu()
        )
        
    else:
        # Первый игрок ждет соперника
        waiting_players[chat_id] = {
            'player_id': user_id,
            'player_name': username,
            'timestamp': time.time()
        }
        
        bot.send_message(chat_id, 
            f"⏳ {username} ждет соперника для игры в КНБ...\n"
            f"Другой игрок должен нажать '⚔️ КНБ с игроком'",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Дартс
@bot.message_handler(func=lambda message: message.text == "🎯 Дартс")
def darts_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    games[chat_id] = {
        'type': 'darts',
        'players': {},
        'current_player': user_id,
        'round': 1,
        'max_rounds': 3
    }
    
    # Добавляем первого игрока
    games[chat_id]['players'][user_id] = {
        'name': message.from_user.first_name,
        'score': 0,
        'throws': []
    }
    
    bot.send_message(chat_id,
        f"🎯 *Началась игра в Дартс!*\n"
        f"Игрок: {message.from_user.first_name}\n"
        f"Раундов: {games[chat_id]['max_rounds']}\n\n"
        f"Другие игроки могут присоединиться, написав '➕ Присоединиться'",
        parse_mode='Markdown', reply_markup=darts_menu()
    )

# Обработка присоединения к дартсу
@bot.message_handler(func=lambda message: message.text == "➕ Присоединиться" and message.chat.id in games and games[message.chat.id]['type'] == 'darts')
def join_darts(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    if user_id not in games[chat_id]['players']:
        games[chat_id]['players'][user_id] = {
            'name': username,
            'score': 0,
            'throws': []
        }
        
        players_list = "\n".join([f"• {player['name']}" for player in games[chat_id]['players'].values()])
        
        bot.send_message(chat_id,
            f"🎯 {username} присоединился к игре в Дартс!\n\n"
            f"Текущие игроки:\n{players_list}",
            reply_markup=darts_menu()
        )

# Бросок дротика
@bot.message_handler(func=lambda message: message.text == "🎯 Бросить дротик" and message.chat.id in games and games[message.chat.id]['type'] == 'darts')
def throw_dart(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    game_data = games[chat_id]
    
    if game_data['current_player'] != user_id:
        bot.send_message(chat_id, "Сейчас не твой ход!")
        return
    
    # Бросок дротика (от 0 до 60 очков)
    throw_score = random.randint(0, 60)
    game_data['players'][user_id]['score'] += throw_score
    game_data['players'][user_id]['throws'].append(throw_score)
    
    # Определяем следующий игрока
    player_ids = list(game_data['players'].keys())
    current_index = player_ids.index(user_id)
    next_index = (current_index + 1) % len(player_ids)
    game_data['current_player'] = player_ids[next_index]
    
    # Если все игроки сделали броски в этом раунде
    if game_data['current_player'] == player_ids[0]:
        game_data['round'] += 1
        
        if game_data['round'] > game_data['max_rounds']:
            # Игра окончена
            show_darts_results(chat_id)
            return
    
    # Показываем результат броска
    next_player_name = game_data['players'][game_data['current_player']]['name']
    bot.send_message(chat_id,
        f"🎯 {message.from_user.first_name} бросает дротик!\n"
        f"Результат: {throw_score} очков\n"
        f"Общий счёт: {game_data['players'][user_id]['score']}\n\n"
        f"Следующий игрок: {next_player_name}",
        reply_markup=darts_menu()
    )

# Показать результаты дартса
@bot.message_handler(func=lambda message: message.text == "🏆 Результаты" and message.chat.id in games and games[message.chat.id]['type'] == 'darts')
def show_darts_results(chat_id=None):
    if not chat_id:
        return
    
    game_data = games[chat_id]
    results_text = "🏆 *Результаты Дартса:*\n\n"
    
    # Сортируем игроков по очкам
    sorted_players = sorted(game_data['players'].items(), key=lambda x: x[1]['score'], reverse=True)
    
    for i, (player_id, player_data) in enumerate(sorted_players):
        results_text += f"{i+1}. {player_data['name']}: {player_data['score']} очков\n"
        results_text += f"   Броски: {', '.join(map(str, player_data['throws']))}\n\n"
    
    # Определяем победителя
    if len(sorted_players) > 0:
        winner_id, winner_data = sorted_players[0]
        user_stats[winner_id]['wins'] += 1
        user_stats[winner_id]['darts_score'] += winner_data['score']
        user_stats[winner_id]['darts_games'] += 1
    
    bot.send_message(chat_id, results_text, parse_mode='Markdown')
    
    # Завершаем игру
    del games[chat_id]

# Статистика
@bot.message_handler(func=lambda message: message.text == "🏆 Статистика")
def show_stats(message):
    user_id = message.from_user.id
    stats = user_stats.get(user_id, {})
    
    text = "📊 *Твоя статистика:*\n\n"
    text += f"🎮 Всего игр: {stats.get('games_played', 0)}\n"
    text += f"🏆 Побед: {stats.get('wins', 0)}\n"
    text += f"✊ КНБ vs Бот: {stats.get('rps_wins', 0)}\n"
    text += f"⚔️ КНБ vs Игрок: {stats.get('rps_multi_wins', 0)}\n"
    text += f"🎯 Дартс: {stats.get('darts_score', 0)} очков ({stats.get('darts_games', 0)} игр)"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# Выход
@bot.message_handler(func=lambda message: message.text == "❌ Выход")
def exit_game(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Очищаем все игры пользователя
    if chat_id in games:
        del games[chat_id]
    if chat_id in waiting_players:
        del waiting_players[chat_id]
    if chat_id in active_matches:
        del active_matches[chat_id]
    
    bot.send_message(chat_id, "🎮 Игра завершена!", reply_markup=main_menu())

# Обработка callback-ов
@bot.callback_query_handler(func=lambda call: call.data.startswith('rps_'))
def handle_rps(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    if call.data.startswith('rps_bot_'):
        # КНБ с ботом
        user_choice = call.data.split('_')[2]
        choices = {'rock': '✊', 'scissors': '✌️', 'paper': '✋'}
        bot_choice = random.choice(list(choices.keys()))
        
        if user_choice == bot_choice:
            result = "🤝 Ничья!"
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'scissors' and bot_choice == 'paper') or \
             (user_choice == 'paper' and bot_choice == 'rock'):
            result = "🎉 Ты выиграл!"
            user_stats[user_id]['wins'] += 1
            user_stats[user_id]['rps_wins'] += 1
        else:
            result = "🤖 Бот выиграл!"
        
        user_stats[user_id]['games_played'] += 1
        
        bot.edit_message_text(
            f"✊ *Камень-Ножницы-Бумага*\n\n"
            f"Твой выбор: {choices[user_choice]}\n"
            f"Выбор бота: {choices[bot_choice]}\n\n"
            f"{result}",
            chat_id, call.message.message_id, parse_mode='Markdown'
        )
    
    elif call.data.startswith('rps_multi_'):
        # КНБ с игроком (обработка через текстовые сообщения)
        pass

# Обработка текстовых сообщений для multiplayer игр
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Обработка выбора в КНБ с игроком
    if chat_id in active_matches and active_matches[chat_id]['status'] == 'waiting_choices':
        match_data = active_matches[chat_id]
        
        # Определяем, какой это игрок
        player_key = None
        if user_id == match_data['player1']['id']:
            player_key = 'player1'
        elif user_id == match_data['player2']['id']:
            player_key = 'player2'
        
        if player_key and text in ["✊", "✌️", "✋"]:
            match_data[player_key]['choice'] = text
            
            # Проверяем, сделали ли выбор оба игрока
            if match_data['player1']['choice'] and match_data['player2']['choice']:
                # Определяем победителя
                determine_rps_winner(chat_id, match_data)
            else:
                bot.send_message(chat_id, f"✅ {message.from_user.first_name} сделал выбор! Ждем второго игрока...")
    
    # Обработка других игр
    elif chat_id in games:
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

# Определение победителя в КНБ
def determine_rps_winner(chat_id, match_data):
    choice_map = {"✊": "камень", "✌️": "ножницы", "✋": "бумага"}
    p1_choice = match_data['player1']['choice']
    p2_choice = match_data['player2']['choice']
    
    if p1_choice == p2_choice:
        result_text = "🤝 Ничья!"
        winner = None
    elif (p1_choice == "✊" and p2_choice == "✌️") or \
         (p1_choice == "✌️" and p2_choice == "✋") or \
         (p1_choice == "✋" and p2_choice == "✊"):
        result_text = f"🎉 {match_data['player1']['name']} выиграл!"
        winner = match_data['player1']['id']
    else:
        result_text = f"🎉 {match_data['player2']['name']} выиграл!"
        winner = match_data['player2']['id']
    
    # Обновляем статистику
    if winner:
        user_stats[winner]['wins'] += 1
        user_stats[winner]['rps_multi_wins'] += 1
        user_stats[winner]['games_played'] += 1
    
    # Отправляем результат
    bot.send_message(chat_id,
        f"⚔️ *Результат матча КНБ:*\n\n"
        f"{match_data['player1']['name']}: {p1_choice} ({choice_map[p1_choice]})\n"
        f"{match_data['player2']['name']}: {p2_choice} ({choice_map[p2_choice]})\n\n"
        f"{result_text}",
        parse_mode='Markdown', reply_markup=main_menu()
    )
    
    # Удаляем матч
    del active_matches[chat_id]

# Запуск бота
# Запуск бота с обработкой ошибок
if __name__ == "__main__":
    logger.info("🎮 Multiplayer игровой бот запущен...")
    load_trivia_questions()
    
    try:
        bot.polling(none_stop=True, interval=2, timeout=30)
    except Exception as e:
        logger.error(f"❌ Ошибка в работе бота: {e}")
        logger.info("🔄 Попытка перезапуска через 10 секунд...")
        time.sleep(10)
