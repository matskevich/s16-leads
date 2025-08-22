# Scope: project
# Priority: 70
# Telegram-инварианты (MUST)

MUST:
- Все Telethon-вызовы — через tg_core.TelegramGateway.safe_call
- FLOOD_WAIT: обязательный экспоненциальный backoff; единый RPS-лимит на сессию (лимитер tg_core) не обходить
- Единый структурный логгер tg_core (опц. JSON); PII не логировать
- Базовые тесты на лимитер/ретраи — зелёные; изменения, ломающие их, запрещены

NEVER:
- Прямые Telethon-вызовы из apps/*
- Вшивать ключи/ID/сессии в код/логи

SHOULD:
- Хранить .session вне VCS; .env.sample — без секретов

SLO:
- Не снижать производительность >10% от текущих показателей без одобренного ADR.

Observability (метрики):
- rate_limit_requests_total — количество запросов, прошедших через лимитер
- rate_limit_throttled_total — количество запросов, задержанных/отклонённых лимитером
- flood_wait_events_total — количество событий FLOOD_WAIT (по уровням)
- tele_call_latency_seconds (histogram) — задержка вызовов к Telegram API
