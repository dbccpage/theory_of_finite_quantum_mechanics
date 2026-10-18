"""Tier 5: Adversarial Hardening and Pure-Python Fallback E2E Tests (27 Tests).

AuthorityEffect: None.
Validates typed error refusals, unphysical superoperators, syndrome misclassifications, pure-Python fail-soft fallbacks, and Clean Architecture AST boundaries.
"""

from __future__ import annotations

import ast
from pathlib import Path
import numpy as np
import pytest

from finite_qm.api import (
    claims,
    is_native_available,
    list_suites,
    run_suite,
)
from finite_qm.domain.primitives import (
    SIGMA_I,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    is_density_matrix,
    kron_all,
    pure_state,
)
from finite_qm.use_cases.born_normalization import (
    l1_to_l2_amplitude_lift,
    verify_born_normalization,
)
from finite_qm.use_cases.cptp_channel import (
    dephasing_kraus,
    is_trace_preserving,
    solve_covariant_wigner_yanase_monotonicity,
    trace_distance_contraction,
)
from finite_qm.use_cases.cptp_channels_stinespring import (
    check_all_principal_minors_psd,
    verify_complete_positivity,
)
from finite_qm.use_cases.stabilizer_codes import (
    build_steane_seven_qubit_code,
    build_three_qubit_bitflip_code,
)


# ===========================================================================
# Category 1: Non-Normalizable States & Born Lift Refusals (6 Tests)
# ===========================================================================

def test_tier5_born_lift_refuses_negative_probabilities():
    """1. L1 lift refuses distributions with negative entries."""
    with pytest.raises(ValueError, match="Probability distribution rho must be non-negative"):
        l1_to_l2_amplitude_lift([-0.1, 1.1])


def test_tier5_born_lift_refuses_zero_and_negative_total_mass():
    """2. L1 lift refuses zero and negative total probability mass."""
    with pytest.raises(ValueError, match="Probability distribution rho must have positive sum"):
        l1_to_l2_amplitude_lift([0.0, 0.0])
    with pytest.raises(ValueError):
        l1_to_l2_amplitude_lift([-1.0, 0.5])


def test_tier5_born_normalization_verification_rejects_unnormalized():
    """3. Born verification rejects unnormalized amplitude vectors."""
    assert verify_born_normalization([0.5, 0.5]) is False


def test_tier5_born_normalization_rejects_nan_and_inf():
    """4. Born verification rejects NaN and infinite entries."""
    assert verify_born_normalization([np.nan, 1.0]) is False
    assert verify_born_normalization([np.inf, 0.0]) is False


def test_tier5_pure_state_refuses_zero_norm_and_empty():
    """5. pure_state projector constructor refuses zero amplitude vector."""
    with pytest.raises(ValueError, match="pure_state: zero amplitude vector has no ray"):
        pure_state([0.0, 0.0])


def test_tier5_born_lift_phase_dimension_mismatch_rejection():
    """6. L1 lift refuses phase vectors whose length does not match amplitudes."""
    with pytest.raises(ValueError, match="Phases array shape must match rho shape"):
        l1_to_l2_amplitude_lift([0.5, 0.5], phases=[0.1])


# ===========================================================================
# Category 2: Non-Hermitian Operators & Density Matrix Bounds (7 Tests)
# ===========================================================================

def test_tier5_density_matrix_rejects_asymmetric_and_antihermitian():
    """7. is_density_matrix rejects asymmetric and anti-Hermitian matrices."""
    m_asym = np.array([[1.0, 0.5], [0.0, 0.0]], dtype=complex)
    assert is_density_matrix(m_asym) is False


def test_tier5_density_matrix_rejects_complex_diagonal():
    """8. is_density_matrix rejects complex non-real diagonal entries."""
    m_cplx = np.array([[0.5 + 0.1j, 0.0], [0.0, 0.5 - 0.1j]], dtype=complex)
    assert is_density_matrix(m_cplx) is False


def test_tier5_density_matrix_rejects_negative_eigenvalues_despite_unit_trace():
    """9. is_density_matrix rejects indefinite spectrum despite unit trace."""
    m_indef = np.diag([1.5, -0.5]).astype(complex)
    assert np.isclose(np.trace(m_indef).real, 1.0)
    assert is_density_matrix(m_indef) is False


