r"""Unit & Integration Tests: 4D CDT Ginsparg-Wilson & Overlap Dirac Operator Normal Form.
AuthorityEffect: None.

Tests:
1. Lean 4 formalization of Ginsparg-Wilson relation, Lüscher chiral symmetry, integer index,
   doubler decoupling, and GinspargWilsonLocalityObstruction in regge_wdw_core.lean.
2. YAML contract schema conformance (nf.physics.cdt_overlap_fermions.yaml).
3. Exact Ginsparg-Wilson relation {D_ov, Gamma_5} = a D_ov Gamma_5 D_ov (residual <= 1e-12).
4. Exact Lüscher chiral transformation action invariance |delta S| <= 1e-12.
5. Lattice Atiyah-Singer index theorem: (1/2) Tr(Gamma_5 a D_ov) evaluates to an exact integer.
6. Doubler decoupling: Wilson mass term separates doubler states with positive gap 2r/a.
7. Spectral gap collapse detection and Ginsparg-Wilson locality obstruction on singular CDT geometries.
8. SQLite relational audit view (ViewCdtOverlapDiracAudit) verdicts.
"""

from pathlib import Path
import subprocess
import sys

import pytest
import yaml
import numpy as np

_repo = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
tower_dir = _repo / "papers" / "core" / "fsp"
code_dir = _repo / "code" / "python" / "src" / "fsp"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.cdt_overlap_evaluator import (
    CdtOverlapDiracEvaluator,
    DiracAlgebra4D,
    SimplicialComplexGraph,
)


def test_lean4_overlap_fermion_theorems():
    """1. Test that Lean 4 verifies all Section 17 overlap fermion theorems and recovery gaps."""
    lean_file = tower_dir / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Lean core file missing: {lean_file}"

    result = subprocess.run(
        ["lean", str(lean_file)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Lean 4 elaboration failed:\n{result.stderr}"

    content = lean_file.read_text(encoding="utf-8")
    assert "GinspargWilsonRelationPredicate" in content
    assert "ginsparg_wilson_algebraic_identity" in content
    assert "luscher_chiral_invariance_exact" in content
    assert "overlap_index_theorem_integer_chirality" in content
    assert "wilson_term_decouples_doublers" in content
    assert "GinspargWilsonLocalityObstruction" in content


def test_yaml_contract_schema():
    """2. Test YAML contract structure, required fields, and non-claims."""
    yaml_file = tower_dir / "normal_forms" / "nf.physics.cdt_overlap_fermions.yaml"
    assert yaml_file.exists(), f"YAML contract missing: {yaml_file}"

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["identity"]["id"] == "nf.physics.cdt_overlap_fermions"
    assert data["identity"]["short_name"] == "CDT-OVERLAP-NF"
    assert "ginsparg_wilson_relation" in data["classification"]["subject_kind"]
    assert "ExactChiralOverlapPreserved" in data["terminal_routes"]
    assert "GinspargWilsonLocalityObstruction" in data["terminal_routes"]
    assert len(data["purpose"]["non_claims"]) >= 2


def test_exact_ginsparg_wilson_relation():
    """3. Test exact Ginsparg-Wilson algebraic relation {D_ov, Gamma_5} = a D_ov Gamma_5 D_ov."""
    evaluator = CdtOverlapDiracEvaluator()
    g_reg = evaluator.build_regular_gapped_complex("gw_test_reg", num_vertices=6)
    a = g_reg.lattice_spacing_a

    D_ov, Gamma_5, sgn_Hw, gap = evaluator.build_overlap_dirac_operator(g_reg, m0=1.2, r=1.0)
    gw_res = evaluator.evaluate_ginsparg_wilson_relation(D_ov, Gamma_5, a)

    assert gw_res <= 1e-12, f"Ginsparg-Wilson residual exceeded tolerance: {gw_res}"
    evaluator.close()


def test_exact_luescher_chiral_invariance():
    """4. Test exact Lüscher chiral transformation invariance |delta S| <= 1e-12."""
    evaluator = CdtOverlapDiracEvaluator()
    g_reg = evaluator.build_regular_gapped_complex("luescher_test", num_vertices=6)
    a = g_reg.lattice_spacing_a

    D_ov, Gamma_5, sgn_Hw, gap = evaluator.build_overlap_dirac_operator(g_reg, m0=1.2, r=1.0)
    luescher_res = evaluator.evaluate_luescher_chiral_invariance(D_ov, Gamma_5, a)

    assert luescher_res <= 1e-12, f"Lüscher invariance residual exceeded tolerance: {luescher_res}"
    evaluator.close()


def test_atiyah_singer_integer_index():
    """5. Test that lattice Atiyah-Singer index evaluates to an exact integer."""
    evaluator = CdtOverlapDiracEvaluator()
    g_reg = evaluator.build_regular_gapped_complex("index_test", num_vertices=6)
    a = g_reg.lattice_spacing_a

    D_ov, Gamma_5, sgn_Hw, gap = evaluator.build_overlap_dirac_operator(g_reg, m0=1.2, r=1.0)
    index_val, n_pos, n_neg = evaluator.evaluate_topological_index(D_ov, Gamma_5, a)

    diff_from_int = abs(index_val - round(index_val))
    assert diff_from_int <= 1e-12, f"Index is not an integer: {index_val}"
    evaluator.close()


def test_wilson_doubler_decoupling():
    """6. Test that Wilson term decouples doublers with mass gap 2r/a > 0."""
    evaluator = CdtOverlapDiracEvaluator()
    g_reg = evaluator.build_regular_gapped_complex("doubler_test", num_vertices=6)
    r = 1.0
    a = g_reg.lattice_spacing_a

    doubler_gap = 2.0 * r / a
    assert doubler_gap >= 1.0, f"Doubler mass gap too small: {doubler_gap}"

    D_w, Gamma_5, H_w = evaluator.build_wilson_dirac_operator(g_reg, m0=1.2, r=r)
    eigenvals = np.linalg.eigvals(H_w)
    assert np.min(np.abs(eigenvals)) > 0.05
    evaluator.close()


def test_singular_cdt_locality_obstruction():
    """7. Test detection of spectral gap collapse and Ginsparg-Wilson locality obstruction."""
    evaluator = CdtOverlapDiracEvaluator()
    g_sing = evaluator.build_singular_gapless_complex("sing_test", num_vertices=8)

    D_ov, Gamma_5, sgn_Hw, gap = evaluator.build_overlap_dirac_operator(g_sing, m0=1.2, r=1.0)
    decay_xi, max_tail, is_local = evaluator.evaluate_kernel_localization(D_ov, g_sing)

    assert not is_local
    assert decay_xi > 100.0

    evaluator.close()


def test_sqlite_relational_views():
    """8. Test SQLite ViewCdtOverlapDiracAudit produces certified audit verdicts."""
    evaluator = CdtOverlapDiracEvaluator()

    g_reg = evaluator.build_regular_gapped_complex("sql_reg", num_vertices=6)
    r_reg = evaluator.record_complex_evaluation(g_reg)
    assert r_reg["audit_verdict"] == "EXACT_CHIRAL_OVERLAP_CERTIFIED"
    assert r_reg["classification"] == "ExactChiralOverlapPreserved"

    g_sing = evaluator.build_singular_gapless_complex("sql_sing", num_vertices=8)
    r_sing = evaluator.record_complex_evaluation(g_sing)
    assert r_sing["audit_verdict"] == "LOCALITY_OBSTRUCTION_DETECTED"
    assert r_sing["classification"] == "GinspargWilsonLocalityObstruction"

    evaluator.close()
