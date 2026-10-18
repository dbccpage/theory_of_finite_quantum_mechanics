"""Attack matrix and contract tests for code_change_proposal_v1."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json

import pytest

from omega_engine_pfp.domain.shared_kernel.canonical import (
    CanonicalizationError,
)
from omega_engine_pfp.domain import (
    CODE_CHANGE_PACKET_FAMILY,
    CODE_CHANGE_PROPOSAL_SCHEMA,
    OBSTRUCTION_VERIFIER_RECEIPT_REQUIRED,
    REFUSAL_CANDIDATE_BUDGET_EXCEEDED,
    REFUSAL_GATE_FAILED,
    REFUSAL_MARKDOWN_CLAIM_INJECTION,
    REFUSAL_MODEL_VERDICT_UNTRUSTED,
    REFUSAL_PATCH_BYTES_ABSENT,
    REFUSAL_REFUSAL_ERASURE,
    REFUSAL_REQUIRED_GATE_MISSING,
    REFUSAL_TOUCHED_PATH_DECLARED_MISMATCH,
    REFUSAL_TOUCHED_PATH_OUTSIDE_OWNED,
    REFUSAL_TOUCHED_PATH_PROTECTED,
    REFUSAL_VERIFIED_PROPOSAL_FORBIDDEN,
    CodeChangeProposalPayloadV1,
    CodeChangeRunRootV1,
    GateReceiptV1,
    attach_candidate,
    bind_patch_bytes,
    build_code_change_proposal_envelope,
    derive_touched_paths_from_patch_bytes,
    evaluate_code_change_candidate,
    loads_strict_json,
    parse_code_change_proposal_envelope,
    render_code_change_run_root_markdown,
    verify_code_change_run_root,
    verify_markdown_does_not_mutate_claims,
    verify_patch_bytes,
)

try:
    from omega_engine_pfp.domain import (
        FABLE_V1_PACKET_ID,
    )
except (ImportError, AttributeError):
    FABLE_V1_PACKET_ID = (
        "0000000000000000000000000000000000000000000000000000000000000000"
    )


def _payload(**overrides: object) -> CodeChangeProposalPayloadV1:
    fields = {
        "objective": "publish strict code_change_proposal_v1 family",
        "source_revision": "deadbeefcafebabe0123456789abcdef01234567",
        "owned_paths": (
            "omega_engine/research/ooutwire_docs/anomalon/omega_engine/symbol_game/code_change_proposal_packets.py",
        ),
        "protected_paths": ("omega_engine/crates/omega_corrigibility/src/lib.rs",),
        "allowed_transforms": ("edit", "emit_evidence", "test"),
        "candidate_budget": 3,
        "operation_budget": 20,
        "required_gates": ("focused_tests", "lint", "replay"),
        "parent_packet_id": FABLE_V1_PACKET_ID,
    }
    fields.update(overrides)
    return CodeChangeProposalPayloadV1(**fields)  # type: ignore[arg-type]


def _envelope(payload: CodeChangeProposalPayloadV1 | None = None):
    payload = payload or _payload()
    return build_code_change_proposal_envelope(
        payload,
        task_id="code-change-proposal-v1-smoke",
    )


OWNED_PATH = (
    "omega_engine/research/ooutwire_docs/anomalon/"
    "omega_engine/symbol_game/code_change_proposal_packets.py"
)
PROTECTED_PATH = "omega_engine/crates/omega_corrigibility/src/lib.rs"


def _unified_diff_for(*paths: str, body_line: str = "+ok") -> bytes:
    chunks: list[str] = []
    for path in paths:
        chunks.append(
            f"diff --git a/{path} b/{path}\n"
            f"--- a/{path}\n"
            f"+++ b/{path}\n"
            f"@@ -1 +1 @@\n"
            f"-old\n"
            f"{body_line}\n"
        )
    return "".join(chunks).encode("utf-8")


def _patch(envelope, *, body: bytes | None = None, touched=None):
    payload = parse_code_change_proposal_envelope(envelope)
    if body is None:
        body = _unified_diff_for(OWNED_PATH)
    return bind_patch_bytes(
        packet_id=envelope.packet_id,
        producer_id="model-worker",
        base_source_revision=payload.source_revision,
        patch_encoding="unified-diff-utf8-lf-v1",
        patch_bytes=body,
        touched_paths=touched,
        claimed_summary="untrusted summary",
    )


def _pass_gates(envelope, candidate_id: str) -> tuple[GateReceiptV1, ...]:
    evidence = hashlib.sha256(b"host-gate-log\n").hexdigest()
    return tuple(
        GateReceiptV1(
            gate_id=gate_id,
            packet_id=envelope.packet_id,
            candidate_id=candidate_id,
            evaluator_id=f"host-{gate_id}",
            disposition="PASS",
            model_claimed_passed=True,  # retained; never controlling alone
            evidence_sha256=evidence,
            evidence_byte_count=14,
            refusal_codes=(),
        )
        for gate_id in ("focused_tests", "lint", "replay")
    )


def test_payload_and_envelope_round_trip_canonical_wire() -> None:
    payload = _payload()
    envelope = _envelope(payload)
    parsed_object = parse_code_change_proposal_envelope(envelope)
    parsed_wire = parse_code_change_proposal_envelope(envelope.to_dict())

    assert envelope.packet_family == CODE_CHANGE_PACKET_FAMILY
    assert envelope.authority_effect == "None"
    assert envelope.source_digest == payload.path_manifest_root
    assert envelope.initial_state_hash == payload.path_manifest_root
    assert envelope.parent_event_id == FABLE_V1_PACKET_ID
    assert payload.schema_version == CODE_CHANGE_PROPOSAL_SCHEMA
    assert parsed_object == payload
    assert parsed_wire == payload
    assert parsed_wire.payload_id == payload.payload_id
    assert _envelope(parsed_wire).packet_id == envelope.packet_id


def test_strict_payload_parser_refuses_unknown_and_missing_fields() -> None:
    wire = _payload().to_dict()
    unknown = deepcopy(wire)
    unknown["promotion_eligible"] = True
    missing = deepcopy(wire)
    del missing["path_manifest_root"]
    extra_gate_field = deepcopy(wire)
    extra_gate_field["verified"] = True

    for attack in (unknown, missing, extra_gate_field):
        with pytest.raises(CanonicalizationError):
            CodeChangeProposalPayloadV1.from_dict(attack)


def test_duplicate_json_keys_are_refused() -> None:
    text = '{"objective":"a","objective":"b"}'
    with pytest.raises(CanonicalizationError, match="duplicate JSON key"):
        loads_strict_json(text)


def test_owned_and_protected_paths_must_be_disjoint_sorted_and_nonempty() -> None:
    with pytest.raises(CanonicalizationError, match="nonempty"):
        _payload(owned_paths=())
    with pytest.raises(CanonicalizationError, match="disjoint"):
        _payload(
            owned_paths=("a/path.py",),
            protected_paths=("a/path.py",),
        )
    with pytest.raises(CanonicalizationError, match="unique and sorted"):
        _payload(owned_paths=("b/x.py", "a/x.py"))


@pytest.mark.parametrize(
    "path",
    (
        "../escape.py",
        "a/../b.py",
        "/abs/path.py",
        r"win\path.py",
        "./relative.py",
        "a//b.py",
        "C:/windows.py",
        "trailing.",
        "CON",
    ),
)
def test_paths_refuse_traversal_absolute_and_noncanonical_forms(path: str) -> None:
    with pytest.raises(CanonicalizationError, match="POSIX path"):
        _payload(owned_paths=(path,))


def test_authority_effect_must_be_none_on_payload_and_envelope() -> None:
    wire = _payload().to_dict()
    wire["authority_effect"] = "Promote"
    with pytest.raises(CanonicalizationError, match="AuthorityEffect None"):
        CodeChangeProposalPayloadV1.from_dict(wire)

    envelope_wire = _envelope().to_dict()
    envelope_wire["authority_effect"] = "Promote"
    with pytest.raises(CanonicalizationError, match="authority"):
        parse_code_change_proposal_envelope(envelope_wire)


def test_path_manifest_root_binds_owned_and_protected_paths() -> None:
    payload = _payload()
    wire = payload.to_dict()
    wire["owned_paths"] = [
        "omega_engine/research/ooutwire_docs/anomalon/_tests_unit/test_code_change_proposal_packets.py"
    ]
    with pytest.raises(CanonicalizationError, match="path_manifest_root"):
        CodeChangeProposalPayloadV1.from_dict(wire)


def test_patch_bytes_are_content_addressed_and_verified() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH, body_line="+line")
    patch = _patch(envelope, body=body)
    assert patch.patch_sha256 == hashlib.sha256(body).hexdigest()
    assert patch.patch_byte_count == len(body)
    assert patch.touched_paths == (OWNED_PATH,)
    verify_patch_bytes(patch, body)
    with pytest.raises(CanonicalizationError, match="PATCH_DIGEST_MISMATCH"):
        verify_patch_bytes(patch, body + b"tamper")


def test_attach_and_evaluate_happy_path_declared_unverified() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(
        envelope,
        patch,
        claimed_valid=True,  # model-authored; ignored for disposition
        claimed_terminal="LabExactCandidate",
    )
    gates = _pass_gates(envelope, candidate.candidate_id)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        gates,
        patch_bytes=body,
    )
    verified = verify_code_change_run_root(
        root,
        packet=envelope,
        candidate=candidate,
        patch=patch,
        patch_bytes=body,
        gate_receipts=gates,
    )

    # Declared gate PASS is not independent verification.
    assert verified.terminal_status == "DeclaredUnverified"
    assert OBSTRUCTION_VERIFIER_RECEIPT_REQUIRED in verified.open_obstruction_ids
    assert "BUDGET_HOST_STATE_ABSENT" in verified.open_obstruction_ids
    assert "SOURCE_REVISION_UNBOUND" in verified.open_obstruction_ids
    assert verified.refusals == ()
    assert verified.authority_effect == "None"
    assert verified.task_packet_id == envelope.packet_id
    assert candidate.claimed_valid is True  # retained only


def test_candidate_patch_substitution_is_refused() -> None:
    envelope = _envelope()
    body_a = _unified_diff_for(OWNED_PATH, body_line="+a")
    body_b = _unified_diff_for(OWNED_PATH, body_line="+b")
    patch_a = _patch(envelope, body=body_a)
    patch_b = _patch(envelope, body=body_b)
    candidate = attach_candidate(envelope, patch_a)
    with pytest.raises(CanonicalizationError, match="CANDIDATE_PATCH_MISBIND"):
        evaluate_code_change_candidate(
            envelope,
            candidate,
            patch_b,
            _pass_gates(envelope, candidate.candidate_id),
            patch_bytes=body_b,
        )


def test_positive_terminal_verify_without_evidence_is_refused() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    gates = _pass_gates(envelope, candidate.candidate_id)
    root = evaluate_code_change_candidate(
        envelope, candidate, patch, gates, patch_bytes=body
    )
    with pytest.raises(
        CanonicalizationError, match="POSITIVE_TERMINAL_NEEDS_EVIDENCE_REPLAY"
    ):
        verify_code_change_run_root(root)


def test_forged_positive_terminal_with_zero_evidence_is_refused() -> None:
    with pytest.raises(CanonicalizationError):
        CodeChangeRunRootV1(
            task_packet_id="a" * 64,
            task_packet_sha256="b" * 64,
            candidate_ids=(),
            patch_ids=(),
            gate_receipt_ids=(),
            attempts=(),
            repairs=(),
            refusals=(),
            terminal_status="TransportValidated",
            open_obstruction_ids=(),
        )
    with pytest.raises(CanonicalizationError):
        CodeChangeRunRootV1(
            task_packet_id="a" * 64,
            task_packet_sha256="b" * 64,
            candidate_ids=(),
            patch_ids=(),
            gate_receipt_ids=(),
            attempts=(),
            repairs=(),
            refusals=(),
            terminal_status="DeclaredUnverified",
            open_obstruction_ids=(OBSTRUCTION_VERIFIER_RECEIPT_REQUIRED,),
        )


def test_verified_proposal_terminal_is_forbidden() -> None:
    with pytest.raises(
        CanonicalizationError, match=REFUSAL_VERIFIED_PROPOSAL_FORBIDDEN
    ):
        CodeChangeRunRootV1(
            task_packet_id="a" * 64,
            task_packet_sha256="b" * 64,
            candidate_ids=("c" * 64,),
            patch_ids=("d" * 64,),
            gate_receipt_ids=(),
            attempts=(),
            repairs=(),
            refusals=(),
            terminal_status="VerifiedProposal",
            open_obstruction_ids=(),
        )


def test_declared_touched_paths_must_match_host_derived_from_bytes() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    with pytest.raises(
        CanonicalizationError, match=REFUSAL_TOUCHED_PATH_DECLARED_MISMATCH
    ):
        bind_patch_bytes(
            packet_id=envelope.packet_id,
            producer_id="model-worker",
            base_source_revision=parse_code_change_proposal_envelope(
                envelope
            ).source_revision,
            patch_encoding="unified-diff-utf8-lf-v1",
            patch_bytes=body,
            # Lie: claim only owned while diff could be anything; mismatch vs derived
            touched_paths=(PROTECTED_PATH,),
        )
    derived = derive_touched_paths_from_patch_bytes("unified-diff-utf8-lf-v1", body)
    assert derived == (OWNED_PATH,)


@pytest.mark.parametrize(
    "body",
    (
        b"diff --git a/omega_engine/x.py b/omega_engine/x.py\n",
        b"diff --git a/omega_engine/x.py b/omega_engine/x.py\n"
        b"--- a/omega_engine/x.py\n+++ b/omega_engine/x.py\n"
        b"@@ -1 +1 @@\n-old\n",
        b"diff --git a/omega_engine/x.py b/omega_engine/x.py\n"
        b"--- a/omega_engine/x.py\n+++ b/omega_engine/x.py\n"
        b"@@ -1 +1 @@\n-old\n+new\n+extra\n",
    ),
)
def test_host_diff_parser_refuses_empty_truncated_and_overlong_hunks(
    body: bytes,
) -> None:
    with pytest.raises(CanonicalizationError, match="unified-diff patch is invalid"):
        derive_touched_paths_from_patch_bytes("unified-diff-utf8-lf-v1", body)


def test_host_diff_parser_accepts_git_quoted_paths_with_spaces() -> None:
    path = "omega_engine/crates/symbol_game/a file.py"
    body = (
        f'diff --git "a/{path}" "b/{path}"\n'
        f'--- "a/{path}"\n'
        f'+++ "b/{path}"\n'
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
    ).encode("utf-8")
    assert derive_touched_paths_from_patch_bytes("unified-diff-utf8-lf-v1", body) == (
        path,
    )


def test_protected_file_patch_is_typed_refusal() -> None:
    envelope = _envelope()
    body = _unified_diff_for(PROTECTED_PATH)
    patch = bind_patch_bytes(
        packet_id=envelope.packet_id,
        producer_id="model-worker",
        base_source_revision=parse_code_change_proposal_envelope(
            envelope
        ).source_revision,
        patch_encoding="unified-diff-utf8-lf-v1",
        patch_bytes=body,
    )
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        (),
        patch_bytes=body,
    )
    assert root.terminal_status == "TypedRefusal"
    assert REFUSAL_TOUCHED_PATH_OUTSIDE_OWNED in root.refusals
    assert REFUSAL_TOUCHED_PATH_PROTECTED in root.refusals


def test_missing_patch_bytes_is_typed_refusal() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        _pass_gates(envelope, candidate.candidate_id),
        patch_bytes=None,
    )
    assert root.terminal_status == "TypedRefusal"
    assert REFUSAL_PATCH_BYTES_ABSENT in root.refusals


def test_touched_path_outside_owned_is_typed_refusal() -> None:
    envelope = _envelope()
    outside = "omega_engine/crates/omega_solvers/src/lib.rs"
    body = _unified_diff_for(outside)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        _pass_gates(envelope, candidate.candidate_id),
        patch_bytes=body,
    )
    assert root.terminal_status == "TypedRefusal"
    assert REFUSAL_TOUCHED_PATH_OUTSIDE_OWNED in root.refusals


def test_touched_protected_path_is_typed_refusal() -> None:
    envelope = _envelope()
    with pytest.raises(CanonicalizationError, match="disjoint"):
        _payload(
            owned_paths=(
                PROTECTED_PATH,
                OWNED_PATH,
            ),
            protected_paths=(PROTECTED_PATH,),
        )
    body = _unified_diff_for(PROTECTED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        _pass_gates(envelope, candidate.candidate_id),
        patch_bytes=body,
    )
    assert REFUSAL_TOUCHED_PATH_PROTECTED in root.refusals
    assert REFUSAL_TOUCHED_PATH_OUTSIDE_OWNED in root.refusals


def test_missing_required_gate_is_typed_refusal() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    only_lint = (
        GateReceiptV1(
            gate_id="lint",
            packet_id=envelope.packet_id,
            candidate_id=candidate.candidate_id,
            evaluator_id="host-lint",
            disposition="PASS",
            model_claimed_passed=None,
            evidence_sha256="a" * 64,
            evidence_byte_count=0,
            refusal_codes=(),
        ),
    )
    root = evaluate_code_change_candidate(
        envelope, candidate, patch, only_lint, patch_bytes=body
    )
    assert root.terminal_status == "TypedRefusal"
    assert REFUSAL_REQUIRED_GATE_MISSING in root.refusals
    assert "GATE_ABSENT:focused_tests" in root.open_obstruction_ids


def test_gate_fail_disposition_controls_outcome_not_model_passed() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch, claimed_valid=True)
    evidence = "b" * 64
    receipts = (
        GateReceiptV1(
            gate_id="lint",
            packet_id=envelope.packet_id,
            candidate_id=candidate.candidate_id,
            evaluator_id="host-lint",
            disposition="FAIL",
            model_claimed_passed=True,  # model lies
            evidence_sha256=evidence,
            evidence_byte_count=1,
            refusal_codes=("LINT_ERROR",),
        ),
        GateReceiptV1(
            gate_id="focused_tests",
            packet_id=envelope.packet_id,
            candidate_id=candidate.candidate_id,
            evaluator_id="host-tests",
            disposition="PASS",
            model_claimed_passed=False,
            evidence_sha256=evidence,
            evidence_byte_count=1,
            refusal_codes=(),
        ),
        GateReceiptV1(
            gate_id="replay",
            packet_id=envelope.packet_id,
            candidate_id=candidate.candidate_id,
            evaluator_id="host-replay",
            disposition="PASS",
            model_claimed_passed=None,
            evidence_sha256=evidence,
            evidence_byte_count=1,
            refusal_codes=(),
        ),
    )
    root = evaluate_code_change_candidate(
        envelope, candidate, patch, receipts, patch_bytes=body
    )
    assert root.terminal_status == "TypedRefusal"
    assert REFUSAL_GATE_FAILED in root.refusals
    assert REFUSAL_MODEL_VERDICT_UNTRUSTED in root.refusals
    assert "LINT_ERROR" in root.refusals


def test_gate_receipt_refuses_passed_and_promotion_fields() -> None:
    envelope = _envelope()
    candidate_id = "c" * 64
    good = GateReceiptV1(
        gate_id="lint",
        packet_id=envelope.packet_id,
        candidate_id=candidate_id,
        evaluator_id="host-lint",
        disposition="PASS",
        model_claimed_passed=None,
        evidence_sha256="d" * 64,
        evidence_byte_count=0,
        refusal_codes=(),
    ).to_dict()
    attack = deepcopy(good)
    attack["passed"] = True
    with pytest.raises(CanonicalizationError, match="untrusted|passed"):
        GateReceiptV1.from_dict(attack)
    attack2 = deepcopy(good)
    attack2["promotion_eligible"] = True
    with pytest.raises(CanonicalizationError, match="forbidden"):
        GateReceiptV1.from_dict(attack2)


def test_candidate_budget_exhaustion_is_typed() -> None:
    envelope = _envelope(_payload(candidate_budget=1))
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        _pass_gates(envelope, candidate.candidate_id),
        prior_candidate_count=1,
        patch_bytes=body,
    )
    assert root.terminal_status == "BudgetExhausted"
    assert REFUSAL_CANDIDATE_BUDGET_EXCEEDED in root.refusals


def test_markdown_cannot_erase_refusals_or_add_claims() -> None:
    envelope = _envelope()
    outside = "omega_engine/crates/omega_solvers/src/lib.rs"
    body = _unified_diff_for(outside)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        _pass_gates(envelope, candidate.candidate_id),
        patch_bytes=body,
    )
    markdown = render_code_change_run_root_markdown(root)
    verify_markdown_does_not_mutate_claims(root, markdown)
    assert REFUSAL_TOUCHED_PATH_OUTSIDE_OWNED in root.refusals
    assert f"`{REFUSAL_TOUCHED_PATH_OUTSIDE_OWNED}`" in markdown

    erased = markdown.replace(f"`{REFUSAL_TOUCHED_PATH_OUTSIDE_OWNED}`", "`HIDDEN`")
    with pytest.raises(CanonicalizationError, match=REFUSAL_REFUSAL_ERASURE):
        verify_markdown_does_not_mutate_claims(root, erased)

    injected = markdown + "\npromotion_eligible: true\n"
    with pytest.raises(CanonicalizationError, match=REFUSAL_MARKDOWN_CLAIM_INJECTION):
        verify_markdown_does_not_mutate_claims(root, injected)


def test_run_root_refuses_unknown_fields_and_authority_booleans() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        _pass_gates(envelope, candidate.candidate_id),
        patch_bytes=body,
    )
    wire = root.to_dict()
    wire["promotion_eligible"] = True
    with pytest.raises(CanonicalizationError, match="forbidden|unknown"):
        CodeChangeRunRootV1.from_dict(wire)
    missing = root.to_dict()
    del missing["terminal_status"]
    with pytest.raises(CanonicalizationError, match="missing fields"):
        CodeChangeRunRootV1.from_dict(missing)


def test_family_identity_is_not_research_claim_or_research_packets() -> None:
    envelope = _envelope()
    assert envelope.packet_family == "code_change_proposal_v1"
    assert envelope.packet_family != "research_claim_v1"
    payload = parse_code_change_proposal_envelope(envelope)
    assert payload.family == "code_change_proposal"
    assert "research" not in payload.family


def test_positive_terminal_cannot_retain_refusals() -> None:
    envelope = _envelope()
    body = _unified_diff_for(OWNED_PATH)
    patch = _patch(envelope, body=body)
    candidate = attach_candidate(envelope, patch)
    root = evaluate_code_change_candidate(
        envelope,
        candidate,
        patch,
        _pass_gates(envelope, candidate.candidate_id),
        patch_bytes=body,
    )
    wire = root.to_dict()
    wire["refusals"] = ["FORGED"]
    forged = deepcopy(wire)
    del forged["run_root_id"]
    rebuilt = {
        **forged,
        "run_root_id": "e" * 64,
    }
    with pytest.raises(CanonicalizationError):
        CodeChangeRunRootV1.from_dict(rebuilt)
