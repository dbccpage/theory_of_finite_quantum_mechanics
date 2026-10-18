"""2×2 toric code: CSS checks on the torus, rank over F2, and even overlap.

Origin: code/python/src/qm/campaigns/toric.py
Claim: vertex and plaquette checks commute, and n − rank(H_x) − rank(H_z) = 2.
AuthorityEffect: None.
"""


class ToricError(Exception):
    """The toric checks overlapped oddly or the code dimension was not 2."""


def _vertex_support(row: int, col: int) -> set:
    return {
        row * 2 + col,
        row * 2 + ((col - 1) % 2),
        4 + row * 2 + col,
        4 + ((row - 1) % 2) * 2 + col,
    }


def _plaquette_support(row: int, col: int) -> set:
    return {
        row * 2 + col,
        4 + row * 2 + ((col + 1) % 2),
        ((row + 1) % 2) * 2 + col,
        4 + row * 2 + col,
    }


def _rank_f2(rows: list) -> int:
    matrix = [row[:] for row in rows]
    pivot_row = 0
    width = 8
    for col in range(width):
        host = next((r for r in range(pivot_row, len(matrix)) if matrix[r][col] == 1), None)
        if host is None:
            continue
        matrix[pivot_row], matrix[host] = matrix[host], matrix[pivot_row]
        for other in range(len(matrix)):
            if other != pivot_row and matrix[other][col] == 1:
                matrix[other] = [a ^ b for a, b in zip(matrix[other], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row


def toric_dimension() -> int:
    vertices = [_vertex_support(r, c) for r in range(2) for c in range(2)]
    plaquettes = [_plaquette_support(r, c) for r in range(2) for c in range(2)]
    for vertex in vertices:
        for plaquette in plaquettes:
            if len(vertex & plaquette) % 2 != 0:
                raise ToricError("a vertex check anticommutes with a plaquette check")
    def bits(support):
        return [1 if index in support else 0 for index in range(8)]
    rank_z = _rank_f2([bits(support) for support in vertices])
    rank_x = _rank_f2([bits(support) for support in plaquettes])
    dimension = 8 - rank_x - rank_z
    if dimension != 2:
        raise ToricError(f"toric dimension is {dimension}, not 2")
    return dimension
