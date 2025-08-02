# S16-Leads

Telegram-клиент для работы с лидами на базе Telethon с встроенной S16 конфигурацией и системой сверки участников.

## ✨ Новые возможности

### 🎯 **S16 Configuration System**
Специальная система для работы с экосистемой S16:
- **Референсная группа**: s16 space (автоконфигурация)
- **Сверка участников** между S16 группами  
- **Анализ пересечений** и поиск новых лидов
- **Production-ready**: протестировано на 259+ участниках

```bash
# Сверка участников S16 групп
PYTHONPATH=. python3 examples/s16_crosscheck.py -1002540509234 \
  --name "S16 Coliving DOMA" --output results.json

# Результат: 61.9% overlap, 38.1% new leads 
```

## 🚀 Быстрый старт

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd s16-leads
```

2. **Создайте виртуальное окружение:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте конфигурацию:**
```bash
cp .env.sample .env
# Отредактируйте .env файл, добавив ваши API ключи
```

5. **Протестируйте подключение:**
```bash
python3 src/infra/tele_client.py
```

## 🔐 Безопасность

**ВАЖНО:** Проект содержит конфиденциальные данные. Ознакомьтесь с [документацией по безопасности](docs/SECURITY.md).

### Ключевые моменты:
- ✅ API ключи хранятся в `.env` (не коммитится)
- ✅ Сессионные файлы в `data/sessions/` (защищено)
- ✅ Правильные права доступа на файлы
- ✅ Обработка ошибок аутентификации

## 📁 Структура проекта

```
s16-leads/
├── src/
│   ├── infra/
│   │   └── tele_client.py    # Telegram клиент
│   └── cli.py                # CLI интерфейс
├── data/sessions/            # Сессионные файлы
├── docs/
│   └── SECURITY.md           # Документация по безопасности
├── .env                      # Конфигурация (не коммитится)
├── .env.sample               # Шаблон конфигурации
└── requirements.txt          # Зависимости
```

## 🔧 CLI Команды

### Основные команды:
```bash
# Информация о группе
PYTHONPATH=. python3 src/cli.py info -1002188344480

# Получение участников
PYTHONPATH=. python3 src/cli.py participants -1002540509234 --limit 100

# Поиск участников
PYTHONPATH=. python3 src/cli.py search -1002540509234 --query "Dmitry"

# Экспорт участников
PYTHONPATH=. python3 src/cli.py export -1002540509234 --output data/export/members.json
```

### S16 специальные команды:
```bash
# Сверка участников с s16 space
PYTHONPATH=. python3 examples/s16_crosscheck.py -1002540509234 \
  --name "S16 Coliving DOMA" --output data/export/crosscheck.json

# Тестирование S16 конфигурации
PYTHONPATH=. python3 examples/test_s16_config.py

# Просмотр всех ваших чатов
PYTHONPATH=. python3 examples/list_my_chats.py
```

## 🛠️ Разработка

### Проверка безопасности:
```bash
# Проверка подключения
python3 src/infra/tele_client.py

# Проверка прав доступа
ls -la data/sessions/

# Проверка .gitignore
git status --ignored
```

## 🚚 Передача проекта

### Автоматическая подготовка к передаче

Для безопасной передачи проекта другому разработчику используйте специальный скрипт:

```bash
# Запустите скрипт подготовки
python3 scripts/prepare_for_transfer.py
```

Скрипт автоматически:
- 🔍 Найдет все конфиденциальные файлы
- 📁 Создаст чистую копию проекта  
- 🗜️ Создаст ZIP архив
- 📝 Добавит скрипт быстрой настройки
- 🛡️ Исключит все API ключи и сессии

### Что получит ваш друг:

1. **Полный проект** без конфиденциальных данных
2. **Подробное руководство** в `docs/TRANSFER_GUIDE.md`
3. **Скрипт быстрой настройки** `setup.sh`
4. **Примеры использования** в папке `examples/`

### Безопасная передача:

```bash
# 1. Подготовка проекта
python3 scripts/prepare_for_transfer.py

# 2. Отправка архива другу
# Отправьте созданный ZIP файл любым способом

# 3. Инструкции для друга
# Пусть читает docs/TRANSFER_GUIDE.md
```

### Полная документация по передаче:

📚 **[Подробное руководство по передаче](docs/TRANSFER_GUIDE.md)** - полная инструкция для вашего друга

## 📝 Лицензия

MIT License
