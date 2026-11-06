"""Injected-fault mutants for CODA-MUR decision procedures.

Each mutant locally redefines one production decision. Tests assert that the
mutant disagrees with the real oracle on a known packet, so the suite kills
the fault if it is ever injected into production.
"""

from __future__ import annotations

from coda_mur_core import (
    DescentSquareCertificate,
    LossLedger,
    MorphismKind,
    TerminalRegime,
    compute_transport_quotient_obstruction,
    evaluate_transport_authority,
)
from finite_fixtures import finite_certificate
from sympy import Matrix, Rational


def _target_regime(can_terminalize: bool = True, is_authorized: bool = True) -> TerminalRegime:
    return TerminalRegime(
        regime_id="Regime_B",
        terminalize=lambda x: f"term_{x}" if can_terminalize else None,
        is_auth=lambda t: is_authorized,
    )


def mutant_skip_certificate(source_id, regime, artifact, certificate):
    """Treat a missing certificate as success whenever the target terminalizes."""
    terminal = regime.terminalize(artifact)
    return terminal is not None and regime.is_auth(terminal)


def mutant_skip_loss_ledger(certificate: DescentSquareCertificate) -> bool:
    """Treat a quotient morphism as valid even with an empty loss ledger."""
    return bool(certificate.chi_certified and certificate.commutes)


def mutant_chi_alone_grants_target(source_id, regime, artifact, certificate):
    """Treat a valid certificate as enough, skipping target terminalization."""
    return certificate is not None and certificate.is_valid()


def mutant_l2_residual(repair_map, cochain) -> Rational:
    """Swap the L1 quotient leftover for an L2 projection residual."""
    matrix = Matrix(repair_map)
    x = Matrix(cochain)
    gram = matrix.T * matrix
    coeff = gram.inv() * (matrix.T * x)
    residual = x - matrix * coeff
    return sum((entry ** 2 for entry in residual), start=Rational(0))


def test_mutant_skip_certificate_killed_on_missing_chi() -> None:
    regime = _target_regime()
    real = evaluate_transport_authority("source_01", regime, "artifact_01", None)
    mutant_inhabits = mutant_skip_certificate("source_01", regime, "artifact_01", None)
    assert real.inhabited is False
    assert mutant_inhabits is True
    assert mutant_inhabits is not real.inhabited


def test_mutant_skip_loss_ledger_killed_on_empty_quotient() -> None:
    cert = finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_quot",
        morphism_kind=MorphismKind.QUOTIENT,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger.empty(),
    )
    real = evaluate_transport_authority("source_01", _target_regime(), "artifact_01", cert)
    mutant_valid = mutant_skip_loss_ledger(cert)
    assert real.inhabited is False
    assert real.refusal_code == "R_unpriced_loss"
    assert mutant_valid is True
    assert cert.is_valid() is False


def test_mutant_chi_alone_killed_when_target_cannot_terminalize() -> None:
    cert = finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_exact",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=True,
    )
    regime = _target_regime(can_terminalize=False, is_authorized=True)
    real = evaluate_transport_authority("source_01", regime, "artifact_01", cert)
    mutant_inhabits = mutant_chi_alone_grants_target("source_01", regime, "artifact_01", cert)
    assert real.inhabited is False
    assert real.refusal_code == "R_noterminal"
    assert mutant_inhabits is True
    assert mutant_inhabits is not real.inhabited


def test_mutant_l2_residual_killed_on_column_instance() -> None:
    repair_map = Matrix([[1], [1], [1]])
    cochain = Matrix([[0], [0], [10]])
    real = compute_transport_quotient_obstruction(repair_map, cochain)
    mutant_value = mutant_l2_residual(repair_map, cochain)
    assert real.distance == Rational(10)
    assert mutant_value == Rational(200, 3)
    assert real.distance != mutant_value
