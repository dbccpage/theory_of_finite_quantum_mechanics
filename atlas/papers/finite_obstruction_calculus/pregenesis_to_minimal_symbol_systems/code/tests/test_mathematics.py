"""Finite counterexamples and independent characterizations of the paper's laws."""
import itertools
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preservation import (
    bell_pair_distribution,
    boundary,
    chsh,
    component_labels,
    component_totals,
    components,
    cyclic_representative,
    demand_step,
    encode,
    graph_homology_ranks,
    protocol,
    refine,
    report_factor,
    triangle_coboundary,
    triangle_h1_class,
)


def test_report_factor_against_pairwise_criterion():
    for size in range(5):
        for reports in itertools.product(range(3), repeat=size):
            for answers in itertools.product(range(2), repeat=size):
                factor = report_factor(reports, answers)
                criterion = all(reports[i] != reports[j] or answers[i] == answers[j]
                                for i in range(size) for j in range(size))
                assert (factor is not None) == criterion
                if factor is not None:
                    assert set(factor) == set(reports)
                    assert all(factor[r] == s for r, s in zip(reports, answers, strict=True))


def test_empty_image_and_unequal_lengths():
    assert report_factor([], []) == {}
    with pytest.raises(ValueError):
        report_factor([0], [])


def test_demand_accounting_with_rebirth():
    for size in range(6):
        # Per element: absent, birth, retained, discharged, discharged+reborn.
        for status in itertools.product(range(5), repeat=size):
            w = {i for i, x in enumerate(status) if x >= 2}
            d = {i for i, x in enumerate(status) if x >= 3}
            b = {i for i, x in enumerate(status) if x in (1, 4)}
            new = demand_step(w, d, b)
            assert len(new) == len(w) - len(d) + len(b)
            assert new == (w - d) | b


def test_invalid_demand_steps_refused():
    with pytest.raises(ValueError):
        demand_step({0}, {1}, set())
    with pytest.raises(ValueError):
        demand_step({0}, set(), {0})


def test_tag_refinement_and_triangle_coloring():
    refined = refine([0, 0, 0], [0, 1, 2])
    assert [x[0] for x in refined] == [0, 0, 0]
    assert len(set(refined)) == 3
    assert not any(len(set(tags)) == 3 for tags in itertools.product(range(2), repeat=3))


def test_graph_rank_against_components_with_loops_and_repeats():
    for vertices in range(1, 5):
        possible = list(itertools.product(range(vertices), repeat=2))
        for length in range(3):
            for edges in itertools.product(possible, repeat=length):
                h0, h1 = graph_homology_ranks(vertices, edges)
                count = components(vertices, edges)
                assert h0 == count
                assert h1 == len(edges) - vertices + count
    assert graph_homology_ranks(0, []) == (0, 0)


def test_component_coordinates_against_integral_boundary_image():
    for vertices in range(4):
        possible = list(itertools.product(range(vertices), repeat=2))
        for length in range(3):
            for edges in itertools.product(possible, repeat=length):
                image = {boundary(vertices, edges, weights)
                         for weights in itertools.product(range(-2, 3), repeat=length)}
                for chain in itertools.product((-1, 0, 1), repeat=vertices):
                    coordinates = component_totals(vertices, edges, chain)
                    assert (chain in image) == all(total == 0 for _, total in coordinates)
                    assert len(coordinates) == components(vertices, edges)
    assert component_labels(4, [(3, 2), (2, 0), (3, 2), (1, 1)]) == (0, 1, 0, 0)
    assert component_totals(4, [(3, 2), (2, 0)], [2, -1, 3, -2]) == ((0, 3), (1, -1))
    assert component_totals(0, [], []) == ()


def test_component_coordinates_ignore_orientation_and_boundary_additions():
    edges = [(0, 1), (1, 2), (2, 0), (3, 3), (0, 1)]
    chain = (3, -1, 5, -4)
    for weights in itertools.product((-2, 0, 2), repeat=len(edges)):
        change = boundary(4, edges, weights)
        shifted = tuple(a+b for a, b in zip(chain, change, strict=True))
        assert component_totals(4, edges, shifted) == component_totals(4, edges, chain)
    assert component_totals(4, [(b, a) for a, b in edges], chain) == component_totals(4, edges, chain)
    with pytest.raises(ValueError):
        component_totals(2, [], [1])


@pytest.mark.parametrize("record", ["v1\tcomponents\t2\t0,2\t1,1",
    "v1\tcomponents\t2\t0\t1,1", "v1\tcomponents\t2\t\t1",
    "v1\tcomponents\t9\t\t", "v1\tcomponents\t02\t\t1,1"])
def test_component_protocol_refuses_invalid_records(record):
    assert protocol(record) == "REFUSE"


def test_bridge_and_filled_triangle():
    assert boundary(2, [(0, 1)], [1]) == (-1, 1)
    assert graph_homology_ranks(2, []) == (2, 0)
    assert graph_homology_ranks(2, [(0, 1)]) == (1, 0)
    edges = [(0, 1), (1, 2), (2, 0)]
    assert boundary(3, edges, [1, 1, 1]) == (0, 0, 0)
    assert graph_homology_ranks(3, edges) == (1, 1)
    # Attaching one face with boundary (1,1,1) kills that rank-one kernel.
    assert boundary(3, edges, [7, 7, 7]) == (0, 0, 0)


