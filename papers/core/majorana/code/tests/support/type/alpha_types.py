"""Paper Alpha base types.

Alpha scalar-presheaf prototype: diagnostic only, NOT core and NOT authority.
These scalar (float-valued) constructions duplicate, in simplified form, the
finite-dimensional numpy machinery in `banach_presheaf_types`; prefer that
module for non-prototype use. Nothing here terminalizes or enforces anything.
"""

from typing import Dict, List, Optional, Set, Tuple

from .finite_poset import FinitePoset  # noqa: E402



class EvaluationMap:
    """Finite dense scalar evaluation table over a labeled set."""

    def __init__(self, elements: List[str], matrix: List[List[float]]):
        n = len(elements)
        if not n > 0:
            raise ValueError("Elements must be non-empty")
        if not len(matrix) == n:
            raise ValueError("Matrix row count must match elements")
        if not all(len(row) == n for row in matrix):
            raise ValueError("Matrix must be square")
        self.elements = elements
        self.matrix = matrix
        self.n = n

    def diagonal(self) -> List[float]:
        return [self.matrix[i][i] for i in range(self.n)]

    def row(self, i: int) -> List[float]:
        return self.matrix[i]


class LocalObservationAct:
    """Finite scoped observation carrying scalar verdicts on some elements."""

    def __init__(self, label: str, scope: Set[str], verdicts: Dict[str, float]):
        if not scope:
            raise ValueError("Scope must be non-empty")
        if not set(verdicts.keys()) <= scope:
            raise ValueError("Verdicts must be within scope")
        self.label = label
        self.scope = scope
        self.verdicts = verdicts


class ObservationPoset:
    """Finite dependency DAG over observation labels.

    An edge (a, b) means a precedes / constrains b.
    """

    def __init__(
        self,
        acts: List[LocalObservationAct],
        dep_edges: List[Tuple[str, str]],
    ):
        self.labels = [a.label for a in acts]
        self.acts = {a.label: a for a in acts}
        self.poset = FinitePoset(self.labels, dep_edges)

    def is_well_founded(self) -> bool:
        return self._topo_sort() is not None

    def _topo_sort(self) -> Optional[List[str]]:
        in_deg = {n: 0 for n in self.labels}
        for _, b in self.poset.edges:
            in_deg[b] = in_deg.get(b, 0) + 1
        queue = [n for n in self.labels if in_deg[n] == 0]
        order: List[str] = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for nb in self.poset.successors(node):
                in_deg[nb] -= 1
                if in_deg[nb] == 0:
                    queue.append(nb)
        return order if len(order) == len(self.labels) else None


class RestrictionMap:
    """Scalar multiplier used as a prototype restriction map."""

    def __init__(self, source: str, target: str, multiplier: float):
        self.source = source
        self.target = target
        self.mult = multiplier

    def apply(self, value: float) -> float:
        return self.mult * value

    @staticmethod
    def verify_composition(
        ab: "RestrictionMap", bc: "RestrictionMap", ac: "RestrictionMap"
    ) -> Tuple[bool, float]:
        err = abs(ab.mult * bc.mult - ac.mult)
        return (err < 1e-10, err)


class BanachPresheaf:
    """Finite scalar presheaf prototype over a dependency poset."""

    def __init__(
        self,
        poset: FinitePoset,
        restrictions: Dict[Tuple[str, str], RestrictionMap],
    ):
        self.poset = poset
        self.restrictions = restrictions

    def coboundary(self, section: Dict[str, float]) -> Dict[Tuple[str, str], float]:
        delta: Dict[Tuple[str, str], float] = {}
        for a, b in self.poset.edges:
            s_a = section.get(a, 0.0)
            s_b = section.get(b, 0.0)
            rho = self.restrictions.get((a, b))
            delta[(a, b)] = s_b - (rho.apply(s_a) if rho else s_a)
        return delta

    def verify_functoriality(self) -> Tuple[bool, List[str]]:
        violations: List[str] = []
        for a in self.poset.nodes:
            for b in self.poset.successors(a):
                for c in self.poset.successors(b):
                    ab = self.restrictions.get((a, b))
                    bc = self.restrictions.get((b, c))
                    ac = self.restrictions.get((a, c))
                    if ab and bc and ac:
                        ok, err = RestrictionMap.verify_composition(ab, bc, ac)
                        if not ok:
                            violations.append(
                                f"rho({a},{b}) o rho({b},{c}) != rho({a},{c}), err={err:.2e}"
                            )
        return (len(violations) == 0, violations)
