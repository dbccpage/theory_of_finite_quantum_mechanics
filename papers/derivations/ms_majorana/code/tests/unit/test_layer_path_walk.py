from __future__ import annotations
"""M9 — The full layer-path walk: claim -> trichotomy -> authority gate ->
compression conservation -> sealed GtlaReceipt -> bound DescentWitness.

THEORETICAL MINIMUM
  INVARIANT  One executable composition carries the Rabbit claim through
             classify_gtfoc_trichotomy, validate_gtfda_authority, the
             compression validators, and the owner receipt emission; every
             step carries the four axes with registry tokens; authority is
             None at every point; the witness binds the exact bytes.
  BREAK      Pre-repair OD-7: no non-test code composed the walk — the
             layer-path story had no executable owner.
  WITNESS    The frozen tape "C · E · E · C · R · Λ · D · I · T", the
             six bundle fingerprints in bundle order, the sorted debt ids,
             per-step axis-token membership, witness.replay_hash equality.
  MUTATION   In receipt_emission.derive_step_axes, emit authority_status
             from the step's raw field instead of the literal after the
             check (or widen it) -> receipt construction refuses -> red.

AuthorityEffect: None throughout.
"""


import hashlib

import pytest

from omega_engine.crates.discrete_deformation_algebra.rabbit_intake import (
    Prime001TransportReceipt,
    RABBIT_PROMPT,
    RabbitIntakePipeline,
    build_rabbit_loss_ledger,
)
from omega_engine.crates.discrete_deformation_algebra.receipt_emission import emit_gtla_receipt
from omega_engine.crates.discrete_deformation_algebra.tower_boundary import (
    GtfocTerminalClass,
    classify_gtfoc_trichotomy,
    validate_gtfda_authority,
    validate_gtla_summary_compression,
    validate_gtla_summary_compression_multiset,
)
from omega_engine.crates.type.runtime_axes import (
    DiagnosticClass,
    ExtensionStatus,
    RoutingTerminal,
)

EXPECTED_TAPE = "C · E · E · C · R · Λ · D · I · T"
FOUR_AXES = (
    "diagnostic_class",
    "routing_terminal",
    "extension_status",
    "authority_status",
)


@pytest.fixture(scope="module")
def walk():
    """Run the whole walk once; every test asserts on the same composition."""
    prompt_sha256 = hashlib.sha256(RABBIT_PROMPT.encode("utf-8")).hexdigest()
    pipeline = RabbitIntakePipeline(RABBIT_PROMPT)
    packets = pipeline.build_diagnostic_packet_bundle()
    loss_ledger = build_rabbit_loss_ledger()
    prime001 = Prime001TransportReceipt(
        receipt_id="prime001_rabbit_v1",
        source_carrier="RabbitPrompt",
        target_carrier="SymbolicOdeCarrier",
        residual_preservation_verified=True,
    )
    engine, tape = pipeline.execute_admitted_dda_trace(
        include_symbolic_carrier=True,
        loss_ledger=loss_ledger,
        lce_licensed=True,
        prime001_receipt=prime001,
    )
    emission = emit_gtla_receipt(
        claim_id="RABBIT_PROMPT_V1",
        claim_sha256=prompt_sha256,
        scope="rabbit-intake-finite-example",
        engine=engine,
        diagnostic_bundle=packets,
        loss_ledger=loss_ledger,
    )
    return {
        "prompt_sha256": prompt_sha256,
        "packets": packets,
        "loss_ledger": loss_ledger,
        "engine": engine,
        "tape": tape,
        "emission": emission,
    }


class TestWalkStage1TrichotomyAndAuthorityGate:
    def test_every_bundle_packet_is_diagnostic_only_authority_none(self, walk) -> None:
        assert len(walk["packets"]) == 6
        for pkt in walk["packets"]:
            assert pkt.authority_effect == "None"
            assert pkt.support_grade == "DiagnosticOnly"

    def test_open_residual_families_classify_open_not_exact(self, walk) -> None:
        for pkt in walk["packets"]:
            cls = classify_gtfoc_trichotomy(
                pkt.family_id, is_repaired=False, is_missing_fields=True
            )
            assert cls is GtfocTerminalClass.Open

    def test_no_authority_without_descent_packet_on_the_walk_answer(self) -> None:
        assert (
            validate_gtfda_authority(
                "R(10) remains unevaluated pending residual discharge",
                None,
                "None",
            )
            == "R_nopacket"
        )
        with pytest.raises(ValueError, match="R_nopacket"):
            validate_gtfda_authority("R(10) = 22026", None, "Certified")


