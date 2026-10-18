from __future__ import annotations

import hashlib
import json
from dataclasses import field
from datetime import datetime, timezone
from fractions import Fraction
from typing import Any, Dict, Generic, List, Optional, TypeVar, Tuple, Union
from pydantic.dataclasses import dataclass

THeader = TypeVar("THeader")
TPayload = TypeVar("TPayload")

CONTRACT_ID = "urn:omega:domain:packet:v1.0.0"
SCHEMA_VERSION = "omega.domain.packet.v1"


@dataclass(frozen=True)
class ExactnessWitness:
    """Rational exactness witness for categorical and mathematical proofs over Q."""
    duality_gap_numerator: int = 0
    duality_gap_denominator: int = 1
    exact_fraction_str: str = "0/1"
    is_exact: bool = True
    phi_1_norm: float = 0.0
    gamma_2_rate: float = 0.0

    @classmethod
    def zero_gap(cls) -> ExactnessWitness:
        return cls(
            duality_gap_numerator=0,
            duality_gap_denominator=1,
            exact_fraction_str="0/1",
            is_exact=True,
            phi_1_norm=0.0,
            gamma_2_rate=0.0
        )

    @classmethod
    def from_fraction(cls, frac: Fraction, phi_1: float = 0.0, gamma_2: float = 0.0) -> ExactnessWitness:
        return cls(
            duality_gap_numerator=frac.numerator,
            duality_gap_denominator=frac.denominator,
            exact_fraction_str=f"{frac.numerator}/{frac.denominator}",
            is_exact=(frac.numerator == 0),
            phi_1_norm=phi_1,
            gamma_2_rate=gamma_2
        )


@dataclass(frozen=True)
class DomainPacketHeader:
    """Immutable header metadata for a domain packet."""
    packet_id: str
    crate_source: str
    crate_target: str
    payload_type: str
    schema_version: str = SCHEMA_VERSION
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    contract_uri: Optional[str] = None
    correlation_id: Optional[str] = None


@dataclass(frozen=True)
class DomainPacket(Generic[THeader, TPayload]):
    """Unified base DomainPacket value object for all omega_engine crates.

    Invariants:
    - Immutable Value Object.
    - Deterministic SHA-256 content addressing.
    - Default AuthorityEffect: None (proposals require human minting).
    - Contains exactness witness certification for mathematical operators.
    """
    header: DomainPacketHeader
    payload: TPayload
    witness: ExactnessWitness = field(default_factory=ExactnessWitness.zero_gap)
    trace_refs: List[str] = field(default_factory=list)
    sha256_digest: str = field(default_factory=str)
    authority_effect: str = "None"

    def compute_digest(self) -> str:
        """Deterministically computes the SHA-256 digest of header and payload."""
        data = {
            "header": {
                "packet_id": self.header.packet_id,
                "crate_source": self.header.crate_source,
                "crate_target": self.header.crate_target,
                "payload_type": self.header.payload_type,
                "schema_version": self.header.schema_version,
                "contract_uri": self.header.contract_uri,
            },
            "payload": self._serialize_payload(self.payload),
            "witness": {
                "gap": self.witness.exact_fraction_str,
                "is_exact": self.witness.is_exact,
                "phi_1": self.witness.phi_1_norm,
            },
            "authority_effect": self.authority_effect,
        }
        raw_bytes = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(raw_bytes).hexdigest()

    def _serialize_payload(self, p: Any) -> Any:
        if hasattr(p, "__dict__"):
            return {k: str(v) for k, v in p.__dict__.items() if not k.startswith("_")}
        elif isinstance(p, dict):
            return {str(k): str(v) for k, v in p.items()}
        elif isinstance(p, (list, tuple, set)):
            return [str(x) for x in p]
        return str(p)


# Concrete Typed Domain Packets

@dataclass(frozen=True)
class SymbolGamePayload:
    symbol: str
    alphabet: List[str]
    rewrite_rules: Dict[str, str] = field(default_factory=dict)
    ast_tree: Optional[Dict[str, Any]] = None
    step_count: int = 0


@dataclass(frozen=True)
class SymbolGamePacket(DomainPacket[DomainPacketHeader, SymbolGamePayload]):
    """Typed packet for Symbol Game AST transformations and string rewrites."""
    pass


@dataclass(frozen=True)
class CarrierPayload:
    carrier_id: str
    nodes: List[str] = field(default_factory=list)
    edges: List[Tuple[str, str]] = field(default_factory=list)
    dimension: int = 1
    is_closed: bool = True


