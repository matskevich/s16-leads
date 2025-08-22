#!/usr/bin/env python3
"""
Экспорт мужчин из тантрических групп в CSV для Google Sheets
"""

import json
import csv
from pathlib import Path

def main():
    # Путь к финальному JSON
    json_path = Path("data/tantra_project/tantra_participants_ultra_final.json")
    
    if not json_path.exists():
        print(f"❌ Файл не найден: {json_path}")
        return
    
    print("📊 ЭКСПОРТ МУЖЧИН ИЗ ТАНТРИЧЕСКИХ ГРУПП В CSV:")
    print("=" * 60)
    
    # Загружаем данные
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Фильтруем только мужчин
    men = [p for p in data['participants'] if p['gender_analysis'] == 'male']
    
    # Сортируем по количеству тантр (убывание), потом по имени
    men.sort(key=lambda x: (-x['tantra_count'], x['first_name'].lower()))
    
    # Подготавливаем данные для CSV
    csv_data = []
    
    for participant in men:
        # Формируем ссылку на Telegram
        tg_link = f"https://t.me/{participant['username']}" if participant['username'] else ""
        
        # Формируем ФИО
        full_name = f"{participant['first_name']} {participant['last_name']}".strip()
        
        # Формируем список тантр
        tantra_events = []
        if participant['altai22']:
            tantra_events.append('Altai22')
        if participant['bali23']:
            tantra_events.append('Bali23')
        if participant['lisbon24']:
            tantra_events.append('Lisbon24')
        
        tantra_list = ' + '.join(tantra_events)
        
        # Добавляем в CSV данные
        csv_data.append({
            'Telegram Link': tg_link,
            'Username': f"@{participant['username']}" if participant['username'] else "",
            'Full Name': full_name,
            'Tantra Count': participant['tantra_count'],
            'Tantra Events': tantra_list,
            'Premium': 'Yes' if participant.get('is_premium', False) else 'No'
        })
    
    # Сохраняем в CSV
    output_path = Path("data/tantra_project/tantra_men.csv")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Telegram Link', 'Username', 'Full Name', 'Tantra Count', 'Tantra Events', 'Premium']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ ЭКСПОРТ ЗАВЕРШЕН:")
    print(f"   📁 Файл: {output_path}")
    print(f"   👥 Мужчин найдено: {len(men)}")
    print(f"   📋 Столбцы: Telegram Link, Username, Full Name, Tantra Count, Tantra Events, Premium")
    
    # Статистика по количеству тантр
    tantra_stats = {}
    for man in men:
        count = man['tantra_count']
        tantra_stats[count] = tantra_stats.get(count, 0) + 1
    
    print()
    print("📈 СТАТИСТИКА ПО КОЛИЧЕСТВУ ТАНТР:")
    for count in sorted(tantra_stats.keys(), reverse=True):
        print(f"   {count} тантр{'ы' if count in [2,3,4] else ''}: {tantra_stats[count]} мужчин")
    
    # Показываем топ-5 самых активных
    print()
    print("🏆 ТОП-5 САМЫХ АКТИВНЫХ МУЖЧИН:")
    for i, man in enumerate(men[:5], 1):
        events = []
        if man['altai22']: events.append('Altai22')
        if man['bali23']: events.append('Bali23')
        if man['lisbon24']: events.append('Lisbon24')
        
        premium = " ⭐" if man.get('is_premium', False) else ""
        print(f"   {i}. @{man['username']} ({man['first_name']}) - {man['tantra_count']} тантр{premium}")
        print(f"      События: {' + '.join(events)}")
    
    print()
    print("💡 ГОТОВО ДЛЯ ИМПОРТА В GOOGLE SHEETS:")
    print("   1. Откройте Google Sheets")
    print("   2. Файл → Импорт → Загрузить")
    print("   3. Выберите tantra_men.csv")
    print("   4. Разделитель: Запятая, Кодировка: UTF-8")

if __name__ == "__main__":
    main()
