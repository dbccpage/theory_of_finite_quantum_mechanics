"""Carrier State Contract Implementation.

Conforms strictly to contract specification:
    urn:omega:state:carrier:v1.0.0
    (omega_engine/crates/omega_contracts/src/contract_canonical_definitions/01_core_state/carrier.contract.yaml)

Doctrine:
- Carrier is finite declared cohomological structure (C^0, C^1, C^2, d0, d1).
- Carrier is NOT world, model, ontology, semantic domain, embedding space, terminalizer, or executor.
- Carrier artifacts default to AuthorityEffect: EvidenceOnly.
- Promotion to FactOnly requires checked chain/cochain law d1 ∘ d0 = 0.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Sequence

try:
    from omega_engine.crates.homology_theory.carrier import Carrier as MathCarrier
    from omega_engine.crates.homology_theory.qmatrix import QMatrix
except ImportError:
    MathCarrier = None
    QMatrix = None


CONTRACT_ID = "urn:omega:state:carrier:v1.0.0"
SCHEMA_VERSION = "omega.contract.v1"


@dataclass(frozen=True)
class CarrierArtifact:
    """Contract-level declared carrier record (EvidenceOnly by default)."""
    carrier_id: str
    carrier_kind: str
    c0_ref: str
    c1_ref: str
    c2_ref: str
    d0_ref: str
    d1_ref: str
    admissible_repair_set: str
    context_family: str
    coefficient_semantics: str
    schema_hash: str
    carrier_hash: str
    chain_law_witness: Optional[str] = None
    chain_law_certificate: Optional[str] = None
    witness_refs: List[str] = field(default_factory=list)
    certificate_refs: List[str] = field(default_factory=list)
    authority_effect: str = "EvidenceOnly"


@dataclass(frozen=True)
class CheckedCarrierArtifact:
    """Checked contract wrapper, FactOnly after verified d1 ∘ d0 = 0."""
    artifact: CarrierArtifact
    is_valid_chain_law: bool
    authority_effect: str = "FactOnly"

    def __post_init__(self) -> None:
        if not self.is_valid_chain_law:
            raise ValueError("CheckedCarrierArtifact requires is_valid_chain_law=True")


class Carrier:
    """Finite declared cohomological carrier state space."""

    def __init__(
        self,
        c0_dim: int,
        c1_dim: int,
        c2_dim: int,
        d0: List[List[float]],
        d1: List[List[float]],
        carrier_kind: str = "cochain_complex",
        coefficient_semantics: str = "GF2_or_Rational",
        context_family: str = "standard_family",
        admissible_repair_set: str = "linear_subspace",
    ):
        if c0_dim <= 0 or c1_dim <= 0 or c2_dim < 0:
            raise ValueError(f"Invalid dimensions: c0={c0_dim}, c1={c1_dim}, c2={c2_dim}")
        
        self.c0_dim = c0_dim
        self.c1_dim = c1_dim
        self.c2_dim = c2_dim
        self.d0 = d0
        self.d1 = d1
        self.carrier_kind = carrier_kind
        self.coefficient_semantics = coefficient_semantics
        self.context_family = context_family
        self.admissible_repair_set = admissible_repair_set
        
        self.carrier_id = f"carrier:{self.compute_carrier_hash()[:16]}"
        self.schema_hash = self.compute_schema_hash()
        self.carrier_hash = self.compute_carrier_hash()

    def compute_schema_hash(self) -> str:
        data = f"{CONTRACT_ID}:{SCHEMA_VERSION}:{self.carrier_kind}:{self.coefficient_semantics}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def compute_carrier_hash(self) -> str:
        data = {
            "c0_dim": self.c0_dim,
            "c1_dim": self.c1_dim,
            "c2_dim": self.c2_dim,
            "d0": self.d0,
            "d1": self.d1,
            "carrier_kind": self.carrier_kind,
        }
        raw = json.dumps(data, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def verify_chain_law(self) -> bool:
        """Verify d1 ∘ d0 = 0."""
        if self.c2_dim == 0 or not self.d1 or not self.d0:
            return True
        
        # Matrix multiplication d1 (c2 x c1) * d0 (c1 x c0)
        n_c2 = len(self.d1)
        n_c1 = len(self.d0)
        n_c0 = len(self.d0[0]) if n_c1 > 0 else 0
        
        for i in range(n_c2):
            for j in range(n_c0):
                val = sum(self.d1[i][k] * self.d0[k][j] for k in range(n_c1))
                if abs(val) > 1e-9:
                    return False
        return True

    def to_artifact(self) -> CarrierArtifact:
        """Export as EvidenceOnly CarrierArtifact."""
        is_zero = self.verify_chain_law()
        witness = f"witness:d1_d0_zero:{self.carrier_hash[:8]}" if is_zero else None
        
        return CarrierArtifact(
            carrier_id=self.carrier_id,
            carrier_kind=self.carrier_kind,
            c0_ref=f"space:c0:{self.c0_dim}",
            c1_ref=f"space:c1:{self.c1_dim}",
            c2_ref=f"space:c2:{self.c2_dim}",
            d0_ref=f"map:d0:{self.c1_dim}x{self.c0_dim}",
            d1_ref=f"map:d1:{self.c2_dim}x{self.c1_dim}",
            admissible_repair_set=self.admissible_repair_set,
            context_family=self.context_family,
            coefficient_semantics=self.coefficient_semantics,
            schema_hash=self.schema_hash,
            carrier_hash=self.carrier_hash,
            chain_law_witness=witness,
            authority_effect="EvidenceOnly",
        )

    def check_contract(self) -> CheckedCarrierArtifact:
        """Verify chain law d1 ∘ d0 = 0 and promote to CheckedCarrierArtifact (FactOnly)."""
        artifact = self.to_artifact()
        if not self.verify_chain_law():
            raise ValueError(f"Carrier {self.carrier_id} violates chain law d1 ∘ d0 = 0")
        
        return CheckedCarrierArtifact(
            artifact=artifact,
            is_valid_chain_law=True,
            authority_effect="FactOnly",
        )


def verify_carrier_contract(carrier: Carrier) -> Dict[str, Any]:
    """Helper to audit carrier against urn:omega:state:carrier:v1.0.0 contract invariants."""
    is_law = carrier.verify_chain_law()
    artifact = carrier.to_artifact()
    
    return {
        "contract_id": CONTRACT_ID,
        "carrier_id": carrier.carrier_id,
        "is_valid_chain_law": is_law,
        "schema_hash": carrier.schema_hash,
        "carrier_hash": carrier.carrier_hash,
        "authority_effect": "FactOnly" if is_law else "EvidenceOnly",
        "admissible": is_law,
    }


__all__ = [
    "Carrier",
    "CarrierArtifact",
    "CheckedCarrierArtifact",
    "verify_carrier_contract",
    "CONTRACT_ID",
    "SCHEMA_VERSION",
]




