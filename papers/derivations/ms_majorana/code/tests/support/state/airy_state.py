from __future__ import annotations

import math
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ComplexScalarV1:
    """Canonical finite complex scalar encoded as two normalized float hexes."""

    real_hex: str
    imag_hex: str

    def __post_init__(self) -> None:
        for label, encoded in (
            ("real_hex", self.real_hex),
            ("imag_hex", self.imag_hex),
        ):
            if type(encoded) is not str:
                raise TypeError(f"{label} must be an exact string")
            try:
                value = float.fromhex(encoded)
            except (ValueError, OverflowError) as exc:
                raise ValueError(f"{label} is not a float-hex value") from exc
            if not math.isfinite(value):
                raise ValueError(f"{label} must encode a finite float")
            if value.hex() != encoded:
                raise ValueError(f"{label} must use normalized float.hex encoding")

    @classmethod
    def from_complex(cls, value: complex) -> "ComplexScalarV1":
        if type(value) is not complex:
            raise TypeError("complex scalar input must be an exact complex value")
        if not math.isfinite(value.real) or not math.isfinite(value.imag):
            raise ValueError("complex scalar components must be finite")
        return cls(value.real.hex(), value.imag.hex())

    def to_complex(self) -> complex:
        return complex(float.fromhex(self.real_hex), float.fromhex(self.imag_hex))

# Delaying import to avoid circular dependency
# from omega_engine.crates.carrier.airy_carrier import AirySeedSlotV1
def _get_AirySeedSlotV1():
    from omega_engine.crates.carrier.airy_carrier import AirySeedSlotV1
    return AirySeedSlotV1


@dataclass(frozen=True, slots=True)
class AiryCriticalStateV1:
    """Five labeled values; duplicate roots remain distinct carrier slots."""

    slots: tuple[Any, ...]  # Any is used here to avoid typing circular dependency issues

    def __post_init__(self) -> None:
        if type(self.slots) is not tuple or len(self.slots) != 5:
            raise ValueError("Airy critical state requires exactly five slots")
        AirySeedSlotV1 = _get_AirySeedSlotV1()
        if any(type(slot) is not AirySeedSlotV1 for slot in self.slots):
            raise TypeError("Airy critical state slots must be AirySeedSlotV1")
        slot_ids = tuple(slot.slot_id for slot in self.slots)
        if len(set(slot_ids)) != len(slot_ids):
            raise ValueError("Airy critical state slot ids must be unique")

    @classmethod
    def from_complex_values(
        cls,
        slot_ids: tuple[str, ...],
        values: tuple[complex, ...],
    ) -> "AiryCriticalStateV1":
        if type(slot_ids) is not tuple or type(values) is not tuple:
            raise TypeError("Airy slot ids and values must be exact tuples")
        if len(slot_ids) != len(values):
            raise ValueError("Airy slot ids and values must have equal length")
        AirySeedSlotV1 = _get_AirySeedSlotV1()
        return cls(
            tuple(
                AirySeedSlotV1(slot_id, ComplexScalarV1.from_complex(value))
                for slot_id, value in zip(slot_ids, values)
            )
        )

    @property
    def slot_ids(self) -> tuple[str, ...]:
        return tuple(slot.slot_id for slot in self.slots)

    def complex_values(self) -> tuple[complex, ...]:
        return tuple(slot.value.to_complex() for slot in self.slots)
