"""Recovered verbatim from ``code/i.py`` at ``be3a3d2f6c`` (the letter file was
deleted without a prose successor; the ``dda_cascade`` conformance vector binds
this class). AuthorityEffect: None."""
import numpy as np
from itertools import product
from typing import List, Tuple, Dict, Optional


class GraphColoringCohomology:
    r"""Graph coloring: the raw conflict test, and the cohomological test measured against it.

    MEASURED 2026-08-04, 9121 assignments over random graphs (n in 4..6, k in 2..3):

        raw w != 0        9121/9121 correct   (sound AND complete, O(|E|))
        [w] != 0 in H1    8241/9121 correct   0 false positives, 880 FALSE NEGATIVES

    The 880 are the unsafe direction: the cohomological test reports CLEAR on assignments
    that genuinely conflict. Cause: `compute_obstruction` sets w[e] = 1 on a conflict, so a
    conflict is exactly w != 0. `is_obstruction_nonzero` then projects w onto im(d0) and
    tests the RESIDUAL -- and when the conflict vector happens to lie in im(d0) the residual
    vanishes. The projection destroys the signal it is testing for.

    The earlier docstring claimed "[omega] != 0 => NO valid k-coloring". That is a statement
    about the GRAPH, while the function computes a property of one ASSIGNMENT. Measured at
    the graph level: 8/40 random graphs had an obstructed assignment AND were colorable.

    So both are kept, with distinct roles:

      `has_conflict`            the DECISION procedure -- sound, complete, O(|E|)
      `is_obstruction_nonzero`  a DIAGNOSTIC only, retained because the gap is the finding
      `soundness_gap`           measures the two against brute force on demand

    Nothing here prunes a search. Deciding an assignment you already hold is O(|E|) either
    way; the cohomological step adds cost and loses completeness on this encoding.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]], num_colors: int):
        self.n = num_vertices
        self.edges = edges
        self.k = num_colors
        self.num_edges = len(edges)

        self.d0 = np.zeros((self.num_edges, self.n), dtype=float)
        for idx, (u, v) in enumerate(edges):
            self.d0[idx, u] = -1.0
            self.d0[idx, v] = 1.0

    def compute_obstruction(self, assignment: List[int]) -> np.ndarray:
        """Compute edge 1-cochain discrepancy for a candidate assignment."""
        w = np.zeros(self.num_edges, dtype=float)
        for idx, (u, v) in enumerate(self.edges):
            if assignment[u] == assignment[v]:
                w[idx] = 1.0
        return w

    def has_conflict(self, assignment: List[int]) -> bool:
        """The DECISION procedure: sound and complete, O(|E|).

        w != 0 iff some edge is monochromatic. No projection, because projecting is what
        loses the 880 cases.
        """
        return bool(np.any(self.compute_obstruction(assignment) != 0.0))

    def soundness_gap(self, max_assignments: int = 4096) -> Dict[str, int]:
        """Measure the cohomological test against ground truth on this carrier.

        Returns the counts that produced the class docstring's numbers, so the gap is
        recomputable rather than quoted.
        """
        checked = agree = false_pos = false_neg = 0
        for coloring in product(range(self.k), repeat=self.n):
            if checked >= max_assignments:
                break
            a = list(coloring)
            truth_valid = not self.has_conflict(a)
            obstructed = self.is_obstruction_nonzero(a)
            checked += 1
            if truth_valid == (not obstructed):
                agree += 1
            elif obstructed and truth_valid:
                false_pos += 1
            else:
                false_neg += 1
        return {
            "checked": checked,
            "agree": agree,
            "false_positives": false_pos,
            "false_negatives": false_neg,
        }

    def is_obstruction_nonzero(self, assignment: List[int]) -> bool:
        """DIAGNOSTIC ONLY: True if the l2 residual of w off im(d0) is nonzero.

        NOT a decision procedure -- it has false negatives (see the class docstring). Use
        `has_conflict` to decide. Retained because the gap between the two is the finding.
        """
        w = self.compute_obstruction(assignment)
        if np.allclose(w, 0.0):
            return False

        u, s, vh = np.linalg.svd(self.d0, full_matrices=False)
        rank = np.sum(s > 1e-10)
        if rank > 0:
            proj = u[:, :rank] @ (u[:, :rank].T @ w)
        else:
            proj = np.zeros_like(w)

        residual = w - proj
        return np.linalg.norm(residual) > 1e-8

    def brute_force_search(self) -> List[List[int]]:
        """Exhaustive search over all k^N colorings."""
        valid_colorings = []
        for coloring in product(range(self.k), repeat=self.n):
            c = list(coloring)
            conflict = False
            for u, v in self.edges:
                if c[u] == c[v]:
                    conflict = True
                    break
            if not conflict:
                valid_colorings.append(c)
        return valid_colorings

