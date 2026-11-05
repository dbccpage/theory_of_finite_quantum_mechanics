"""Regression probes for the 2026-10-02 publication review."""

from types import SimpleNamespace

import numpy as np
import pytest

from carrier import Cochain, GraphComplex
from closure import ClosureBoundEvaluator
from gauges import EuclideanGauge, audit_so_k_invariance, audit_sphere_constancy
from socp_certifier import CycleClosedFormCertifier, SOCPCertifier
from solver import MixedNormSolver


@pytest.mark.parametrize("method", ["auto", "cycle_closed_form"])
@pytest.mark.parametrize(
    "amplitude,weight", [(1e-9, 1e12), (1e-15, 1e16), (1e-200, 1e200)]
)
def test_small_nonzero_cycle_keeps_weighted_witness(method, amplitude, weight):
    graph = GraphComplex.create_cycle_graph(3, stalk_dim=1, edge_weights=[weight] * 3)
    omega = Cochain([[amplitude], [0.0], [0.0]])
    cert = SOCPCertifier(graph).certify(omega, method=method)
    expected = amplitude * weight
    assert cert.solver_method == "cycle_closed_form"
    assert cert.is_optimal
    assert cert.primal_value == pytest.approx(expected, rel=1e-12, abs=0)
    assert cert.dual_value == pytest.approx(expected, rel=1e-12, abs=0)
    assert cert.details["circulation"] == [amplitude]


@pytest.mark.parametrize("certifier", [SOCPCertifier, CycleClosedFormCertifier, MixedNormSolver])
@pytest.mark.parametrize("tol", [True, -1.0, float("nan"), float("inf"), "small"])
def test_invalid_certificate_tolerance_is_rejected(certifier, tol):
    with pytest.raises(ValueError, match="tolerance"):
        certifier(GraphComplex.create_cycle_graph(3), tol=tol)


def test_zero_tolerance_is_an_allowed_strict_gate():
    graph = GraphComplex.create_cycle_graph(3)
    assert SOCPCertifier(graph, tol=0).certify(Cochain(np.zeros((3, 2)))).is_optimal


@pytest.mark.parametrize("audit", [audit_so_k_invariance, audit_sphere_constancy])
@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), -1.0])
def test_invalid_gauge_outputs_cannot_pass_an_audit(audit, bad_value):
    with pytest.raises(ValueError, match="finite nonnegative"):
        audit(lambda x: bad_value, dim=2, num_samples=3)


def test_rotation_audit_cannot_pass_without_a_valid_sample():
    class ZeroSamples:
        def normal(self, *, size):
            return np.zeros(size)

    with pytest.raises(ValueError, match="No valid"):
        audit_so_k_invariance(EuclideanGauge(), dim=2, num_samples=3, rng=ZeroSamples())


def test_degenerate_face_does_not_supply_a_cycle_orientation():
    graph = GraphComplex(
        4, [(0, 1), (1, 2), (2, 3), (3, 0)],
        faces=[[(0, 1), (0, -1), (1, 1), (1, -1)]],
    )
    assert graph.verify_complex()
    cert = SOCPCertifier(graph).certify(Cochain([[1, 0], [0, 1], [0, 0], [0, 0]]))
    assert cert.is_optimal
    assert cert.primal_value == pytest.approx(np.sqrt(2))
    assert cert.divergence_norm == pytest.approx(0)


def test_smoothed_solver_obeys_declared_gap_tolerance(monkeypatch):
    monkeypatch.setattr(
        "solver.minimize",
        lambda **kw: SimpleNamespace(
            x=kw["x0"], message="stopped before repair", nit=0, success=False,
        ),
    )
    graph = GraphComplex.create_cycle_graph(3)
    cert = MixedNormSolver(graph, tol=1e-12).solve(
        Cochain([[1e-5, 0], [0, 1e-5], [0, 0]]), method="smoothed_lbfgs",
    )
    assert 1e-12 < cert.duality_gap < 1e-4
    assert not cert.is_optimal
    assert not cert.is_zero_gap


def test_small_positive_quotient_is_not_an_exact_repair():
    result = ClosureBoundEvaluator(GraphComplex.create_cycle_graph(3, stalk_dim=1)).evaluate(
        Cochain([[1e-8], [0], [0]])
    )
    assert result.certified_bound_holds
    assert not result.is_exact_repair
    assert result.closure_ratio == pytest.approx(1)


def test_uncertified_candidate_does_not_supply_a_quotient_ratio(monkeypatch):
    graph = GraphComplex.create_cycle_graph(3, stalk_dim=1)
    evaluator = ClosureBoundEvaluator(graph)
    monkeypatch.setattr(evaluator.solver, "solve", lambda h: SimpleNamespace(
        primal_value=2.0, is_optimal=False, duality_gap=1.0, signed_duality_gap=1.0,
        residual_cochain=h,
    ))
    result = evaluator.evaluate(Cochain([[1], [0], [0]]))
    assert result.certified_quotient_value is None
    assert result.closure_ratio is None
