from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Case:
    id: str
    input: str
    expected: dict[str, Any] = field(default_factory=dict)  # contains, regex, format, required_keys
    context: str | None = None                              # source text for groundedness


@dataclass
class RunResult:
    """What the runner returns for one case."""
    text: str
    latency_ms: int = 0
    cost_usd: float = 0.0


Runner = Callable[[Case], RunResult]


@dataclass
class CaseScore:
    id: str
    scores: dict[str, float]
    latency_ms: int
    cost_usd: float
    output: str


@dataclass
class Report:
    prompt_ref: str
    dataset: str
    n_cases: int
    aggregates: dict[str, float]      # mean per scorer + latency_p95_ms + cost_per_case_usd
    thresholds: dict[str, float]
    checks: dict[str, bool]           # threshold name -> passed
    passed: bool
    cases: list[CaseScore]

    def to_dict(self) -> dict:
        return {
            "prompt_ref": self.prompt_ref,
            "dataset": self.dataset,
            "n_cases": self.n_cases,
            "aggregates": self.aggregates,
            "thresholds": self.thresholds,
            "checks": self.checks,
            "passed": self.passed,
            "cases": [c.__dict__ for c in self.cases],
        }
