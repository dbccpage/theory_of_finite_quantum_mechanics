r"""
Feynman Path-Sum Graded Transport Test Suite (`QM_031`).

Verifies discrete $1$-cochain phase fiber summation and matrix power equivalence:
  M^n_{u, v} = \sum_{\gamma \in \text{Paths}_n(u, v)} \prod_{e \in \gamma} w(e) e^{i \theta(e)}

Under Chapman-Kolmogorov composition:
  M^{a+b} = M^a \cdot M^b
"""

import math
import cmath


class DiscreteGraph:
    """Finite weighted graph with U(1) 1-cochain phase fibers."""

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.weights = [
            [0.0 + 0.0j for _ in range(num_nodes)] for _ in range(num_nodes)
        ]

    def set_edge(self, src: int, dst: int, weight: float, phase_rad: float):
        self.weights[src][dst] = weight * cmath.exp(1j * phase_rad)

    def transition_matrix(self):
        return self.weights


def matrix_multiply(A, B):
    n = len(A)
    C = [[0.0 + 0.0j for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def matrix_power(A, power: int):
    n = len(A)
    result = [
        [1.0 + 0.0j if i == j else 0.0 + 0.0j for j in range(n)] for i in range(n)
    ]
    base = A
    p = power
    while p > 0:
        if p % 2 == 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        p //= 2
    return result


def enumerate_path_sum(
    graph: DiscreteGraph, src: int, dst: int, length: int
) -> complex:
    """Recursively sum products of 1-cochain phase fibers along all length-n paths."""
    n = graph.num_nodes
    if length == 0:
        return 1.0 + 0.0j if src == dst else 0.0 + 0.0j

    total_amplitude = 0.0 + 0.0j
    for nxt in range(n):
        w = graph.weights[src][nxt]
        if abs(w) > 0:
            total_amplitude += w * enumerate_path_sum(graph, nxt, dst, length - 1)
    return total_amplitude


def test_feynman_path_sum_matrix_power_equivalence():
    """Verify that 1-cochain path sum matches matrix power M^n for QM_031."""
    g = DiscreteGraph(3)
    g.set_edge(0, 1, 0.707, math.pi / 4)
    g.set_edge(0, 2, 0.707, -math.pi / 4)
    g.set_edge(1, 2, 1.0, math.pi / 2)
    g.set_edge(2, 0, 1.0, 0.0)

    M = g.transition_matrix()
    M_3 = matrix_power(M, 3)

    for i in range(3):
        for j in range(3):
            path_amp = enumerate_path_sum(g, i, j, 3)
            mat_amp = M_3[i][j]
            assert abs(path_amp - mat_amp) < 1e-10


def test_chapman_kolmogorov_composition():
    """Verify matrix power composition law M^(a+b) = M^a * M^b."""
    g = DiscreteGraph(4)
    g.set_edge(0, 1, 0.5, 0.1)
    g.set_edge(1, 2, 0.8, 0.3)
    g.set_edge(2, 3, 0.6, 0.5)
    g.set_edge(3, 0, 0.9, 0.7)

    M = g.transition_matrix()
    M_2 = matrix_power(M, 2)
    M_3 = matrix_power(M, 3)
    M_5_expected = matrix_power(M, 5)

    M_5_composed = matrix_multiply(M_2, M_3)

    for i in range(4):
        for j in range(4):
            assert abs(M_5_composed[i][j] - M_5_expected[i][j]) < 1e-10
