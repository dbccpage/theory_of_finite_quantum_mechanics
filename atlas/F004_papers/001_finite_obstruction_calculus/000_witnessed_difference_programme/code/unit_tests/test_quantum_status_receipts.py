from dataclasses import replace
from fractions import Fraction
from math import pi

import pytest
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.projective import GaussianRational
from witnessed_difference.quantum import (
    EVIDENCE_ANCHORS,
    MAX_U1_TOLERANCE,
    AlgebraicNonFactorableWitness,
    CombiningSystemsInterface,
    EntanglementWitness,
    IntegerWeights,
    InterferenceObstruction,
    PermutationIsometryEnvelope,
    PhaseBlindReadout,
    PresentedCarrier,
    QuantumEvidence,
    U1Connection,
    edge_phase,
    fixed_scale_phase,
    gauge_transform,
    get_exposed_quantum_imports,
    holonomy,
    make_connection,
    supports_quantum_reconstruction,
)
from witnessed_difference.receipts import (
    canonical_json,
    content_hash,
    make_receipt,
    verify_receipt,
)
from witnessed_difference.relative_status import (
    Claim,
    ClaimStatus,
    EvaluationProfile,
    attach_finite_witness,
    route_claim,
)


def connection():
    result = make_connection(
        ("a", "b", "c"),
        (("a", "b", 1j), ("b", "c", 1 + 0j), ("a", "c", 1 + 0j)),
    )
    assert isinstance(result, Accepted)
    return result.value


class BrokenFloat(float):
    def __float__(self) -> float:
        raise ValueError("conversion disabled")


class BrokenComplex(complex):
    def __complex__(self) -> complex:
        raise ValueError("conversion disabled")


def test_connection_validation_surface() -> None:
    invalid = [
        make_connection((), ()),
        make_connection(("a", "a"), ()),
        make_connection(("a",), (), tolerance=0),
        make_connection(("a",), (("a", "a", 1 + 0j),)),
        make_connection(("a", "b"), (("a", "b", 2 + 0j),)),
        make_connection(("a", "b"), (("a", "b", 1 + 0j), ("a", "b", 1 + 0j))),
        make_connection(("a", "b"), (("a", "b", 1j), ("b", "a", 1j))),
        make_connection(("a", "b"), (("a", "b", 0j),), tolerance=float("inf")),
        make_connection(("a", "b"), (("a", "b", complex(float("nan"), 0)),)),
    ]
    assert all(isinstance(item, Refused) for item in invalid)
    assert invalid[4].code is RefusalCode.NON_UNIT_PHASE
    assert invalid[6].code is RefusalCode.NON_UNIT_PHASE
    assert invalid[7].code is RefusalCode.INVALID_INPUT
    assert invalid[8].code is RefusalCode.NON_UNIT_PHASE
    assert make_connection(("a",), (), tolerance=True).code is RefusalCode.INVALID_INPUT
    assert (
        make_connection(("a",), (), tolerance=BrokenFloat(1)).code
        is RefusalCode.INVALID_INPUT
    )
    assert (
        make_connection(("a", "b"), (("a", "b", "not-a-phase"),)).code
        is RefusalCode.NON_UNIT_PHASE
    )
    assert (
        make_connection(("a", "b"), (("a", "b", BrokenComplex(1)),)).code
        is RefusalCode.NON_UNIT_PHASE
    )
    with pytest.raises(ValueError, match="unit modulus"):
        U1Connection(("a", "b"), (("a", "b", 0j),))


def test_direct_connection_constructor_rejects_each_structural_defect() -> None:
    # Invariant: direct construction enforces the same carrier/orientation laws.
    invalid = (
        ((), (), "unique named vertices"),
        (("a", "b"), (("a", "outside", 1 + 0j),), "leaves the carrier"),
        (
            ("a", "b"),
            (("a", "b", 1 + 0j), ("a", "b", 1 + 0j)),
            "duplicated",
        ),
        (
            ("a", "b"),
            (("a", "b", 1j), ("b", "a", 1j)),
            "conjugate phase",
        ),
    )
    for vertices, phases, message in invalid:
        with pytest.raises(ValueError, match=message):
            U1Connection(vertices, phases)


