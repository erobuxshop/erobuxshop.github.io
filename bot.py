import asyncio
import os
from telethon import TelegramClient, events
from telethon.tl.types import Message

# Настройки
API_ID = 28171360
API_HASH = 'dd21bb5576fd1f889eb5ee5798bf49d7'
PHONE_NUMBER = '+17473403097'

# Фреймы анимации
ANIMATION_FRAMES = [
    "8✊🏻====D🤔",
    "8=✊🏻===D🤔",
    "8==✊🏻==D🤔", 
    "8===✊🏻=D🤔",
    "8====✊🏻D🤔",
    "8===✊🏻=D🤔",
    "8==✊🏻==D🤔",
    "8=✊🏻===D🤔",
    "8✊🏻====D🤔",
    "8=✊🏻===D🤔",
    "8==✊🏻==D🤔",
    "8===✊🏻=D🤔",
    "8====✊🏻D💦😩",
    "8===✊🏻=D🤔",
    "8====✊🏻D💦😩",
    "8===✊🏻=D🤔",
    "8====✊🏻D💦😩"
]

class EmojiAnimationUserBot:
    def __init__(self):
        self.client = TelegramClient('emoji_animation_session', API_ID, API_HASH)
        self.animation_active = False
        self.setup_handlers()

    def setup_handlers(self):
        @self.client.on(events.NewMessage(pattern=r'\.animate(?:\s+(\d+))?', outgoing=True))
        async def animate_handler(event):
            """Обработчик команды .animate [количество_повторов]"""
            if self.animation_active:
                await event.edit("⏹️ Анимация уже запущена!")
                return
            
            try:
                # Получаем количество повторов из аргумента
                repeats = 10
                if event.pattern_match.group(1):
                    repeats = int(event.pattern_match.group(1))
                    repeats = min(repeats, 50)
                
                self.animation_active = True
                message = event.message
                
                # БЫСТРАЯ АНИМАЦИЯ - 0.1 секунды на кадр
                for cycle in range(repeats):
                    if not self.animation_active:
                        break
                    
                    for frame in ANIMATION_FRAMES:
                        if not self.animation_active:
                            break
                        await message.edit(frame)
                        await asyncio.sleep(0.1)  # ⚡ БЫСТРО (0.1 секунды)
                
                if self.animation_active:
                    await message.edit("✅ Анимация завершена!")
                else:
                    await message.edit("⏹️ Анимация остановлена")
                    
                self.animation_active = False
                
            except Exception as e:
                await event.edit(f"❌ Ошибка: {str(e)}")
                self.animation_active = False

        @self.client.on(events.NewMessage(pattern=r'\.fast', outgoing=True))
        async def fast_animate_handler(event):
            """Сверхбыстрая анимация"""
            if self.animation_active:
                await event.edit("⏹️ Анимация уже запущена!")
                return
            
            try:
                self.animation_active = True
                message = event.message
                
                # СВЕРХБЫСТРАЯ АНИМАЦИЯ - 0.05 секунды на кадр
                for cycle in range(15):
                    if not self.animation_active:
                        break
                    
                    for frame in ANIMATION_FRAMES:
                        if not self.animation_active:
                            break
                        await message.edit(frame)
                        await asyncio.sleep(0.05)  # ⚡⚡ ОЧЕНЬ БЫСТРО (0.05 секунды)
                
                if self.animation_active:
                    await message.edit("✅ Сверхбыстрая анимация завершена!")
                self.animation_active = False
                
            except Exception as e:
                await event.edit(f"❌ Ошибка: {str(e)}")
                self.animation_active = False

        @self.client.on(events.NewMessage(pattern=r'\.slow', outgoing=True))
        async def slow_animate_handler(event):
            """Медленная анимация"""
            if self.animation_active:
                await event.edit("⏹️ Анимация уже запущена!")
                return
            
            try:
                self.animation_active = True
                message = event.message
                
                # МЕДЛЕННАЯ АНИМАЦИЯ - 0.5 секунды на кадр
                for cycle in range(5):
                    if not self.animation_active:
                        break
                    
                    for frame in ANIMATION_FRAMES:
                        if not self.animation_active:
                            break
                        await message.edit(frame)
                        await asyncio.sleep(0.5)  # 🐢 МЕДЛЕННО (0.5 секунды)
                
                if self.animation_active:
                    await message.edit("✅ Медленная анимация завершена!")
                self.animation_active = False
                
            except Exception as e:
                await event.edit(f"❌ Ошибка: {str(e)}")
                self.animation_active = False

        @self.client.on(events.NewMessage(pattern=r'\.stop', outgoing=True))
        async def stop_handler(event):
            """Остановка анимации"""
            if self.animation_active:
                self.animation_active = False
                await event.edit("⏹️ Анимация остановлена")
            else:
                await event.edit("❌ Анимация не запущена!")

        @self.client.on(events.NewMessage(pattern=r'\.help', outgoing=True))
        async def help_handler(event):
            """Справка"""
            help_text = """
🤖 **UserBot с анимацией эмодзи**

**Команды:**
`.animate [число]` - Быстрая анимация (0.1s)
`.fast` - Сверхбыстрая анимация (0.05s)  
`.slow` - Медленная анимация (0.5s)
`.stop` - Остановить анимацию
`.help` - Показать справку

**Скорости:**
⚡ `.fast` - очень быстро (0.05 сек/кадр)
🚀 `.animate` - быстро (0.1 сек/кадр)
🐢 `.slow` - медленно (0.5 сек/кадр)
            """
            await event.edit(help_text)

    async def start(self):
        """Запуск userbot"""
        print("🚀 Запуск UserBot с анимацией эмодзи...")
        
        try:
            await self.client.start(phone=PHONE_NUMBER)
            print("✅ UserBot успешно запущен!")
            print("📋 Доступные команды:")
            print(".animate - Быстрая анимация (0.1s)")
            print(".fast    - Сверхбыстрая анимация (0.05s)")
            print(".slow    - Медленная анимация (0.5s)")
            print(".stop    - Остановить анимацию")
            print(".help    - Показать справку")
            
            await self.client.run_until_disconnected()
            
        except Exception as e:
            print(f"❌ Ошибка при запуске: {e}")

if __name__ == "__main__":
    # Проверяем установлены ли зависимости
    try:
        import telethon
    except ImportError:
        print("❌ Telethon не установлен!")
        os.system('pip install telethon')
    
    # Запускаем бота
    bot = EmojiAnimationUserBot()
    asyncio.run(bot.start())
