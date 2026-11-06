"""Exact representation and anti-forgery checks for the educational primitives."""

from __future__ import annotations

import importlib
import json
from dataclasses import FrozenInstanceError, dataclass, replace
from fractions import Fraction

import pytest

_PACKAGE = "omega_engine_education.documentation.001_genesis.primitives.code"
gp = importlib.import_module(_PACKAGE)
codec = importlib.import_module(f"{_PACKAGE}.canonical")
represented = importlib.import_module(f"{_PACKAGE}.represented_progress")
engine = importlib.import_module(f"{_PACKAGE}.derivation_engine")
traces = importlib.import_module(f"{_PACKAGE}.transition_and_trace")
trace_algebra = importlib.import_module(f"{_PACKAGE}.trace_algebra")


@pytest.mark.parametrize(
    "constructor,args",
    [
        (gp.Supply, (True,)),
        (gp.AdmitForm, (True,)),
        (gp.Impose, (False, 1)),
        (gp.Bounds, (True, 2)),
        (gp.PS, ()),
    ],
)
def test_exact_types_reject_bool_integer_confusion(constructor, args):
    if constructor is gp.PS:
        with pytest.raises(TypeError, match="REFUSED_SHAPE"):
            constructor(licensed=1)
    else:
        with pytest.raises(TypeError, match="REFUSED_SHAPE"):
            constructor(*args)


def test_dataclass_type_identity_and_hash_lookup():
    supply = gp.Supply("opaque")
    admission = gp.AdmitDatum("opaque")
    assert supply != admission
    assert {supply: "supply"}[gp.Supply("opaque")] == "supply"
    with pytest.raises(TypeError, match="REFUSED_SHAPE"):
        gp.Regime([], (), frozenset(), frozenset(), frozenset())
    with pytest.raises(ValueError, match="REFUSED_SHAPE"):
        gp.Regime(("opaque",), (2,), frozenset({(0, (0, 1))}), frozenset(), frozenset())
    kernel = gp.bool_kernel()
    integer_endpoints = gp.WitnessedDiff(kernel.delta, kernel.zero, 0, 1)
    assert kernel != integer_endpoints
    assert len({kernel, integer_endpoints}) == 2


def test_mapping_copy_hash_and_canonical_order():
    original = {0: 1, 1: 0}
    left = gp.FrameTransformation("a", "b", original)
    right = gp.FrameTransformation("a", "b", {1: 0, 0: 1})
    original[0] = 99
    assert left.mapping[0] == 1
    assert left == right
    assert hash(left) == hash(right)
    assert {left: "frame"}[right] == "frame"
    assert codec.canonical_json(left) == codec.canonical_json(right)
    with pytest.raises(TypeError):
        left.mapping[0] = 2
    with pytest.raises(FrozenInstanceError):
        left.mapping._items = ()
    with pytest.raises(ValueError, match="bijective"):
        gp.FrameTransformation("a", "b", {0: 0, 1: 0})
    proposal = represented.ProposalRecord("p", (0, 1), {0: 0, 1: 1}, 2)
    assert proposal.is_valid_retraction((0, 1))
    assert not proposal.is_valid_retraction((False, 1))
    assert hash(proposal) == hash(replace(proposal, down_map={1: 1, 0: 0}))


def test_canonical_rationals_lf_and_float_refusal():
    encoded = codec.canonical_json({"fraction": Fraction(2, 4), "integer_rational": Fraction(1)})
    assert encoded == b'{"fraction":"1/2","integer_rational":"1/1"}\n'
    assert not encoded.startswith(b"\xef\xbb\xbf") and b"\r" not in encoded
    with pytest.raises(TypeError, match="REFUSED_FLOAT"):
        codec.canonical_json({"value": 0.5})
    with pytest.raises(TypeError, match="UNSERIALIZABLE"):
        codec.canonical_json(gp.bool_kernel())
    assert json.loads(codec.canonical_json(gp.EMPTY))["$type"] == "seed_and_regime.Regime"


def test_map_and_generic_endpoints_reject_nested_bool_integer_aliases():
    integer_key = codec.FrozenMap({1: "value"})
    boolean_key = codec.FrozenMap({True: "value"})
    assert integer_key != boolean_key
    with pytest.raises(KeyError):
        integer_key[True]
    with pytest.raises(KeyError):
        boolean_key[1]
    integer_value = codec.FrozenMap({"payload": (frozenset({1}),)})
    boolean_value = codec.FrozenMap({"payload": (frozenset({True}),)})
    assert integer_value != boolean_value
    assert len({integer_key, boolean_key, integer_value, boolean_value}) == 4
    duplicate = codec.FrozenMap({"payload": (frozenset({1}),)})
    assert integer_value == duplicate and hash(integer_value) == hash(duplicate)
    assert {integer_value: "found"}[duplicate] == "found"
    assert codec.canonical_json(integer_value) != codec.canonical_json(boolean_value)

    @dataclass(frozen=True, eq=False)
    class IdentityPayload:
        value: int

    first, second = IdentityPayload(1), IdentityPayload(1)
    first_map, second_map = (
        codec.FrozenMap({"payload": first}),
        codec.FrozenMap({"payload": second}),
    )
    assert first_map != second_map
    assert len({first_map, second_map}) == 2
    assert first_map == codec.FrozenMap({"payload": first})
    assert hash(first_map) == hash(codec.FrozenMap({"payload": first}))
    diagnostic_nan = float("nan")
    nan_map = codec.FrozenMap({"diagnostic": diagnostic_nan})
    assert nan_map == nan_map
    assert nan_map == codec.FrozenMap({"diagnostic": diagnostic_nan})
    with pytest.raises(TypeError, match="REFUSED_FLOAT"):
        codec.canonical_json(nan_map)
    kernel = gp.bool_kernel()
    integer_endpoints = gp.WitnessedDiff(kernel.delta, kernel.zero, (0,), (1,))
    boolean_endpoints = gp.WitnessedDiff(kernel.delta, kernel.zero, (False,), (True,))
    assert integer_endpoints != boolean_endpoints
    assert len({integer_endpoints, boolean_endpoints}) == 2


