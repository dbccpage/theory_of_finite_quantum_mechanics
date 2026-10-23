from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from omega_engine_pfp.infrastructure.wdp_abstention_governor_adapter import (
    WdpAbstentionGovernorAdapter,
)
from omega_engine_pfp.use_cases.abstention_governor import (
    EvaluateAbstentionGovernorUseCase,
)


def witness() -> dict[str, object]:
    adapter = WdpAbstentionGovernorAdapter()
    use_case = EvaluateAbstentionGovernorUseCase(adapter)

    sym_graph = {
        "s": [("branch_sym", "1", ["u1", "u2"]), ("expensive", "5", ["t"])],
        "u1": [("finish", "2", ["t"])],
        "u2": [("finish", "2", ["t"])],
        "t": [],
    }
    res_out_of_fuel = use_case.execute(
        sym_graph, initial="s", targets=("t",), budget="2", compress_quotient=True
    )
    res_terminated = use_case.execute(
        sym_graph, initial="s", targets=("t",), budget="3", compress_quotient=True
    )

    impossible_graph = {
        "s": [("loop", "1", ["s"])],
        "t": [],
    }
    res_impossible = use_case.execute(
        impossible_graph, initial="s", targets=("t",), budget="10", compress_quotient=False
    )

    out_fuel = res_out_of_fuel.value
    term = res_terminated.value
    imp = res_impossible.value

    return {
        "goal_id": "PROD-P1",
        "runtime_package": "omega_engine_pfp",
        "out_of_fuel_label": out_fuel["termination_label"],
        "terminated_label": term["termination_label"],
        "impossible_label": imp["termination_label"],
        "initial_value": term["initial_value"],
        "raw_state_count": term["raw_state_count"],
        "quotient_state_count": term["quotient_state_count"],
        "quotient_verified": term["quotient_verified"],
        "authority_effect": term["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