def test_connection_rejects_mutable_carriers_and_phase_collections() -> None:
    refused = (
        make_connection(["a", "b"], (("a", "b", 1 + 0j),)),
        make_connection(("a", "b"), [("a", "b", 1 + 0j)]),
        make_connection(("a", "b"), (["a", "b", 1 + 0j],)),
    )
    assert all(isinstance(result, Refused) for result in refused)
    assert all(result.code is RefusalCode.INVALID_INPUT for result in refused)
    with pytest.raises(ValueError, match="immutable tuples"):
        U1Connection(["a", "b"], (("a", "b", 1 + 0j),))
    with pytest.raises(ValueError, match="immutable tuples"):
        U1Connection(("a", "b"), [("a", "b", 1 + 0j)])
    with pytest.raises(ValueError, match="edge triples"):
        U1Connection(("a", "b"), (["a", "b", 1 + 0j],))


def test_connection_tolerance_ceiling_preserves_unit_modulus_gate() -> None:
    default = make_connection(("a", "b"), (("a", "b", 1 + 0j),))
    boundary = make_connection(
        ("a", "b"),
        (("a", "b", 1 + 0j),),
        tolerance=MAX_U1_TOLERANCE,
    )
    assert isinstance(default, Accepted)
    assert isinstance(boundary, Accepted)
    too_loose = make_connection(
        ("a", "b"),
        (("a", "b", 1 + 0j),),
        tolerance=2 * MAX_U1_TOLERANCE,
    )
    assert isinstance(too_loose, Refused)
    assert too_loose.code is RefusalCode.INVALID_INPUT
    zero = make_connection(
        ("a", "b"),
        (("a", "b", 0j),),
        tolerance=MAX_U1_TOLERANCE,
    )
    small = make_connection(
        ("a", "b"),
        (("a", "b", 0.1 + 0j),),
        tolerance=MAX_U1_TOLERANCE,
    )
    assert isinstance(zero, Refused) and zero.code is RefusalCode.NON_UNIT_PHASE
    assert isinstance(small, Refused) and small.code is RefusalCode.NON_UNIT_PHASE
    with pytest.raises(ValueError, match=r"in \(0,"):
        U1Connection(
            ("a", "b"),
            (("a", "b", 1 + 0j),),
            tolerance=2 * MAX_U1_TOLERANCE,
        )


def test_edge_phase_direct_reverse_and_missing() -> None:
    direct = edge_phase(connection(), "a", "b")
    reverse = edge_phase(connection(), "b", "a")
    missing = edge_phase(connection(), "a", "x")
    assert isinstance(direct, Accepted) and direct.value == GaussianRational(0, 1)
    assert isinstance(reverse, Accepted) and reverse.value == GaussianRational(0, -1)
    assert isinstance(missing, Refused) and missing.code is RefusalCode.MISSING_EDGE


def test_holonomy_requires_an_explicit_closed_supported_path() -> None:
    assert holonomy(connection(), ("a",)).code is RefusalCode.INVALID_INPUT
    assert holonomy(connection(), ("a", "b")).code is RefusalCode.OPEN_PATH
    assert holonomy(connection(), ("a", "x", "a")).code is RefusalCode.MISSING_EDGE
    result = holonomy(connection(), ("a", "b", "c", "a"))
    assert isinstance(result, Accepted) and result.value == GaussianRational(0, 1)


