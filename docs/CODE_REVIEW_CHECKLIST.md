# 🔍 Code Review Checklist для S16-leads

## 🛡️ **КРИТИЧЕСКИЙ: Анти-спам проверки**

### ❗ **БЛОКИРУЮЩИЕ проверки (обязательно)**

- [ ] **🚨 Telegram API вызовы**
  - [ ] Все `client.*` вызовы используют `_safe_api_call()` или `safe_call()`
  - [ ] НЕТ прямых `await client.get_entity()`, `client.iter_participants()`, etc.
  - [ ] НЕТ прямых `async for user in client.iter_*()` без обертки
  
- [ ] **📥 Импорты**
  - [ ] Файлы с Telegram API импортируют `safe_call` или `_safe_api_call`
  - [ ] `from src.infra.limiter import safe_call` присутствует
  
- [ ] **🧪 Тесты**
  - [ ] Новые функции имеют тесты
  - [ ] Тесты НЕ используют прямые API вызовы (только моки)
  - [ ] Все тесты проходят: `make test`

### ⚡ **Автоматические проверки**

Запустите перед ревью:
```bash
# Быстрая проверка
make dev-check

# Полная проверка  
make check-all

# Специальный аудит Telegram API
make telegram-api-audit
```

---

## 📋 **GENERAL CODE REVIEW**

### **🏗️ Архитектура**

- [ ] **Слои разделены**
  - [ ] `src/core/` - бизнес логика
  - [ ] `src/infra/` - инфраструктура (Telegram, лимитеры)
  - [ ] `examples/` - примеры использования
  
- [ ] **Зависимости корректны**
  - [ ] Нет циклических импортов
  - [ ] Core не зависит от infra напрямую (только через интерфейсы)

### **🔒 Безопасность**

- [ ] **Персональные данные** 
  - [ ] НЕТ коммитов телефонов, token'ов, паролей
  - [ ] Используется `.env` для конфиденциальных данных
  - [ ] Personal data помечена в комментариях

- [ ] **API ключи**
  - [ ] Все secrets в `.env.sample` как примеры
  - [ ] НЕТ hardcoded API keys/tokens

### **📊 Производительность**

- [ ] **Rate Limiting**
  - [ ] Большие операции используют `smart_pause()`
  - [ ] Batch операции имеют лимиты (не более 1000 за раз)
  
- [ ] **Обработка ошибок**
  - [ ] `try/except` для Telegram API
  - [ ] `FloodWaitError` обрабатывается корректно
  - [ ] Логирование ошибок присутствует

### **📝 Качество кода**

- [ ] **Стиль кода**
  - [ ] Форматирование: `make format-check` ✅
  - [ ] Линтинг: `make lint` ✅
  - [ ] Naming conventions соблюдены
  
- [ ] **Документация**
  - [ ] Docstrings для всех public функций
  - [ ] Комментарии для сложной логики
  - [ ] README обновлен при необходимости

### **🧪 Тестирование**

- [ ] **Покрытие тестами**
  - [ ] Новые функции имеют unit тесты
  - [ ] Тесты покрывают happy path и edge cases
  - [ ] Mock'и используются правильно
  
- [ ] **Интеграционные тесты**
  - [ ] Критические flow имеют интеграционные тесты
  - [ ] Тесты НЕ требуют real Telegram connection

---

## 🚨 **КРАСНЫЕ ФЛАГИ (немедленный reject)**

### ❌ **БЛОКИРУЮЩИЕ проблемы**

1. **Прямые Telegram API вызовы без safe_call**
   ```python
   # ❌ НЕ ТАК
   await client.get_entity("@group")
   async for user in client.iter_participants():
   
   # ✅ ПРАВИЛЬНО  
   await _safe_api_call(client.get_entity, "@group")
   await safe_call(client.get_entity, "@group", operation_type="api")
   ```

2. **Коммит персональных данных**
   ```json
   // ❌ НЕ ТАК
   {"phone": "+1234567890", "api_id": "12345"}
   
   // ✅ ПРАВИЛЬНО
   // Personal data excluded from commit
   ```

3. **Hardcoded secrets**
   ```python
   # ❌ НЕ ТАК
   API_ID = "12345"
   API_HASH = "abcdef123456"
   
   # ✅ ПРАВИЛЬНО
   API_ID = os.getenv("API_ID")
   ```

4. **Broken tests**
   - Если `make test` падает - немедленный reject

---

## ✅ **ПРОЦЕДУРА REVIEW**

### **👨‍💻 Для автора PR:**

1. **Перед созданием PR:**
   ```bash
   # Самопроверка
   make dev-check
   make test
   make anti-spam-check
   ```

2. **В описании PR указать:**
   - [ ] Checklist пройден ✅
   - [ ] Анти-спам проверки прошли ✅ 
   - [ ] Тесты добавлены/обновлены ✅
   - [ ] Breaking changes описаны

### **👥 Для reviewer:**

1. **Автоматические проверки:**
   ```bash
   git checkout feature-branch
   make check-all
   ```

2. **Ручная проверка:**
   - [ ] Архитектура соответствует принципам
   - [ ] Код читаемый и поддерживаемый
   - [ ] Нет code smells
   
3. **Специальные проверки:**
   ```bash
   # Поиск прямых API вызовов
   grep -r "await.*client\." --include="*.py" . | grep -v safe_call
   
   # Проверка imports
   grep -r "from telethon" --include="*.py" .
   ```

### **🎯 Критерии одобрения:**

- ✅ Все автоматические проверки проходят
- ✅ Нет блокирующих проблем  
- ✅ Код следует architectural patterns
- ✅ Тесты добавлены и проходят
- ✅ Документация обновлена

---

## 📞 **В случае проблем:**

### **🚨 Если найдены анти-спам нарушения:**

1. **Запустить диагностику:**
   ```bash
   make telegram-api-audit
   python scripts/check_anti_spam_compliance.py
   ```

2. **Типичные исправления:**
   ```python
   # Исправление get_entity
   - await client.get_entity(group_id)
   + await _safe_api_call(client.get_entity, group_id)
   
   # Исправление iter_participants  
   - async for user in client.iter_participants(group):
   + async def get_users():
   +     users = []
   +     async for user in client.iter_participants(group):
   +         users.append(user)
   +     return users
   + users = await _safe_api_call(get_users)
   ```

3. **Добавить import если нужно:**
   ```python
   from src.infra.limiter import safe_call, smart_pause
   # или для group_manager.py
   # использовать уже существующий _safe_api_call
   ```

### **❓ Если сомневаетесь:**

- Запустите `make telegram-api-audit` 
- Проверьте `docs/ANTI_SPAM_AUDIT_REPORT.md`
- Консультируйтесь с lead developer

---

**🎯 Цель:** Обеспечить 100% защиту от Telegram API блокировок при сохранении функциональности и качества кода.