"""SunGrid Support Agent — recruiter-friendly Streamlit demo."""

from __future__ import annotations

import bootstrap_env  # noqa: F401 — before Chroma loads

import html
import re
import threading
import time

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

WORKFLOW_STATUS_MESSAGES = [
    "Classifying customer intent...",
    "Retrieving policy documents from Chroma...",
    "Sending grounded context to Claude...",
    "Generating customer-ready response...",
    "Validating citations against sources...",
    "Scoring risk and escalation...",
    "Formatting support draft...",
]
WORKFLOW_ESTIMATED_SECONDS = 20.0
WORKFLOW_STATUS_INTERVAL_SECONDS = 2.5

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
    st.sidebar.header("Project Tech Stack")
    st.sidebar.markdown(
        "LLM: Claude · Framework: LangChain · Vector DB: Chroma · "
        "Workflow: LangGraph · Tracing: LangSmith"
    )


def render_workflow_code_snippets(result: dict) -> None:
    is_safety = result.get("risk_level") == "High" or "safety" in result.get("intent", "").lower()

    for snippet in WORKFLOW_CODE_SNIPPETS:
        code = snippet.get("code_safety") if snippet["node"] == "generate_answer" and is_safety else snippet["code"]
        st.markdown(f"`{snippet['node']}` · `{snippet['file']}`")
        st.code(code, language="python")


def _recommended_action_bullets(action: str) -> list[str]:
    """Split internal recommended action text into one item per numbered step."""
    if not action or not action.strip():
        return ["Review draft and respond to homeowner."]

    text = re.sub(r"\s+", " ", action.strip())

    if re.search(r"\d+\.\s", text):
        parts = re.split(r"\s*(?=\d+\.\s)", text)
        bullets: list[str] = []
        for part in parts:
            cleaned = re.sub(r"^\d+\.\s*", "", part.strip()).strip()
            if cleaned:
                bullets.append(cleaned)
        if bullets:
            return bullets

    bullets = []
    for line in action.strip().split("\n"):
        cleaned = re.sub(r"^\d+\.\s*", "", line.strip())
        if cleaned:
            bullets.append(cleaned)

    if bullets:
        return bullets

    return [action.strip()]


def render_internal_note(result: dict, note: dict) -> None:
    st.markdown("##### Internal note (for the rep)")

    issue_type = note.get("issue_type", result.get("intent", ""))
    st.markdown(
        f"**Issue type**  \n<span style='font-size:0.95rem;'>{html.escape(issue_type)}</span>",
        unsafe_allow_html=True,
    )

    bullets = _recommended_action_bullets(note.get("recommended_action", ""))
    steps_html = "".join(
        f'<li style="margin-bottom:0.65rem;">{html.escape(bullet)}</li>'
        for bullet in bullets
    )
    st.markdown(
        f"""
<div style="
    background: linear-gradient(135deg, #1a2744 0%, #121a2e 100%);
    border: 1px solid #3d6fa8;
    border-left: 5px solid #5dade2;
    border-radius: 10px;
    padding: 1.1rem 1.35rem;
    margin-top: 1rem;
">
    <p style="
        font-size: 1.25rem;
        font-weight: 700;
        color: #5dade2;
        margin: 0 0 0.85rem 0;
    ">Recommended action</p>
    <ol style="
        margin: 0;
        padding-left: 1.35rem;
        color: #f0f4f8;
        line-height: 1.55;
        font-size: 0.98rem;
    ">{steps_html}</ol>
</div>
        """,
        unsafe_allow_html=True,
    )

    validation_notes = note.get("validation_notes", result.get("validation_notes", ""))
    if validation_notes:
        st.caption(f"Validation: {validation_notes}")


def run_agent_with_progress(question: str, workflow) -> dict | None:
    """Run the agent with a time-based progress bar and rotating status labels."""
    progress = st.progress(0)
    status = st.empty()

    result_box: dict = {}
    error_box: dict = {}

    def _run() -> None:
        try:
            result_box["result"] = invoke_agent(question, app=workflow)
        except Exception as exc:
            error_box["error"] = exc

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    start = time.time()
    while thread.is_alive():
        elapsed = time.time() - start
        pct = min(int(elapsed / WORKFLOW_ESTIMATED_SECONDS * 100), 99)
        progress.progress(pct)

        msg_index = int(elapsed // WORKFLOW_STATUS_INTERVAL_SECONDS) % len(
            WORKFLOW_STATUS_MESSAGES
        )
        status.markdown(f"**{WORKFLOW_STATUS_MESSAGES[msg_index]}**")

        time.sleep(0.2)

    thread.join()
    progress.progress(100)
    time.sleep(0.4)
    progress.empty()
    status.empty()

    if "error" in error_box:
        st.error(f"Workflow failed: {error_box['error']}")
        return None

    return result_box.get("result")


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
            result = run_agent_with_progress(trimmed, workflow)
            if result is not None:
                st.session_state["last_result"] = result

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


def render_answer_trace_and_sources(result: dict) -> None:
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; letter-spacing: 0.15em; color: #888;'>"
        "*********</p>",
        unsafe_allow_html=True,
    )
    st.caption(
        "The section below is for engineers, developers, and technical reviewers. "
        "Support reps can focus on the customer reply and internal note above."
    )
    st.markdown("##### Answer Trace & Sources")
    st.code(
        "RAG + LangGraph execution path:\n"
        "question\n"
        "-> classify_intent\n"
        "-> retrieve_documents\n"
        "-> generate_answer\n"
        "-> validate_answer\n"
        "-> risk_scoring\n"
        "-> format_response",
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

    with st.expander("Developer implementation snippets", expanded=False):
        render_workflow_code_snippets(result)


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

    note = result.get("internal_note", {})
    render_internal_note(result, note)

    st.markdown("##### Reply to send the customer")
    st.info(result.get("customer_response", ""))

    render_answer_trace_and_sources(result)


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
