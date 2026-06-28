"""Format final structured response."""

from __future__ import annotations

from src.graph_state import AgentState, append_trace
from src.response_formatter import build_internal_note


def format_response(state: AgentState) -> AgentState:
    escalation_required = state.get("escalation_required", False)
    internal_note = build_internal_note(
        issue_type=state.get("intent", "General"),
        risk_level=state.get("risk_level", "Low"),
        confidence=int(state.get("confidence", 0)),
        sources=state.get("sources", []),
        recommended_action=state.get("recommended_action", "Review and respond."),
        escalation_required=escalation_required,
        validation_notes=state.get("validation_notes", ""),
    )

    if escalation_required:
        trace = append_trace(state, "Step 6: Escalation required")
    else:
        trace = append_trace(state, "Step 6: Returned answer to support rep")

    return {
        **state,
        "internal_note": internal_note,
        "workflow_trace": trace,
    }
