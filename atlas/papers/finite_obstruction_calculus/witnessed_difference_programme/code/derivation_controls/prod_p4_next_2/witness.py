"""Executable witness for PROD-P4-NEXT-2 (Map CompletionTarget raw/quotient/both onto distinct_image targets)."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_paths() -> Path:
    here = Path(__file__).resolve()
    repo_root = next((p for p in here.parents if (p / ".git").exists()), None)
    if repo_root is None:
        raise FileNotFoundError("repository root not found")
    for candidate in (
        repo_root,
        repo_root
        / "omega_engine_atlas"
        / "coda_atlas"
        / "papers"
        / "finite_obstruction_calculus"
        / "witnessed_difference_programme"
        / "code",
    ):
        s = str(candidate)
        if s not in sys.path:
            sys.path.insert(0, s)
    return repo_root


_ensure_paths()

from observer_completion.observer_completion import M  # noqa: E402
from omega_engine_applications.wdp_products.p4_observation_budget.adapter import (  # noqa: E402
    map_completion_target_to_distinct_image,
)
from omega_engine_applications.wdp_products.p4_observation_budget.contracts import (  # noqa: E402
    CompletionTarget,
)


def witness() -> dict[str, object]:
    source = M([[0, 0], [1, 0], [0, 1], [0, 0]], 2)
    repair = M([[1, 0], [0, 1], [0, 0], [0, 0]], 2)
    observer = M([[0, 0, 0, 1]], 4)

    results: dict[str, int] = {}
    for kind in ("raw", "quotient", "both"):
        target = CompletionTarget(kind=kind, pairs_to_separate=(("s0", "s1"),))
        out = map_completion_target_to_distinct_image(source, repair, observer, target)
        if not isinstance(out, dict) or not out.get("accepted"):
            raise RuntimeError(f"failed to map CompletionTarget({kind!r})")
        results[kind] = int(out["minimum"])

    return {
        "goal_id": "PROD-P4-NEXT-2",
        "raw_minimum": results["raw"],
        "quotient_minimum": results["quotient"],
        "joint_minimum": results["both"],
        "separate_sum": results["raw"] + results["quotient"],
        "strict_subadditivity": results["both"] < results["raw"] + results["quotient"],
        "authority_effect": "None",
    }


def refuse_non_completion_target() -> None:
    source = M([[1]], 1)
    repair = M([[1]], 1)
    observer = M([[1]], 1)
    res = map_completion_target_to_distinct_image(source, repair, observer, "not-a-target")  # type: ignore[arg-type]
    if hasattr(res, "code"):
        raise ValueError(f"{res.code}: {res.reason}")
