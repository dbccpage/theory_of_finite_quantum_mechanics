from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from omega_engine_cognitive_operations.infrastructure.wdp_observation_budget_adapter import (
    WdpObservationBudgetAdapter,
)
from omega_engine_cognitive_operations.use_cases.observation_budget_planner import (
    ObservationBudgetRequest,
    plan_observation_budget,
)


def witness() -> dict[str, object]:
    adapter = WdpObservationBudgetAdapter()
    req = ObservationBudgetRequest(
        outcome_map={
            "I_buyer_monolithic": {"s0": "0", "s1": "1", "s2": "2"},
            "I_pair01": {"s0": "0", "s1": "1", "s2": "1"},
            "I_pair12": {"s0": "0", "s1": "0", "s2": "1"},
        },
        instrument_prices={
            "I_buyer_monolithic": "5",
            "I_pair01": "3/2",
            "I_pair12": "2",
        },
        pairs_to_separate=(("s0", "s1"), ("s1", "s2"), ("s0", "s2")),
        preserve_future_operations=True,
    )
    res = plan_observation_budget(req, adapter)
    assert res.is_ok()
    payload = res.unwrap()

    infeasible_req = ObservationBudgetRequest(
        outcome_map={"I_blind": {"s0": "0", "s1": "0"}},
        instrument_prices={"I_blind": "1"},
        pairs_to_separate=(("s0", "s1"),),
    )
    infeasible_res = plan_observation_budget(infeasible_req, adapter)

    return {
        "goal_id": "PROD-P4",
        "runtime_package": "omega_engine_cognitive_operations",
        "planned_suite": list(payload["planned_suite"]),
        "planned_cost": payload["planned_cost"],
        "suite_verified": payload["suite_verified"],
        "future_preserving_cost": payload["future_preserving_cost"],
        "static_safe_suite_cost": payload["static_safe_suite_cost"],
        "beats_static_safe_suite": payload["beats_static_safe_suite"],
        "infeasible_refused": infeasible_res.is_err(),
        "authority_effect": payload["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
