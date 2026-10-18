"""Port of ``omega_linear_algebra::linear_algebra::incidence_matrix``.

Oriented edge-node incidence matrix. Convention (matching the Rust source):
- rows are edges;
- columns are nodes;
- for edge ``(source, target)``: entry ``(edge, source) = -1``,
  entry ``(edge, target) = +1``.
"""

from __future__ import annotations
from typing import List, Tuple

import numpy as np


class IncidenceMatrixError(Exception):
    pass


def incidence_matrix(num_nodes: int, edges: List[Tuple[int, int]]) -> np.ndarray:
    """Return the oriented incidence matrix of shape ``(len(edges), num_nodes)``."""
    if num_nodes < 0:
        raise IncidenceMatrixError(f"num_nodes must be non-negative, got {num_nodes}")
    m = np.zeros((len(edges), num_nodes), dtype=np.int64)
    for row, (source, target) in enumerate(edges):
        if source < 0 or target < 0 or source >= num_nodes or target >= num_nodes:
            raise IncidenceMatrixError(
                f"edge index out of bounds at edge {row}: "
                f"({source}, {target}), num_nodes={num_nodes}"
            )
        if source == target:
            raise IncidenceMatrixError(f"self-loop at edge {row}: node={source}")
        m[row, source] = -1
        m[row, target] = 1
    return m

