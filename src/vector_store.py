"""Build and persist the Chroma vector store for SunGrid documents."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import settings
from src.document_loader import load_documents

HASH_FILE = "docs_hash.json"
COLLECTION_NAME = "sungrid_docs"
CHROMA_CLIENT_SETTINGS = Settings(anonymized_telemetry=False)


def _docs_fingerprint(docs_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(docs_dir.glob("*.md")):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _read_stored_hash(chroma_dir: Path) -> str | None:
    hash_path = chroma_dir / HASH_FILE
    if not hash_path.exists():
        return None
    try:
        payload = json.loads(hash_path.read_text(encoding="utf-8"))
        return payload.get("hash")
    except (json.JSONDecodeError, OSError):
        return None


def _write_stored_hash(chroma_dir: Path, fingerprint: str, chunk_count: int) -> None:
    chroma_dir.mkdir(parents=True, exist_ok=True)
    hash_path = chroma_dir / HASH_FILE
    hash_path.write_text(
        json.dumps({"hash": fingerprint, "chunk_count": chunk_count}, indent=2),
        encoding="utf-8",
    )


def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)


def build_vector_store(force_rebuild: bool = False) -> Chroma:
    """Create or load the Chroma store; rebuild when docs change."""
    docs_dir = settings.docs_dir
    chroma_dir = settings.chroma_dir
    fingerprint = _docs_fingerprint(docs_dir)
    stored_hash = _read_stored_hash(chroma_dir)

    embeddings = get_embeddings()

    if not force_rebuild and stored_hash == fingerprint and chroma_dir.exists():
        return Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(chroma_dir),
            client_settings=CHROMA_CLIENT_SETTINGS,
        )

    documents = load_documents(docs_dir)
    if chroma_dir.exists():
        import shutil

        shutil.rmtree(chroma_dir)

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(chroma_dir),
        client_settings=CHROMA_CLIENT_SETTINGS,
    )
    _write_stored_hash(chroma_dir, fingerprint, len(documents))
    return vector_store


def get_vector_store(force_rebuild: bool = False) -> Chroma:
    return build_vector_store(force_rebuild=force_rebuild)
