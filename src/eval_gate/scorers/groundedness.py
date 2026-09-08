"""Heuristic: share of output sentences whose content words mostly appear in the context.

This is a lexical overlap check, not a fact checker. A high score means the output
stays close to the source text; it does not prove the output is true.
"""
import re

from ..models import Case

_STOP = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "at", "for", "by", "with",
    "is", "are", "was", "were", "be", "been", "it", "this", "that", "these", "those",
    "as", "from", "into", "than", "then", "so", "if", "not", "no",
}


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9_.-]{3,}", text.lower()) if w not in _STOP}


def groundedness(case: Case, output: str, min_overlap: float = 0.5) -> float:
    if not case.context:
        return 1.0  # nothing to ground against
    ctx = _words(case.context)
    sentences = [s for s in re.split(r"(?<=[.!?\n])\s+", output.strip()) if len(_words(s)) >= 3]
    if not sentences:
        return 1.0
    grounded = 0
    for s in sentences:
        w = _words(s)
        if len(w & ctx) / len(w) >= min_overlap:
            grounded += 1
    return grounded / len(sentences)
