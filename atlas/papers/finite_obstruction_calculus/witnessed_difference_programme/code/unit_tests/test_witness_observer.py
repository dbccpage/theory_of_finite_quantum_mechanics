from dataclasses import replace
from fractions import Fraction

import pytest
from witnessed_difference.observer import (
    ObserverBridge,
    ObserverObject,
    OperationalObserverPacket,
    QuotientObserver,
    RetentionPacket,
    adapt_operational,
    adapt_quotient,
    make_cm1_static_carrier,
    make_cm2_blind_readout,
    make_cm3_coarse_grained_report,
    make_cm4_nontrivial_tolerance,
    make_cm5_lossy_reset,
    tree_behavior_equivalent,
    validate_report_profile_separation,
)
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.witness import (
    ReaccessReceipt,
    Registration,
    WitnessReceipt,
    make_witness,
    payload_digest,
    verify_witness,
)


def bridge(kind: str = "quotient", *, local: str = "local") -> ObserverBridge:
    return ObserverBridge(
        kind, local, "delta", "d0", "d1", "gauge", "transform", "terminal"
    )


def quotient() -> QuotientObserver:
    return QuotientObserver(
        ("a", "b", "c"), (frozenset({"a", "b"}), frozenset({"c"})), "same block"
    )


def operational() -> OperationalObserverPacket:
    return OperationalObserverPacket(
        ("s0", "s1"),
        "s0",
        ("tick",),
        (("s0", "tick", "s1"), ("s1", "tick", "s1")),
        (("s0", "quiet"), ("s1", "seen")),
        (("s0", "p0"), ("s1", "p1")),
    )


@pytest.mark.parametrize(
    ("carrier_id", "occurrence"),
    [("", 0), ("log", -1), ("log", True), ("log", 0.5), ("log", "2")],
)
def test_registration_validation(carrier_id, occurrence) -> None:
    with pytest.raises(ValueError):
        Registration(carrier_id, "mark", occurrence)
    with pytest.raises(ValueError, match="boolean"):
        Registration("log", "mark", 0, 1)


def test_reaccess_receipt_rejects_malformed_identity_and_digests() -> None:
    # Invariant: re-access identity and both SHA-256 bindings are structurally valid.
    valid_digest = "0" * 64
    with pytest.raises(ValueError, match="evaluator_id"):
        ReaccessReceipt("", valid_digest, valid_digest)
    with pytest.raises(ValueError, match="SHA-256"):
        ReaccessReceipt("E", "0" * 63, valid_digest)
    with pytest.raises(ValueError, match="SHA-256"):
        ReaccessReceipt("E", "g" * 64, valid_digest)


def test_witness_requires_retention_evaluator_and_matching_reaccess() -> None:
    wrong_registration = make_witness(object(), "mark", "E")
    assert isinstance(wrong_registration, Refused)
    assert wrong_registration.code is RefusalCode.INVALID_INPUT
    unretained = make_witness(Registration("log", "mark", 0, False), "mark", "E")
    assert (
        isinstance(unretained, Refused) and unretained.code is RefusalCode.NOT_RETAINED
    )
    no_evaluator = make_witness(Registration("log", "mark", 0), "mark", "")
    assert (
        isinstance(no_evaluator, Refused)
        and no_evaluator.code is RefusalCode.INVALID_INPUT
    )
    mismatch = make_witness(Registration("log", "mark", 0), "other", "E")
    assert (
        isinstance(mismatch, Refused) and mismatch.code is RefusalCode.REACCESS_FAILED
    )
    malformed_observed = make_witness(Registration("log", "mark", 0), object(), "E")
    assert isinstance(malformed_observed, Refused)
    assert malformed_observed.code is RefusalCode.INVALID_INPUT
    malformed_retained = make_witness(Registration("log", object(), 0), object(), "E")
    assert isinstance(malformed_retained, Refused)
    assert malformed_retained.code is RefusalCode.INVALID_INPUT


