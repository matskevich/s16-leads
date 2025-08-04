#!/usr/bin/env python3
"""
Скрипт для вывода всех чатов пользователя
ИСПОЛЬЗУЕТ S16-leads анти-спам интерфейсы
"""

import asyncio
from src.infra.tele_client import get_client
from src.infra.limiter import safe_call, get_rate_limiter
from src.core.group_manager import GroupManager
import logging

logger = logging.getLogger(__name__)

async def get_my_chats_with_details():
    """Получает список всех чатов с детальной информацией через S16-leads интерфейсы"""
    try:
        print("🔍 Получение списка чатов через S16-leads анти-спам интерфейсы...\n")
        
        # Получаем клиент и инициализируем rate limiter
        client = get_client()
        await client.start()
        rate_limiter = get_rate_limiter()
        manager = GroupManager(client)
        
        # Получаем список диалогов через safe_call
        print("📡 Получение диалогов через safe_call...")
        dialogs_list = []
        
        # Используем safe_call для получения диалогов
        async def get_dialogs():
            dialogs = []
            async for dialog in client.iter_dialogs():
                dialogs.append(dialog)
            return dialogs
        
        dialogs = await safe_call(get_dialogs, operation_type="api")
        
        print("📋 Список всех чатов:\n")
        print("ID".ljust(15) + " | " + "Тип".ljust(10) + " | " + "Участники".ljust(10) + " | " + "Название")
        print("-" * 100)
        
        groups_data = []
        
        for dialog in dialogs:
            # Определяем тип чата
            if dialog.is_user:
                chat_type = "👤 Личный"
                participants_count = "-"
            elif dialog.is_group:
                chat_type = "👥 Группа"
                # Для групп получаем информацию через GroupManager (с анти-спам защитой)
                try:
                    group_info = await manager.get_group_info(dialog.id)
                    participants_count = str(group_info.get('participants_count', '?')) if group_info else "?"
                    if group_info:
                        groups_data.append({
                            'id': dialog.id,
                            'title': dialog.title,
                            'participants_count': group_info.get('participants_count', 0),
                            'type': 'group'
                        })
                except Exception as e:
                    logger.warning(f"Не удалось получить информацию о группе {dialog.id}: {e}")
                    participants_count = "?"
            elif dialog.is_channel:
                chat_type = "📢 Канал"
                # Для каналов также получаем информацию через GroupManager
                try:
                    channel_info = await manager.get_group_info(dialog.id)
                    participants_count = str(channel_info.get('participants_count', '?')) if channel_info else "?"
                    if channel_info:
                        groups_data.append({
                            'id': dialog.id,
                            'title': dialog.title,
                            'participants_count': channel_info.get('participants_count', 0),
                            'type': 'channel'
                        })
                except Exception as e:
                    logger.warning(f"Не удалось получить информацию о канале {dialog.id}: {e}")
                    participants_count = "?"
            else:
                chat_type = "❓ Другой"
                participants_count = "-"
            
            # Выводим информацию
            chat_id = str(dialog.id)
            title = dialog.title[:40] if dialog.title else "Без названия"  # Ограничиваем длину названия
            
            print(f"{chat_id.ljust(15)} | {chat_type.ljust(10)} | {participants_count.ljust(10)} | {title}")
        
        print(f"\n✅ Найдено {len(dialogs)} чатов")
        
        # Статистика rate limiter
        stats = rate_limiter.get_stats()
        print(f"📊 Статистика анти-спам: API вызовов: {stats['api_calls']}, FLOOD_WAIT: {stats['flood_waits']}")
        
        await client.disconnect()
        return groups_data
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        logger.error(f"Ошибка при получении чатов: {e}")
        return []

async def main():
    """Главная функция с использованием S16-leads интерфейсов"""
    groups_data = await get_my_chats_with_details()
    
    # Дополнительная информация о группах
    if groups_data:
        print(f"\n📊 СТАТИСТИКА ГРУПП И КАНАЛОВ:")
        print(f"Всего групп/каналов: {len(groups_data)}")
        
        # Сортируем по количеству участников
        groups_data.sort(key=lambda x: x.get('participants_count', 0), reverse=True)
        
        print(f"\n🔝 ТОП-10 по участникам:")
        for i, group in enumerate(groups_data[:10], 1):
            title = group['title'][:35]
            participants = group.get('participants_count', 0)
            group_type = "🏢" if group['type'] == 'channel' else "👥"
            print(f"   {i:2d}. {group_type} {title} - {participants} чел.")

if __name__ == "__main__":
    asyncio.run(main()) 