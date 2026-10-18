"""Paper Alpha Lawvere diagonal obstruction.

Finite boolean diagnostic over a simulated, finite mapping table. These
routines evaluate boolean/numeric diagnostics on an explicit finite
``EvaluationMap``; they do NOT constitute a categorical proof of the
Lawvere fixed-point / diagonal-impossibility theorem.
"""

from typing import List, Tuple

from omega_engine.crates.type.alpha_types import EvaluationMap, LocalObservationAct


class LawvereImpossibility:
    """Finite diagnostic: checks whether the diagonal d(x)=1-e(x,x) matches
    any row of a finite, simulated evaluation table ``e``.

    This is a finite boolean diagnostic over a fixed mapping table, not a
    categorical proof of the Lawvere diagonal-impossibility theorem. A
    passing check means surjectivity failed for this particular finite
    instance only.
    """

    @staticmethod
    def negation_diagonal(em: EvaluationMap) -> List[float]:
        return [1.0 - em.matrix[i][i] for i in range(em.n)]

    @staticmethod
    def check_surjectivity_failure(em: EvaluationMap) -> Tuple[bool, str]:
        d = LawvereImpossibility.negation_diagonal(em)
        for i in range(em.n):
            if all(abs(d[j] - em.row(i)[j]) < 1e-12 for j in range(em.n)):
                return (False, f"d matches row {i} - surjectivity holds")
        return (True, "d matches no row - surjectivity fails (Lawvere)")

    @staticmethod
    def shatter(em: EvaluationMap, partition_size: int) -> List[LocalObservationAct]:
        acts = []
        for start in range(0, em.n, partition_size):
            end = min(start + partition_size, em.n)
            scope = set(em.elements[start:end])
            indices = list(range(start, end))
            for row_idx in range(em.n):
                verdicts = {em.elements[c]: em.matrix[row_idx][c] for c in indices}
                acts.append(
                    LocalObservationAct(f"act_r{row_idx}_b{start}", scope, verdicts)
                )
        return acts

    @staticmethod
    def obstruction_vector(em: EvaluationMap) -> List[float]:
        return [abs(2 * em.matrix[i][i] - 1) for i in range(em.n)]



