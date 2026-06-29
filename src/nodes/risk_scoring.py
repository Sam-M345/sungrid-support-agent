"""Assign risk level and escalation recommendation."""

from __future__ import annotations

import re

from src.graph_state import AgentState, append_trace


def _sentence_bounds(text: str, pos: int) -> tuple[int, int]:
    start = text.rfind(".", 0, pos) + 1
    end = text.find(".", pos)
    if end == -1:
        end = len(text)
    return start, end


def _action_requires_handoff(action: str) -> bool:
    """True when rep-facing steps require handing off to another team now."""
    lower = action.lower()

    if re.search(r"\bdispatch\b", lower) and not re.search(r"do not dispatch", lower):
        return True
    if re.search(r"\bsafety\s+dispatch\b", lower):
        return True
    if "escalate immediately" in lower:
        return True

    for match in re.finditer(r"\bescalat\w*\s+(?:to|per)\b", lower):
        start, end = _sentence_bounds(lower, match.start())
        sentence = lower[start:end].strip()
        if re.search(r"\bif\b.+\bescalat", sentence):
            continue
        if re.search(r"\bescalat\w*\s+(?:to|per)\b.+\bonly if\b", sentence):
            continue
        if re.search(r"\bdo not escalat", sentence):
            continue
        return True
    return False


def risk_scoring(state: AgentState) -> AgentState:
    safety_risk = state.get("safety_risk", False)
    validation_passed = state.get("validation_passed", True)
    confidence = int(state.get("confidence", 70))
    intents = state.get("intents", [])

    if safety_risk:
        risk_level = "High"
        escalation_required = True
    elif not validation_passed or confidence < 60:
        risk_level = "Medium"
        escalation_required = True
    elif "financing" in intents:
        risk_level = "Medium"
        escalation_required = False
    elif "warranty" in intents and "troubleshooting" in intents:
        risk_level = "Medium"
        escalation_required = False
    else:
        risk_level = "Low"
        escalation_required = False

    recommended_action = state.get("recommended_action", "")
    if not escalation_required and _action_requires_handoff(recommended_action):
        escalation_required = True
        if risk_level == "Low":
            risk_level = "Medium"

    if safety_risk:
        trace = append_trace(state, "Step 5: Risk level High - Escalation required")
    elif escalation_required:
        trace = append_trace(
            state,
            f"Step 5: Risk level {risk_level} - Escalation recommended",
        )
    else:
        trace = append_trace(
            state,
            f"Step 5: Risk level {risk_level} - Escalation: Not immediate",
        )

    return {
        **state,
        "risk_level": risk_level,
        "escalation_required": escalation_required,
        "workflow_trace": trace,
    }
