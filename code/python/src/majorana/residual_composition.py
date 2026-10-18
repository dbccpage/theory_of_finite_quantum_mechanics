r"""
Level 3: Finite Composition Functor Structures.
AuthorityEffect: None.

Recovered verbatim from ``use_cases/level3_residual_composition.py`` as of
``ca2e966c95^`` — the letter purge folded the class into ``a.py`` and the
de-lettering then deleted it while ``code/pipeline.py`` kept importing it.
Only the imports are adapted to the consolidated layout; the mathematical
body is unchanged.
"""

from typing import Any, Dict, List, Tuple
import numpy as np

from omega_engine.crates.quantum_physics.primitives import partial_trace_a, partial_trace_b, trace_norm
from omega_engine.crates.obstruction_theory.levels_crosswalk import Level1FiniteObstruction


class Level3ResidualComposition:
    """Level 3: Finite Composition Functor Structures."""

    @staticmethod
    def cartesian_product_carriers(
        carrier_a: Tuple[List[int], List[Tuple[int, int]], List[Tuple[int, int, int]]],
        carrier_b: Tuple[List[int], List[Tuple[int, int]], List[Tuple[int, int, int]]]
    ) -> Dict[str, Any]:
        """Construct Cartesian product A x B of two 2-truncated simplicial carriers."""
        nodes_a, edges_a, faces_a = carrier_a
        nodes_b, edges_b, faces_b = carrier_b

        nodes_ab = [(u, x) for u in nodes_a for x in nodes_b]

        edges_ab = []
        for (u, v) in edges_a:
            for x in nodes_b:
                edges_ab.append(((u, x), (v, x)))
        for u in nodes_a:
            for (x, y) in edges_b:
                edges_ab.append(((u, x), (u, y)))

        foc_a = Level1FiniteObstruction(len(nodes_a), edges_a, faces_a)
        foc_b = Level1FiniteObstruction(len(nodes_b), edges_b, faces_b)
        cochain_a = np.ones(len(edges_a))
        cochain_b = np.ones(len(edges_b))

        l1_a = foc_a.compute_l1_gauge_norm(cochain_a)
        l1_b = foc_b.compute_l1_gauge_norm(cochain_b)
        composite_bound = l1_a + l1_b

        return {
            "n_nodes": len(nodes_ab),
            "n_edges": len(edges_ab),
            "l1_norm_a": l1_a,
            "l1_norm_b": l1_b,
            "l1_composite_subadditive_bound": composite_bound,
            "structure_type": "CartesianProduct",
            "tomography_status": "TRIVIAL_PROJECTIONS_AVAILABLE"
        }

    @staticmethod
    def local_tomography_test_harness(rho_ab: np.ndarray) -> Dict[str, Any]:
        """Local tomography test harness for residual composition candidates."""
        rho_a = partial_trace_b(rho_ab)
        rho_b = partial_trace_a(rho_ab)
        rho_tensor = np.kron(rho_a, rho_b)

        defect = trace_norm(rho_ab - rho_tensor)
        is_factorized = defect < 1e-12

        return {
            "residual_defect": defect,
            "local_tomography_exact": is_factorized,
            "contract_status": "PASSED" if is_factorized else "FRONTIER_NON_ZERO_RESIDUAL"
        }

    @staticmethod
    def partial_trace_residual_loss_ledger(rho_ab: np.ndarray) -> Dict[str, Any]:
        """Partial-trace residual loss ledger recording loss of bipartite correlations."""
        harness = Level3ResidualComposition.local_tomography_test_harness(rho_ab)
        trace_loss = abs(float(np.trace(rho_ab).real) - 1.0)

        return {
            "trace_loss": trace_loss,
            "correlation_residual_loss": harness["residual_defect"],
            "tomography_status": harness["contract_status"],
            "loss_ledger_recorded": True
        }



