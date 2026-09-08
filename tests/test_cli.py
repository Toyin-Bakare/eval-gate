import json
from pathlib import Path

from eval_gate.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_cli_pass(tmp_path, capsys):
    out = tmp_path / "report.json"
    code = main([
        "run",
        "--dataset", str(ROOT / "examples/cases.jsonl"),
        "--runner", "examples.echo_runner:run_case",
        "--thresholds", str(ROOT / "examples/thresholds.json"),
        "--prompt-ref", "demo@0.0.1",
        "--out", str(out),
    ])
    assert code == 0
    assert "PASS" in capsys.readouterr().out
    assert json.loads(out.read_text())["n_cases"] == 3


def test_cli_fail(tmp_path):
    t = tmp_path / "t.json"
    t.write_text('{"cost_per_case_usd": 0.0}')
    code = main([
        "run",
        "--dataset", str(ROOT / "examples/cases.jsonl"),
        "--runner", "examples.echo_runner:run_case",
        "--thresholds", str(t),
    ])
    assert code == 1
