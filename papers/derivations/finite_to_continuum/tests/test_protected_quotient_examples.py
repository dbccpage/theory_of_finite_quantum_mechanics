"""Exact finite evidence for the dense protected-subgroup countermodel."""

from fractions import Fraction

import pytest

from omega_engine_projects.finite_to_continuum.code.coda_inductive_presentation import (
    CyclicPresentation,
)
from omega_engine_projects.finite_to_continuum.code.protected_quotient_examples import (
    crt_residue,
    discontinuity_point,
    protected_quotient_witness,
    replay,
    six_coordinate,
    six_coordinates,
    six_transition,
    three_primary_character,
    verify_protected_witness,
)


def test_crt_uniqueness_and_all_tested_transition_maps():
    for n in range(5):
        order = 6**n
        candidates = [a for a in range(order) if a % (2**n) == 0 and (a - 1) % (3**n) == 0]
        assert candidates == [crt_residue(n)]
        assert crt_residue(n + 1) % order == crt_residue(n)
        for k in range(order):
            higher = six_transition(n, k)
            assert six_coordinate(n, k) == six_coordinate(n + 1, higher)
            assert Fraction(crt_residue(n) * k, order) % 1 == (
                Fraction(crt_residue(n + 1) * higher, 6 * order) % 1
            )


def test_homomorphism_law_on_small_finite_carriers():
    for n in range(4):
        points = [six_coordinate(n, k) for k in range(6**n)]
        images = [three_primary_character(x) for x in points]
        for i, x in enumerate(points):
            for j, y in enumerate(points):
                assert three_primary_character(x + y) == (images[i] + images[j]) % 1


def test_existing_dyadic_owner_is_annihilated_and_third_is_not():
    for n in range(9):
        dyadic, higher = CyclicPresentation(n), CyclicPresentation(n + 1)
        for k in dyadic.elements:
            x = dyadic.dyadic_coordinate(k)
            assert x == higher.dyadic_coordinate(dyadic.inclusion_to_next(k))
            assert x == six_coordinate(n, k * 3**n)
            assert three_primary_character(x) == 0
    assert three_primary_character(Fraction(1, 3)) == Fraction(1, 3)


def test_sequence_formula_and_supplied_delta_witnesses():
    for n in range(1, 101):
        x = discontinuity_point(n)
        assert x == Fraction((2**n) % 3, 3 * 2**n)
        assert 0 < x < Fraction(1, 2**n)
        assert three_primary_character(x) == Fraction(1, 3)
        level, numerator = six_coordinates(x)
        assert six_coordinate(level, numerator) == x
    for delta in (2, Fraction(1, 3), Fraction(1, 4), Fraction(1, 10**200)):
        witness = protected_quotient_witness(delta)
        assert verify_protected_witness(witness) is True
        assert 0 < witness["point"] < delta


@pytest.mark.parametrize(
    "field,replacement",
    [
        ("residue", 1),
        ("next_residue", 0),
        ("next_numerator", 1),
        ("character_value", Fraction(0)),
        ("point", Fraction(1, 5)),
        ("point", Fraction(1, 3)),
        ("topology", "discrete"),
        ("obstruction", "PASS"),
        ("epsilon", Fraction(1, 6)),
        ("delta", Fraction(0)),
        ("level", True),
        ("numerator", 0.5),
        ("character_value", True),
    ],
)
def test_independent_verifier_rejects_mutations_without_repair(field, replacement):
    witness = protected_quotient_witness(Fraction(1, 8))
    witness[field] = replacement
    before = dict(witness)
    assert verify_protected_witness(witness) is False
    assert witness == before


def test_missing_extra_fields_and_strict_delta_boundary():
    witness = protected_quotient_witness(Fraction(1, 8))
    witness["delta"] = witness["point"]
    assert verify_protected_witness(witness) is False
    del witness["residue"]
    assert verify_protected_witness(witness) is False
    witness = protected_quotient_witness(1)
    witness["unused"] = 1
    assert verify_protected_witness(witness) is False


@pytest.mark.parametrize("bad", [True, False, 0.1, complex(1), "not-a-rational"])
def test_exact_type_boundaries(bad):
    for function in (crt_residue, discontinuity_point, protected_quotient_witness, six_coordinates):
        with pytest.raises(TypeError):
            function(bad)


def test_invalid_carrier_and_nonpositive_inputs():
    for x in (Fraction(1, 5), Fraction(1, 7), Fraction(1, 10)):
        with pytest.raises(ValueError):
            three_primary_character(x)
    for delta in (0, -1):
        with pytest.raises(ValueError):
            protected_quotient_witness(delta)
    with pytest.raises(ValueError):
        crt_residue(-1)
    with pytest.raises(ValueError):
        discontinuity_point(0)
    with pytest.raises(ValueError):
        six_coordinate(2, 36)
    assert three_primary_character(-Fraction(1, 3)) == Fraction(2, 3)


def test_existing_exact_string_contract_and_integer_level_boundary():
    assert three_primary_character("1/3") == Fraction(1, 3)
    assert verify_protected_witness(protected_quotient_witness("1/100")) is True
    with pytest.raises(TypeError):
        crt_residue("1")


def test_replay_scope_is_finite():
    result = replay()
    assert result["status"] == "PASS"
    assert result["infinite_quantifiers_checked"] is False
