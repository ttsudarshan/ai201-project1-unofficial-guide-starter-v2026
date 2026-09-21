"""
Judges one answer against the `expects` phrase written in questions.py before
any results existed.

An answer is correct when it contains the expects phrase (ignoring case and
extra whitespace) AND the answer is not the refusal line.
"""

import re

REFUSAL = "i don't have enough information"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def judge(question: str, expects: str, answer: str, results) -> bool:
    a = _norm(answer)
    return _norm(expects) in a and REFUSAL not in a
