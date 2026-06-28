"""Generate customer-ready and internal draft responses."""

from __future__ import annotations

from src.graph_state import AgentState, append_trace, format_context, invoke_llm, parse_sections
from src.prompts import (
    GENERATE_SYSTEM,
    GENERATE_USER,
    SAFETY_GENERATE_SYSTEM,
    SAFETY_GENERATE_USER,
)


def generate_answer(state: AgentState) -> AgentState:
    context = format_context(state.get("retrieved_chunks", []))
    question = state["question"]

    if state.get("safety_risk"):
        raw = invoke_llm(
            SAFETY_GENERATE_SYSTEM,
            SAFETY_GENERATE_USER.format(question=question, context=context),
        )
        trace_msg = "Step 3: Generated limited safe response"
    else:
        raw = invoke_llm(
            GENERATE_SYSTEM,
            GENERATE_USER.format(
                question=question,
                intent=state.get("intent", ""),
                context=context,
            ),
        )
        trace_msg = "Step 3: Generated grounded answer"

    customer_response, internal_body = parse_sections(raw)
    recommended_action = internal_body or "Review draft and respond to homeowner."

    if "Recommended action:" in recommended_action:
        recommended_action = recommended_action.split("Recommended action:", 1)[-1].strip()

    return {
        **state,
        "customer_response": customer_response,
        "recommended_action": recommended_action,
        "workflow_trace": append_trace(state, trace_msg),
    }
