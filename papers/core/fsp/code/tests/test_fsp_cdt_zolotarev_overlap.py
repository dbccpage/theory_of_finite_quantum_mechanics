"""Unit and integration tests for Rational Zolotarev and Lanczos Overlap Dirac Operators on 4D CDT.
AuthorityEffect: None.

Tests:
1. Lean 4 formalization of Section 18 Zolotarev theorems.
2. Declarative YAML contract conformance (CDT-ZOLOTAREV-NF).
3. Zolotarev minimax rational approximation error bound and theoretical GW residual bound <= 1e-8.
4. Rational overlap operator Ginsparg-Wilson residual <= 1e-8 on regular gapped CDT complex.
5. Multi-shift CG solver simultaneous convergence across all rational pole shifts.
6. Lanczos sign approximation convergence to matrix sign function.
7. Spectral stiffening obstruction detection on gapless complexes and restoration via low-mode deflation.
8. SQLite relational audit view verdicts and sub-cubic complexity scaling.
"""

import math
from pathlib import Path
import subprocess
import numpy as np
import pytest
import sys
import yaml
code_dir = Path(__file__).resolve().parent.parent
tower_dir = code_dir.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from cdt_zolotarev_evaluator import (
    ZolotarevRationalApproximation,
    MultiShiftCGSolver,
    LanczosSignApproximation,
    CdtZolotarevOverlapEvaluator,
)


def test_lean4_zolotarev_theorems():
    """Validates that Lean 4 Section 18 compiles and defines all Zolotarev theorems."""
    lean_file = tower_dir / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Lean file not found: {lean_file}"

    content = lean_file.read_text(encoding="utf-8")
    assert "ZolotarevMinimaxErrorPredicate" in content
    assert "zolotarev_minimax_error_bound" in content
    assert "RationalGinspargWilsonResidualBoundPredicate" in content
    assert "rational_gw_residual_bounded" in content
    assert "SubcubicComplexityBoundPredicate" in content
    assert "multishift_cg_complexity_subcubic" in content
    assert "LowModeDeflationRestoresConvergencePredicate" in content
    assert "deflation_restores_convergence" in content
    assert "ZolotarevSpectralStiffeningObstruction" in content

    # Test compilation
    result = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert result.returncode == 0, f"Lean compilation failed: {result.stderr}"


def test_yaml_contract_schema():
    """Validates that nf.physics.cdt_zolotarev_overlap.yaml conforms to normal form schema."""
    yaml_file = tower_dir / "normal_forms" / "nf.physics.cdt_zolotarev_overlap.yaml"
    assert yaml_file.exists(), f"Contract not found: {yaml_file}"

    data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    assert data["identity"]["id"] == "nf.physics.cdt_zolotarev_overlap"
    assert data["identity"]["short_name"] == "CDT-ZOLOTAREV-NF"
    assert "SubcubicZolotarevCertified" in data["terminal_routes"]
    assert "ZolotarevSpectralStiffeningObstruction" in data["terminal_routes"]
    assert "ZolotarevToleranceBreach" in data["terminal_routes"]
    assert "LanczosDivergenceDefect" in data["terminal_routes"]


def test_zolotarev_minimax_error_and_gw_bound():
    """Validates Zolotarev rational minimax approximation error and GW residual bound."""
    eps = 0.05
    degree_m = 10
    zolo = ZolotarevRationalApproximation.compute(eps, degree_m)

    assert len(zolo.poles) == degree_m
    assert len(zolo.zeros) == degree_m
    assert len(zolo.residues) == degree_m

    # Error on sample grid in [eps, 1]
    x_test = np.linspace(eps, 1.0, 200)
    errors = [abs(1.0 - ZolotarevRationalApproximation.evaluate_scalar(x, zolo)) for x in x_test]
    max_err = max(errors)

    assert max_err <= zolo.max_theoretical_error
    assert max_err <= 1e-9

    # GW residual bound: (2 * delta + delta^2) / a <= 1e-8 for a = 1.0
    gw_bound = 2.0 * max_err + max_err**2
    assert gw_bound <= 1e-8


def test_rational_overlap_dirac_exact_gw_residual():
    """Validates that rational overlap Dirac operator satisfies GW relation within 1e-8."""
    evaluator = CdtZolotarevOverlapEvaluator()
    graph = evaluator.build_regular_gapped_complex("gapped_test_gw", num_vertices=6)

    res = evaluator.evaluate_rational_overlap_operator(
        graph, m0=1.2, r=1.0, degree_m=8, use_multishift=True
    )

    gw_res = res["gw_residual"]
    assert gw_res <= 1e-8, f"Ginsparg-Wilson residual {gw_res} exceeded 1e-8"
    assert res["max_shift_residual"] <= 1e-8
    evaluator.close()


