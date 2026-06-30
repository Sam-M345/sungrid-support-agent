"""Format structured graph output for CLI and Streamlit."""

from __future__ import annotations

import re

from langchain_core.documents import Document

CHEESY_PHRASE_PATTERNS = (
    r",?\s*and we(?:'|')?re glad you did!?",
    r",?\s*we are glad you did!?",
    r",?\s*we(?:'|')?re so glad you reached out!?",
    r",?\s*we are so glad you reached out!?",
    r",?\s*we(?:'|')?re happy you reached out!?",
    r",?\s*we are happy you reached out!?",
    r",?\s*we(?:'|')?re delighted you contacted us!?",
    r"\s*[—–-]\s*we(?:'|')?re glad you did!?",
    r"\s*[—–-]\s*we are glad you did!?",
)


NUMBERED_STEP_SPLIT = re.compile(r"(?<=[.!?])\s+(?=\d+\.\s)")


def _strip_step_marker(text: str) -> str:
    cleaned = re.sub(r"^\d+\.\s*", "", text.strip())
    cleaned = re.sub(r"^[-–—]+\s*", "", cleaned)
    return cleaned.strip()


def split_numbered_steps(action: str) -> list[str]:
    """Split rep guidance on list markers like '2. ' only after sentence endings."""
    if not action or not action.strip():
        return []

    text = action.strip()
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if len(lines) > 1 and all(re.match(r"^\d+\.\s", line) for line in lines):
        return [_strip_step_marker(line) for line in lines]

    text = re.sub(r"\s+", " ", text)
    if not re.search(r"\d+\.\s", text):
        return [text.strip()]

    parts = NUMBERED_STEP_SPLIT.split(text)
    steps: list[str] = []
    for part in parts:
        cleaned = _strip_step_marker(part)
        if cleaned:
            steps.append(cleaned)
    return steps or [text.strip()]


def _normalize_customer_paragraphs(text: str) -> str:
    """Capitalize the first letter of each paragraph when it starts lowercase."""
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    normalized: list[str] = []
    for part in parts:
        if part and part[0].islower():
            part = part[0].upper() + part[1:]
        normalized.append(part)
    return "\n\n".join(normalized)


def format_customer_response(text: str) -> str:
    """Normalize customer reply tone and add a paragraph break after the greeting."""
    if not text or not text.strip():
        return text

    cleaned = text.strip()
    for pattern in CHEESY_PHRASE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    cleaned = re.sub(r"\s+([.!?])", r"\1", cleaned)
    cleaned = re.sub(r"\s*[-—–]+\s*$", "", cleaned)

    if "\n\n" in cleaned:
        return _normalize_customer_paragraphs(cleaned)

    if not re.search(r"\bthank\b", cleaned, re.IGNORECASE):
        return cleaned

    dash_parts = re.split(r"\s*[—–-]\s+", cleaned, maxsplit=1)
    if len(dash_parts) == 2 and re.search(r"\bthank\b", dash_parts[0], re.IGNORECASE):
        greeting = dash_parts[0].strip().rstrip(",")
        if greeting[-1] not in ".!?":
            greeting += "."
        return _normalize_customer_paragraphs(f"{greeting}\n\n{dash_parts[1].strip()}")

    sentence_match = re.match(r"^(.+?[.!?])\s+(.+)$", cleaned, re.DOTALL)
    if sentence_match and re.search(r"\bthank\b", sentence_match.group(1), re.IGNORECASE):
        return _normalize_customer_paragraphs(
            f"{sentence_match.group(1).strip()}\n\n{sentence_match.group(2).strip()}"
        )

    body_match = re.match(
        r"^(Thank you.+?reaching out to us)\.?\s+([A-Z].+)$",
        cleaned,
        re.DOTALL | re.IGNORECASE,
    )
    if body_match:
        greeting = body_match.group(1).strip().rstrip(",")
        if greeting[-1] not in ".!?":
            greeting += "."
        return _normalize_customer_paragraphs(
            f"{greeting}\n\n{body_match.group(2).strip()}"
        )

    return cleaned


def format_sources(documents: list[Document]) -> list[str]:
    sources: list[str] = []
    seen: set[str] = set()
    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        section_id = doc.metadata.get("section_id", "?")
        section_title = doc.metadata.get("section_title", "Unknown")
        label = f"{source}, Section {section_id}, {section_title}"
        if label in seen:
            continue
        seen.add(label)
        sources.append(label)
    return sources


def build_internal_note(
    issue_type: str,
    risk_level: str,
    confidence: int,
    sources: list[str],
    recommended_action: str,
    escalation_required: bool,
    validation_notes: str = "",
) -> dict[str, str | int | bool | list[str]]:
    return {
        "issue_type": issue_type,
        "risk_level": risk_level,
        "confidence": confidence,
        "sources_used": sources,
        "recommended_action": recommended_action,
        "escalation_needed": escalation_required,
        "validation_notes": validation_notes,
    }


def build_final_response(state: dict) -> dict:
    return {
        "question": state.get("question", ""),
        "customer_response": state.get("customer_response", ""),
        "internal_note": state.get("internal_note", {}),
        "sources": state.get("sources", []),
        "risk_level": state.get("risk_level", "Low"),
        "confidence": state.get("confidence", 0),
        "escalation_required": state.get("escalation_required", False),
        "workflow_trace": state.get("workflow_trace", []),
        "retrieved_chunks": state.get("retrieved_chunks", []),
        "intent": state.get("intent", ""),
        "validation_notes": state.get("validation_notes", ""),
    }
