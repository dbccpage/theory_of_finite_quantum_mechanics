from __future__ import annotations
"""Carrier-manifest v2 parity with Rust, against SHARED golden vectors.

This test and ``omega_engine/crates/omega_homology/tests/golden_carrier_manifest_v2.rs``
read the SAME file: ``tests/golden/carrier_manifest_v2.json`` at the repo root.
That is what makes this a parity check rather than two suites that happen to agree
today -- if either implementation drifts, one of the two tests fails.

Rust is the authority. The fixture is regenerated only by the Rust test under
``OMEGA_REGEN_GOLDEN=1``; nothing here can rewrite it, so a Python regression
cannot quietly move the goalposts.
"""


import json
from pathlib import Path

import pytest

from omega_engine.crates.homology_theory import hashing as h

# .../anomalon/math/omega_homology/tests -> 7 ancestors up to the
# repo root, where tests/golden/ is shared with the Rust suite.
def _find_golden() -> Path:
    cur = Path(__file__).resolve().parent
    for _ in range(10):
        target = cur / "tests" / "golden" / "carrier_manifest_v2.json"
        if target.exists():
            return target
        if cur.parent == cur:
            break
        cur = cur.parent
    return cur / "tests" / "golden" / "carrier_manifest_v2.json"

GOLDEN = _find_golden()


def _fixture() -> dict:
    if not GOLDEN.exists():  # pragma: no cover - configuration failure
        pytest.fail(f"shared golden fixture missing at {GOLDEN}")
    return json.loads(GOLDEN.read_text(encoding="utf-8"))


def _pairs(raw) -> list:
    """Fixture rationals are decimal STRINGS so values beyond i64 survive JSON."""
    return [(int(n), int(d)) for n, d in raw]


def _rational_digest(numer: int, denom: int) -> str:
    import blake3

    hasher = blake3.blake3()
    h.hash_rational(hasher, numer, denom)
    return hasher.digest().hex()


def test_the_fixture_declares_expectations():
    """A fixture with an empty ``expected`` block would make every test below
    vacuously pass, so the premise is checked first."""
    expected = _fixture()["expected"]
    assert expected, "the fixture has no expectations - regenerate it from Rust"
    for key in (
        "rationals",
        "d0_hash",
        "d1_hash",
        "weights_hash",
        "provenance_hash",
        "witness_hash",
        "carrier_hash",
    ):
        assert key in expected, f"the fixture does not pin {key}"


def test_rational_framing_matches_rust():
    fixture = _fixture()
    pairs = _pairs(fixture["inputs"]["rationals"])
    expected = fixture["expected"]["rationals"]
    assert len(pairs) == len(expected)

    for (numer, denom), want in zip(pairs, expected):
        got = _rational_digest(numer, denom)
        assert got == want, f"{numer}/{denom}: python {got} != rust {want}"


def test_the_unframed_collision_pair_is_separated():
    """1/515 and 769/2 both serialise to ``01 03 02`` without the length prefixes.

    Their presence in the fixture is what stops a Python implementation that
    forgot the framing from passing, so the collision is asserted here rather
    than assumed.
    """
    unframed = lambda n, d: h.signed_bytes_le(n) + h.signed_bytes_le(d)  # noqa: E731
    assert unframed(1, 515) == unframed(769, 2), (
        "premise broken - this pair must collide"
    )

    assert _rational_digest(1, 515) != _rational_digest(769, 2)


def test_matrix_weights_provenance_and_witness_match_rust():
    fixture = _fixture()
    inputs, expected = fixture["inputs"], fixture["expected"]

    d0, d1 = inputs["d0"], inputs["d1"]
    assert (
        h.hash_matrix_v2(d0["rows"], d0["cols"], _pairs(d0["data"])).hex()
        == expected["d0_hash"]
    )
    assert (
        h.hash_matrix_v2(d1["rows"], d1["cols"], _pairs(d1["data"])).hex()
        == expected["d1_hash"]
    )
    assert (
        h.hash_weights_v2(_pairs(inputs["weights"])).hex() == expected["weights_hash"]
    )

    provenance = h.hash_provenance_v2(inputs["provenance"])
    assert provenance.hex() == expected["provenance_hash"]
    assert (
        h.hash_cochain_witness_v2(
            (d0["rows"], d0["cols"]), (d1["rows"], d1["cols"]), provenance
        ).hex()
        == expected["witness_hash"]
    )


def test_carrier_hash_matches_rust():
    fixture = _fixture()
    inputs, expected = fixture["inputs"], fixture["expected"]
    d0, d1 = inputs["d0"], inputs["d1"]

    got = h.hash_carrier_manifest_v2(
        inputs["c0_dim"],
        inputs["c1_dim"],
        inputs["c2_dim"],
        h.hash_matrix_v2(d0["rows"], d0["cols"], _pairs(d0["data"])),
        h.hash_matrix_v2(d1["rows"], d1["cols"], _pairs(d1["data"])),
        h.hash_weights_v2(_pairs(inputs["weights"])),
    )
    assert got.hex() == expected["carrier_hash"]


def test_domain_and_representation_constants_match_rust():
    expected = _fixture()["expected"]
    assert h.COEFFICIENT_DOMAIN == expected["coefficient_domain"]
    assert h.COEFFICIENT_REPRESENTATION == expected["coefficient_representation"]
    assert h.CARRIER_MANIFEST_VERSION == 2
    assert h.COEFFICIENT_DOMAIN != h.COEFFICIENT_REPRESENTATION


def test_signed_byte_encoding_matches_num_bigint_at_the_boundaries():
    """``to_signed_bytes_le`` is minimal two's complement, and the boundaries are
    where a plausible-looking implementation goes wrong.

    128 needs two bytes because ``0x80`` alone reads as -128; -128 needs one.
    Zero is one byte, not zero.
    """
    cases = {
        0: b"\x00",
        1: b"\x01",
        -1: b"\xff",
        127: b"\x7f",
        128: b"\x80\x00",
        -128: b"\x80",
        -129: b"\x7f\xff",
        255: b"\xff\x00",
        256: b"\x00\x01",
    }
    for value, want in cases.items():
        assert h.signed_bytes_le(value) == want, (
            f"{value}: {h.signed_bytes_le(value)!r}"
        )


def test_coefficients_beyond_i64_round_trip():
    """The point of ADR-001: a value no fixed-width lane could carry."""
    huge = 170141183460469231731687303715884105727
    assert huge > 2**63 - 1, "premise: the value must exceed i64"
    assert int.from_bytes(h.signed_bytes_le(huge), "little", signed=True) == huge
    # And it is one of the fixture's pinned rationals, so Rust agrees on its digest.
    pairs = _pairs(_fixture()["inputs"]["rationals"])
    assert (huge, 1) in pairs



