"""Round-2 hardening tests: l1 boundary endpoints, hodge checker fail-closed,
obstruction core lengths, cadical literal validation."""

import types

import pytest

from omega_engine.crates.evaluator.eval_hodge_certificate import (
    CertRejectReason,
    HodgeCertificate,
    check_hodge_certificate,
)
from omega_engine.crates.solver.solv_cadical_unsat_core import (
    CadicalUnsatCoreLocalizer,
    UnsatCoreLocalization,
)
from omega_engine.crates.solver.solv_l1_obstruction_witness import (
    L1ObstructionProposal,
)
from omega_engine.crates.solver.solv_phi1_l1_boundary import Boundary1, BoundaryEdge, solve_phi1
from omega_engine.crates.type.finite_directed_graph import FiniteDirectedGraph
from omega_engine.crates.type.network_simplex_error import NetworkSimplexError


def _g(pairs):
    return FiniteDirectedGraph.from_pairs(pairs)


# 1-3. l1 boundary solver endpoint validation
def test_l1_rejects_negative_tail():
    b = Boundary1(num_vertices=2, edges=[BoundaryEdge(tail=-1, head=0, weight=1)])
    with pytest.raises(NetworkSimplexError):
        solve_phi1(b, [0])


def test_l1_rejects_out_of_range_head():
    b = Boundary1(num_vertices=2, edges=[BoundaryEdge(tail=0, head=5, weight=1)])
    with pytest.raises(NetworkSimplexError):
        solve_phi1(b, [0])


def test_l1_rejects_self_loop():
    b = Boundary1(num_vertices=2, edges=[BoundaryEdge(tail=1, head=1, weight=1)])
    with pytest.raises(NetworkSimplexError):
        solve_phi1(b, [0])


# 4-6. hodge checker shape mismatches
def test_hodge_rejects_tau_length_mismatch():
    g = _g([(0, 1)])  # 1 edge, 2 nodes
    cert = HodgeCertificate(tau=[0.0, 0.0], primal_alpha=[0.0, 0.0], dual_witness=[0.0])
    s = check_hodge_certificate(g, cert, 1e-9)
    assert s.reason is CertRejectReason.ShapeMismatch


def test_hodge_rejects_dual_length_mismatch():
    g = _g([(0, 1)])
    cert = HodgeCertificate(tau=[0.0], primal_alpha=[0.0, 0.0], dual_witness=[0.0, 0.0])
    assert (
        check_hodge_certificate(g, cert, 1e-9).reason is CertRejectReason.ShapeMismatch
    )


def test_hodge_rejects_alpha_length_mismatch():
    g = _g([(0, 1)])
    cert = HodgeCertificate(tau=[0.0], primal_alpha=[0.0], dual_witness=[0.0])
    assert (
        check_hodge_certificate(g, cert, 1e-9).reason is CertRejectReason.ShapeMismatch
    )


# 7-8. hodge checker non-finite
def test_hodge_rejects_nan_tau():
    g = _g([(0, 1)])
    cert = HodgeCertificate(
        tau=[float("nan")], primal_alpha=[0.0, 0.0], dual_witness=[0.0]
    )
    assert (
        check_hodge_certificate(g, cert, 1e-9).reason is CertRejectReason.NonFiniteInput
    )


def test_hodge_rejects_inf_dual():
    g = _g([(0, 1)])
    cert = HodgeCertificate(
        tau=[0.0], primal_alpha=[0.0, 0.0], dual_witness=[float("inf")]
    )
    assert (
        check_hodge_certificate(g, cert, 1e-9).reason is CertRejectReason.NonFiniteInput
    )


def test_hodge_rejects_negative_tol():
    g = _g([(0, 1)])
    cert = HodgeCertificate(tau=[0.0], primal_alpha=[0.0, 0.0], dual_witness=[0.0])
    assert (
        check_hodge_certificate(g, cert, -1e-9).reason
        is CertRejectReason.InvalidTolerance
    )


def test_hodge_accepts_simple_zero_certificate():
    g = _g([(0, 1)])
    cert = HodgeCertificate(tau=[0.0], primal_alpha=[0.0, 0.0], dual_witness=[0.0])
    assert check_hodge_certificate(g, cert, 1e-9).accept is True


# 9. l1 obstruction proposal rejects mismatched core lengths
def test_l1_obstruction_rejects_mismatched_core():
    core = types.SimpleNamespace(
        delta_exact=[1.0, 2.0], delta_irr=[1.0], f_star=[0.0, 0.0]
    )
    with pytest.raises(ValueError):
        L1ObstructionProposal.try_from_core(_g([(0, 1)]), core)


# 10. cadical localizer rejects literal 0 and out-of-range literals
def test_cadical_rejects_zero_literal():
    loc = CadicalUnsatCoreLocalizer(num_vars=3)
    with pytest.raises(ValueError):
        loc.add_clause([1, 0, -2])


def test_cadical_rejects_out_of_range_literal():
    loc = CadicalUnsatCoreLocalizer(num_vars=3)
    with pytest.raises(ValueError):
        loc.add_clause([1, 4])  # var 4 > num_vars 3


def test_cadical_rejects_negative_num_vars():
    with pytest.raises(ValueError):
        CadicalUnsatCoreLocalizer(num_vars=-1)


def test_cadical_label_map_is_a_copy():
    loc = CadicalUnsatCoreLocalizer(num_vars=2)
    loc.add_labeled_clause([1, -2], "rule-A")
    m = loc.get_label_map()
    m[99] = "injected"
    assert 99 not in loc.get_label_map()  # internal state unchanged


