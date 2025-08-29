#!/bin/bash

cd ~

echo "🚀 Запускаем multiplayer_game1_bot.py..."
echo "📅 Дата запуска: $(date)"

# Проверим существует ли файл
if [ ! -f "multiplayer_game1_bot.py" ]; then
    echo "❌ Файл multiplayer_game1_bot.py не найден!"
    echo "📋 Создайте файл с правильным именем"
    exit 1
fi

# Бесконечный цикл для перезапуска при падении
while true; do
    echo "🔄 Запуск бота: $(date)"
    python multiplayer_game1_bot.py
    
    echo "💥 Бот остановился, перезапуск через 5 секунд..."
    sleep 5
done
