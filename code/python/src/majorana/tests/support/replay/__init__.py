"""Deterministic, evidence-only replay packets.

This Python mirror deliberately does not certify mathematical truth or mint
authority. It binds a canonical trace packet to a SHA-256 digest so an
independent host can replay the exact same bytes.
"""

from __future__ import annotations
from dataclasses import asdict as asdict, dataclass as dataclass
import hashlib
import hmac
import json
import re
from typing import Any as Any, Dict as Dict, Tuple as Tuple


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

_FOUR_AXES = (
    "diagnostic_class",
    "routing_terminal",
    "extension_status",
    "authority_status",
)

_DIAGNOSTIC_CLASS_TOKENS = frozenset(
    {
        "ExactClass",
        "ClosedResidual",
        "ActiveClosureFailure",
        "DetectorInadequate",
        "NotComputed",
    }
)
_ROUTING_TERMINAL_TOKENS = frozenset(
    {
        "ShapeChecked",
        "CheckPassed",
        "Repair",
        "Refusal",
        "OracleNeeded",
        "NoRule",
        "BudgetUnknown",
        "RequiresLift",
    }
)
_EXTENSION_STATUS_TOKENS = frozenset(
    {
        "NoExtensionNeeded",
        "ExtensionRequested",
        "LicensedLift",
        "ExtensionRefused",
    }
)

_AXIS_TOKEN_SETS = {
    "diagnostic_class": ("DiagnosticClass", _DIAGNOSTIC_CLASS_TOKENS),
    "routing_terminal": ("RoutingTerminal", _ROUTING_TERMINAL_TOKENS),
    "extension_status": ("ExtensionStatus", _EXTENSION_STATUS_TOKENS),
}


def _require_sha256(value: str, field_name: str) -> None:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a lowercase SHA-256 hex digest")


def _checked_layer_path(steps: Any) -> Tuple[Dict[str, Any], ...]:
    """Validate and freeze a GTLA layer path: each step carries the four axes.

    Law: every step's ``diagnostic_class`` / ``routing_terminal`` /
    ``extension_status`` value must be a registry token of its OWN axis
    (token sets mirrored above from
    ``omega_discrete_deformation_algebra.types``); unknown or wrong-axis
    tokens raise ``ValueError`` fail-closed. ``authority_status`` must be
    the literal ``'None'`` on every step — the receipt mints no authority.
    """

    if isinstance(steps, (str, bytes)) or not isinstance(steps, (list, tuple)):
        raise ValueError("layer_path must be a tuple of per-step four-axis dicts")
    checked = []
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            raise ValueError(
                f"layer_path[{index}] must be a dict carrying the four axes"
            )
        for axis in _FOUR_AXES:
            if axis not in step:
                raise ValueError(
                    f"layer_path[{index}] is missing required axis '{axis}'"
                )
            if not isinstance(step[axis], str) or not step[axis]:
                raise ValueError(
                    f"layer_path[{index}].{axis} must be a non-empty string"
                )
        for axis, (axis_enum_name, tokens) in _AXIS_TOKEN_SETS.items():
            value = step[axis]
            if value not in tokens:
                raise ValueError(
                    f"layer_path[{index}].{axis} carries unregistered token "
                    f"'{value}' ({axis_enum_name} axis; legal tokens: "
                    f"{sorted(tokens)})"
                )
        if step["authority_status"] != "None":
            raise ValueError(
                f"layer_path[{index}].authority_status must be 'None' "
                f"(got '{step['authority_status']}')"
            )
        checked.append(dict(step))
    return tuple(checked)


def _checked_str_tuple(values: Any, field_name: str) -> Tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        raise ValueError(f"{field_name} must be a tuple of strings")
    out = []
    for index, value in enumerate(values):
        if not isinstance(value, str):
            raise ValueError(f"{field_name}[{index}] must be a string")
        out.append(value)
    return tuple(out)


