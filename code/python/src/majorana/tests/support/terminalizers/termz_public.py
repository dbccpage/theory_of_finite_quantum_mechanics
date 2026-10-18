"""Public-safe projection of a diagnostic certificate.

Maps internal terminal statuses to public labels and strips internal vocabulary
(EPK, Symbol Game, operator algebra, normal forms, coboundary, residual). The
public certificate reports only: what was checked, what failed, what can be
repaired, and what must not be treated as authoritative.
"""

from __future__ import annotations
from typing import Any, Dict, List

from omega_engine.crates.omega_mvp.models import OmegaCertificate, TerminalStatus

TS = TerminalStatus

# Internal terminal status -> public label.
PUBLIC_TERMINAL_LABELS: Dict[TerminalStatus, str] = {
    TS.PACKETIZED: "Scoped",
    TS.PARSED: "Scoped",
    TS.BOUNDARY_CHECKED: "BoundaryChecked",
    TS.EVIDENCE_ONLY: "BoundaryChecked",
    TS.REDACTED_REASONING: "RedactedReasoning",
    TS.REFUSED_REASONING_LEAK: "RedactedReasoning",
    TS.REFUSED_OVERCLAIM: "OverclaimRefused",
    TS.REFUSED_UNDERSPECIFIED: "RepairRequired",
    TS.REPAIR_REQUIRED: "RepairRequired",
    TS.PARSE_ERROR: "MalformedInput",
    TS.QUANTUM_PACKET_VALID: "QuantumPacketValid",
    TS.QUANTUM_PACKET_INVALID: "QuantumPacketInvalid",
    TS.QUANTUM_CHANNEL_VALID: "QuantumChannelValid",
    TS.CHANNEL_REFUSED: "ChannelRefused",
    TS.CANDIDATE_WITH_RESIDUAL: "RepairRequired",
    TS.SOLVED_RELATIVE_TO_PACKET: "BoundaryChecked",
    TS.REFUSED: "Refused",
}

# Operator class -> public, jargon-free repair description.
_REPAIR_TEXT = {
    "C": "Expose a missing context or field",
    "E": "Apply an exact repair",
    "R": "Apply a minimal repair",
    "I": "Recognize a structural symmetry",
    "M": "Refuse unsafe or overclaiming content",
}

# Human-readable failure descriptions (no internal vocabulary).
_FAILURE_TEXT = {
    "chain_of_thought_leak": "Hidden reasoning detected and removed",
    "overclaim": "Unsupported certainty claim",
    "underspecified": "Request is missing required details",
    "json_parse_error": "Input is not valid structured data",
}


def _violation_label(v: str) -> str:
    for key, text in _FAILURE_TEXT.items():
        if v.startswith(key):
            return text
    if v.startswith("trace_not_one"):
        return "Probability does not sum to one"
    if v.startswith("negative_eigenvalue"):
        return "Negative probability detected"
    if v.startswith("non_hermitian"):
        return "Object is not a valid quantum state"
    if v.startswith("not_trace_preserving"):
        return "Transformation does not conserve probability"
    if "shape" in v or "no_kraus" in v:
        return "Malformed mathematical object"
    return "Validation issue"


def _trace_consistency(cert: OmegaCertificate) -> Dict[str, Any]:
    """Public 'trace consistency diagnostics' (EPK renamed, internals hidden)."""
    d = cert.epk.defects
    vals = [d.delta_e, d.delta_p, d.delta_c, d.delta_r, d.delta_total]
    has_defect = any(abs(x or 0.0) > 1e-9 for x in vals)
    if not cert.epk.enabled or all(x is None for x in vals):
        return {"checked": False}
    if not has_defect:
        return {"checked": True, "status": "Consistent"}
    # Local-green / global-red surfaces as a public defect label.
    label = (
        "GlobalConsistencyFailure" if (d.delta_e or 0.0) != 0.0 else "CompositionDefect"
    )
    return {"checked": True, "status": label}


def public_certificate(cert: OmegaCertificate) -> Dict[str, Any]:
    """Project a diagnostic certificate to its public, internal-name-free form."""
    classes = [s.operator_class for s in cert.operator_trace]

    failures: List[str] = [_violation_label(v) for v in cert.qm.violations]
    if (
        cert.terminal_status in (TS.QUANTUM_PACKET_INVALID, TS.CHANNEL_REFUSED)
        and not failures
    ):
        failures.append("Invalid mathematical object")

    tc = _trace_consistency(cert)
    public_status = PUBLIC_TERMINAL_LABELS.get(
        cert.terminal_status, str(cert.terminal_status.value)
    )
    if tc.get("status") == "GlobalConsistencyFailure":
        public_status = "GlobalConsistencyFailure"
        failures.append("Global consistency failure across composed steps")

    checked: List[str] = []
    if cert.qm.density_matrix_valid is not None:
        checked.append("Quantum state validity (Hermitian, unit trace, positivity)")
    if cert.qm.channel_valid is not None:
        checked.append("Quantum channel validity (probability conservation)")
    if tc.get("checked"):
        checked.append("Trace consistency across composed steps")
    if cert.terminal_status in (TS.BOUNDARY_CHECKED, TS.EVIDENCE_ONLY, TS.PACKETIZED):
        checked.append("Scope and boundary of the output")
    if any(v.startswith("chain_of_thought_leak") for v in cert.qm.violations):
        checked.append("Hidden-reasoning policy boundary")

    repairs = [_REPAIR_TEXT.get(c, "Repair") for c in classes if c != "M"]
    refused = any(c == "M" for c in classes)

    return {
        "input_id": cert.input_id,
        "status": public_status,
        "checked": checked or ["Input shape"],
        "failures": failures,
        "repairs_available": repairs,
        "refused": refused,
        "trace_consistency": tc,
        "authority": {
            "is_authoritative": False,
            "note": "Diagnostic certificate. This output is scoped and checkable, "
            "not authoritative, unless a full terminal proof is attached.",
        },
        "certificate_kind": "diagnostic",
    }


