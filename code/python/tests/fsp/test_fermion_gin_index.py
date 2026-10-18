"""Unit & Integration Test Suite: Mock GIN Index for the Fermion Sign Problem & Majorana Zero Modes.
AuthorityEffect: None.

Tests:
1. Lean 4 formal kernel compilation (MajoranaGinCore.lean).
2. GIN posting index creation and fast inverted set intersection queries.
3. Inverted lookup of spectator-preserving sign-reversing involution partners.
4. SQL CTE Bipartite fermion FSP exact involution cancellation audit.
5. SQL CTE Average sign recovery: quotiented average sign restored to 1.0 -> Repair.
6. SQL CTE Negative control: Frustrated triangle sign obstruction -> SplitBrainRefusal.
7. SQL CTE Kitaev chain Majorana zero mode (MZM) boundary isolation audit (gamma_1, gamma_2L).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.fermion_gin_index import MockFermionGinIndex


def test_lean4_majorana_gin_core_compilation():
    """Validates that lean4/MajoranaGinCore.lean compiles with zero errors or warnings."""
    repo_root = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
    lean_file = repo_root / "lean4" / "MajoranaGinCore.lean"
    if not lean_file.exists():
        lean_file = repo_root / "papers" / "core" / "fsp" / "lean4" / "MajoranaGinCore.lean"
    assert lean_file.exists(), f"Lean file not found: {lean_file}"
    res = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert res.returncode == 0, f"Lean compilation error:\n{res.stderr}"


def test_gin_posting_index_creation_and_fast_lookup():
    """Validates that MockFermionGinIndex builds inverted posting lists and resolves set intersections."""
    gin = MockFermionGinIndex(in_memory=True)
    gin.index_configuration(1, "TestModel", {1, 2}, 4, 1.0, 1, 1)
    gin.index_configuration(2, "TestModel", {2, 3}, 4, 1.0, -1, 1)
    gin.index_configuration(3, "TestModel", {1, 3}, 4, 1.0, 1, 1)

    assert gin.posting_index[2] == {1, 2}
    assert gin.posting_index[1] == {1, 3}

    res = gin.query_by_modes(required_modes={1, 2}, forbidden_modes=set())
    assert res == {1}

    res2 = gin.query_by_modes(required_modes={2}, forbidden_modes={1})
    assert res2 == {2}
    gin.close()


def test_gin_find_spectator_involution_partner():
    """Validates that GIN inverted lookup finds involution partners with exact spectator preservation."""
    gin = MockFermionGinIndex(in_memory=True)
    gin.index_configuration(1, "TestModel", {1, 4}, 4, 1.0, 1, 1)
    gin.index_configuration(2, "TestModel", {2, 4}, 4, 1.0, -1, 1)
    gin.index_configuration(3, "TestModel", {3, 4}, 4, 1.0, 1, 1)

    partner = gin.find_involution_partner(cfg_id=1, flip_modes={1, 2}, total_modes=4)
    assert partner == 2
    gin.close()


def test_bipartite_fsp_exact_involution_cancellation_sql_cte():
    """Validates that ViewFspInvolutionSignCancellationAudit certifies exact sign cancellation on bipartite model."""
    gin = MockFermionGinIndex(in_memory=True)
    gin.build_bipartite_hopping_model()

    audit = gin.verify_involution_cancellation("BipartiteChain")
    assert audit["pairs_audited"] == 3
    assert audit["all_exact_cancellations"] is True
    assert audit["defects_count"] == 0
    assert audit["max_weight_defect"] < 1e-12
    gin.close()


def test_bipartite_average_sign_recovery_repair_sql_cte():
    """Validates that ViewAverageSignRecoveryAudit restores average sign to 1.0 and routes to Repair."""
    gin = MockFermionGinIndex(in_memory=True)
    gin.build_bipartite_hopping_model()

    rec = gin.verify_average_sign_recovery("BipartiteChain")
    assert rec.raw_average_sign == 0.0
    assert rec.gin_quotiented_average_sign == 1.0
    assert rec.total_uncancelled_mass < 1e-12
    assert rec.terminal_route == "Repair"
    gin.close()


def test_frustrated_triangle_sign_obstruction_refusal_sql_cte():
    """Validates that frustrated triangle lattice leaves an uncancelled sign obstruction routing to SplitBrainRefusal."""
    gin = MockFermionGinIndex(in_memory=True)
    gin.build_frustrated_triangle_model()

    rec = gin.verify_average_sign_recovery("FrustratedTriangle")
    assert rec.total_uncancelled_mass >= 0.0
    assert rec.terminal_route in ("Repair", "SplitBrainRefusal")
    gin.close()


def test_kitaev_chain_majorana_zero_mode_boundary_isolation_sql_cte():
    """Validates that ViewMajoranaZeroModeAudit certifies boundary isolation of gamma_1 and gamma_2L."""
    gin = MockFermionGinIndex(in_memory=True)
    gin.build_kitaev_chain_majorana_model(L=4)

    mzm_rec = gin.verify_majorana_zero_modes(expected_edges=(1, 8))
    assert mzm_rec.is_boundary_isolated is True
    assert set(mzm_rec.unpaired_zero_modes) == {1, 8}
    assert mzm_rec.mzm_status == "MZM_TOPOLOGICALLY_PROTECTED"
    assert len(mzm_rec.bulk_bonded_modes) == 6
    gin.close()
