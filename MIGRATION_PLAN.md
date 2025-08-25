# MIGRATION_PLAN

# Цель
Единая телеграм-сессия, несколько apps (S16, GConf, …), общее ядро tg_core: антиспам/лимитер, логгер, доступ к Telegram, конфиг, метрики. Любой app использует только публичный API tg_core.

# Границы и инварианты
- Не менять бизнес-логику apps/*; только раскладка и импорты
- Все Telethon-вызовы — через tg_core.TelegramGateway.safe_call
- Глобальный RPS-лимитер общий на всю сессию
- PII/секреты не в код/логи; .env.sample без секретов

# Партии (миграционный маршрут)
1) Scaffold ✅
   - Создать каркас: packages/tg_core/tg_core/{infra,domain,config}, packages/tg_core/tg_core/typing.py
   - Создать apps/s16-leads и tests/core/*
2) Move common ✅
   - Перенести общий код в tg_core: tele_client.py, limiter.py, group_manager.py
   - Добавить tg_core/infra/logging.py, tg_core/config/loader.py, tg_core/typing.py (скелеты)
3) App split ✅
   - src/cli.py → apps/s16-leads/cli.py
   - S16-скрипты из examples/ → apps/s16-leads/examples/ (или scripts/)
4) Fix imports ✅
   - Все импорты вида src.infra/*, src.core/* заменить на tg_core.*
   - Установить tg_core локально: `pip install -e packages/tg_core`
5) Tests & guardrails ✅
   - Базовые тесты лимитера/ретраев и сторожки:
     • core не импортирует apps
     • apps не используют Telethon напрямую

# Риски и смягчения
- Разъезд импортов → IMPORT_REWRITE.md + серийные коммиты
- Лимитер изменит поведение → sanity-тесты и лог-пробы RPS/FLOOD_WAIT
- Неявные зависимости → останов и вопросы (stop-условие)

# Откат
- Ветка pre-migration; rebase/merge-strategy: по партиям
- Revert конкретных коммитов step 2/4 при падении тестов

# Definition of Done
- apps/* собираются и работают на tg_core.*
- Все Telethon-вызовы проходят через safe_call
- Тесты зелёные; сторожки активны
- MIGRATION_PLAN.md / PROPOSED_TREE.md актуальны

# Next
- Apps skeletons: `apps/{s16leads,wildtantra,gconf,kuprianov,vahue}` ✅
- Observability: minimal metrics in `tg_core.infra.metrics` ✅
- CI: GitHub Actions pytest workflow ✅
- Versioning: `tg_core.__version__=0.1.0`, bump script
