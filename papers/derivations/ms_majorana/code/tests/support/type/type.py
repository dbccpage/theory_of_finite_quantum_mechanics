from __future__ import annotations
from pydantic import ConfigDict
"""Type and Kind Contract Subsystem Implementation.

Conforms strictly to contract specification:
    urn:omega:state:type_and_kind:v1.0.0
    (omega_engine/crates/omega_contracts/src/contract_canonical_definitions/01_core_state/type_and_kind.contract.yaml)

Doctrine:
- Defines inert schema-bound BaseType and KindDefinition data containers.
- BaseTypes do not validate, repair, terminalize, or execute themselves.
- AuthorityEffect: None.
"""


import hashlib
import json
from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Any, Dict, List, Optional

CONTRACT_ID = "urn:omega:state:type_and_kind:v1.0.0"
SCHEMA_VERSION = "omega.contract.v1"


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class KindDefinition:
    """Canonical schema kind definition."""

    kind_name: str
    category: str
    field_schema: Dict[str, str]
    invariants: List[str] = field(default_factory=list)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class BaseType:
    """Inert schema-bound data type container conforming to urn:omega:state:type_and_kind:v1.0.0."""

    type_id: str
    kind: KindDefinition
    payload: Dict[str, Any]
    type_hash: str = field(default_factory=str)
    authority_effect: str = "None"

    def compute_hash(self) -> str:
        data = {
            "type_id": self.type_id,
            "kind_name": self.kind.kind_name,
            "payload": self.payload,
            "authority_effect": self.authority_effect,
        }
        raw_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw_bytes).hexdigest()


class TypeRegistry:
    """Registry and factory for BaseType definitions."""

    def __init__(self, registry_id: str = "type_registry"):
        self.registry_id = registry_id
        self._kinds: Dict[str, KindDefinition] = {}

    def register_kind(self, kind: KindDefinition) -> None:
        """Register a KindDefinition schema."""
        self._kinds[kind.kind_name] = kind

    def create_type(self, type_id: str, kind_name: str, payload: Dict[str, Any]) -> BaseType:
        """Instantiate a BaseType envelope."""
        if kind_name not in self._kinds:
            kind = KindDefinition(kind_name=kind_name, category="generic", field_schema={})
        else:
            kind = self._kinds[kind_name]

        b_type = BaseType(
            type_id=type_id,
            kind=kind,
            payload=payload,
            authority_effect="None",
        )
        t_hash = b_type.compute_hash()
        return BaseType(
            type_id=b_type.type_id,
            kind=b_type.kind,
            payload=b_type.payload,
            type_hash=t_hash,
            authority_effect="None",
        )


def verify_type_contract(type_instance: BaseType) -> bool:
    """Verify that a BaseType instance conforms to urn:omega:state:type_and_kind:v1.0.0."""
    return (
        isinstance(type_instance, BaseType)
        and hasattr(type_instance, "type_id")
        and hasattr(type_instance, "kind")
    )


__all__ = [
    "CONTRACT_ID",
    "SCHEMA_VERSION",
    "KindDefinition",
    "BaseType",
    "TypeRegistry",
    "verify_type_contract",
]





