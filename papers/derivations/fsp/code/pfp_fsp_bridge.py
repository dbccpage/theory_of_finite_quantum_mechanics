"""pfp_fsp_bridge.py — Proposal Fidelity Protocol (PFP) Mediation for FSP 4D SU(2).

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Paper 011, gemini_000.md.

Implements:
1. Multi-Agent Symbol Game Match Architecture:
   - Proposer Agent: Proposes 4D lattice link updates and cluster moves.
   - Referee / EIS Gatekeeper: Verifies unitarity, det(U) == 1, and orientation-reversing
     involution tau symmetry.
2. PFP Wire Packet Envelopes:
   - FspLinkProposal: Single link candidate mutation.
   - FspPfpProposalPacket: Full round update candidate with action delta.
   - FspPfpReceipt: Cryptographic witness receipt stamped with SHA-256 under AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple

from su2_link_holonomy_4d import ExactRationalSU2, Lattice4DCoord, Lattice4DSU2


@dataclass(frozen=True)
class FspLinkProposal:
    """Individual link update proposal."""

    x0: int
    x1: int
    x2: int
    x3: int
    mu: int
    candidate_link: ExactRationalSU2

    def to_dict(self) -> Dict[str, Any]:
        return {
            "coord": [self.x0, self.x1, self.x2, self.x3],
            "mu": self.mu,
            "components": [
                str(self.candidate_link.a0),
                str(self.candidate_link.a1),
                str(self.candidate_link.a2),
                str(self.candidate_link.a3),
            ],
        }


@dataclass(frozen=True)
class FspPfpProposalPacket:
    """Complete round proposal packet submitted to the PFP referee."""

    round_id: str
    proposer_id: str
    lattice_dims: Tuple[int, int, int, int]
    proposals: Tuple[FspLinkProposal, ...]
    declared_initial_action: Fraction
    declared_delta_action: Fraction

    def canonical_digest(self) -> str:
        """Computes deterministic SHA-256 hash of proposal payload."""
        payload = {
            "round_id": self.round_id,
            "proposer_id": self.proposer_id,
            "lattice_dims": list(self.lattice_dims),
            "proposals": [p.to_dict() for p in self.proposals],
            "declared_initial_action": str(self.declared_initial_action),
            "declared_delta_action": str(self.declared_delta_action),
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class FspPfpReceipt:
    """Receipt emitted by the PFP Referee certifying proposal fidelity and physical validity."""

    receipt_id: str
    round_id: str
    proposer_id: str
    is_accepted: bool
    status_reason: str
    unitarity_verified: bool
    determinant_verified: bool
    involution_pairing_verified: bool
    computed_initial_action: Fraction
    computed_final_action: Fraction
    computed_delta_action: Fraction
    proposal_digest: str
    authority_effect: str = "None"

    def canonical_receipt_digest(self) -> str:
        """Computes SHA-256 digest of the receipt."""
        payload = {
            "receipt_id": self.receipt_id,
            "round_id": self.round_id,
            "proposer_id": self.proposer_id,
            "is_accepted": self.is_accepted,
            "status_reason": self.status_reason,
            "unitarity_verified": self.unitarity_verified,
            "determinant_verified": self.determinant_verified,
            "involution_pairing_verified": self.involution_pairing_verified,
            "computed_initial_action": str(self.computed_initial_action),
            "computed_final_action": str(self.computed_final_action),
            "computed_delta_action": str(self.computed_delta_action),
            "proposal_digest": self.proposal_digest,
            "authority_effect": self.authority_effect,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class FspPfpReferee:
    """Referee agent enforcing physical laws and proposal fidelity in FSP."""

    def __init__(self, lattice: Lattice4DSU2) -> None:
        self.lattice = lattice

    def evaluate_proposal(
        self,
        packet: FspPfpProposalPacket,
        random_threshold: Fraction = Fraction(1, 2),
    ) -> FspPfpReceipt:
        """Evaluates a proposed link update packet against physical invariants and acceptance rules."""
        if not (Fraction(0, 1) <= random_threshold <= Fraction(1, 1)):
            raise ValueError(f"Random threshold must be in [0, 1], got {random_threshold}")

        initial_action = self.lattice.total_wilson_action()

        all_unitary = True
        all_det_one = True
        for prop in packet.proposals:
            if not prop.candidate_link.is_unitary():
                all_unitary = False
            if prop.candidate_link.determinant() != Fraction(1, 1):
                all_det_one = False

        if not all_unitary or not all_det_one:
            return FspPfpReceipt(
                receipt_id=f"rec_{packet.round_id}_unitarity_refusal",
                round_id=packet.round_id,
                proposer_id=packet.proposer_id,
                is_accepted=False,
                status_reason="REFUSAL: Candidate links violate SU(2) unitarity or determinant",
                unitarity_verified=all_unitary,
                determinant_verified=all_det_one,
                involution_pairing_verified=False,
                computed_initial_action=initial_action,
                computed_final_action=initial_action,
                computed_delta_action=Fraction(0, 1),
                proposal_digest=packet.canonical_digest(),
            )

        saved_links = []
        for prop in packet.proposals:
            coord = Lattice4DCoord(prop.x0, prop.x1, prop.x2, prop.x3, self.lattice.dims)
            saved_links.append((coord, prop.mu, self.lattice.get_link(coord, prop.mu)))
            self.lattice.set_link(coord, prop.mu, prop.candidate_link)

        candidate_action = self.lattice.total_wilson_action()
        computed_delta = candidate_action - initial_action

        inv_check = self.lattice.verify_involution_sign_balance()
        inv_verified = bool(inv_check["sign_cancellation_certified"])

        is_accepted = False
        status_reason = ""

        if not inv_verified:
            is_accepted = False
            status_reason = "REFUSAL: Involution tau sign balance breached"
        elif computed_delta <= Fraction(0, 1):
            is_accepted = True
            status_reason = "ACCEPTED: Action descending or stationary (Delta S <= 0)"
        else:
            alpha = Fraction(1, 1) / (Fraction(1, 1) + computed_delta)
            if random_threshold <= alpha:
                is_accepted = True
                status_reason = f"ACCEPTED: Metropolis rational ratio {alpha} >= {random_threshold}"
            else:
                is_accepted = False
                status_reason = f"REJECTED: Metropolis rational ratio {alpha} < {random_threshold}"

        if not is_accepted:
            for coord, mu, link in saved_links:
                self.lattice.set_link(coord, mu, link)
            final_action = initial_action
        else:
            final_action = candidate_action

        return FspPfpReceipt(
            receipt_id=f"rec_{packet.round_id}",
            round_id=packet.round_id,
            proposer_id=packet.proposer_id,
            is_accepted=is_accepted,
            status_reason=status_reason,
            unitarity_verified=all_unitary,
            determinant_verified=all_det_one,
            involution_pairing_verified=inv_verified,
            computed_initial_action=initial_action,
            computed_final_action=final_action,
            computed_delta_action=computed_delta,
            proposal_digest=packet.canonical_digest(),
        )
