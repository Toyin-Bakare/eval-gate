import json

from eval_gate import Case, RunResult, gate


def cases():
    return [
        Case("1", "a", {"contains": ["ok"], "format": "json", "required_keys": ["k"]}),
        Case("2", "b", {"contains": ["ok"], "format": "json", "required_keys": ["k"]}),
    ]


def good(case):
    return RunResult(json.dumps({"k": "ok"}), latency_ms=100, cost_usd=0.001)


def bad(case):
    return RunResult("nope", latency_ms=100, cost_usd=0.001)


def test_pass():
    r = gate.run(cases(), good, prompt_ref="p@1")
    assert r.passed and r.n_cases == 2
    assert r.aggregates["task_completion"] == 1.0
    assert r.checks["latency_p95_ms"]


def test_fail_on_content():
    r = gate.run(cases(), bad)
    assert not r.passed
    assert not r.checks["task_completion"] and not r.checks["format_validity"]


def test_fail_on_cost():
    r = gate.run(cases(), good, thresholds={"cost_per_case_usd": 0.0001})
    assert not r.passed and not r.checks["cost_per_case_usd"]


def test_report_dict_roundtrip():
    d = gate.run(cases(), good).to_dict()
    assert json.loads(json.dumps(d))["passed"] is True
