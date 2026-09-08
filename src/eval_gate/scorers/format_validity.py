"""Is the output in the expected shape? Supports expected.format = "json" and required_keys."""
import json
import re

from ..models import Case


def _strip_fences(text: str) -> str:
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    return m.group(1) if m else text


def format_validity(case: Case, output: str) -> float:
    fmt = case.expected.get("format")
    if fmt is None:
        return 1.0
    if fmt == "json":
        try:
            obj = json.loads(_strip_fences(output).strip())
        except json.JSONDecodeError:
            return 0.0
        keys = case.expected.get("required_keys", [])
        if not keys:
            return 1.0
        if not isinstance(obj, dict):
            return 0.0
        return sum(k in obj for k in keys) / len(keys)
    raise ValueError(f"unknown format: {fmt}")
