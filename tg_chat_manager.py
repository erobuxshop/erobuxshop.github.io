import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime, timedelta
import re

# Ваши данные API
API_ID = '28171360'  # Замените на ваш API ID
API_HASH = 'dd21bb5576fd1f889eb5ee5798bf49d7'  # Замените на ваш API Hash

# Инициализация клиента
client = TelegramClient('session_name', API_ID, API_HASH)

# Функция для разбора времени
def parse_time(time_str):
    time_str = time_str.lower()
    if time_str == 'навсегда':
        return None
    
    time_units = {
        'м': 60,
        'ч': 3600,
        'д': 86400,
        'н': 604800,
        'мес': 2592000,
        'г': 31536000
    }
    
    total_seconds = 0
    matches = re.findall(r'(\d+)\s*([а-яa-z]+)', time_str)
    
    for amount, unit in matches:
        if unit in time_units:
            total_seconds += int(amount) * time_units[unit]
        elif unit.startswith('м') and not unit.startswith('мес'):
            total_seconds += int(amount) * time_units['м']
        elif unit.startswith('мес'):
            total_seconds += int(amount) * time_units['мес']
    
    return timedelta(seconds=total_seconds) if total_seconds > 0 else None

# Обработчик новых сообщений
@client.on(events.NewMessage)
async def handler(event):
    # Проверяем, что сообщение от нас
    if event.is_private:
        return
    
    message = event.message.message
    sender = await event.get_sender()
    chat = await event.get_chat()
    
    # Проверяем, что у нас есть права администратора
    if not (await event.get_chat()).admin_rights:
        return
    
    # Команда бана
    if message.startswith('!ban'):
        parts = message.split(' ', 3)
        if len(parts) < 4:
            await event.reply('Формат команды: !ban @username срок причина\nПример: !ban @username 7д спам')
            return
        
        username = parts[1].replace('@', '')
        time_str = parts[2]
        reason = parts[3] if len(parts) > 3 else "Не указана"
        
        # Парсим время
        until_date = parse_time(time_str)
        
        try:
            # Ищем пользователя
            user = await client.get_entity(username)
            
            # Настраиваем права бана
            banned_rights = ChatBannedRights(
                until_date=until_date,
                view_messages=True,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                send_polls=True,
                change_info=True,
                invite_users=True,
                pin_messages=True
            )
            
            # Выполняем бан
            await client(EditBannedRequest(chat.id, user, banned_rights))
            await event.reply(f'Пользователь @{username} забанен на {time_str}. Причина: {reason}')
            
        except Exception as e:
            await event.reply(f'Ошибка: {str(e)}')
    
    # Команда мута
    elif message.startswith('!mute'):
        parts = message.split(' ', 3)
        if len(parts) < 4:
            await event.reply('Формат команды: !mute @username срок причина\nПример: !mute @username 2ч флуд')
            return
        
        username = parts[1].replace('@', '')
        time_str = parts[2]
        reason = parts[3] if len(parts) > 3 else "Не указана"
        
        # Парсим время
        until_date = parse_time(time_str)
        
        try:
            # Ищем пользователя
            user = await client.get_entity(username)
            
            # Настраиваем права мута
            banned_rights = ChatBannedRights(
                until_date=until_date,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                send_polls=True
            )
            
            # Выполняем мут
            await client(EditBannedRequest(chat.id, user, banned_rights))
            await event.reply(f'Пользователь @{username} замучен на {time_str}. Причина: {reason}')
            
        except Exception as e:
            await event.reply(f'Ошибка: {str(e)}')
    
    # Команда разбана
    elif message.startswith('!unban'):
        parts = message.split(' ', 1)
        if len(parts) < 2:
            await event.reply('Формат команды: !unban @username')
            return
        
        username = parts[1].replace('@', '')
        
        try:
            # Ищем пользователя
            user = await client.get_entity(username)
            
            # Настраиваем права (снимаем все ограничения)
            banned_rights = ChatBannedRights(
                until_date=None,
                view_messages=False,
                send_messages=False,
                send_media=False,
                send_stickers=False,
                send_gifs=False,
                send_games=False,
                send_inline=False,
                send_polls=False,
                change_info=False,
                invite_users=False,
                pin_messages=False
            )
            
            # Выполняем разбан
            await client(EditBannedRequest(chat.id, user, banned_rights))
            await event.reply(f'Пользователь @{username} разбанен.')
            
        except Exception as e:
            await event.reply(f'Ошибка: {str(e)}')
    
    # Команда удаления всех сообщений
    elif message.startswith('!purge'):
        try:
            # Удаляем все сообщения в чате
            async for msg in client.iter_messages(chat.id):
                await msg.delete()
                await asyncio.sleep(0.5)  # Чтобы не превысить лимиты API
            
            await event.reply('Все сообщения удалены.')
            
        except Exception as e:
            await event.reply(f'Ошибка: {str(e)}')
    
    # Команда помощи
    elif message.startswith('!help'):
        help_text = """
Доступные команды:
!ban @username срок причина - Забанить пользователя
!mute @username срок причина - Замутить пользователя
!unban @username - Разбанить пользователя
!purge - Удалить все сообщения в чате
!help - Показать эту справку

Примеры сроков: 30м, 2ч, 7д, 1нед, 1мес, 1г, навсегда
        """
        await event.reply(help_text)

# Запуск клиента
async def main():
    await client.start()
    print("Бот запущен! Ожидание сообщений...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
