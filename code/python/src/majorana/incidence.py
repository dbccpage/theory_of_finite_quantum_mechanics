
import numpy as np
from typing import Tuple
try:
    from omega_engine.crates.type.finite_poset import FinitePoset
except ImportError:
    try:
        from omega_engine.crates.type.finite_poset import FinitePoset
    except ImportError:
        from omega_engine.crates.type.finite_poset import FinitePoset


def build_incidence_matrix(poset: FinitePoset) -> Tuple[np.ndarray, dict, list]:
    """
    Build signed incidence matrix B from a FinitePoset.
    B[e, src] = -1, B[e, dst] = +1  for edge e = (src -> dst).
    """
    node_index = {n: i for i, n in enumerate(poset.nodes)}
    m = len(poset.edges)
    n = len(poset.nodes)
    B = np.zeros((m, n))
    for i, (u, v) in enumerate(poset.edges):
        B[i, node_index[u]] = -1.0
        B[i, node_index[v]] = 1.0
    return B, node_index, list(poset.edges)