def test_gauge_transform_preserves_closed_holonomy() -> None:
    original = connection()
    transformed = gauge_transform(original, {"a": 1j, "b": -1 + 0j, "c": 1 + 0j})
    assert isinstance(transformed, Accepted)
    before = holonomy(original, ("a", "b", "c", "a"))
    after = holonomy(transformed.value, ("a", "b", "c", "a"))
    assert isinstance(before, Accepted) and isinstance(after, Accepted)
    assert before.value == after.value
    assert gauge_transform(original, {"a": 1 + 0j}).code is RefusalCode.NON_UNIT_PHASE
    assert (
        gauge_transform(original, {"a": 2 + 0j, "b": 1 + 0j, "c": 1 + 0j}).code
        is RefusalCode.NON_UNIT_PHASE
    )
    assert (
        gauge_transform(
            original,
            {"a": 0j, "b": 0j, "c": 0j},
            tolerance=float("inf"),
        ).code
        is RefusalCode.INVALID_INPUT
    )


def test_fixed_scale_phase_and_reconstruction_scope_firewall() -> None:
    phase = fixed_scale_phase(pi, 1)
    assert isinstance(phase, Refused) and phase.code is RefusalCode.NOT_EXACT
    zero = fixed_scale_phase(0, 1)
    assert isinstance(zero, Accepted) and zero.value == GaussianRational(1, 0)
    assert fixed_scale_phase(1, 0).code is RefusalCode.INVALID_INPUT
    assert fixed_scale_phase(float("inf"), 1).code is RefusalCode.INVALID_INPUT
    assert fixed_scale_phase(1, float("nan")).code is RefusalCode.INVALID_INPUT
    assert fixed_scale_phase(True, 1).code is RefusalCode.INVALID_INPUT
    assert fixed_scale_phase(BrokenFloat(1), 1).code is RefusalCode.INVALID_INPUT
    for evidence in QuantumEvidence:
        result = supports_quantum_reconstruction(evidence)
        assert result.code is RefusalCode.SCOPE_VIOLATION
        assert evidence.value in result.detail


def test_relative_status_routing_preserves_open_and_outside_profile() -> None:
    profile = EvaluationProfile("finite", frozenset({"open", "established", "refuted"}))
    open_routed = route_claim(Claim("open", ClaimStatus.OPEN), profile)
    assert open_routed.relative_status is ClaimStatus.OPEN
    assert attach_finite_witness(open_routed, "W-1").relative_status is ClaimStatus.OPEN
    established = route_claim(Claim("established", ClaimStatus.ESTABLISHED), profile)
    assert (
        attach_finite_witness(established, "W-2").relative_status
        is ClaimStatus.ESTABLISHED
    )
    refuted = route_claim(Claim("refuted", ClaimStatus.REFUTED), profile)
    assert attach_finite_witness(refuted, "W-3").relative_status is ClaimStatus.REFUTED
    outside = route_claim(Claim("other", ClaimStatus.CONJECTURE), profile)
    assert outside.relative_status is ClaimStatus.OUTSIDE_PROFILE
    attached = attach_finite_witness(outside, "W-4")
    assert attached.relative_status is ClaimStatus.OUTSIDE_PROFILE
    assert "no refutation or promotion" in attached.detail
    with pytest.raises(ValueError, match="witness_id"):
        attach_finite_witness(open_routed, "")


def test_canonical_receipt_round_trip_and_normalized_claims() -> None:
    made = make_receipt(
        "symmetry-census", {"n": 3}, {"count": 4}, ("WDP-CH03-P01", "WDP-CH03-P01")
    )
    assert isinstance(made, Accepted)
    receipt = made.value
    assert receipt.claim_ids == ("WDP-CH03-P01",)
    assert receipt.authority_effect.value == "None"
    assert isinstance(verify_receipt(receipt, {"n": 3}, {"count": 4}), Accepted)
    assert canonical_json({"fraction": Fraction(1, 2)}) == (
        '{"__wdp_type__":"mapping","items":[["fraction",'
        '{"__wdp_type__":"fraction","denominator":2,"numerator":1}]]}'
    )
    assert content_hash({"a": 1}) == content_hash({"a": 1})


