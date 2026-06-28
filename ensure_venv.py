"""Ensure root runners use the project .venv (fixes VS Code play button)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"


def ensure_venv() -> None:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    if not VENV_PYTHON.exists():
        return

    if Path(sys.executable).resolve() == VENV_PYTHON.resolve():
        return

    raise SystemExit(subprocess.call([str(VENV_PYTHON), *sys.argv]))


ensure_venv()
