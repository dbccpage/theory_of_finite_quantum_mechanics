from __future__ import annotations
"""Carrier: a weighted cochain complex C^0 -> C^1 -> C^2 with positive weights.

Port of ``carrier.rs``. Computes the homological invariants the Omega tower
relies on:

    rank_d0, rank_d1
    dim_q1 = c1_dim - rank_d0          (Q^1 = C^1 / im d0)
    dim_h1 = c1_dim - rank_d0 - rank_d1 (H^1 = ker d1 / im d0)
"""


from typing import List

from .errors import CoboundaryLawViolation, DimensionMismatch, NonPositiveWeight
from .ids import TheoremProvenance
from .qmatrix import QMatrix


class Carrier:
    def __init__(
        self,
        c0_dim: int,
        c1_dim: int,
        c2_dim: int,
        d0: QMatrix,
        d1: QMatrix,
        weights: List,
        provenance: TheoremProvenance,
    ):
        self._c0 = c0_dim
        self._c1 = c1_dim
        self._c2 = c2_dim
        self._d0 = d0
        self._d1 = d1
        self._weights = weights
        self._provenance = provenance

    @classmethod
    def new(
        cls,
        c0_dim: int,
        c1_dim: int,
        c2_dim: int,
        d0: QMatrix,
        d1: QMatrix,
        weights: List,
        provenance: TheoremProvenance,
    ) -> "Carrier":
        if d0.shape != (c1_dim, c0_dim):
            raise DimensionMismatch(f"d0 must be {c1_dim}x{c0_dim}, got {d0.shape}")
        if d1.shape != (c2_dim, c1_dim):
            raise DimensionMismatch(f"d1 must be {c2_dim}x{c1_dim}, got {d1.shape}")
        if len(weights) != c1_dim:
            raise DimensionMismatch(
                f"weights must have length {c1_dim}, got {len(weights)}"
            )
        for w in weights:
            if w <= 0:
                raise NonPositiveWeight(f"weight {w} is not strictly positive")
        if c2_dim > 0 and not d1.matmul(d0).is_zero():
            raise CoboundaryLawViolation("d1 . d0 != 0")
        return cls(c0_dim, c1_dim, c2_dim, d0, d1, list(weights), provenance)

    def c0_dim(self) -> int:
        return self._c0

    def c1_dim(self) -> int:
        return self._c1

    def c2_dim(self) -> int:
        return self._c2

    def d0(self) -> QMatrix:
        return self._d0

    def d1(self) -> QMatrix:
        return self._d1

    def weights(self) -> List:
        return self._weights

    def provenance(self) -> TheoremProvenance:
        return self._provenance

    def rank_d0(self) -> int:
        return self._d0.rank()

    def rank_d1(self) -> int:
        return self._d1.rank()

    def dim_q1(self) -> int:
        return self._c1 - self.rank_d0()

    def dim_h1(self) -> int:
        return self._c1 - self.rank_d0() - self.rank_d1()


from typing import Any  


class _RustSurfaceMeta(type):
    def __getattr__(cls, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {cls.__name__}.{name} is not ported"
            )

        return unavailable


class _RustSurfaceObject(metaclass=_RustSurfaceMeta):
    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {type(self).__name__}.{name} is not ported"
            )

        return unavailable


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::new"
    )


def c0_dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``c0_dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::c0_dim"
    )


def c1_dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``c1_dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::c1_dim"
    )


def c2_dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``c2_dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::c2_dim"
    )


def d0(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``d0``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::d0"
    )


def d1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``d1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::d1"
    )


def weights(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``weights``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::weights"
    )


def complex(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``complex``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::complex"
    )


def rank_d0(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``rank_d0``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::rank_d0"
    )


def rank_d1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``rank_d1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::rank_d1"
    )


def dim_q1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dim_q1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::dim_q1"
    )


def dim_h1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dim_h1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::dim_h1"
    )


def manifest(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``manifest``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier.rs::manifest"
    )



