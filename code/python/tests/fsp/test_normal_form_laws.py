"""Exact laws, independent quotient invariants, and adversarial old failures."""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.fsp.bqnf_sign_evaluator import (
    BQNFSignEvaluator, CochainComplex, TerminalRoute, normalize_sign_cochain,
)


def evaluator(d0, d1=None, columns=None):
    return BQNFSignEvaluator(CochainComplex(
        len(d0[0]) if d0 else (columns or 0), len(d0), len(d1 or []), d0, d1 or []))


@pytest.mark.parametrize("entries", list(product((-1, 0, 1), repeat=4)))
def test_rational_section_soundness_idempotence_and_gauge_invariance(entries):
    matrix = [list(entries[:2]), list(entries[2:])]
    engine = evaluator(matrix)
    for c in product((-1, 0, 1), repeat=2):
        normal = engine.normalize_cochain(c)
        assert tuple(c[i] - sum(Q(matrix[i][j]) * normal.gauge[j] for j in range(2)) for i in range(2)) == normal.representative
        assert engine.normalize_cochain(normal.representative).representative == normal.representative
        for alpha in product((-1, 0, 1), repeat=2):
            shifted = [c[i] + sum(matrix[i][j] * alpha[j] for j in range(2)) for i in range(2)]
            assert engine.normalize_cochain(shifted).representative == normal.representative


def test_rational_completeness_against_independent_annihilator():
    engine = evaluator([[1, -1], [1, 0], [0, 1]], [[1, -1, 1]])
    representatives = {}
    for c in product(range(-2, 3), repeat=3):
        invariant = c[0] - c[1] + c[2]
        normal = engine.normalize_cochain(c).representative
        assert normal == (0, 0, invariant)
        representatives.setdefault(invariant, normal)
        assert representatives[invariant] == normal
    assert len(set(representatives.values())) == len(representatives)


def test_rational_normal_form_independent_of_gauge_generator_basis():
    one = evaluator([[1, -1], [1, 0], [0, 1]])
    two = evaluator([[-1, 2, 0], [0, 1, 0], [1, -1, 0]])
    for c in product((-1, 0, 1), repeat=3):
        assert one.normalize_cochain(c).representative == two.normalize_cochain(c).representative


def test_l1_section_is_not_l1_minimizer_and_exact_distance_is():
    engine = evaluator([[1], [2]])
    assert engine.normalize_cochain([1, 0]).representative == (0, -2)
    for c in product((Q(-1, 3), 0, Q(5, 7)), repeat=2):
        distance, gauge = engine.solve_quotient_distance(c)
        assert distance == abs(2 * c[0] - c[1]) / 2
        assert distance == sum(abs(c[i] - (i + 1) * gauge[0]) for i in range(2))


def test_exact_distance_and_membership_survive_exponential_budget_refusal():
    engine = evaluator([[1, 0], [0, 1], [1, 1], [1, -1]])
    with pytest.raises(RuntimeError, match="budget"):
        engine.solve_quotient_distance([1, 0, 0, 0], max_candidates=1)
    packet = engine.evaluate_sign_packet([1, 0, 0, 0], [1] * 4, max_candidates=1)
    assert packet["distance_status"] == "budget_unknown"
    assert packet["phi_1_residual"] is None
    assert packet["route"] == TerminalRoute.STABILIZED_SURVIVOR
    repaired = engine.evaluate_sign_packet([1, 0, 1, 1], [1] * 4, max_candidates=1)
    assert repaired["route"] == TerminalRoute.EXACT_REPAIR
    assert repaired["phi_1_residual"] == 0


@pytest.mark.parametrize("vertex_count,edges", [
    (0, []), (3, []), (2, [(0, 1)]), (3, [(0, 1), (1, 2), (2, 0)]),
    (4, [(0, 1), (0, 1), (2, 2)]),
    (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
])
def test_sign_section_exhaustive_soundness_idempotence_completeness(vertex_count, edges):
    classes = {}
    for signs in product((0, 1), repeat=len(edges)):
        normal = normalize_sign_cochain(vertex_count, edges, signs)
        assert normal.parities == tuple(s ^ normal.gauge[u] ^ normal.gauge[v] for s, (u, v) in zip(signs, edges))
        assert all(normal.parities[i] == 0 for i in normal.forest_edges)
        assert normalize_sign_cochain(vertex_count, edges, normal.parities).parities == normal.parities
        orbit = {
            tuple(s ^ alpha[u] ^ alpha[v] for s, (u, v) in zip(signs, edges))
            for alpha in product((0, 1), repeat=vertex_count)
        }
        for shifted in orbit:
            assert normalize_sign_cochain(vertex_count, edges, shifted).parities == normal.parities
        if normal.parities in classes:
            assert classes[normal.parities] == orbit
        classes[normal.parities] = orbit
        for cycle in normal.obstruction_cycles:
            assert sum(signs[i] for i in cycle) % 2 == 1
            assert all(sum((edges[i][0] == v) + (edges[i][1] == v) for i in cycle) % 2 == 0 for v in range(vertex_count))
        assert bool(normal.obstruction_cycles) == any(normal.parities)
    assert sum(len(orbit) for orbit in classes.values()) == 2 ** len(edges)


@pytest.mark.parametrize("weights,signs", [([1, Q(10000001, 10000000)], [1, -1]), ([2, 1, 1], [1, -1, -1])])
def test_near_equal_or_zero_total_does_not_imply_equal_weight_pairing(weights, signs):
    assert evaluator([[0]]).search_meron_involution(weights, signs) is None


def test_no_tolerance_certifies_nonzero_residual_or_nilpotence():
    engine = evaluator([[0]], [[1]])
    packet = engine.evaluate_sign_packet([Q(1, 10**30)], [1], tol=1)
    assert packet["route"] == TerminalRoute.OPEN_SIGN_OBSTRUCTION
    assert packet["phi_1_residual"] == Q(1, 10**30)
    with pytest.raises(ValueError, match="d1"):
        evaluator([[1]], [[Q(1, 10**30)]])


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), True, "1/0"])
def test_invalid_exact_coefficients_are_refused(bad):
    assert evaluator([[0]]).evaluate_sign_packet([bad], [1])["route"] == TerminalRoute.REFUSED


def test_exact_pairing_checks_all_active_rows_and_input_signs():
    engine = evaluator([[0]])
    witness = engine.search_meron_involution([Q(1, 3), 0, Q(1, 3)], [1, 1, -1])
    assert witness.mapping == {0: 2, 2: 0}
    for weights, signs in [([1], [0]), ([1], [True]), ([1, 1], [1]), ([-1, -1], [1, -1])]:
        with pytest.raises(ValueError):
            engine.search_meron_involution(weights, signs)


def test_empty_and_zero_dimensional_complexes():
    engine = evaluator([], columns=2)
    normal = engine.normalize_cochain([])
    assert normal.representative == () and normal.gauge == (0, 0)
    assert engine.solve_quotient_distance([]) == (0, [0, 0])
    with pytest.raises(ValueError, match="dimension"):
        CochainComplex(2, 1, 0, [[1]], [])
