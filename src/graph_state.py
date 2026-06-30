"""Shared graph state and LLM helpers."""

from __future__ import annotations

import json
import re
from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage

from src.config import configure_langsmith, settings

configure_langsmith()


class AgentState(TypedDict):
    question: str
    intent: str
    intents: list[str]
    safety_risk: bool
    retrieved_chunks: list[Document]
    sources: list[str]
    customer_response: str
    internal_note: dict
    recommended_action: str
    risk_level: str
    confidence: int
    escalation_required: bool
    workflow_trace: list[str]
    validation_notes: str
    validation_passed: bool


def get_llm() -> ChatAnthropic:
    return ChatAnthropic(
        model=settings.anthropic_model,
        api_key=settings.anthropic_api_key,
        temperature=0,
    )


def append_trace(state: AgentState, message: str) -> list[str]:
    return state.get("workflow_trace", []) + [message]


def format_context(documents: list[Document]) -> str:
    blocks: list[str] = []
    for index, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "Unknown")
        section_id = doc.metadata.get("section_id", "?")
        section_title = doc.metadata.get("section_title", "Unknown")
        blocks.append(
            f"[{index}] {source} | Section {section_id} - {section_title}\n"
            f"{doc.page_content}"
        )
    return "\n\n---\n\n".join(blocks)


def parse_sections(text: str) -> tuple[str, str]:
    customer_match = re.search(
        r"CUSTOMER_RESPONSE:\s*(.*?)\s*INTERNAL_NOTE:",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    internal_match = re.search(
        r"INTERNAL_NOTE:\s*(.*)$",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    customer = customer_match.group(1).strip() if customer_match else text.strip()
    internal = internal_match.group(1).strip() if internal_match else ""
    return customer, internal


def parse_json_content(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```.*$", "", cleaned, flags=re.DOTALL).strip()

    start = cleaned.find("{")
    if start == -1:
        return json.loads(cleaned)

    payload, _ = json.JSONDecoder().raw_decode(cleaned[start:])
    return payload


def invoke_llm(system_prompt: str, user_prompt: str) -> str:
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )
    return response.content if isinstance(response.content, str) else str(response.content)
