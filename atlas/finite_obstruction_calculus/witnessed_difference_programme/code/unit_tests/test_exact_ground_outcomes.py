from dataclasses import dataclass
from fractions import Fraction

import pytest
from witnessed_difference.exact import as_fraction, canonical_data, l1
from witnessed_difference.ground import (
    Difference,
    odd_cycle_frustrated,
    parity,
    primitive_difference,
    triangle_boundary,
    triangle_identity,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.witness import payload_digest


@dataclass(frozen=True)
class Sample:
    count: Fraction


def test_typed_outcomes_never_mint_authority() -> None:
    accepted = Accepted(3)
    refused = Refused(RefusalCode.INVALID_INPUT, "bad")
    assert accepted.authority_effect is AuthorityEffect.NONE
    assert refused.authority_effect is AuthorityEffect.NONE
    assert refused.detail == "bad"
    with pytest.raises(ValueError, match="authority effect"):
        Accepted(3, "promoted")
    with pytest.raises(ValueError, match="authority effect"):
        Refused(RefusalCode.INVALID_INPUT, "bad", "promoted")


@pytest.mark.parametrize(
    ("value", "expected"),
    [(3, Fraction(3)), ("3/4", Fraction(3, 4)), (Fraction(2, 5), Fraction(2, 5))],
)
def test_as_fraction_accepts_only_exact_scalars(value, expected) -> None:
    assert as_fraction(value) == expected


@pytest.mark.parametrize("value", [True, False, 1.25, object()])
def test_as_fraction_refuses_inexact_or_unsupported_values(value) -> None:
    with pytest.raises(TypeError, match="exact|unsupported"):
        as_fraction(value)


def test_l1_and_canonical_data_cover_supported_shapes() -> None:
    assert l1((Fraction(-2), Fraction(1, 2))) == Fraction(5, 2)
    value = {
        "dataclass": Sample(Fraction(2, 3)),
        "enum": Difference.DIFFERENT,
        "bytes": b"ab",
        "complex": 1 + 2j,
        "set": {3, 1},
        "sequence": (None, "x", True),
    }
    canonical = canonical_data(value)
    assert canonical["__wdp_type__"] == "mapping"
    items = dict(canonical["items"])
    assert items["dataclass"]["__wdp_type__"] == "dataclass"
    assert items["dataclass"]["fields"] == [
        ["count", {"__wdp_type__": "fraction", "denominator": 3, "numerator": 2}]
    ]
    assert items["enum"]["__wdp_type__"] == "enum"
    assert items["enum"]["value"] == 1
    assert items["bytes"] == {"__wdp_type__": "bytes", "hex": "6162"}
    assert items["complex"]["__wdp_type__"] == "complex"
    assert items["set"] == {"__wdp_type__": "set", "items": [1, 3]}
    assert items["sequence"] == {
        "__wdp_type__": "tuple",
        "items": [None, "x", True],
    }


def test_canonical_type_envelopes_prevent_semantic_substitution() -> None:
    collisions = (
        (Fraction(1, 2), {"denominator": 2, "numerator": 1}),
        (b"ab", {"hex": "6162"}),
        (1 + 2j, {"imag": "2", "real": "1"}),
        (Difference.DIFFERENT, 1),
        ((1, 2), [1, 2]),
        ({1, 2}, [1, 2]),
        (Sample(Fraction(1, 2)), {"count": Fraction(1, 2)}),
    )
    for left, right in collisions:
        assert canonical_data(left) != canonical_data(right)
        assert payload_digest(left) != payload_digest(right)
    with pytest.raises(TypeError, match="finite components"):
        canonical_data(complex(float("inf"), 0))


def test_canonical_data_refuses_opaque_objects() -> None:
    with pytest.raises(TypeError, match="unsupported canonical"):
        canonical_data(object())


def test_canonical_data_refuses_key_coercion_collisions() -> None:
    with pytest.raises(TypeError, match="string keys"):
        canonical_data({1: "integer key", "1": "string key"})


def test_primitive_difference_and_triangle_identity() -> None:
    assert primitive_difference("a", "a") is Difference.SAME
    assert primitive_difference("a", "b") is Difference.DIFFERENT
    assert triangle_boundary("a", "b", "a") == (
        Difference.DIFFERENT,
        Difference.DIFFERENT,
        Difference.SAME,
    )
    assert all(triangle_identity(a, b, c) for a in range(2) for b in range(2) for c in range(2))


def test_parity_and_frustration_are_explicit() -> None:
    assert parity(()) is Difference.SAME
    assert parity((1, 0, Difference.DIFFERENT)) is Difference.SAME
    assert odd_cycle_frustrated((1, 1, 1))
    assert not odd_cycle_frustrated((1, 1, 0))
    with pytest.raises(ValueError, match="zero/one"):
        parity((2,))
# Executable finite evidence; AuthorityEffect: None.
