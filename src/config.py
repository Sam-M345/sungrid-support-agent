"""Environment and path configuration for SunGrid Support Agent."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
CHROMA_DIR = ROOT_DIR / ".chroma"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

load_dotenv(ROOT_DIR / ".env")

# See bootstrap_env.py — disables Chroma PostHog telemetry noise in dev
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _optional(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _optional_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    anthropic_model: str
    langchain_tracing_v2: bool
    langchain_api_key: str
    langchain_project: str
    langchain_endpoint: str
    docs_dir: Path
    chroma_dir: Path
    embedding_model: str


def load_settings() -> Settings:
    return Settings(
        anthropic_api_key=_require("ANTHROPIC_API_KEY"),
        anthropic_model=_optional("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        langchain_tracing_v2=_optional_bool("LANGCHAIN_TRACING_V2", False),
        langchain_api_key=_optional("LANGCHAIN_API_KEY"),
        langchain_project=_optional("LANGCHAIN_PROJECT", "sungrid-support-agent"),
        langchain_endpoint=_optional(
            "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
        ),
        docs_dir=DOCS_DIR,
        chroma_dir=CHROMA_DIR,
        embedding_model=EMBEDDING_MODEL,
    )


settings = load_settings()


def configure_langsmith() -> None:
    """Apply LangSmith tracing env vars when enabled."""
    if settings.langchain_tracing_v2 and settings.langchain_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
