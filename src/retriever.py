"""Retrieve relevant document chunks for a customer question."""

from __future__ import annotations

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.vector_store import get_vector_store

DEFAULT_TOP_K = 4

SAFETY_KEYWORDS = (
    "burning",
    "smell",
    "smoke",
    "fire",
    "shock",
    "electrical shock",
    "exposed",
    "wiring",
    "wire",
    "tape",
    "spark",
    "overheat",
    "hot battery",
)

SAFETY_FILE = "safety_escalation_policy.md"


def _is_safety_query(query: str) -> bool:
    lowered = query.lower()
    return any(keyword in lowered for keyword in SAFETY_KEYWORDS)


def _dedupe_documents(documents: list[Document]) -> list[Document]:
    seen: set[tuple[str, str, int]] = set()
    unique: list[Document] = []
    for doc in documents:
        key = (
            doc.metadata.get("file_name", ""),
            doc.metadata.get("section_id", ""),
            doc.metadata.get("chunk_index", 0),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(doc)
    return unique


def retrieve_documents(
    query: str,
    vector_store: Chroma | None = None,
    top_k: int = DEFAULT_TOP_K,
) -> list[Document]:
    """Return top-k chunks; safety queries prioritize the safety policy doc."""
    store = vector_store or get_vector_store()
    fetch_k = max(top_k * 3, 12)

    if _is_safety_query(query):
        results = store.similarity_search(query, k=fetch_k)
        safety_docs = [
            doc for doc in results if doc.metadata.get("file_name") == SAFETY_FILE
        ]
        other_docs = [
            doc for doc in results if doc.metadata.get("file_name") != SAFETY_FILE
        ]
        merged = _dedupe_documents(safety_docs + other_docs)
        return merged[:top_k]

    results = store.max_marginal_relevance_search(
        query,
        k=top_k,
        fetch_k=fetch_k,
    )

    lowered = query.lower()
    if "warranty" in lowered and any(
        term in lowered for term in ("producing", "production", "energy", "panels")
    ):
        troubleshooting_hits = store.similarity_search(
            "low energy output checklist troubleshooting monitoring",
            k=2,
            filter={"file_name": "installation_troubleshooting_guide.md"},
        )
        results = _dedupe_documents(troubleshooting_hits + results)[:top_k]

    if "bill" in lowered and any(
        term in lowered for term in ("higher", "utility", "solar", "payment")
    ):
        billing_hits = store.similarity_search(
            "higher utility bill despite solar panels connection fee financing",
            k=2,
            filter={"file_name": "financing_faq.md"},
        )
        results = _dedupe_documents(billing_hits + results)[:top_k]

    return _dedupe_documents(results)


def format_chunk_for_display(doc: Document, rank: int) -> str:
    """Format a retrieved chunk for smoke-test or UI output."""
    source = doc.metadata.get("source", "Unknown")
    section_id = doc.metadata.get("section_id", "?")
    section_title = doc.metadata.get("section_title", "Unknown")
    preview = doc.page_content.replace("\n", " ").strip()
    preview = preview.encode("ascii", errors="replace").decode("ascii")
    if len(preview) > 180:
        preview = preview[:177] + "..."
    return (
        f"{rank}. {source} | Section {section_id} - {section_title}\n"
        f"   {preview}"
    )
