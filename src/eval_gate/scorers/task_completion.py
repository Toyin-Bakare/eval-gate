"""Did the output contain what the case expects? Uses expected.contains and expected.regex."""
import re

from ..models import Case


def task_completion(case: Case, output: str) -> float:
    exp = case.expected
    checks: list[bool] = []
    low = output.lower()
    for s in exp.get("contains", []):
        checks.append(s.lower() in low)
    for s in exp.get("not_contains", []):
        checks.append(s.lower() not in low)
    for pat in exp.get("regex", []):
        checks.append(re.search(pat, output, re.IGNORECASE | re.DOTALL) is not None)
    if not checks:
        return 1.0  # nothing to check
    return sum(checks) / len(checks)
