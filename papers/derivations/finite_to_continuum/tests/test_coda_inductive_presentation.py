"""Tests for the finite cyclic presentation, character sums, and interval enclosures."""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pytest
from coda_inductive_presentation import (
    ContinuumEnclosure,
    CyclicPresentation,
    PontryaginCharacter,
    e_enclosure_sequence,
    generate_inductive_presentation_receipt,
    lift_mark_to_continuum,
    ln2_enclosure_sequence,
    pi_enclosure_sequence,
    sqrt2_enclosure_sequence,
    verify_character_orthogonality,
)
from interval_calculus import RationalInterval


def test_cyclic_presentation_basic() -> None:
    """Verifies finite cyclic presentation G_n structure and inclusions."""
    g2 = CyclicPresentation(2)
    assert g2.level == 2
    assert g2.order == 4
    assert g2.elements == (0, 1, 2, 3)

    assert g2.dyadic_coordinate(0) == Fraction(0, 1)
    assert g2.dyadic_coordinate(1) == Fraction(1, 4)
    assert g2.dyadic_coordinate(2) == Fraction(1, 2)
    assert g2.dyadic_coordinate(3) == Fraction(3, 4)

    g3 = CyclicPresentation(3)
    for el in g2.elements:
        next_el = g2.inclusion_to_next(el)
        assert g2.dyadic_coordinate(el) == g3.dyadic_coordinate(next_el)

    with pytest.raises(TypeError):
        CyclicPresentation(2.5)
    with pytest.raises(TypeError):
        CyclicPresentation(True)
    with pytest.raises(ValueError):
        CyclicPresentation(-1)


def test_pontryagin_character_duality() -> None:
    """Finite character index arithmetic on a cyclic group of order 8."""
    c0 = PontryaginCharacter(3, 0)
    c1 = PontryaginCharacter(3, 1)
    c2 = PontryaginCharacter(3, 2)
    c7 = PontryaginCharacter(3, 7)

    c3 = c1.multiply(c2)
    assert c3.index == 3
    assert c3.level == 3

    c1_conj = c1.conjugate()
    assert c1_conj.index == 7

    re0, im0 = c0.eval_interval(0)
    assert re0.lo == re0.hi == Fraction(1)
    assert im0.lo == im0.hi == Fraction(0)

    re_pi, im_pi = c2.eval_interval(2)
    assert re_pi.lo == re_pi.hi == Fraction(-1)
    assert im_pi.lo == im_pi.hi == Fraction(0)

    c_high = PontryaginCharacter(4, 9)
    c_low = c0.dual_pullback_from_next(c_high)
    assert c_low.level == 3
    assert c_low.index == 9 % 8 == 1


def test_character_orthogonality_haar() -> None:
    """The finite normalized character sum equals the algebraic delta."""
    rec_diag = verify_character_orthogonality(level=2, k=1, j=1)
    assert rec_diag.is_orthogonal
    assert rec_diag.sum_exact_delta == Fraction(1)
    assert rec_diag.real_interval.lo <= Fraction(1) <= rec_diag.real_interval.hi

    rec_off = verify_character_orthogonality(level=2, k=1, j=2)
    assert rec_off.is_orthogonal
    assert rec_off.sum_exact_delta == Fraction(0)
    assert rec_off.real_interval.lo <= Fraction(0) <= rec_off.real_interval.hi

    assert rec_diag.authority_effect == "None"
    assert rec_off.authority_effect == "None"


def test_continuum_enclosures() -> None:
    """Verifies constructive Cauchy contraction for fundamental constants."""
    pi_enc = pi_enclosure_sequence(max_terms=6)
    assert pi_enc.is_cauchy_contractive()
    assert pi_enc.final_width < Fraction(1, 1000)
    assert pi_enc.final_interval.lo < Fraction(31416, 10000)
    assert pi_enc.final_interval.hi > Fraction(31415, 10000)

    e_enc = e_enclosure_sequence(max_order=6)
    assert e_enc.is_cauchy_contractive()
    assert e_enc.final_width < Fraction(1, 100)
    assert e_enc.final_interval.lo < Fraction(272, 100)
    assert e_enc.final_interval.hi > Fraction(271, 100)

    sqrt2_enc = sqrt2_enclosure_sequence(max_steps=5)
    assert sqrt2_enc.is_cauchy_contractive()
    assert sqrt2_enc.final_width < Fraction(1, 1000)
    assert sqrt2_enc.final_interval.lo < Fraction(1415, 1000)
    assert sqrt2_enc.final_interval.hi > Fraction(1414, 1000)

    ln2_enc = ln2_enclosure_sequence(max_order=6)
    assert ln2_enc.is_cauchy_contractive()
    assert ln2_enc.final_width < Fraction(1, 100)
    assert ln2_enc.final_interval.lo < Fraction(70, 100)
    assert ln2_enc.final_interval.hi > Fraction(69, 100)