def test_triangle_kernel_against_integer_boundary_and_attachment():
    edges = [(0, 1), (1, 2), (2, 0)]
    for chain in itertools.product(range(-5, 6), repeat=3):
        cycle = boundary(3, edges, chain) == (0, 0, 0)
        if cycle:
            k = triangle_h1_class(False, chain)
            assert chain == (k, k, k)
            assert triangle_h1_class(True, chain) == 0
        else:
            for filled in (False, True):
                with pytest.raises(ValueError):
                    triangle_h1_class(filled, chain)
    for k, j in itertools.product(range(-8, 9), repeat=2):
        left, right = (k, k, k), (j, j, j)
        difference = tuple(a-b for a, b in zip(left, right, strict=True))
        # No two-cells before attachment; one face after attachment.
        assert (triangle_h1_class(False, left) == triangle_h1_class(False, right)) == (difference == (0, 0, 0))
        assert difference == (k-j, k-j, k-j)
        assert triangle_h1_class(True, left) == triangle_h1_class(True, right)
    with pytest.raises(ValueError):
        triangle_h1_class(False, [1, 1])


@pytest.mark.parametrize("record", ["v1\ttriangle\t0\t1,1,0", "v1\ttriangle\t1\t1,0,1",
    "v1\ttriangle\t2\t1,1,1", "v1\ttriangle\t01\t1,1,1",
    "v1\ttriangle\t0\t1,1", "v1\ttriangle\t0\t1000001,1000001,1000001"])
def test_triangle_protocol_refuses_noncycles_and_invalid_records(record):
    assert protocol(record) == "REFUSE"


def test_dual_triangle_pairing_and_square_zero():
    """Check the circulation dual witness and a constructive primal repair."""
    # Independently encode the vertex-to-edge differential. The row (1,1,1)
    # annihilates each column, so a nonzero pairing rules out every potential.
    differential_columns = ((-1, 0, 1), (1, -1, 0), (0, 1, -1))
    dual_witness = (1, 1, 1)
    assert all(sum(a*b for a, b in zip(dual_witness, col, strict=True)) == 0
               for col in differential_columns)
    for cochain in itertools.product(range(-4, 5), repeat=3):
        for k in range(-4, 5):
            pairing = sum(phi * edge for phi, edge in zip(cochain, (k, k, k), strict=True))
            assert triangle_coboundary(cochain) * k == pairing
        p, q, r = cochain
        circulation = sum(a*b for a, b in zip(dual_witness, cochain, strict=True))
        potential = (0, p, p+q)
        repaired = tuple(sum(potential[j] * differential_columns[j][i]
                             for j in range(3)) for i in range(3))
        assert (repaired == cochain) == (circulation == 0)
        if circulation != 0:
            # This is an impossibility certificate, independent of a search bound.
            assert sum(repaired) == 0 and repaired != cochain
        coboundary_from_vertices = (q-p, r-q, p-r)
        assert triangle_coboundary(coboundary_from_vertices) == 0
    with pytest.raises(ValueError):
        triangle_coboundary([1, 2])
    assert protocol("v1\tcochain\t1000000,1000000,1000000") == "3000000"
    assert protocol("v1\tcochain\t1,2,03") == "REFUSE"


def test_exact_uniform_pair_distributions_and_target_correlations():
    correlations = []
    for x, y in itertools.product((False, True), repeat=2):
        p = bell_pair_distribution(x and not y)
        assert all(value >= 0 for value in p)
        assert sum(p) == 1
        assert (p[0]+p[1], p[2]+p[3], p[0]+p[2], p[1]+p[3]) == (Fraction(1, 2),)*4
        correlations.append(p[0]-p[1]-p[2]+p[3])
    assert correlations == [1, 1, -1, 1]
    for flag in ("2", "01", "-1", "+1", "١", ""):
        assert protocol("v1\tbellpair\t"+flag) == "REFUSE"


def test_nonuniquely_decodable_code():
    assert encode("aa") == encode("b") == "00"
    assert encode("ab") == encode("ba") == "000"
    with pytest.raises(ValueError):
        encode("c")


def test_chsh_orientation_and_deterministic_obstruction():
    assert chsh([1, 1, -1, 1]) == (0, 4)
    target = (1, 1, -1, 1)
    for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4):
        signs = (a0*b0, a0*b1, a1*b0, a1*b1)
        assert signs != target
        assert signs[0]*signs[1]*signs[2]*signs[3] == 1


def test_integral_quotient_classes_against_divisibility():
    for modulus, x, y in itertools.product(range(-5, 6), range(-8, 9), range(-8, 9)):
        same_class = (x == y if modulus == 0 else (x-y) % modulus == 0)
        assert (cyclic_representative(modulus, x) == cyclic_representative(modulus, y)) == same_class
        if modulus:
            assert 0 <= cyclic_representative(modulus, x) < abs(modulus)
    assert cyclic_representative(2, 1) != 0
    assert cyclic_representative(2, 1+1) == 0
    assert cyclic_representative(0, -3) == -3


@pytest.mark.parametrize("record", ["v1\tcyclic\t2", "v1\tcyclic\t2,1,0",
    "v1\tcyclic\t02,1", "v1\tcyclic\t2,1000001", "v1\tcyclic\t٢,1"])
def test_cyclic_protocol_refuses_invalid_records(record):
    assert protocol(record) == "REFUSE"


@pytest.mark.parametrize("record", ["v2\tcode\ta", "v1\tcode\tc", "v1\tdemand\t2\t4\t0\t0",
    "v1\tdemand\t2\t1\t2\t0", "v1\tdemand\t2\t1\t0\t1",
    "v1\tfactor\t0\t", "v1\tboundary\t1\t0,1\t1",
    "v1\tboundary\t2\t0\t1", "v1\tchsh\t1,1,1", "v1\tcode\t"+"a"*65])
def test_protocol_refuses_invalid_records(record):
    assert protocol(record) == "REFUSE"


def test_graph_ranks_reject_negative_vertices_without_edges():
    with pytest.raises(ValueError, match="invalid graph dimensions"):
        graph_homology_ranks(-1, [])
