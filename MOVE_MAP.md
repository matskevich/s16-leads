# MOVE_MAP

## File → File

src/infra/tele_client.py      → packages/tg_core/tg_core/infra/tele_client.py
src/infra/limiter.py          → packages/tg_core/tg_core/infra/limiter.py
src/core/group_manager.py     → packages/tg_core/tg_core/domain/groups.py
src/core/s16_config.py        → apps/s16-leads/app/config.py    # app-специфика, не в core
src/cli.py                    → apps/s16-leads/cli.py

## Dirs → Dirs (по содержанию)
examples/ (S16-специфичные)   → apps/s16-leads/examples/

## New files (скелеты)
packages/tg_core/tg_core/infra/logging.py
packages/tg_core/tg_core/config/loader.py
packages/tg_core/tg_core/typing.py

## Удаления/чистки
— старые путевые импорты src.* после переписывания импортов


