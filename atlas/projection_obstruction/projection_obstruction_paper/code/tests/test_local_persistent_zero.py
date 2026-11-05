"""Adversarial finite checks for the supplied local persistent-zero model."""

from dataclasses import replace

import pytest

sp = pytest.importorskip("sympy")

from local_persistent_zero import LocalModel, LocalTerm, propose_local_zero, verify_local_zero

I = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
ZERO = sp.diag(1, 0)


def boundary_model(boundary=None):
    if boundary is None:
        boundary = sp.kronecker_product(Z, X)
    return LocalModel((2, 2), (0,), (LocalTerm((0, 1), boundary),),
                      (I, Z), ZERO, ({(0, 1): sp.S.One, (0, 0): -sp.S.One},), 1)


def test_boundary_checked_model_and_nonconstant_flow_polynomial():
    model = boundary_model()
    assert verify_local_zero(model, propose_local_zero(model))
    rotation = LocalModel((2,), (0,), (LocalTerm((0,), X),), (I, X, Y, Z), ZERO,
                         ({(0, 0, 2, 0): sp.S.One, (0, 0, 0, 2): sp.S.One,
                           (0, 0, 0, 0): -sp.S.One},), 2)
    certificate = propose_local_zero(rotation)
    assert certificate.generator != sp.zeros(4)
    assert verify_local_zero(rotation, certificate)


def test_changed_boundary_is_rejected_despite_zero_first_jet():
    model = boundary_model()
    certificate = propose_local_zero(model)
    bad = boundary_model(sp.kronecker_product(X, X))
    assert not verify_local_zero(bad, certificate)
    # Independent control: first jet vanishes but the second does not.
    h = bad.terms[0].operator
    rho = sp.kronecker_product(ZERO, ZERO)
    observable = sp.kronecker_product(Z, I)
    first = -sp.I * (h * rho - rho * h)
    second = -sp.I * (h * first - first * h)
    assert sp.trace(observable * first) == 0
    assert sp.trace(observable * second) == -4


def test_every_crossing_is_checked_and_omission_changes_binding():
    good = boundary_model()
    certificate = propose_local_zero(good)
    added = replace(good, terms=good.terms + (LocalTerm((0, 1), sp.kronecker_product(X, X)),))
    assert not verify_local_zero(added, certificate)
    assert not verify_local_zero(replace(good, terms=()), certificate)


def test_basis_identity_independence_hermiticity_and_invariance_are_checked():
    model = boundary_model()
    certificate = propose_local_zero(model)
    changes = [replace(model, basis=(I, I)), replace(model, basis=(Z,)),
               replace(model, basis=(I, sp.Matrix([[0, 1], [0, 0]]))),
               replace(model, terms=(LocalTerm((0,), X),))]
    assert all(not verify_local_zero(changed, certificate) for changed in changes)


def test_changed_readout_degree_and_state_are_checked():
    model = boundary_model()
    certificate = propose_local_zero(model)
    for changed in [replace(model, degree=0),
                    replace(model, readouts=({(0, 1): sp.S.One},)),
                    replace(model, initial_region_state=sp.diag(2, -1)),
                    replace(model, initial_region_state=I),
                    replace(model, initial_region_state=sp.Matrix([[1, 1], [0, 0]]))]:
        assert not verify_local_zero(changed, certificate)


def test_forged_generator_jets_and_annihilator_are_rejected():
    model = boundary_model()
    cert = propose_local_zero(model)
    assert not verify_local_zero(model, replace(cert, generator=sp.eye(2)))
    assert not verify_local_zero(model, replace(cert, onset=replace(cert.onset, annihilator=(sp.S.One, sp.S.One))))
    assert not verify_local_zero(model, replace(cert, onset=replace(cert.onset, derivatives=((sp.S.One,),))))
    assert not verify_local_zero(model, replace(cert, model_digest="0" * 64))


def test_wrong_support_and_inexact_entries_are_refused():
    model = boundary_model()
    cert = propose_local_zero(model)
    for changed in [replace(model, region=(0, 0)),
                    replace(model, terms=(LocalTerm((1, 0), sp.eye(4)),)),
                    replace(model, basis=(I, sp.Float(1.0) * Z))]:
        assert not verify_local_zero(changed, cert)
