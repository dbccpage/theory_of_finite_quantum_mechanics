from __future__ import annotations

from dataclasses import dataclass

from omega_engine.crates.state.airy_state import ComplexScalarV1

def _is_sha256(value: any) -> bool:
    return bool(
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )

def _require_sha256(value: any, label: str) -> str:
    if not _is_sha256(value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")
    return value

@dataclass(frozen=True, slots=True)
class AirySeedSlotV1:
    slot_id: str
    value: ComplexScalarV1

    def __post_init__(self) -> None:
        if type(self.slot_id) is not str or not self.slot_id:
            raise ValueError("Airy slot id must be a non-empty exact string")
        if type(self.value) is not ComplexScalarV1:
            raise TypeError("Airy slot value must be ComplexScalarV1")

@dataclass(frozen=True, slots=True)
class AiryCriticalCarrierV1:
    lambda_scalar: ComplexScalarV1
    slot_ids: tuple[str, ...]
    research_parent_event_id: str
    source_digest: str

    @property
    def carrier_id(self) -> str:
        return "witten-airy-critical-five-slot-v1"

    def __post_init__(self) -> None:
        if type(self.lambda_scalar) is not ComplexScalarV1:
            raise TypeError("Airy carrier lambda must be ComplexScalarV1")
        if self.lambda_scalar.to_complex() == 0.0j:
            raise ValueError("Airy critical carrier requires nonzero lambda")
        if type(self.slot_ids) is not tuple or len(self.slot_ids) != 5:
            raise ValueError("Airy carrier requires exactly five slot ids")
        if any(type(slot_id) is not str or not slot_id for slot_id in self.slot_ids):
            raise ValueError("Airy carrier slot ids must be non-empty exact strings")
        if len(set(self.slot_ids)) != len(self.slot_ids):
            raise ValueError("Airy carrier slot ids must be unique")
        _require_sha256(
            self.research_parent_event_id,
            "research_parent_event_id",
        )
        _require_sha256(self.source_digest, "source_digest")
