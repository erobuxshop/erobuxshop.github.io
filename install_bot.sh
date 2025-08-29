#!/bin/bash

echo "📦 Установка игрового бота..."

# Делаем все скрипты исполняемыми
chmod +x start_bot.sh
chmod +x bot_service.sh
chmod +x bot_control.sh
chmod +x run_bot.sh

echo "✅ Все скрипты сделаны исполняемыми"
echo "📋 Для запуска используйте:"
echo "   ./bot_control.sh  # Меню управления"
echo "   ./bot_service.sh  # Запуск в фоне"
echo "   ./run_bot.sh      # Простой запуск"
