"""Assign risk level and escalation recommendation."""

from __future__ import annotations

import re

from src.graph_state import AgentState, append_trace


from src.response_formatter import split_numbered_steps


def _action_steps(action: str) -> list[str]:
    """Split numbered rep guidance into individual steps."""
    steps = split_numbered_steps(action)
    return steps or [action.strip()]


def _step_requires_handoff(step: str) -> bool:
    lower = step.lower()
    if re.search(r"\bif\b", lower):
        return False
    if re.search(r"\bonly if\b", lower):
        return False
    if re.search(r"\bdo not (?:escalat|dispatch)", lower):
        return False
    if re.search(r"\bescalat\w*\s+(?:to|per)\b", lower):
        return True
    if re.search(r"\bdispatch\b", lower):
        return True
    return False


def _action_requires_handoff(action: str) -> bool:
    """True when rep-facing steps require handing off to another team now."""
    lower = action.lower()

    if re.search(r"\bsafety\s+dispatch\b", lower):
        return True
    if "escalate immediately" in lower:
        return True

    return any(_step_requires_handoff(step) for step in _action_steps(action))


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
