from __future__ import annotations
"""M12 + M17 — Frozen golden pin for the canonical Rabbit GtlaReceipt, and
the owner's decided step-hygiene semantics.

THEORETICAL MINIMUM (M12)
  INVARIANT  The canonical Rabbit receipt's replay hash is the frozen hex
             below. Two same-process constructions cannot catch
             canonicalization drift; a cross-session constant can.
  BREAK      Any canonical-encoding change (key order, separators, field
             set) silently shifts every hash.
  WITNESS    Equality with GOLDEN_RABBIT_REPLAY_HASH, computed ONCE from the
             live owner on 2026-07-29 and corroborated byte-for-byte by the
             flagship artifact gtla/tests/receipts/rabbit_prompt_trace.json.
  MUTATION   Reorder or extend GtlaReceipt.canonical_payload -> red.

THEORETICAL MINIMUM (M17)
  INVARIANT  The owner's DECIDED hygiene semantics (pinned, not invented):
             extra step keys are declared-legal and hash-bound (carried into
             canonical bytes, never silently dropped); an empty layer_path
             constructs (a receipt may bind a zero-step trace).
  BREAK      Extra keys dropped from the canonical bytes would let smuggled
             step data ride outside the hash.
  WITNESS    replay_hash inequality between with/without the extra key.
  MUTATION   Strip non-axis keys in _checked_layer_path -> red.

AuthorityEffect: None throughout.
"""


import hashlib

from omega_engine.crates.discrete_deformation_algebra.rabbit_intake import (
    Prime001TransportReceipt,
    RABBIT_PROMPT,
    RabbitIntakePipeline,
    build_rabbit_loss_ledger,
)
from omega_engine.crates.discrete_deformation_algebra.receipt_emission import emit_gtla_receipt
from omega_engine.crates.replay import GtlaReceipt

# Computed ONCE from the live owner emission path (2026-07-29) and equal to
# the replay_hash frozen in the flagship artifact rabbit_prompt_trace.json.
GOLDEN_RABBIT_REPLAY_HASH = (
    "7d358e0ac309106ade2d6b6e83f125b2bfaec449d460c4ccae5b4f8e76712eec"
)


def _canonical_rabbit_receipt() -> GtlaReceipt:
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
    ).receipt


def _minimal_step(**extra) -> dict:
    step = {
        "diagnostic_class": "ExactClass",
        "routing_terminal": "CheckPassed",
        "extension_status": "NoExtensionNeeded",
        "authority_status": "None",
    }
    step.update(extra)
    return step


def _receipt(layer_path) -> GtlaReceipt:
    return GtlaReceipt(
        claim_id="HYGIENE_TEST",
        claim_sha256="a" * 64,
        scope="step-hygiene",
        layer_path=layer_path,
        dda_tape="E",
        residuals=(),
        debt=(),
        unresolved_obligations=(),
    )


class TestGoldenRabbitReplayHashPin:
    def test_canonical_rabbit_receipt_matches_the_frozen_golden(self) -> None:
        receipt = _canonical_rabbit_receipt()
        assert receipt.replay_hash == GOLDEN_RABBIT_REPLAY_HASH

    def test_canonical_bytes_are_stable_within_process_too(self) -> None:
        receipt = _canonical_rabbit_receipt()
        assert (
            receipt.canonical_bytes() == _canonical_rabbit_receipt().canonical_bytes()
        )


class TestStepHygieneDecidedSemantics:
    """M17: pin what the owner DECIDED, so any future change is a loud diff."""

    def test_extra_step_keys_are_declared_legal(self) -> None:
        receipt = _receipt((_minimal_step(step_id="s1", letter="E"),))
        assert receipt.layer_path[0]["step_id"] == "s1"

    def test_extra_step_keys_are_hash_bound_not_silently_dropped(self) -> None:
        bare = _receipt((_minimal_step(),))
        annotated = _receipt((_minimal_step(step_id="s1"),))
        # The extra key must ride INSIDE the canonical bytes: same receipt
        # with and without it must hash differently.
        assert annotated.replay_hash != bare.replay_hash
        assert b"step_id" in annotated.canonical_bytes()

    def test_empty_layer_path_is_legal_and_hash_stable(self) -> None:
        receipt = _receipt(())
        assert receipt.layer_path == ()
        assert receipt.replay_hash == _receipt(()).replay_hash


