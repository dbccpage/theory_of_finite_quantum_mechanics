# -*- coding: utf-8 -*-
"""
test_rust_bridge.py: Tests integration with Rust crates in omega_engine/crates_rs.

AuthorityEffect: None.
"""

from __future__ import annotations

from sympy import Matrix, Rational
from witnessed_difference.native_functionals import dual_bound

from coda_application.infrastructure.exact_solver_adapter import ExactSolverAdapter
from coda_application.infrastructure.rust_bridge import RustCrateBridge


def test_rust_workspace_detection_and_member_crates():
    """Verifies that the Rust workspace in omega_engine/crates_rs is detected with key crates."""
    bridge = RustCrateBridge()
    assert bridge.is_workspace_available() is True

    crates = bridge.get_available_crates()
    assert len(crates) > 30

    # Key mathematical, pipeline, and contract crates must be present
    assert "omega_solvers" in crates
    assert "omega_pipelines" in crates
    assert "omega_homology" in crates
    assert "omega_terminalizers" in crates
    assert "omega_types" in crates
    assert "omega_contracts" in crates
    assert "omega_epk" in crates

def test_configured_native_evaluator_works_without_workspace_discovery(monkeypatch):
    """A standalone copy reports absent Rust rather than inventing execution."""
    monkeypatch.setattr(RustCrateBridge, "_default_workspace", staticmethod(lambda: None))
    bridge = RustCrateBridge()
    assert not bridge.is_workspace_available()
    assert bridge.get_available_crates() == []
    result = bridge.solve_phi1_l1_via_rust(Matrix([[-1, 1], [1, -1]]), Matrix([1, 1]))
    assert result["status"] == "NATIVE_CERTIFICATE_VERIFIED"
    assert result["rust_workspace_present"] is False
    assert result["phi1"] == [2, 1]


def test_rust_solver_schema_payload_preparation():
    """Verifies that boundary matrices and cochains serialize to exact rational payloads for Rust solvers."""
    bridge = RustCrateBridge()
    d0 = Matrix([[-1, 1], [1, -1]])
    cochain = Matrix([Rational(1, 2), Rational(1, 2)])

    schema = bridge.solve_phi1_l1_via_rust(d0, cochain)
    assert schema is not None
    # The configured native executable performs and verifies the evaluation.
    assert schema["status"] == "NATIVE_CERTIFICATE_VERIFIED"
    assert schema["crate"] == "omega_functional"
    assert schema["payload_dim"] == (2, 2)
    assert schema["phi1"] == [1, 1]  # circulation 1/2 + 1/2 around the 2-cycle


def test_exact_solver_adapter_quotient_and_dual_witness():
    """Verifies ExactSolverAdapter computing exact L1 quotient distance and dual witness certificates."""
    d0 = Matrix([[-1, 1], [1, -1]])

    # Case 1: In image of d0
    c_in = Matrix([Rational(-2), Rational(2)])
    dist_in, witness_in, residual_in = ExactSolverAdapter.compute_quotient_distance(d0, c_in)
    assert dist_in.numerator == 0
    assert witness_in is None
    assert residual_in == Matrix([Rational(0), Rational(0)])

    # Case 2: Obstructed cochain
    c_obs = Matrix([Rational(1), Rational(0)])
    dist_obs, witness_obs, _ = ExactSolverAdapter.compute_quotient_distance(d0, c_obs)
    assert dist_obs.numerator > 0
    assert witness_obs is not None
    assert witness_obs.pairing_value == dist_obs
    assert dual_bound([[-1, 1], [1, -1]], 2, [1, 0], [1, 1], witness_obs.fractions) == dist_obs.fraction
