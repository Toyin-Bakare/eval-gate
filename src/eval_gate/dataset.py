import json
from pathlib import Path

from .models import Case


def load(path: str | Path) -> list[Case]:
    """JSONL: one case per line with id, input, optional expected and context."""
    cases = []
    for i, line in enumerate(Path(path).read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        d = json.loads(line)
        cases.append(
            Case(
                id=str(d.get("id", i)),
                input=d["input"],
                expected=d.get("expected", {}),
                context=d.get("context"),
            )
        )
    if not cases:
        raise ValueError(f"no cases in {path}")
    return cases
