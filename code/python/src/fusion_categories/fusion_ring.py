"""Fusion rings: the based ring K_0 of a fusion category as a table of
non-negative integer structure constants N_{ab}^c.

A FusionTable is a declared table checked for shape only, and
FusionTable.first_defect reports the first failure of the ring laws.
A FusionRing is a table that has passed the ring laws.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional, Sequence, Dict
from enum import Enum


MAX_RANK: int = 32
MAX_FUSION_WORD: int = 1 << 14


class RingDefectType(Enum):
    UNIT = "unit"
    COMMUTATIVITY = "commutativity"
    ASSOCIATIVITY = "associativity"
    DUALITY = "duality"
    RECIPROCITY = "reciprocity"
    OVERFLOW = "overflow"


@dataclass(frozen=True)
class RingDefect:
    defect_type: RingDefectType
    message: str
    labels: Optional[Tuple[int, ...]] = None


class AbelianGroup:
    """A finite abelian group Z_{m_1} x ... x Z_{m_r} with labels in mixed radix."""

    def __init__(self, moduli: Sequence[int]) -> None:
        if not moduli:
            raise ValueError("Moduli cannot be empty")
        order = 1
        for m in moduli:
            if m < 2:
                raise ValueError(f"Modulus {m} must be at least 2")
            order *= m
            if order > MAX_RANK:
                raise ValueError(f"Order {order} exceeds MAX_RANK {MAX_RANK}")
        self._moduli = list(moduli)
        self._order = order

    @property
    def moduli(self) -> List[int]:
        return list(self._moduli)

    @property
    def order(self) -> int:
        return self._order

    def digits(self, label: int) -> List[int]:
        if not (0 <= label < self._order):
            raise ValueError(f"Label {label} out of range for order {self._order}")
        res = []
        rest = label
        for m in self._moduli:
            res.append(rest % m)
            rest //= m
        return res

    def label(self, digits: Sequence[int]) -> int:
        if len(digits) != len(self._moduli):
            raise ValueError(f"Expected {len(self._moduli)} digits, got {len(digits)}")
        lbl = 0
        stride = 1
        for d, m in zip(digits, self._moduli):
            if not (0 <= d < m):
                raise ValueError(f"Digit {d} out of range for modulus {m}")
            lbl += d * stride
            stride *= m
        return lbl

    def add(self, a: int, b: int) -> int:
        da = self.digits(a)
        db = self.digits(b)
        s = [(x + y) % m for x, y, m in zip(da, db, self._moduli)]
        return self.label(s)

    def negate(self, a: int) -> int:
        da = self.digits(a)
        neg = [(m - x) % m for x, m in zip(da, self._moduli)]
        return self.label(neg)


class FusionTable:
    """A declared fusion table of rank r: N_{ab}^c for labels 0..r-1."""

    def __init__(
        self,
        rank: int,
        multiplicities: Sequence[int],
        names: Optional[Sequence[str]] = None,
    ) -> None:
        if rank <= 0 or rank > MAX_RANK:
            raise ValueError(f"Rank {rank} must be between 1 and {MAX_RANK}")
        expected = rank * rank * rank
        if len(multiplicities) != expected:
            raise ValueError(f"Expected {expected} multiplicities, got {len(multiplicities)}")
        if any(m < 0 for m in multiplicities):
            raise ValueError("Fusion multiplicities must be non-negative")
        self._rank = rank
        self._n = list(multiplicities)
        if names is not None:
            if len(names) != rank:
                raise ValueError(f"Expected {rank} names, got {len(names)}")
            self._names = list(names)
        else:
            self._names = [str(i) for i in range(rank)]

    @classmethod
    def from_3d(
        cls,
        tensor: Sequence[Sequence[Sequence[int]]],
        names: Optional[Sequence[str]] = None,
    ) -> FusionTable:
        rank = len(tensor)
        flat = []
        for plane in tensor:
            if len(plane) != rank:
                raise ValueError("Inconsistent tensor dimensions")
            for row in plane:
                if len(row) != rank:
                    raise ValueError("Inconsistent tensor dimensions")
                flat.extend(row)
        return cls(rank, flat, names)

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def names(self) -> List[str]:
        return list(self._names)

    def n(self, a: int, b: int, c: int) -> int:
        if not (0 <= a < self._rank and 0 <= b < self._rank and 0 <= c < self._rank):
            raise IndexError("Label out of bounds")
        return self._n[(a * self._rank + b) * self._rank + c]

    def _check_unit_defect(self) -> Optional[RingDefect]:
        r = self._rank
        for a in range(r):
            for c in range(r):
                expected = 1 if c == a else 0
                if self.n(0, a, c) != expected or self.n(a, 0, c) != expected:
                    return RingDefect(
                        RingDefectType.UNIT,
                        f"Unit law fails on label {a}",
                        (a,)
                    )
        return None

    def _check_commutativity_defect(self) -> Optional[RingDefect]:
        r = self._rank
        for a in range(r):
            for b in range(a + 1, r):
                for c in range(r):
                    if self.n(a, b, c) != self.n(b, a, c):
                        return RingDefect(
                            RingDefectType.COMMUTATIVITY,
                            f"Labels {a} and {b} do not commute",
                            (a, b)
                        )
        return None

    def _check_associativity_defect(self) -> Optional[RingDefect]:
        r = self._rank
        for a in range(r):
            for b in range(r):
                for c in range(r):
                    for d in range(r):
                        left = sum(self.n(a, b, x) * self.n(x, c, d) for x in range(r))
                        right = sum(self.n(b, c, y) * self.n(a, y, d) for y in range(r))
                        if left != right:
                            return RingDefect(
                                RingDefectType.ASSOCIATIVITY,
                                f"Associativity fails on ({a}, {b}, {c}) for outcome {d}",
                                (a, b, c, d)
                            )
        return None

    def _check_duality_defect(self) -> Tuple[Optional[RingDefect], Dict[int, int]]:
        r = self._rank
        duals: Dict[int, int] = {}
        for a in range(r):
            dual_candidates = [b for b in range(r) if self.n(a, b, 0) == 1]
            if len(dual_candidates) != 1:
                return (RingDefect(
                    RingDefectType.DUALITY,
                    f"Label {a} does not have a unique dual",
                    (a,)
                ), {})
            b = dual_candidates[0]
            if sum(self.n(a, x, 0) for x in range(r)) != 1:
                return (RingDefect(
                    RingDefectType.DUALITY,
                    f"Label {a} has non-unique unit occurrence",
                    (a,)
                ), {})
            duals[a] = b

        for a, b in duals.items():
            if duals.get(b) != a:
                return (RingDefect(
                    RingDefectType.DUALITY,
                    f"Duality is not an involution: dual({a}) = {b}, dual({b}) = {duals.get(b)}",
                    (a,)
                ), {})
        return (None, duals)

    def _check_reciprocity_defect(self, duals: Dict[int, int]) -> Optional[RingDefect]:
        r = self._rank
        for a in range(r):
            a_star = duals[a]
            for b in range(r):
                b_star = duals[b]
                for c in range(r):
                    val = self.n(a, b, c)
                    if self.n(a_star, c, b) != val or self.n(c, b_star, a) != val:
                        return RingDefect(
                            RingDefectType.RECIPROCITY,
                            f"Frobenius reciprocity fails on ({a}, {b}, {c})",
                            (a, b, c)
                        )
        return None

    def first_defect(self) -> Optional[RingDefect]:
        defect = self._check_unit_defect()
        if defect is not None:
            return defect
        defect = self._check_commutativity_defect()
        if defect is not None:
            return defect
        defect = self._check_associativity_defect()
        if defect is not None:
            return defect
        defect, duals = self._check_duality_defect()
        if defect is not None:
            return defect
        return self._check_reciprocity_defect(duals)


class FusionRing:
    """A validated based fusion ring K_0."""

    def __init__(self, table: FusionTable) -> None:
        defect = table.first_defect()
        if defect is not None:
            raise ValueError(f"Invalid fusion table: {defect.message}")
        self._table = table
        self._rank = table.rank
        self._duals = [
            next(b for b in range(self._rank) if table.n(a, b, 0) == 1)
            for a in range(self._rank)
        ]

    @property
    def table(self) -> FusionTable:
        return self._table

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def names(self) -> List[str]:
        return self._table.names

    def n(self, a: int, b: int, c: int) -> int:
        return self._table.n(a, b, c)

    def dual(self, a: int) -> int:
        return self._duals[a]

    def fusion_matrix(self, a: int) -> List[List[int]]:
        r = self._rank
        return [[self.n(a, b, c) for c in range(r)] for b in range(r)]

    def fusion_path_count(self, start: int, word: Sequence[int], target: int) -> int:
        if len(word) > MAX_FUSION_WORD:
            raise ValueError(f"Word length {len(word)} exceeds MAX_FUSION_WORD {MAX_FUSION_WORD}")
        r = self._rank
        v = [0] * r
        v[start] = 1
        for factor in word:
            next_v = [0] * r
            for b in range(r):
                if v[b] == 0:
                    continue
                for c in range(r):
                    mult = self.n(factor, b, c)
                    if mult > 0:
                        next_v[c] += v[b] * mult
            v = next_v
        return v[target]

    @staticmethod
    def _power_iteration(matrix: List[List[int]], r: int) -> float:
        v = [1.0] * r
        for _ in range(150):
            next_v = [sum(matrix[i][j] * v[j] for j in range(r)) for i in range(r)]
            norm = math.sqrt(sum(x * x for x in next_v))
            if norm == 0:
                return 0.0
            v = [x / norm for x in next_v]
        return sum(v[i] * sum(matrix[i][j] * v[j] for j in range(r)) for i in range(r))

    def frobenius_perron_dimension(self, a: int) -> float:
        """Computes the Frobenius-Perron dimension d_a as the spectral radius of N_a.
        Uses a shifted power iteration (N_a + I) to guarantee Perron-Frobenius convergence."""
        r = self._rank
        if r == 1:
            return 1.0
        mat = self.fusion_matrix(a)
        m = [[mat[i][j] + (1 if i == j else 0) for j in range(r)] for i in range(r)]
        rayleigh_m = self._power_iteration(m, r)
        return max(0.0, rayleigh_m - 1.0)

    def global_dimension_squared(self) -> float:
        return sum(self.frobenius_perron_dimension(a) ** 2 for a in range(self._rank))

    @classmethod
    def ising(cls) -> FusionRing:
        table_arr = [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
            [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
        ]
        table = FusionTable.from_3d(table_arr, ["1", "sigma", "psi"])
        return cls(table)

    @classmethod
    def fibonacci(cls) -> FusionRing:
        table_arr = [
            [[1, 0], [0, 1]],
            [[0, 1], [1, 1]],
        ]
        table = FusionTable.from_3d(table_arr, ["1", "tau"])
        return cls(table)

    @classmethod
    def toric_code(cls) -> FusionRing:
        grp = AbelianGroup([2, 2])
        r = 4
        table_arr = [[[0] * r for _ in range(r)] for _ in range(r)]
        for a in range(r):
            for b in range(r):
                c = grp.add(a, b)
                table_arr[a][b][c] = 1
        table = FusionTable.from_3d(table_arr, ["1", "e", "m", "epsilon"])
        return cls(table)

    @classmethod
    def rep_s3(cls) -> FusionRing:
        table_arr = [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
            [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
        ]
        table = FusionTable.from_3d(table_arr, ["1", "s", "v"])
        return cls(table)
