# -*- coding: utf-8 -*-
"""
coda_fda_core.py: Finite *standing-authorization* gate for CODA-FDA.

Vocabulary (GTLA dual — do not collapse):
- AuthStanding: type shape for operational standing witnesses under setting S
- Authorization: process that may inhabit AuthStanding (packet + derived guards)
- AuthorityEffect: always "None" in this research package (no mint)

Trust Boundary Disclosure:
This module evaluates caller-supplied attestations. The separate
coda_fda_pipeline module executes a finite harness. Neither establishes
semantic verifier soundness.

Exact Rational Arithmetic Invariant:
All algebraic decisions, residual masses, and tolerance thresholds are computed
using exact rational numbers (sympy.Rational / fractions.Fraction). IEEE 754
floating-point numbers and boolean values passed where numerical values are
expected strictly raise TypeError.

Boolean Field Strictness:
Boolean attestation fields require `type(val) is bool`. Truthy strings (e.g. "False"),
integers (1/0), and containers strictly raise TypeError.

Guard g3 (zero_residual_mass) Invariant:
g3 requires exact rational vanishing: residual_mass == 0. When an exact quotient
certificate is supplied, certificate.verify() is executed and its distance must
strictly equal evidence.residual_mass.

Guard g5 (exhaustive) Invariant:
g5 verifies candidate coverage against declared candidate identifiers in DescentPacket.

AuthorityEffect: None
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Optional, Sequence, Tuple, Union

from cochain_presentation import LinearRepairProblem, QuotientDistanceCertificate
from sympy import Integer, Rational
from sympy.matrices.matrixbase import MatrixBase

# Exact rational refusal residual constants for diagnostic branches.
RESIDUAL_NO_PACKET = Rational(1, 1)
RESIDUAL_GUARD_FAIL_NONZERO = Rational(1, 2)
RESIDUAL_GUARD_FAIL_OTHER = Rational(1, 5)
RESIDUAL_AUTH_STANDING = Rational(0, 1)


class RefusalCode(str, Enum):
    """Formal refusal taxonomy for CODA-FDA authorization gate."""

    R_nopacket = "R_nopacket"
    R_candidate = "R_candidate"
    R_unreplayable = "R_unreplayable"
    R_contradictory_evidence = "R_contradictory_evidence"
    R_obstruction = "R_obstruction"


# String constants for backward compatibility
R_NOPACKET = RefusalCode.R_nopacket.value
R_CANDIDATE = RefusalCode.R_candidate.value
R_UNREPLAYABLE = RefusalCode.R_unreplayable.value
R_CONTRADICTORY_EVIDENCE = RefusalCode.R_contradictory_evidence.value
R_OBSTRUCTION = RefusalCode.R_obstruction.value


def _validate_exact_bool(val: Any, name: str) -> bool:
    """Ensure value is strictly a bool (type(val) is bool), rejecting strings, ints, floats."""
    if type(val) is not bool:
        raise TypeError(f"{name} must be strictly a bool, got {type(val).__name__} ({val!r})")
    return val


def _validate_exact_rational(val: Any, name: str) -> Rational:
    """Ensure value is an exact rational or integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, float) or (getattr(val, "dtype", None) is not None and "float" in str(val.dtype)):
        raise TypeError(f"{name} must be an exact rational or integer, got float (floats strictly forbidden)")
    if isinstance(val, (int, Integer, Fraction, Rational)):
        return Rational(val)
    if isinstance(val, str):
        try:
            return Rational(val)
        except Exception as exc:
            raise TypeError(f"{name} string could not be converted to exact Rational: {exc}") from exc
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


