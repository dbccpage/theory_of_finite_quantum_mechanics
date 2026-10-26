"""Genesis Primitives Category 9: Pre-Topological Contact Spaces & Replacement Kernels.

Selected educational models related to 19L57G1 (lean4/Derivation/PrimitiveContact.lean, ContactKernel.lean).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

The common replacement kernel WitnessedDiff, discrete proximity/contact relations,
and pre-topological spaces without metric or continuum coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from .canonical import exact_equal, validate_typed_fields

X = TypeVar("X")
R = TypeVar("R")


@dataclass(frozen=True)
class WitnessedDiff(Generic[X, R]):
    """Common replacement kernel: a valued difference presentation with designated
    endpoints, a diagonal-zero law, and a refutation-grade non-zero witness."""

    delta: Callable[[X, X], R]
    zero: Callable[[R], bool]
    a: X
    b: X

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        return (
            self.delta == other.delta
            and self.zero == other.zero
            and exact_equal(self.a, other.a)
            and exact_equal(self.b, other.b)
        )

    def is_diag_zero(self, x: X) -> bool:
        """Diagonal-zero law: delta(x, x) is zero."""
        return self.zero(self.delta(x, x))

    def is_witness_nonzero(self) -> bool:
        """Designated witness is non-zero."""
        return not self.zero(self.delta(self.a, self.b))

    def kernel_apart(self, x: X, y: X) -> bool:
        """Induced apartness: non-zero difference value."""
        return not self.zero(self.delta(x, y))


def bool_kernel() -> WitnessedDiff[bool, bool]:
    """Canonical realization: the oriented two-element kernel on Bool."""

    def delta(x: bool, y: bool) -> bool:
        return (not x) and y  # marks ordered pair (False, True)

    def zero(v: bool) -> bool:
        return not v

    return WitnessedDiff(
        delta=delta,
        zero=zero,
        a=False,
        b=True,
    )


@dataclass(frozen=True)
class ContactKernel:
    """Finite matrix representation of a pre-topological proximity/contact relation."""

    size: int
    contacts: frozenset[tuple[frozenset[int], frozenset[int]]]

    def __post_init__(self) -> None:
        validate_typed_fields(self)
        if self.size < 0 or any(
            not 0 <= point < self.size
            for pair in self.contacts
            for subset in pair
            for point in subset
        ):
            raise ValueError("REFUSED_SHAPE: contact outside declared carrier")

    def touches(self, a: set[int] | frozenset[int], b: set[int] | frozenset[int]) -> bool:
        """Quasi-topological contact relation C(A, B)."""
        fa, fb = frozenset(a), frozenset(b)
        if not fa or not fb:
            return False
        # Overlapping sets always touch
        if fa & fb:
            return True
        return (fa, fb) in self.contacts or (fb, fa) in self.contacts

    def separated(self, a: set[int] | frozenset[int], b: set[int] | frozenset[int]) -> bool:
        """Proximity separation: ¬ C(A, B)."""
        return not self.touches(a, b)
