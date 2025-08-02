# 🚀 S16-Leads - Руководство по передаче проекта

## 📋 Что это за проект?

**S16-Leads** - это Telegram-клиент для работы с лидами на базе библиотеки Telethon. Проект позволяет:

- 🔍 **Получать списки участников** из Telegram групп и каналов
- 🎯 **Фильтровать участников** по различным критериям  
- 📊 **Экспортировать данные** в JSON/CSV форматы
- 🛡️ **Защита от банов** - встроенная anti-spam система
- 💻 **CLI интерфейс** для удобного использования

### 🏆 Особенности проекта:
- ✅ **Production-ready** - протестирован на 386+ участниках
- ✅ **Anti-spam защита** - система rate limiting (4 RPS)
- ✅ **Comprehensive tests** - 21 unit тест
- ✅ **Memory Bank** - система управления задачами
- ✅ **Полная документация** - включая архивы выполненных задач

---

## 🛠️ Быстрый старт для друга

### Шаг 1: Клонирование и настройка

```bash
# 1. Клонируйте проект
git clone <repository-url>
cd s16-leads

# 2. Создайте виртуальное окружение
python3 -m venv venv

# Активация на Linux/Mac:
source venv/bin/activate

# Активация на Windows:
venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt
```

### Шаг 2: Получение Telegram API ключей

1. **Перейдите на** https://my.telegram.org/apps
2. **Войдите** с помощью вашего телефона
3. **Создайте новое приложение:**
   - App title: `S16-Leads`
   - Short name: `s16leads`
   - Platform: `Desktop`
4. **Сохраните** `api_id` и `api_hash`

### Шаг 3: Настройка конфигурации

```bash
# 1. Скопируйте шаблон конфигурации
cp .env.sample .env

# 2. Отредактируйте .env файл
nano .env  # или любой другой редактор
```

**В файле `.env` укажите:**
```bash
# ОБЯЗАТЕЛЬНО заполните:
TG_API_ID=ваш_api_id_здесь
TG_API_HASH=ваш_api_hash_здесь

# Остальное можно оставить как есть
SESSION_NAME=s16_session
RATE_RPS=4
MAX_DM_PER_DAY=20
# ... остальные настройки уже настроены
```

### Шаг 4: Первый запуск и тест

```bash
# 1. Протестируйте подключение
python3 src/infra/tele_client.py

# При первом запуске потребуется:
# - Ввести номер телефона
# - Ввести код подтверждения из Telegram
# - Возможно, пароль 2FA

# 2. Проверьте что все работает
python3 examples/list_my_chats.py
```

---

## 🎯 Примеры использования

### Пример 1: Просмотр всех ваших чатов
```bash
python3 examples/list_my_chats.py
```

### Пример 2: Тестирование функций групп
```bash
python3 examples/test_group_functions.py
```

### Пример 3: Получение участников группы
```python
from src.infra.tele_client import get_client
from src.core.group_manager import GroupManager

async def get_participants_example():
    client = get_client()
    await client.start()
    
    manager = GroupManager(client)
    participants = await manager.get_participants("python", limit=100)
    
    print(f"Найдено {len(participants)} участников")
    await client.disconnect()
```

---

## 🛡️ Безопасность (ВАЖНО!)

### ⚠️ НИКОГДА НЕ ДЕЛИТЕСЬ:
- Файлом `.env` (содержит API ключи)
- Файлами из `data/sessions/` (токены доступа)
- Файлами с экспортированными данными

### ✅ Безопасная передача:
1. **Удалите** `.env` файл перед отправкой
2. **Очистите** папку `data/sessions/`
3. **Проверьте** `.gitignore` - защищённые файлы не должны попасть в git

```bash
# Проверка безопасности перед передачей:
git status --ignored
ls -la data/sessions/
```

---

## 📁 Структура проекта

```
s16-leads/
├── src/                          # 💻 Основной код
│   ├── infra/
│   │   ├── tele_client.py        # 🔌 Telegram клиент
│   │   └── limiter.py            # 🛡️ Anti-spam система
│   ├── core/
│   │   └── group_manager.py      # 👥 Управление группами
│   └── cli.py                    # 💻 CLI интерфейс
├── tests/                        # 🧪 Тесты (21 тест)
├── examples/                     # 📖 Примеры использования
├── docs/                         # 📚 Документация
│   ├── SECURITY.md              # 🔐 Безопасность
│   ├── ANTI_SPAM_PLAN.md        # 🛡️ Anti-spam документация
│   └── archive/                 # 📦 Архив выполненных задач
├── memory_bank/                  # 🧠 Memory Bank система
├── data/                         # 💾 Данные (игнорируется git)
│   ├── sessions/                # 🔑 Сессии Telegram
│   ├── export/                  # 📊 Экспорт данных
│   └── anti_spam/               # 🛡️ Счётчики anti-spam
├── .env.sample                   # 📝 Шаблон конфигурации
└── requirements.txt              # 📦 Зависимости
```