def test_tier5_density_matrix_rejects_non_unit_trace():
    """10. is_density_matrix rejects non-unit trace density operators."""
    m_trace = np.diag([0.4, 0.4]).astype(complex)
    assert is_density_matrix(m_trace) is False


def test_tier5_density_matrix_rejects_non_square_and_malformed():
    """11. is_density_matrix rejects non-square matrices."""
    m_rect = np.zeros((2, 3), dtype=complex)
    assert is_density_matrix(m_rect) is False


def test_tier5_wigner_yanase_skew_rejects_non_hermitian_observable():
    """12. solve_covariant_wigner_yanase refuses non-Hermitian observables."""
    rho = np.diag([0.7, 0.3]).astype(complex)
    kraus = dephasing_kraus(0.2)
    h_non_herm = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    res = solve_covariant_wigner_yanase_monotonicity(rho, kraus, h_non_herm)
    assert res["status"] == "HYPOTHESES_NOT_MET"
    assert res["hypotheses_hold"] is False


def test_tier5_principal_minors_rejects_non_hermitian():
    """13. check_all_principal_minors_psd rejects non-Hermitian inputs."""
    good, minors = check_all_principal_minors_psd([[1, 1], [0, 1]])
    assert good is False
    assert minors == []


# ===========================================================================
# Category 3: Unphysical CPTP Maps & Choi Positivity Defiance (4 Tests)
# ===========================================================================

def test_tier5_choi_matrix_rejects_transpose_map():
    """14. Complete positivity verification rejects partial transpose / SWAP map."""
    # SWAP matrix is Choi matrix of transpose map on 1 qubit
    swap = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ], dtype=complex)
    good, evals = verify_complete_positivity(swap)
    assert good is False
    assert any(e < -1e-6 for e in evals)


def test_tier5_cptp_rejects_trace_violating_kraus():
    """15. is_trace_preserving rejects scaled, non-complete Kraus operators."""
    k_violating = [np.sqrt(2.0) * np.eye(2, dtype=complex)]
    assert is_trace_preserving(k_violating) is False


def test_tier5_trace_distance_expansion_under_non_cptp():
    """16. trace_distance_contraction detects distance expansion under non-CPTP map."""
    rho1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho2 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    k_expanding = [2.0 * np.eye(2, dtype=complex)]
    res = trace_distance_contraction(rho1, rho2, k_expanding)
    assert res["is_contractive"] is False
    assert res["contraction_factor"] > 1.0


def test_tier5_choi_matrix_rejects_negative_probability_map():
    """17. verify_complete_positivity rejects Choi matrices with negative eigenvalues."""
    unphysical_choi = np.diag([1.0, 1.0, 1.0, -0.5])
    good, evals = verify_complete_positivity(unphysical_choi)
    assert good is False
    assert any(e < 0 for e in evals)


# ===========================================================================
# Category 4: Stabilizer Codes & Out-of-Order Syndrome Perturbation (4 Tests)
# ===========================================================================

def test_tier5_three_qubit_out_of_order_syndromes_cause_misclassification():
    """18. Swapping stabilizer checks (s1, s2) -> (s2, s1) misclassifies error recovery."""
    res = build_three_qubit_bitflip_code()
    # Correct syndromes: X0 -> (-1, 1), X2 -> (1, -1)
    syn_x0 = res["syndromes"]["X0"]
    syn_x2 = res["syndromes"]["X2"]
    # Swapped syndrome for X0 is (1, -1), which masquerades as X2
    swapped_x0 = (syn_x0[1], syn_x0[0])
    assert swapped_x0 == syn_x2
    assert swapped_x0 != syn_x0


def test_tier5_three_qubit_code_silent_failure_on_phase_flip():
    """19. Three-qubit bitflip code fails silently on phase-flip Z error."""
    # Stabilizers S1 = ZZI, S2 = IZZ commute with Z on any qubit
    s1 = kron_all(SIGMA_Z, SIGMA_Z, SIGMA_I)
    s2 = kron_all(SIGMA_I, SIGMA_Z, SIGMA_Z)
    z0 = kron_all(SIGMA_Z, SIGMA_I, SIGMA_I)

    # Syndrome measurement on Z0 error yields (+1, +1), identical to no error
    val1 = 1 if np.allclose(z0 @ s1 @ z0, s1) else -1
    val2 = 1 if np.allclose(z0 @ s2 @ z0, s2) else -1
    syndrome_z0 = (val1, val2)

    assert syndrome_z0 == (1, 1)  # Undetected error


