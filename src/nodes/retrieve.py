"""Retrieve relevant policy chunks."""

from __future__ import annotations

from src.graph_state import AgentState, append_trace
from src.response_formatter import format_sources
from src.retriever import retrieve_documents


def retrieve_documents_node(state: AgentState) -> AgentState:
    documents = retrieve_documents(state["question"])
    sources = format_sources(documents)
    trace = append_trace(
        state,
        f"Step 2: Retrieved {len(documents)} document chunks",
    )
    return {
        **state,
        "retrieved_chunks": documents,
        "sources": sources,
        "workflow_trace": trace,
    }
