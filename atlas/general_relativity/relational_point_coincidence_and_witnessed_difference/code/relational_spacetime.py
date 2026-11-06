"""Relational Spacetime and Dressing Field Exact Rational Engine.

Implements relational spacetime event schemas, candidate key point-coincidence
verification, Heath's theorem lossless join decomposition, dressing field
projections, and exact rational cochain dual witness certification.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Dict, FrozenSet, List, Optional, Set, Tuple


@dataclass
class EventTuple:
    """A single witnessed physical event tuple in a relational spacetime schema."""
    data: Dict[str, Any]

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.data.items())))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EventTuple):
            return False
        return self.data == other.data

    def project(self, attributes: FrozenSet[str]) -> EventTuple:
        return EventTuple({k: self.data[k] for k in attributes if k in self.data})

    def get(self, attr: str) -> Any:
        return self.data.get(attr)


class SpacetimeRelation:
    """A finite relation of physical spacetime events r(U)."""

    def __init__(self, attributes: Set[str], tuples: Optional[List[EventTuple]] = None) -> None:
        self.attributes: FrozenSet[str] = frozenset(attributes)
        self.tuples: List[EventTuple] = []
        if tuples:
            for t in tuples:
                self.add_tuple(t)

    def add_tuple(self, t: EventTuple) -> None:
        if not frozenset(t.data.keys()).issubset(self.attributes):
            missing = frozenset(t.data.keys()) - self.attributes
            raise ValueError(f"Tuple contains undeclared attributes: {missing}")
        if t not in self.tuples:
            self.tuples.append(t)

    def project(self, attributes: Set[str]) -> SpacetimeRelation:
        """Relational projection pi_X(r)."""
        attrs = frozenset(attributes) & self.attributes
        projected_tuples = [t.project(attrs) for t in self.tuples]
        return SpacetimeRelation(set(attrs), projected_tuples)

    def natural_join(self, other: SpacetimeRelation) -> SpacetimeRelation:
        """Natural join r1 bowtie r2."""
        common_attrs = self.attributes & other.attributes
        joined_attrs = set(self.attributes | other.attributes)
        joined_tuples: List[EventTuple] = []

        for t1 in self.tuples:
            for t2 in other.tuples:
                # Check agreement on common attributes
                agrees = all(t1.get(a) == t2.get(a) for a in common_attrs)
                if agrees:
                    merged = dict(t1.data)
                    merged.update(t2.data)
                    jt = EventTuple(merged)
                    if jt not in joined_tuples:
                        joined_tuples.append(jt)

        return SpacetimeRelation(joined_attrs, joined_tuples)

    def check_functional_dependency(self, lhs: Set[str], rhs: Set[str]) -> bool:
        """Check whether functional dependency LHS -> RHS holds in this relation."""
        lhs_frozen = frozenset(lhs)
        rhs_frozen = frozenset(rhs)

        seen: Dict[Tuple[Any, ...], Tuple[Any, ...]] = {}
        for t in self.tuples:
            lhs_vals = tuple(t.get(a) for a in sorted(lhs_frozen))
            rhs_vals = tuple(t.get(a) for a in sorted(rhs_frozen))
            if lhs_vals in seen:
                if seen[lhs_vals] != rhs_vals:
                    return False
            else:
                seen[lhs_vals] = rhs_vals
        return True

    def is_superkey(self, candidate_key: Set[str]) -> bool:
        """Check if candidate_key functionally determines all attributes in U."""
        return self.check_functional_dependency(candidate_key, set(self.attributes))

    def verify_heaths_theorem(self, key: Set[str], attr_set_a: Set[str], attr_set_b: Set[str]) -> bool:
        """Verify Heath's Theorem: r = pi_{K union A}(r) bowtie pi_{K union B}(r) when K -> A."""
        if not self.check_functional_dependency(key, attr_set_a):
            return False

        proj_a = self.project(key | attr_set_a)
        proj_b = self.project(key | attr_set_b)
        reconstructed = proj_a.natural_join(proj_b)

        # Check tuple equality
        s1 = set(self.tuples)
        s2 = set(reconstructed.tuples)
        return s1 == s2 and self.attributes == reconstructed.attributes

    def check_rpcnf(self, candidate_key: Set[str], forbidden_coordinates: Set[str]) -> Dict[str, Any]:
        """Check Relational Point Coincidence Normal Form (RPCNF) compliance."""
        violations = []

        # 1. Coordinate check
        coords_present = self.attributes & forbidden_coordinates
        if coords_present:
            violations.append(f"Forbidden coordinate attributes present: {coords_present}")

        # 2. Key size check (exactly 4 scalar fields for 4D spacetime)
        if len(candidate_key) != 4:
            violations.append(f"Candidate key size {len(candidate_key)} != 4")

        # 3. Superkey check
        if not self.is_superkey(candidate_key):
            violations.append(f"Declared key {candidate_key} does not functionally determine all attributes")

        return {
            "is_rpcnf": len(violations) == 0,
            "violations": violations,
            "candidate_key": sorted(candidate_key),
            "attribute_count": len(self.attributes),
            "tuple_count": len(self.tuples),
        }


