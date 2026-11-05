"""Mathematical replay and protocol failure controls, beyond source custody."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from derivation.iso import IsoBudgetError, canonical, rename
from derivation.model import Regime
from portable_key import (
    U64_MAX,
    PortableKeyError,
    decode_portable_key_v1,
    encode_structural_key_v1,
    portable_key_v1,
)
from reproduce import python_replay


def test_mathematical_replay():
    result, _ = python_replay()
    assert result["context_count_cases"] == 35
    assert result["progress_regimes"] == 1436
    assert result["progress_targets"] == 3996


def test_portable_key_renaming_and_historical_mismatch():
    r = Regime(("a", "b"), (1,), frozenset({(0, (0,))}), frozenset(), frozenset())
    s = rename(r, (1, 0), (0,))
    assert portable_key_v1(r) == portable_key_v1(s)
    # The Python repr-ranked key labels the marked endpoint first. The
    # portable structural minimum labels it zero by the explicit protocol.
    assert canonical(r)[2] == ((0, (0,)),)
    assert portable_key_v1(r).startswith(b"GENESIS-KEY\x00\x01")
    with pytest.raises(IsoBudgetError):
        portable_key_v1(r, budget=0)
    too_large = Regime(tuple(map(str, range(9))), (), frozenset(), frozenset(), frozenset())
    with pytest.raises(IsoBudgetError):
        portable_key_v1(too_large)


def test_all_vendored_source_bytes_are_pinned():
    for name in ["mechanization_sources.json", "rust_sources.json"]:
        manifest = json.loads((ROOT / "manifests" / name).read_text(encoding="utf-8"))
        for item in manifest["files"]:
            path = ROOT / item["path"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], item["path"]


def test_empty_regime_wire_vector():
    r = Regime((), (), frozenset(), frozenset(), frozenset())
    assert portable_key_v1(r) == b"GENESIS-KEY\x00\x01" + bytes(40)


@pytest.mark.parametrize("r", [
    Regime((), (0,), frozenset(), frozenset(), frozenset()),
    Regime((), (2**64,), frozenset(), frozenset(), frozenset()),
    Regime(("a",), (1,), frozenset({(0, (1,))}), frozenset(), frozenset()),
    Regime(("a",), (1,), frozenset({(1, (0,))}), frozenset(), frozenset()),
    Regime(("a",), (1,), frozenset({(0, ())}), frozenset(), frozenset()),
    Regime(("a",), (), frozenset(), frozenset({0}), frozenset()),
    Regime(("a", "b"), (), frozenset(), frozenset(), frozenset({(1, 0)})),
    Regime(("a", "b"), (), frozenset(), frozenset(), frozenset({(0, 2)})),
])
def test_portable_key_rejects_invalid_domain(r):
    with pytest.raises(PortableKeyError):
        portable_key_v1(r)


def test_wire_maximum_word_and_bounded_budget_failure():
    key = (U64_MAX, (U64_MAX,), (), (), ())
    assert decode_portable_key_v1(encode_structural_key_v1(key)) == key
    huge = Regime(tuple(map(str, range(5000))), (), frozenset(), frozenset(), frozenset())
    with pytest.raises(IsoBudgetError):
        portable_key_v1(huge)
    with pytest.raises(IsoBudgetError):
        portable_key_v1(huge, U64_MAX)
    for budget in (-1, 2**64, True):
        with pytest.raises(PortableKeyError):
            portable_key_v1(Regime((), (), frozenset(), frozenset(), frozenset()), budget)
    with pytest.raises(IsoBudgetError):
        portable_key_v1(Regime((), (), frozenset(), frozenset(), frozenset()), 0)
    for data in ("GENESIS-KEY", bytearray(b"GENESIS-KEY")):
        with pytest.raises(PortableKeyError):
            decode_portable_key_v1(data)
    mixed = Regime(("a",), (1,), frozenset(), frozenset({0, "x"}), frozenset())
    with pytest.raises(PortableKeyError):
        portable_key_v1(mixed)


@pytest.mark.parametrize("data,target,swap", [
    (("a", "b"), (0, 1), (1, 0)),
    (("initial", "a", "b"), (1, 2), (0, 2, 1)),
])
def test_unordered_requirement_identifies_unary_endpoint_responses(data, target, swap):
    left = Regime(data, (1,), frozenset({(0, (target[0],))}), frozenset(), frozenset({target}))
    right = Regime(data, (1,), frozenset({(0, (target[1],))}), frozenset(), frozenset({target}))
    assert rename(left, swap, (0,)).reqs == right.reqs
    assert rename(left, swap, (0,)).insts == right.insts
    assert portable_key_v1(left) == portable_key_v1(right)
