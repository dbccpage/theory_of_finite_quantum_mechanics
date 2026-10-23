from fractions import Fraction
from itertools import permutations, product

import pytest
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.projective import (
    I_UNIT,
    IDENTITY,
    ONE,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    UNIT_PHASES_Z4,
    ZERO,
    GaussianRational,
    Matrix2,
    ProjectiveRepresentation,
    commutator_ratio,
    klein_four_pauli,
    matrix2,
    projective_cocycle,
    rephase,
    verify_cocycle_identity,
)

RATIONAL_UNIT_POINTS = (
    GaussianRational(Fraction(3, 5), Fraction(4, 5)),
    GaussianRational(Fraction(5, 13), Fraction(-12, 13)),
    GaussianRational(Fraction(-8, 17), Fraction(15, 17)),
)


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def test_gaussian_rational_arithmetic_is_exact() -> None:
    assert I_UNIT * I_UNIT == -ONE
    z = GaussianRational("1/2", -3)
    assert z * z.conjugate() == GaussianRational(z.norm_squared())
    assert (z / z) == ONE and (ONE / I_UNIT) == -I_UNIT
    assert z + (-z) == ZERO and type(z.real) is Fraction and type(z.imag) is Fraction
    assert all(point.norm_squared() == 1 for point in RATIONAL_UNIT_POINTS + UNIT_PHASES_Z4)
    with pytest.raises(ZeroDivisionError):
        ONE / ZERO
    for bad in (0.5, True):
        with pytest.raises(TypeError):
            GaussianRational(bad)


def test_matrix_validation_and_pauli_products() -> None:
    for entries in ((ONE, ONE, ONE), [ONE] * 4, (ONE, ONE, ONE, 1)):
        with pytest.raises(ValueError):
            Matrix2(entries)
    assert SIGMA_X @ SIGMA_Z == SIGMA_Y.scaled(-I_UNIT)
    assert SIGMA_X @ SIGMA_Z != SIGMA_Y.scaled(-ONE)
    assert SIGMA_Z @ SIGMA_X == SIGMA_Y.scaled(I_UNIT)
    for sigma in (SIGMA_X, SIGMA_Y, SIGMA_Z):
        assert sigma @ sigma == IDENTITY and sigma.is_unitary() and sigma.adjoint() == sigma
    assert not matrix2(1, 1, 0, 1).is_unitary()


def test_klein_four_pauli_cocycle_table() -> None:
    representation = klein_four_pauli()
    omega = accepted(projective_cocycle(representation))
    assert omega[("x", "z")] == -I_UNIT and omega[("z", "x")] == I_UNIT
    assert omega[("x", "x")] == omega[("z", "z")] == omega[("xz", "xz")] == ONE
    assert omega[("xz", "x")] == -I_UNIT and omega[("x", "xz")] == I_UNIT
    assert all(omega[("e", g)] == omega[(g, "e")] == ONE for g in representation.elements)
    assert all(value.norm_squared() == 1 for value in omega.values())
    assert accepted(verify_cocycle_identity(representation, omega)) == 64
    assert accepted(commutator_ratio(representation, "x", "z")) == -ONE
    assert accepted(commutator_ratio(representation, "x", "x")) == ONE


def test_commutator_ratio_is_invariant_under_every_z4_rephasing() -> None:
    representation = klein_four_pauli()
    base = accepted(projective_cocycle(representation))
    for phases in product(UNIT_PHASES_Z4, repeat=4):
        lam = dict(zip(representation.elements, phases))
        moved = accepted(rephase(representation, lam))
        omega = accepted(projective_cocycle(moved))
        assert accepted(verify_cocycle_identity(moved, omega)) == 64
        assert accepted(commutator_ratio(moved, "x", "z")) == -ONE
        for (g, h), value in omega.items():
            assert value == base[(g, h)] * lam[g] * lam[h] / lam[representation.product[(g, h)]]


def test_commutator_ratio_is_invariant_under_rational_unit_rephasings() -> None:
    representation = klein_four_pauli()
    for phases in product(RATIONAL_UNIT_POINTS + (ONE,), repeat=4):
        moved = accepted(rephase(representation, dict(zip(representation.elements, phases))))
        assert accepted(commutator_ratio(moved, "z", "x")) == -ONE


