"""Produce, independently replay and challenge finite observation certificates."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction

from certified_progress.checker import check_certificate
from certified_progress.model import digest
from certified_progress.producer import solve_progress
from .core import construct, coordinate_example, example, fixed_suite_cost
from .checker import check_construction


def run_case(instance):
    original = copy.deepcopy(instance)
    built = construct(original)
    submitted = solve_progress(built["model"])["certificate"]
    # Reconstruct from the original input for the checker; it imports no search code.
    rebuilt = construct(original)
    construction_check = check_construction(original, rebuilt)
    checked = check_certificate(rebuilt["model"], submitted)
    if not checked["accepted"]:
        raise RuntimeError(checked)
    value = next((row["value"] for row in submitted["values"] if row["belief"] == ["n0"]), None)
    return {"input": original, "input_sha256": digest(original), "compiled": rebuilt,
            "certificate": submitted, "construction_checker": construction_check,
            "checker": checked, "initial_value": value}


def replay():
    cases = {
        "recoverable_disturbance": run_case(example()),
        "non_disturbing_only": run_case(example(flip=False, restore=False)),
        "expensive_restore": run_case(example(restore_cost="4")),
        "unrecoverable_disturbance": run_case(example(safe=False, restore=False)),
        "independent_coordinates": run_case(coordinate_example()),
    }
    expected = {"recoverable_disturbance": "15/4", "non_disturbing_only": "4",
                "expensive_restore": "4", "unrecoverable_disturbance": None,
                "independent_coordinates": "3"}
    for name, case in cases.items():
        if case["initial_value"] != expected[name]:
            raise RuntimeError((name, case["initial_value"], expected[name]))
    base = cases["recoverable_disturbance"]
    controls = {}
    changed = copy.deepcopy(base["input"])
    for row in changed["rows"]:
        if row["action"] == "restore":
            row["cost"] = "4"
    controls["changed_price_rejects_old_certificate"] = not check_certificate(
        construct(changed)["model"], base["certificate"])["accepted"]
    forged = copy.deepcopy(base["certificate"])
    next(r for r in forged["values"] if r["belief"] == ["n0"])["value"] = "1"
    controls["forged_lower_bound_rejected"] = not check_certificate(base["compiled"]["model"], forged)["accepted"]
    forged = copy.deepcopy(base["certificate"])
    terminal = next(r for r in forged["values"] if r["value"] == "0")
    terminal["value"] = "100"
    controls["nonzero_terminal_rejected"] = not check_certificate(base["compiled"]["model"], forged)["accepted"]
    changed = copy.deepcopy(base["input"])
    changed["protected_class"]["A00"] = changed["protected_class"]["B00"]
    try:
        construct(changed)
    except ValueError:
        controls["fabricated_future_quotient_rejected"] = True
    else:
        controls["fabricated_future_quotient_rejected"] = False
    changed = copy.deepcopy(base["input"])
    for row in changed["rows"]:
        if row["action"] == "flip_read":
            row["reports"] = {s: "*" for s in row["successors"]}
    controls["changed_report_rejects_old_certificate"] = not check_certificate(
        construct(changed)["model"], base["certificate"])["accepted"]
    changed = copy.deepcopy(base["input"])
    changed["rows"] = [row for row in changed["rows"] if not (
        row["action"] == "restore" and row["state"] == "A01")]
    controls["changed_guard_rejects_old_certificate"] = not check_certificate(
        construct(changed)["model"], base["certificate"])["accepted"]
    answer_model = construct(base["input"], answers_only=True)["model"]
    answer_certificate = solve_progress(answer_model)["certificate"]
    answer_check = check_certificate(answer_model, answer_certificate)
    answer_cost = next(r["value"] for r in answer_certificate["values"] if r["belief"] == ["n0"])
    controls["current_information_does_not_preserve_futures"] = answer_check["accepted"] and answer_cost == "7/2"
    # A non-splitting repair still changes the original/current relation and can be essential.
    useful_restore = False
    for row in base["certificate"]["strategy"]:
        if row["action"] != "restore":
            continue
        node = row["belief"][0]
        relation = base["compiled"]["relations"][node]
        moves = next(r for r in base["compiled"]["model"]["transitions"]
                     if r["state"] == node and r["action"] == "restore")
        if len(moves["successors"]) == 1:
            child = base["compiled"]["relations"][moves["successors"][0]]
            useful_restore |= len(relation) == len(child)
    controls["non_splitting_restore_is_retained"] = useful_restore
    # Same current state does not erase two different original states.
    collision = (("A00", "A00"), ("B00", "A00"))
    controls["original_anchor_survives_a_current_state_collision"] = (
        len({base["input"]["protected_class"][x] for x, _ in collision}) == 2
        and len({y for _, y in collision}) == 1)
    bad_construction = copy.deepcopy(base["compiled"])
    bad_construction["relations"]["n0"].pop()
    try:
        check_construction(base["input"], bad_construction)
    except AssertionError:
        controls["omitted_original_state_rejected"] = True
    else:
        controls["omitted_original_state_rejected"] = False
    safe_cost, suite = fixed_suite_cost(base["input"])
    coordinate_cost, coordinate_suite = fixed_suite_cost(cases["independent_coordinates"]["input"])
    controls["strict_static_dynamic_gap"] = safe_cost == Fraction(6) and Fraction(4) < safe_cost
    controls["static_dynamic_coordinate_equality"] = coordinate_cost == Fraction(3)
    if not all(controls.values()):
        raise RuntimeError({k: v for k, v in controls.items() if not v})
    sources = {str(p.name): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in (Path(__file__), Path(__file__).with_name("core.py"), Path(__file__).with_name("checker.py"))}
    return {"cases": cases, "controls": controls, "answer_only_cost": answer_cost,
            "fixed_suite": {"cost": str(safe_cost), "actions": list(suite)},
            "coordinate_fixed_suite": {"cost": str(coordinate_cost), "actions": list(coordinate_suite)},
            "source_sha256": sources, "authority_effect": "None"}


def main():
    if not __debug__:
        raise RuntimeError("optimized Python disables construction assertions")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = replay()
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write("\n")
    print(json.dumps({"values": {k: v["initial_value"] for k, v in result["cases"].items()},
                      "controls": result["controls"], "fixed_suite": result["fixed_suite"],
                      "answer_only_cost": result["answer_only_cost"]}, sort_keys=True))


if __name__ == "__main__":
    main()
