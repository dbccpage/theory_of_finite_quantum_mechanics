# -*- coding: utf-8 -*-
"""
Domain entities for the CODA application.
Encapsulates problem specifications, local sections, cochains, terminal outcomes, and authority tokens.

Immutability is enforced, not declared: problem instances, layer records and outcomes
are frozen, their mappings are read-only views, their matrices are immutable, and an
outcome refuses at construction any combination the Master Normal Form forbids
(a token on a residual, AUTHORIZED without a token, a token bound to other evidence).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Dict, Mapping, Optional, Tuple

from sympy import Matrix, Rational
from sympy.matrices import MatrixBase

from coda_application.domain._seal import seal_ok
from coda_application.domain.value_objects import (
    DualWitness,
    ExactRational,
    FirewallDecision,
    LayerId,
)


class TerminalKind(str, Enum):
    """The three pairwise disjoint terminal kinds in the CODA Master Normal Form (GTLA-T8)."""

    AUTHORIZED = "AUTHORIZED"           # T_auth
    CLOSED_RESIDUAL = "CLOSED_RESIDUAL" # T_res (retained residual; an anomalon when Phi_1 > 0)
    REFUSED = "REFUSED"                 # F_term


def freeze(value: Any) -> Any:
    """Deep read-only copy: dicts become MappingProxyType, lists and tuples become tuples."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class Section:
    """Local section over an open set U_i."""

    label: str
    values: Tuple[ExactRational, ...]


@dataclass(frozen=True)
class Overlap:
    """Double overlap U_i cap U_j."""

    source_label: str
    target_label: str
    is_compatible: bool
    discrepancy_norm: ExactRational


@dataclass(frozen=True)
class Cochain:
    """Exact rational cochain representation."""

    degree: int
    components: Tuple[ExactRational, ...]

    def to_matrix(self) -> Matrix:
        return Matrix([c.sympy_rational for c in self.components])

    @classmethod
    def from_matrix(cls, degree: int, mat: Matrix) -> Cochain:
        components = tuple(
            ExactRational.from_rational(mat[i, 0])
            for i in range(mat.rows)
        )
        return cls(degree=degree, components=components)


@dataclass(frozen=True)
class ResidualPair:
    """Functional evaluation pair (Phi_1, Gamma_2)."""

    phi1: ExactRational   # L1 quotient defect
    gamma2: ExactRational # Coherent cocycle violation

    @property
    def is_coherent(self) -> bool:
        """Coherent residual: Gamma_2 == 0."""
        return self.gamma2.is_zero

    @property
    def is_exact_zero(self) -> bool:
        """Zero defect: Phi_1 == 0 and Gamma_2 == 0."""
        return self.phi1.is_zero and self.gamma2.is_zero


def _token_body(token: Any) -> Dict[str, Any]:
    return {
        "token_id": token.token_id,
        "licensee": token.licensee,
        "authority_id": token.authority_id,
        "binding": token.binding,
        "granted_externally": token.granted_externally,
        "halt_guards_satisfied": token.halt_guards_satisfied,
    }


@dataclass(frozen=True)
class AuthorityToken:
    """
    Sovereign authorization token.
    Can ONLY be admitted by an authenticated external authority license.
    Cannot be minted by internal derivation, heuristic search, or green tests.

    Only the authority firewall mints tokens: each carries a seal under the
    process-private key over every field, so a caller cannot construct one, re-issue
    one with ``dataclasses.replace`` (the old seal no longer matches), or predict its
    random id. ``binding`` is the digest of the evidence the grant was checked against.
    """

    token_id: str
    licensee: str
    granted_externally: bool
    halt_guards_satisfied: bool
    authority_id: str = ""
    binding: str = ""
    seal: str = ""

    def __post_init__(self):
        if self.granted_externally is not True:
            raise PermissionError(
                "AUTHORITY CONSERVATION BREACH: Attempted internal creation of AuthorityToken without external license"
            )
        if not self.is_valid():
            raise PermissionError(
                "AUTHORITY CONSERVATION BREACH: AuthorityToken was not minted by the authority firewall"
            )

    def is_valid(self) -> bool:
        """Re-verify the seal; also catches tokens built with ``object.__new__``."""
        try:
            return self.granted_externally is True and seal_ok("authority-token", _token_body(self), self.seal)
        except AttributeError:
            return False


@dataclass(frozen=True)
class LayerExecutionRecord:
    """Audit record emitted by each layer of the CODA stack (metadata is read-only)."""

    layer_id: LayerId
    succeeded: bool
    diagnostic_message: str
    defect_mass: ExactRational
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.layer_id, LayerId):
            raise TypeError("layer_id must be a LayerId")
        if not isinstance(self.succeeded, bool):
            raise TypeError("succeeded must be a bool")
        if not isinstance(self.defect_mass, ExactRational):
            raise TypeError("defect_mass must be an ExactRational")
        object.__setattr__(self, "metadata", freeze(dict(self.metadata)))