def test_witness_round_trip_and_tamper_detection() -> None:
    registration = Registration("log", {"value": 3}, 7)
    result = make_witness(registration, {"value": 3}, "E")
    assert isinstance(result, Accepted)
    receipt = result.value
    assert receipt.authority_effect.value == "None"
    assert isinstance(verify_witness(receipt, {"value": 3}), Accepted)
    artifact_tamper = verify_witness(receipt, {"value": 4})
    assert (
        isinstance(artifact_tamper, Refused)
        and artifact_tamper.code is RefusalCode.DIGEST_MISMATCH
    )
    digest_tamper = verify_witness(
        replace(receipt, receipt_digest="0" * 64), {"value": 3}
    )
    assert (
        isinstance(digest_tamper, Refused)
        and digest_tamper.code is RefusalCode.RECEIPT_MISMATCH
    )
    with pytest.raises(ValueError, match="authority effect"):
        replace(receipt, authority_effect="promoted")
    forged = replace(receipt)
    object.__setattr__(forged, "authority_effect", "promoted")
    firewall = verify_witness(forged, {"value": 3})
    assert (
        isinstance(firewall, Refused)
        and firewall.code is RefusalCode.CLAIM_STATUS_FIREWALL
    )
    malformed = verify_witness(receipt, object())
    assert isinstance(malformed, Refused)
    assert malformed.code is RefusalCode.INVALID_INPUT
    wrong_receipt = verify_witness(object(), {"value": 3})
    assert isinstance(wrong_receipt, Refused)
    assert wrong_receipt.code is RefusalCode.INVALID_INPUT


def test_witness_detects_mutation_of_aliased_retained_mark() -> None:
    mark = {"value": 3}
    registration = Registration("log", mark, 0)
    made = make_witness(registration, {"value": 3}, "E")
    assert isinstance(made, Accepted)
    mark["value"] = 4
    replay = verify_witness(made.value, {"value": 3})
    assert isinstance(replay, Refused)
    assert replay.code is RefusalCode.DIGEST_MISMATCH


def test_witness_digest_does_not_accept_cross_type_substitution() -> None:
    registration = Registration("log", Fraction(1, 2), 0)
    result = make_witness(registration, {"denominator": 2, "numerator": 1}, "E")
    assert isinstance(result, Refused)
    assert result.code is RefusalCode.REACCESS_FAILED


def test_witness_verifier_refuses_unretained_and_internally_mismatched_receipts() -> (
    None
):
    registration = Registration("log", "mark", 0, False)
    reaccess = ReaccessReceipt("E", payload_digest("mark"), payload_digest("mark"))
    receipt = WitnessReceipt(registration, reaccess, "unused")
    assert verify_witness(receipt, "mark").code is RefusalCode.NOT_RETAINED
    retained = replace(registration, retained=True)
    bad_reaccess = ReaccessReceipt("E", payload_digest("mark"), payload_digest("other"))
    bad = WitnessReceipt(retained, bad_reaccess, payload_digest({"unrelated": True}))
    assert verify_witness(bad, "other").code is RefusalCode.RECEIPT_MISMATCH


@pytest.mark.parametrize(
    "factory",
    [
        lambda: QuotientObserver((), (), "cmp"),
        lambda: QuotientObserver(("a", "a"), (frozenset({"a"}),), "cmp"),
        lambda: QuotientObserver(("a",), (frozenset({"a"}),), ""),
        lambda: QuotientObserver(
            ("a", "b"), (frozenset(), frozenset({"a", "b"})), "cmp"
        ),
        lambda: QuotientObserver(
            ("a", "b"), (frozenset({"a"}), frozenset({"a", "b"})), "cmp"
        ),
        lambda: QuotientObserver(("a",), (frozenset({"x"}),), "cmp"),
        lambda: QuotientObserver(("a", "b"), (frozenset({"a"}),), "cmp"),
        lambda: QuotientObserver(["a", "b"], (frozenset({"a", "b"}),), "cmp"),
        lambda: QuotientObserver((1, 2), (frozenset({1}), frozenset({2})), "cmp"),
        lambda: QuotientObserver(("a", "b"), [frozenset({"a", "b"})], "cmp"),
        lambda: QuotientObserver(("a", "b"), ({"a", "b"},), "cmp"),
        lambda: QuotientObserver(("a",), (frozenset({"a"}),), 1),
    ],
)
def test_quotient_observer_requires_a_partition(factory) -> None:
    with pytest.raises(ValueError):
        factory()


