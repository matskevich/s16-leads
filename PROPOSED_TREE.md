# PROPOSED_TREE

Целевое дерево папок/файлов.

```text
packages/
  tg_core/
    tg_core/
      infra/
        tele_client.py
        limiter.py
        logging.py
        monitors.py   # опционально
      domain/
        groups.py
      config/
        loader.py
      typing.py
    pyproject.toml
apps/
  s16-leads/
    cli.py
    app/
      config.py       # бывший s16_config.py
    examples/         # бывшие examples/, относящиеся к S16
tests/
  core/
    test_limiter.py
    test_arch_contracts.py
docs/
  HELLO_AGENT.md
MIGRATION_PLAN.md
PROPOSED_TREE.md
MOVE_MAP.md
IMPORT_REWRITE.md
```


