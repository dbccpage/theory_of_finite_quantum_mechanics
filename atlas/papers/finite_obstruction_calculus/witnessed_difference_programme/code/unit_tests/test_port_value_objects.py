# Executable finite evidence; AuthorityEffect: None.
"""Exact-type equality, hashing and keyed reads of the port value objects."""

from __future__ import annotations

from fractions import Fraction

import pytest

from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.ports import (
    DigestReceipt,
    GenesisDescentRequest,
    GenesisDescentResult,
    L1Solution,
    ObstructionSolveRequest,
    QuotientCertificate,
    QuotientVerificationReceipt,
    WdpObstructionSolution,
)
from witnessed_difference.rop import Refusal

EDGE = ("a", "b")
HALF = Fraction(1, 2)

INSTANCES = [
    L1Solution(HALF, {"a": Fraction(0)}, {EDGE: HALF}, {EDGE: Fraction(1)}, False, 3),
    ObstructionSolveRequest(("a", "b"), (EDGE,), {EDGE: HALF}, {EDGE: Fraction(1)}),
    GenesisDescentRequest(((0,),), 0, ((0,),), (((1,),),), 0, (0,), ((0,),)),
    GenesisDescentResult("collision", (0,), "c", (0, 1), (1, 0)),
    QuotientCertificate(HALF, {"a": Fraction(0)}, {EDGE: HALF}, {EDGE: Fraction(1)}, False),
    QuotientVerificationReceipt(True, HALF, True, True),
    DigestReceipt("r", "s", "b", "e"),
    WdpObstructionSolution(HALF, False, {"a": Fraction(0)}, {EDGE: HALF}, {EDGE: Fraction(1)}),
]


@pytest.mark.parametrize("value", INSTANCES, ids=lambda v: type(v).__name__)
def test_value_objects_compare_by_exact_type_and_hash_consistently(value: object) -> None:
    twin = type(value)(**{f: getattr(value, f) for f in value.__dataclass_fields__})
    assert value == twin and hash(value) == hash(twin)
    assert value != object()
    assert value != "not a value object"


def test_l1_solution_keyed_reads() -> None:
    solution = INSTANCES[0]
    expected = {
        "phi1": HALF, "phi1_value": HALF, "potential": {"a": 0}, "residual": {EDGE: HALF},
        "dual": {EDGE: 1}, "is_exact": False, "iterations": 3,
        "authority_effect": "None", "backend": "rust",
    }
    for key, value in expected.items():
        assert solution[key] == value
    assert solution.get("missing", "fallback") == "fallback"


def test_genesis_result_keyed_reads_with_and_without_collisions() -> None:
    result = INSTANCES[3]
    assert [result[k] for k in ("kind", "prefix", "certificate", "collision_first",
                                "collision_second", "authority_effect", "backend")] == [
        "collision", [0], "c", [0, 1], [1, 0], "None", "rust"]
    bare = GenesisDescentResult("descends")
    assert bare["collision_first"] is None and bare["collision_second"] is None
    assert bare.get("nope") is None


def test_obstruction_solution_keyed_reads_and_absent_dual() -> None:
    solution = INSTANCES[-1]
    for key in ("phi1", "is_exact", "potential", "residual", "dual", "dual_witness",
                "backend", "authority_effect"):
        assert solution[key] is not None or key == "dual"
    assert solution.get("missing", 7) == 7
    no_dual = WdpObstructionSolution(HALF, False, {}, {})
    assert no_dual != solution and no_dual == WdpObstructionSolution(HALF, False, {}, {})
    assert hash(no_dual) == hash(WdpObstructionSolution(HALF, False, {}, {}))


def test_accepted_and_refused_follow_the_railway_shape() -> None:
    accepted = Accepted(5)
    assert accepted.is_ok and not accepted.is_err and accepted.unwrap() == 5
    with pytest.raises(ValueError, match="unwrap_err"):
        accepted.unwrap_err()
    refused = Refused(RefusalCode.NOT_EXACT, "residual is nonzero")
    assert refused.is_err and not refused.is_ok
    with pytest.raises(ValueError, match="cannot unwrap Refused"):
        refused.unwrap()
    refusal = refused.unwrap_err()
    assert isinstance(refusal, Refusal)
    assert refusal.code == "NOT_EXACT" and dict(refusal.details) == {"authority_effect": "None"}
    for factory in (lambda: Accepted(1, "granted"), lambda: Refused(RefusalCode.NO_RULE, "x", "y")):
        with pytest.raises(ValueError, match="authority effect"):
            factory()
    assert AuthorityEffect.NONE.value == "None"