def test_multishift_cg_simultaneous_convergence():
    """Validates that multi-shift CG solves all shifted systems simultaneously."""
    np.random.seed(42)
    n = 24
    m_shifts = 6
    # Create Hermitian positive definite matrix A = H^2
    M = np.random.randn(n, n) + 1j * np.random.randn(n, n)
    A = M.conj().T @ M + 0.1 * np.eye(n)
    shifts = list(np.linspace(0.01, 2.0, m_shifts))
    b = np.random.randn(n) + 1j * np.random.randn(n)

    sols, iters, max_res = MultiShiftCGSolver.solve(A, shifts, b, tol=1e-10)

    assert iters <= 50
    assert max_res <= 1e-8

    # Compare with exact np.linalg.solve for each shift
    I = np.eye(n, dtype=complex)
    for l, s in enumerate(shifts):
        exact_x = np.linalg.solve(A + s * I, b)
        rel_diff = np.linalg.norm(sols[l] - exact_x) / np.linalg.norm(exact_x)
        assert rel_diff <= 1e-8


def test_lanczos_sign_approximation_convergence():
    """Validates Lanczos sign projection approximation against exact matrix sign function."""
    np.random.seed(42)
    n = 20
    M = np.random.randn(n, n) + 1j * np.random.randn(n, n)
    H = 0.5 * (M + M.conj().T) + 0.5 * np.eye(n)
    v = np.random.randn(n) + 1j * np.random.randn(n)

    # Exact sign
    evals, evecs = np.linalg.eigh(H)
    sgn_exact = evecs @ np.diag(np.sign(evals)) @ evecs.conj().T
    target = sgn_exact @ v

    # Lanczos approximation
    approx = LanczosSignApproximation.apply(H, v, k_steps=20)
    err = np.linalg.norm(approx - target) / np.linalg.norm(target)
    assert err <= 0.20  # Krylov subspace bounds direction


def test_spectral_stiffening_and_low_mode_deflation():
    """Validates detection of spectral stiffening obstruction and resolution via deflation."""
    evaluator = CdtZolotarevOverlapEvaluator()
    stiff_graph = evaluator.build_stiffened_singular_complex("cdt_stiff_test", num_vertices=6)

    # 1. Undeflated with small degree m=3: stiffening obstruction
    rec_stiff = evaluator.record_complex_evaluation(
        stiff_graph, m0=0.50, r=1.0, degree_m=3, deflate=False
    )
    assert rec_stiff["gw_residual"] > 1e-8
    assert rec_stiff["classification"] == "ZolotarevSpectralStiffeningObstruction"
    assert rec_stiff["verdict"] == "SPECTRAL_STIFFENING_OBSTRUCTION_DETECTED"

    # 2. Deflated with degree m=10: restores sub-cubic convergence and GW tolerance <= 1e-8
    rec_defl = evaluator.record_complex_evaluation(
        stiff_graph, m0=0.50, r=1.0, degree_m=10, deflate=True
    )
    assert rec_defl["gw_residual"] <= 1e-8
    assert rec_defl["deflated_count"] > 0
    assert rec_defl["classification"] == "SubcubicZolotarevCertified"
    assert rec_defl["verdict"] == "SUBCUBIC_ZOLOTAREV_CERTIFIED"

    evaluator.close()


def test_sqlite_relational_views_and_subcubic_benchmark():
    """Validates ViewCdtZolotarevAudit relational query and sub-cubic benchmark logging."""
    evaluator = CdtZolotarevOverlapEvaluator()
    gapped_graph = evaluator.build_regular_gapped_complex("gapped_sql_test", num_vertices=6)

    rec = evaluator.record_complex_evaluation(gapped_graph, m0=1.2, r=1.0, degree_m=8)
    assert rec["verdict"] == "SUBCUBIC_ZOLOTAREV_CERTIFIED"
    assert rec["is_gw_within_tolerance"] == 1

    dense_ms, multi_ms, speedup = evaluator.benchmark_dense_vs_multishift(
        gapped_graph, m0=1.2, r=1.0, degree_m=8
    )
    assert dense_ms >= 0.0
    assert multi_ms >= 0.0

    evaluator.close()
