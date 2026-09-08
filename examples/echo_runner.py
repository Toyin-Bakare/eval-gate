"""A runner that needs no model. Swap for one that calls llm-gateway in real use.

    eval-gate run --dataset examples/cases.jsonl --runner examples.echo_runner:run_case \
        --thresholds examples/thresholds.json --prompt-ref demo@0.0.1
"""
import json

from eval_gate import Case, RunResult


def run_case(case: Case) -> RunResult:
    # Pretend answer built from the input so the demo gate passes.
    out = {"cause": case.input, "fix": "See context: " + (case.context or "")}
    return RunResult(text=json.dumps(out), latency_ms=120, cost_usd=0.001)