@dataclass(frozen=True)
class ReplayTracePacket:
    """Canonical replay carrier for one proposed sweep step.

    A replay hash proves byte-for-byte stability of this packet only. It does
    not prove the paper claim, a coboundary identity, or an authority result.
    """

    paper_sha256: str
    proposal_sha256: str
    gate_receipt_sha256: str
    loop_pass: int
    step_index: int
    status: str
    authority_effect: str = "none"
    schema_version: str = "omega.replay_trace.v1"

    def __post_init__(self) -> None:
        _require_sha256(self.paper_sha256, "paper_sha256")
        _require_sha256(self.proposal_sha256, "proposal_sha256")
        _require_sha256(self.gate_receipt_sha256, "gate_receipt_sha256")
        if self.loop_pass < 1 or self.step_index < 1:
            raise ValueError("loop_pass and step_index must be positive")
        if not self.status:
            raise ValueError("status must be non-empty")
        if self.authority_effect != "none":
            raise ValueError("replay trace packets must carry AuthorityEffect::None")

    def canonical_payload(self) -> Dict[str, Any]:
        return asdict(self)

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.canonical_payload(),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    @property
    def replay_hash(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


@dataclass(frozen=True)
class GtlaReceipt:
    """Canonical GTLA descent receipt (sealed sibling of ReplayTracePacket).

    Binds one finite GTLA trace — claim identity, frozen scope, per-layer
    four-axis steps (diagnostic_class / routing_terminal / extension_status /
    authority_status), the DDA tape, and the residual/debt/obligation ledgers —
    to a canonical byte encoding. The replay hash proves byte-for-byte
    stability of this receipt only. It does not prove the claim, and it mints
    no authority: every layer step must carry ``authority_status == 'None'``
    and the receipt itself must carry ``authority_effect == 'none'``.
    """

    claim_id: str
    claim_sha256: str
    scope: str
    layer_path: Tuple[Dict[str, Any], ...]
    dda_tape: str
    residuals: Tuple[str, ...]
    debt: Tuple[str, ...]
    unresolved_obligations: Tuple[str, ...]
    authority_effect: str = "none"
    schema_version: str = "omega.gtla_receipt.v1"

    def __post_init__(self) -> None:
        if not isinstance(self.claim_id, str) or not self.claim_id:
            raise ValueError("claim_id must be a non-empty string")
        _require_sha256(self.claim_sha256, "claim_sha256")
        if not isinstance(self.scope, str) or not self.scope:
            raise ValueError("scope must be a non-empty string")
        if not isinstance(self.dda_tape, str):
            raise ValueError("dda_tape must be a string of DDA letters")
        object.__setattr__(self, "layer_path", _checked_layer_path(self.layer_path))
        for field_name in ("residuals", "debt", "unresolved_obligations"):
            object.__setattr__(
                self,
                field_name,
                _checked_str_tuple(getattr(self, field_name), field_name),
            )
        if self.authority_effect != "none":
            raise ValueError("gtla receipts must carry AuthorityEffect::None")
        if self.schema_version != "omega.gtla_receipt.v1":
            raise ValueError("schema_version must be 'omega.gtla_receipt.v1'")

    def canonical_payload(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "claim_id": self.claim_id,
            "claim_sha256": self.claim_sha256,
            "scope": self.scope,
            "layer_path": [dict(step) for step in self.layer_path],
            "dda_tape": self.dda_tape,
            "residuals": list(self.residuals),
            "debt": list(self.debt),
            "unresolved_obligations": list(self.unresolved_obligations),
            "authority_effect": self.authority_effect,
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.canonical_payload(),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    @property
    def replay_hash(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


class DescentWitness:
    """Sealed binding between a canonical trace packet and an expected hash.

    Sealing is BEST-EFFORT (Inspector M18): Python has no private fields,
    so a sufficiently determined caller can still reach the name-mangled
    class key. The seal blocks casual/accidental construction and makes
    forgery loud in review; it is an honesty check, not a cryptographic
    unforgeability guarantee.
    """

    __sealed_key = object()

    def __init__(
        self,
        key: object,
        trace_packet: "ReplayTracePacket | GtlaReceipt",
        replay_hash: str,
    ) -> None:
        if key is not DescentWitness.__sealed_key:
            raise TypeError(
                "DescentWitness construction is sealed; use from_verified_replay()"
            )
        self.trace_packet = trace_packet
        self.replay_hash = replay_hash

    @property
    def trace_or_packet(self) -> "ReplayTracePacket | GtlaReceipt":
        """Compatibility alias for the original prototype surface."""

        return self.trace_packet

    @classmethod
    def from_verified_replay(
        cls,
        trace_packet: "ReplayTracePacket | GtlaReceipt",
        expected_replay_hash: str,
    ) -> "DescentWitness":
        """Recompute and bind the canonical packet hash.

        The caller must supply the independently retained expected digest.
        Arbitrary strings and untyped objects are refused.
        """

        if not isinstance(trace_packet, (ReplayTracePacket, GtlaReceipt)):
            raise TypeError(
                "DescentWitness requires a ReplayTracePacket or GtlaReceipt"
            )
        _require_sha256(expected_replay_hash, "expected_replay_hash")
        computed = trace_packet.replay_hash
        if not hmac.compare_digest(computed, expected_replay_hash):
            raise ValueError("replay hash mismatch")
        return cls(cls.__sealed_key, trace_packet, computed)

    def __repr__(self) -> str:
        return f"DescentWitness(replay_hash={self.replay_hash!r})"


from .replay import (
    ReplayKernel,
    ReplayReport,
    VerifiedReplayReport,
    ReplayStatus,
    verify_replay_contract,
)

__all__ = [
    "ReplayTracePacket",
    "GtlaReceipt",
    "DescentWitness",
    "ReplayKernel",
    "ReplayReport",
    "VerifiedReplayReport",
    "ReplayStatus",
    "verify_replay_contract",
]

