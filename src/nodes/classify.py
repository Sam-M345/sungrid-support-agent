"""Classify homeowner question intent and safety risk."""

from __future__ import annotations

import json

from src.graph_state import AgentState, append_trace, invoke_llm, parse_json_content
from src.prompts import CLASSIFY_SYSTEM
from src.retriever import _is_safety_query


def classify_intent(state: AgentState) -> AgentState:
    question = state["question"]
    safety_risk = _is_safety_query(question)

    raw = invoke_llm(
        CLASSIFY_SYSTEM,
        f"Classify this homeowner question:\n{question}",
    )
    try:
        payload = parse_json_content(raw)
    except (json.JSONDecodeError, ValueError):
        payload = {"intents": ["troubleshooting"], "reasoning": "Fallback classification"}

    intents = payload.get("intents", [])
    if safety_risk and "safety" not in intents:
        intents.append("safety")

    if not intents:
        intents = ["troubleshooting"]

    intent_label = " + ".join(intents)
    trace = append_trace(
        state,
        f"Step 1: Classified as {intent_label}"
        + (" (Safety Risk)" if safety_risk else ""),
    )

    return {
        **state,
        "intents": intents,
        "intent": intent_label,
        "safety_risk": safety_risk,
        "workflow_trace": trace,
    }
