import statistics

from .models import Case, CaseScore, Report, Runner
from .scorers import SCORERS

DEFAULT_THRESHOLDS = {
    "task_completion": 0.8,     # mean, min
    "groundedness": 0.7,        # mean, min
    "format_validity": 1.0,     # mean, min
    "latency_p95_ms": 10000,    # max
    "cost_per_case_usd": 0.05,  # max
}
_MAX_KEYS = {"latency_p95_ms", "cost_per_case_usd"}


def _p95(values: list[int]) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return float(values[0])
    return float(statistics.quantiles(values, n=20)[-1])


def run(
    cases: list[Case],
    runner: Runner,
    thresholds: dict[str, float] | None = None,
    prompt_ref: str = "",
    dataset_name: str = "",
) -> Report:
    thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    case_scores: list[CaseScore] = []
    for case in cases:
        result = runner(case)
        scores = {name: fn(case, result.text) for name, fn in SCORERS.items()}
        case_scores.append(
            CaseScore(case.id, scores, result.latency_ms, result.cost_usd, result.text)
        )

    agg: dict[str, float] = {}
    for name in SCORERS:
        agg[name] = round(statistics.fmean(c.scores[name] for c in case_scores), 4)
    agg["latency_p95_ms"] = round(_p95([c.latency_ms for c in case_scores]), 1)
    agg["cost_per_case_usd"] = round(statistics.fmean(c.cost_usd for c in case_scores), 6)

    checks: dict[str, bool] = {}
    for key, limit in thresholds.items():
        if key not in agg:
            continue
        checks[key] = agg[key] <= limit if key in _MAX_KEYS else agg[key] >= limit

    return Report(
        prompt_ref=prompt_ref,
        dataset=dataset_name,
        n_cases=len(cases),
        aggregates=agg,
        thresholds=thresholds,
        checks=checks,
        passed=all(checks.values()),
        cases=case_scores,
    )