def _immutable_matrix(value: Any) -> Any:
    if isinstance(value, MatrixBase) and not getattr(value, "is_Immutable", False) and hasattr(value, "as_immutable"):
        return value.as_immutable()
    return value


@dataclass(frozen=True)
class ProblemInstance:
    """
    Complete problem specification for CODA 9-layer evaluation.
    Encapsulates raw data, candidate sieves, profiles, local sections, overlaps, differentials,
    and a legacy license claim.

    ``fda_license_granted`` is only a claim. A bare value never authorizes; authorization
    requires an ``AuthorityGrant`` verified by the firewall. Structural checks (shapes,
    exact entries, d1 d0 = 0) run at intake, so a malformed instance still constructs
    and is then refused by name rather than crashing the pipeline.
    """

    problem_id: str
    raw_data: str
    candidate_sieve: Tuple[str, ...]
    coarse_profile: Tuple[int, int]
    fine_profile: Tuple[int, int]
    projection_map: Dict[int, int]
    local_sections: Dict[str, Tuple[Rational, ...]]
    overlaps: Dict[Tuple[str, str], bool]
    d0: Matrix
    d1: Matrix
    defect_cochain: Matrix
    fda_license_granted: Any = False
    enclosure_interval: Tuple[Rational, Rational] = field(
        default_factory=lambda: (Rational(0), Rational(1))
    )

    def __post_init__(self):
        if not isinstance(self.problem_id, str):
            raise TypeError("problem_id must be a string")
        if not self.problem_id.strip():
            raise ValueError("problem_id cannot be empty or blank")
        for name in ("projection_map", "local_sections", "overlaps"):
            value = getattr(self, name)
            if isinstance(value, Mapping):
                object.__setattr__(self, name, freeze(dict(value)))
        for name in ("candidate_sieve", "coarse_profile", "fine_profile", "enclosure_interval"):
            value = getattr(self, name)
            if isinstance(value, list):
                object.__setattr__(self, name, tuple(value))
        for name in ("d0", "d1", "defect_cochain"):
            object.__setattr__(self, name, _immutable_matrix(getattr(self, name)))


@dataclass(frozen=True)
class MasterNormalFormOutcome:
    """
    Immutable outcome emitted by the CODA Master Normal Form pipeline.
    Carries terminal kind, residual pair, dual witness and primal repair (when the
    evidence was computed), optional authority token, and the 9-layer execution trace.

    Construction enforces GTLA-T8 disjointness: a token appears exactly on AUTHORIZED
    outcomes, only with a zero residual, only when every layer succeeded, and only if
    it was minted for this outcome's evidence.
    """

    problem_id: str
    terminal_kind: TerminalKind
    residual_pair: Optional[ResidualPair]
    dual_witness: Optional[DualWitness]
    authority_token: Optional[AuthorityToken]
    layer_records: Tuple[LayerExecutionRecord, ...]
    firewall_decision: FirewallDecision
    reason: str
    primal_repair: Optional[Tuple[ExactRational, ...]] = None
    evidence_digest: str = ""

    def __post_init__(self):
        if not isinstance(self.terminal_kind, TerminalKind):
            raise TypeError("terminal_kind must be a TerminalKind")
        object.__setattr__(self, "layer_records", tuple(self.layer_records))
        token = self.authority_token
        if self.terminal_kind == TerminalKind.AUTHORIZED:
            if token is None:
                raise ValueError("DISJOINTNESS VIOLATION: AUTHORIZED outcome without an AuthorityToken")
            if self.firewall_decision != FirewallDecision.PERMIT_AUTHORIZED:
                raise ValueError("DISJOINTNESS VIOLATION: AUTHORIZED outcome without a permit decision")
            if self.residual_pair is None or not self.residual_pair.is_exact_zero:
                raise ValueError("DISJOINTNESS VIOLATION: AUTHORIZED outcome with a non-zero or unknown residual")
            if not all(r.succeeded for r in self.layer_records):
                raise ValueError("DISJOINTNESS VIOLATION: AUTHORIZED outcome carries a failed layer record")
            if not isinstance(token, AuthorityToken) or not token.is_valid():
                raise ValueError("DISJOINTNESS VIOLATION: AuthorityToken was not minted by the firewall")
            if not self.evidence_digest or token.binding != self.evidence_digest:
                raise ValueError("DISJOINTNESS VIOLATION: AuthorityToken is bound to other evidence")
        elif token is not None:
            raise ValueError(f"DISJOINTNESS VIOLATION: {self.terminal_kind.value} outcome carried an AuthorityToken")

    @property
    def is_authorized(self) -> bool:
        token = self.authority_token
        return (
            self.terminal_kind == TerminalKind.AUTHORIZED
            and isinstance(token, AuthorityToken)
            and token.is_valid()
            and bool(self.evidence_digest)
            and token.binding == self.evidence_digest
        )

    @property
    def is_closed_residual(self) -> bool:
        return self.terminal_kind == TerminalKind.CLOSED_RESIDUAL

    @property
    def is_refused(self) -> bool:
        return self.terminal_kind == TerminalKind.REFUSED
