from __future__ import annotations
"""Carrier manifest v2 -- a real port of ``carrier_manifest.rs``, digest-identical.

Emits the SAME BLAKE3 digests as the Rust implementation for the same carrier.
That equality is not asserted, it is pinned: ``tests/golden/carrier_manifest_v2.json``
at the repo root is read by both this rail's ``test_manifest_v2_parity`` and Rust's
``golden_carrier_manifest_v2``, so a drift on either side fails the other's test.

This file previously carried ``ADVISORY_SCHEMA`` and declared itself incomparable
with Rust, because it used SHA-256 over a decimal-text encoding and recorded no
version, domain, or representation. That was the honest description of what it was.
It is no longer what it is: ``blake3`` is now a declared dependency of the rail and
the encoding is the framed binary one ADR-001 requires, so the schema marker is
gone rather than kept as a comforting label on an object that outgrew it.

Rust remains the authority. This produces manifests; it deliberately does NOT
parse them. Rust's ``CarrierManifest::from_slice`` verifies version, domain,
representation, and recomputes ``carrier_hash`` before a record is accepted, and
duplicating that trust boundary in a second language would create a second place
for it to be got wrong.

AuthorityEffect: None.
"""


from dataclasses import dataclass

from .carrier import Carrier
from .hashing import (
    CARRIER_MANIFEST_VERSION,
    COEFFICIENT_DOMAIN,
    COEFFICIENT_REPRESENTATION,
    Hash32,
    hash_carrier_manifest_v2,
    hash_cochain_witness_v2,
    hash_matrix_v2,
    hash_provenance_v2,
    hash_weights_v2,
)


def _pairs(values):
    """``(numerator, denominator)`` for each exact rational, as Python ints.

    Accepts anything exposing ``numerator``/``denominator`` (``fractions.Fraction``
    and this rail's ``Q`` both do). Floats are refused rather than rounded: a float
    coefficient cannot produce a digest Rust would agree with, and silently hashing
    one would be exactly the kind of quiet degradation ADR-001 forbids.
    """
    out = []
    for v in values:
        if isinstance(v, float):
            raise TypeError(
                "float coefficient in a v2 manifest: the exact domain is Q and a "
                "float cannot be hashed to a digest Rust would reproduce"
            )
        if isinstance(v, int):
            out.append((v, 1))
            continue
        try:
            out.append((int(v.numerator), int(v.denominator)))
        except AttributeError as exc:  
            raise TypeError(f"not an exact rational: {v!r}") from exc
    return out


@dataclass(frozen=True)
class CarrierManifest:
    """Deterministic manifest of a carrier. Digest-identical to Rust v2."""

    manifest_version: int
    carrier_hash: Hash32
    d0_hash: Hash32
    d1_hash: Hash32
    weights_hash: Hash32
    witness_hash: Hash32
    provenance_hash: Hash32
    coefficient_domain: str
    coefficient_representation: str
    c0_dim: int
    c1_dim: int
    c2_dim: int
    rank_d0: int
    dim_q1: int
    dim_h1: int

    @classmethod
    def from_carrier(cls, carrier: Carrier) -> "CarrierManifest":
        d0, d1 = carrier.d0(), carrier.d1()
        d0_hash = hash_matrix_v2(d0.rows, d0.cols, _pairs(d0.as_flat()))
        d1_hash = hash_matrix_v2(d1.rows, d1.cols, _pairs(d1.as_flat()))
        weights_hash = hash_weights_v2(_pairs(carrier.weights()))
        provenance_hash = hash_provenance_v2(carrier.provenance().verification_source)
        witness_hash = hash_cochain_witness_v2(
            (d0.rows, d0.cols), (d1.rows, d1.cols), provenance_hash
        )
        return cls(
            manifest_version=CARRIER_MANIFEST_VERSION,
            carrier_hash=hash_carrier_manifest_v2(
                carrier.c0_dim(),
                carrier.c1_dim(),
                carrier.c2_dim(),
                d0_hash,
                d1_hash,
                weights_hash,
            ),
            d0_hash=d0_hash,
            d1_hash=d1_hash,
            weights_hash=weights_hash,
            witness_hash=witness_hash,
            provenance_hash=provenance_hash,
            coefficient_domain=COEFFICIENT_DOMAIN,
            coefficient_representation=COEFFICIENT_REPRESENTATION,
            c0_dim=carrier.c0_dim(),
            c1_dim=carrier.c1_dim(),
            c2_dim=carrier.c2_dim(),
            rank_d0=carrier.rank_d0(),
            dim_q1=carrier.dim_q1(),
            dim_h1=carrier.dim_h1(),
        )


from dataclasses import dataclass  
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


def from_carrier(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``from_carrier``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/carrier_manifest.rs::from_carrier"
    )




