#!/usr/bin/env python3
"""
Пример использования S16 конфигурации
Демонстрирует работу с настройками ключевых групп проекта S16
"""

import asyncio
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))  # adds apps/s16-leads to sys.path
from app.config import get_s16_config, get_space_group_id, get_space_group_name
from tg_core.infra.tele_client import get_client
from tg_core.domain.groups import GroupManager


async def test_s16_config():
    """Тестирует S16 конфигурацию и показывает информацию о ключевой группе"""
    
    print("🚀 Тестирование S16 конфигурации\n")
    
    # 1. Показываем конфигурацию
    config = get_s16_config()
    print("📋 Текущая конфигурация S16:")
    print(config)
    print()
    
    # 2. Быстрый доступ к настройкам
    print("⚡ Быстрый доступ к настройкам:")
    print(f"   🎯 ID группы s16 space: {get_space_group_id()}")
    print(f"   📝 Название группы: {get_space_group_name()}")
    print(f"   🔍 Сверка включена: {config.is_cross_check_enabled()}")
    print(f"   🏷️  Помечать существующих: {config.should_mark_existing_members()}")
    print(f"   📊 Экспорт сравнения: {config.should_export_comparison()}")
    print()
    
    # 3. Проверяем доступ к ключевой группе
    try:
        print("🔌 Подключение к Telegram...")
        client = get_client()
        await client.start()
        
        manager = GroupManager(client)
        
        print(f"📊 Получение информации о ключевой группе '{get_space_group_name()}'...")
        group_info = await manager.get_group_info(get_space_group_id())
        
        if group_info:
            print("✅ Информация о ключевой группе s16 space:")
            print(f"   📝 Название: {group_info['title']}")
            print(f"   👥 Участников: {group_info['participants_count']}")
            print(f"   🔗 Username: @{group_info['username'] or 'Нет username'}")
            print(f"   📄 Описание: {group_info['description'][:100] if group_info['description'] else 'Нет описания'}...")
        else:
            print(f"❌ Не удалось получить информацию о группе {get_space_group_id()}")
        
        await client.disconnect()
        
    except Exception as e:
        print(f"❌ Ошибка при подключении: {e}")
    
    print("\n✅ Тестирование S16 конфигурации завершено!")


async def demo_cross_check_logic():
    """Демонстрирует логику сверки участников с s16 space"""
    
    print("\n" + "="*50)
    print("🔍 DEMO: Логика сверки участников")
    print("="*50)
    
    config = get_s16_config()
    
    if not config.is_cross_check_enabled():
        print("⚠️  Сверка участников отключена в конфигурации")
        return
    
    print(f"🎯 Ключевая группа для сверки: {get_space_group_name()}")
    print(f"📊 ID группы: {get_space_group_id()}")
    print()
    
    # Псевдо-логика сверки (для демонстрации)
    print("💡 Логика работы сверки:")
    print("   1. Получаем участников из целевой группы")
    print("   2. Получаем участников из s16 space")
    print("   3. Сравниваем списки")
    
    if config.should_mark_existing_members():
        print("   4. ✅ Помечаем участников уже состоящих в s16 space")
    
    if config.should_export_comparison():
        print("   5. 📊 Экспортируем результаты сравнения")
    
    print("\n📋 Пример результата сверки:")
    print("   👥 Всего участников в группе: 150")
    print("   ✅ Уже в s16 space: 45 (30%)")
    print("   🆕 Новых участников: 105 (70%)")


if __name__ == "__main__":
    asyncio.run(test_s16_config())
    asyncio.run(demo_cross_check_logic()) 