@dataclass(frozen=True)
class CarrierPacket(DomainPacket[DomainPacketHeader, CarrierPayload]):
    """Typed packet for Carrier graphs, complexes, and topological substrates."""
    pass


@dataclass(frozen=True)
class ResidualPayload:
    cochain_id: str
    phi_1_defect_norm: float
    gamma_2_rate: float
    is_coboundary: bool
    defect_vector: List[float] = field(default_factory=list)


@dataclass(frozen=True)
class ResidualPacket(DomainPacket[DomainPacketHeader, ResidualPayload]):
    """Typed packet for Residual defect norms and coboundary evaluations."""
    pass


@dataclass(frozen=True)
class ObserverPayload:
    """Minimal 9-tuple Observer: O = (K, F, R, delta, d0, d1, J, M, tau)."""
    observer_id: str
    carrier_k: List[str] = field(default_factory=list)                     # K: finite carrier
    local_state_spaces_f: Dict[str, Any] = field(default_factory=dict)     # F: local state spaces
    comparison_relation_r: List[Tuple[str, str]] = field(default_factory=list) # R: comparison relation
    delta_defect_map: Dict[str, float] = field(default_factory=dict)       # delta: defect operator
    d0_admissible_repair: List[str] = field(default_factory=list)          # d0: local repair / gauge shift
    d1_closure_operator: str = "coboundary_d1"                             # d1: closure check
    gauge_norm_j: str = "L1_defect_norm"                                  # J: measuring ruler / norm
    transformation_class_m: str = "EquivariantMorphisms"                   # M: compatible transformation class
    terminalizer_tau: str = "PASS_TO_MASTER"                               # tau: terminal status rule
    measurement_operator: str = ""
    probe_fields: List[str] = field(default_factory=list)
    observed_values: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class ObserverPacket(DomainPacket[DomainPacketHeader, ObserverPayload]):
    """Typed packet for Observer measurement operators and diagnostic probes."""
    pass


@dataclass(frozen=True)
class ContractPayload:
    contract_id: str
    crate_name: str
    preconditions_passed: bool
    postconditions_passed: bool
    invariants_verified: List[str] = field(default_factory=list)
    violations: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ContractPacket(DomainPacket[DomainPacketHeader, ContractPayload]):
    """Typed packet for contract boundary enforcement and verification receipts."""
    pass


@dataclass(frozen=True)
class SolverPayload:
    solver_id: str
    problem_type: str
    objective_value: float
    duality_gap_fraction: str
    constraints: List[str] = field(default_factory=list)
    solution_vector: List[float] = field(default_factory=list)
    is_optimal: bool = True


@dataclass(frozen=True)
class SolverPacket(DomainPacket[DomainPacketHeader, SolverPayload]):
    """Typed packet for L1 gauge solvers, primal-dual relaxations, and exact rational certificates."""
    pass


@dataclass(frozen=True)
class SearchPayload:
    search_id: str
    search_algorithm: str
    current_state_digest: str
    frontier_size: int = 0
    expanded_nodes: int = 0
    heuristic_scores: Dict[str, float] = field(default_factory=dict)
    best_path: List[str] = field(default_factory=list)
    is_terminated: bool = False


@dataclass(frozen=True)
class SearchPacket(DomainPacket[DomainPacketHeader, SearchPayload]):
    """Typed packet for AST rewrite search, beam exploration, and homotopy state traversal."""
    pass


@dataclass(frozen=True)
class GaugePayload:
    """Gauge Specification: Freedom of re-description under d0 and transformation class M."""
    gauge_id: str
    reference_frame: str
    transformation_class_m: str
    admissible_shifts_d0: List[str] = field(default_factory=list)
    is_pure_coboundary: bool = True
    residual_after_gauge: float = 0.0


@dataclass(frozen=True)
class GaugePacket(DomainPacket[DomainPacketHeader, GaugePayload]):
    """Typed packet for gauge transformations, reference shifts, and quotient evaluation Q1 = C1 / im(d0)."""
    pass