class TestWalkStage2CompressionConservation:
    def test_faithful_compression_passes_both_validators(self, walk) -> None:
        fingerprints = [pkt.residual_fingerprint for pkt in walk["packets"]]
        routes = sorted(
            pkt.witness_or_refusal["refusal_route"]
            for pkt in walk["packets"]
            if isinstance(pkt.witness_or_refusal.get("refusal_route"), str)
        )
        validate_gtla_summary_compression(
            set(fingerprints), set(routes), set(fingerprints), set(routes)
        )
        validate_gtla_summary_compression_multiset(
            fingerprints, routes, fingerprints, routes
        )

    def test_dropping_one_real_fingerprint_refuses(self, walk) -> None:
        fingerprints = [pkt.residual_fingerprint for pkt in walk["packets"]]
        with pytest.raises(
            ValueError, match="OBLIGATION_COMPRESSION_LAUNDERING_REFUSED"
        ):
            validate_gtla_summary_compression(
                set(fingerprints), set(), set(fingerprints[1:]), set()
            )


class TestWalkStage3SealedReceiptAndWitness:
    def test_tape_is_the_frozen_licensed_walk(self, walk) -> None:
        receipt = walk["emission"].receipt
        assert walk["tape"] == EXPECTED_TAPE
        assert receipt.dda_tape == EXPECTED_TAPE
        assert walk["engine"].get_tape_string() == EXPECTED_TAPE

    def test_every_step_carries_the_four_axes_with_registry_tokens(self, walk) -> None:
        receipt = walk["emission"].receipt
        assert len(receipt.layer_path) == 9
        diagnostic_tokens = {m.value for m in DiagnosticClass}
        routing_tokens = {m.value for m in RoutingTerminal}
        extension_tokens = {m.value for m in ExtensionStatus}
        for step in receipt.layer_path:
            for axis in FOUR_AXES:
                assert axis in step
            assert step["diagnostic_class"] in diagnostic_tokens
            assert step["routing_terminal"] in routing_tokens
            assert step["extension_status"] in extension_tokens
            assert step["authority_status"] == "None"

    def test_residuals_are_the_bundle_fingerprints_in_bundle_order(self, walk) -> None:
        receipt = walk["emission"].receipt
        assert receipt.residuals == tuple(
            pkt.residual_fingerprint for pkt in walk["packets"]
        )

    def test_debt_is_the_sorted_unresolved_loss_ids(self, walk) -> None:
        receipt = walk["emission"].receipt
        expected_debt = tuple(
            sorted(
                entry.loss_id
                for entry in walk["loss_ledger"].entries.values()
                if entry.discharge_status == "unresolved"
            )
        )
        assert receipt.debt == expected_debt
        assert len(receipt.debt) == 6

    def test_obligations_are_the_typed_refusal_routes(self, walk) -> None:
        receipt = walk["emission"].receipt
        assert receipt.unresolved_obligations == (
            "MISSING_MODEL_PARAMETERS",
            "MODEL_UNDERDECLARED",
            "OUTPUT_TYPE_UNRESOLVED",
            "TASK_CONTRACT_AMBIGUOUS",
            "UNIT_POLICY_AMBIGUOUS",
        )

    def test_witness_binds_the_receipt_bytes_and_authority_stays_none(
        self, walk
    ) -> None:
        emission = walk["emission"]
        assert emission.witness.replay_hash == emission.receipt.replay_hash
        assert emission.witness.trace_packet is emission.receipt
        assert emission.receipt.authority_effect == "none"
        assert emission.authority_effect == "None"
        assert emission.receipt.claim_sha256 == walk["prompt_sha256"]


