#!/usr/bin/env python3
"""
S16 Cross-Check Example
Использует существующие интерфейсы проекта для сверки участников между S16 группами
"""

import asyncio
import argparse
from pathlib import Path
from tg_core.infra.tele_client import get_client
from tg_core.domain.groups import GroupManager
from apps.s16leads.app.config import get_space_group_id, get_space_group_name


async def s16_crosscheck(target_group_id: int, target_group_name: str = None, output_file: str = None):
    """
    Сверка участников целевой группы с референсной группой s16 space
    
    Args:
        target_group_id: ID целевой группы для сверки
        target_group_name: Название группы (для отчетов)
        output_file: Файл для сохранения результатов
    """
    print(f"🔍 S16 Cross-Check: {target_group_name or target_group_id}")
    print("=" * 60)
    
    client = get_client()
    await client.start()
    manager = GroupManager(client)
    
    # Референсная группа из конфигурации
    space_id = get_space_group_id()
    space_name = get_space_group_name()
    
    try:
        # 1. Получаем информацию о группах
        print(f"📊 Целевая группа: {target_group_name or 'Unknown'} (ID: {target_group_id})")
        print(f"📊 Референсная группа: {space_name} (ID: {space_id})")
        print()
        
        # 2. Получаем участников (используем существующий API)
        print("📥 Получение участников целевой группы...")
        target_participants = await manager.get_participants(target_group_id, limit=300)
        print(f"✅ Получено {len(target_participants)} участников")
        
        print(f"📥 Получение участников {space_name}...")
        space_participants = await manager.get_participants(space_id, limit=500)
        print(f"✅ Получено {len(space_participants)} участников")
        print()
        
        # 3. Анализ пересечений (используем существующие данные)
        target_ids = {p['id'] for p in target_participants}
        space_ids = {p['id'] for p in space_participants}
        
        existing_in_space = target_ids & space_ids
        new_participants = target_ids - space_ids
        
        # 4. Результаты
        result = {
            'target_group': target_group_name or str(target_group_id),
            'target_id': target_group_id,
            'space_group': space_name,
            'space_id': space_id,
            'total_target': len(target_participants),
            'total_space': len(space_participants),
            'existing_count': len(existing_in_space),
            'new_count': len(new_participants),
            'existing_percentage': len(existing_in_space) / len(target_participants) * 100,
            'new_percentage': len(new_participants) / len(target_participants) * 100,
            'existing_members': [],
            'new_members': []
        }
        
        # 5. Детальные списки
        for p in target_participants:
            member_info = {
                'id': p['id'],
                'username': p.get('username'),
                'first_name': p.get('first_name'),
                'last_name': p.get('last_name'),
                'is_premium': p.get('is_premium', False)
            }
            
            if p['id'] in existing_in_space:
                result['existing_members'].append(member_info)
            else:
                result['new_members'].append(member_info)
        
        # 6. Вывод результатов
        print_results(result)
        
        # 7. Сохранение в файл (если указан)
        if output_file:
            await save_results(result, output_file)
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        
    await client.disconnect()


def print_results(result: dict):
    """Выводит результаты сверки в консоль"""
    print("🎯 РЕЗУЛЬТАТЫ СВЕРКИ:")
    print(f"👥 Всего в {result['target_group']}: {result['total_target']}")
    print(f"✅ Уже в {result['space_group']}: {result['existing_count']} ({result['existing_percentage']:.1f}%)")
    print(f"🆕 Новых участников: {result['new_count']} ({result['new_percentage']:.1f}%)")
    print()
    
    if result['existing_members']:
        print(f"✅ УЖЕ В {result['space_group'].upper()} ({len(result['existing_members'])} чел.):")
        for i, member in enumerate(result['existing_members'][:10], 1):  # Показываем первые 10
            name = f"{member.get('first_name', '')} {member.get('last_name') or ''}".strip()
            username = member.get('username') or 'no_username'
            premium = '👑' if member.get('is_premium') else ''
            print(f"   {i:2d}. @{username} - {name} {premium}")
        
        if len(result['existing_members']) > 10:
            print(f"   ... и еще {len(result['existing_members']) - 10} участников")
        print()
    
    if result['new_members']:
        print(f"🆕 НОВЫЕ УЧАСТНИКИ ({len(result['new_members'])} чел.):")
        for i, member in enumerate(result['new_members'][:10], 1):  # Показываем первые 10
            name = f"{member.get('first_name', '')} {member.get('last_name') or ''}".strip()
            username = member.get('username') or 'no_username'
            premium = '👑' if member.get('is_premium') else ''
            print(f"   {i:2d}. @{username} - {name} {premium}")
            
        if len(result['new_members']) > 10:
            print(f"   ... и еще {len(result['new_members']) - 10} участников")


async def save_results(result: dict, output_file: str):
    """Сохраняет результаты в JSON файл"""
    import json
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"💾 Результаты сохранены в: {output_file}")


async def main():
    """CLI интерфейс для S16 сверки"""
    parser = argparse.ArgumentParser(description='S16 Cross-Check: Сверка участников с s16 space')
    parser.add_argument('target_group', help='ID целевой группы для сверки')
    parser.add_argument('--name', help='Название целевой группы')
    parser.add_argument('--output', help='Файл для сохранения результатов (JSON)')
    
    args = parser.parse_args()
    
    try:
        target_id = int(args.target_group)
        await s16_crosscheck(target_id, args.name, args.output)
    except ValueError:
        print("❌ Ошибка: target_group должен быть числовым ID")
    except KeyboardInterrupt:
        print("\n⚠️ Операция прервана пользователем")


if __name__ == "__main__":
    asyncio.run(main()) 