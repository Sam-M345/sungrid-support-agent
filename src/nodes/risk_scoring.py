"""Assign risk level and escalation recommendation."""

from __future__ import annotations

from src.graph_state import AgentState, append_trace


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
