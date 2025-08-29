#!/bin/bash

echo "🎮 Управление игровым ботом"
echo "1. 🚀 Запустить бота"
echo "2. ⏹️ Остановить бота"
echo "3. 📊 Статус бота"
echo "4. 📝 Логи бота"
echo "5. 🔄 Перезапустить бота"
echo "6. ❌ Выход"

read -p "Выберите действие (1-6): " choice

case $choice in
    1)
        echo "🚀 Запускаем бота..."
        bash ~/bot_service.sh
        ;;
    2)
        echo "⏹️ Останавливаем бота..."
        pkill -f "python multiplayer_game1_bot.py"
        tmux kill-session -t game_bot 2>/dev/null
        echo "✅ Бот остановлен"
        ;;
    3)
        echo "📊 Статус бота:"
        if pgrep -f "python multiplayer_game1_bot.py" > /dev/null; then
            echo "✅ Бот работает"
            echo "PID: $(pgrep -f 'python multiplayer_game1_bot.py')"
        else
            echo "❌ Бот не запущен"
        fi
        
        if tmux has-session -t game_bot 2>/dev/null; then
            echo "📦 Tmux сессия: активна"
        else
            echo "📦 Tmux сессия: неактивна"
        fi
        ;;
    4)
        echo "📝 Последние логи:"
        if [ -f "bot.log" ]; then
            tail -20 bot.log
        else
            echo "Файл логов не найден"
        fi
        ;;
    5)
        echo "🔄 Перезапускаем бота..."
        pkill -f "python multiplayer_game1_bot.py"
        sleep 2
        bash ~/bot_service.sh
        ;;
    6)
        echo "👋 Выход"
        exit 0
        ;;
    *)
        echo "❌ Неверный выбор"
        ;;
esac