@pytest.mark.parametrize(
    "args",
    [
        ("", {}, {}, ("C",)),
        ("subject", {}, {}, ()),
        ("subject", {}, {}, ("",)),
    ],
)
def test_receipt_creation_refuses_incomplete_identity(args) -> None:
    assert isinstance(make_receipt(*args), Refused)
    assert isinstance(
        make_receipt("subject", {}, {}, ("C",), implementation_version=""), Refused
    )
    assert (
        make_receipt("subject", object(), {}, ("C",)).code is RefusalCode.INVALID_INPUT
    )
    assert (
        make_receipt("subject", {}, object(), ("C",)).code is RefusalCode.INVALID_INPUT
    )


def test_receipt_verification_detects_body_input_and_output_tampering() -> None:
    result = make_receipt("subject", {"input": 1}, {"output": 2}, ("C",))
    assert isinstance(result, Accepted)
    receipt = result.value
    body_tamper = verify_receipt(
        replace(receipt, subject="other"), {"input": 1}, {"output": 2}
    )
    input_tamper = verify_receipt(receipt, {"input": 2}, {"output": 2})
    output_tamper = verify_receipt(receipt, {"input": 1}, {"output": 3})
    assert body_tamper.code is RefusalCode.RECEIPT_MISMATCH
    assert input_tamper.code is RefusalCode.DIGEST_MISMATCH
    assert output_tamper.code is RefusalCode.DIGEST_MISMATCH
    with pytest.raises(ValueError, match="authority effect"):
        replace(receipt, authority_effect="promoted")
    forged = replace(receipt)
    object.__setattr__(forged, "authority_effect", "promoted")
    firewall = verify_receipt(forged, {"input": 1}, {"output": 2})
    assert isinstance(firewall, Refused)
    assert firewall.code is RefusalCode.CLAIM_STATUS_FIREWALL
    assert (
        verify_receipt(receipt, object(), {"output": 2}).code
        is RefusalCode.INVALID_INPUT
    )
    assert (
        verify_receipt(receipt, {"input": 1}, object()).code
        is RefusalCode.INVALID_INPUT
    )
    assert (
        verify_receipt(object(), {"input": 1}, {"output": 2}).code
        is RefusalCode.INVALID_INPUT
    )


def test_presented_carrier_validation_and_same_report() -> None:
    carrier = PresentedCarrier(
        carrier_states=("x0", "x1", "x2"),
        report_states=("q0", "q1"),
        presentation_map=(("x0", "q0"), ("x1", "q0"), ("x2", "q1")),
    )
    assert carrier.same_report("x0", "x1") is True
    assert carrier.same_report("x0", "x2") is False

    with pytest.raises(ValueError, match="immutable tuples"):
        PresentedCarrier(["x0"], ("q0",), (("x0", "q0"),))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="carrier states must be unique"):
        PresentedCarrier((), ("q0",), ())
    with pytest.raises(ValueError, match="carrier states must be unique"):
        PresentedCarrier(("x0", "x0"), ("q0",), (("x0", "q0"),))
    with pytest.raises(ValueError, match="report states must be unique"):
        PresentedCarrier(("x0",), (), ())
    with pytest.raises(ValueError, match="cover all carrier states"):
        PresentedCarrier(("x0", "x1"), ("q0",), (("x0", "q0"),))
    with pytest.raises(ValueError, match="belong to report states"):
        PresentedCarrier(("x0",), ("q0",), (("x0", "outside"),))


def test_integer_weights_and_mass_preservation() -> None:
    w = IntegerWeights((("q0", 3), ("q1", 5), ("q2", -1)))
    assert w.total_mass == 7
    assert w.weight_of("q0") == 3
    assert w.weight_of("q1") == 5
    assert w.weight_of("unknown") == 0

    with pytest.raises(ValueError, match="immutable tuple"):
        IntegerWeights([("q0", 1)])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="unique state keys"):
        IntegerWeights((("q0", 1), ("q0", 2)))
    with pytest.raises(ValueError, match="weights must be integers"):
        IntegerWeights((("q0", 1.5),))  # type: ignore[arg-type]


