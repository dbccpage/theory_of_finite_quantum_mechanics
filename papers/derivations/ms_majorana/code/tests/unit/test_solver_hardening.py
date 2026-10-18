"""Hardening tests for the omega_solvers Python ports.

Guards the two places Python can silently lie: negative array indices and
non-finite trust gates. Plus budget, mutation, orientation, and the
deprecated-Hodge refusal boundary.
"""

import pytest

from omega_engine.crates.evaluator.eval_solver_evidence import (
    TrustPolicy,
    TrustRefusal,
    decide_trust,
    enforce_trust_or_refuse,
)
from omega_engine.crates.operator.lambda_op.lamb_fixpoint import fixpoint_bounded_recursion
from omega_engine.crates.operator.constructor.ctor_incidence_matrix import (
    IncidenceMatrixError,
    incidence_matrix,
)
from omega_engine.crates.type.finite_directed_graph import DirectedGraphError, FiniteDirectedGraph
from omega_engine.crates.type.solver_evidence import (
    Certificate,
    CertificateKind,
    SolverDiagnostics,
    SolverResult,
)
import omega_engine.crates.solver.solv_hodge_primal_dual as hodge


def test_finite_graph_rejects_negative_source():
    with pytest.raises(DirectedGraphError):
        FiniteDirectedGraph.from_pairs([(-1, 0)])


def test_finite_graph_rejects_negative_target():
    with pytest.raises(DirectedGraphError):
        FiniteDirectedGraph.from_pairs([(0, -2)])


def test_incidence_rejects_negative_source():
    with pytest.raises(IncidenceMatrixError):
        incidence_matrix(2, [(-1, 1)])


def test_incidence_rejects_negative_target():
    with pytest.raises(IncidenceMatrixError):
        incidence_matrix(2, [(0, -1)])


def test_incidence_orientation_and_self_loop():
    m = incidence_matrix(2, [(0, 1)])
    assert m[0, 0] == -1 and m[0, 1] == 1
    with pytest.raises(IncidenceMatrixError):
        incidence_matrix(2, [(1, 1)])


class _NeverConverges:
    def step(self, s):
        return s + 1

    def has_converged(self, old, new):
        return False


class _ConvergesImmediately:
    def step(self, s):
        return s

    def has_converged(self, old, new):
        return old == new


def test_fixpoint_rejects_negative_budget():
    with pytest.raises(ValueError):
        fixpoint_bounded_recursion(_NeverConverges(), 0, -5)


def test_fixpoint_rejects_zero_budget():
    with pytest.raises(ValueError):
        fixpoint_bounded_recursion(_NeverConverges(), 0, 0)


def test_fixpoint_returns_after_budget_when_not_converged():
    out = fixpoint_bounded_recursion(_NeverConverges(), 0, 3)
    assert out == 3


def test_fixpoint_stops_on_convergence():
    out = fixpoint_bounded_recursion(_ConvergesImmediately(), 7, 100)
    assert out == 7


def _res(**kw):
    return SolverResult(value=None, diagnostics=SolverDiagnostics(converged=True, **kw))


def test_trust_rejects_nan_primal_residual():
    d = decide_trust(_res(primal_residual=float("nan")), TrustPolicy(max_residual=1.0))
    assert d.trusted is False and "Non-finite" in d.reason


def test_trust_rejects_infinite_dual_residual():
    d = decide_trust(_res(dual_residual=float("inf")), TrustPolicy(max_residual=1.0))
    assert d.trusted is False and "Non-finite" in d.reason


def test_trust_rejects_negative_gap():
    d = decide_trust(_res(primal_dual_gap=-0.5), TrustPolicy(max_residual=1.0))
    assert d.trusted is False and "Negative" in d.reason


def test_trust_rejects_nan_even_without_max_residual():
    d = decide_trust(_res(primal_residual=float("nan")), TrustPolicy())
    assert d.trusted is False


def test_enforce_raises_typed_refusal():
    with pytest.raises(TrustRefusal):
        enforce_trust_or_refuse(
            decide_trust(_res(primal_residual=float("nan")), TrustPolicy())
        )


def test_certificate_serializes_by_name():
    cert = Certificate(kind=CertificateKind.DualWitness, payload=b"abc")
    assert cert.as_dict()["kind"] == "DualWitness"


@pytest.mark.parametrize(
    "fn",
    [
        hodge.solve_l1_hodge_primal_dual,
        hodge.compute_l2_hodge_independent,
        hodge.chambolle_pock_l1_hodge,
    ],
)
def test_deprecated_hodge_refuses(fn):
    with pytest.raises(NotImplementedError):
        try:
            fn(None, None)
        except TypeError:
            fn(None, None, 0, 0.0)


def test_topology_independent_rejects_negative():
    with pytest.raises(ValueError):
        hodge.Topology.independent(-1)


def test_edges_mutation_does_not_corrupt_graph():
    g = FiniteDirectedGraph.from_pairs([(0, 1), (1, 2)])
    e = g.edges()
    e.append((99, 99))
    assert g.num_edges() == 2
    assert (99, 99) not in g.edges()


