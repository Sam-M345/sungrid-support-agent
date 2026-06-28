"""SunGrid Support Agent — recruiter-friendly Streamlit demo."""

from __future__ import annotations

import streamlit as st

from src.graph import build_graph, invoke_agent
from src.vector_store import get_vector_store

DISCLAIMER = (
    "Demo note: This is a synthetic portfolio project using fictional company "
    "documents. Not real solar, warranty, safety, or financial advice."
)

SAMPLE_QUESTIONS = [
    (
        "Warranty + production",
        "My panels are producing about 35% less energy than expected. "
        "Is this covered under warranty?",
    ),
    (
        "Monitoring app",
        "My monitoring app stopped showing production data. "
        "Does that mean my system is broken?",
    ),
    (
        "Safety: burning smell",
        "I smell something burning near the inverter. What should I do?",
    ),
    (
        "Financing cancellation",
        "Can I cancel my solar financing agreement after installation?",
    ),
    (
        "Storm + inverter error",
        "My inverter is showing an error code after a storm. Should I reset it?",
    ),
    (
        "Higher utility bill",
        "My bill is higher than expected even though I have solar panels. Why?",
    ),
    (
        "Safety: exposed wires",
        "There are exposed wires near the panel connection box. "
        "Can I tape them myself?",
    ),
    (
        "Warranty claim docs",
        "What information do I need before starting a warranty claim?",
    ),
]

DEFAULT_QUESTION = SAMPLE_QUESTIONS[0][1]


@st.cache_resource(show_spinner="Loading knowledge base...")
def load_resources():
    vector_store = get_vector_store()
    workflow = build_graph()
    return vector_store, workflow


def render_header() -> None:
    st.title("SunGrid Support Agent")
    st.markdown(
        "Helps solar **customer support reps** answer homeowner questions using "
        "synthetic company documents, **RAG**, **LangGraph** workflow routing, "
        "and **risk-based escalation**."
    )
    st.caption(DISCLAIMER)


def render_sidebar() -> None:
    st.sidebar.header("About this demo")
    st.sidebar.markdown(
        "- **User:** SunGrid customer support rep  \n"
        "- **Input:** Homeowner question  \n"
        "- **Output:** Draft reply, internal note, sources, workflow trace  \n"
        "- **Why not a generic chatbot:** Answers are grounded in internal policy docs"
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Stack:** Claude, LangChain, LangGraph, Chroma, LangSmith")


def render_sample_questions() -> None:
    st.subheader("Sample homeowner questions")
    st.caption("Click a sample to load it below, then run the assistant.")

    cols = st.columns(2)
    for index, (label, question) in enumerate(SAMPLE_QUESTIONS):
        column = cols[index % 2]
        if column.button(label, key=f"sample_btn_{index}", use_container_width=True):
            st.session_state["question_input"] = question


def render_results(result: dict) -> None:
    risk_level = result.get("risk_level", "Low")
    escalation_required = result.get("escalation_required", False)
    is_high_risk = risk_level == "High"

    st.subheader("Results")

    metric_cols = st.columns(4)
    metric_cols[0].metric("Risk level", risk_level)
    metric_cols[1].metric("Confidence", f"{result.get('confidence', 0)}%")
    metric_cols[2].metric("Escalation", "Yes" if escalation_required else "No")
    metric_cols[3].metric("Sources", len(result.get("sources", [])))

    if is_high_risk:
        st.error(
            "High-risk case: remote troubleshooting is stopped. "
            "Escalate to a qualified technician."
        )

    st.markdown("#### Customer-ready response")
    st.info(result.get("customer_response", ""))

    note = result.get("internal_note", {})
    st.markdown("#### Internal support note")
    st.markdown(
        f"""
| Field | Value |
|---|---|
| **Issue type** | {note.get("issue_type", result.get("intent", ""))} |
| **Risk level** | {note.get("risk_level", risk_level)} |
| **Confidence** | {note.get("confidence", result.get("confidence", 0))}% |
| **Recommended action** | {note.get("recommended_action", "")} |
| **Escalation needed** | {"Yes" if note.get("escalation_needed", escalation_required) else "No"} |
        """
    )

    if note.get("validation_notes"):
        st.caption(f"Validation: {note.get('validation_notes')}")

    st.markdown("#### Sources used")
    sources = result.get("sources", [])
    if sources:
        for index, source in enumerate(sources, start=1):
            st.markdown(f"{index}. {source}")
    else:
        st.write("No sources returned.")

    st.markdown("#### Workflow trace")
    for step in result.get("workflow_trace", []):
        st.markdown(f"- {step}")

    with st.expander("View retrieved context"):
        chunks = result.get("retrieved_chunks", [])
        if not chunks:
            st.write("No retrieved chunks.")
            return
        for index, chunk in enumerate(chunks, start=1):
            metadata = chunk.metadata
            st.markdown(
                f"**[{index}] {metadata.get('source', 'Unknown')} | "
                f"Section {metadata.get('section_id', '?')} - "
                f"{metadata.get('section_title', 'Unknown')}**"
            )
            st.code(chunk.page_content, language="markdown")


def main() -> None:
    st.set_page_config(
        page_title="SunGrid Support Agent",
        page_icon="☀️",
        layout="wide",
    )

    if "question_input" not in st.session_state:
        st.session_state["question_input"] = DEFAULT_QUESTION

    render_sidebar()
    render_header()
    render_sample_questions()

    st.subheader("Ask a homeowner question")
    question = st.text_area(
        "Homeowner question",
        key="question_input",
        height=120,
        placeholder="Example: My monitoring app stopped showing production data...",
    )

    run_clicked = st.button("Run SunGrid Support Agent", type="primary")

    if run_clicked:
        trimmed = question.strip()
        if not trimmed:
            st.warning("Enter a homeowner question or click a sample question first.")
        else:
            _, workflow = load_resources()
            with st.spinner("Running LangGraph workflow..."):
                st.session_state["last_result"] = invoke_agent(trimmed, app=workflow)

    if "last_result" in st.session_state:
        st.markdown("---")
        render_results(st.session_state["last_result"])


if __name__ == "__main__":
    main()
