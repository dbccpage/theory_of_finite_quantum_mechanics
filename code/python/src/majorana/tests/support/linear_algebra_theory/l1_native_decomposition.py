from __future__ import annotations
from typing import Dict
from omega_engine.crates.solver.solv_cohomological_l1_norm import CohomologicalNorm
from omega_engine.crates.solver.solv_cut_duality import CutDuality
from omega_engine.crates.homology_theory.discrete_derham import DiscreteDeRham
import numpy as np

class L1NativeDecomposition:
    def __init__(self, graph: DiscreteDeRham):
        self.graph = graph
        self.primal = CohomologicalNorm(graph)
        self.dual = CutDuality(graph)

    def decompose(self, delta: np.ndarray) -> Dict:
        primal = self.primal.compute_phi(delta)
        dual = self.dual.solve_dual(delta)

        f_star = primal["f_star"]
        r_star = primal["r_star"]
        phi_star = dual["phi_star"]

        delta_exact = self.graph.d0(f_star)
        primal_val = primal["Phi"]
        dual_val = dual["dual_value"]

        saturation_lhs = float(np.dot(phi_star, r_star))
        saturation_rhs = float(np.sum(np.abs(r_star)))

        return {
            "f_star": f_star,
            "delta_exact": delta_exact,
            "delta_irr": r_star,
            "phi_star": phi_star,
            "Phi": primal_val,
            "duality_gap": abs(primal_val - dual_val),
            "reconstruction_error": float(
                np.linalg.norm(delta - (delta_exact + r_star))
            ),
            "saturation_gap": abs(saturation_lhs - saturation_rhs),
            "primal_objective": primal_val,
            "dual_objective": dual_val,
        }



