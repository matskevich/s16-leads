# IMPORT_REWRITE

## Импорт-правила (old → new)

from src.infra.limiter import ...        → from tg_core.infra.limiter import ...
from src.infra.tele_client import ...    → from tg_core.infra.tele_client import ...
from src.core.group_manager import ...   → from tg_core.domain.groups import ...

## Запрет прямых Telethon
import telethon
from telethon import ...                 → заменить на:
from tg_core.infra.tele_client import TelegramGateway
# и оборачивать вызовы через gateway.safe_call

## Поиск/замена (шаблоны)
FIND:  from src\.infra\.limiter import (.*)
REPL:  from tg_core.infra.limiter import \1

FIND:  from src\.infra\.tele_client import (.*)
REPL:  from tg_core.infra.tele_client import \1

FIND:  from src\.core\.group_manager import (.*)
REPL:  from tg_core.domain.groups import \1

## Примечания
- После move — установить tg_core локально: `pip install -e packages/tg_core`
- Проверить, что tg_core не импортирует apps (см. test_arch_contracts.py)


