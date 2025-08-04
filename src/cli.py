#!/usr/bin/env python3
"""
CLI интерфейс для работы с группами Telegram
"""

import asyncio
import argparse
import json
from pathlib import Path
from src.infra.tele_client import get_client
from src.core.group_manager import GroupManager

async def main():
    parser = argparse.ArgumentParser(description='S16-Leads: Работа с группами Telegram')
    parser.add_argument('command', choices=['info', 'participants', 'search', 'export', 'creation-date'], 
                       help='Команда для выполнения')
    parser.add_argument('group', help='Username группы (без @) или ID группы')
    parser.add_argument('--limit', type=int, default=100, 
                       help='Максимальное количество участников (по умолчанию: 100)')
    parser.add_argument('--query', help='Поисковый запрос (для команды search)')
    parser.add_argument('--output', help='Файл для экспорта (для команды export)')
    parser.add_argument('--format', choices=['json', 'csv'], default='json',
                       help='Формат вывода (по умолчанию: json)')
    
    args = parser.parse_args()
    
    try:
        # Получаем клиент
        client = get_client()
        await client.start()
        
        # Создаем менеджер групп
        group_manager = GroupManager(client)
        
        if args.command == 'info':
            await handle_info(group_manager, args.group)
            
        elif args.command == 'participants':
            await handle_participants(group_manager, args.group, args.limit, args.format)
            
        elif args.command == 'search':
            if not args.query:
                print("❌ Для команды search необходимо указать --query")
                return
            await handle_search(group_manager, args.group, args.query, args.limit, args.format)
            
        elif args.command == 'export':
            if not args.output:
                print("❌ Для команды export необходимо указать --output")
                return
            await handle_export(group_manager, args.group, args.output, args.limit)
            
        elif args.command == 'creation-date':
            await handle_creation_date(group_manager, args.group)
        
        await client.disconnect()
        
    except KeyboardInterrupt:
        print("\n⚠️ Операция прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

async def handle_info(group_manager: GroupManager, group: str):
    """Обработка команды info"""
    print(f"📋 Получение информации о группе: {group}")
    
    info = await group_manager.get_group_info(group)
    if info:
        print(f"✅ Найдена группа: {info['title']}")
        print(f"   ID: {info['id']}")
        print(f"   Username: @{info['username']}" if info['username'] else "   Username: Нет")
        print(f"   Тип: {info['type']}")
        print(f"   Участников: {info['participants_count']}")
    else:
        print(f"❌ Группа {group} не найдена")

async def handle_participants(group_manager: GroupManager, group: str, limit: int, format: str):
    """Обработка команды participants"""
    print(f"👥 Получение участников группы: {group} (лимит: {limit})")
    
    participants = await group_manager.get_participants(group, limit)
    
    if participants:
        print(f"✅ Получено {len(participants)} участников")
        
        if format == 'json':
            print(json.dumps(participants, ensure_ascii=False, indent=2))
        else:
            # Простой текстовый вывод
            for i, participant in enumerate(participants, 1):
                username = participant['username'] or 'Нет username'
                name = f"{participant['first_name'] or ''} {participant['last_name'] or ''}".strip()
                print(f"{i:3d}. {username} - {name}")
    else:
        print("❌ Не удалось получить участников")

async def handle_search(group_manager: GroupManager, group: str, query: str, limit: int, format: str):
    """Обработка команды search"""
    print(f"🔍 Поиск участников в группе {group} по запросу: {query}")
    
    participants = await group_manager.search_participants(group, query, limit)
    
    if participants:
        print(f"✅ Найдено {len(participants)} участников")
        
        if format == 'json':
            print(json.dumps(participants, ensure_ascii=False, indent=2))
        else:
            for i, participant in enumerate(participants, 1):
                username = participant['username'] or 'Нет username'
                name = f"{participant['first_name'] or ''} {participant['last_name'] or ''}".strip()
                print(f"{i:3d}. {username} - {name}")
    else:
        print("❌ Участники не найдены")

async def handle_export(group_manager: GroupManager, group: str, output: str, limit: int):
    """Обработка команды export"""
    print(f"📤 Экспорт участников группы {group} в файл: {output}")
    
    # Создаем директорию для экспорта если нужно
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if output_path.suffix.lower() == '.csv':
        success = await group_manager.export_participants_to_csv(group, output, limit)
    else:
        # JSON экспорт
        participants = await group_manager.get_participants(group, limit)
        if participants:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(participants, f, ensure_ascii=False, indent=2)
            print(f"✅ Экспортировано {len(participants)} участников в {output}")
            success = True
        else:
            success = False
    
    if not success:
        print("❌ Ошибка при экспорте")

async def handle_creation_date(group_manager: GroupManager, group: str):
    """Обработка команды creation-date"""
    print(f"📅 Получение даты создания группы {group}...")
    
    creation_date = await group_manager.get_group_creation_date(group)
    
    if creation_date:
        formatted_date = creation_date.strftime("%Y-%m-%d %H:%M:%S UTC")
        formatted_date_short = creation_date.strftime("%Y-%m-%d")
        
        print(f"✅ Группа создана: {formatted_date}")
        print(f"📊 Краткий формат: {formatted_date_short}")
        
        # Дополнительная информация
        from datetime import datetime
        now = datetime.now(creation_date.tzinfo)
        age = now - creation_date
        
        years = age.days // 365
        months = (age.days % 365) // 30
        days = age.days % 30
        
        age_str = []
        if years > 0:
            age_str.append(f"{years} лет")
        if months > 0:
            age_str.append(f"{months} месяцев")
        if days > 0:
            age_str.append(f"{days} дней")
        
        if age_str:
            print(f"🕐 Возраст группы: {', '.join(age_str)}")
        
    else:
        print("❌ Не удалось получить дату создания группы")

if __name__ == "__main__":
    asyncio.run(main())