def test_rephasing_refusals() -> None:
    representation = klein_four_pauli()
    elements = representation.elements
    refused(rephase(representation, dict.fromkeys(elements, GaussianRational(1, 1))), RefusalCode.NON_UNIT_PHASE)
    refused(rephase(representation, dict.fromkeys(elements, GaussianRational(2))), RefusalCode.NON_UNIT_PHASE)
    refused(rephase(representation, {"e": ONE}), RefusalCode.INVALID_INPUT)
    refused(rephase(representation, dict.fromkeys(elements, 1)), RefusalCode.INVALID_INPUT)
    refused(rephase("rep", {}), RefusalCode.INVALID_INPUT)


def _z2(matrices) -> ProjectiveRepresentation:
    table = {("e", "e"): "e", ("e", "g"): "g", ("g", "e"): "g", ("g", "g"): "e"}
    return ProjectiveRepresentation(("e", "g"), table, matrices)


def test_non_unitary_and_non_projective_inputs_are_refused() -> None:
    non_unitary = _z2({"e": IDENTITY, "g": matrix2(1, 1, 0, 1)})
    refused(projective_cocycle(non_unitary), RefusalCode.NOT_PROJECTIVE, "unitary")
    refused(commutator_ratio(non_unitary, "g", "g"), RefusalCode.NOT_PROJECTIVE)
    non_projective = _z2({"e": SIGMA_X, "g": IDENTITY})
    refused(projective_cocycle(non_projective), RefusalCode.NOT_PROJECTIVE, "phase times")
    linear = accepted(projective_cocycle(_z2({"e": IDENTITY, "g": SIGMA_Z})))
    assert set(linear.values()) == {ONE}
    for function in (projective_cocycle, lambda rep: commutator_ratio(rep, "x", "z")):
        refused(function("rep"), RefusalCode.INVALID_INPUT)
    refused(verify_cocycle_identity("rep", {}), RefusalCode.INVALID_INPUT)


def test_tampered_phase_tables_fail_the_cocycle_identity() -> None:
    representation = klein_four_pauli()
    omega = accepted(projective_cocycle(representation))
    refused(
        verify_cocycle_identity(representation, {**omega, ("x", "z"): ONE}),
        RefusalCode.CERTIFICATE_MISMATCH,
        "2-cocycle identity",
    )
    refused(verify_cocycle_identity(representation, {("e", "e"): ONE}), RefusalCode.INVALID_INPUT)
    refused(verify_cocycle_identity(representation, {**omega, ("x", "z"): -1}), RefusalCode.INVALID_INPUT)


def test_projective_representation_post_construction_mutation_prevented() -> None:
    labels = ("0", "1")
    table = {(a, b): str(int(a) ^ int(b)) for a in labels for b in labels}
    rep = ProjectiveRepresentation(labels, table, {a: IDENTITY for a in labels})
    table[("0", "0")] = "1"
    assert rep.product[("0", "0")] == "0"
    with pytest.raises(TypeError):
        rep.product[("0", "0")] = "1"


def _s3_trivial() -> ProjectiveRepresentation:
    elements = tuple(permutations(range(3)))
    names = {permutation: "".join(map(str, permutation)) for permutation in elements}
    table = {
        (names[p], names[q]): names[tuple(p[q[i]] for i in range(3))] for p in elements for q in elements
    }
    return ProjectiveRepresentation(tuple(names.values()), table, dict.fromkeys(names.values(), IDENTITY))


def test_commutator_ratio_scope_refusals() -> None:
    s3 = _s3_trivial()
    refused(commutator_ratio(s3, "102", "021"), RefusalCode.INVALID_INPUT, "commuting")
    refused(commutator_ratio(klein_four_pauli(), "x", "y"), RefusalCode.OUTSIDE_CARRIER)
    assert accepted(commutator_ratio(s3, "012", "102")) == ONE


@pytest.mark.parametrize(
    ("elements", "table", "matrices", "message"),
    [
        (("e", "e"), {}, {}, "unique"),
        ((), {}, {}, "unique"),
        (("e",), {}, {"e": IDENTITY}, "total"),
        (("e",), {("e", "e"): "f"}, {"e": IDENTITY}, "closed"),
        (("e",), {("e", "e"): "e"}, {}, "matrix"),
        (("e",), {("e", "e"): "e"}, {"e": "I"}, "matrix"),
    ],
)
def test_representation_validation(elements, table, matrices, message) -> None:
    with pytest.raises(ValueError, match=message):
        ProjectiveRepresentation(elements, table, matrices)


def test_non_associative_tables_are_refused() -> None:
    table = {("a", "a"): "b", ("a", "b"): "a", ("b", "a"): "b", ("b", "b"): "b"}
    with pytest.raises(ValueError, match="associative"):
        ProjectiveRepresentation(("a", "b"), table, {"a": IDENTITY, "b": IDENTITY})
# Executable finite evidence; AuthorityEffect: None.
