"""
Packet Firewall Host and Three-Layer Verification Protocol.

This module implements:
1. The 4-field packet kernel: (contract, task, payload, parent_hash).
2. Closed-operator first-token linter policing mandatory evidence verbs.
3. Explicit Unicode codepoint pinning for carrier alphabet.
4. The Three Firewalls: FW-CARRIER, FW-MOVE, FW-REPLAY fail-closed.
5. SHA-256 content-addressed derivation event DAG.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

DECLARED_OPERATORS: Set[str] = {
    "ASSERT",
    "CUT",
    "REDUCE",
    "PROVE",
    "VERIFY",
    "RETRACT",
    "REFUSE",
}


def is_valid_carrier_codepoint(cp: int) -> bool:
    """
    Standard Unicode codepoint ranges for carrier validation.
    ASCII basic Latin (32..126), Greek uppercase (0x0391..0x03A9), Greek lowercase (0x03B1..0x03C9),
    and logic/relation symbols (->, |-, bot, ==, delta, Phi).
    """
    if 32 <= cp <= 126:
        return True
    if 0x0391 <= cp <= 0x03A9:
        return True
    if 0x03B1 <= cp <= 0x03C9:
        return True
    if cp in {0x2192, 0x22A2, 0x22A5, 0x2261, 0x03B4, 0x03A6}:
        return True
    return False


class FirewallRefusalCode(Enum):
    """Refusal codes for Three-Layer Sovereign Firewalls."""
    FW_CARRIER_VIOLATION = "FW_CARRIER_VIOLATION"
    FW_MOVE_VIOLATION = "FW_MOVE_VIOLATION"
    FW_REPLAY_VIOLATION = "FW_REPLAY_VIOLATION"
    OP_UNDECLARED = "OP_UNDECLARED"
    HASH_MISMATCH = "HASH_MISMATCH"


@dataclass(frozen=True)
class PacketKernel:
    """The 4-field core packet envelope."""
    contract: str = "CONTRACT_SG_V1"
    task: str = "T01"
    payload: Any = field(default_factory=dict)
    parent_hash: Optional[str] = None

    def compute_hash(self) -> str:
        """Computes deterministic SHA-256 content digest."""
        serialized = json.dumps(
            {
                "contract": self.contract,
                "task": self.task,
                "payload": self.payload,
                "parent_hash": self.parent_hash,
            },
            sort_keys=True,
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class DerivationStep:
    """Candidate derivation move proposed by proposer (LLM)."""
    op: str
    position: int
    rule_id: str
    substitution: Dict[str, str]
    pre_state_hash: str
    post_state_hash: str
    content: str


@dataclass
class FirewallVerdict:
    """Result of host firewall evaluation."""
    admitted: bool
    refusal_code: Optional[FirewallRefusalCode] = None
    reason: Optional[str] = None
    verified_post_hash: Optional[str] = None


def is_valid_sha256(h: str) -> bool:
    """True iff h is a valid 64-character hexadecimal SHA-256 digest."""
    return isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdefABCDEF" for c in h)


class PacketFirewallHost:
    """
    Host-side independent verification oracle executing the Three Firewalls fail-closed.
    """

    def __init__(self, carrier_alphabet: Optional[Set[str]] = None):
        self.carrier_alphabet = carrier_alphabet

    def lint_first_token_op(self, statement: str) -> Tuple[bool, Optional[str]]:
        """
        Enforces that the first token of every statement is in DECLARED_OPERATORS.
        """
        tokens = statement.strip().split()
        if not tokens:
            return False, "Statement is empty"
        first_op = tokens[0].upper()
        if first_op not in DECLARED_OPERATORS:
            return False, f"Operator '{first_op}' is undeclared. Mandatory first token must be in {sorted(DECLARED_OPERATORS)}"
        return True, first_op

    def check_fw_carrier(self, text: str) -> FirewallVerdict:
        """
        FW-CARRIER: Asserts that all characters belong to the pinned carrier codepoint set.
        """
        for char in text:
            cp = ord(char)
            if self.carrier_alphabet is not None:
                if char not in self.carrier_alphabet:
                    return FirewallVerdict(
                        admitted=False,
                        refusal_code=FirewallRefusalCode.FW_CARRIER_VIOLATION,
                        reason=f"Character '{char}' (U+{cp:04X}) violates pinned carrier alphabet.",
                    )
            else:
                if not is_valid_carrier_codepoint(cp):
                    return FirewallVerdict(
                        admitted=False,
                        refusal_code=FirewallRefusalCode.FW_CARRIER_VIOLATION,
                        reason=f"Codepoint U+{cp:04X} outside declared carrier.",
                    )
        return FirewallVerdict(admitted=True)

    def check_fw_move(self, step: DerivationStep, licensed_rules: Dict[str, Any]) -> FirewallVerdict:
        """
        FW-MOVE: Verifies that rule_id is declared, licensed, and priced.
        """
        valid_op, op_err = self.lint_first_token_op(step.op)
        if not valid_op:
            return FirewallVerdict(
                admitted=False,
                refusal_code=FirewallRefusalCode.OP_UNDECLARED,
                reason=op_err,
            )

        if step.rule_id not in licensed_rules:
            return FirewallVerdict(
                admitted=False,
                refusal_code=FirewallRefusalCode.FW_MOVE_VIOLATION,
                reason=f"Rule '{step.rule_id}' is not in licensed rule schema (unpriced move / smuggled axiom).",
            )
        return FirewallVerdict(admitted=True)

    def check_fw_replay(
        self,
        current_state_str: str,
        step: DerivationStep,
        apply_fn: Any,
    ) -> FirewallVerdict:
        """
        FW-REPLAY: Recomputes state transition independently and checks SHA-256 digests.
        """
        computed_pre_hash = hashlib.sha256(current_state_str.encode("utf-8")).hexdigest()
        if computed_pre_hash != step.pre_state_hash:
            return FirewallVerdict(
                admitted=False,
                refusal_code=FirewallRefusalCode.HASH_MISMATCH,
                reason=f"Pre-state hash mismatch: computed {computed_pre_hash[:8]} != claimed {step.pre_state_hash[:8]}",
            )

        next_state_str = apply_fn(current_state_str, step.position, step.rule_id, step.substitution)

        v_post_carrier = self.check_fw_carrier(next_state_str)
        if not v_post_carrier.admitted:
            return v_post_carrier

        computed_post_hash = hashlib.sha256(next_state_str.encode("utf-8")).hexdigest()

        if computed_post_hash != step.post_state_hash:
            return FirewallVerdict(
                admitted=False,
                refusal_code=FirewallRefusalCode.FW_REPLAY_VIOLATION,
                reason=f"Post-state hash mismatch: host produced {computed_post_hash[:8]} != claimed {step.post_state_hash[:8]}",
                verified_post_hash=computed_post_hash,
            )

        return FirewallVerdict(admitted=True, verified_post_hash=computed_post_hash)

    def verify_step(
        self,
        step: DerivationStep,
        licensed_rules: Optional[Dict[str, Any]] = None,
    ) -> FirewallVerdict:
        """
        Evaluates carrier, hash format, and move licensing for a single derivation step (preflight).
        """
        if not is_valid_sha256(step.pre_state_hash) or not is_valid_sha256(step.post_state_hash):
            return FirewallVerdict(
                admitted=False,
                refusal_code=FirewallRefusalCode.HASH_MISMATCH,
                reason="Invalid state hash format: pre and post hashes must be valid 64-hex SHA-256 digests.",
            )
        v_carrier = self.check_fw_carrier(step.content)
        if not v_carrier.admitted:
            return v_carrier
        if licensed_rules is not None:
            v_move = self.check_fw_move(step, licensed_rules)
            if not v_move.admitted:
                return v_move
            return FirewallVerdict(
                admitted=False,
                refusal_code=FirewallRefusalCode.FW_REPLAY_VIOLATION,
                reason="Preflight move/carrier check passed; full host replay required for admission.",
            )
        return FirewallVerdict(
            admitted=False,
            refusal_code=FirewallRefusalCode.FW_MOVE_VIOLATION,
            reason="Licensed rules and full host replay are required",
        )

    def evaluate_pipeline(
        self,
        current_state_str: str,
        step: DerivationStep,
        licensed_rules: Dict[str, Any],
        apply_fn: Any,
    ) -> FirewallVerdict:
        """
        Sequential execution through FW-CARRIER -> FW-MOVE -> FW-REPLAY.
        """
        if not is_valid_sha256(step.pre_state_hash) or not is_valid_sha256(step.post_state_hash):
            return FirewallVerdict(
                admitted=False,
                refusal_code=FirewallRefusalCode.HASH_MISMATCH,
                reason="Invalid state hash format: pre and post hashes must be valid 64-hex SHA-256 digests.",
            )

        v_pre = self.check_fw_carrier(current_state_str)
        if not v_pre.admitted:
            return v_pre

        v_carrier = self.check_fw_carrier(step.content)
        if not v_carrier.admitted:
            return v_carrier

        v_move = self.check_fw_move(step, licensed_rules)
        if not v_move.admitted:
            return v_move

        v_replay = self.check_fw_replay(current_state_str, step, apply_fn)
        return v_replay


__all__ = [
    "DECLARED_OPERATORS",
    "is_valid_carrier_codepoint",
    "FirewallRefusalCode",
    "PacketKernel",
    "DerivationStep",
    "FirewallVerdict",
    "PacketFirewallHost",
]
