"""Small exact counterexamples to incomplete dual-witness heuristics."""

import pytest
from finite_obstruction import LinearRepairProblem
from sympy import Matrix


@pytest.mark.parametrize(
    ("repair", "defect", "expected"),
    [
        ([[0], [0]], [0, 5], 5),
        ([[1], [1], [1]], [1, 1, 0], 1),
        ([[1], [0], [0]], [0, 0, 1], 1),
        ([[1], [0], [0]], [0, 1, 1], 2),
        ([[-1, 1, 0], [1, -1, 0], [-1, 0, 1], [1, 0, -1]], [1, 1, -1, -1], 4),
        (
            [
                [-1, 1, 0, 0, 0],
                [0, -1, 1, 0, 0],
                [-1, 0, 1, 0, 0],
                [-1, 0, 0, 1, 0],
                [0, 0, 0, -1, 1],
                [-1, 0, 0, 0, 1],
            ],
            [1, 0, 0, 1, 0, 0],
            2,
        ),
        ([[1], [1]], [1, 0], 1),
    ],
    ids=[
        "zero-column", "ones-column", "missed-kernel-direction",
        "two-kernel-directions", "opposite-circulations",
        "two-triangles", "positive-witness-pairing",
    ],
)
def test_exact_quotient_conformance(repair, defect, expected):
    certificate = LinearRepairProblem(Matrix(repair)).quotient_l1_distance(Matrix(defect))
    assert certificate.distance == expected
    assert certificate.dual_pairing == expected
    assert certificate.verify()


def test_one_feasible_kernel_vector_can_miss_an_obstruction():
    repair = Matrix([[1], [0], [0]])
    defect = Matrix([0, 0, 1])
    feasible = Matrix([0, 1, 0])
    assert repair.T * feasible == Matrix.zeros(1, 1)
    assert max(abs(value) for value in feasible) == 1
    assert (feasible.T * defect)[0] == 0
    assert LinearRepairProblem(repair).quotient_l1_distance(defect).distance == 1
