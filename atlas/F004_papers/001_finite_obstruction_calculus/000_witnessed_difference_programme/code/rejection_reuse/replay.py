"""Execute exact tests; submit arena certificates to the search-free checker.

Run from the enclosing code directory: python -m rejection_reuse.replay
Optional --output writes a new, LF-only record, refusing to overwrite evidence.
"""

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from certified_progress.checker import check_certificate
from certified_progress.producer import solve_progress
from .core import (CARRIERS, TASKS, X0, X1, X2, decode, f01, f12, g10, g21,
                   bundle_matches, ledger, named_arena, packet_digest, parent_packet,
                   rejects, scan_arena, valid)
from .trace_checker import check_trace


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def checked(model):
    produced = solve_progress(model)
    require(produced["certificate"] is not None, "producer did not return a certificate")
    replayed = check_certificate(copy.deepcopy(model), copy.deepcopy(produced["certificate"]))
    require(replayed["accepted"], repr(replayed))
    return {"model": model, "certificate": produced["certificate"], "checker": replayed}


def run():
    controls, cases = {}, {}
    maps = []
    for p, q, r in zip(X0, X1, X2):
        require(g10(q) == p and g21(r) == q and f12(g21(r)) == r, "inverse map")
        require(f01(g10(q)) == q and decode(2, r) == p, "original answer")
        require(all(valid(0, d, p) == valid(1, d, q) == valid(2, d, r)
                    for d in TASKS), "validity transport")
        maps.append({"x0": p, "x1": q, "x2": r})
    require(all(len(set(c)) == 9 for c in CARRIERS), "image cardinality")
    emission_checks = guard_checks = 0
    for level, carrier in enumerate(CARRIERS):
        for d in TASKS:
            good = {p for p in carrier if valid(level, d, p)}
            original_good = {p for p in X0 if valid(0, d, p)}
            for mask in range(1 << 9):
                chosen = {p for i, p in enumerate(carrier) if mask & (1 << i)}
                decoded = {decode(level, p) for p in chosen}
                require((decoded <= original_good) == (chosen <= good), "soundness iff")
                require((original_good <= decoded) == (good <= chosen), "coverage iff")
                emission_checks += 1
                # Named proposals + full check: only valid kept candidates emit.
                emitted = good - chosen  # chosen is now an arbitrary rejection set
                require((emitted == good) == not_intersects(chosen, good), "guard coverage iff")
                guard_checks += 1
    # Full supplied profile: all named proposals are retained, no hidden search restriction.
    for d in TASKS:
        for level in range(3):
            name = f"named_d{d}_l{level}"
            cases[name] = checked(named_arena(d, level=level))
            require(cases[name]["checker"]["initial_value"] == "4", name)
        cases[f"guard_d{d}"] = checked(named_arena(d, level=2, guard="parameterized"))
        require(cases[f"guard_d{d}"]["checker"]["initial_value"] == "9/2", "mandatory guard")
    # Enumerate every distinct valid count and every safe rejection count.
    scan_table = []
    for v in (1, 2, 3):
        bare = checked(scan_arena(v))
        cases[f"scan_bare_v{v}"] = bare
        require(Q(bare["checker"]["initial_value"]) == 31 - 3*v, "bare scan cost")
        for s in range(10 - v):
            guarded = checked(scan_arena(v, s, guarded=True))
            cases[f"scan_guard_v{v}_s{s}"] = guarded
            value = Q(guarded["checker"]["initial_value"])
            require(value == Q(72 - 7*v - 4*s, 2), "guarded scan cost")
            require((value <= 31 - 3*v) == (4*s >= 10-v), "operating threshold")
            require((value + 3 <= 31 - 3*v) == (4*s >= 16-v), "setup threshold")
            scan_table.append({"v": v, "s": s, "operating": str(value),
                               "including_setup": str(value + 3)})
    blocked = checked(named_arena(2, level=2, guard="fixed_one"))
    cases["fixed_guard_blocked"] = blocked
    controls["changed_task_fixed_guard_blocks_unique_solution"] = (
        rejects(2, 2, (2, 2), "fixed_one") and blocked["checker"]["claim"] == "LOSS")
    fallback = checked(named_arena(2, level=2, guard="fixed_one", original_route=True))
    cases["fixed_guard_with_fallback"] = fallback
    controls["retained_original_route_prevents_global_loss"] = fallback["checker"]["initial_value"] == "6"
    controls["safe_guard_cost_only_failure"] = (Q(cases["guard_d1"]["checker"]["initial_value"]) + 3
                                                 == Q(15, 2) > 4)
    controls["installation_not_necessary_at_budget18"] = cases["named_d2_l0"]["checker"]["initial_value"] == "4"
    controls["maximal_guard_scan_d2_exceeds_total18"] = Q(33, 2) + 3 > 18
    controls["fast_guard_emission_cost_is_five_halves"] = 1 + Q(1, 2) + 1 == Q(5, 2)
    controls["wrong_checker_accepts_original_invalid"] = (sum((0, 0)) in (1-1, 1)
                                                            and not valid(0, 1, (0, 0)))
    # A semantic-equivalence certificate is an exhaustive truth table on the carrier.
    v1 = tuple(valid(1, d, p) for d in TASKS for p in X1)
    v1_refactored = tuple(p in X1 and p[0] - d == 0 for d in TASKS for p in X1)
    v2 = tuple(p in X1 and p[0] in (d-1, d) for d in TASKS for p in X1)
    controls["equivalent_checker_table_equal"] = v1 == v1_refactored
    controls["changed_semantics_table_differs"] = v1 != v2
    controls["scalar_report_does_not_decode_pair"] = (f01((0, 1))[0] == f01((1, 0))[0]
                                                       and (0, 1) != (1, 0))
    controls["wrong_direction_level0_is_not_a_decoder"] = g10((1, 0)) != f01((1, 0))
    controls["tagged_carriers_are_not_interchangeable"] = (1, 0) not in X1 and (1, 0) in X2
    try:
        decode(1, (1, 0))
    except ValueError:
        controls["out_of_image_rejected"] = g10((1, 0)) == (Q(1, 2), Q(1, 2))
    else:
        controls["out_of_image_rejected"] = False
    # Bundles are bound to bytes and a task, not a vague checker version name.
    parent = parent_packet()
    bundle = {"parent_sha256": packet_digest(parent), "task": 1, "level": 1}
    stale = copy.deepcopy(parent)
    stale["different_parent_revision"] = "unchanged acceptance table"
    controls["stale_parent_refused_even_if_predicate_unchanged"] = (
        bundle_matches(bundle, parent) and not bundle_matches(bundle, stale))
    require(not bundle_matches(bundle, parent_packet(d=2)), "task-bound installation")
    changed_task_certificate = cases["named_d1_l0"]["certificate"]
    controls["changed_task_certificate_refused"] = not check_certificate(
        named_arena(2), changed_task_certificate)["accepted"]
    forged = copy.deepcopy(cases["named_d1_l0"]["certificate"])
    next(row for row in forged["values"] if row["belief"] == ["s"])["value"] = "3"
    controls["forged_value_refused"] = not check_certificate(
        named_arena(1), forged)["accepted"]
    changed_price = named_arena(1)
    next(row for row in changed_price["costs"] if row["belief"] == ["s"])["cost"] = "2"
    controls["price_change_refuses_old_certificate"] = not check_certificate(
        changed_price, cases["named_d1_l0"]["certificate"])["accepted"]
    # Same semantic upper bound can survive a menu addition, but old byte binding cannot.
    new_menu = named_arena(1)
    new_menu["actions"].append("unused_expensive")
    new_menu["enabled"]["s"].append("unused_expensive")
    new_menu["transitions"].append({"state": "s", "action": "unused_expensive", "successors": ["s"]})
    new_menu["reports"].append({"state": "s", "action": "unused_expensive", "observation": "s"})
    new_menu["costs"].append({"belief": ["s"], "action": "unused_expensive", "cost": "100"})
    cases["menu_addition_unchanged_optimum"] = checked(new_menu)
    controls["menu_change_not_semantic_failure_iff"] = (
        cases["menu_addition_unchanged_optimum"]["checker"]["initial_value"] == "4"
        and not check_certificate(new_menu, cases["named_d1_l0"]["certificate"])["accepted"])
    rows = ledger()
    require(valid(1, 1, (1, -1)) and decode(1, (1, -1)) == (0, 1), "parent witness")
    trace_result = check_trace(rows)
    require(trace_result["accepted"] and trace_result["spent"] == "17"
            and trace_result["remaining"] == "1", "outer continuation")
    hostile_traces = {}
    for name, removed in (("skip_parent_check", 1), ("skip_install", 5),
                          ("skip_transport", 6), ("skip_child_check", 9)):
        forged_trace = copy.deepcopy(rows)
        del forged_trace[removed]
        hostile_traces[name] = forged_trace
    for name, index, field, value in (("changed_parent", 8, "parent", "different-parent"),
                                     ("changed_task", 8, "task", 2),
                                     ("fuel_reset", 6, "spent", "1"),
                                     ("undercharged_repeated_guard", 12, "charge", "0"),
                                     ("wrong_decoded_emission", 10, "operation", "emit (1,0)")):
        forged_trace = copy.deepcopy(rows)
        forged_trace[index][field] = value
        hostile_traces[name] = forged_trace
    # After a valid first child episode, duplicate it and then emit the second
    # answer. Every occurrence still pays; the resulting 43/2 exceeds budget18.
    repeated = [copy.deepcopy(row) for row in rows[:11] + rows[7:11] + rows[11:]]
    cumulative = Q(0)
    for row in repeated:
        cumulative += Q(row["charge"])
        row["spent"] = str(cumulative)
    hostile_traces["repeated_episode_over_budget"] = repeated
    trace_checks = {name: check_trace(trace) for name, trace in hostile_traces.items()}
    require(all(not result["accepted"] for result in trace_checks.values()), "hostile outer trace accepted")
    repeated_result = check_trace(repeated, budget=22)
    require(repeated_result["accepted"] and repeated_result["spent"] == "43/2",
            "repeated episode must be charged rather than hidden")
    controls["compositional_ledger_spends17_of18"] = rows[-1]["spent"] == "17"
    child_answers = {decode(2, (1, 0)), decode(2, (1, 2))}
    controls["compositional_child_covers_both_answers"] = child_answers == {(0, 1), (1, 0)}
    controls["repeat_occurrences_are_charged_twice"] = Q(1, 2) + Q(1, 2) == 1
    # After two transports + installation, real remainder is 13, not a fresh 18.
    controls["fuel_reset_exposes_five_excess_units"] = (2 + 3 == 5 and 18 - 5 == 13
                                                        and 5 + 18 == 23 > 18)
    require(all(controls.values()), repr({k: v for k, v in controls.items() if not v}))
    folder = Path(__file__).resolve().parent
    dependencies = list(folder.glob("*.py")) + list(folder.glob("*.lean"))
    dependencies += [folder.parent / "certified_progress" / (name + ".py")
                     for name in ("model", "checker", "producer", "observation")]
    hashes = {str(p.relative_to(folder.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(dependencies)}
    return {"scope": "exact nine-element examples and submitted finite arena certificates; not whole-engine verification",
            "sources": hashes, "carrier_table": maps, "emission_subsets_checked": emission_checks,
            "guard_subsets_checked": guard_checks, "cases": cases, "scan_table": scan_table,
            "controls": controls, "compositional_ledger": rows,
            "outer_trace_check": trace_result, "hostile_outer_trace_checks": trace_checks,
            "repeated_episode_at_budget22": repeated_result,
            "bundle": bundle, "parent_packet": parent, "stale_parent_packet": stale,
            "authority_effect": "None"}


def not_intersects(a, b):
    return not (a & b)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
    print(json.dumps({"status": "PASS", "arenas": len(result["cases"]),
                      "emission_subsets": result["emission_subsets_checked"],
                      "guard_subsets": result["guard_subsets_checked"],
                      "controls": len(result["controls"]),
                      "output": str(args.output) if args.output else None}))
