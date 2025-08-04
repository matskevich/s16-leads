# 🚀 Быстрый старт: Анти-спам система S16-leads

## 🎯 **Для новых разработчиков**

### ⚡ **Установка (одна команда)**

```bash
python scripts/setup_anti_spam_system.py
```

Эта команда автоматически:
- ✅ Устанавливает все зависимости
- ✅ Настраивает pre-commit hooks
- ✅ Проверяет весь код на анти-спам соответствие
- ✅ Запускает все тесты

---

## 🛡️ **ГЛАВНОЕ ПРАВИЛО**

> **Каждый Telegram API вызов ДОЛЖЕН использовать анти-спам обертку**

```python
# ❌ НЕ ТАК
await client.get_entity(user_id)
async for user in client.iter_participants(group):

# ✅ ПРАВИЛЬНО
await _safe_api_call(client.get_entity, user_id)
await safe_call(client.get_entity, user_id, operation_type="api")
```

---

## 🔧 **Ежедневные команды**

### **Перед коммитом:**
```bash
make dev-check
```

### **Проверка анти-спам:**
```bash
make anti-spam-check
```

### **Полная проверка:**
```bash
make check-all
```

---

## 📋 **Шаблоны для новых функций**

### **Простая API функция:**
```python
async def new_function(self, param: str) -> Optional[Dict]:
    try:
        result = await _safe_api_call(self.client.your_method, param)
        return self._process_result(result) if result else None
    except Exception as e:
        logger.error(f"Error in new_function: {e}")
        return None
```

### **Bulk операция:**
```python
async def bulk_function(self, items: List[str]) -> List[Dict]:
    async def process_bulk():
        results = []
        for i, item in enumerate(items):
            async for result in self.client.iter_something(item):
                results.append(result)
                if (i + 1) % 100 == 0:
                    await smart_pause("bulk_operation", i + 1)
        return results
    
    return await _safe_api_call(process_bulk)
```

---

## 🚨 **Если что-то сломалось**

### **Проблема: Pre-commit блокирует коммит**
```bash
# Исправить автоматически:
make format

# Проверить что исправлено:
make dev-check
```

### **Проблема: Анти-спам проверка падает**
```bash
# Посмотреть детали:
python scripts/check_anti_spam_compliance.py

# Запустить аудит:
make telegram-api-audit
```

### **Проблема: Тесты падают**
```bash
# Запустить отдельно:
make test

# Verbose output:
PYTHONPATH=. python -m pytest tests/ -v -s
```

---

## 📚 **Документация**

1. 📋 **[Code Review Checklist](CODE_REVIEW_CHECKLIST.md)** - обязательно к прочтению
2. 🏗️ **[Telegram API Patterns](TELEGRAM_API_PATTERNS.md)** - архитектурные паттерны  
3. 🛡️ **[Anti-spam Audit Report](ANTI_SPAM_AUDIT_REPORT.md)** - подробный отчет по системе

---

## ❓ **FAQ**

### **Q: Можно ли использовать прямые client.* вызовы в тестах?**
A: Да, в тестах используются моки, анти-спам проверки автоматически отключаются.

### **Q: Что делать если нужно добавить новый API метод?**
A: Используйте паттерн `_safe_api_call()` или `safe_call()` + изучите существующие примеры.

### **Q: Как часто запускать проверки?**
A: Pre-commit hooks делают это автоматически. Дополнительно запускайте `make telegram-api-audit` раз в неделю.

### **Q: Можно ли отключить анти-спам проверки?**
A: Нет. Это критически важно для защиты от блокировок Telegram.

---

## 🎯 **Успешная разработка = всегда зеленые проверки!**

```bash
make check-all  # Должно быть всегда ✅
```