@pytest.mark.parametrize(
    "factory",
    [
        lambda: OperationalObserverPacket((), "s", ("x",), (), (), ()),
        lambda: OperationalObserverPacket(
            ("s", "s"), "s", ("x",), (), (("s", "r"),), (("s", "p"),)
        ),
        lambda: OperationalObserverPacket(
            ("s",), "x", ("a",), (), (("s", "r"),), (("s", "p"),)
        ),
        lambda: OperationalObserverPacket(
            ("s",), "s", (), (), (("s", "r"),), (("s", "p"),)
        ),
        lambda: OperationalObserverPacket(
            ("s",), "s", ("a", "a"), (), (("s", "r"),), (("s", "p"),)
        ),
        lambda: OperationalObserverPacket(
            ("s",), "s", ("a",), (("s", "a", "x"),), (("s", "r"),), (("s", "p"),)
        ),
        lambda: OperationalObserverPacket(("s",), "s", ("a",), (), (), (("s", "p"),)),
        lambda: OperationalObserverPacket(("s",), "s", ("a",), (), (("s", "r"),), ()),
        lambda: OperationalObserverPacket(
            ("s0", "s1"),
            "s0",
            ("a",),
            (),
            (("s0", "r0"), ("s0", "duplicate"), ("s1", "r1")),
            (("s0", "p0"), ("s1", "p1")),
        ),
        lambda: OperationalObserverPacket(
            ("s0", "s1"),
            "s0",
            ("a",),
            (),
            (("s0", "r0"), ("s1", "r1")),
            (("s0", "p0"), ("s0", "duplicate"), ("s1", "p1")),
        ),
        lambda: OperationalObserverPacket(
            ["s0", "s1"],
            "s0",
            ("a",),
            (),
            (("s0", "r0"), ("s1", "r1")),
            (("s0", "p0"), ("s1", "p1")),
        ),
        lambda: OperationalObserverPacket(
            ("s0", 1),
            "s0",
            ("a",),
            (),
            (("s0", "r0"), (1, "r1")),
            (("s0", "p0"), (1, "p1")),
        ),
        lambda: OperationalObserverPacket(
            ("s0",),
            "s0",
            ("a",),
            (["s0", "a", "s0"],),
            (("s0", "r0"),),
            (("s0", "p0"),),
        ),
        lambda: OperationalObserverPacket(
            ("s0",),
            "s0",
            ("a",),
            (),
            (("s0", 1),),
            (("s0", "p0"),),
        ),
    ],
)
def test_operational_observer_validation(factory) -> None:
    with pytest.raises(ValueError):
        factory()


def test_observer_object_completeness() -> None:
    complete = ObserverObject("K", "F", "R", "delta", "d0", None, "J", "M", "tau")
    assert complete.complete
    assert not replace(complete, transform_m="").complete


@pytest.mark.parametrize("adapter", [adapt_quotient, adapt_operational])
def test_observer_adapters_require_explicit_matching_bridges(adapter) -> None:
    observer = quotient() if adapter is adapt_quotient else operational()
    assert adapter(observer, None).code is RefusalCode.MISSING_ADAPTER
    wrong = bridge("operational" if adapter is adapt_quotient else "quotient")
    assert adapter(observer, wrong).code is RefusalCode.ADAPTER_MISMATCH
    incomplete = bridge(
        "quotient" if adapter is adapt_quotient else "operational", local=""
    )
    assert adapter(observer, incomplete).code is RefusalCode.INVALID_INPUT
    bad_kind = "quotient" if adapter is adapt_quotient else "operational"
    untyped = ObserverBridge(bad_kind, 1, "delta", "d0", None, "g", "m", "tau")
    assert adapter(observer, untyped).code is RefusalCode.INVALID_INPUT


def test_distinct_observers_adapt_only_through_declared_bridges() -> None:
    q_result = adapt_quotient(quotient(), bridge("quotient"))
    o_result = adapt_operational(operational(), bridge("operational"))
    assert isinstance(q_result, Accepted) and q_result.value.carrier_k.startswith(
        "quotient:"
    )
    assert isinstance(o_result, Accepted) and o_result.value.carrier_k.startswith(
        "operational:"
    )
    assert q_result.value != o_result.value


def test_profile_distinction_must_force_report_distinction() -> None:
    assert isinstance(validate_report_profile_separation(operational()), Accepted)
    collapsed = OperationalObserverPacket(
        ("s0", "s1"),
        "s0",
        ("tick",),
        (("s0", "tick", "s1"),),
        (("s0", "same"), ("s1", "same")),
        (("s0", "p0"), ("s1", "p1")),
    )
    result = validate_report_profile_separation(collapsed)
    assert isinstance(result, Refused)
    assert result.code is RefusalCode.REPORT_PROFILE_COLLAPSE


