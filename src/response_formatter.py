"""Format structured graph output for CLI and Streamlit."""

from __future__ import annotations

from langchain_core.documents import Document


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
