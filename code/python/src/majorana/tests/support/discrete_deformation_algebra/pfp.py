"""M5 — Proposal Fidelity Protocol frontend."""

from __future__ import annotations
from omega_engine_governance.contracts import ProposalEnvelope, FidelityPacket


class PfpFrontendEngine:
    def verify_proposal(
        self, envelope: ProposalEnvelope, raw_input: str
    ) -> FidelityPacket:
        shape_pass = bool(envelope.ephemeral_payload_ref) and bool(
            envelope.payload_sha256
        )
        semantic_pass = True
        for boundary in envelope.protected_boundaries:
            if boundary == "NO_UNSOUND_UNSAFE" and "unsafe" in raw_input.lower():
                semantic_pass = False
            elif boundary == "SORRY_FREE_LEAN" and (
                "sorry" in raw_input or "admit" in raw_input
            ):
                semantic_pass = False
        status = (
            "SHAPE_PASS_SEMANTIC_PASS"
            if shape_pass and semantic_pass
            else "SEMANTIC_FAILURE"
        )
        return FidelityPacket(
            proposal_envelope=envelope,
            family_verifier_id=f"PFP_VERIFIER_{envelope.family_id}",
            shape_check_passed=shape_pass,
            semantic_check_passed=semantic_pass,
            fidelity_report=f"Report: {status}",
            authority_effect="None",
        )


def false_green_blocked(
    *,
    local_checks_pass: bool,
    global_descent_present: bool,
    fluency_only: bool,
) -> dict:
    """False-green regression: local green without descent is Refusal, not PASS."""
    if fluency_only or (local_checks_pass and not global_descent_present):
        return {
            "routing": "Refusal",
            "reason": "false_green_local_without_descent",
            "authority_effect": "None",
            "banned_label_verified": False,
        }
    if local_checks_pass and global_descent_present:
        return {
            "routing": "ShapeChecked",
            "reason": "local_and_descent",
            "authority_effect": "None",
            "banned_label_verified": False,
        }
    return {
        "routing": "Refusal",
        "reason": "local_fail",
        "authority_effect": "None",
        "banned_label_verified": False,
    }



