from __future__ import annotations

from .models import EvaluationResult


def markdown(result: EvaluationResult) -> str:
    status = "PASS" if result.passed else "FAIL"
    rows = "\n".join(
        f"| {c.dimension} | {c.check_id} | {'PASS' if c.passed else 'FAIL'} | {c.weight:g} | {c.message} |"
        for c in result.checks
    )
    return f"""# ChangeBench evaluation: {result.scenario_id}

**Agent:** {result.agent_name}  
**Decision:** {status}  
**Score:** {result.score}/100  
**Integrity receipt:** `{result.receipt}`

| Dimension | Check | Result | Weight | Requirement |
|---|---|---:|---:|---|
{rows}

## Unit economics

- Estimated monthly cost delta: ${result.metrics['estimated_monthly_cost_delta_usd']:,.2f}
- Estimated revenue exposure: ${result.metrics['estimated_revenue_exposure_usd']:,.2f}
- Tool calls: {result.metrics['tool_calls']:g}
- Evaluation latency: {result.metrics['latency_seconds']:g}s

> A receipt proves integrity of this serialized evaluation, not identity or non-repudiation. Production use requires authenticated signing and evidence custody.
"""

