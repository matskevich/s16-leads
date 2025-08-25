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


def test_apps_do_not_import_each_other():
    apps_dir = Path(__file__).resolve().parents[2] / "apps"
    offenders = []
    for app_dir in [p for p in apps_dir.iterdir() if p.is_dir()]:
        app_name = app_dir.name
        for py in app_dir.rglob("*.py"):
            text = py.read_text(encoding="utf-8")
            # forbid imports like from apps.<other>.app ...
            if "from apps." in text and f"from apps.{app_name}." not in text:
                offenders.append(str(py))
    assert offenders == [], f"cross-app imports are forbidden: {offenders}"


def test_no_sys_path_append_in_code():
    repo = Path(__file__).resolve().parents[2]
    offenders = []
    for path in repo.rglob("*.py"):
        # skip tests and scripts
        rel = path.relative_to(repo)
        if str(rel).startswith("tests/") or str(rel).startswith("scripts/"):
            continue
        text = path.read_text(encoding="utf-8")
        if "sys.path.append(" in text:
            offenders.append(str(rel))
    assert offenders == [], f"sys.path hacks forbidden in code: {offenders}"


