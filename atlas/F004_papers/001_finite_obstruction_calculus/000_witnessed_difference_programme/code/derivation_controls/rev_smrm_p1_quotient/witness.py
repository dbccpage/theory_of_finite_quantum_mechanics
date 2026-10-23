from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
_WDP_CODE = (
    _REPO_ROOT
    / "omega_engine_atlas"
    / "coda_atlas"
    / "F004_papers"
    / "001_finite_obstruction_calculus"
    / "000_witnessed_difference_programme"
    / "code"
)
if str(_WDP_CODE) not in sys.path:
    sys.path.insert(0, str(_WDP_CODE))

from certified_progress import checker as cp_checker
from certified_progress import model as cp_model
from certified_progress import observation as cp_obs
from certified_progress import producer as cp_producer
from certified_progress import structural as cp_structural


def witness() -> dict[str, object]:
    raw_graph = {
        "s": [("branch_sym", "1", ["u1", "u2"]), ("expensive", "5", ["t"])],
        "u1": [("finish", "2", ["t"])],
        "u2": [("finish", "2", ["t"])],
        "t": [],
    }
    model = cp_model.graph_model(
        raw_graph, initial="s", targets=("t",), task_id="quotient-compression-test"
    )
    arena = cp_model.compile_model(model)
    target_block = [list(b) for b in arena.reachable if b in arena.targets]
    non_target_block = [list(b) for b in arena.reachable if b not in arena.targets]
    seed = [target_block, non_target_block]

    refinement_out = cp_obs.refine_operation_presentation(model, seed)
    blocks = refinement_out["blocks"]
    table = refinement_out["table"]

    refinement_ok = cp_structural.check_refinement(model, seed, refinement_out["refinement"])
    quotient_ok = cp_structural.check_quotient(model, blocks, table)
    congruent = cp_obs.is_congruence(model, blocks)

    q_model = cp_obs.quotient_model(model, blocks)
    q_arena = cp_model.compile_model(q_model)

    raw_cert = cp_producer.solve_progress(model)["certificate"]
    q_cert = cp_producer.solve_progress(q_model)["certificate"]
    raw_check = cp_checker.check_certificate(model, raw_cert)
    q_check = cp_checker.check_certificate(q_model, q_cert)

    bad_blocks = [[list(b) for b in arena.reachable]]
    bad_congruent = cp_obs.is_congruence(model, bad_blocks)

    return {
        "goal_id": "REV-SMRM-P1-QUOTIENT",
        "raw_reachable_count": len(arena.reachable),
        "quotient_reachable_count": len(q_arena.reachable),
        "refinement_check_passed": refinement_ok,
        "quotient_check_passed": quotient_ok,
        "refined_congruent": congruent,
        "bad_blocks_congruent": bad_congruent,
        "raw_initial_value": raw_check["initial_value"],
        "quotient_initial_value": q_check["initial_value"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
