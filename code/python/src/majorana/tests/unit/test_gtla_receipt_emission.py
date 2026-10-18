from __future__ import annotations
"""M7 — F10 narrative laundering through the owner emission path (OD-7).

THEORETICAL MINIMUM
  INVARIANT  A narrative sentence rides the sealed GtlaReceipt as DATA only:
             it changes no authority field, and one flipped character in it
             changes the canonical bytes so the frozen witness refuses. The
             owner refuses unterminalized traces and authority-widening steps
             in type.
  BREAK      A narrative (or its edit) slips into the receipt without moving
             the replay hash, or a widened step / unfinished trace emits.
  WITNESS    receipt.authority_effect / per-step authority_status; ValueError
             "replay hash mismatch" on the tampered variant;
             ReceiptEmissionRefusal tokens.
  MUTATION   In omega_replay.DescentWitness.from_verified_replay, accept any
             expected hash (drop the hmac comparison) -> the tamper rows red.

AuthorityEffect: None throughout.
"""


import dataclasses
import hashlib

import pytest

from omega_engine.crates.discrete_deformation_algebra.axis_adapter import AliasAdapterRefusal
from omega_engine.crates.discrete_deformation_algebra.dda import DdaTraceEngine
from omega_engine.crates.discrete_deformation_algebra.rabbit_intake import (
    Prime001TransportReceipt,
    RABBIT_PROMPT,
    RabbitIntakePipeline,
    build_rabbit_loss_ledger,
)
from omega_engine.crates.discrete_deformation_algebra.receipt_emission import (
    LETTER_EXTENSION,
    LETTER_ROUTING_DEFAULT,
    ReceiptEmissionRefusal,
    derive_step_axes,
    emit_gtla_receipt,
)
from omega_engine.crates.type.runtime_axes import (
    DdaLetter,
    DdaStepReceipt,
    ExtensionStatus,
    RoutingTerminal,
)
from omega_engine.crates.replay import DescentWitness, GtlaReceipt

NARRATIVE = (
    "NARRATIVE (data only): assuming exponential growth would give "
    "R(10) = R0*e^(10r); every symbol on the right is an unresolved residual."
)


def _rabbit_emission(unresolved_obligations=None):
    pipeline = RabbitIntakePipeline(RABBIT_PROMPT)
    packets = pipeline.build_diagnostic_packet_bundle()
    loss_ledger = build_rabbit_loss_ledger()
    prime001 = Prime001TransportReceipt(
        receipt_id="prime001_rabbit_v1",
        source_carrier="RabbitPrompt",
        target_carrier="SymbolicOdeCarrier",
        residual_preservation_verified=True,
    )
    engine, _tape = pipeline.execute_admitted_dda_trace(
        include_symbolic_carrier=True,
        loss_ledger=loss_ledger,
        lce_licensed=True,
        prime001_receipt=prime001,
    )
    return emit_gtla_receipt(
        claim_id="RABBIT_PROMPT_V1",
        claim_sha256=hashlib.sha256(RABBIT_PROMPT.encode("utf-8")).hexdigest(),
        scope="rabbit-intake-finite-example",
        engine=engine,
        diagnostic_bundle=packets,
        loss_ledger=loss_ledger,
        unresolved_obligations=unresolved_obligations,
    )


class TestNarrativeRidesAsDataOnly:
    def test_narrative_in_receipt_changes_no_authority_field(self) -> None:
        emission = _rabbit_emission(
            unresolved_obligations=(
                NARRATIVE,
                "MODEL_UNDERDECLARED",
                "MISSING_MODEL_PARAMETERS",
            )
        )
        receipt = emission.receipt
        assert NARRATIVE in receipt.unresolved_obligations
        assert receipt.authority_effect == "none"
        for step in receipt.layer_path:
            assert step["authority_status"] == "None"
        assert emission.witness.replay_hash == receipt.replay_hash

    def test_one_char_narrative_tamper_is_refused_by_the_frozen_witness(self) -> None:
        emission = _rabbit_emission(
            unresolved_obligations=(NARRATIVE, "MODEL_UNDERDECLARED")
        )
        original = emission.receipt
        tampered_narrative = NARRATIVE[:-1] + "!"
        assert tampered_narrative != NARRATIVE
        tampered = GtlaReceipt(
            claim_id=original.claim_id,
            claim_sha256=original.claim_sha256,
            scope=original.scope,
            layer_path=original.layer_path,
            dda_tape=original.dda_tape,
            residuals=original.residuals,
            debt=original.debt,
            unresolved_obligations=(tampered_narrative, "MODEL_UNDERDECLARED"),
        )
        assert tampered.replay_hash != original.replay_hash
        with pytest.raises(ValueError, match="replay hash mismatch"):
            DescentWitness.from_verified_replay(tampered, original.replay_hash)


