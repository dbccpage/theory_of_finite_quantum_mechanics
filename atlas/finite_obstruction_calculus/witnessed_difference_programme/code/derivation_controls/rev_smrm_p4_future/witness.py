from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction
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

from certified_progress import checker as cp_checker
from certified_progress import producer as cp_producer
from realizable_observation import checker as ro_checker
from realizable_observation import core as ro_core
from realizable_observation import replay as ro_replay


def witness() -> dict[str, object]:
    instance = ro_core.example()
    built_preserved = ro_core.construct(copy.deepcopy(instance), answers_only=False)
    construction_verdict = ro_checker.check_construction(instance, built_preserved)

    cert_preserved = cp_producer.solve_progress(built_preserved["model"])["certificate"]
    check_preserved = cp_checker.check_certificate(built_preserved["model"], cert_preserved)

    built_answers_only = ro_core.construct(copy.deepcopy(instance), answers_only=True)
    cert_answers_only = cp_producer.solve_progress(built_answers_only["model"])["certificate"]
    check_answers_only = cp_checker.check_certificate(
        built_answers_only["model"], cert_answers_only
    )

    safe_cost, safe_suite = ro_core.fixed_suite_cost(instance)
    replay_out = ro_replay.replay()

    return {
        "goal_id": "REV-SMRM-P4-FUTURE",
        "preserved_cost": check_preserved["initial_value"],
        "answers_only_cost": check_answers_only["initial_value"],
        "fixed_suite_cost": str(safe_cost),
        "fixed_suite": list(safe_suite),
        "strictly_cheaper_than_fixed": Fraction(check_preserved["initial_value"]) < safe_cost,
        "construction_verified": construction_verdict["accepted"],
        "certificate_verified": check_preserved["accepted"],
        "replay_verified": all(replay_out["controls"].values()),
        "authority_effect": replay_out["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
