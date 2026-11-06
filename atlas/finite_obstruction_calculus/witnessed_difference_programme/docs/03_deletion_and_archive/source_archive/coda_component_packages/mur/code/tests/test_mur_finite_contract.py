"""Regressions for the finite verification and evidence boundaries."""
from dataclasses import replace
from itertools import product

import pytest
from coda_mur_core import (
    DescentSquareCertificate,
    FiniteCoreAction,
    LossLedger,
    MorphismKind,
    TerminalRegime,
    compute_transport_quotient_obstruction,
    evaluate_transport_authority,
    paste_certificates,
)
from sympy import Matrix, Rational


def square(**changes):
    fields = dict(
        source_regime="A", target_regime="B", morphism_name="id",
        morphism_kind=MorphismKind.EXACT, chi_certified=True,
        carrier=("a", "b"), state_map=lambda x: x,
        source_look=lambda x: x, target_look=lambda x: x,
        observation_map=lambda x: x,
    )
    fields.update(changes)
    return DescentSquareCertificate(**fields)


def target():
    return TerminalRegime("B", lambda x: "term:" + x, lambda _: True)


def fail(_):
    raise LookupError("undefined")


@pytest.mark.parametrize("missing", ["carrier", "state_map", "source_look", "target_look", "observation_map"])
def test_verified_transport_requires_complete_finite_square(missing):
    cert = square(**{missing: None})
    assert not cert.verify()
    assert not cert.is_valid()
    assert evaluate_transport_authority("a", target(), "a", cert).refusal_code == "R_notransport"
    flags = DescentSquareCertificate("A", "B", "flags", MorphismKind.EXACT, True)
    assert not flags.verify()
    assert not evaluate_transport_authority("a", target(), "unrelated", flags).inhabited
    assert not square(carrier=()).verify()
    assert not square(state_map=fail).verify()


def test_requested_source_and_artifact_are_verified_without_action():
    cert = square()
    assert evaluate_transport_authority("a", target(), None, cert).inhabited
    assert evaluate_transport_authority("a", target(), "b", cert).refusal_code == "R_substituted_artifact"
    # The requested source extends the checked finite set; it cannot bypass maps.
    bad_outside = square(target_look=lambda x: "wrong" if x == "outside" else x)
    assert bad_outside.verify()
    assert evaluate_transport_authority("outside", target(), "outside", bad_outside).refusal_code == "R_notransport"
    undefined_outside = square(state_map=lambda x: fail(x) if x == "outside" else x)
    assert evaluate_transport_authority("outside", target(), None, undefined_outside).refusal_code == "R_notransport"
    for mapping in (lambda x: "substitute", fail):
        action = FiniteCoreAction("A", "B", mapping)
        assert evaluate_transport_authority("a", target(), None, cert, action=action).refusal_code == "R_substituted_artifact"


def test_quotient_must_match_both_declared_cochain_and_repair_model():
    cochain = Matrix([0, 0])
    declared = Matrix([[1], [-1]])
    q = compute_transport_quotient_obstruction(declared, cochain)
    cert = square(defect_vector=cochain, repair_map=declared)
    assert evaluate_transport_authority("a", target(), "a", cert, q).inhabited
    for altered in (square(), replace(cert, repair_map=None),
                    replace(cert, repair_map=Matrix([[1], [1]])),
                    replace(cert, defect_vector=Matrix([1, -1]))):
        assert evaluate_transport_authority("a", target(), "a", altered, q).refusal_code == "R_malformed_quotient"
    assert evaluate_transport_authority("a", target(), "a", cert, object()).refusal_code == "R_malformed_quotient"
    positive = square(defect_vector=Matrix([1]))
    assert evaluate_transport_authority("a", target(), "a", positive).refusal_code == "R_obstruction"


def test_pasting_preserves_declared_repair_model_and_rejects_mismatch():
    model = Matrix([[1]])
    f = square(defect_vector=Matrix([2]), repair_map=model)
    g = square(source_regime="B", target_regime="C", defect_vector=Matrix([3]), repair_map=model)
    composite = paste_certificates(f, g)
    assert composite.defect_vector == Matrix([5])
    assert composite.repair_map == model
    assert paste_certificates(square(), g).defect_vector == Matrix([3])
    assert paste_certificates(f, replace(g, defect_vector=None, repair_map=None)).defect_vector == Matrix([2])
    with pytest.raises(ValueError, match="repair models disagree"):
        paste_certificates(f, replace(g, repair_map=Matrix([[2]])))
    with pytest.raises(ValueError, match="first leg"):
        paste_certificates(replace(f, chi_certified=False), g)


def test_finite_collision_transport_and_nonrecoverability():
    # The source look already identifies 2 and 4; the transport must preserve it.
    f = square(carrier=(2, 3, 4), state_map=lambda x: x + 2,
               source_look=lambda x: x % 2, target_look=lambda x: x % 2,
               observation_map=lambda x: x)
    assert f.is_valid()
    assert f.source_look(2) == f.source_look(4) == 0
    assert f.target_look(f.state_map(2)) == f.target_look(f.state_map(4)) == 0
    for post in (lambda x: x, lambda x: 1 - x, lambda x: "*"):
        assert post(f.source_look(2)) == post(f.source_look(4))
    # Exhaust every recovery Unit -> Bool, exactly the Lean countermodel.
    assert not any(all(recovery[0] == bit for bit in (False, True))
                   for recovery in product((False, True), repeat=1))


def test_pasting_evaluates_composite_maps_on_carrier():
    f = square(carrier=(2, 3, 4), state_map=lambda x: x % 2,
               observation_map=lambda x: x % 2,
               morphism_kind=MorphismKind.QUOTIENT,
               loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 5)))
    g = square(source_regime="B", target_regime="C", carrier=(0, 1),
               state_map=lambda x: "*", observation_map=lambda x: "*",
               morphism_kind=MorphismKind.APPROXIMATION,
               loss_ledger=LossLedger(a=True, loss_mass=Rational(2, 5)))
    h = paste_certificates(f, g)
    assert h.verify()
    assert [h.state_map(x) for x in f.carrier] == ["*", "*", "*"]
    assert h.loss_ledger.loss_mass == Rational(3, 5)
    assert h.leg_ledgers == (f.loss_ledger, g.loss_ledger)

