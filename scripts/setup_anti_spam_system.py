#!/usr/bin/env python3
"""
Setup скрипт для анти-спам системы S16-leads
Устанавливает все компоненты автоматической проверки
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd: str, description: str) -> bool:
    """Запускает команду и возвращает результат"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"   Error: {e.stderr}")
        return False

def setup_anti_spam_system():
    """Главная функция установки"""
    print("🛡️ УСТАНОВКА АНТИ-СПАМ СИСТЕМЫ S16-LEADS")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    success_count = 0
    total_steps = 8
    
    # 1. Установка development dependencies
    if run_command("make dev-install", "Установка development dependencies"):
        success_count += 1
    
    # 2. Настройка pre-commit hooks
    if run_command("make pre-commit-setup", "Настройка pre-commit hooks"):
        success_count += 1
    
    # 3. Проверка анти-спам соответствия
    if run_command("python scripts/check_anti_spam_compliance.py", "Проверка анти-спам соответствия"):
        success_count += 1
    
    # 4. Запуск линтера
    if run_command("make lint", "Проверка качества кода"):
        success_count += 1
    
    # 5. Проверка форматирования
    if run_command("make format-check", "Проверка форматирования кода"):
        success_count += 1
    
    # 6. Запуск тестов
    if run_command("make test", "Запуск тестов"):
        success_count += 1
    
    # 7. Comprehensive audit
    if run_command("make telegram-api-audit", "Комплексный аудит Telegram API"):
        success_count += 1
    
    # 8. Security check
    if run_command("make security-check", "Проверка безопасности"):
        success_count += 1
    
    print()
    print("=" * 60)
    print(f"📊 РЕЗУЛЬТАТЫ УСТАНОВКИ: {success_count}/{total_steps}")
    
    if success_count == total_steps:
        print("✅ ВСЯ АНТИ-СПАМ СИСТЕМА УСТАНОВЛЕНА И РАБОТАЕТ!")
        print()
        print("🎯 ДОСТУПНЫЕ КОМАНДЫ:")
        print("  make anti-spam-check    - Быстрая проверка анти-спам соответствия")
        print("  make dev-check          - Проверки перед коммитом")
        print("  make check-all          - Полная проверка (CI pipeline)")
        print("  make telegram-api-audit - Аудит Telegram API использования")
        print("  make help-security      - Справка по всем security командам")
        print()
        print("🪝 PRE-COMMIT HOOKS АКТИВНЫ:")
        print("  При каждом коммите будут автоматически запускаться:")
        print("  - Проверка анти-спам соответствия")
        print("  - Форматирование кода")
        print("  - Линтинг")
        print("  - Security scan")
        print()
        print("🚀 СЛЕДУЮЩИЕ ШАГИ:")
        print("  1. Прочитайте docs/CODE_REVIEW_CHECKLIST.md")
        print("  2. Изучите docs/TELEGRAM_API_PATTERNS.md")
        print("  3. При создании новых функций используйте templates")
        print("  4. Регулярно запускайте 'make telegram-api-audit'")
        
        return True
    else:
        print("❌ УСТАНОВКА ЗАВЕРШЕНА С ОШИБКАМИ")
        print("🔧 Исправьте ошибки и запустите скрипт снова")
        return False

def main():
    """Entry point"""
    if not setup_anti_spam_system():
        sys.exit(1)
    
    print()
    print("🎉 АНТИ-СПАМ СИСТЕМА S16-LEADS ГОТОВА К РАБОТЕ!")

if __name__ == "__main__":
    main()