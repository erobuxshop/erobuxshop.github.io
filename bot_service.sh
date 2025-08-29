#!/bin/bash

echo "📦 Запускаем бота в tmux сессии..."
tmux new-session -d -s game_bot "bash ~/start_bot.sh"
echo "✅ Бот запущен в фоне!"
echo "📋 Команды для управления:"
echo "   tmux attach -t game_bot  # Подключиться к сессии"
echo "   tmux kill-session -t game_bot  # Остановить бота"
echo "   tail -f bot.log  # Посмотреть логи"
