"""eval-gate run --dataset cases.jsonl --runner pkg.module:function [--thresholds t.json] ..."""
import argparse
import importlib
import json
import os
import sys
from pathlib import Path

from . import dataset, gate


def _load_runner(spec: str):
    if ":" not in spec:
        sys.exit("runner must be module:function, e.g. myapp.triage:run_case")
    mod, fn = spec.split(":", 1)
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())  # so repo-local runners import from the working dir
    return getattr(importlib.import_module(mod), fn)


def _print_summary(report) -> None:
    status = "PASS" if report.passed else "FAIL"
    print(f"eval-gate {status}  {report.prompt_ref or '(no prompt_ref)'}  {report.n_cases} cases")
    for key, ok in report.checks.items():
        mark = "ok  " if ok else "FAIL"
        print(f"  {mark} {key:<20} {report.aggregates[key]:<10} threshold {report.thresholds[key]}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="eval-gate")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="score a prompt version and gate it")
    r.add_argument("--dataset", required=True, help="JSONL file of cases")
    r.add_argument("--runner", required=True, help="module:function that takes a Case, returns a RunResult")
    r.add_argument("--thresholds", help="JSON file; keys override defaults")
    r.add_argument("--prompt-ref", default="", help="label written into the report, e.g. triage@1.2.0")
    r.add_argument("--out", help="write full JSON report here")
    args = p.parse_args(argv)

    cases = dataset.load(args.dataset)
    runner = _load_runner(args.runner)
    thresholds = json.loads(Path(args.thresholds).read_text()) if args.thresholds else None
    report = gate.run(cases, runner, thresholds, args.prompt_ref, Path(args.dataset).name)

    _print_summary(report)
    if args.out:
        Path(args.out).write_text(json.dumps(report.to_dict(), indent=2))
        print(f"  report -> {args.out}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
