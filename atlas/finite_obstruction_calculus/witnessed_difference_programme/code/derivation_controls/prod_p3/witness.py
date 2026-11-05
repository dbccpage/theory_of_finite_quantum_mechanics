from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from omega_engine_epistemic_immune_system.infrastructure.wdp_transferable_guard_adapter import (
    WdpTransferableGuardAdapter,
)
from omega_engine_epistemic_immune_system.use_cases.transferable_guard_library import (
    GuardTransferEvaluationRequest,
    GuardTransferRefusal,
    evaluate_guard_transfer,
)


def witness() -> dict[str, object]:
    adapter = WdpTransferableGuardAdapter()
    valid_req = GuardTransferEvaluationRequest(task_id=1, level=1, episode_budget=18)
    verdict = evaluate_guard_transfer(valid_req, adapter)

    stale_refused = False
    refusal_clause = ""
    try:
        evaluate_guard_transfer(
            GuardTransferEvaluationRequest(
                task_id=1,
                level=1,
                episode_budget=18,
                override_parent_digest="sha256:stale_parent_digest",
            ),
            adapter,
        )
    except GuardTransferRefusal as exc:
        stale_refused = True
        refusal_clause = exc.clause

    return {
        "goal_id": "PROD-P3",
        "runtime_package": "omega_engine_epistemic_immune_system",
        "bundle_matches_parent": verdict["bundle_matches_parent"],
        "sound_on_valid": verdict["sound_on_valid"],
        "adapter_pullback_verified": verdict["adapter_pullback_verified"],
        "trace_verified": verdict["trace_verified"],
        "transfer_accepted": verdict["transfer_accepted"],
        "net_savings": verdict["net_savings"],
        "stale_parent_refused": stale_refused,
        "refusal_clause": refusal_clause,
        "authority_effect": verdict["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
