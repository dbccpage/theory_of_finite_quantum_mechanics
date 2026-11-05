from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
_WDP_CODE = (
    _REPO_ROOT
    / "omega_engine_atlas"
    / "coda_atlas"
    / "papers"
    / "finite_obstruction_calculus"
    / "witnessed_difference_programme"
    / "code"
)
if str(_WDP_CODE) not in sys.path:
    sys.path.insert(0, str(_WDP_CODE))

from rejection_reuse import core as rr_core
from rejection_reuse import trace_checker as rr_trace_checker


def witness() -> dict[str, object]:
    packet = rr_core.parent_packet(d=1, level=1)
    digest = rr_core.packet_digest(packet)
    bundle = {
        "parent_sha256": digest,
        "task": 1,
        "level": 1,
    }
    matches_parent = rr_core.bundle_matches(bundle, packet)

    stale_packet = copy.deepcopy(packet)
    stale_packet["extra_field"] = "mutated"
    tampered_rejected = not rr_core.bundle_matches(bundle, stale_packet)

    carrier_points = [tuple(p) for p in packet["carrier"]]
    valid_points = [p for p in carrier_points if rr_core.valid(1, 1, p)]
    sound_on_valid = all(not rr_core.rejects(1, 1, p, "parameterized") for p in valid_points)

    rows = rr_core.ledger()
    trace_verdict = rr_trace_checker.check_trace(rows, budget=18)

    return {
        "goal_id": "REV-SMRM-P3-MINE",
        "trace_verified": trace_verdict["accepted"],
        "spent": trace_verdict["spent"],
        "remaining": trace_verdict["remaining"],
        "parent_digest": digest,
        "bundle_matches_parent": matches_parent,
        "tampered_parent_rejected": tampered_rejected,
        "sound_on_valid": sound_on_valid,
        "authority_effect": trace_verdict["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