class TestEmissionOwnerRefusals:
    def test_unterminalized_trace_refused(self) -> None:
        engine = DdaTraceEngine("unfinished")
        engine.emit_step(
            DdaLetter.E, "s0", "s1", "carrier", "ExactClass", "ExactClass", "w0"
        )
        with pytest.raises(
            ReceiptEmissionRefusal, match="UNTERMINALIZED_TRACE_REFUSED"
        ) as excinfo:
            emit_gtla_receipt(
                claim_id="X",
                claim_sha256="a" * 64,
                scope="s",
                engine=engine,
                diagnostic_bundle=(),
            )
        assert excinfo.value.token == "UNTERMINALIZED_TRACE_REFUSED"

    def test_widened_step_refused_by_derive_step_axes(self) -> None:
        widened = DdaStepReceipt(
            step_id="s_bad",
            letter=DdaLetter.E,
            input_state_hash="i",
            output_state_hash="o",
            carrier_hash="c",
            diagnostic_before="ExactClass",
            diagnostic_after="ExactClass",
            required_witness="w",
            witness_hash="wh",
            authority_effect="LocalGreen",
        )
        with pytest.raises(
            ReceiptEmissionRefusal, match="AUTHORITY_WIDENING_REFUSED"
        ) as excinfo:
            derive_step_axes(widened)
        assert excinfo.value.token == "AUTHORITY_WIDENING_REFUSED"

    def test_widened_step_inside_a_terminalized_trace_refuses_whole_emission(
        self,
    ) -> None:
        engine = DdaTraceEngine("widened")
        engine.emit_step(
            DdaLetter.T, "s0", "terminal", "carrier", "ExactClass", "ExactClass", "w0"
        )
        engine.receipts.append(
            dataclasses.replace(engine.receipts[0], authority_effect="LocalGreen")
        )
        with pytest.raises(ReceiptEmissionRefusal, match="AUTHORITY_WIDENING_REFUSED"):
            emit_gtla_receipt(
                claim_id="X",
                claim_sha256="a" * 64,
                scope="s",
                engine=engine,
                diagnostic_bundle=(),
            )

    def test_unregistered_diagnostic_token_fails_closed_not_unavailable(self) -> None:
        bad_step = DdaStepReceipt(
            step_id="s_tok",
            letter=DdaLetter.E,
            input_state_hash="i",
            output_state_hash="o",
            carrier_hash="c",
            diagnostic_before="Closed",
            diagnostic_after="Closed",
            required_witness="w",
            witness_hash="wh",
        )
        with pytest.raises(AliasAdapterRefusal, match="UNKNOWN_TERMINAL_TOKEN_REFUSED"):
            derive_step_axes(bad_step)


class TestDeclaredLetterAdapter:
    def test_refusal_reason_on_non_r_step_reroutes_to_refusal(self) -> None:
        step = DdaStepReceipt(
            step_id="s_ref",
            letter=DdaLetter.E,
            input_state_hash="i",
            output_state_hash="o",
            carrier_hash="c",
            diagnostic_before="ExactClass",
            diagnostic_after="ExactClass",
            required_witness="w",
            witness_hash="wh",
            refusal_reason="TYPED_REFUSAL_ROUTE",
        )
        axes = derive_step_axes(step)
        assert axes["routing_terminal"] == RoutingTerminal.Refusal.value

    def test_lambda_step_routes_requires_lift_with_licensed_lift_extension(
        self,
    ) -> None:
        step = DdaStepReceipt(
            step_id="s_lift",
            letter=DdaLetter.LAMBDA,
            input_state_hash="i",
            output_state_hash="o",
            carrier_hash="c",
            diagnostic_before="ClosedResidual",
            diagnostic_after="ClosedResidual",
            required_witness="w",
            witness_hash="wh",
        )
        axes = derive_step_axes(step)
        assert axes["routing_terminal"] == RoutingTerminal.RequiresLift.value
        assert axes["extension_status"] == ExtensionStatus.LicensedLift.value
        assert axes["authority_status"] == "None"

    def test_letter_tables_cover_the_whole_alphabet(self) -> None:
        assert set(LETTER_ROUTING_DEFAULT) == set(DdaLetter)
        assert set(LETTER_EXTENSION) <= set(DdaLetter)