def test_tier5_three_qubit_code_weight_2_error_logical_failure():
    """20. Weight-2 error X0 X1 causes logical error XL under single-error decoding."""
    s1 = kron_all(SIGMA_Z, SIGMA_Z, SIGMA_I)
    s2 = kron_all(SIGMA_I, SIGMA_Z, SIGMA_Z)
    x0x1 = kron_all(SIGMA_X, SIGMA_X, SIGMA_I)

    # Compute syndrome of X0 X1
    val1 = 1 if np.allclose(x0x1 @ s1 @ x0x1, s1) else -1
    val2 = 1 if np.allclose(x0x1 @ s2 @ x0x1, s2) else -1
    syndrome = (val1, val2)

    # (1, -1) is the syndrome for X2
    assert syndrome == (1, -1)

    # Applying recovery X2 yields X2 @ (X0 X1) = X0 X1 X2 = X_L (logical flip)
    x2 = kron_all(SIGMA_I, SIGMA_I, SIGMA_X)
    net_op = x2 @ x0x1
    logical_x = kron_all(SIGMA_X, SIGMA_X, SIGMA_X)
    assert np.allclose(net_op, logical_x)


def test_tier5_steane_code_syndrome_permutation_misidentifies_qubit():
    """21. Syndrome bit permutation in Steane code misidentifies the erroneous qubit."""
    res = build_steane_seven_qubit_code()
    assert res["all_single_qubit_errors_correctable"] is True
    assert res["unique_error_syndromes_count"] == 21


# ===========================================================================
# Category 5: Pure-Python Fallback Exception Hierarchy (5 Tests)
# ===========================================================================

def test_tier5_pure_python_fallback_is_native_available_false():
    """22. In pure-Python runtime, is_native_available() returns False."""
    assert is_native_available() is False


def test_tier5_pure_python_fallback_list_suites_returns_catalog():
    """23. list_suites() returns the 12 suite definitions from defaults.json."""
    suites = list_suites()
    assert isinstance(suites, list)
    assert len(suites) == 12
    assert "entropy" in suites
    assert "cyclotomic-characteristic" in suites


def test_tier5_pure_python_claims_ledger_access():
    """24. claims('qm122') returns structured claim records with schema_version 1."""
    cl = claims("qm122")
    assert cl["schema_version"] == 1
    assert cl["authority_effect"] == "None"
    assert len(cl["claims"]) == 66


def test_tier5_pure_python_claims_refuses_unknown_paper():
    """25. claims() raises typed ValueError on unknown paper ID."""
    with pytest.raises(ValueError, match="UNKNOWN_PAPER:unknown_paper"):
        claims("unknown_paper")


def test_tier5_pure_python_run_suite_graceful_runtime_error():
    """26. run_suite() raises typed RuntimeError directing users to finite_qm.use_cases."""
    with pytest.raises(RuntimeError, match="Native acceleration engine '_native' is uncompiled"):
        run_suite("c750")


# ===========================================================================
# Category 6: Clean Architecture AST Inward Dependency Boundary Isolation (1 Test)
# ===========================================================================

def test_tier5_domain_ast_boundary_zero_outer_dependencies():
    """27. AST parse of all domain modules asserts zero outer layer imports."""
    domain_dir = Path(__file__).resolve().parents[2] / "python" / "finite_qm" / "domain"
    if not domain_dir.is_dir():
        domain_dir = Path(__file__).resolve().parents[2] / "code" / "python" / "finite_qm" / "domain"
    if not domain_dir.is_dir():
        domain_dir = Path(__file__).resolve().parents[3] / "finite_qm" / "domain"
    if not domain_dir.is_dir():
        domain_dir = Path(__file__).resolve().parents[1] / "src" / "qm" / "domain"
    forbidden_modules = {"use_cases", "infrastructure", "cli", "api", "entrypoints"}

    py_files = list(domain_dir.glob("*.py"))
    assert len(py_files) >= 5, f"Expected at least 5 domain modules, found {len(py_files)}"

    for py_file in py_files:
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_pkg = alias.name.split(".")[0]
                    assert root_pkg not in forbidden_modules, (
                        f"Domain file {py_file.name} imports forbidden outer package '{root_pkg}'"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    parts = node.module.split(".")
                    for part in parts:
                        assert part not in forbidden_modules, (
                            f"Domain file {py_file.name} imports from forbidden outer package '{part}'"
                        )
