"""Domain interfaces and immutable request/certificate containers.

Construction freezes the supplied containers; it does not verify a certificate.
Only the canonical checker can establish a certificate's validity.

AuthorityEffect: None.
Clean Architecture Layer: Domain Ports & Value Objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Mapping, Optional, Protocol, Sequence, Tuple, runtime_checkable

from witnessed_difference.rop import Refusal, Result


@dataclass(frozen=True)
class L1Solution:
    """Exact L1 quotient minimization solution."""

    phi1_value: Fraction
    potential: Mapping[str, Fraction]
    residual: Mapping[Tuple[str, str], Fraction]
    dual: Mapping[Tuple[str, str], Fraction]
    is_exact: bool
    iterations: int = 0
    authority_effect: str = "None"
    backend: str = "rust"

    def __post_init__(self) -> None:
        if self.potential is not None:
            object.__setattr__(self, "potential", MappingProxyType(dict(self.potential)))
        if self.residual is not None:
            object.__setattr__(self, "residual", MappingProxyType(dict(self.residual)))
        if self.dual is not None:
            object.__setattr__(self, "dual", MappingProxyType(dict(self.dual)))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, L1Solution)
        return (
            self.phi1_value == other.phi1_value
            and dict(self.potential) == dict(other.potential)
            and dict(self.residual) == dict(other.residual)
            and dict(self.dual) == dict(other.dual)
            and self.is_exact == other.is_exact
            and self.iterations == other.iterations
            and self.authority_effect == other.authority_effect
            and self.backend == other.backend
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.phi1_value,
            tuple(sorted(self.potential.items())),
            tuple(sorted(self.residual.items())),
            tuple(sorted(self.dual.items())),
            self.is_exact,
            self.iterations,
            self.authority_effect,
            self.backend,
        ))

    def __getitem__(self, key: str) -> Any:
        if key in ("phi1", "phi1_value"):
            return self.phi1_value
        if key == "potential":
            return self.potential
        if key == "residual":
            return self.residual
        if key == "dual":
            return self.dual
        if key == "is_exact":
            return self.is_exact
        if key == "iterations":
            return self.iterations
        if key == "authority_effect":
            return self.authority_effect
        if key == "backend":
            return self.backend
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@dataclass(frozen=True)
class ObstructionSolveRequest:
    """Request for exact 1-cochain L1 quotient solving."""

    vertices: Tuple[str, ...]
    edges: Tuple[Tuple[str, str], ...]
    cochain: Mapping[Tuple[str, str], Fraction]
    weights: Mapping[Tuple[str, str], Fraction]
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if self.cochain is not None:
            object.__setattr__(self, "cochain", MappingProxyType(dict(self.cochain)))
        if self.weights is not None:
            object.__setattr__(self, "weights", MappingProxyType(dict(self.weights)))
        object.__setattr__(self, "vertices", tuple(self.vertices))
        object.__setattr__(self, "edges", tuple(tuple(edge) for edge in self.edges))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, ObstructionSolveRequest)
        return (
            self.vertices == other.vertices
            and self.edges == other.edges
            and dict(self.cochain) == dict(other.cochain)
            and dict(self.weights) == dict(other.weights)
            and self.authority_effect == other.authority_effect
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.vertices,
            self.edges,
            tuple(sorted(self.cochain.items())),
            tuple(sorted(self.weights.items())),
            self.authority_effect,
        ))


@dataclass(frozen=True)
class GenesisDescentRequest:
    """Request for Moore machine history descent analysis."""

    memory_transitions: Tuple[Tuple[int, ...], ...]
    memory_initial: int
    transducer_transitions: Tuple[Tuple[int, ...], ...]
    transducer_emit: Tuple[Tuple[Tuple[int, ...], ...], ...]
    transducer_initial: int
    prefix_words: Tuple[int, ...]
    final_words: Tuple[Tuple[int, ...], ...]
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        for name in ("memory_transitions", "transducer_transitions", "final_words"):
            object.__setattr__(self, name, tuple(tuple(row) for row in getattr(self, name)))
        object.__setattr__(self, "transducer_emit", tuple(tuple(tuple(word) for word in row) for row in self.transducer_emit))
        object.__setattr__(self, "prefix_words", tuple(self.prefix_words))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, GenesisDescentRequest)
        return (
            self.memory_transitions == other.memory_transitions
            and self.memory_initial == other.memory_initial
            and self.transducer_transitions == other.transducer_transitions
            and self.transducer_emit == other.transducer_emit
            and self.transducer_initial == other.transducer_initial
            and self.prefix_words == other.prefix_words
            and self.final_words == other.final_words
            and self.authority_effect == other.authority_effect
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.memory_transitions,
            self.memory_initial,
            self.transducer_transitions,
            self.transducer_emit,
            self.transducer_initial,
            self.prefix_words,
            self.final_words,
            self.authority_effect,
        ))


@dataclass(frozen=True)
class GenesisDescentResult:
    """Outcome of Genesis Moore machine descent verification."""

    kind: str
    prefix: Tuple[int, ...] = ()
    certificate: str = ""
    collision_first: Optional[Tuple[int, ...]] = None
    collision_second: Optional[Tuple[int, ...]] = None
    authority_effect: str = "None"
    backend: str = "rust"

    def __post_init__(self) -> None:
        for name in ("prefix", "collision_first", "collision_second"):
            if getattr(self, name) is not None:
                object.__setattr__(self, name, tuple(getattr(self, name)))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, GenesisDescentResult)
        return (
            self.kind == other.kind
            and self.prefix == other.prefix
            and self.certificate == other.certificate
            and self.collision_first == other.collision_first
            and self.collision_second == other.collision_second
            and self.authority_effect == other.authority_effect
            and self.backend == other.backend
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.kind,
            self.prefix,
            self.certificate,
            self.collision_first,
            self.collision_second,
            self.authority_effect,
            self.backend,
        ))

    def __getitem__(self, key: str) -> Any:
        if key == "kind":
            return self.kind
        if key == "prefix":
            return list(self.prefix)
        if key == "certificate":
            return self.certificate
        if key == "collision_first":
            return list(self.collision_first) if self.collision_first is not None else None
        if key == "collision_second":
            return list(self.collision_second) if self.collision_second is not None else None
        if key == "authority_effect":
            return self.authority_effect
        if key == "backend":
            return self.backend
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@dataclass(frozen=True)
class QuotientCertificate:
    """Independently verifiable primal potential and dual circulation certificate."""

    phi1: Fraction
    potential: Mapping[str, Fraction]
    residual: Mapping[Tuple[str, str], Fraction]
    dual_witness: Mapping[Tuple[str, str], Fraction]
    is_exact: bool
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if self.potential is not None:
            object.__setattr__(self, "potential", MappingProxyType(dict(self.potential)))
        if self.residual is not None:
            object.__setattr__(self, "residual", MappingProxyType(dict(self.residual)))
        if self.dual_witness is not None:
            object.__setattr__(self, "dual_witness", MappingProxyType(dict(self.dual_witness)))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, QuotientCertificate)
        return (
            self.phi1 == other.phi1
            and dict(self.potential) == dict(other.potential)
            and dict(self.residual) == dict(other.residual)
            and dict(self.dual_witness) == dict(other.dual_witness)
            and self.is_exact == other.is_exact
            and self.authority_effect == other.authority_effect
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.phi1,
            tuple(sorted(self.potential.items())),
            tuple(sorted(self.residual.items())),
            tuple(sorted(self.dual_witness.items())),
            self.is_exact,
            self.authority_effect,
        ))


@dataclass(frozen=True)
class QuotientVerificationReceipt:
    """Algebraic verification receipt for a QuotientCertificate."""

    is_verified: bool
    phi1: Fraction
    divergence_zero: bool
    duality_gap_zero: bool
    authority_effect: str = "None"

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, QuotientVerificationReceipt)
        return (
            self.is_verified == other.is_verified
            and self.phi1 == other.phi1
            and self.divergence_zero == other.divergence_zero
            and self.duality_gap_zero == other.duality_gap_zero
            and self.authority_effect == other.authority_effect
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.is_verified,
            self.phi1,
            self.divergence_zero,
            self.duality_gap_zero,
            self.authority_effect,
        ))


@dataclass(frozen=True)
class DigestReceipt:
    """Cryptographic execution receipt binding request, response, and binary image."""

    request_digest: str
    response_digest: str
    binary_digest: str
    execution_digest: str
    authority_effect: str = "None"

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, DigestReceipt)
        return (
            self.request_digest == other.request_digest
            and self.response_digest == other.response_digest
            and self.binary_digest == other.binary_digest
            and self.execution_digest == other.execution_digest
            and self.authority_effect == other.authority_effect
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.request_digest,
            self.response_digest,
            self.binary_digest,
            self.execution_digest,
            self.authority_effect,
        ))


@dataclass(frozen=True)
class WdpObstructionSolution:
    """Solution to WDP obstruction problem with dual witness and dict-like access."""

    phi1: Fraction
    is_exact: bool
    potential: Mapping[str, Fraction]
    residual: Mapping[Tuple[str, str], Fraction]
    dual_witness: Optional[Mapping[Tuple[str, str], Fraction]] = None
    backend: str = "rust"
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if self.potential is not None:
            object.__setattr__(self, "potential", MappingProxyType(dict(self.potential)))
        if self.residual is not None:
            object.__setattr__(self, "residual", MappingProxyType(dict(self.residual)))
        if self.dual_witness is not None:
            object.__setattr__(self, "dual_witness", MappingProxyType(dict(self.dual_witness)))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, WdpObstructionSolution)
        return (
            self.phi1 == other.phi1
            and self.is_exact == other.is_exact
            and dict(self.potential) == dict(other.potential)
            and dict(self.residual) == dict(other.residual)
            and (
                dict(self.dual_witness) == dict(other.dual_witness)
                if self.dual_witness is not None and other.dual_witness is not None
                else self.dual_witness == other.dual_witness
            )
            and self.backend == other.backend
            and self.authority_effect == other.authority_effect
        )

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.phi1,
            self.is_exact,
            tuple(sorted(self.potential.items())),
            tuple(sorted(self.residual.items())),
            tuple(sorted(self.dual_witness.items())) if self.dual_witness is not None else None,
            self.backend,
            self.authority_effect,
        ))

    def __getitem__(self, key: str) -> Any:
        if key == "phi1":
            return self.phi1
        if key == "is_exact":
            return self.is_exact
        if key == "potential":
            return self.potential
        if key == "residual":
            return self.residual
        if key in ("dual", "dual_witness"):
            return self.dual_witness
        if key == "backend":
            return self.backend
        if key == "authority_effect":
            return self.authority_effect
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@runtime_checkable
class WdpObstructionSolverPort(Protocol):
    """Port for exact rational simplicial L1 quotient LP duality solving."""

    def solve_obstruction_l1(
        self,
        request: ObstructionSolveRequest,
    ) -> Result[L1Solution, Refusal]:
        """Solve min_phi ||h - d0 phi||_{1,w} and emit dual certificate y."""
        ...


@runtime_checkable
class GenesisObserverPort(Protocol):
    """Port for Genesis history memory descent and Moore transducer quotient analysis."""

    def solve_genesis_descent(
        self,
        request: GenesisDescentRequest,
    ) -> Result[GenesisDescentResult, Refusal]:
        """Compute state descent or extract collision witness."""
        ...


@runtime_checkable
class QuotientVerifierPort(Protocol):
    """Port for independent algebraic recomputation of quotient certificates."""

    def verify_certificate(
        self,
        certificate: QuotientCertificate,
    ) -> Result[QuotientVerificationReceipt, Refusal]:
        """Verify residual, bounds, divergence-free property, and zero duality gap."""
        ...


@runtime_checkable
class CanonicalDigestPort(Protocol):
    """Port for deterministic RFC 8785 Canonical JSON serialization and SHA-256 hashing."""

    def canonical_json(self, value: Mapping[str, Any]) -> Result[bytes, Refusal]:
        """Serialize dictionary to RFC 8785 canonical bytes."""
        ...

    def sha256_digest(self, payload: bytes) -> str:
        """Compute SHA-256 hexadecimal string from bytes."""
        ...

    def bind_execution(
        self,
        request_bytes: bytes,
        response_bytes: bytes,
        binary_digest: str,
    ) -> DigestReceipt:
        """Create compound two-pass execution receipt."""
        ...
