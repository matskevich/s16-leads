#!/usr/bin/env python3
"""
Простой экспорт групп в 3 JSON файла
ИСПОЛЬЗУЕТ S16-leads анти-спам защиту
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Set

from tg_core.infra.tele_client import get_client
from tg_core.infra.limiter import get_rate_limiter, smart_pause
from tg_core.domain.groups import GroupManager
import logging

logger = logging.getLogger(__name__)

# Ваш список групп
GROUP_IDS = [
    -1002188344480,  # s16 space
    -1002609724956,  # Заповедник '25
    -1002214341140,  # S16 Festival // Landing
    -1001527724829,  # S16 Open Coliving '22
    -1001267405994,  # S16 (ne)Slët
    -1001709503226,  # Coliving '23
    -1002540509234,  # S16 Coliving DOMA
    -1001631833231,  # s16 camp on waking life
    -1002507355081,  # Пасха 2025
    -1001393171192,  # Shmit16 21 — Coliving
    -1001454118014,  # Shmit16 @ Anatman 2019
    -1001461037525,  # Halloween Party
    -1001926931511,  # New Year on Madeira
]

async def export_to_3_jsons():
    """Экспорт в 3 JSON файла с анти-спам защитой"""
    
    print("🚀 Экспорт в 3 JSON файла с анти-спам защитой...")
    print(f"📊 Групп к обработке: {len(GROUP_IDS)}")
    print("")
    
    # Инициализация
    client = get_client()
    await client.start()
    
    rate_limiter = get_rate_limiter()
    manager = GroupManager(client)
    
    # Подготовка данных
    groups = []           # для groups.json
    all_members = {}      # для дедупликации members
    group_members = []    # для group_members.json
    
    # ЭТАП 1: Собираем группы и участников
    print("=" * 50)
    print("ЭТАП 1: СБОР ДАННЫХ")
    print("=" * 50)
    
    for i, group_id in enumerate(GROUP_IDS, 1):
        try:
            print(f"📊 {i:2d}/{len(GROUP_IDS)} Обработка группы {group_id}...")
            
            # Получаем информацию о группе
            group_info = await manager.get_group_info(group_id)
            if not group_info:
                print(f"   ❌ Не удалось получить информацию о группе")
                continue
                
            print(f"   📝 {group_info['title']} ({group_info.get('participants_count', '?')} участников)")
            
            # Добавляем в groups (используем исходный group_id, а не тот что из API)
            groups.append({
                "group_id": group_id,  # Используем исходный ID из списка
                "title": group_info['title']
            })
            
            # Получаем участников
            participants = await manager.get_participants(group_id, limit=None)
            if not participants:
                print(f"   ⚠️ Не удалось получить участников")
                continue
            
            # Обрабатываем участников
            for participant in participants:
                user_id = participant['id']
                
                # Добавляем уникального участника
                if user_id not in all_members:
                    all_members[user_id] = {
                        "user_id": user_id,
                        "username": participant.get('username'),
                        "first_name": participant.get('first_name'),
                        "last_name": participant.get('last_name'),
                        "is_premium": participant.get('is_premium', False),
                        "is_verified": participant.get('is_verified', False)
                    }
                
                # Добавляем связь группа-участник
                group_members.append({
                    "group_id": group_id,
                    "user_id": user_id
                })
            
            print(f"   ✅ Обработано {len(participants)} участников")
            
            # Smart pause каждые 3 группы
            if i % 3 == 0 and i < len(GROUP_IDS):
                await smart_pause("export", i)
                print(f"   ⏳ Пауза для анти-спам защиты...")
                
        except Exception as e:
            logger.error(f"Ошибка при обработке группы {group_id}: {e}")
            continue
        
        print("")
    
    # ЭТАП 2: Сохранение JSON файлов
    print("=" * 50)
    print("ЭТАП 2: СОХРАНЕНИЕ JSON ФАЙЛОВ")
    print("=" * 50)
    
    # Создаем директорию
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"data/export/s16_export_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Конвертируем members в список
    members = list(all_members.values())
    
    # 1. groups.json
    groups_file = f"{output_dir}/groups.json"
    groups_data = {
        "groups": groups
    }
    with open(groups_file, 'w', encoding='utf-8') as f:
        json.dump(groups_data, f, ensure_ascii=False, indent=2)
    print(f"✅ {groups_file} - {len(groups)} групп")
    
    # 2. members.json  
    members_file = f"{output_dir}/members.json"
    members_data = {
        "members": members
    }
    with open(members_file, 'w', encoding='utf-8') as f:
        json.dump(members_data, f, ensure_ascii=False, indent=2)
    print(f"✅ {members_file} - {len(members)} уникальных участников")
    
    # 3. group_members.json
    group_members_file = f"{output_dir}/group_members.json"
    group_members_data = {
        "group_members": group_members
    }
    with open(group_members_file, 'w', encoding='utf-8') as f:
        json.dump(group_members_data, f, ensure_ascii=False, indent=2)
    print(f"✅ {group_members_file} - {len(group_members)} связей")
    
    # ФИНАЛЬНАЯ СТАТИСТИКА
    print("\n" + "=" * 50)
    print("🎉 ЭКСПОРТ ЗАВЕРШЕН!")
    print("=" * 50)
    
    stats = rate_limiter.get_stats()
    print(f"🛡️ Анти-спам статистика:")
    print(f"   • API вызовов: {stats['api_calls']}")
    print(f"   • FLOOD_WAIT ошибок: {stats['flood_waits']}")
    print(f"   • Текущий RPS: {stats['current_rps']}")
    
    print(f"\n📊 Результаты:")
    print(f"   • Групп обработано: {len(groups)}")
    print(f"   • Уникальных участников: {len(members)}")
    print(f"   • Связей группа-участник: {len(group_members)}")
    print(f"   • Директория: {output_dir}")
    
    await client.disconnect()
    return True

if __name__ == "__main__":
    print("📋 Экспорт 13 S16 групп в 3 JSON файла")
    print("🛡️ Использует анти-спам защиту S16-leads")
    print("")
    
    success = asyncio.run(export_to_3_jsons())
    if success:
        print("\n🎯 Все готово! Три JSON файла созданы.")
    else:
        print("\n❌ Произошла ошибка при экспорте")