---

## 🧠 Memory Bank система

Проект использует продвинутую **Memory Bank** систему для управления задачами:

### Основные файлы:
- `memory_bank/tasks.md` - Активные задачи
- `memory_bank/activeContext.md` - Текущий контекст
- `memory_bank/progress.md` - Прогресс выполнения
- `memory_bank/projectbrief.md` - Описание проекта

### Архив задач:
- `docs/archive/` - Полные архивы выполненных задач
- Последняя задача: **Anti-Spam System** (Level 3, 1548+ строк кода)

---

## 🔧 Доступные команды

### Основные команды:
```bash
# Тестирование подключения
python3 src/infra/tele_client.py

# Просмотр чатов
python3 examples/list_my_chats.py

# Тестирование функций групп
python3 examples/test_group_functions.py

# Запуск тестов
pytest

# Проверка anti-spam статуса
make check-anti-spam  # если есть make
```

### Make команды (если установлен make):
```bash
make test          # Запуск тестов
make sync-env      # Синхронизация .env
make check-env     # Проверка конфигурации
```

---

## 🚨 Troubleshooting

### Проблема: "Permission denied" при первом запуске
```bash
chmod 600 data/sessions/*.session
```

### Проблема: "Module not found"
```bash
# Убедитесь что виртуальное окружение активировано
source venv/bin/activate
pip install -r requirements.txt
```

### Проблема: "FLOOD_WAIT" ошибки
Проект имеет встроенную anti-spam защиту, но если получаете ошибки:
- Уменьшите `RATE_RPS` в `.env` (например, до 2)
- Увеличьте паузы между операциями

### Проблема: "API_ID_INVALID"
- Проверьте правильность `TG_API_ID` и `TG_API_HASH` в `.env`
- Убедитесь что нет лишних пробелов

---

## 🎯 Что можно делать с проектом

### 📊 Базовые операции:
- Получение списков участников групп
- Поиск участников по критериям
- Экспорт данных в JSON/CSV
- Анализ активности пользователей

### 🔍 Продвинутые возможности:
- Массовая обработка групп
- Фильтрация по множественным критериям
- Автоматическая обработка FLOOD_WAIT ошибок
- Мониторинг квот и ограничений

### 🛡️ Безопасность:
- Автоматическое соблюдение лимитов Telegram
- Защита от блокировки аккаунта
- Умное управление паузами
- Логирование всех операций

---

## 📚 Дополнительная документация

### Для изучения кода:
1. **Начните с** `examples/` - примеры использования
2. **Изучите** `src/core/group_manager.py` - основная логика
3. **Посмотрите** `src/infra/limiter.py` - anti-spam система
4. **Читайте** `tests/` - понимание через тесты

### Для понимания архитектуры:
- `docs/archive/feature-anti-spam-system-20250720.md` - детальное описание anti-spam системы
- `memory_bank/projectbrief.md` - общее описание проекта
- `docs/SECURITY.md` - принципы безопасности

---

## 🚀 Следующие шаги

После успешной настройки ваш друг может:

1. **Изучить примеры** в папке `examples/`
2. **Протестировать** на небольших группах
3. **Настроить** параметры под свои нужды
4. **Расширить функционал** используя Memory Bank систему

### Для разработки:
```bash
# Установка dev зависимостей
pip install pytest pytest-asyncio pytest-mock

# Запуск тестов
pytest -v

# Проверка покрытия
pytest --cov=src tests/
```

---

## 🆘 Поддержка

При возникновении вопросов:

1. **Сначала** изучите документацию в `docs/`
2. **Проверьте** примеры в `examples/`
3. **Посмотрите** тесты в `tests/` - там много примеров использования
4. **Читайте** логи - проект логирует все важные события

### Полезные файлы для понимания:
- `README.md` - быстрый старт
- `docs/SECURITY.md` - безопасность
- `docs/archive/` - примеры выполненных задач
- `memory_bank/` - история разработки

---

**Удачи в использовании S16-Leads! 🚀**

> **Помните**: Проект готов к production использованию и протестирован на 386+ участниках с 100% success rate! 