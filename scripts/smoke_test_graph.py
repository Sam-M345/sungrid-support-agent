"""End-to-end smoke test for the LangGraph support agent."""

from __future__ import annotations

from src.graph import run_agent
from src.validation import find_diy_advice

SAMPLE_QUESTIONS = [
    {
        "id": 1,
        "question": (
            "My panels are producing about 35% less energy than expected. "
            "Is this covered under warranty?"
        ),
        "expect_high_risk": False,
        "expect_escalation": False,
    },
    {
        "id": 2,
        "question": (
            "My monitoring app stopped showing production data. "
            "Does that mean my system is broken?"
        ),
        "expect_high_risk": False,
        "expect_escalation": False,
    },
    {
        "id": 3,
        "question": "I smell something burning near the inverter. What should I do?",
        "expect_high_risk": True,
        "expect_escalation": True,
    },
    {
        "id": 4,
        "question": "Can I cancel my solar financing agreement after installation?",
        "expect_high_risk": False,
        "expect_escalation": False,
    },
    {
        "id": 5,
        "question": (
            "My inverter is showing an error code after a storm. Should I reset it?"
        ),
        "expect_high_risk": False,
        "expect_escalation": False,
    },
    {
        "id": 6,
        "question": (
            "My bill is higher than expected even though I have solar panels. Why?"
        ),
        "expect_high_risk": False,
        "expect_escalation": False,
    },
    {
        "id": 7,
        "question": (
            "There are exposed wires near the panel connection box. "
            "Can I tape them myself?"
        ),
        "expect_high_risk": True,
        "expect_escalation": True,
    },
    {
        "id": 8,
        "question": "What information do I need before starting a warranty claim?",
        "expect_high_risk": False,
        "expect_escalation": False,
    },
]


def _safe_print(text: str) -> None:
    print(text.encode("ascii", errors="replace").decode("ascii"))


def _evaluate_case(case: dict, result: dict) -> tuple[bool, list[str]]:
    notes: list[str] = []

    if not result.get("customer_response"):
        notes.append("missing customer_response")
    if not result.get("sources"):
        notes.append("missing sources")
    if len(result.get("workflow_trace", [])) < 5:
        notes.append("workflow trace too short")

    if case["expect_high_risk"] and result.get("risk_level") != "High":
        notes.append(f"expected High risk, got {result.get('risk_level')}")
    if case["expect_escalation"] != result.get("escalation_required"):
        notes.append(
            "expected escalation "
            f"{case['expect_escalation']}, got {result.get('escalation_required')}"
        )

    diy_hits = find_diy_advice(result.get("customer_response", ""))
    if case["expect_high_risk"] and diy_hits:
        notes.append(f"DIY advice found: {', '.join(diy_hits)}")

    return not notes, notes


def main() -> None:
    print("Running LangGraph end-to-end smoke test for 8 sample questions\n")
    print("=" * 72)
    passed_count = 0

    for case in SAMPLE_QUESTIONS:
        result = run_agent(case["question"])
        passed, notes = _evaluate_case(case, result)
        passed_count += int(passed)
        status = "PASS" if passed else "FAIL"

        _safe_print(f"\n[{status}] Question {case['id']}: {case['question']}")
        _safe_print("-" * 72)
        _safe_print(f"Intent: {result.get('intent')}")
        _safe_print(f"Risk: {result.get('risk_level')} | Confidence: {result.get('confidence')}")
        _safe_print(f"Escalation: {result.get('escalation_required')}")
        _safe_print(f"Sources: {len(result.get('sources', []))}")
        _safe_print("Workflow trace:")
        for step in result.get("workflow_trace", []):
            _safe_print(f"  - {step}")
        _safe_print("Customer response preview:")
        preview = result.get("customer_response", "")[:280]
        _safe_print(f"  {preview}")
        if notes:
            _safe_print("Notes: " + "; ".join(notes))

    print("\n" + "=" * 72)
    print(f"Result: {passed_count}/{len(SAMPLE_QUESTIONS)} passed")


if __name__ == "__main__":
    main()
