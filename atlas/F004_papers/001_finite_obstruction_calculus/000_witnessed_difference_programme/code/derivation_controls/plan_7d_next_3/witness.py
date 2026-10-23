"""Full workflow endpoint runner control: SG-40 admission then SG-48 reuse (PLAN-7D-NEXT-3).

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_sibling_witness(control_name: str):
    path = Path(__file__).resolve().parents[1] / control_name / "witness.py"
    module_name = f"{control_name}_witness_loaded"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def run_workflow_endpoints(
    substitute_q6_continuation: bool = False,
    substitute_generic_controller_stages: bool = False,
    withhold_sg48_task2_until_admission: bool = True,
) -> dict[str, object]:
    """Run SG-40 then SG-48 and reject Q.6 or generic stage-record substitutions."""
    if (
        type(substitute_q6_continuation) is not bool
        or type(substitute_generic_controller_stages) is not bool
        or type(withhold_sg48_task2_until_admission) is not bool
    ):
        raise ValueError("invalid PLAN-7D-NEXT-3 control flags")
    if substitute_q6_continuation:
        raise ValueError("Q.6 continuation record cannot substitute for SG-40/SG-48 execution")
    if substitute_generic_controller_stages:
        raise ValueError("generic research-controller stage log cannot substitute for SG-40/SG-48")
    if not withhold_sg48_task2_until_admission:
        raise ValueError("SG-48 Task 2 must remain withheld until Task 1 Stage 5 admission")

    sg40_res = _load_sibling_witness("sg_40").witness()
    if sg40_res["after_receipt"]["free_h1_rank"] != 0:
        raise RuntimeError("SG-40 failed to discharge H1 obstruction")

    sg48_res = _load_sibling_witness("sg_48").run_sg_48_episodes(
        task2_sealed_during_ep1=withhold_sg48_task2_until_admission
    )
    if sg48_res["episode_2_receipt"]["terminal_state"] != "c":
        raise RuntimeError("SG-48 Episode 2 failed to reach terminal state c")

    return {
        "execution_order": ("SG-40", "SG-48"),
        "sg_40": sg40_res,
        "sg_48": sg48_res,
        "anti_substitution_verified": True,
    }


def witness() -> dict[str, object]:
    return run_workflow_endpoints()
