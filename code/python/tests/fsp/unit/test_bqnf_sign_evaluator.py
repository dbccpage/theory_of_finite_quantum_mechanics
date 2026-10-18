"""
test_bqnf_sign_evaluator.py — Unit Tests for BQNF Sign Evaluator and Cochain Complex
Status: Unit Test Suite
AuthorityEffect: None
"""

import pytest
import sys
from pathlib import Path

# Add code directory to path
current_dir = Path(__file__).resolve().parent
pkg_dir = current_dir.parent.parent
if str(pkg_dir) not in sys.path:
    sys.path.insert(0, str(pkg_dir))

from src.fsp.bqnf_sign_evaluator import (
    CochainComplex,
    BQNFSignEvaluator,
    TerminalRoute
)


class TestBQNFSignEvaluator:
    @pytest.fixture
    def cochain_setup(self):
        # Construct small nilpotent complex: C0 (2) -> C1 (3) -> C2 (1)
        # d0: 3 x 2, d1: 1 x 3 such that d1 . d0 = 0
        d0 = [
            [1.0, -1.0],
            [1.0, 0.0],
            [0.0, 1.0]
        ]
        # d1 = [1.0, -1.0, 1.0]
        # d1 . d0 = [1*(1) + (-1)*(1) + 1*(0), 1*(-1) + (-1)*(0) + 1*(1)] = [0, 0]
        d1 = [
            [1.0, -1.0, 1.0]
        ]
        return CochainComplex(dim_c0=2, dim_c1=3, dim_c2=1, d0=d0, d1=d1)

    def test_exact_repair_routing(self, cochain_setup):
        evaluator = BQNFSignEvaluator(cochain_setup)
        # Pure boundary c1 = d0 * [2.0, 1.0]
        alpha = [2.0, 1.0]
        c1 = [
            1.0 * alpha[0] - 1.0 * alpha[1],  # 1.0
            1.0 * alpha[0],                  # 2.0
            1.0 * alpha[1]                   # 1.0
        ]
        signs = [1, 1, 1]
        res = evaluator.evaluate_sign_packet(c1, signs, tol=1e-4)
        assert res["route"] == TerminalRoute.EXACT_REPAIR
        assert res["phi_1_residual"] == pytest.approx(0.0, abs=1e-3)

    def test_exact_cancellation_meron_routing(self):
        # 4-dim complex for clean meron pair testing
        d0 = [[0.0], [0.0], [0.0], [0.0]]
        d1 = [[1.0, 1.0, 1.0, 1.0]]
        complex_meron = CochainComplex(dim_c0=1, dim_c1=4, dim_c2=1, d0=d0, d1=d1)
        evaluator = BQNFSignEvaluator(complex_meron)

        # Equal weights with opposite signs (Meron clusters)
        c1 = [1.5, 1.5, 2.0, 2.0]
        signs = [1, -1, 1, -1]
        res = evaluator.evaluate_sign_packet(c1, signs)
        assert res["route"] == TerminalRoute.EXACT_CANCELLATION
        assert res["pair_count"] == 2

    def test_open_sign_obstruction_routing(self, cochain_setup):
        evaluator = BQNFSignEvaluator(cochain_setup)
        # Non-boundary, non-cancelling defect
        c1 = [10.0, 0.0, 0.0]
        signs = [1, 1, 1]
        res = evaluator.evaluate_sign_packet(c1, signs)
        assert res["route"] in [TerminalRoute.OPEN_SIGN_OBSTRUCTION, TerminalRoute.STABILIZED_SURVIVOR]
        assert res["phi_1_residual"] > 0.0

    def test_refused_malformed_packet(self, cochain_setup):
        evaluator = BQNFSignEvaluator(cochain_setup)
        # Dimension mismatch: c1 has 4 elements, dim_c1 is 3
        c1 = [1.0, 2.0, 3.0, 4.0]
        signs = [1, 1, 1, 1]
        res = evaluator.evaluate_sign_packet(c1, signs)
        assert res["route"] == TerminalRoute.REFUSED
