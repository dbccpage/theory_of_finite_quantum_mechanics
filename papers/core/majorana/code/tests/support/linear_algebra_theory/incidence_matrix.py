import numpy as np
from .basic_matrix import BasicMatrix, MatrixError


class IncidenceMatrixError(Exception):
    pass


class EdgeIndexOutOfBounds(IncidenceMatrixError):
    def __init__(self, edge_index, source_node, target_node, num_nodes):
        super().__init__(
            f"edge index out of bounds at edge {edge_index}: "
            f"({source_node}, {target_node}), num_nodes={num_nodes}"
        )


class SelfLoop(IncidenceMatrixError):
    def __init__(self, edge_index, node):
        super().__init__(f"self-loop at edge {edge_index}: node={node}")


def incidence_matrix(num_nodes: int, edges: list) -> BasicMatrix:
    try:
        matrix = BasicMatrix.zero(len(edges), num_nodes, zero_val=0)
    except MatrixError as e:
        raise IncidenceMatrixError(str(e))

    for row, (source, target) in enumerate(edges):
        if source >= num_nodes or target >= num_nodes:
            raise EdgeIndexOutOfBounds(row, source, target, num_nodes)

        if source == target:
            raise SelfLoop(row, source)

        try:
            matrix.set(row, source, -1)
            matrix.set(row, target, 1)
        except MatrixError as e:
            raise IncidenceMatrixError(str(e))

    return matrix


def incidence_matrix_dmatrix(num_nodes: int, edges: list) -> np.ndarray:
    bm = incidence_matrix(num_nodes, edges)
    n_r = bm.rows() if callable(getattr(bm, "rows", None)) else bm.nrows()
    n_c = bm.cols() if callable(getattr(bm, "cols", None)) else bm.ncols()
    arr = np.zeros((n_r, n_c), dtype=int)
    for r in range(n_r):
        for c in range(n_c):
            arr[r, c] = bm.get(r, c)
    return arr

