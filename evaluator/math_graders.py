"""Deterministic graders for the reasoning/math evaluation.

Unlike tool-calling, there is no structured API field to lean on: tiny models
emit free-form reasoning plus a final answer in unpredictable formats. So we
extract the answer with layered heuristics, then compare numerically with a
small tolerance.

Two distinct failures are tracked:
    answer_parsed  - could we extract ANY number from the output?
    answer_correct - the extracted number matches the expected answer
This mirrors the tool eval's format_valid vs tool_correct split.
"""
from __future__ import annotations

import re
from typing import Any, Optional

NUMERIC_TOLERANCE = 1e-6

# Patterns tried in priority order. Each must end with a regex group that
# captures the numeric token (possibly a fraction like "3/4").
_ANSWER_PATTERNS = [
    re.compile(r"answer\s*[:=]?\s*([-+]?\d[\d,]*\s*(?:\.\d+)?(?:/\s*\d+)?)", re.IGNORECASE),
    re.compile(r"the\s+answer\s+is\s+([-+]?\d[\d,]*\s*(?:\.\d+)?(?:/\s*\d+)?)", re.IGNORECASE),
    re.compile(r"final\s+answer\s*[:=]?\s*([-+]?\d[\d,]*\s*(?:\.\d+)?(?:/\s*\d+)?)", re.IGNORECASE),
    re.compile(r"=\s*([-+]?\d[\d,]*\s*(?:\.\d+)?(?:/\s*\d+)?)\s*$", re.MULTILINE),
    # Plain trailing numbers: "so the answer is 42", "42", "42 minutes".
    re.compile(r"([-+]?\d[\d,]*\s*(?:\.\d+)?(?:/\s*\d+)?)\s*$", re.MULTILINE),
]

_LAST_NUMBER = re.compile(r"[-+]?\d[\d,]*\s*(?:\.\d+)?(?:/\s*\d+)?")


def _to_float(token: str) -> Optional[float]:
    """Convert an extracted token like '42', '1,000', '3/4', '-7.5' to float."""
    t = token.strip().replace(",", "")
    if "/" in t:
        parts = t.split("/")
        if len(parts) == 2:
            try:
                return float(parts[0].strip()) / float(parts[1].strip())
            except Exception:
                return None
    try:
        return float(t)
    except Exception:
        return None


def extract_answer(text: str) -> Optional[float]:
    """Extract the final numeric answer from free-form model output."""
    if not text or not text.strip():
        return None
    for pat in _ANSWER_PATTERNS:
        m = pat.search(text)
        if m:
            v = _to_float(m.group(1))
            if v is not None:
                return v
    # Last resort: scan every number in the text, take the last one.
    nums = [_to_float(m.group(0)) for m in _LAST_NUMBER.finditer(text)]
    nums = [n for n in nums if n is not None]
    return nums[-1] if nums else None


def _nearly_equal(got: float, expected: float) -> bool:
    return abs(got - expected) <= NUMERIC_TOLERANCE


def grade(example: dict, extracted: Optional[float]) -> dict:
    """Grade a single example. Returns the flags used for the CSV row."""
    expected = _to_float(str(example["answer"]))
    return {
        "answer_parsed": extracted is not None,
        "answer_correct": (
            expected is not None
            and extracted is not None
            and _nearly_equal(extracted, expected)
        ),
        "extracted_answer": extracted,
        "expected_answer": expected,
    }
