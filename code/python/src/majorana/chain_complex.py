from __future__ import annotations
"""Chain complexes, chains, and the cycle checker.

Port of ``chain_complex.rs`` / ``chain.rs`` / ``cycle.rs``. A ChainComplex of
degree 2 carries boundary maps d2 : C_2 -> C_1 and d1 : C_1 -> C_0 with the law
d1 . d2 = 0.
"""


from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional

from .errors import CoboundaryLawViolation, DimensionMismatch, NotCycle
from .hashing import Hash32, hash_bytes, hash_matrix
from .ids import BasisId, Degree
from .qmatrix import QMatrix
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix


@dataclass
class BoundaryMap:
    """A boundary operator with its matrix (rows = lower degree, cols = higher)."""

    matrix: QMatrix


class ChainComplex:
    """Degree-2 chain complex: C_2 --d2--> C_1 --d1--> C_0, with d1.d2 = 0."""

    def __init__(
        self,
        n0: int,
        n1: int,
        n2: int,
        boundary_1: BoundaryMap,
        boundary_2: BoundaryMap,
    ):
        self.n0 = n0
        self.n1 = n1
        self.n2 = n2
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

    @classmethod
    def new(cls, n0: int, n1: int, n2: int, d1: QMatrix, d2: QMatrix) -> "ChainComplex":
        if d1.shape != (n0, n1):
            raise DimensionMismatch(f"d1 must be {n0}x{n1}, got {d1.shape}")
        if d2.shape != (n1, n2):
            raise DimensionMismatch(f"d2 must be {n1}x{n2}, got {d2.shape}")
        if n2 > 0 and not d1.matmul(d2).is_zero():
            raise CoboundaryLawViolation("d1 . d2 != 0")
        return cls(n0, n1, n2, BoundaryMap(d1), BoundaryMap(d2))

    def complex_hash(self) -> Hash32:
        return hash_bytes(
            f"{self.n2},{self.n1},{self.n0};".encode("utf-8"),
            hash_matrix(self.boundary_1.matrix).digest,
            hash_matrix(self.boundary_2.matrix).digest,
        )


@dataclass
class Chain:
    degree: Degree
    basis_id: BasisId
    values: List[Fraction]

    @classmethod
    def new(cls, degree: Degree, basis_id: BasisId, values: List) -> "Chain":
        return cls(degree, basis_id, [Fraction(v) for v in values])

    @classmethod
    def zero(cls, degree: Degree, basis_id: BasisId, dim: int) -> "Chain":
        return cls(degree, basis_id, [Fraction(0)] * dim)

    def column(self) -> QMatrix:
        return QMatrix(len(self.values), 1, [[v] for v in self.values])


@dataclass
class CycleWitness:
    chain: Chain
    complex_hash: Hash32


def try_cycle(
    chain: Chain, boundary: Optional[BoundaryMap], complex_hash: Hash32
) -> CycleWitness:
    """Verify d(chain) = 0. Returns a witness or raises NotCycle."""
    if boundary is not None:
        dz = boundary.matrix.matmul(chain.column())
        if not dz.is_zero():
            raise NotCycle("chain has nonzero boundary; not a cycle")
    return CycleWitness(chain, complex_hash)


from dataclasses import dataclass  
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
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/chain_complex.rs::new"
    )


def complex_hash(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``complex_hash``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/chain_complex.rs::complex_hash"
    )


def dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/chain_complex.rs::dim"
    )


@dataclass(frozen=True)
class GF2ChainComplex:
    graph: Any
    faces: tuple[tuple[int, ...], ...]

    @property
    def num_vertices(self) -> int:
        return len(self.graph.nodes())

    @property
    def num_edges(self) -> int:
        return len(self.graph.edges())

    @property
    def num_faces(self) -> int:
        return len(self.faces)

    def boundary_1(self) -> GF2Matrix:
        """∂1: C1 -> C0"""
        data = [[0] * self.num_edges for _ in range(self.num_vertices)]
        for edge_idx, (u, v) in enumerate(self.graph.edges()):
            data[u][edge_idx] = 1
            data[v][edge_idx] = 1
        return GF2Matrix(data)

    def boundary_2(self) -> GF2Matrix:
        """∂2: C2 -> C1"""
        if self.num_faces == 0:
            return GF2Matrix.zeros(self.num_edges, 0)

        data = [[0] * self.num_faces for _ in range(self.num_edges)]
        for face_idx, edge_indices in enumerate(self.faces):
            for edge_idx in edge_indices:
                if edge_idx < 0 or edge_idx >= self.num_edges:
                    raise ValueError(f"Face {face_idx} references invalid edge {edge_idx}")
                data[edge_idx][face_idx] = 1
        return GF2Matrix(data)

    def to_cochain(self) -> Any:
        from .cochain_complex import GF2CochainComplex
        return GF2CochainComplex.from_chain(self)








