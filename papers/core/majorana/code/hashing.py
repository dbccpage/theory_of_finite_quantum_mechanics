"""Deterministic hashing for carriers/matrices/weights (port of Rust ``hashing``).

Uses SHA-256 over a canonical textual encoding so that equal inputs always
produce equal digests and different inputs differ -- matching the determinism
guarantees the Rust manifests rely on.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Sequence

from .qmatrix import QMatrix


class Hash32:
    __slots__ = ("digest",)

    def __init__(self, digest: bytes):
        if len(digest) != 32:
            raise ValueError("Hash32 requires 32 bytes")
        self.digest = digest

    @property
    def is_zero(self) -> bool:
        return self.digest == b"\x00" * 32

    def hex(self) -> str:
        return self.digest.hex()

    def __eq__(self, other) -> bool:
        return isinstance(other, Hash32) and self.digest == other.digest

    def __hash__(self) -> int:
        return hash(self.digest)


def hash_bytes(*parts: bytes) -> Hash32:
    h = hashlib.sha256()
    for p in parts:
        h.update(len(p).to_bytes(8, "little"))
        h.update(p)
    return Hash32(h.digest())


def _frac_bytes(seq: Sequence) -> bytes:
    return ";".join(f"{x.numerator}/{x.denominator}" for x in seq).encode("utf-8")


def hash_matrix(m: QMatrix) -> Hash32:
    header = f"{m.rows}x{m.cols}:".encode("utf-8")
    return hash_bytes(header, _frac_bytes(m.as_flat()))


def hash_weights(weights: Sequence) -> Hash32:
    return hash_bytes(b"weights:", _frac_bytes(weights))


def hash_text(text: str) -> Hash32:
    return hash_bytes(text.encode("utf-8"))



try:
    import blake3 as _blake3
except ImportError:
    _blake3 = None


def signed_bytes_le(value: int) -> bytes:
    """``num_bigint::BigInt::to_signed_bytes_le`` — minimal two's-complement LE.

    Minimal means the fewest bytes ``L`` with ``-2^(8L-1) <= value < 2^(8L-1)``.
    Zero is one byte, not zero bytes. Getting this wrong is undetectable without
    the golden vectors: ``128`` needs two bytes (``80 00``) because ``0x80`` alone
    reads as ``-128``, while ``-128`` needs one.
    """
    length = 1
    while not (-(1 << (8 * length - 1)) <= value < (1 << (8 * length - 1))):
        length += 1
    return value.to_bytes(length, "little", signed=True)


def _u64(n: int) -> bytes:
    return int(n).to_bytes(8, "little", signed=False)


def _hash_bigint(hasher, value: int) -> None:
    """``len:u64 || signed-le-bytes``.

    The length prefix is load-bearing: ``BigInt`` has no fixed width, so bare
    concatenation is not injective. ``1/515`` and ``769/2`` both serialise to
    ``01 03 02`` unframed, and both appear in the golden vectors so an
    implementation that drops the prefix cannot pass.
    """
    raw = signed_bytes_le(value)
    hasher.update(_u64(len(raw)))
    hasher.update(raw)


def hash_rational(hasher, numer: int, denom: int) -> None:
    """One rational, numerator then denominator, each framed."""
    _hash_bigint(hasher, numer)
    _hash_bigint(hasher, denom)


def hash_matrix_v2(rows: int, cols: int, data: Sequence) -> Hash32:
    """Row-major ``BasicMatrix<BigRational>``. ``data`` is ``(numer, denom)`` pairs."""
    if _blake3 is None:
        raise RuntimeError("blake3 package is required for hash_matrix_v2 but not installed.")
    h = _blake3.blake3()
    h.update(b"MSSN.BasicMatrix<BigRational>.v2")
    h.update(_u64(rows))
    h.update(_u64(cols))
    for numer, denom in data:
        hash_rational(h, numer, denom)
    return Hash32(h.digest())


def hash_weights_v2(weights: Sequence) -> Hash32:
    if _blake3 is None:
        raise RuntimeError("blake3 package is required for hash_weights_v2 but not installed.")
    h = _blake3.blake3()
    h.update(b"MSSN.CarrierWeights<BigRational>.v2")
    h.update(_u64(len(weights)))
    for numer, denom in weights:
        hash_rational(h, numer, denom)
    return Hash32(h.digest())


def hash_provenance_v2(verification_source: str) -> Hash32:
    if _blake3 is None:
        raise RuntimeError("blake3 package is required for hash_provenance_v2 but not installed.")
    h = _blake3.blake3()
    h.update(b"MSSN.TheoremProvenance.v1")
    h.update(verification_source.encode("utf-8"))
    return Hash32(h.digest())


def hash_cochain_witness_v2(d0_shape, d1_shape, provenance_hash: Hash32) -> Hash32:
    if _blake3 is None:
        raise RuntimeError("blake3 package is required for hash_cochain_witness_v2 but not installed.")
    h = _blake3.blake3()
    h.update(b"MSSN.CochainComplexWitness.v1")
    for extent in (d0_shape[0], d0_shape[1], d1_shape[0], d1_shape[1]):
        h.update(_u64(extent))
    h.update(provenance_hash.digest)
    return Hash32(h.digest())


CARRIER_MANIFEST_VERSION = 2
COEFFICIENT_DOMAIN = "Q"
COEFFICIENT_REPRESENTATION = "BigRational"


def hash_carrier_manifest_v2(
    c0_dim: int,
    c1_dim: int,
    c2_dim: int,
    d0_hash: Hash32,
    d1_hash: Hash32,
    weights_hash: Hash32,
) -> Hash32:
    """Binds dimensions, boundary maps, weights, domain and representation.

    Domain and representation are folded in SEPARATELY, matching the Rust split:
    recording only one of the two is what made the v1 receipt false after the
    widening.
    """
    if _blake3 is None:
        raise RuntimeError("blake3 package is required for hash_carrier_manifest_v2 but not installed.")
    h = _blake3.blake3()
    h.update(b"OMEGA.CarrierManifest.v2")
    h.update(CARRIER_MANIFEST_VERSION.to_bytes(4, "little", signed=False))
    h.update(d0_hash.digest)
    h.update(d1_hash.digest)
    h.update(weights_hash.digest)
    for extent in (c0_dim, c1_dim, c2_dim):
        h.update(_u64(extent))
    h.update(COEFFICIENT_DOMAIN.encode("utf-8"))
    h.update(COEFFICIENT_REPRESENTATION.encode("utf-8"))
    return Hash32(h.digest())


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


@dataclass(init=False)
class Hash256(_RustSurfaceObject):
    """Structural mirror of Rust ``Hash256``."""

    hex: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("hex",)
        if len(args) > len(names):
            raise TypeError("Hash256 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def as_bytes(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``as_bytes``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::as_bytes"
    )


def to_hex(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``to_hex``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::to_hex"
    )


def hash_vector(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_vector``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::hash_vector"
    )


def hash_chain_complex_manifest(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_chain_complex_manifest``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::hash_chain_complex_manifest"
    )


def hash_cochain_complex_manifest(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_cochain_complex_manifest``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::hash_cochain_complex_manifest"
    )


def hash_carrier_manifest(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_carrier_manifest``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::hash_carrier_manifest"
    )


def hash_provenance(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_provenance``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::hash_provenance"
    )


def hash_cochain_witness(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_cochain_witness``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/hashing.rs::hash_cochain_witness"
    )




