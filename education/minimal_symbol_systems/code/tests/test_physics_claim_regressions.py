"""Independent counterexamples for retained finite-model checks."""
import sys
from pathlib import Path

import numpy as np
import pytest

DOMAINS = Path(__file__).resolve().parents[2] / 'domains'
sys.path[:0] = [str(DOMAINS / 'physics/code'), str(DOMAINS / 'ansi_sql/code')]
from cdt_overlap_evaluator import CdtOverlapDiracEvaluator
from cdt_spectral_dimension import DiscreteHeatDiffusionEngine
from cdt_matter_coupling import CoupledCdtMatterEngine
from nonabelian_anyon_evaluator import NonAbelianAnyonEvaluator


def test_missing_associator_data_cannot_pass():
    e = NonAbelianAnyonEvaluator()
    try:
        assert not e.verify_f_matrix_involution()['is_consistent']
    finally:
        e.close()


def test_braid_check_rejects_zero_r_matrix():
    e = NonAbelianAnyonEvaluator()
    try:
        e.populate_fibonacci_model()
        assert e.verify_braid_relation()['is_consistent']
        e.conn.execute('UPDATE AnyonRMatrices SET val_re=0, val_im=0')
        assert not e.verify_braid_relation()['is_consistent']
    finally:
        e.close()


def test_partial_associator_cannot_pass():
    e = NonAbelianAnyonEvaluator()
    try:
        e.populate_fibonacci_model()
        e.conn.execute('DELETE FROM AnyonFSymbols WHERE e != f')
        assert not e.verify_braid_relation()['is_consistent']
    finally:
        e.close()


def test_overlap_index_agrees_with_positive_zero_mode():
    gamma = np.diag([1., -1.])
    d = np.diag([0., 2.])
    assert np.array_equal(d @ gamma + gamma @ d, d @ gamma @ d)
    assert CdtOverlapDiracEvaluator.evaluate_topological_index(None, d, gamma) == (1., 1, 0)


def test_chirality_is_basis_invariant():
    d = np.diag([0., 0., 2., 2.])
    gamma = np.diag([1., 1., -1., -1.])
    u, _ = np.linalg.qr(np.random.default_rng(19).normal(size=(4, 4)))
    index, plus, minus = CdtOverlapDiracEvaluator.evaluate_topological_index(None, u @ d @ u.T, u @ gamma @ u.T)
    assert index == pytest.approx(2.)
    assert (plus, minus) == (2, 0)


def test_isolated_graph_vertex_preserves_probability():
    assert DiscreteHeatDiffusionEngine.compute_return_probability_random_walk(1, [[]], tau_max=4) == [1.] * 5


def test_graph_trace_is_invariant_under_vertex_relabeling():
    adjacency = [[1], [0]] + [[] for _ in range(40)]
    order = list(reversed(range(42)))
    inverse = {old: new for new, old in enumerate(order)}
    relabeled = [[inverse[v] for v in adjacency[u]] for u in order]
    f = DiscreteHeatDiffusionEngine.compute_return_probability_random_walk
    assert f(42, adjacency, tau_max=3) == pytest.approx(f(42, relabeled, tau_max=3))


def test_matter_diffusion_depends_on_graph():
    f = CoupledCdtMatterEngine.evaluate_coupled_diffusion
    isolated = f({0: []}, max_tau=5)
    connected = f({0: [1], 1: [0, 2], 2: [1]}, max_tau=5)
    assert all(v == pytest.approx(0.) for v in isolated.values())
    assert isolated != connected

@pytest.mark.parametrize('matrix,clocks,state', [([], 0, None), ([[1.]], 2, [0.]), ([[float('nan')]], 2, None)])
def test_history_rejects_invalid_inputs(matrix, clocks, state):
    from regge_wdw_evaluator import ReggeWdwEvaluator
    e = ReggeWdwEvaluator()
    try:
        with pytest.raises(ValueError):
            e.evaluate_finite_history('invalid', matrix, clocks, state)
    finally:
        e.close()


def test_missing_fusion_table_cannot_pass():
    e = NonAbelianAnyonEvaluator()
    try:
        assert not e.verify_fusion_associativity()['is_associative']
    finally:
        e.close()
