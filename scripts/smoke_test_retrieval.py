"""Smoke test: verify retrieval for the 8 sample demo questions.

VS Code: open this file and click Run (play button).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ensure_venv  # noqa: F401 — use project .venv when Play is clicked

from src.retriever import format_chunk_for_display, retrieve_documents
from src.vector_store import get_vector_store

SAMPLE_QUESTIONS = [
    {
        "id": 1,
        "question": (
            "My panels are producing about 35% less energy than expected. "
            "Is this covered under warranty?"
        ),
        "expected_files": {
            "warranty_policy.md",
            "installation_troubleshooting_guide.md",
        },
        "expected_sections": {"2.1", "3.2"},
        "require_all_files": False,
    },
    {
        "id": 2,
        "question": (
            "My monitoring app stopped showing production data. "
            "Does that mean my system is broken?"
        ),
        "expected_files": {"installation_troubleshooting_guide.md"},
        "expected_sections": {"3.1"},
    },
    {
        "id": 3,
        "question": "I smell something burning near the inverter. What should I do?",
        "expected_files": {"safety_escalation_policy.md"},
        "expected_sections": {"2.0", "3.1", "6.0"},
    },
    {
        "id": 4,
        "question": "Can I cancel my solar financing agreement after installation?",
        "expected_files": {"financing_faq.md"},
        "expected_sections": {"5.2"},
    },
    {
        "id": 5,
        "question": (
            "My inverter is showing an error code after a storm. Should I reset it?"
        ),
        "expected_files": {"installation_troubleshooting_guide.md"},
        "expected_sections": {"4.1", "4.2", "5.2"},
    },
    {
        "id": 6,
        "question": (
            "My bill is higher than expected even though I have solar panels. Why?"
        ),
        "expected_files": {"financing_faq.md"},
        "expected_sections": {"3.2"},
    },
    {
        "id": 7,
        "question": (
            "There are exposed wires near the panel connection box. "
            "Can I tape them myself?"
        ),
        "expected_files": {"safety_escalation_policy.md"},
        "expected_sections": {"2.0", "3.2", "7.0"},
    },
    {
        "id": 8,
        "question": "What information do I need before starting a warranty claim?",
        "expected_files": {"warranty_policy.md"},
        "expected_sections": {"5.0"},
    },
]


def _evaluate_case(case: dict, documents) -> tuple[bool, list[str]]:
    notes: list[str] = []
    retrieved_files = {doc.metadata.get("file_name") for doc in documents}
    retrieved_sections = {doc.metadata.get("section_id") for doc in documents}

    if case.get("require_all_files", True):
        files_ok = case["expected_files"].issubset(retrieved_files)
    else:
        files_ok = bool(case["expected_files"] & retrieved_files)

    sections_ok = any(
        section in retrieved_sections for section in case["expected_sections"]
    )

    if not files_ok:
        if case.get("require_all_files", True):
            missing = case["expected_files"] - retrieved_files
            notes.append(f"missing files: {', '.join(sorted(missing))}")
        else:
            notes.append(
                "missing any expected file from: "
                + ", ".join(sorted(case["expected_files"]))
            )
    if not sections_ok:
        notes.append(
            "missing expected sections: "
            + ", ".join(sorted(case["expected_sections"]))
        )

    passed = files_ok and sections_ok
    return passed, notes


def main() -> None:
    print("Building / loading Chroma vector store...")
    store = get_vector_store()
    print("Running retrieval smoke test for 8 sample questions\n")
    print("=" * 72)

    passed_count = 0

    for case in SAMPLE_QUESTIONS:
        documents = retrieve_documents(case["question"], vector_store=store)
        passed, notes = _evaluate_case(case, documents)
        passed_count += int(passed)

        status = "PASS" if passed else "FAIL"
        print(f"\n[{status}] Question {case['id']}: {case['question']}")
        print("-" * 72)
        for rank, doc in enumerate(documents, start=1):
            print(format_chunk_for_display(doc, rank))
        if notes:
            print("Notes:", "; ".join(notes))

    print("\n" + "=" * 72)
    print(f"Result: {passed_count}/{len(SAMPLE_QUESTIONS)} passed")


if __name__ == "__main__":
    main()