def test_permutation_isometry_envelope() -> None:
    states = ("q0", "q1", "q2")
    perm = (("q0", "q1"), ("q1", "q2"), ("q2", "q0"))
    iso = PermutationIsometryEnvelope(3, perm, states)

    assert iso.is_isometry() is True
    mat = iso.matrix()
    assert mat == ((0, 1, 0), (0, 0, 1), (1, 0, 0))

    w = IntegerWeights((("q0", 2), ("q1", 3), ("q2", 5)))
    w_next = iso.apply(w)
    assert w_next.total_mass == w.total_mass
    assert w_next.weight_of("q1") == 2
    assert w_next.weight_of("q2") == 3
    assert w_next.weight_of("q0") == 5

    inv = iso.inverse()
    w_restored = inv.apply(w_next)
    assert w_restored.weights == w.weights

    with pytest.raises(ValueError, match="positive integer"):
        PermutationIsometryEnvelope(0, perm, states)
    with pytest.raises(ValueError, match="immutable tuples"):
        PermutationIsometryEnvelope(3, list(perm), states)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="match dimension"):
        PermutationIsometryEnvelope(2, perm, states)
    with pytest.raises(ValueError, match="bijection"):
        PermutationIsometryEnvelope(3, (("q0", "q1"), ("q1", "q1"), ("q2", "q2")), states)


def test_phase_blind_readout_and_superposition_fiber() -> None:
    v1 = (1 + 0j, 1 + 0j)
    v2 = (1 + 0j, -1 + 0j)
    pi1 = PhaseBlindReadout.readout(v1)
    pi2 = PhaseBlindReadout.readout(v2)
    assert pi1 == (1.0, 1.0)
    assert pi2 == (1.0, 1.0)
    assert PhaseBlindReadout.fiber_relative_phase(v1, v2) is True
    assert PhaseBlindReadout.fiber_relative_phase(v1, v1) is False
    assert PhaseBlindReadout.fiber_relative_phase(v1, (1 + 0j,)) is False
    assert PhaseBlindReadout.fiber_relative_phase(v1, (2 + 0j, 1 + 0j)) is False


def test_interference_obstruction_over_integers() -> None:
    assert InterferenceObstruction.unnormalized_hadamard_2() == ((1, 1), (1, -1))
    assert InterferenceObstruction.mix((1, 1)) == (2, 0)
    assert InterferenceObstruction.mix((1, -1)) == (0, 2)
    assert InterferenceObstruction.demonstrates_non_descent() is True


def test_entanglement_witness_and_schmidt_rank() -> None:
    bell = EntanglementWitness()
    assert bell.determinant == 1
    assert bell.is_entangled() is True

    product = EntanglementWitness(((1, 0), (0, 0)))
    assert product.determinant == 0
    assert product.is_entangled() is False


def test_combining_systems_interface_tensor_non_forcing() -> None:
    u = (0, 1)
    v = (0, 1)
    t = CombiningSystemsInterface.tensor_comb(u, v)
    d = CombiningSystemsInterface.dump_right_comb(u, v)
    assert t == ((0, 0), (0, 1))
    assert d == ((0, 0), (1, 0))
    assert CombiningSystemsInterface.demonstrates_non_forcing() is True


def test_exposed_quantum_imports_catalog() -> None:
    imports = get_exposed_quantum_imports()
    assert len(imports) == 8
    names = [item.name for item in imports]
    assert "Field C" in names
    assert "Continuous Circle Group U(1)" in names
    assert "Spectral Theorem for Self-Adjoint Operators" in names
    assert "Gleason Frame Continuity (n >= 3)" in names
    assert "Unique Hilbert Tensor Product" in names
    assert any(n in names for n in ("CPTP Channels & Unitary Dilation", "CPTP Channels & Stinespring Dilation"))
    assert "Continuous 1-Parameter Unitary Groups / Stone's Theorem" in names
    assert "Continuous Dual Cone Completion" in names
    verdicts = {item.host_verdict for item in imports}
    assert verdicts == {"refused", "imported"}
    by_name = {item.name: item for item in imports}
    gleason = by_name["Gleason Frame Continuity (n >= 3)"]
    assert "continuum sphere" in gleason.mathematical_cost.lower()
    assert "finite" in gleason.mathematical_cost.lower()
    tensor = by_name["Unique Hilbert Tensor Product"]
    assert "hilbert tensor" in tensor.mathematical_cost.lower()
    assert "dumpright" in tensor.mathematical_cost.lower()
    dilation = [item for item in imports if "Dilation" in item.name][0]
    assert "cptp" in dilation.mathematical_cost.lower()
    assert "unitary" in dilation.mathematical_cost.lower()


