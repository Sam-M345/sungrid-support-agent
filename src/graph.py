"""LangGraph workflow for SunGrid Support Agent."""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from src.graph_state import AgentState
from src.nodes.classify import classify_intent
from src.nodes.format_response import format_response
from src.nodes.generate import generate_answer
from src.nodes.retrieve import retrieve_documents_node
from src.nodes.risk_scoring import risk_scoring
from src.nodes.validate import validate_answer
from src.response_formatter import build_final_response


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_documents", retrieve_documents_node)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("validate_answer", validate_answer)
    graph.add_node("risk_scoring", risk_scoring)
    graph.add_node("format_response", format_response)

    graph.set_entry_point("classify_intent")
    graph.add_edge("classify_intent", "retrieve_documents")
    graph.add_edge("retrieve_documents", "generate_answer")
    graph.add_edge("generate_answer", "validate_answer")
    graph.add_edge("validate_answer", "risk_scoring")
    graph.add_edge("risk_scoring", "format_response")
    graph.add_edge("format_response", END)

    return graph.compile()


def invoke_agent(question: str, app=None) -> dict:
    """Run the support agent workflow for a homeowner question."""
    workflow = app or build_graph()
    initial_state: AgentState = {
        "question": question,
        "intent": "",
        "intents": [],
        "safety_risk": False,
        "retrieved_chunks": [],
        "sources": [],
        "customer_response": "",
        "internal_note": {},
        "recommended_action": "",
        "risk_level": "Low",
        "confidence": 0,
        "escalation_required": False,
        "workflow_trace": [],
        "validation_notes": "",
        "validation_passed": True,
    }
    final_state = workflow.invoke(initial_state)
    return build_final_response(final_state)


def run_agent(question: str) -> dict:
    """Backward-compatible entry point."""
    return invoke_agent(question)
