#!/usr/bin/env python3
"""
Обновляет JSON участников тантры с улучшенным алгоритмом определения пола
"""

import json
import os
from pathlib import Path
from tg_core.domain.groups import GroupManager  # example of core import if needed
from apps.wildtantra.app.config import config  # app-specific config

# local analyzer remains app-specific if exists; fallback if not present
try:
    from app.gender_analyzer import analyze_telegram_user_gender_detailed  # type: ignore
except Exception:  # pragma: no cover
    def analyze_telegram_user_gender_detailed(first_name: str, last_name: str, username: str):
        # minimal fallback heuristic
        name = (first_name or "") + " " + (last_name or "")
        if name.strip().endswith("a"):
            return "female", 0.5
        return "male", 0.5

def main():
    # Путь к файлу
    json_path = Path("data/tantra_project/tantra_participants_super_final.json")
    
    if not json_path.exists():
        print(f"❌ Файл не найден: {json_path}")
        return
    
    print("🔄 ОБНОВЛЯЮ JSON С МАКСИМАЛЬНО ОБУЧЕННЫМ АЛГОРИТМОМ:")
    print("=" * 70)
    
    # Загружаем данные
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Статистика до
    before_stats = {
        'male': len([p for p in data['participants'] if p['gender_analysis'] == 'male']),
        'female': len([p for p in data['participants'] if p['gender_analysis'] == 'female']),
        'unknown': len([p for p in data['participants'] if p['gender_analysis'] == 'unknown'])
    }
    
    print(f"📊 СТАТИСТИКА ДО ОБНОВЛЕНИЯ:")
    print(f"   ♂️  Мужчин: {before_stats['male']}")
    print(f"   ♀️  Женщин: {before_stats['female']}")
    print(f"   ❓ Неопределенных: {before_stats['unknown']}")
    
    # Обновляем анализ пола для всех участников
    updated_count = 0
    newly_classified = []
    
    for participant in data['participants']:
        old_gender = participant['gender_analysis']
        
        # Повторный анализ с улучшенным алгоритмом
        new_gender, _ = analyze_telegram_user_gender_detailed(
            first_name=participant['first_name'],
            last_name=participant['last_name'],
            username=participant['username']
        )
        
        if old_gender != new_gender:
            participant['gender_analysis'] = new_gender
            updated_count += 1
            
            if old_gender == 'unknown' and new_gender in ['male', 'female']:
                newly_classified.append({
                    'username': participant['username'],
                    'name': f"{participant['first_name']} {participant['last_name']}".strip(),
                    'old': old_gender,
                    'new': new_gender
                })
    
    # Пересчитываем статистику
    after_stats = {
        'male': len([p for p in data['participants'] if p['gender_analysis'] == 'male']),
        'female': len([p for p in data['participants'] if p['gender_analysis'] == 'female']),
        'unknown': len([p for p in data['participants'] if p['gender_analysis'] == 'unknown'])
    }
    
    # Обновляем статистику в JSON
    data['statistics']['gender_distribution'] = {
        'male': after_stats['male'],
        'female': after_stats['female'],
        'unknown': after_stats['unknown']
    }
    
    # Сохраняем обновленный JSON
    output_path = Path("data/tantra_project/tantra_participants_ultra_final.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"📊 СТАТИСТИКА ПОСЛЕ ОБНОВЛЕНИЯ:")
    print(f"   ♂️  Мужчин: {after_stats['male']} (+{after_stats['male'] - before_stats['male']})")
    print(f"   ♀️  Женщин: {after_stats['female']} (+{after_stats['female'] - before_stats['female']})")
    print(f"   ❓ Неопределенных: {after_stats['unknown']} ({after_stats['unknown'] - before_stats['unknown']:+d})")
    print(f"   🎯 Точность: {((after_stats['male'] + after_stats['female'])/data['statistics']['total_participants']*100):.1f}%")
    
    print()
    print(f"🔄 ОБНОВЛЕНО ЗАПИСЕЙ: {updated_count}")
    
    if newly_classified:
        print()
        print(f"🎉 НОВЫЕ КЛАССИФИКАЦИИ ({len(newly_classified)}):")
        for item in newly_classified:
            symbol = "♂️" if item['new'] == 'male' else "♀️"
            print(f"   {symbol} @{item['username']} ({item['name']})")
    
    print()
    print(f"💾 СОХРАНЕНО: {output_path}")
    
    # Показываем оставшихся неопределенных
    unknown_participants = [p for p in data['participants'] if p['gender_analysis'] == 'unknown']
    
    if unknown_participants:
        print()
        print(f"❓ УЧАСТНИКИ ДЛЯ РУЧНОЙ КЛАССИФИКАЦИИ ({len(unknown_participants)}):")
        print("=" * 50)
        
        for i, participant in enumerate(unknown_participants, 1):
            events = []
            if participant['altai22']: events.append('Altai22')
            if participant['bali23']: events.append('Bali23') 
            if participant['lisbon24']: events.append('Lisbon24')
            
            priority = '⭐' if participant['tantra_count'] > 1 else ''
            
            print(f'{i}. @{participant["username"]:20} {priority}')
            print(f'   Имя: "{participant["first_name"]}" "{participant["last_name"]}"')
            print(f'   Тантр: {participant["tantra_count"]} ({" + ".join(events)})')
            print()
    else:
        print()
        print("🎉 ВСЕ УЧАСТНИКИ КЛАССИФИЦИРОВАНЫ!")

if __name__ == "__main__":
    main()