def test_mark_to_domain_lift() -> None:
    """Verifies Genesis Mark-to-Domain lift and non-authoritative boundary."""
    pi_enc = pi_enclosure_sequence(max_terms=4)
    elem = lift_mark_to_continuum("<pi_constant>", pi_enc)
    assert elem.mark == "<pi_constant>"
    assert elem.is_witness_verified
    assert elem.authority_effect == "None"

    with pytest.raises(ValueError):
        lift_mark_to_continuum("", pi_enc)

    bad_ivs = [
        RationalInterval(Fraction(0), Fraction(1)),
        RationalInterval(Fraction(0), Fraction(2)),
    ]
    bad_enc = ContinuumEnclosure("bad", bad_ivs)
    with pytest.raises(ValueError, match="failed Cauchy"):
        lift_mark_to_continuum("<bad>", bad_enc)


def _body_contains_float(value: object) -> bool:
    if type(value) is float:
        return True
    if type(value) is dict:
        return any(_body_contains_float(item) for item in value.values())
    if type(value) in (list, tuple):
        return any(_body_contains_float(item) for item in value)
    return False


def test_generate_stamped_receipt() -> None:
    """The digest is the sorted body, and the file matches the writer."""
    receipt = generate_inductive_presentation_receipt()
    assert receipt["schema"] == "omega.coda.inductive_presentation.v1"
    assert receipt["authority_effect"] == "None"
    body = {key: value for key, value in receipt.items() if key != "evidence_sha256"}
    assert receipt["zero_float_law_verified"] is (not _body_contains_float(body))
    raw = json.dumps(body, sort_keys=True, indent=2)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    assert receipt["evidence_sha256"] == digest

    receipt_path = (
        Path(__file__).resolve().parent.parent
        / "results"
        / "inductive_presentation_receipt.json"
    )
    raw_bytes = receipt_path.read_bytes()
    assert b"\r" not in raw_bytes
    assert raw_bytes.decode("utf-8") == json.dumps(receipt, indent=2) + "\n"


def test_edge_cases_and_error_paths() -> None:
    """Tests out-of-bounds, type mismatches, and contractive checks for 100% coverage."""
    from coda_inductive_presentation import _contains_float, constructive_cauchy_completion

    g = CyclicPresentation(2)
    with pytest.raises(ValueError, match="out of bounds"):
        g.inclusion_to_next(-1)
    with pytest.raises(ValueError, match="out of bounds"):
        g.inclusion_to_next(4)
    with pytest.raises(ValueError, match="out of bounds"):
        g.dyadic_coordinate(-1)
    with pytest.raises(ValueError, match="out of bounds"):
        g.dyadic_coordinate(4)

    c1 = PontryaginCharacter(2, 1)
    c2 = PontryaginCharacter(3, 1)
    with pytest.raises(ValueError, match="Cannot multiply characters of different levels"):
        c1.multiply(c2)
    with pytest.raises(ValueError, match="Higher character must be at level 3"):
        c1.dual_pullback_from_next(c1)

    with pytest.raises(ValueError, match="requires at least one interval"):
        ContinuumEnclosure("empty", [])
    with pytest.raises(TypeError, match="must be RationalInterval"):
        ContinuumEnclosure("bad_type", [Fraction(1, 2)])

    disjoint = ContinuumEnclosure(
        "disjoint",
        [
            RationalInterval(Fraction(0), Fraction(1)),
            RationalInterval(Fraction(2), Fraction(3)),
        ],
    )
    assert not disjoint.is_cauchy_contractive()

    with pytest.raises(ValueError, match="Steps must be >= 1"):
        constructive_cauchy_completion("zero_steps", lambda n: RationalInterval(Fraction(0), Fraction(1)), steps=0)

    comp = constructive_cauchy_completion(
        "half_seq",
        lambda n: RationalInterval(Fraction(0), Fraction(1, 2**n)),
        steps=4,
    )
    assert comp.steps == 4
    assert comp.final_width == Fraction(1, 8)

    comp_jump = constructive_cauchy_completion(
        "jump_seq",
        lambda n: RationalInterval(Fraction(n * 10), Fraction(n * 10 + 1)),
        steps=2,
    )
    assert comp_jump.steps == 2

    assert _contains_float(3.14)
    assert _contains_float({"key": 2.71})
    assert _contains_float([Fraction(1, 2), 1.41])
    assert not _contains_float({"key": Fraction(1, 2), "list": [1, 2, Fraction(3, 4)]})
