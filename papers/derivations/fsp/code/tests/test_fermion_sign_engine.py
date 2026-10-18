"""
test_fermion_sign_engine.py — Unit Tests for Fermion Sign Problem Code Suite

Status: Unit Test Suite
AuthorityEffect: None
"""

import pytest
import math
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
pkg_dir = current_dir.parent
if str(pkg_dir) not in sys.path:
    sys.path.insert(0, str(pkg_dir))

from fermion_boson_germ import (
    GermState,
    DirectedCutD2,
    SymmetricLinkS2,
    LoopCycleZ1,
    verify_invariant_blindness,
    swap_action_on_pair
)

from fermionic_hamiltonian import (
    FermionicLattice,
    FockState,
    DiscreteFermionicHamiltonian,
    WheelerDeWittToyConstraint
)

from bqnf_sign_evaluator import (
    CochainComplex,
    BQNFSignEvaluator,
    TerminalRoute
)


class TestFermionBosonGerm:
    def test_germ_genesis_walk(self):
        state = GermState()
        state.step_00_void()
        assert state.stage == 0
        assert len(state.carrier) == 0

        state.step_01_lone_mark("x")
        assert state.stage == 1
        assert state.carrier == {"x"}

        state.step_02_unmarked_pair("x", "y")
        assert state.stage == 2
        assert state.carrier == {"x", "y"}

        d2 = state.step_03_directed_cut("x", "y")
        assert d2.source == "x"
        assert d2.target == "y"
        assert d2.boundary_0chain == {"y": 1, "x": -1}
        assert len(d2.automorphism_group()) == 1

        success, reason = state.step_04_refuse_self_loop("x")
        assert not success
        assert "boundary a - a = 0" in reason

        s2 = state.step_05_symmetric_link("x", "y")
        assert len(s2.automorphism_group()) == 2

    def test_invariant_blindness(self):
        d2 = DirectedCutD2(source="a", target="b")
        preds = [
            lambda pair: set(pair),
            lambda pair: len(pair),
            lambda pair: pair[0] == pair[1]
        ]
        results = verify_invariant_blindness(d2, preds)
        assert all(results.values()), "Every swap-invariant predicate must evaluate identically on D2 and D2_rev"


class TestFermionicHamiltonian:
    def test_bipartite_vs_frustrated_lattice(self):
        chain2 = FermionicLattice.linear_chain(2)
        h_chain = DiscreteFermionicHamiltonian(chain2, t=1.0, u=2.0, num_up=1, num_down=1)
        assert h_chain.dim == 4
        res_chain = h_chain.compute_partition_functions(beta=1.0, trotter_steps=3)
        assert res_chain["z_bosonic"] > 0
        assert res_chain["z_fermionic"] > 0
        assert res_chain["average_sign"] > 0.5

        tri = FermionicLattice.triangle_cluster()
        h_tri = DiscreteFermionicHamiltonian(tri, t=1.0, u=0.0, num_up=2, num_down=0)
        assert h_tri.dim == 3
        res_tri = h_tri.compute_partition_functions(beta=2.0, trotter_steps=3)
        assert res_tri["z_bosonic"] > res_tri["z_fermionic"]
        assert 0.0 < res_tri["average_sign"] < 1.0
        assert res_tri["sign_problem_severity"] > 0.0

    def test_path_generation(self):
        chain2 = FermionicLattice.linear_chain(2)
        h_chain = DiscreteFermionicHamiltonian(chain2, t=1.0, u=0.5, num_up=1, num_down=1)
        paths = h_chain.generate_sample_paths(beta=0.5, trotter_steps=2)
        assert len(paths) > 0
        for p in paths:
            assert "signed_amplitude" in p
            assert "parity" in p
            assert abs(p["signed_amplitude"]) == pytest.approx(p["abs_weight"])

    def test_wheeler_dewitt_toy_constraint(self):
        wdw = WheelerDeWittToyConstraint(
            vertices=[0, 1, 2],
            momenta={0: 1.0, 1: 0.5},
            curvatures={0: 0.2, 1: -0.1, 2: 0.0},
            dual_volumes={0: 1.0, 1: 1.0, 2: 1.0}
        )
        violations = wdw.evaluate_scalar_violations()
        assert len(violations) == 3
        l1_defect = wdw.evaluate_l1_hamiltonian_defect()
        assert l1_defect > 0.0


class TestBQNFSignEvaluator:
    @pytest.fixture
    def cochain_setup(self):
        d0 = [
            [1.0, -1.0],
            [1.0, 0.0],
            [0.0, 1.0]
        ]
        d1 = [
            [1.0, -1.0, 1.0]
        ]
        return CochainComplex(dim_c0=2, dim_c1=3, dim_c2=1, d0=d0, d1=d1)

    def test_exact_repair_routing(self, cochain_setup):
        evaluator = BQNFSignEvaluator(cochain_setup)
        alpha = [2.0, 1.0]
        c1 = [
            1.0 * alpha[0] - 1.0 * alpha[1],
            1.0 * alpha[0],
            1.0 * alpha[1]
        ]
        signs = [1, 1, 1]
        res = evaluator.evaluate_sign_packet(c1, signs, tol=1e-4)
        assert res["route"] == TerminalRoute.EXACT_REPAIR
        assert res["phi_1_residual"] == pytest.approx(0.0, abs=1e-3)

    def test_exact_cancellation_meron_routing(self, cochain_setup):
        d0 = [[0.0], [0.0], [0.0], [0.0]]
        d1 = [[1.0, 1.0, 1.0, 1.0]]
        complex_meron = CochainComplex(dim_c0=1, dim_c1=4, dim_c2=1, d0=d0, d1=d1)
        evaluator = BQNFSignEvaluator(complex_meron)

        c1 = [1.5, 1.5, 2.0, 2.0]
        signs = [1, -1, 1, -1]
        res = evaluator.evaluate_sign_packet(c1, signs)
        assert res["route"] == TerminalRoute.EXACT_CANCELLATION
        assert res["pair_count"] == 2

    def test_open_sign_obstruction_routing(self, cochain_setup):
        evaluator = BQNFSignEvaluator(cochain_setup)
        c1 = [10.0, 0.0, 0.0]
        signs = [1, 1, 1]
        res = evaluator.evaluate_sign_packet(c1, signs)
        assert res["route"] in [TerminalRoute.OPEN_SIGN_OBSTRUCTION, TerminalRoute.STABILIZED_SURVIVOR]
        assert res["phi_1_residual"] > 0.0
