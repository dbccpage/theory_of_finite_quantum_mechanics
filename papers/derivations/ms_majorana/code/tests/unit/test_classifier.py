from __future__ import annotations

"""Invariants for the end-to-end residual classifier.

`TypedHarmonic` must be *earned*: it is `ClosedResidual` plus a certified-exact
l1 minimum and a determined class. If the search is capped, the terminal must
fall back rather than assert exactness it did not compute.
"""


import random

import pytest

from omega_engine.crates.majorana.carriers.surface_carrier import (
    build_tetron_array,
    logical_class_representative,
)
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.engines.classifier import (
    TERMINALS,
    classify,
    classify_carrier,
)
from omega_engine.crates.majorana.engines.terminalizer import terminalize


def _random_residuals(count: int, length: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randint(0, 1) for _ in range(length)] for _ in range(count)]




@pytest.mark.parametrize("topology", ["disk", "cylinder", "torus"])
def test_base_three_way_split_is_unchanged(topology: str) -> None:
    """classify() refines terminalize(); it must never contradict it."""
    carrier, report = build_tetron_array(3, 3, topology)
    for residual in _random_residuals(24, report.num_channels, seed=11):
        base = terminalize(carrier.D0, carrier.D1, residual)
        refined = classify(carrier.D0, carrier.D1, residual)
        if base["terminal_status"] == "ClosedResidual":
            assert refined["terminal_status"] in ("ClosedResidual", "TypedHarmonic")
        else:
            assert refined["terminal_status"] == base["terminal_status"]




def test_disk_never_yields_a_closed_or_typed_residual() -> None:
    """H^1 = 0, so every closed residual is exact. This is the old behaviour,
    and here it is *correct* -- an open tetron array has no protected error."""
    carrier, report = build_tetron_array(3, 3, "disk")
    seen = set()
    for residual in _random_residuals(200, report.num_channels, seed=3):
        seen.add(classify(carrier.D0, carrier.D1, residual)["terminal_status"])
    assert seen <= {"Exact", "OpenObstruction"}
    assert "ClosedResidual" not in seen and "TypedHarmonic" not in seen




def test_torus_reaches_every_terminal() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    seen = set()

    alpha = [0] * report.num_mzm
    alpha[0] = 1
    seen.add(classify(carrier.D0, carrier.D1, d0.mat_vec_mul(alpha))["terminal_status"])

    single = [0] * report.num_channels
    single[0] = 1
    seen.add(classify(carrier.D0, carrier.D1, single)["terminal_status"])

    logical = logical_class_representative(report, axis="column", index=0)
    seen.add(classify(carrier.D0, carrier.D1, logical)["terminal_status"])

    seen.add(
        classify(carrier.D0, carrier.D1, logical, budget=4)["terminal_status"]
    )

    assert seen == {"Exact", "OpenObstruction", "TypedHarmonic", "ClosedResidual"}
    assert seen <= set(TERMINALS)




@pytest.mark.parametrize("axis,index", [("column", 0), ("row", 0), ("column", 1)])
def test_typed_harmonic_certificate_is_complete(axis: str, index: int) -> None:
    carrier, report = build_tetron_array(3, 4, "torus")
    residual = logical_class_representative(report, axis=axis, index=index)
    cert = classify(carrier.D0, carrier.D1, residual)

    assert cert["terminal_status"] == "TypedHarmonic"
    assert cert["phi1_exact"] is True
    assert cert["class_coordinates"] is not None
    assert any(cert["class_coordinates"]), "a typed class must be nonzero"
    assert cert["class_id"] is not None and cert["class_id"].startswith("h1:")
    assert cert["phi1_weight"] == sum(cert["phi1_representative"])
    assert cert["phi1_verified"] is True
    assert cert["dim_h1"] == 2


def test_capped_search_falls_back_and_never_claims_exactness() -> None:
    carrier, report = build_tetron_array(3, 4, "torus")
    residual = logical_class_representative(report, axis="column", index=0)

    capped = classify(carrier.D0, carrier.D1, residual, budget=4)
    assert capped["terminal_status"] == "ClosedResidual"
    assert capped["phi1_exact"] is False
    assert any(capped["class_coordinates"])
    assert capped["phi1_weight"] >= classify(
        carrier.D0, carrier.D1, residual
    )["phi1_weight"]




def test_exact_residual_has_zero_class_and_zero_phi1() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    alpha = [0] * report.num_mzm
    alpha[3] = 1
    cert = classify(carrier.D0, carrier.D1, d0.mat_vec_mul(alpha))
    assert cert["terminal_status"] == "Exact"
    assert cert["class_coordinates"] == [0, 0]
    assert cert["class_id"] == "h1:00"
    assert cert["phi1_weight"] == 0


