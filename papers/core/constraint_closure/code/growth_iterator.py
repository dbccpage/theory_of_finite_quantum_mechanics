import numpy as np
from scipy.optimize import linprog
from dataclasses import dataclass
from typing import Tuple, List

try:
    from lib.poset import Poset, Extension
except ImportError:
    from poset import Poset, Extension

@dataclass
class IteratorResult:
    """Result of one iterator step."""
    final_poset: Poset
    final_section: np.ndarray
    l1_norm_history: List[float]
    augmentations: List[Extension]
    converged: bool
    steps: int

class CellGrowthIterator:
    """
    Cell Growth Iterator solving the Discrete L1 Optimization Constraint
    using a linear programming selection algorithm for extension candidates.

    Note: Midpoint subdivision preserves total variation along an edge since
    |m - a| + |b - m| = |b - a| for m = (a + b)/2. Therefore, subdivision alone
    does not guarantee strict L1 descent; it preserves total variation until combined
    with section updates.
    """

    def __init__(self, tolerance: float = 1e-6, max_steps: int = 1000):
        self.tolerance = tolerance
        self.max_steps = max_steps

    def _build_lp(self, poset: Poset, admissible: List[Extension], defect: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Formulate extension selection as a linear program solving:
        Λ* = argmin_{Λ ∈ A} I_{P U Λ}(s).
        Minimizes topological extension cost subject to candidate boundary activation.
        (No formal Wasserstein transport correspondence is claimed.)
        """
        num_ext = len(admissible)
        c = np.ones(num_ext)

        num_edges = len(poset.edges)
        A_eq = np.zeros((num_edges, num_ext))
        b_eq = np.abs(defect)

        for idx, ext in enumerate(admissible):
            if ext.type == "subdivide":
                e_idx = poset.edges.index(ext.source_edge)
                A_eq[e_idx, idx] = b_eq[e_idx]
                c[idx] = ext.cost

        return c, A_eq, b_eq

    def step(self, poset: Poset, section: np.ndarray) -> Tuple[Poset, np.ndarray, float, List[Extension]]:
        """
        Execute one minimal iterator step computing the optimal structure to heal tension.
        Returns:
            (augmented_poset, new_section, new_l1_norm, applied_extensions)
        """
        delta_s = poset.coboundary(section)
        l1_norm = float(np.sum(np.abs(delta_s)))

        if l1_norm < self.tolerance:
            return poset, section, l1_norm, []

        admissible = poset.get_admissible_extensions(delta_s, self.tolerance)
        if not admissible:
            return poset, section, l1_norm, []

        c, A_eq, b_eq = self._build_lp(poset, admissible, delta_s)
        num_ext = len(c)
        bounds = [(0, 1) for _ in range(num_ext)]

        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if result.success:
            Lambda_star = [ext for i, ext in enumerate(admissible) if result.x[i] > 1e-3]
        else:
            Lambda_star = admissible

        if not Lambda_star:
            return poset, section, l1_norm, []

        poset_new = poset.add_extensions(Lambda_star)

        new_section = np.zeros(poset_new.num_vertices)
        new_section[:poset.num_vertices] = section

        w = poset.num_vertices
        for ext in Lambda_star:
            if ext.type == "subdivide":
                u, v = ext.source_edge
                new_section[w] = (section[u] + section[v]) / 2.0
                w += len(ext.new_vertices)

        delta_s_new = poset_new.coboundary(new_section)
        l1_norm_new = float(np.sum(np.abs(delta_s_new)))

        return poset_new, new_section, l1_norm_new, Lambda_star

    def iterate(self, poset_0: Poset, section_0: np.ndarray) -> IteratorResult:
        """
        Run to topological equilibrium (convergence).
        """
        poset = poset_0
        section = section_0
        l1_history = []
        all_augmentations = []

        for step in range(self.max_steps):
            delta_s = poset.coboundary(section)
            current_norm = float(np.sum(np.abs(delta_s)))
            l1_history.append(current_norm)

            if current_norm < self.tolerance:
                return IteratorResult(
                    final_poset=poset,
                    final_section=section,
                    l1_norm_history=l1_history,
                    augmentations=all_augmentations,
                    converged=True,
                    steps=step
                )

            poset, section, new_norm, aux = self.step(poset, section)
            all_augmentations.extend(aux)

            if not aux or poset.num_vertices >= 200 or (step > 0 and abs(new_norm - current_norm) < self.tolerance):
                break

        final_norm = float(np.sum(np.abs(poset.coboundary(section))))
        l1_history.append(final_norm)

        return IteratorResult(
            final_poset=poset,
            final_section=section,
            l1_norm_history=l1_history,
            augmentations=all_augmentations,
            converged=(final_norm < self.tolerance),
            steps=self.max_steps
        )

AutopoeticIterator = CellGrowthIterator
