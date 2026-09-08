"""Runner that calls a model through llm-gateway. Requires: pip install llm-gateway[anthropic]"""
from llm_gateway import Gateway, GatewayConfig

from eval_gate import Case, RunResult

SYSTEM = (
    "You triage CI failures. Reply with JSON only: "
    '{"cause": "<one sentence>", "fix": "<one sentence>"}'
)
_gw = Gateway(GatewayConfig(provider="anthropic", model="claude-sonnet-4-5", max_tokens=300))


def run_case(case: Case) -> RunResult:
    r = _gw.call(system=SYSTEM, user=case.input, session_id="eval", caller="eval-gate")
    return RunResult(text=r.text, latency_ms=r.latency_ms, cost_usd=r.cost_usd)
