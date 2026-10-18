from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/residual_receipt.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


from pydantic.dataclasses import dataclass
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


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ResidualReceipt(_RustSurfaceObject):
    """Structural mirror of Rust ``ResidualReceipt``."""

    packet_id: Any = None
    closure_discipline: Any = None
    residual_class: Any = None
    transport_receipts: Any = None
    repair_attempts: Any = None
    terminal: Any = None
    authority_boundary: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "packet_id",
            "closure_discipline",
            "residual_class",
            "transport_receipts",
            "repair_attempts",
            "terminal",
            "authority_boundary",
        )
        if len(args) > len(names):
            raise TypeError("ResidualReceipt received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ResidualTransitionLedger(_RustSurfaceObject):
    """Structural mirror of Rust ``ResidualTransitionLedger``."""

    receipt: Any = None
    transitions: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("receipt", "transitions")
        if len(args) > len(names):
            raise TypeError(
                "ResidualTransitionLedger received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)




