from __future__ import annotations
from pydantic import ConfigDict
"""Python mirror of the Rust omega_contracts source file.

This module is generated as an executable Python QA surface for the
leading-edge omega_engine_py stack. It preserves Rust provenance and
declared symbols without minting authority or pretending that every
Rust implementation has already been semantically hand-ported.

Rust source: tests/v1_core_lifts.rs
Rust SHA-256: 134ca0b3da80a620b9c09ad5bc113e2a92a4b9babbcc63e1f815a040c3f16630
"""


from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Any, Mapping, Sequence

RUST_SOURCE_PATH = "tests/v1_core_lifts.rs"
RUST_SOURCE_SHA256 = "134ca0b3da80a620b9c09ad5bc113e2a92a4b9babbcc63e1f815a040c3f16630"
PORT_STATUS = "mechanical_python_mirror"


class RustPortPending(NotImplementedError):
    """Raised when a Rust implementation body still needs a semantic Python port."""

    pass


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class RustDeclaration:
    kind: str
    name: str
    detail: Mapping[str, Any] = field(default_factory=dict)


def lift_license_loads_and_validates(*args: Any, **kwargs: Any) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_core_lifts.rs::lift_license_loads_and_validates"
    )


def lift_license_without_machinery_is_rejected_by_registry(
    *args: Any, **kwargs: Any
) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_core_lifts.rs::lift_license_without_machinery_is_rejected_by_registry"
    )


RUST_DECLARATIONS = [
    {"kind": "function", "name": "lift_license_loads_and_validates", "detail": {}},
    {
        "kind": "function",
        "name": "lift_license_without_machinery_is_rejected_by_registry",
        "detail": {},
    },
]


def declarations() -> Sequence[RustDeclaration]:
    return tuple(RustDeclaration(**item) for item in RUST_DECLARATIONS)


def source_identity() -> dict[str, str]:
    return {
        "path": RUST_SOURCE_PATH,
        "sha256": RUST_SOURCE_SHA256,
        "status": PORT_STATUS,
    }





