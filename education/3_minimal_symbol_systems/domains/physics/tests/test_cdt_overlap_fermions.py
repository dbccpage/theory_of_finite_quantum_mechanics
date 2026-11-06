"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import subprocess
import sys
from pathlib import Path

import numpy as np
import yaml

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from cdt_overlap_evaluator import (
    CdtOverlapDiracEvaluator,
)






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

    # Check integer proximity
    diff_from_int = abs(index_val - round(index_val))
    assert diff_from_int <= 1e-12, f"Index is not an integer: {index_val}"
    evaluator.close()
