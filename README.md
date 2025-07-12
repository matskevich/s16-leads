# S16-Leads

Telegram-клиент для работы с лидами на базе Telethon.

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

## 📝 Лицензия

MIT License
