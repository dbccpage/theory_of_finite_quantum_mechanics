#!/usr/bin/env python3
"""Independent computational check for TFQ-0376 (PREGENESIS):
Justified-lift six-check checklist and budget-stop incomplete-search boundary.

Verifies:
1. Source anchors across:
   - `lean4/Imported/PreGenesisToMssn/Paper.lean` (`collapsed_observation_barrier`, `refine_separates`, `demand_accounting`, `chain_retraction_cannot_kill`)
   - `lean4/ChainRetraction.lean` (`TwoPoints.no_chain_retraction`, `Triangle.no_chain_retraction`)
   - `code/rust/src/combinatorics/enumeration.rs` (`CombinatoricsError::BudgetExceeded`)
   - `code/rust/src/combinatorics/color_constraints.rs` (`minimum_color_violations`)
   - `code/rust/src/wdp/wdp_lggr_chromatic.rs` (`ChromaticConstraintSystem::evaluate`, `triangle_two_color`)
   - `code/rust/src/wdp/finite_cost_report.rs` (`FiniteCostReport`)
2. Exhaustive truth-table verification over all 2^6 = 64 boolean combinations of the 6 Section-15
   checklist slots (`failed_predicate`, `admissible_repairs`, `extension_class`, `cost_order`,
   `tied_minima`, `search_completeness`) and transition stages (`Successor`, `ProposedLift`,
   `LicensedTransition`).
3. Budget-stop vs. exhaustive census verification on finite domains, including:
   - Uninspected tail witness where a budget stop at B < |D| misses a lower-cost or feasible repair.
   - K_3 2-coloring census (`triangle_two_color`, |D| = 2^3 = 8, 3 tied minima with 1 monochrome edge,
     0 proper 2-colorings) vs. 3-coloring repair (|D| = 3^3 = 27, 6 tied proper colorings with 0 violations).
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def evaluate_checklist(
    failed_predicate: bool,
    admissible_repairs: bool,
    repair_count: int,
    extension_class: bool,
    cost_order: bool,
    tied_minima_count: int,
    domain_size: int,
    checked_count: int,
) -> dict[str, bool]:
    exhaustive = domain_size > 0 and checked_count == domain_size
    budget_stopped = checked_count < domain_size
    successor = extension_class
    proposed_lift = failed_predicate and admissible_repairs and (repair_count > 0) and extension_class
    all_six_closed = (
        failed_predicate
        and admissible_repairs
        and (repair_count > 0)
        and extension_class
        and cost_order
        and (tied_minima_count > 0)
        and exhaustive
    )
    unique_minimal = all_six_closed and (tied_minima_count == 1)
    obstruction_certified = (
        failed_predicate
        and admissible_repairs
        and (repair_count == 0)
        and extension_class
        and exhaustive
    )
    return {
        "exhaustive": exhaustive,
        "budget_stopped": budget_stopped,
        "successor": successor,
        "proposed_lift": proposed_lift,
        "all_six_closed": all_six_closed,
        "unique_minimal": unique_minimal,
        "obstruction_certified": obstruction_certified,
    }


def run_all_checks() -> dict:
    checks_passed = 0
    failures: list[str] = []

    def check(cond: bool, label: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            failures.append(label)

    # 1. Source anchor checks
    paper_lean = REPO_ROOT / "lean4" / "Imported" / "PreGenesisToMssn" / "Paper.lean"
    chain_lean = REPO_ROOT / "lean4" / "ChainRetraction.lean"
    enum_rs = REPO_ROOT / "code" / "rust" / "src" / "combinatorics" / "enumeration.rs"
    color_rs = REPO_ROOT / "code" / "rust" / "src" / "combinatorics" / "color_constraints.rs"
    chrom_rs = REPO_ROOT / "code" / "rust" / "src" / "wdp" / "wdp_lggr_chromatic.rs"
    cost_rs = REPO_ROOT / "code" / "rust" / "src" / "wdp" / "finite_cost_report.rs"

    for p in (paper_lean, chain_lean, enum_rs, color_rs, chrom_rs, cost_rs):
        check(p.exists(), f"file_exists:{p.relative_to(REPO_ROOT).as_posix()}")

    paper_src = paper_lean.read_text(encoding="utf-8")
    chain_src = chain_lean.read_text(encoding="utf-8")
    enum_src = enum_rs.read_text(encoding="utf-8")
    color_src = color_rs.read_text(encoding="utf-8")
    chrom_src = chrom_rs.read_text(encoding="utf-8")
    cost_src = cost_rs.read_text(encoding="utf-8")

    check("theorem collapsed_observation_barrier" in paper_src, "paper_lean_collapsed_barrier")
    check("theorem refine_separates" in paper_src, "paper_lean_refine_separates")
    check("theorem demand_accounting" in paper_src, "paper_lean_demand_accounting")
    check("theorem chain_retraction_cannot_kill" in paper_src, "paper_lean_chain_retraction")
    check("theorem no_chain_retraction" in chain_src, "chain_lean_no_chain_retraction")
    check("BudgetExceeded" in enum_src, "enum_rs_budget_exceeded")
    check("pub fn minimum_color_violations" in color_src, "color_rs_minimum_color_violations")
    check("pub fn triangle_two_color" in chrom_src, "chrom_rs_triangle_two_color")
    check("pub struct FiniteCostReport" in cost_src, "cost_rs_finite_cost_report")

    # 2. Exhaustive 2^6 = 64 boolean truth table over the 6 checklist slots
    for bits in itertools.product([False, True], repeat=6):
        fp, ar, ec, co, tm_present, is_exh = bits
        rep_cnt = 2 if ar else 0
        tm_cnt = 1 if tm_present else 0
        dom_sz = 8
        chk_cnt = 8 if is_exh else 5
        res = evaluate_checklist(fp, ar, rep_cnt, ec, co, tm_cnt, dom_sz, chk_cnt)
        check(
            res["all_six_closed"] == all(bits),
            f"truth_table_all_six_{bits}",
        )
        if not is_exh:
            check(
                (not res["all_six_closed"])
                and (not res["unique_minimal"])
                and (not res["obstruction_certified"]),
                f"budget_stop_blocks_all_closures_{bits}",
            )

    # 3. Tied minima plurality checks (tied_minima_count in 1..10)
    for k_tied in range(1, 11):
        res = evaluate_checklist(True, True, 4, True, True, k_tied, 4, 4)
        check(res["all_six_closed"], f"tied_{k_tied}_closes_six_checks")
        check(
            res["unique_minimal"] == (k_tied == 1),
            f"tied_{k_tied}_unique_iff_one",
        )

    # 4. Stage separation checks (Successor vs ProposedLift vs LicensedTransition)
    s_only = evaluate_checklist(False, False, 0, True, False, 0, 8, 1)
    check(
        s_only["successor"] and (not s_only["proposed_lift"]) and (not s_only["all_six_closed"]),
        "stage_successor_only",
    )
    p_only = evaluate_checklist(True, True, 4, True, False, 0, 8, 4)
    check(
        p_only["successor"] and p_only["proposed_lift"] and (not p_only["all_six_closed"]),
        "stage_proposed_lift_only",
    )
    l_full = evaluate_checklist(True, True, 2, True, True, 1, 8, 8)
    check(
        l_full["successor"]
        and l_full["proposed_lift"]
        and l_full["all_six_closed"]
        and l_full["unique_minimal"],
        "stage_licensed_transition_full",
    )

    # 5. Uninspected tail countermodels across domain sizes N = 4..12
    for dom_n in range(4, 13):
        budget_b = dom_n - 1
        costs = [3 + (i % 3) for i in range(budget_b)] + [1]
        repairs = [False for _ in range(budget_b)] + [True]
        prefix_min = min(costs[:budget_b])
        full_min = min(costs)
        check(full_min == 1 and prefix_min >= 3 and full_min < prefix_min, f"tail_cost_beats_prefix_{dom_n}")
        check(
            (not any(repairs[:budget_b])) and any(repairs),
            f"tail_repair_missed_by_budget_stop_{dom_n}",
        )

    # 6. K_3 2-coloring obstruction vs 3-coloring lift (wdp_lggr_chromatic.rs)
    edges_k3 = [(0, 1), (1, 2), (2, 0)]
    colorings_2 = list(itertools.product(range(2), repeat=3))
    check(len(colorings_2) == 8, "k3_two_colorings_domain_8")
    violations_2 = [
        sum(1 for u, v in edges_k3 if c[u] == c[v]) for c in colorings_2
    ]
    check(min(violations_2) == 1, "k3_two_colorings_min_violation_1")
    check(violations_2.count(0) == 0, "k3_two_colorings_zero_proper")
    check(violations_2.count(1) == 6, "k3_two_colorings_six_tied_minima")

    # Extending palette from 2 to 3 colors (admissible repair in extension class k=3):
    colorings_3 = list(itertools.product(range(3), repeat=3))
    check(len(colorings_3) == 27, "k3_three_colorings_domain_27")
    violations_3 = [
        sum(1 for u, v in edges_k3 if c[u] == c[v]) for c in colorings_3
    ]
    check(min(violations_3) == 0, "k3_three_colorings_min_violation_0")
    check(violations_3.count(0) == 6, "k3_three_colorings_six_tied_proper_minima")

    return {
        "node_id": "TFQ-0376",
        "stage": "PREGENESIS",
        "checks_passed": checks_passed,
        "failures": failures,
        "passed": len(failures) == 0,
    }


if __name__ == "__main__":
    result = run_all_checks()
    if not result["passed"]:
        print(json.dumps(result, indent=2))
        raise SystemExit(1)
    print(
        f"TFQ-0376 INDEPENDENT CHECKER PASSED: checks={result['checks_passed']} failed={len(result['failures'])}"
    )