def test_nullable_union_fields_and_callable_hashability():
    record = engine.RoundRecord(0, 0, None, 0, 0, 0)
    assert record == replace(record) and hash(record) == hash(replace(record))
    assert json.loads(codec.canonical_json(record))["first_pair"] is None
    with pytest.raises(TypeError, match="REFUSED_SHAPE"):
        replace(record, first_pair=(False, 1))
    state = gp.PS(obs=None)
    assert state == replace(state) and hash(state) == hash(replace(state))
    with pytest.raises(TypeError, match="REFUSED_SHAPE"):
        replace(state, obs=((False,),))

    class UnhashableCallable:
        __hash__ = None

        def __call__(self, *_args):
            return False

    with pytest.raises(TypeError, match="must be hashable"):
        gp.WitnessedDiff(UnhashableCallable(), gp.bool_kernel().zero, False, True)

    @dataclass(frozen=True)
    class UnhashableFrozenPayload:
        value: int
        __hash__ = None

    with pytest.raises(TypeError, match="must be hashable"):
        codec.FrozenMap({"payload": UnhashableFrozenPayload(1)})

    @dataclass(frozen=True)
    class FrozenCallable:
        def __call__(self, *_args):
            return False

    with pytest.raises(TypeError, match="executable payload"):
        codec.canonical_json(FrozenCallable())


def test_exact_snapshot_requires_all_simplicial_faces():
    malformed = gp.Complex(c0=(0, 1, 2), c2=((0, 1, 2),))
    with pytest.raises(ValueError, match="boundary face"):
        codec.canonical_json(malformed)
    good = gp.Complex(c0=(0, 1, 2), c1=((0, 1), (0, 2), (1, 2)), c2=((0, 1, 2),))
    assert codec.canonical_json(good).endswith(b"\n")


def test_false_source_certification_and_transition_forgery_refused():
    args = dict(node_id=0, history=(), regime=gp.EMPTY, depth=0, canon=())
    with pytest.raises(ValueError, match="REFUSED_UNVERIFIED_SOURCE_CERTIFICATE"):
        engine.Node(**args, certified=True)
    node = engine.Node(**args)
    with pytest.raises(ValueError, match="REFUSED_UNVERIFIED_SOURCE_CERTIFICATE"):
        node.certified = True
    tree = engine.Tree("L", "mu1", gp.Bounds(), 1, 2, True)
    assert tree.stats()["all_certified"] is False
    assert tree.stats()["certification_status"] == "SOURCE_ENGINE_REPLAY_REQUIRED"
    with pytest.raises(TypeError, match="mutable runtime"):
        codec.canonical_json(node)
    good = traces.make_record(gp.GENESIS_P, ("admitOcc", 0))
    assert good.is_well_formed()
    with pytest.raises(TypeError, match="REFUSED_SHAPE"):
        replace(good, profile=("forged",) * 7)
    for forged in (replace(good, cls="forged"), replace(good, spend="forged")):
        assert not forged.is_well_formed()
        with pytest.raises(ValueError, match="does not replay"):
            codec.canonical_json(forged)
    raw_trace = trace_algebra.TRecord(good.pre, good.ev, good.pre, True)
    assert not raw_trace.is_well_formed()
    with pytest.raises(ValueError, match="does not replay"):
        codec.canonical_json(raw_trace)


def test_controller_and_unbounded_integer_ray_boundaries():
    with pytest.raises(ValueError, match="Boolean"):
        gp.response_live((1,) * 10)
    with pytest.raises(ValueError, match="Boolean"):
        gp.enabled((False,), ("admitOcc", 0))
    assert gp.same_ray((0,), {0: 10_001}, {0: 1}, max_scale=1)
    assert gp.same_ray((0,), {0: 0}, {0: 0})
    assert not gp.same_ray((0,), {0: 0}, {0: 1})
    with pytest.raises(ValueError, match="natural-number"):
        gp.same_profile((0,), {0: True}, {0: 1})
    assert not gp.is_apart(True, frozenset())
    assert not gp.is_apart(2, frozenset({(-1, -1)}))
    with pytest.raises(ValueError, match="REFUSED_SHAPE"):
        gp.apply_perm_pair((1, 0), (-1, 0))


def test_numerical_observer_mapping_is_immutable_and_exact_codec_refuses_float():
    original = {(1,): 1.0}
    section = gp.LocalSection(gp.MeasurementContext(("A",)), original)
    original[(1,)] = 0.0
    assert section.distribution[(1,)] == 1.0
    assert hash(section) == hash(gp.LocalSection(gp.MeasurementContext(("A",)), {(1,): 1.0}))
    with pytest.raises(TypeError, match="REFUSED_FLOAT"):
        codec.canonical_json(section)
