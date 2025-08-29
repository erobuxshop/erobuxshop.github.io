# Автозапуск бота при входе в Termux
if [ ! -f ~/.bot_disabled ] && [ -z "$TMUX" ]; then
    echo "🔍 Проверяем запущен ли бот..."
    if ! pgrep -f "python muptiplayer_bot.py" > /dev/null; then
        echo "🚀 Запускаем игрового бота..."
        tmux new-session -d -s game_bot "bash ~/start_bot.sh"
    else
        echo "✅ Бот уже запущен"
    fi
fi

# Алиасы для удобства
alias bot-start="bash ~/bot_service.sh"
alias bot-stop="pkill -f 'python multiplayer_game_bot.py' && tmux kill-session -t game_bot"
alias bot-status="bash ~/bot_control.sh"
alias bot-logs="tail -f bot.log"
alias bot-restart="bot-stop && sleep 2 && bot-start"
