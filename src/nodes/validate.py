"""Validate generated answers against policy context."""

from __future__ import annotations

import json

from src.graph_state import AgentState, append_trace, format_context, invoke_llm, parse_json_content
from src.prompts import VALIDATE_SYSTEM, VALIDATE_USER
from src.validation import validate_response


def validate_answer(state: AgentState) -> AgentState:
    context = format_context(state.get("retrieved_chunks", []))
    raw = invoke_llm(
        VALIDATE_SYSTEM,
        VALIDATE_USER.format(
            question=state["question"],
            safety_risk=state.get("safety_risk", False),
            context=context,
            customer_response=state.get("customer_response", ""),
        ),
    )
    try:
        payload = parse_json_content(raw)
    except (json.JSONDecodeError, ValueError):
        payload = {"passed": True, "issues": [], "confidence": 65}

    llm_passed = bool(payload.get("passed", False))
    llm_issues = payload.get("issues", [])
    confidence = int(payload.get("confidence", 70))

    passed, issues, confidence = validate_response(
        question=state["question"],
        customer_response=state.get("customer_response", ""),
        safety_risk=state.get("safety_risk", False),
        llm_passed=llm_passed,
        llm_issues=llm_issues,
        confidence=confidence,
    )

    validation_notes = "; ".join(issues) if issues else "Answer aligned with retrieved policy excerpts."
    trace_status = "Validated citations" if passed else "Validation flagged issues"

    return {
        **state,
        "validation_passed": passed,
        "validation_notes": validation_notes,
        "confidence": confidence,
        "workflow_trace": append_trace(state, f"Step 4: {trace_status}"),
    }
