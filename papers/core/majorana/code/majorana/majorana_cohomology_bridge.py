"""Bridge connecting anomalon Network cochains to omega_engine.crates.majorana GF(2) parity cohomology solvers.

Maps continuous/discrete L1 edge residual parities to F2 boundary matrices (GF2Matrix).
``betti_1_f2`` is native ``majorana_gf2_diagnostic`` operation ``classify`` ``dim_h1``.
Majorana parity obstruction certificates carry AuthorityEffect = None.
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np

# Ensure code directories are in sys.path
code_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path(".")
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

majorana_dir = code_dir.parents[2] / "omega_engine.crates.majorana"
if str(majorana_dir) not in sys.path and majorana_dir.exists():
    sys.path.insert(0, str(majorana_dir))

from omega_engine.crates.residuals.network_residual import Network, build_incidence
from omega_engine.crates.majorana.core.gf2_diagnostic import classify_native
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix


@dataclass(frozen=True)
class MajoranaParityCert:
    """Certificate tracking GF(2) Majorana parity obstruction and F2 Betti number."""
    network_nodes: int
    network_edges: int
    gf2_rank: int
    betti_1_f2: int
    is_solvable: bool
    total_parity_sum: int
    authority_effect: str = "None"

    def is_valid(self) -> bool:
        return self.authority_effect == "None"


def evaluate_network_majorana_parity(
    network: Network,
    edge_values: Dict[Tuple[Any, Any], float] | None = None,
    threshold: float = 1e-4,
) -> MajoranaParityCert:
    """Evaluates GF(2) parity obstruction over a anomalon Network topology."""
    n_v, n_e = len(network.nodes), len(network.edges)
    if n_e == 0:
        return MajoranaParityCert(
            network_nodes=n_v,
            network_edges=0,
            gf2_rank=0,
            betti_1_f2=0,
            is_solvable=True,
            total_parity_sum=0,
        )

    # 1. Build GF(2) incidence matrix from Network edges
    d0_gf2_rows = []
    node_idx = {n: i for i, n in enumerate(network.nodes)}
    for u, v in network.edges:
        row = [0] * n_v
        row[node_idx[u]] = 1
        row[node_idx[v]] = 1
        d0_gf2_rows.append(row)

    gf2_mat = GF2Matrix(d0_gf2_rows)
    _, pivots = gf2_mat.rref()
    rank_f2 = len(pivots)

    # 2. Extract binary parity defect vector b from edge values under threshold
    if edge_values is not None:
        b_vec = [1 if abs(edge_values.get(e, 0.0)) > threshold else 0 for e in network.edges]
    else:
        # Default: boundary mode defect at edge 0
        b_vec = [0] * n_e
        b_vec[0] = 1

    total_parity = sum(b_vec) % 2
    # dim_h1 and the Exact schedule are native classify, not n_e - rank.
    # A zero face keeps the graph rectangular; it does not add a constraint.
    measured = classify_native(d0_gf2_rows, [[0] * n_e], b_vec, budget=1)
    dim = measured["dim_h1"]
    if isinstance(dim, bool) or not isinstance(dim, int):
        raise ValueError("native classify returned no dim_h1")
    betti_1_f2 = dim
    is_solvable = measured["terminal"] == "Exact"

    return MajoranaParityCert(
        network_nodes=n_v,
        network_edges=n_e,
        gf2_rank=rank_f2,
        betti_1_f2=betti_1_f2,
        is_solvable=is_solvable,
        total_parity_sum=total_parity,
    )


if __name__ == "__main__":
    # Test on a 10-site Kitaev ring network topology
    nodes = list(range(10))
    edges = [(i, (i + 1) % 10) for i in range(10)]
    ring_net = Network(nodes=nodes, edges=edges)

    cert = evaluate_network_majorana_parity(ring_net)
    print("=== Majorana Parity Cohomology Bridge Test ===")
    print(f"Nodes: {cert.network_nodes}, Edges: {cert.network_edges}")
    print(f"GF(2) Rank: {cert.gf2_rank}, F2 Betti b1: {cert.betti_1_f2} (native classify dim_h1)")
    print(f"Is Parity Defect Solvable: {cert.is_solvable}")
    print(f"Total Parity Sum: {cert.total_parity_sum}")
    print(f"AuthorityEffect: {cert.authority_effect}")







