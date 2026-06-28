"""Validation helpers for generated support responses."""

from __future__ import annotations

DIY_PHRASES = (
    "electrical tape",
    "tape the wire",
    "tape them",
    "tape it",
    "fix it yourself",
    "fix this yourself",
    "open the inverter",
    "open the panel",
    "reset the breaker",
    "touch the wire",
    "wire nut",
    "splice the wire",
    "climb on the roof",
    "diy",
)

GUARANTEE_PHRASES = (
    "guaranteed coverage",
    "definitely covered",
    "will replace your entire system",
    "you will get 30%",
    "you qualify for the tax credit",
    "cancel anytime after installation",
)


PROHIBITION_PREFIXES = (
    "do not ",
    "don't ",
    "never ",
    "not ",
    "avoid ",
    "prohibited",
    "cannot ",
    "can't ",
)


def find_diy_advice(text: str) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    for phrase in DIY_PHRASES:
        if phrase not in lowered:
            continue
        index = 0
        is_advice = False
        while True:
            position = lowered.find(phrase, index)
            if position == -1:
                break
            window = lowered[max(0, position - 25) : position]
            if not any(prefix in window for prefix in PROHIBITION_PREFIXES):
                is_advice = True
                break
            index = position + len(phrase)
        if is_advice:
            hits.append(phrase)
    return hits


def find_unsupported_guarantees(text: str) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in GUARANTEE_PHRASES if phrase in lowered]


def validate_response(
    question: str,
    customer_response: str,
    safety_risk: bool,
    llm_passed: bool,
    llm_issues: list[str],
    confidence: int,
) -> tuple[bool, list[str], int]:
    """Combine deterministic checks with LLM validation output."""
    issues = list(llm_issues)

    if safety_risk:
        diy_hits = find_diy_advice(customer_response)
        if diy_hits:
            issues.extend([f"DIY advice detected: {hit}" for hit in diy_hits])
        troubleshooting_hits = [
            phrase
            for phrase in ("try resetting", "power-cycle", "reset the inverter")
            if phrase in customer_response.lower()
        ]
        if troubleshooting_hits:
            issues.extend(
                [f"Troubleshooting advice in safety case: {hit}" for hit in troubleshooting_hits]
            )

    guarantee_hits = find_unsupported_guarantees(customer_response)
    if guarantee_hits:
        issues.extend([f"Unsupported guarantee: {hit}" for hit in guarantee_hits])

    passed = llm_passed and not issues
    adjusted_confidence = confidence
    if issues:
        adjusted_confidence = min(confidence, 45)
    if safety_risk and passed:
        adjusted_confidence = max(adjusted_confidence, 85)

    return passed, issues, adjusted_confidence