def test_retention_packet_validation() -> None:
    with pytest.raises(ValueError, match="memory carrier must be a tuple"):
        RetentionPacket(["m0"], ("i0",), (), (), ())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="memory carrier must be a tuple"):
        RetentionPacket((), ("i0",), (), (), ())
    with pytest.raises(ValueError, match="memory carrier must be a tuple"):
        RetentionPacket(("m0", "m0"), ("i0",), (), (), ())
    with pytest.raises(ValueError, match="inputs must be a tuple"):
        RetentionPacket(("m0",), ["i0"], (), (), ())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="inputs must be a tuple"):
        RetentionPacket(("m0",), (), (), (), ())
    with pytest.raises(ValueError, match="update transitions must map"):
        RetentionPacket(("m0",), ("i0",), (("m0", "i0", "outside"),), (("m0", "r0"),), ())
    with pytest.raises(ValueError, match="reports must map"):
        RetentionPacket(("m0",), ("i0",), (("m0", "i0", "m0"),), (("outside", "r0"),), ())
    with pytest.raises(ValueError, match="comparison must be pairs"):
        RetentionPacket(("m0",), ("i0",), (("m0", "i0", "m0"),), (("m0", "r0"),), (("r0",),))  # type: ignore[arg-type]


def test_cm1_static_carrier_independence() -> None:
    cm1 = make_cm1_static_carrier()
    assert len(cm1.memory_carrier) == 2
    assert cm1.is_observable() is True
    assert cm1.is_reversible("tick") is True
    # Carrier is non-trivial, but state never updates under inputs
    step0 = cm1.step("m0", "tick")
    step1 = cm1.step("m1", "tick")
    assert isinstance(step0, Accepted) and step0.value == "m0"
    assert isinstance(step1, Accepted) and step1.value == "m1"
    assert isinstance(cm1.step("m0", "bad"), Refused)


def test_cm2_blind_readout_independence() -> None:
    cm2 = make_cm2_blind_readout()
    assert cm2.is_reversible("toggle") is True
    # Internal states toggle between m0 and m1
    next_state = cm2.step("m0", "toggle")
    assert isinstance(next_state, Accepted) and next_state.value == "m1"
    # But report is completely blind (constant)
    rep0 = cm2.report("m0")
    rep1 = cm2.report("m1")
    assert isinstance(rep0, Accepted) and rep0.value == "constant"
    assert isinstance(rep1, Accepted) and rep1.value == "constant"
    assert cm2.is_observable() is False
    assert isinstance(cm2.report("outside"), Refused)


def test_cm3_coarse_grained_report_independence() -> None:
    cm3 = make_cm3_coarse_grained_report()
    assert len(cm3.memory_carrier) == 3
    assert cm3.is_reversible("cycle") is True
    # Invertible cyclic dynamics on 3 states, but report merges m0 and m2
    assert cm3.is_observable() is False
    assert cm3.report("m0").value == "even"  # type: ignore[union-attr]
    assert cm3.report("m1").value == "odd"  # type: ignore[union-attr]
    assert cm3.report("m2").value == "even"  # type: ignore[union-attr]


def test_cm4_nontrivial_tolerance_independence() -> None:
    cm4 = make_cm4_nontrivial_tolerance()
    assert cm4.is_observable() is True
    # Report values are distinct (val0 != val1)
    assert cm4.report("m0").value == "val0"  # type: ignore[union-attr]
    assert cm4.report("m1").value == "val1"  # type: ignore[union-attr]
    # But declared comparison relation declares val0 ~ val1
    assert cm4.are_equivalent("val0", "val1") is True
    assert cm4.are_equivalent("val0", "unknown") is False


def test_cm5_lossy_reset_independence() -> None:
    cm5 = make_cm5_lossy_reset()
    assert cm5.is_observable() is True
    assert cm5.is_reversible("keep") is True
    # Collapsing reset destroys reversibility: both m0 and m1 go to m0
    assert cm5.is_reversible("reset") is False
    assert cm5.step("m0", "reset").value == "m0"  # type: ignore[union-attr]
    assert cm5.step("m1", "reset").value == "m0"  # type: ignore[union-attr]