class DressingFieldProjection:
    """Implements Dressing Field Method (DFM) retraction on field configurations."""

    def __init__(
        self,
        gauge_action: Callable[[Any, Any], Any],
        dressing_field: Callable[[Any], Any],
    ) -> None:
        self.gauge_action = gauge_action
        self.dressing_field = dressing_field

    def dress(self, field_state: Any) -> Any:
        """Apply dressing projection: phi^u = rho(u(phi)) phi."""
        u = self.dressing_field(field_state)
        return self.gauge_action(u, field_state)

    def verify_idempotence(self, field_state: Any) -> bool:
        """Verify Pi^2 = Pi."""
        dressed_1 = self.dress(field_state)
        dressed_2 = self.dress(dressed_1)
        return dressed_1 == dressed_2

    def verify_gauge_invariance(self, field_state: Any, gauge_element: Any) -> bool:
        """Verify Pi(phi^g) == Pi(phi)."""
        transformed_state = self.gauge_action(gauge_element, field_state)
        dressed_original = self.dress(field_state)
        dressed_transformed = self.dress(transformed_state)
        return dressed_original == dressed_transformed


class ExactRationalDualWitness:
    """Exact rational LP dual witness verifier for cochain obstruction over Q."""

    @staticmethod
    def inner_product(u: List[Fraction], v: List[Fraction]) -> Fraction:
        return sum(a * b for a, b in zip(u, v))

    @staticmethod
    def matrix_vector_mult(mat: List[List[Fraction]], vec: List[Fraction]) -> List[Fraction]:
        return [sum(row[j] * vec[j] for j in range(len(vec))) for row in mat]

    @staticmethod
    def matrix_transpose_vector_mult(mat: List[List[Fraction]], vec: List[Fraction]) -> List[Fraction]:
        num_cols = len(mat[0]) if mat else 0
        res = []
        for c in range(num_cols):
            res.append(sum(mat[r][c] * vec[r] for r in range(len(mat))))
        return res

    @classmethod
    def verify_dual_witness(
        cls,
        D: List[List[Fraction]],
        omega: List[Fraction],
        w: List[Fraction],
        claimed_quotient: Fraction,
    ) -> Dict[str, Any]:
        """Verify that w in Q^m is a valid dual witness certifying Phi_D([omega]) >= claimed_quotient."""
        m = len(omega)
        k = len(D[0]) if D else 0

        # 1. Check dimension
        if len(w) != m or len(D) != m:
            return {"valid": False, "reason": "Dimension mismatch between D, omega, and w"}

        # 2. Check divergence-free: D^T w = 0
        dt_w = cls.matrix_transpose_vector_mult(D, w)
        is_divergence_free = all(val == Fraction(0) for val in dt_w)
        if not is_divergence_free:
            return {
                "valid": False,
                "reason": f"Dual witness is not divergence-free: D^T w = {dt_w}",
                "dt_w": dt_w,
            }

        # 3. Check infinity norm bound: ||w||_infty <= 1
        inf_norm = max(abs(val) for val in w)
        if inf_norm > Fraction(1):
            return {
                "valid": False,
                "reason": f"Dual witness violates ||w||_infty <= 1: {inf_norm} > 1",
                "inf_norm": inf_norm,
            }

        # 4. Check duality pairing: <w, omega>
        dual_val = cls.inner_product(w, omega)
        if dual_val < claimed_quotient:
            return {
                "valid": False,
                "reason": f"Dual pairing <w, omega> = {dual_val} < claimed quotient {claimed_quotient}",
            }

        return {
            "valid": True,
            "dual_value": dual_val,
            "is_divergence_free": True,
            "inf_norm": inf_norm,
            "certified_lower_bound": dual_val,
        }
