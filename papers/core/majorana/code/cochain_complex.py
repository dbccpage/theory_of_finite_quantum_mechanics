from __future__ import annotations
"""Cochain complex C^0 --d0--> C^1 --d1--> C^2 with the coboundary law d1.d0 = 0.

Port of ``cochain_complex.rs``. Construction validates dimensions and the law,
so a successful ``CochainComplex.new`` is itself the proof that d1.d0 = 0.
"""


from .errors import CoboundaryLawViolation, DimensionMismatch, HomologicalError
from .ids import TheoremProvenance
from .qmatrix import QMatrix

try:
    from omega_engine.crates.type.refusal import Refusal, Result
except ImportError:
    try:
        from omega_engine.crates.type.refusal import Refusal, Result
    except ImportError:
        from omega_engine.crates.type.refusal import Refusal, Result

__all__ = ["CochainComplex", "TheoremProvenance", "create_cochain_complex"]


class CochainComplex:
    def __init__(
        self,
        c0_dim: int,
        c1_dim: int,
        c2_dim: int,
        d0: QMatrix,
        d1: QMatrix,
        provenance: TheoremProvenance | None = None,
    ):
        self.c0_dim = c0_dim
        self.c1_dim = c1_dim
        self.c2_dim = c2_dim
        self.d0 = d0
        self.d1 = d1
        self.provenance = provenance if provenance is not None else TheoremProvenance("default")


    @classmethod
    def new(
        cls,
        c0_dim: int,
        c1_dim: int,
        c2_dim: int,
        d0: QMatrix,
        d1: QMatrix,
        provenance: TheoremProvenance,
    ) -> "CochainComplex":
        if d0.shape != (c1_dim, c0_dim):
            raise DimensionMismatch(f"d0 must be {c1_dim}x{c0_dim}, got {d0.shape}")
        if d1.shape != (c2_dim, c1_dim):
            raise DimensionMismatch(f"d1 must be {c2_dim}x{c1_dim}, got {d1.shape}")
        if c2_dim > 0 and not d1.matmul(d0).is_zero():
            raise CoboundaryLawViolation("d1 . d0 != 0")
        return cls(c0_dim, c1_dim, c2_dim, d0, d1, provenance)


def create_cochain_complex(
    c0_dim: int,
    c1_dim: int,
    c2_dim: int,
    d0: QMatrix,
    d1: QMatrix,
    provenance: TheoremProvenance,
) -> Result["CochainComplex"]:
    """Replay-safe builder mirroring ``CochainComplex.new``.

    Unlike ``CochainComplex.new`` (which raises ``HomologicalError`` subclasses
    on dimension/coboundary-law violations), this wrapper catches those errors
    and returns a typed ``Result``: a ``Refusal`` with a descriptive reason on
    failure, or the constructed ``CochainComplex`` on success. Use this at
    replay boundaries where a raised exception would crash execution.

    ``CochainComplex.new`` is intentionally left raising for utility-level use.
    """
    try:
        return CochainComplex.new(c0_dim, c1_dim, c2_dim, d0, d1, provenance)
    except HomologicalError as exc:
        return Refusal(
            reason=f"create_cochain_complex: {type(exc).__name__}: {exc}",
            details={
                "c0_dim": c0_dim,
                "c1_dim": c1_dim,
                "c2_dim": c2_dim,
                "error_type": type(exc).__name__,
            },
        )


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
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/cochain_complex.rs::new"
    )


def verification_source(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verification_source``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/cochain_complex.rs::verification_source"
    )


def provenance_hash(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``provenance_hash``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/cochain_complex.rs::provenance_hash"
    )


def complex_hash(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``complex_hash``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/cochain_complex.rs::complex_hash"
    )


def dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/cochain_complex.rs::dim"
    )


from dataclasses import dataclass
from typing import Sequence
from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.core.gf2_schema import mod2


@dataclass(frozen=True)
class GF2CochainComplex:
    d0: GF2Matrix
    d1: GF2Matrix
    metadata: dict

    @classmethod
    def from_chain(cls, chain: Any) -> GF2CochainComplex:
        boundary_1 = chain.boundary_1()
        boundary_2 = chain.boundary_2()

        d0 = boundary_1.transpose()
        d1 = boundary_2.transpose()

        return cls(
            d0=d0,
            d1=d1,
            metadata={
                "nodes": list(chain.graph.nodes()),
                "edges": list(chain.graph.edges()),
                "faces": [list(face) for face in chain.faces],
                "construction": "cochain_from_directed_graph",
            },
        )

    def validate_cochain(self) -> None:
        for col_idx in range(self.d0.cols):
            col = [self.d0[row][col_idx] for row in range(self.d0.rows)]
            out = self.d1.mat_vec_mul(col)
            if any(out):
                raise ValueError(f"Invalid cochain complex: d1d0 != 0 at column {col_idx}: {out}")

    def create_carrier(self, residual: Sequence[int]) -> MajoranaParityCarrier:
        self.validate_cochain()

        r = [mod2(x) for x in residual]
        if len(r) != self.d0.rows:
            raise ValueError(
                f"Residual length {len(r)} must equal C^1 dimension {self.d0.rows}"
            )

        return MajoranaParityCarrier(
            carrier_kind="majorana_parity_gf2",
            coefficient_field="GF2",
            D0=self.d0.to_list(),
            D1=self.d1.to_list(),
            residual=r,
            metadata=self.metadata,
        ).normalized()








