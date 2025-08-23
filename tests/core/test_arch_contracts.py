import pkgutil
import sys
from pathlib import Path


def test_tg_core_does_not_import_apps():
    # make sure tg_core is importable
    sys.path.append(str(Path(__file__).resolve().parents[2] / "packages" / "tg_core"))
    import tg_core  # noqa: F401

    # ensure no module named apps.* is imported as dependency of tg_core
    imported_apps = [name for _, name, _ in pkgutil.iter_modules() if name.startswith("apps")]
    assert not imported_apps, "tg_core must not import apps.*"


def test_apps_have_no_direct_telethon_imports():
    apps_dir = Path(__file__).resolve().parents[2] / "apps"
    offenders = []
    for path in apps_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "import telethon" in text or "from telethon import" in text:
            offenders.append(str(path))
    assert offenders == [], f"apps must not import telethon directly: {offenders}"


