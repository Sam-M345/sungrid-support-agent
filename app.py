"""SunGrid Support Agent — recruiter-friendly Streamlit demo."""

from __future__ import annotations

import streamlit as st

from src.graph import build_graph, invoke_agent
from src.vector_store import get_vector_store

DISCLAIMER = (
    "Synthetic portfolio demo — fictional company documents only. "
    "Not real solar, warranty, safety, or financial advice."
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

DEFAULT_QUESTION = SAMPLE_QUESTIONS[4][1]  # Storm + inverter — good general demo

WORKFLOW_CODE_SNIPPETS = [
    {
        "node": "classify_intent",
        "file": "src/nodes/classify.py",
        "code": (
            "safety_risk = _is_safety_query(question)\n"
            'raw = invoke_llm(CLASSIFY_SYSTEM, f"Classify this homeowner question:\\n{question}")\n'
            "intents = payload.get('intents', [])\n"
            'intent_label = " + ".join(intents)'
        ),
    },
    {
        "node": "retrieve_documents",
        "file": "src/nodes/retrieve.py",
        "code": (
            'documents = retrieve_documents(state["question"])\n'
            "sources = format_sources(documents)\n"
            'return {**state, "retrieved_chunks": documents, "sources": sources}'
        ),
    },
    {
        "node": "generate_answer",
        "file": "src/nodes/generate.py",
        "code": (
            "context = format_context(state.get('retrieved_chunks', []))\n"
            "raw = invoke_llm(\n"
            "    GENERATE_SYSTEM,\n"
            "    GENERATE_USER.format(question=question, intent=intent, context=context),\n"
            ")"
        ),
        "code_safety": (
            "context = format_context(state.get('retrieved_chunks', []))\n"
            "raw = invoke_llm(\n"
            "    SAFETY_GENERATE_SYSTEM,\n"
            "    SAFETY_GENERATE_USER.format(question=question, context=context),\n"
            ")"
        ),
    },
    {
        "node": "validate_answer",
        "file": "src/nodes/validate.py",
        "code": (
            "passed, issues, confidence = validate_response(\n"
            "    question, customer_response, safety_risk, llm_passed, llm_issues, confidence\n"
            ")\n"
            'return {**state, "validation_passed": passed, "confidence": confidence}'
        ),
    },
    {
        "node": "risk_scoring",
        "file": "src/nodes/risk_scoring.py",
        "code": (
            "if safety_risk:\n"
            '    risk_level = "High"\n'
            "    escalation_required = True\n"
            "elif not validation_passed or confidence < 60:\n"
            "    escalation_required = True"
        ),
    },
]


def select_sample_question(question: str) -> None:
    """Load a sample into the text area (must run via button callback)."""
    st.session_state.question_input = question


@st.cache_resource(show_spinner="Loading knowledge base...")
def load_resources():
    vector_store = get_vector_store()
    workflow = build_graph()
    return vector_store, workflow


def render_header() -> None:
    st.title("SunGrid Support Agent")
    st.info(
        "**Used by:** SunGrid customer support reps. Paste a homeowner message to "
        "generate a customer-ready reply, internal notes, sources, and escalation guidance."
    )
    st.caption(
        "Internal copilot powered by RAG, LangGraph, and risk-based escalation. "
        + DISCLAIMER
    )


def render_sidebar() -> None:
    st.sidebar.header("How it works")
    st.sidebar.markdown(
        "1. Customer contacts SunGrid  \n"
        "2. **Rep** pastes their message  \n"
        "3. AI retrieves internal policies  \n"
        "4. Rep reviews draft + sends to customer"
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Claude · LangChain · LangGraph · Chroma · LangSmith")


def render_workflow_code_snippets(result: dict) -> None:
    st.markdown("**Implementation snippets (from this run's workflow)**")
    is_safety = result.get("risk_level") == "High" or "safety" in result.get("intent", "").lower()

    for snippet in WORKFLOW_CODE_SNIPPETS:
        code = snippet.get("code_safety") if snippet["node"] == "generate_answer" and is_safety else snippet["code"]
        st.markdown(f"`{snippet['node']}` · `{snippet['file']}`")
        st.code(code, language="python")


def render_question_input() -> str:
    st.subheader("Paste the customer's question")
    st.caption(
        "Enter the message as the homeowner wrote it — from email, chat, or phone notes."
    )

    question = st.text_area(
        "Customer message",
        key="question_input",
        height=120,
        placeholder=(
            "Example: The customer wrote — "
            "'My monitoring app stopped showing production. Is my system broken?'"
        ),
        label_visibility="collapsed",
    )

    run_clicked = st.button("Generate support draft", type="primary")

    if run_clicked:
        trimmed = question.strip()
        if not trimmed:
            st.warning("Paste the customer's message first, or pick a sample below.")
        else:
            _, workflow = load_resources()
            with st.spinner("Running LangGraph workflow..."):
                st.session_state["last_result"] = invoke_agent(trimmed, app=workflow)

    return question


def render_sample_questions() -> None:
    with st.expander("Common customer questions", expanded=False):
        st.caption("Click a sample question to test the assistant.")
        cols = st.columns(2)
        for index, (label, question) in enumerate(SAMPLE_QUESTIONS):
            column = cols[index % 2]
            column.button(
                label,
                key=f"sample_btn_{index}",
                use_container_width=True,
                on_click=select_sample_question,
                args=(question,),
            )


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
            "High-risk case: stop remote troubleshooting and escalate to a "
            "qualified technician."
        )

    st.markdown("##### Reply to send the customer")
    st.info(result.get("customer_response", ""))

    note = result.get("internal_note", {})
    st.markdown("##### Internal note (for the rep)")
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

    with st.expander("Answer Trace & Sources", expanded=False):
        st.code(
            "RAG + LangGraph execution path:\n"
            "question -> classify_intent -> retrieve_documents -> generate_answer "
            "-> validate_answer -> risk_scoring -> format_response",
            language="text",
        )
        st.caption(
            "Retrieved chunks were passed into the generation node as grounded context. "
            "The final answer was generated only after citation validation and risk scoring."
        )
        st.markdown("**Sources used**")
        sources = result.get("sources", [])
        if sources:
            for index, source in enumerate(sources, start=1):
                st.markdown(f"{index}. {source}")
        else:
            st.write("No sources returned.")

        st.markdown("**Workflow trace**")
        for step in result.get("workflow_trace", []):
            st.markdown(f"- {step}")

        st.markdown("**Retrieved context**")
        chunks = result.get("retrieved_chunks", [])
        if not chunks:
            st.write("No retrieved chunks.")
        else:
            for index, chunk in enumerate(chunks, start=1):
                metadata = chunk.metadata
                st.markdown(
                    f"**[{index}] {metadata.get('source', 'Unknown')} | "
                    f"Section {metadata.get('section_id', '?')} - "
                    f"{metadata.get('section_title', 'Unknown')}**"
                )
                st.markdown(chunk.page_content)

        st.markdown("---")
        render_workflow_code_snippets(result)


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
    render_question_input()
    render_sample_questions()

    if "last_result" in st.session_state:
        st.markdown("---")
        render_results(st.session_state["last_result"])


if __name__ == "__main__":
    main()
