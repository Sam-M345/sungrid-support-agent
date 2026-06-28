"""Process env defaults — import before Chroma/LangChain (suppresses noisy telemetry)."""

from __future__ import annotations

import logging
import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"


def _quiet_chroma_telemetry_logs() -> None:
    """Chroma may still call a broken PostHog client; hide the error spam."""
    for name in (
        "chromadb.telemetry.product.posthog",
        "chromadb.telemetry.product",
        "posthog",
    ):
        logging.getLogger(name).setLevel(logging.CRITICAL)


_quiet_chroma_telemetry_logs()
