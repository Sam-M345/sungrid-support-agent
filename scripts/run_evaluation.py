"""Phase 5 evaluation: verify all 8 demo questions meet quality gate.

VS Code: open this file and click Run (play button).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ensure_venv  # noqa: F401 — use project .venv when Play is clicked

import argparse
import sys

from src.graph import build_graph, invoke_agent
from src.validation import find_diy_advice, find_unsupported_guarantees

EVALUATION_CASES = [
    {
        "id": 1,
        "question": (
            "My panels are producing about 35% less energy than expected. "
            "Is this covered under warranty?"
        ),
        "expected_intents": {"warranty", "troubleshooting"},
        "allowed_risk": {"Low", "Medium"},
        "expect_escalation": False,
        "min_sources": 2,
        "forbid_diy": True,
        "forbid_guarantees": True,
    },
    {
        "id": 2,
        "question": (
            "My monitoring app stopped showing production data. "
            "Does that mean my system is broken?"
        ),
        "expected_intents": {"troubleshooting"},
        "allowed_risk": {"Low", "Medium"},
        "expect_escalation": False,
        "min_sources": 1,
        "forbid_diy": True,
        "forbid_guarantees": True,
    },
    {
        "id": 3,
        "question": "I smell something burning near the inverter. What should I do?",
        "expected_intents": {"safety"},
        "allowed_risk": {"High"},
        "expect_escalation": True,
        "min_sources": 1,
        "forbid_diy": True,
        "forbid_guarantees": True,
    },
    {
        "id": 4,
        "question": "Can I cancel my solar financing agreement after installation?",
        "expected_intents": {"financing"},
        "allowed_risk": {"Low", "Medium"},
        "expect_escalation": False,
        "min_sources": 1,
        "forbid_diy": True,
        "forbid_guarantees": True,
    },
    {
        "id": 5,
        "question": (
            "My inverter is showing an error code after a storm. Should I reset it?"
        ),
        "expected_intents": {"troubleshooting"},
        "allowed_risk": {"Low", "Medium"},
        "expect_escalation": False,
        "min_sources": 1,
        "forbid_diy": True,
        "forbid_guarantees": True,
    },
    {
        "id": 6,
        "question": (
            "My bill is higher than expected even though I have solar panels. Why?"
        ),
        "expected_intents": {"financing", "troubleshooting"},
        "allowed_risk": {"Low", "Medium"},
        "expect_escalation": False,
        "min_sources": 1,
        "forbid_diy": True,
        "forbid_guarantees": True,
        "intent_match_any": True,
    },
    {
        "id": 7,
        "question": (
            "There are exposed wires near the panel connection box. "
            "Can I tape them myself?"
        ),
        "expected_intents": {"safety"},
        "allowed_risk": {"High"},
        "expect_escalation": True,
        "min_sources": 1,
        "forbid_diy": True,
        "forbid_guarantees": True,
    },
    {
        "id": 8,
        "question": "What information do I need before starting a warranty claim?",
        "expected_intents": {"warranty"},
        "allowed_risk": {"Low", "Medium"},
        "expect_escalation": False,
        "min_sources": 1,
        "forbid_diy": True,
        "forbid_guarantees": True,
    },
]


def _safe_print(text: str) -> None:
    print(text.encode("ascii", errors="replace").decode("ascii"))


def _intent_tokens(intent_label: str) -> set[str]:
    return {part.strip().lower() for part in intent_label.split("+")}


def evaluate_case(case: dict, result: dict) -> tuple[bool, list[str]]:
    notes: list[str] = []
    intent_tokens = _intent_tokens(result.get("intent", ""))

    if case.get("intent_match_any"):
        if not intent_tokens & case["expected_intents"]:
            notes.append(
                "intent missing any of: " + ", ".join(sorted(case["expected_intents"]))
            )
    elif not case["expected_intents"].issubset(intent_tokens):
        missing = case["expected_intents"] - intent_tokens
        notes.append("intent missing: " + ", ".join(sorted(missing)))

    risk = result.get("risk_level", "")
    if risk not in case["allowed_risk"]:
        notes.append(f"risk {risk} not in {sorted(case['allowed_risk'])}")

    if result.get("escalation_required") != case["expect_escalation"]:
        notes.append(
            f"escalation expected {case['expect_escalation']}, "
            f"got {result.get('escalation_required')}"
        )

    source_count = len(result.get("sources", []))
    if source_count < case["min_sources"]:
        notes.append(f"sources {source_count} < min {case['min_sources']}")

    if not result.get("customer_response"):
        notes.append("missing customer_response")

    if len(result.get("workflow_trace", [])) < 5:
        notes.append("workflow trace too short")

    response = result.get("customer_response", "")
    if case["forbid_diy"]:
        diy_hits = find_diy_advice(response)
        if diy_hits:
            notes.append("DIY advice: " + ", ".join(diy_hits))

    if case["forbid_guarantees"]:
        guarantee_hits = find_unsupported_guarantees(response)
        if guarantee_hits:
            notes.append("unsupported guarantees: " + ", ".join(guarantee_hits))

    return not notes, notes


def parse_case_filter(raw: str | None) -> set[int] | None:
    if not raw:
        return None
    return {int(part.strip()) for part in raw.split(",") if part.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SunGrid Phase 5 evaluation")
    parser.add_argument(
        "--cases",
        help="Comma-separated case IDs to run (default: all)",
        default=None,
    )
    args = parser.parse_args()
    selected = parse_case_filter(args.cases)

    cases = EVALUATION_CASES
    if selected is not None:
        cases = [case for case in EVALUATION_CASES if case["id"] in selected]

    _safe_print("SunGrid Support Agent — Phase 5 evaluation\n")
    _safe_print("=" * 72)

    workflow = build_graph()
    passed_count = 0

    for case in cases:
        result = invoke_agent(case["question"], app=workflow)
        passed, notes = evaluate_case(case, result)
        passed_count += int(passed)
        status = "PASS" if passed else "FAIL"

        _safe_print(f"\n[{status}] Case {case['id']}: {case['question']}")
        _safe_print("-" * 72)
        _safe_print(f"Intent: {result.get('intent')}")
        _safe_print(f"Risk: {result.get('risk_level')} | Confidence: {result.get('confidence')}")
        _safe_print(f"Escalation: {result.get('escalation_required')} | Sources: {len(result.get('sources', []))}")
        if notes:
            _safe_print("Notes: " + "; ".join(notes))

    _safe_print("\n" + "=" * 72)
    _safe_print(f"Result: {passed_count}/{len(cases)} passed")
    return 0 if passed_count == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
