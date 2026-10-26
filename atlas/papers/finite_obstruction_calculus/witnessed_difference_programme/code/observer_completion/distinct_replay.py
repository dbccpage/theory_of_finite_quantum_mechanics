"""Independent replay of distinct-image and Chapter 23 witnesses.

No model calls. Checkers do not invoke producers. Run from the paper code
directory:

    python -m observer_completion.distinct_replay
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

from observer_completion.distinct_image import (
    FIELD,
    SOURCE,
    TASK,
    M,
    analyze,
    check_completion,
    inclusion_examples,
    produce_completion,
)
from observer_completion.observer_completion import hc
import toric_code_observer_completion as toric


def _column(*entries):
    return M([[entry] for entry in entries], 1)


def _pack(columns):
    return hc(*columns)


def _base_witness(**overrides):
    source = _column(1, 0, 0)
    repair = _pack([_column(1, 0, 0), _column(0, 1, 0)])
    observer = M([[0, 0, 1]], 3)
    witness = produce_completion(source, repair, observer, "raw")
    witness.update(overrides)
    return source, repair, observer, witness


def _expect_reject(name, function):
    try:
        function()
    except ValueError as error:
        return {"name": name, "rejected": True, "reason": str(error)}
    return {"name": name, "rejected": False, "reason": "accepted"}


def check_inertia_promotion(claim: dict) -> None:
    """A finite list of inertias, including the Gate E point, is not an all-M theorem."""
    receipt_path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "meron_field_limit_derivations"
        / "code"
        / "gate_e_exact_counterexample_receipt.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (
        receipt["r"] != "1/10"
        or receipt["negative_eigenvalue"] != "-1/706440"
        or receipt["quadratic_form_exact"] != "-1/88305"
        or receipt["test_vector"] != [-1, -1, -1, -1, 1, 1, 1, 1]
        or receipt["is_positive_semidefinite"] is not False
    ):
        raise ValueError("gate E receipt changed")
    if F(receipt["r"]) <= F(1, 192):
        raise ValueError("gate E point entered the declared region")
    if claim.get("all_m_from_this_point"):
        raise ValueError("finite_m_promoted_to_all_m")


def check_readout_bound(claim: dict) -> None:
    """A Lieb–Robinson upper bound is not a reconstruction-error floor."""
    if "upper_bound" in claim and claim.get("asserted_floor") is not None:
        raise ValueError("lr_upper_bound_as_error_floor")


def _submit(source, repair, observer, target, rows, minimum, lower):
    facts = analyze(source, repair, observer)
    return {
        "dimensions": {key: facts[key] for key in ("ambient", "raw_minimum", "quotient_minimum", "joint_minimum", "separate_sum")},
        "schema": "wdp-distinct-image-replay-v1",
        "task": TASK,
        "source": SOURCE,
        "field": FIELD,
        "target": target,
        "E": rows.encode(),
        "minimum": minimum,
        "lower_columns": lower.encode(),
        "assumes_equal_images": False,
        "solves_original": False,
    }


def rejection_suite():
    """The fourteen numbered rejection obligations.

    Quotient sufficiency without raw sufficiency and the converse are separate
    witnesses, so the returned list has one entry for each directed failure.
    """
    results = []

    def conflated():
        source, repair, observer, witness = _base_witness(assumes_equal_images=True)
        check_completion(source, repair, observer, witness)

    results.append(_expect_reject("r_and_b_conflated", conflated))

    def blind_direct():
        source = _column(1, 0)
        repair = _column(0, 1)
        observer = M([[0, 0]], 2)
        rows = M([], 2)
        facts = analyze(source, repair, observer)
        check_completion(
            source, repair, observer,
            _submit(source, repair, observer, "raw", rows, facts["raw_minimum"], facts["RK"]),
        )

    results.append(_expect_reject("blind_realizable_defect", blind_direct))

    def quotient_without_raw():
        source = _pack([_column(1, 0, 0), _column(0, 1, 0)])
        repair = _column(1, 0, 0)
        observer = M([[0, 0, 1]], 3)
        quotient = produce_completion(source, repair, observer, "quotient")
        rows = M.decode(quotient["E"])
        facts = analyze(source, repair, observer)
        check_completion(
            source, repair, observer,
            _submit(source, repair, observer, "both", rows, facts["joint_minimum"], facts["RK"]),
        )

    results.append(_expect_reject("quotient_without_raw", quotient_without_raw))

    def raw_without_quotient():
        source = _column(1, 0, 0)
        repair = _column(0, 0, 1)
        observer = M([[0, 0, 1]], 3)
        raw = produce_completion(source, repair, observer, "raw")
        rows = M.decode(raw["E"])
        facts = analyze(source, repair, observer)
        check_completion(
            source, repair, observer,
            _submit(source, repair, observer, "both", rows, facts["joint_minimum"], facts["K"]),
        )

    results.append(_expect_reject("raw_without_quotient", raw_without_quotient))

    def added():
        source = _pack([_column(1, 0, 0), _column(0, 1, 0)])
        repair = _column(1, 0, 0)
        observer = M([[0, 0, 1]], 3)
        facts = analyze(source, repair, observer)
        if facts["separate_sum"] == facts["joint_minimum"]:
            raise RuntimeError("sum coincides with the joint minimum")
        witness = produce_completion(source, repair, observer, "both")
        witness["minimum"] = facts["separate_sum"]
        check_completion(source, repair, observer, witness)

    results.append(_expect_reject("optima_incorrectly_added", added))

    def full_repair():
        source = _column(1, 0)
        repair = hc(_column(1, 0), _column(0, 1))
        observer = M([[1, 0]], 2)
        witness = produce_completion(source, repair, observer, "quotient")
        witness["solves_original"] = True
        check_completion(source, repair, observer, witness)

    results.append(_expect_reject("observation_completion_does_not_certify_repairs", full_repair))

    def wrong_field():
        source, repair, observer, witness = _base_witness(field="real")
        check_completion(source, repair, observer, witness)

    results.append(_expect_reject("wrong_coefficient_field", wrong_field))

    def kernel_is_s():
        report = toric.commutation_kernel_report(3)
        toric.check_kernel_claim({"kernel": "S"}, report)

    results.append(_expect_reject("toric_kernel_identified_with_s", kernel_is_s))

    def rank_as_collision():
        errors = toric.t0_family(toric.pauli_commutation_syndrome(3).shape[1])
        generators = toric.stabilizer_generator_rows(3)
        collision = toric.admitted_collision(
            toric.pauli_commutation_syndrome(3), errors, generators
        )
        report = toric.commutation_kernel_report(3)
        toric.check_rank_defect_claim(
            {"collision_from_global_quotient": True},
            collision,
            report["quotient_dimension"],
        )

    results.append(_expect_reject("rank_defect_as_low_weight_collision", rank_as_collision))

    def t0_full_basis():
        syndrome = toric.pauli_commutation_syndrome(3)
        width = syndrome.shape[1]
        errors = toric.t0_family(width)
        repair = toric.stabilizer_generator_rows(3)
        shelf = [syndrome[row].copy() for row in range(syndrome.shape[0])]
        costs = [F(1)] * len(shelf)
        produced = toric.minimum_cost_suite(shelf, costs, errors, repair)
        if produced["cost"] != 0 or produced["indices"] != tuple():
            raise RuntimeError("t=0 bought a detector")
        # A witness that demands the full check count is not optimal.
        bad = {"feasible": True, "indices": tuple(range(len(shelf))), "cost": F(len(shelf))}
        toric.check_minimum_cost_suite(shelf, costs, errors, repair, bad)

    results.append(_expect_reject("t0_requires_full_detector_basis", t0_full_basis))

    def loses_future():
        toric.current_answer_preserves_future(True, False, True)

    results.append(_expect_reject("current_answer_loses_future_operation", loses_future))

    def false_adaptive():
        gap = toric.passive_adaptive_gap()
        toric.check_adaptive_lower_bound(gap["nonadaptive_cost"])

    results.append(_expect_reject("false_adaptive_lower_bound", false_adaptive))

    def finite_m():
        check_inertia_promotion({"all_m_from_this_point": True})

    results.append(_expect_reject("finite_m_promoted_to_all_m", finite_m))

    def error_floor():
        check_readout_bound({"upper_bound": "2*beta", "asserted_floor": "beta"})

    results.append(_expect_reject("lr_upper_bound_as_error_floor", error_floor))

    def stale():
        source, repair, observer, witness = _base_witness(task="some-other-task")
        check_completion(source, repair, observer, witness)

    results.append(_expect_reject("wrong_task_or_stale_witness", stale))
    return results


def positive_and_negative():
    source = _pack([_column(1, 0, 0), _column(0, 1, 0)])
    repair = _column(1, 0, 0)
    observer = M([[0, 0, 1]], 3)
    good = produce_completion(source, repair, observer, "both")
    # Replay the submitted witness. The checker does not rebuild the rows.
    accepted = check_completion(source, repair, observer, good)
    bad = dict(good)
    bad["E"] = M([], 3).encode()
    try:
        check_completion(source, repair, observer, bad)
    except ValueError as error:
        negative = str(error)
    else:
        negative = "accepted"
    return {"positive": accepted, "negative_reason": negative}


def main():
    payload = {
        "rejections": rejection_suite(),
        "certificates": positive_and_negative(),
        "inclusions": inclusion_examples(),
        "provider_calls": 0,
    }
    failed = [
        item["name"] for item in payload["rejections"]
        if not item["rejected"] or item["reason"] != item["name"]
    ]
    payload["failed"] = failed
    print(json.dumps(payload, indent=2, default=str))
    if failed or payload["certificates"]["negative_reason"] == "accepted":
        raise SystemExit(1)
    if not payload["certificates"]["positive"]["accepted"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
