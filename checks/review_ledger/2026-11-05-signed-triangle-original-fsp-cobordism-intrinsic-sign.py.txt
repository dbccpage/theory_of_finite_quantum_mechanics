"""Exact diagonal-conjugation audit for signed triangle adjacency matrices.

Only the vertex-sign switching representation class is considered.
"""
from itertools import product


def multiply(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))


def main() -> None:
    balanced = 0
    cases = 0
    for a, b, c in product((-1, 1), repeat=3):
        adjacency = ((0, a, c), (a, 0, b), (c, b, 0))
        cycle = a * b * c
        can_be_positive = False
        for gauge in product((-1, 1), repeat=3):
            diagonal = tuple(tuple(gauge[i] if i == j else 0 for j in range(3))
                             for i in range(3))
            transformed = multiply(multiply(diagonal, adjacency), diagonal)
            edges = (transformed[0][1], transformed[1][2], transformed[2][0])
            if edges[0] * edges[1] * edges[2] != cycle:
                raise SystemExit("cycle product changed under diagonal conjugation")
            can_be_positive |= edges == (1, 1, 1)
            if gauge == (1, a, a * b) and edges != (1, 1, cycle):
                raise SystemExit("constructive normal form failed")
            cases += 1
        if can_be_positive != (cycle == 1):
            raise SystemExit("switching classification failed")
        balanced += can_be_positive
    if balanced != 4 or cases != 64:
        raise SystemExit("finite family count mismatch")
    print(f"triangles=8 switching_cases={cases} balanced={balanced} "
          f"obstructed={8-balanced} failures=0")


if __name__ == "__main__":
    main()
