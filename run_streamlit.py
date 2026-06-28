"""Launch the Streamlit demo app.

VS Code: open this file and click Run (play button).
Opens http://localhost:8501 in your browser.
"""

from __future__ import annotations

import ensure_venv  # noqa: F401 — use project .venv when Play is clicked

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = Path(sys.executable)


if __name__ == "__main__":
    subprocess.run(
        [str(PYTHON), "-m", "streamlit", "run", str(ROOT / "app.py")],
        cwd=str(ROOT),
        check=False,
    )
