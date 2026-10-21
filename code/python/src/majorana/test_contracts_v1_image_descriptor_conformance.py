from __future__ import annotations
from pydantic import ConfigDict
"""Python mirror of the Rust omega_contracts source file.

This module is generated as an executable Python QA surface for the
leading-edge omega_engine_py stack. It preserves Rust provenance and
declared symbols without minting authority or pretending that every
Rust implementation has already been semantically hand-ported.

Rust source: tests/v1_image_descriptor_conformance.rs
Rust SHA-256: c199cd251ba8fac5ee2109f2b084e04ab6b1a3b4f1d16bbab8b4face6599272e
"""


from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Any, Mapping, Sequence

RUST_SOURCE_PATH = "tests/v1_image_descriptor_conformance.rs"
RUST_SOURCE_SHA256 = "c199cd251ba8fac5ee2109f2b084e04ab6b1a3b4f1d16bbab8b4face6599272e"
PORT_STATUS = "mechanical_python_mirror"


class RustPortPending(NotImplementedError):
    """Raised when a Rust implementation body still needs a semantic Python port."""

    pass


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class RustDeclaration:
    kind: str
    name: str
    detail: Mapping[str, Any] = field(default_factory=dict)


def collect_contracts(*args: Any, **kwargs: Any) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_image_descriptor_conformance.rs::collect_contracts"
    )


def existing_public_image_names_still_point_at_expected_contracts(
    *args: Any, **kwargs: Any
) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_image_descriptor_conformance.rs::existing_public_image_names_still_point_at_expected_contracts"
    )


def existing_public_image_type_bindings_are_consistent(
    *args: Any, **kwargs: Any
) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_image_descriptor_conformance.rs::existing_public_image_type_bindings_are_consistent"
    )


def generated_image_catalog_covers_every_v1_rust_binding(
    *args: Any, **kwargs: Any
) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_image_descriptor_conformance.rs::generated_image_catalog_covers_every_v1_rust_binding"
    )


def generated_image_descriptors_match_yaml_projection(*args: Any, **kwargs: Any) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_image_descriptor_conformance.rs::generated_image_descriptors_match_yaml_projection"
    )


def v1_contracts_by_id(*args: Any, **kwargs: Any) -> Any:
    raise RustPortPending(
        "Semantic Python port required for tests/v1_image_descriptor_conformance.rs::v1_contracts_by_id"
    )


RUST_DECLARATIONS = [
    {"kind": "function", "name": "collect_contracts", "detail": {}},
    {
        "kind": "function",
        "name": "existing_public_image_names_still_point_at_expected_contracts",
        "detail": {},
    },
    {
        "kind": "function",
        "name": "existing_public_image_type_bindings_are_consistent",
        "detail": {},
    },
    {
        "kind": "function",
        "name": "generated_image_catalog_covers_every_v1_rust_binding",
        "detail": {},
    },
    {
        "kind": "function",
        "name": "generated_image_descriptors_match_yaml_projection",
        "detail": {},
    },
    {"kind": "function", "name": "v1_contracts_by_id", "detail": {}},
]


def declarations() -> Sequence[RustDeclaration]:
    return tuple(RustDeclaration(**item) for item in RUST_DECLARATIONS)


def source_identity() -> dict[str, str]:
    return {
        "path": RUST_SOURCE_PATH,
        "sha256": RUST_SOURCE_SHA256,
        "status": PORT_STATUS,
    }





