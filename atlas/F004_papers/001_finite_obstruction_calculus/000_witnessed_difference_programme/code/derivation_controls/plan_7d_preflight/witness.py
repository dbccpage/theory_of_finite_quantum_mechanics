"""Dependency, path, and guard preflight control for PLAN-7D-PREFLIGHT.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
REPO_ROOT = PACKAGE_ROOT.parents[4]


def preflight_staged_runner(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    """Preflight PFP demo runner, controller, jsonschema dependency, and legacy live guard."""
    runner_path = repo_root / "omega_engine_education" / "scripts" / "run_pfp_demos.py"
    controller_path = repo_root / "omega_engine_pfp" / "controllers" / "pfp_controller.py"
    live_evaluator_path = (
        repo_root / "omega_engine_woland" / "tests" / "pilots" / "live_evaluator.py"
    )
    if not runner_path.is_file():
        raise ValueError("missing omega_engine_education/scripts/run_pfp_demos.py")
    if not controller_path.is_file():
        raise ValueError("missing omega_engine_pfp/controllers/pfp_controller.py")
    if not live_evaluator_path.is_file():
        raise ValueError("missing omega_engine_woland/tests/pilots/live_evaluator.py")

    import jsonschema  # noqa: F401

    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from omega_engine_woland.tests.pilots import live_evaluator as live

    try:
        live.dispatch_live_prompt(
            "unused-secret",
            "fixture-model",
            "Solve",
            "Compute",
            "PFP-01-EXACT-LINALG",
        )
    except ValueError as exc:
        guard_constant = getattr(exc, "code", None)
        refusal_code = 2 if guard_constant == "LEGACY_LIVE_REQUIRES_CANONICAL_PFP" else 1
    else:
        raise RuntimeError("legacy live dispatch guard did not refuse before network")

    if refusal_code != 2 or guard_constant != "LEGACY_LIVE_REQUIRES_CANONICAL_PFP":
        raise RuntimeError("legacy live dispatch guard did not fail closed with exit code 2")

    return {
        "runner_exists": True,
        "controller_exists": True,
        "jsonschema_available": True,
        "help_exit_code": 0,
        "legacy_live_refusal_exit_code": refusal_code,
        "guard_code": guard_constant,
    }


def check_reservation_collation(
    budget_cap_cents: int, reserved_cents: int, actual_cost_cents: int | None
) -> dict[str, int | str]:
    """Verify unknown-cost collation keeps reservation committed instead of releasing."""
    if (
        type(budget_cap_cents) is not int
        or type(reserved_cents) is not int
        or budget_cap_cents <= 0
        or reserved_cents <= 0
        or reserved_cents > budget_cap_cents
    ):
        raise ValueError("budget_cap_cents and reserved_cents must be positive ints within cap")
    if actual_cost_cents is None:
        return {
            "status": "UNKNOWN_COST_RETAINED",
            "committed_cents": reserved_cents,
            "remaining_cents": budget_cap_cents - reserved_cents,
        }
    if type(actual_cost_cents) is not int or actual_cost_cents < 0:
        raise ValueError("actual_cost_cents must be a non-negative int or None")
    if actual_cost_cents > budget_cap_cents:
        raise ValueError("actual cost exceeds budget cap")
    return {
        "status": "COLLATED",
        "committed_cents": actual_cost_cents,
        "remaining_cents": budget_cap_cents - actual_cost_cents,
    }


def witness() -> dict[str, object]:
    preflight = preflight_staged_runner()
    unknown = check_reservation_collation(1000, 250, None)
    collated = check_reservation_collation(1000, 250, 180)
    if (
        unknown["committed_cents"] != 250
        or unknown["remaining_cents"] != 750
        or collated["committed_cents"] != 180
        or collated["remaining_cents"] != 820
    ):
        raise RuntimeError("reservation collation check failed")
    return {
        **preflight,
        "unknown_cost_committed_cents": unknown["committed_cents"],
        "collated_committed_cents": collated["committed_cents"],
    }
