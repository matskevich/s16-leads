# Scope: project
# Priority: 60
# Архитектура (to-be)

Модель: монорепо с единым ядром (packages/tg_core) и несколькими приложениями (apps: s16-leads, gconf, …).

Правила:
- Любой доступ к Telegram — ТОЛЬКО через core (Gateway/safe_call), общий глобальный лимитер на сессию
- apps/* используют только публичный API core; импортов между apps нет
- Прикладную логику apps/* не переносить в core без ADR
- Выделение app в отдельный проект — зависимость от core по SemVer

Уточнения:
- Имя модуля выбрано: `tg_core` (импорты `from tg_core.*`).
- Экстракция app: вынос приложения — через git subtree/отдельный репозиторий; зависимость от core по SemVer.
- Public API core: зафиксированные экспортируемые поверхности — `TelegramGateway`, `RateLimiter`, `GroupManager`, `Settings`. В apps запрещено импортировать приватные детали.

Партии миграции (строго в порядке):
1) Scaffold: создать каркас packages/tg_core/tg_core/{infra,domain,config}, tg_core/typing.py; apps/s16-leads/*; tests/core/*
2) Move common: перенести tele_client.py, limiter.py, group_manager.py в tg_core; добавить tg_core/infra/logging.py, tg_core/config/loader.py, tg_core/typing.py
3) App split: src/cli.py → apps/s16-leads/cli.py; s16-скрипты из examples/ → apps/s16-leads/examples/
4) Fix imports: переписать `src.infra/*`, `src.core/*` → `tg_core.*`; установить tg_core локально (editable)
5) Tests & guardrails: базовые тесты на лимитер/ретраи; проверки — нет прямых Telethon в apps, core не импортирует apps

Стоп-условия:
- Любое расширение скопа за пределы партий — спросить
- Конфликт с .cursor/rules/70-telegram-invariants.md — спросить
