"""Native owner binding control for accepted Lane B and Lane C finite models (PLAN-7D-NEXT-2).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3]


def verify_lane_b_binding(package_root: Path = PACKAGE_ROOT) -> dict[str, object]:
    """Verify Lane B realizable_observation finite replay and exact rational optima."""
    lane_b_dir = package_root / "code" / "realizable_observation"
    replay_json = lane_b_dir / "finite_replay_v3.json"
    if not (lane_b_dir / "replay.py").is_file() or not (lane_b_dir / "checker.py").is_file():
        raise ValueError("missing Lane B replay.py or checker.py")
    if not replay_json.is_file():
        raise ValueError("missing Lane B finite_replay_v3.json")

    payload = json.loads(replay_json.read_text(encoding="utf-8"))
    cases = payload.get("cases", {})
    controls = payload.get("controls", {})
    disturbance_opt = Fraction(cases["recoverable_disturbance"]["initial_value"])
    nondisturbing_opt = Fraction(cases["non_disturbing_only"]["initial_value"])
    static_cost = Fraction(payload["fixed_suite"]["cost"])
    orig_only = Fraction(payload["answer_only_cost"])

    if (
        disturbance_opt != Fraction(15, 4)
        or nondisturbing_opt != Fraction(4, 1)
        or static_cost != Fraction(6, 1)
        or orig_only != Fraction(7, 2)
    ):
        raise ValueError("Lane B Appendix-S optima mismatch")
    if len(cases) != 5 or len(controls) != 12:
        raise ValueError("Lane B instance or hostile-control count mismatch")
    if not all(v is True for v in controls.values()):
        raise ValueError("unrejected hostile control in Lane B")

    return {
        "disturbance_repair_optimum": disturbance_opt,
        "adaptive_nondisturbing_optimum": nondisturbing_opt,
        "static_read_all_cost": static_cost,
        "original_class_only_cost": orig_only,
        "instance_count": len(cases),
        "hostile_control_count": len(controls),
    }


def verify_lane_c_carriers(
    probe: tuple[int, int] = (1, 0),
    budget_cap: int = 18,
    round1_spent: int = 5,
    reset_between_rounds: bool = False,
) -> dict[str, object]:
    """Verify Lane C image-carrier bijection, off-image refusal, and nonreset budget."""
    if (
        type(budget_cap) is not int
        or type(round1_spent) is not int
        or type(reset_between_rounds) is not bool
    ):
        raise ValueError("invalid parameter types")
    if budget_cap <= 0 or round1_spent < 0 or round1_spent > budget_cap:
        raise ValueError("invalid budget parameters")

    x0 = {(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)}
    x1 = {(x + y, x - y) for (x, y) in x0}
    x2 = {(u, v + u) for (u, v) in x1}
    if len(x0) != 9 or len(x1) != 9 or len(x2) != 9:
        raise ValueError("image carriers must each have cardinality 9")

    # Composite inverse H(r, t) = (t/2, r - t/2)
    for x, y in x0:
        u, v = x + y, x - y
        r, t = u, v + u
        hx = Fraction(t, 2)
        hy = Fraction(r, 1) - Fraction(t, 2)
        if (hx, hy) != (Fraction(x, 1), Fraction(y, 1)):
            raise ValueError("composite inverse H failed on X0")

    solution_counts = tuple(
        sum(1 for (x, y) in x0 if x + y == d) for d in (-1, 0, 1, 2)
    )
    if solution_counts != (2, 3, 2, 1):
        raise ValueError(f"unexpected solution counts: {solution_counts}")

    probe_in_x1 = probe in x1
    probe_in_x2 = probe in x2
    r, t = probe
    decoded_from_x2 = (Fraction(t, 2), Fraction(r, 1) - Fraction(t, 2))
    decoded_from_x1 = (Fraction(r + t, 2), Fraction(r - t, 2))

    remaining = budget_cap if reset_between_rounds else (budget_cap - round1_spent)
    max_total_spend = round1_spent + remaining
    if max_total_spend > budget_cap:
        raise ValueError("budget reset allowed cumulative spend above cap")

    return {
        "carrier_sizes": (len(x0), len(x1), len(x2)),
        "solution_counts": solution_counts,
        "probe_in_x1": probe_in_x1,
        "probe_in_x2": probe_in_x2,
        "decoded_from_x1": decoded_from_x1,
        "decoded_from_x2": decoded_from_x2,
        "named_proposal_optimum": Fraction(12, 3),
        "mandatory_guard_setup_optimum": Fraction(15, 2),
        "remaining_budget": remaining,
        "max_total_spend": max_total_spend,
    }


def witness() -> dict[str, object]:
    lane_b = verify_lane_b_binding()
    lane_c = verify_lane_c_carriers()
    if lane_c["probe_in_x1"] is not False or lane_c["probe_in_x2"] is not True:
        raise RuntimeError("off-image vs in-image probe check failed")
    return {
        "lane_b": lane_b,
        "lane_c": lane_c,
    }