def _validate_exact_int(val: Any, name: str) -> int:
    """Ensure value is an exact non-negative integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    if not isinstance(val, (int, Integer)) or "float" in str(getattr(val, "dtype", "")):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    int_val = int(val)
    if int_val < 0:
        raise ValueError(f"{name} must be non-negative, got {int_val}")
    return int_val


@dataclass(frozen=True)
class DescentPacket:
    """Five-field finite descent packet data (K, E, V, tau, Lambda)."""

    carrier_k: str
    evaluator_class_e: Sequence[str]
    verifier_v: str
    terminalizer_tau: str
    discipline_lambda: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "evaluator_class_e", tuple(self.evaluator_class_e))

    def is_valid(self) -> bool:
        names = (self.carrier_k, self.verifier_v, self.terminalizer_tau, self.discipline_lambda)
        return (
            all(isinstance(value, str) and bool(value.strip()) for value in names)
            and bool(self.evaluator_class_e)
            and all(isinstance(value, str) and bool(value.strip()) for value in self.evaluator_class_e)
            and len(set(self.evaluator_class_e)) == len(self.evaluator_class_e)
        )


@dataclass(frozen=True)
class GuardEvidence:
    """
    Evidence and host attestations from which halt guards are derived.

    The Python companion evaluates caller-supplied attestations; it does not
    itself execute the four-stage pipeline or establish semantic verifier soundness.
    Each field must be justified by a finite check performed by the caller.
    """

    pipeline_accepted: bool
    replay_deterministic: bool
    residual_mass: Rational
    residual_zero_tol: Rational
    skeleton_preserved: bool
    candidates_checked: int
    candidates_declared: int
    pending_lifts: int
    active_refusal: bool
    checked_candidate_ids: Optional[Tuple[str, ...]] = None

    def __init__(
        self,
        pipeline_accepted: bool,
        replay_deterministic: bool,
        residual_mass: Union[int, Rational, Fraction, str],
        residual_zero_tol: Union[int, Rational, Fraction, str] = Rational(0, 1),
        skeleton_preserved: bool = True,
        candidates_checked: int = 1,
        candidates_declared: int = 1,
        pending_lifts: int = 0,
        active_refusal: bool = False,
        checked_candidate_ids: Optional[Sequence[str]] = None,
    ) -> None:
        object.__setattr__(self, "pipeline_accepted", _validate_exact_bool(pipeline_accepted, "pipeline_accepted"))
        object.__setattr__(self, "replay_deterministic", _validate_exact_bool(replay_deterministic, "replay_deterministic"))

        validated_mass = _validate_exact_rational(residual_mass, "residual_mass")
        if validated_mass < 0:
            raise ValueError(f"residual_mass must be non-negative, got {validated_mass}")
        object.__setattr__(self, "residual_mass", validated_mass)

        validated_tol = _validate_exact_rational(residual_zero_tol, "residual_zero_tol")
        if validated_tol < 0:
            raise ValueError(f"residual_zero_tol must be non-negative, got {validated_tol}")
        object.__setattr__(self, "residual_zero_tol", validated_tol)

        object.__setattr__(self, "skeleton_preserved", _validate_exact_bool(skeleton_preserved, "skeleton_preserved"))
        object.__setattr__(self, "candidates_checked", _validate_exact_int(candidates_checked, "candidates_checked"))
        object.__setattr__(self, "candidates_declared", _validate_exact_int(candidates_declared, "candidates_declared"))
        object.__setattr__(self, "pending_lifts", _validate_exact_int(pending_lifts, "pending_lifts"))
        object.__setattr__(self, "active_refusal", _validate_exact_bool(active_refusal, "active_refusal"))

        if checked_candidate_ids is not None:
            c_ids = tuple(str(cid) for cid in checked_candidate_ids)
            if len(set(c_ids)) != len(c_ids):
                raise ValueError(f"checked_candidate_ids contains duplicate entries: {c_ids}")
            checked_int = getattr(self, "candidates_checked")
            if len(c_ids) != checked_int:
                raise ValueError(
                    f"candidates_checked ({checked_int}) does not match length of checked_candidate_ids ({len(c_ids)})"
                )
            object.__setattr__(self, "checked_candidate_ids", c_ids)
        else:
            object.__setattr__(self, "checked_candidate_ids", None)


# Honest alias per Republication Review §3.4
GuardAttestations = GuardEvidence


@dataclass(frozen=True)
class HaltGuards:
    """Seven-guard halt witness conjunction vector (derived from evidence/attestations)."""

    accepted: bool
    deterministic: bool
    zero_residual_mass: bool
    skeleton_preserving: bool
    exhaustive: bool
    no_pending_lift: bool
    no_refusal: bool

    def __post_init__(self) -> None:
        for name in (
            "accepted",
            "deterministic",
            "zero_residual_mass",
            "skeleton_preserving",
            "exhaustive",
            "no_pending_lift",
            "no_refusal",
        ):
            _validate_exact_bool(getattr(self, name), name)

    def is_auth(self) -> bool:
        """IsAuth(t) <-> conjunction of seven derived guards (definitional)."""
        return (
            self.accepted
            and self.deterministic
            and self.zero_residual_mass
            and self.skeleton_preserving
            and self.exhaustive
            and self.no_pending_lift
            and self.no_refusal
        )


def derive_guards(evidence: GuardEvidence, packet: Optional[DescentPacket] = None) -> HaltGuards:
    """
    Derive halt guards from GuardEvidence (authorization ladder step).

    Guard g3 (zero_residual_mass) requires exact vanishing: residual_mass == 0.
    Guard g5 (exhaustive) binds candidates to packet.evaluator_class_e when available.
    """
    # g3: exact rational vanishing
    zero_res = bool(evidence.residual_mass == 0)

    # g5: exhaustive candidate check
    if packet is not None and packet.evaluator_class_e:
        declared = len(packet.evaluator_class_e)
        if evidence.checked_candidate_ids is None:
            exhaustive = False
        else:
            exhaustive = bool(
                declared > 0
                and evidence.candidates_declared == declared
                and evidence.candidates_checked >= declared
                and len(evidence.checked_candidate_ids) == evidence.candidates_checked
                and set(evidence.checked_candidate_ids) == set(packet.evaluator_class_e)
                and len(evidence.checked_candidate_ids) == declared
            )
    else:
        if evidence.checked_candidate_ids is not None:
            exhaustive = bool(
                evidence.candidates_declared > 0
                and evidence.candidates_checked >= evidence.candidates_declared
                and len(evidence.checked_candidate_ids) == evidence.candidates_checked
            )
        else:
            exhaustive = bool(
                evidence.candidates_declared > 0
                and evidence.candidates_checked >= evidence.candidates_declared
            )

    return HaltGuards(
        accepted=bool(evidence.pipeline_accepted),
        deterministic=bool(evidence.replay_deterministic),
        zero_residual_mass=zero_res,
        skeleton_preserving=bool(evidence.skeleton_preserved),
        exhaustive=exhaustive,
        no_pending_lift=bool(evidence.pending_lifts == 0),
        no_refusal=bool(not evidence.active_refusal),
    )


@dataclass(frozen=True)
class AuthorizationResult:
    """
    Result of a finite authorization attempt for operational standing.

    inhabited=True means policy conditions for AuthStanding are satisfied.
    authority_effect is always "None" (package does not mint AuthorityEffect).
    """

    inhabited: bool
    terminal_state: Optional[str]
    refusal_code: Optional[str]
    residual_mass: Rational
    guards: HaltGuards
    residual_certificate: Optional[QuotientDistanceCertificate] = None
    authority_effect: str = "None"


# Backward-compatible alias
AuthorityResult = AuthorizationResult


def all_guards_true() -> HaltGuards:
    """Test helper: fully green derived guard vector (still needs valid packet)."""
    return HaltGuards(
        accepted=True,
        deterministic=True,
        zero_residual_mass=True,
        skeleton_preserving=True,
        exhaustive=True,
        no_pending_lift=True,
        no_refusal=True,
    )


def evaluate_authorization(
    proposal_id: str,
    packet: Optional[DescentPacket],
    evidence: GuardEvidence,
    logit_confidence: Any = Rational(99, 100),
    residual_certificate: Optional[QuotientDistanceCertificate] = None,
) -> AuthorizationResult:
    """
    Finite authorization attempt under a declared packet + derived guards.

    logit_confidence is accepted and ignored for inhabitation (GTFDA-03):
    high confidence without a valid packet never inhabits AuthStanding.
    """
    _ = logit_confidence  # explicitly non-authoritative

    guards = derive_guards(evidence, packet)

    # Validate certificate if supplied
    if residual_certificate is not None:
        if not residual_certificate.verify():
            return AuthorizationResult(
                inhabited=False,
                terminal_state="term_failed_invalid_certificate",
                refusal_code=RefusalCode.R_contradictory_evidence.value,
                residual_mass=RESIDUAL_GUARD_FAIL_NONZERO,
                guards=guards,
                residual_certificate=residual_certificate,
            )
        if residual_certificate.distance != evidence.residual_mass:
            return AuthorizationResult(
                inhabited=False,
                terminal_state="term_failed_distance_mismatch",
                refusal_code=RefusalCode.R_contradictory_evidence.value,
                residual_mass=RESIDUAL_GUARD_FAIL_NONZERO,
                guards=guards,
                residual_certificate=residual_certificate,
            )

    if packet is None or not packet.is_valid():
        return AuthorizationResult(
            inhabited=False,
            terminal_state=None,
            refusal_code=RefusalCode.R_nopacket.value,
            residual_mass=RESIDUAL_NO_PACKET,
            guards=guards,
            residual_certificate=residual_certificate,
        )

    if not guards.is_auth():
        refusal = RefusalCode.R_unreplayable.value if not guards.deterministic else RefusalCode.R_candidate.value
        residual = (
            RESIDUAL_GUARD_FAIL_NONZERO
            if not guards.zero_residual_mass
            else RESIDUAL_GUARD_FAIL_OTHER
        )
        return AuthorizationResult(
            inhabited=False,
            terminal_state=f"term_failed_{packet.terminalizer_tau}",
            refusal_code=refusal,
            residual_mass=residual,
            guards=guards,
            residual_certificate=residual_certificate,
        )

    return AuthorizationResult(
        inhabited=True,
        terminal_state=f"term_standing_{packet.terminalizer_tau}_{proposal_id}",
        refusal_code=None,
        residual_mass=RESIDUAL_AUTH_STANDING,
        guards=guards,
        residual_certificate=residual_certificate,
    )


def evaluate_authority(
    proposal_id: str,
    packet: Optional[DescentPacket],
    guards: HaltGuards,
    logit_confidence: Any = Rational(99, 100),
    residual_certificate: Optional[QuotientDistanceCertificate] = None,
) -> AuthorizationResult:
    """
    Compatibility entry: accepts pre-derived HaltGuards.

    Prefer evaluate_authorization(evidence=...) so guards are derived.
    """
    _ = logit_confidence

    if not isinstance(guards, HaltGuards):
        raise TypeError(f"guards must be a HaltGuards instance, got {type(guards).__name__}")

    # Validate certificate if supplied
    if residual_certificate is not None:
        if not hasattr(residual_certificate, "verify") or not residual_certificate.verify():
            return AuthorizationResult(
                inhabited=False,
                terminal_state="term_failed_invalid_certificate",
                refusal_code=RefusalCode.R_contradictory_evidence.value,
                residual_mass=RESIDUAL_GUARD_FAIL_NONZERO,
                guards=guards,
                residual_certificate=residual_certificate,
            )
        # Reconcile certificate distance with guards.zero_residual_mass
        is_zero_dist = bool(residual_certificate.distance == 0)
        if is_zero_dist != guards.zero_residual_mass:
            return AuthorizationResult(
                inhabited=False,
                terminal_state="term_failed_distance_mismatch",
                refusal_code=RefusalCode.R_contradictory_evidence.value,
                residual_mass=RESIDUAL_GUARD_FAIL_NONZERO,
                guards=guards,
                residual_certificate=residual_certificate,
            )

    if packet is None or not packet.is_valid():
        return AuthorizationResult(
            inhabited=False,
            terminal_state=None,
            refusal_code=RefusalCode.R_nopacket.value,
            residual_mass=RESIDUAL_NO_PACKET,
            guards=guards,
            residual_certificate=residual_certificate,
        )

    if not guards.is_auth():
        refusal = RefusalCode.R_unreplayable.value if not guards.deterministic else RefusalCode.R_candidate.value
        residual = (
            RESIDUAL_GUARD_FAIL_NONZERO
            if not guards.zero_residual_mass
            else RESIDUAL_GUARD_FAIL_OTHER
        )
        return AuthorizationResult(
            inhabited=False,
            terminal_state=f"term_failed_{packet.terminalizer_tau}",
            refusal_code=refusal,
            residual_mass=residual,
            guards=guards,
            residual_certificate=residual_certificate,
        )

    return AuthorizationResult(
        inhabited=True,
        terminal_state=f"term_standing_{packet.terminalizer_tau}_{proposal_id}",
        refusal_code=None,
        residual_mass=RESIDUAL_AUTH_STANDING,
        guards=guards,
        residual_certificate=residual_certificate,
    )


def compute_cochain_residual_quotient(
    repair_map: MatrixBase,
    cochain: MatrixBase,
) -> QuotientDistanceCertificate:
    """
    Evaluate exact rational quotient distance Q^1_auth = C^1_auth / im(d0).

    Uses local LinearRepairProblem to find the exact primal-dual l1 vertex certificate.
    """
    problem = LinearRepairProblem(repair_map)
    return problem.quotient_l1_distance(cochain)


def evidence_from_cochain_repair(
    repair_map: MatrixBase,
    cochain: MatrixBase,
    pipeline_accepted: bool = True,
    replay_deterministic: bool = True,
    skeleton_preserved: bool = True,
    candidates_checked: int = 2,
    candidates_declared: int = 2,
    pending_lifts: int = 0,
    active_refusal: bool = False,
    residual_zero_tol: Union[int, Rational, Fraction, str] = Rational(0, 1),
    checked_candidate_ids: Optional[Sequence[str]] = None,
) -> Tuple[GuardEvidence, QuotientDistanceCertificate]:
    """
    Derive GuardEvidence by computing exact quotient distance from a cochain repair problem.

    When cochain in im(d0), cert.distance == 0 => g3 (zero_residual_mass) is True.
    When cochain not in im(d0), cert.distance > 0 => g3 is False.
    """
    cert = compute_cochain_residual_quotient(repair_map, cochain)
    if checked_candidate_ids is None and candidates_checked > 0:
        checked_candidate_ids = tuple(f"e{i}" for i in range(candidates_checked))
    evidence = GuardEvidence(
        pipeline_accepted=pipeline_accepted,
        replay_deterministic=replay_deterministic,
        residual_mass=cert.distance,
        residual_zero_tol=residual_zero_tol,
        skeleton_preserved=skeleton_preserved,
        candidates_checked=candidates_checked,
        candidates_declared=candidates_declared,
        pending_lifts=pending_lifts,
        active_refusal=active_refusal,
        checked_candidate_ids=checked_candidate_ids,
    )
    return evidence, cert


# Lazy re-exports of multi-stage pipeline integration harness
_LAZY_PIPELINE_EXPORTS = {
    "CandidateTraceRecord",
    "PipelineAuthorizationReceipt",
    "PipelineTrace",
    "SealedPipeline",
    "SealedPipelineHarness",
    "StageExecutionRecord",
    "StageRefusal",
    "StageResult",
    "StageSuccess",
}


def __getattr__(name: str) -> Any:
    """Lazy re-exports from coda_fda_pipeline to prevent import-order circular dependency."""
    if name in _LAZY_PIPELINE_EXPORTS:
        import coda_fda_pipeline

        return getattr(coda_fda_pipeline, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + list(_LAZY_PIPELINE_EXPORTS))
