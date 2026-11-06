"""Independent exhaustive finite checks, not a substitute for the group proof."""
from itertools import permutations, product

import pytest

from finite_graph_dressing import Edge, Permutation, forest_dressing, gauge_transform

GROUP = tuple(Permutation(p) for p in permutations(range(3)))
ONE = Permutation.identity(3)


def test_all_s3_triangle_connections_against_closed_walk_and_brute_gauges():
    for a, b, c in product(GROUP, repeat=3):
        edges = (Edge(0, 1, a), Edge(1, 2, b), Edge(2, 0, c))
        result = forest_dressing(3, 3, edges)
        # Independent rooted gauge search does not use the tree algorithm.
        exists = any(all(e.value == g[e.target].inverse() * g[e.source] for e in edges)
                     for x, y in product(GROUP, repeat=2) for g in [(ONE, x, y)])
        assert result.neutralizes() == (c * b * a == ONE) == exists
        assert all(result.residuals[i] == ONE for i in result.tree_edges)


def test_noncommutative_tree_change_and_unrooted_gauge_covariance():
    a, b = Permutation((1, 0, 2)), Permutation((0, 2, 1))
    assert a * b != b * a
    edges = (Edge(0, 1, a), Edge(1, 2, b), Edge(2, 0, ONE), Edge(0, 2, a))
    first = forest_dressing(3, 3, edges)
    second = forest_dressing(3, 3, edges, (3, 2, 1, 0))
    assert first.tree_edges != second.tree_edges
    change = tuple(y.inverse() * x for x, y in zip(first.transports, second.transports))
    for i, e in enumerate(edges):
        assert second.residuals[i] == change[e.target] * first.residuals[i] * change[e.source].inverse()
    for gauge in product(GROUP, repeat=3):
        transformed = forest_dressing(3, 3, gauge_transform(edges, gauge))
        for i, residual in enumerate(first.residuals):
            assert transformed.residuals[i] == gauge[0] * residual * gauge[0].inverse()


def test_disconnected_parallel_loops_and_isolated_vertices():
    a = Permutation((1, 0, 2))
    edges = (Edge(1, 0, a), Edge(1, 0, a), Edge(2, 2, ONE))
    result = forest_dressing(4, 3, edges)
    assert result.neutralizes()
    assert result.roots == (0, 0, 2, 3)
    assert len(result.tree_edges) == 1
    assert not forest_dressing(4, 3, edges + (Edge(2, 2, a),)).neutralizes()
    assert not forest_dressing(2, 3, (Edge(0, 1, a), Edge(0, 1, ONE))).neutralizes()
    assert forest_dressing(0, 3, ()).neutralizes()


def test_local_face_flatness_does_not_neutralize_a_second_cycle():
    a = Permutation((1, 0, 2))
    edges = (Edge(0, 1, ONE), Edge(1, 2, ONE), Edge(2, 0, ONE),
             Edge(2, 3, ONE), Edge(3, 0, a))
    assert edges[2].value * edges[1].value * edges[0].value == ONE
    assert not forest_dressing(4, 3, edges).neutralizes()


@pytest.mark.parametrize('vertices,degree,edges,order', [
    (True, 3, (), None), (-1, 3, (), None), (0, True, (), None),
    (1, 3, (Edge(0, 1, ONE),), None), (1, 3, (Edge(False, 0, ONE),), None),
    (1, 2, (Edge(0, 0, ONE),), None), (1, 3, (Edge(0, 0, ONE),), ()),
    (1, 3, (Edge(0, 0, ONE),), (0, 0)), (1, 3, (Edge(0, 0, ONE),), (False,)),
])
def test_malformed_graphs_are_refused(vertices, degree, edges, order):
    with pytest.raises(ValueError):
        forest_dressing(vertices, degree, edges, order)


@pytest.mark.parametrize('image', [(0, 0), (1,), (False,), (0.0,), [0]])
def test_inexact_or_nonbijective_carriers_are_refused(image):
    with pytest.raises(ValueError):
        Permutation(image)