def test_tree_behavior_equivalence_without_sequence_order() -> None:
    cm1_a = make_cm1_static_carrier()
    cm1_b = make_cm1_static_carrier()
    assert tree_behavior_equivalent(cm1_a, "m0", cm1_b, "m0", depth=3) is True
    assert tree_behavior_equivalent(cm1_a, "m0", cm1_b, "m1", depth=3) is False
    # Negative depth base case
    assert tree_behavior_equivalent(cm1_a, "m0", cm1_b, "m0", depth=-1) is True
    # Non-equivalent systems
    cm2 = make_cm2_blind_readout()
    assert tree_behavior_equivalent(cm1_a, "m0", cm2, "m0", depth=1) is False


def test_is_reversible_hardened_adversarial_checks() -> None:
    # 1. Undeclared input symbol
    cm1 = make_cm1_static_carrier()
    assert cm1.is_reversible("undeclared") is False

    # 2. Non-functional update: same source maps to two distinct targets for same symbol
    m = ("m0", "m1")
    inputs = ("tick",)
    u_nonfunc = (("m0", "tick", "m0"), ("m0", "tick", "m1"))
    r = (("m0", "r0"), ("m1", "r1"))
    approx = (("r0", "r0"), ("r1", "r1"))
    with pytest.raises(ValueError, match="unique"):
        RetentionPacket(m, inputs, u_nonfunc, r, approx)

    # 3. Partial update: source m1 is missing a transition
    u_partial = (("m0", "tick", "m0"),)
    with pytest.raises(ValueError, match="cover all"):
        RetentionPacket(m, inputs, u_partial, r, approx)


def test_tree_behavior_equivalence_disjoint_input_alphabets() -> None:
    m = ("m0", "m1")
    r = (("m0", "r0"), ("m1", "r1"))
    approx = (("r0", "r0"), ("r1", "r1"))
    p1 = RetentionPacket(m, ("alpha",), (("m0", "alpha", "m0"), ("m1", "alpha", "m1")), r, approx)
    p2 = RetentionPacket(m, ("beta",), (("m0", "beta", "m0"), ("m1", "beta", "m1")), r, approx)
    # Disjoint inputs must be refused as behaviorally equivalent in both argument orders
    assert tree_behavior_equivalent(p1, "m0", p2, "m0", depth=1) is False
    assert tree_behavior_equivalent(p2, "m0", p1, "m0", depth=1) is False


def test_retention_packet_duplicate_report_keys_rejected() -> None:
    m = ("m0", "m1")
    inputs = ("tick",)
    u = (("m0", "tick", "m1"), ("m1", "tick", "m0"))
    r_dup = (("m0", "r0"), ("m0", "r1"))
    approx = (("r0", "r0"), ("r1", "r1"))
    with pytest.raises(ValueError, match="reports must have unique source states"):
        RetentionPacket(m, inputs, u, r_dup, approx)


def test_tree_behavior_equivalence_symmetry() -> None:
    m = ("m0", "m1")
    inputs = ("a", "b")
    u1 = (("m0", "a", "m1"), ("m0", "b", "m0"), ("m1", "a", "m0"), ("m1", "b", "m1"))
    r1 = (("m0", "out0"), ("m1", "out1"))
    approx1 = (("out0", "out0"), ("out1", "out1"))
    p1 = RetentionPacket(m, inputs, u1, r1, approx1)

    # p2 has swapped inputs tuple ("b", "a") with isomorphic transitions
    inputs2 = ("b", "a")
    u2 = (("m0", "b", "m0"), ("m0", "a", "m1"), ("m1", "b", "m1"), ("m1", "a", "m0"))
    p2 = RetentionPacket(m, inputs2, u2, r1, approx1)

    for depth in range(-1, 4):
        for s1 in m:
            for s2 in m:
                res1 = tree_behavior_equivalent(p1, s1, p2, s2, depth=depth)
                res2 = tree_behavior_equivalent(p2, s2, p1, s1, depth=depth)
                assert res1 == res2, f"symmetry broken at depth={depth} for s1={s1}, s2={s2}"

    # Asymmetric comparison table: p_loose allows out0 ~ out1, p_strict does not
    approx_loose = (("out0", "out0"), ("out1", "out1"), ("out0", "out1"))
    p_loose = RetentionPacket(m, inputs, u1, r1, approx_loose)
    p_strict = RetentionPacket(m, inputs, u1, r1, approx1)

    # Mutual equivalence must require both to consider reports equivalent, ensuring symmetry
    assert tree_behavior_equivalent(p_loose, "m0", p_strict, "m1", depth=0) is False
    assert tree_behavior_equivalent(p_strict, "m1", p_loose, "m0", depth=0) is False


# Executable finite evidence; AuthorityEffect: None.