def test_open_obstruction_has_no_class_but_still_has_phi1() -> None:
    """Outside ker d1 there is no cohomology class, but Phi_1 is still defined:
    the weight left after the best MZM reference-frame choice."""
    carrier, report = build_tetron_array(3, 3, "torus")
    residual = [0] * report.num_channels
    residual[5] = 1
    cert = classify(carrier.D0, carrier.D1, residual)
    assert cert["terminal_status"] == "OpenObstruction"
    assert cert["class_coordinates"] is None
    assert cert["class_id"] is None
    assert any(cert["coherence_witness"])
    assert cert["phi1_weight"] == 1
    assert cert["phi1_exact"] is True


def test_representation_invalid_passes_through() -> None:
    d0 = [[1, 0], [0, 1]]
    d1 = [[1, 0]]
    cert = classify(d0, d1, [1, 0])
    assert cert["terminal_status"] == "RepresentationInvalid"
    assert cert["class_coordinates"] is None
    assert cert["authority_effect"] == "None"




def test_phi1_never_exceeds_the_rref_normal_form_weight() -> None:
    """The RREF normal form is a canonical coset representative, not a minimal
    one. Phi_1 must dominate it, and must strictly beat it somewhere."""
    carrier, report = build_tetron_array(3, 4, "torus")
    strictly_better = 0
    for residual in _random_residuals(60, report.num_channels, seed=808):
        cert = classify(carrier.D0, carrier.D1, residual)
        if cert["phi1_weight"] is None or cert["q1_norm"] is None:
            continue
        assert cert["phi1_weight"] <= cert["q1_norm"]
        if cert["phi1_weight"] < cert["q1_norm"]:
            strictly_better += 1
    assert strictly_better > 0, (
        "l1 projection must improve on the RREF representative somewhere, "
        "otherwise it adds nothing"
    )


def test_rref_already_attains_phi1_on_closed_residuals() -> None:
    """Tripwire for an observed regularity, NOT a theorem.

    Exhaustively over every closed coset of every carrier below, the RREF
    normal form already has minimum weight, so Phi_1 adds a *certificate* and a
    *class label* there rather than a smaller number. It is Phi_1's strict
    advantage on non-closed residuals (the test above) that justifies the
    search. This was measured on 16 closed cosets across 5 carriers -- a small
    sample. If a future carrier breaks it, that is a finding, not a bug: the
    conjecture would be refuted and the claim ledger must be updated.
    """
    from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix as _G

    for topology, rows, cols in (
        ("cylinder", 2, 2),
        ("torus", 2, 2),
        ("torus", 2, 3),
        ("torus", 3, 3),
    ):
        carrier, report = build_tetron_array(rows, cols, topology)
        kernel = _G(carrier.D1, cols=report.num_channels).kernel_basis()
        for code in range(1 << len(kernel)):
            residual = [0] * report.num_channels
            for index, vector in enumerate(kernel):
                if (code >> index) & 1:
                    residual = [a ^ b for a, b in zip(residual, vector)]
            cert = classify(carrier.D0, carrier.D1, residual)
            assert cert["phi1_weight"] == cert["q1_norm"], (
                f"{topology} {rows}x{cols}: RREF weight {cert['q1_norm']} != "
                f"Phi_1 {cert['phi1_weight']} -- regularity refuted, update the "
                f"claim ledger"
            )




@pytest.mark.parametrize("topology", ["disk", "cylinder", "torus"])
def test_every_certificate_is_authority_effect_none(topology: str) -> None:
    carrier, report = build_tetron_array(2, 3, topology)
    for residual in _random_residuals(40, report.num_channels, seed=5150):
        cert = classify(carrier.D0, carrier.D1, residual)
        assert cert["authority_effect"] == "None"
        assert cert["terminal_status"] in TERMINALS


def test_classification_is_deterministic() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    for residual in _random_residuals(12, report.num_channels, seed=64):
        first = classify(carrier.D0, carrier.D1, residual)
        second = classify(carrier.D0, carrier.D1, residual)
        assert first == second


def test_classify_carrier_matches_classify() -> None:
    residual_seed = _random_residuals(1, 24, seed=1)[0]
    carrier, _ = build_tetron_array(3, 4, "torus", residual=residual_seed)
    assert classify_carrier(carrier) == classify(
        carrier.D0, carrier.D1, carrier.residual
    )


def test_class_id_is_stable_across_representatives_of_one_class() -> None:
    """The type is a property of the class, not of the representative."""
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    logical = logical_class_representative(report, axis="row", index=0)
    baseline = classify(carrier.D0, carrier.D1, logical)
    rng = random.Random(2718)
    for _ in range(6):
        alpha = [rng.randint(0, 1) for _ in range(report.num_mzm)]
        shifted = [a ^ b for a, b in zip(logical, d0.mat_vec_mul(alpha))]
        moved = classify(carrier.D0, carrier.D1, shifted)
        assert moved["class_id"] == baseline["class_id"]
        assert moved["phi1_weight"] == baseline["phi1_weight"]



