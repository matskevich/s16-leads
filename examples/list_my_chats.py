#!/usr/bin/env python3
"""
Скрипт для вывода всех чатов пользователя
"""

import asyncio
from src.infra.tele_client import get_client

async def main():
    """Выводит список всех чатов пользователя"""
    try:
        print("🔍 Получение списка чатов...\n")
        
        # Получаем клиент
        client = get_client()
        await client.start()
        
        print("📋 Список всех чатов:\n")
        print("ID".ljust(15) + " | " + "Тип".ljust(10) + " | " + "Название")
        print("-" * 80)
        
        async for dialog in client.iter_dialogs():
            # Определяем тип чата
            if dialog.is_user:
                chat_type = "👤 Личный"
            elif dialog.is_group:
                chat_type = "👥 Группа"
            elif dialog.is_channel:
                chat_type = "📢 Канал"
            else:
                chat_type = "❓ Другой"
            
            # Выводим информацию
            chat_id = str(dialog.id)
            title = dialog.title[:50]  # Ограничиваем длину названия
            
            print(f"{chat_id.ljust(15)} | {chat_type.ljust(10)} | {title}")
        
        print(f"\n✅ Найдено {len([d async for d in client.iter_dialogs()])} чатов")
        
        await client.disconnect()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 