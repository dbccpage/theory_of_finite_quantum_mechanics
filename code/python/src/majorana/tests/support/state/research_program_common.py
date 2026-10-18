from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/research_program_common.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/research_program_common.rs
# Rust sha256: aba4ee6496b31666e82fea67b001f8e52ccea27c7fcdc2c4c141bfffa65fd9b0
# Structural parity only; no behavioral or authority claim.
from pydantic.dataclasses import dataclass
from enum import Enum
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
class ResearchProgramBoundaryV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ResearchProgramBoundaryV1``."""

    witnesses: Any = None
    evidence_ceiling: Any = None
    publication_permission: Any = None
    promotion_permission: Any = None
    gate_activated: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "witnesses",
            "evidence_ceiling",
            "publication_permission",
            "promotion_permission",
            "gate_activated",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "ResearchProgramBoundaryV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


ResearchProgramCommonError = Enum(
    "ResearchProgramCommonError",
    {
        "InvalidText": "InvalidText",
        "InvalidGitOid": "InvalidGitOid",
        "WriteSurfaceChanged": "WriteSurfaceChanged",
        "WitnessPlan": "WitnessPlan",
        "AuthorityExpansion": "AuthorityExpansion",
        "Json": "Json",
    },
    type=str,
)
ResearchProgramCommonError.__doc__ = (
    "Structural mirror of Rust ``ResearchProgramCommonError`` variants."
)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/research_program_common.rs::validate"
    )


# END GENERATED RUST SURFACE