def test_presented_carrier_duplicate_presentation_keys_rejected() -> None:
    with pytest.raises(ValueError, match="unique source keys"):
        PresentedCarrier(
            ("x0", "x1"),
            ("q0", "q1"),
            (("x0", "q0"), ("x0", "q1")),
        )


def test_presented_carrier_malformed_pairs_rejected() -> None:
    with pytest.raises(ValueError, match="pairs of string labels"):
        PresentedCarrier(
            ("x0", "x1"),
            ("q0", "q1"),
            (("x0", "q0", "extra"), ("x1", "q1")),  # type: ignore[arg-type]
        )


def test_permutation_isometry_envelope_unmatched_carrier_weights_rejected() -> None:
    envelope = PermutationIsometryEnvelope(2, (("q0", "q1"), ("q1", "q0")), ("q0", "q1"))
    unmatched_weights = IntegerWeights((("external_state", 7),))
    with pytest.raises(ValueError, match="weights keys must match envelope states exactly"):
        envelope.apply(unmatched_weights)
    # Matching carrier weights preserve total mass identically
    matched_weights = IntegerWeights((("q0", 4), ("q1", 3)))
    updated = envelope.apply(matched_weights)
    assert updated.total_mass == matched_weights.total_mass == 7
    assert updated.weight_of("q0") == 3
    assert updated.weight_of("q1") == 4


def test_phase_blind_readout_global_phase_not_relative_phase() -> None:
    # Pure global phase factor of -1: (1, 1) -> (-1, -1) has identical relative phase (ratio 1 for both components)
    v1 = (1.0 + 0j, 1.0 + 0j)
    v2 = (-1.0 + 0j, -1.0 + 0j)
    assert PhaseBlindReadout.fiber_relative_phase(v1, v2) is False

    # Pure global phase factor of i: (1, 1) -> (i, i) has no relative phase
    v_i = (1j, 1j)
    assert PhaseBlindReadout.fiber_relative_phase(v1, v_i) is False

    # True non-trivial relative phase: (1, 1) -> (1, -1)
    v_rel = (1.0 + 0j, -1.0 + 0j)
    assert PhaseBlindReadout.fiber_relative_phase(v1, v_rel) is True

    # All zeros has no relative phase
    v_zero = (0.0 + 0j, 0.0 + 0j)
    assert PhaseBlindReadout.fiber_relative_phase(v_zero, v_zero) is False

    # Mismatched supports
    v_supp1 = (1.0 + 0j, 0.0 + 0j)
    v_supp2 = (0.0 + 0j, 1.0 + 0j)
    assert PhaseBlindReadout.fiber_relative_phase(v_supp1, v_supp2) is False


def test_algebraic_nonfactorable_witness() -> None:
    witness = AlgebraicNonFactorableWitness()
    assert witness.is_algebraically_nonfactorable() is True
    assert witness.is_entangled() is True
    assert witness.determinant == 1
    assert "composite Hilbert" in AlgebraicNonFactorableWitness.__doc__


def test_literal_evidence_anchors_execution() -> None:
    assert len(EVIDENCE_ANCHORS) == 13
    for name, anchor in EVIDENCE_ANCHORS.items():
        assert callable(anchor), f"anchor {name} must be callable"
        result = anchor()
        assert result is not None, f"anchor {name} returned None"


# Executable finite evidence; AuthorityEffect: None.