@dataclass(frozen=True)
class AuthorityPayload:
    """Authority Regime: A = (S, claim, sigma, e, V#, tau#, Pi#, RolePolicy, AuthRoot, Verify)."""
    system_host_s: str
    claim: str
    scope_sigma: str
    evidence_refs_e: List[str] = field(default_factory=list)
    verifier_role_v: str = "verifier"
    evaluation_terminal_tau: str = "ACCEPT"
    pipeline_path_pi: str = "canonical_pipeline"
    role_policy_satisfied: bool = True
    auth_root: str = "HumanMultiSig_Root"
    certificate_id: Optional[str] = None
    grade: str = "None"
    refusal_reason: Optional[str] = None


@dataclass(frozen=True)
class AuthorityPacket(DomainPacket[DomainPacketHeader, AuthorityPayload]):
    """Typed packet for operational authorization, role-policy gates, and root-verified certificates."""
    pass


@dataclass(frozen=True)
class QuantumObserverPayload:
    """Quantum Measurement Regime: O_Q = (S(H), A_obs, B_coupling, J_Q, Phi_Q, tau_Q)."""
    observable_basis: str
    quantum_carrier_hilbert_dim: int = 2
    density_matrix_diag: List[float] = field(default_factory=lambda: [0.5, 0.5])
    density_matrix_coherence_norm: float = 0.5
    coupling_boundary: str = "DetectorCoupling"
    trace_norm_defect_j: float = 0.0
    is_divergence_free_dual: bool = True
    registered_terminal_outcome: str = "|0><0|"


@dataclass(frozen=True)
class QuantumObserverPacket(DomainPacket[DomainPacketHeader, QuantumObserverPayload]):
    """Typed packet for quantum density operators, trace-norm distinguishability, and POVM readouts."""
    pass


@dataclass(frozen=True)
class AiLlmObserverPayload:
    """AI-LLM Evaluator Stack: O_AI = (Sigma_prompt, T_trace, B_tools, E_local, E_global, L_res, tau_eval)."""
    prompt_envelope: str
    trace_trajectory_digest: str
    tools_invoked: List[str] = field(default_factory=list)
    local_evaluator_passed: bool = True
    global_evaluator_passed: bool = True
    dropped_boundary_facts: List[str] = field(default_factory=list)
    residual_ledger_entries: List[str] = field(default_factory=list)
    evaluation_terminal_tag: str = "ACCEPT"


@dataclass(frozen=True)
class AiLlmObserverPacket(DomainPacket[DomainPacketHeader, AiLlmObserverPayload]):
    """Typed packet for AI evaluator stacks, boundary fact preservation, and LGGR prevention."""
    pass



from omega_engine_governance.contracts import AuthorityEffect


@dataclass(frozen=True)
class FOCRealCert:
    packet: Any
    witness: Any
    authority_effect: Union[AuthorityEffect, str] = AuthorityEffect.None_

    def __post_init__(self) -> None:
        from omega_engine.crates.replay import ReplayTracePacket
        if not isinstance(self.packet, ReplayTracePacket):
            raise TypeError("requires a ReplayTracePacket")
        packet_hash = getattr(self.packet, "replay_hash", None)
        witness_hash = getattr(self.witness, "replay_hash", None)
        if packet_hash is not None and witness_hash is not None and packet_hash != witness_hash:
            raise ValueError("witness not bound to packet")


@dataclass(frozen=True)
class CheckedPacket:
    """Verified transport packet envelope."""

    cert: Any
    checked_hash: str = ""
    checker_ref: str = ""
    authority_effect: Any = field(default_factory=lambda: AuthorityEffect.None_)

    @property
    def packet(self) -> Any:
        return getattr(self.cert, "packet", self.cert)

    @property
    def replay_hash(self) -> str:
        return getattr(self.packet, "replay_hash", "")


__all__ = [
    "CONTRACT_ID",
    "SCHEMA_VERSION",
    "ExactnessWitness",
    "DomainPacketHeader",
    "DomainPacket",
    "SymbolGamePayload",
    "SymbolGamePacket",
    "CarrierPayload",
    "CarrierPacket",
    "ResidualPayload",
    "ResidualPacket",
    "ObserverPayload",
    "ObserverPacket",
    "ContractPayload",
    "ContractPacket",
    "SolverPayload",
    "SolverPacket",
    "SearchPayload",
    "SearchPacket",
    "GaugePayload",
    "GaugePacket",
    "AuthorityPayload",
    "AuthorityPacket",
    "QuantumObserverPayload",
    "QuantumObserverPacket",
    "AiLlmObserverPayload",
    "AiLlmObserverPacket",
    "FOCRealCert",
    "CheckedPacket",
]

