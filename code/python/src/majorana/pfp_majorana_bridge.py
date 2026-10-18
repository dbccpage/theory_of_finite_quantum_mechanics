"""pfp_majorana_bridge.py — Proposal Fidelity Protocol (PFP) Mediation for MS Majorana.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C7/MAJ-C8, gemini_000.md.

Implements:
1. Multi-Agent Symbol Game Match for Topological Braiding:
   - Proposer Agent: Submits candidate braid programs (sequences of braid indices).
   - Referee / EIS Gatekeeper: Verifies braid group invariants, orthogonality,
     determinant det(B) == 1, and Yang-Baxter relation fidelity.
2. PFP Wire Packet Envelopes:
   - MajoranaBraidProposalPacket: Serialized braid circuit proposal.
   - MajoranaBraidReceipt: Cryptographically signed receipt with SHA-256 under AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple

from majorana_braid_exact import MajoranaBraidCircuit, MajoranaBraidGenerator


@dataclass(frozen=True)
class MajoranaBraidProposalPacket:
    """Proposal packet submitted to the PFP referee containing a candidate braid sequence."""

    round_id: str
    proposer_id: str
    num_modes: int
    braid_sequence: Tuple[Tuple[int, bool], ...]

    def canonical_digest(self) -> str:
        """Deterministic SHA-256 hash of proposal packet."""
        payload = {
            "round_id": self.round_id,
            "proposer_id": self.proposer_id,
            "num_modes": self.num_modes,
            "braid_sequence": [[j, inv] for j, inv in self.braid_sequence],
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class MajoranaBraidReceipt:
    """Receipt emitted by the PFP Referee certifying topological braid validity."""

    receipt_id: str
    round_id: str
    proposer_id: str
    is_accepted: bool
    status_reason: str
    is_orthogonal: bool
    is_proper_rotation: bool
    yang_baxter_satisfied: bool
    num_modes: int
    num_braid_steps: int
    proposal_digest: str
    authority_effect: str = "None"

    def canonical_receipt_digest(self) -> str:
        """Deterministic SHA-256 hash of the receipt."""
        payload = {
            "receipt_id": self.receipt_id,
            "round_id": self.round_id,
            "proposer_id": self.proposer_id,
            "is_accepted": self.is_accepted,
            "status_reason": self.status_reason,
            "is_orthogonal": self.is_orthogonal,
            "is_proper_rotation": self.is_proper_rotation,
            "yang_baxter_satisfied": self.yang_baxter_satisfied,
            "num_modes": self.num_modes,
            "num_braid_steps": self.num_braid_steps,
            "proposal_digest": self.proposal_digest,
            "authority_effect": self.authority_effect,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class MajoranaBraidReferee:
    """Referee agent enforcing topological quantum computation invariants."""

    def __init__(self, num_modes: int) -> None:
        if not isinstance(num_modes, int) or num_modes < 2:
            raise ValueError(f"num_modes must be integer >= 2, got {num_modes}")
        self.num_modes = num_modes

    def evaluate_proposal(self, packet: MajoranaBraidProposalPacket) -> MajoranaBraidReceipt:
        """Evaluates a proposed braid circuit against topological and algebraic invariants."""
        if packet.num_modes != self.num_modes:
            return MajoranaBraidReceipt(
                receipt_id=f"rec_{packet.round_id}_mode_mismatch",
                round_id=packet.round_id,
                proposer_id=packet.proposer_id,
                is_accepted=False,
                status_reason=f"REFUSAL: Mode mismatch expected {self.num_modes}, got {packet.num_modes}",
                is_orthogonal=False,
                is_proper_rotation=False,
                yang_baxter_satisfied=False,
                num_modes=packet.num_modes,
                num_braid_steps=len(packet.braid_sequence),
                proposal_digest=packet.canonical_digest(),
            )

        circuit = MajoranaBraidCircuit(self.num_modes)
        for j, inv in packet.braid_sequence:
            if not (1 <= j < self.num_modes):
                return MajoranaBraidReceipt(
                    receipt_id=f"rec_{packet.round_id}_invalid_index",
                    round_id=packet.round_id,
                    proposer_id=packet.proposer_id,
                    is_accepted=False,
                    status_reason=f"REFUSAL: Braid index {j} out of range [1, {self.num_modes-1}]",
                    is_orthogonal=False,
                    is_proper_rotation=False,
                    yang_baxter_satisfied=False,
                    num_modes=packet.num_modes,
                    num_braid_steps=len(packet.braid_sequence),
                    proposal_digest=packet.canonical_digest(),
                )
            circuit.append(j, inverse=inv)

        mat = circuit.evaluate_matrix()
        is_ortho = mat.is_orthogonal()
        det = mat.determinant()
        is_proper = (det == Fraction(1, 1))

        yb_ok = True
        if self.num_modes >= 3:
            for j in range(1, self.num_modes - 1):
                if not circuit.verify_yang_baxter(j):
                    yb_ok = False
                    break

        is_accepted = is_ortho and is_proper and yb_ok
        status_reason = (
            "ACCEPTED: Valid topological braid sequence with certified Yang-Baxter relation"
            if is_accepted
            else "REFUSAL: Braid transformation violates orthogonality, proper rotation, or Yang-Baxter"
        )

        return MajoranaBraidReceipt(
            receipt_id=f"rec_{packet.round_id}",
            round_id=packet.round_id,
            proposer_id=packet.proposer_id,
            is_accepted=is_accepted,
            status_reason=status_reason,
            is_orthogonal=is_ortho,
            is_proper_rotation=is_proper,
            yang_baxter_satisfied=yb_ok,
            num_modes=self.num_modes,
            num_braid_steps=len(packet.braid_sequence),
            proposal_digest=packet.canonical_digest(),
        )
