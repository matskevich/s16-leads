import pkgutil
import sys
from pathlib import Path


def test_tg_core_does_not_import_apps():
    # make sure tg_core is importable
    sys.path.append(str(Path(__file__).resolve().parents[2] / "packages" / "tg_core"))

    before = set(sys.modules.keys())
    import tg_core  # noqa: F401
    after = set(sys.modules.keys())

    # modules loaded as a result of importing tg_core
    newly_loaded = after - before
    offenders = [m for m in newly_loaded if m.startswith("apps.")]
    assert offenders == [], f"tg_core import must not pull apps.* modules: {offenders}"


def test_apps_have_no_direct_telethon_imports():
    apps_dir = Path(__file__).resolve().parents[2] / "apps"
    offenders = []
    for path in apps_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "import telethon" in text or "from telethon import" in text:
            offenders.append(str(path))
    assert offenders == [], f"apps must not import telethon directly: {offenders}"


