"""Witness-relative status routing that preserves open and outside-profile states."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClaimStatus(str, Enum):
    DEFINITION = "DEFINITION"
    FINITE_PROPOSITION = "FINITE_PROPOSITION"
    TYPING_PROPOSITION = "TYPING_PROPOSITION"
    CONDITIONAL_RESULT = "CONDITIONAL_RESULT"
    OPEN_CLAIM = "OPEN_CLAIM"
    OPEN_INTERFACE = "OPEN_INTERFACE"
    NONCLAIM = "NONCLAIM"
    SYNTHESIS_CONCLUSION = "SYNTHESIS_CONCLUSION"
    ESTABLISHED = "ESTABLISHED"
    FINITE_WITNESS = "FINITE_WITNESS"
    OPEN = "OPEN"
    CONJECTURE = "CONJECTURE"
    INTERPRETIVE = "INTERPRETIVE"
    REFUTED = "REFUTED"
    OUTSIDE_PROFILE = "OUTSIDE_PROFILE"


@dataclass(frozen=True)
class Claim:
    claim_id: str
    status: ClaimStatus


@dataclass(frozen=True)
class EvaluationProfile:
    profile_id: str
    admitted_claims: frozenset[str]


@dataclass(frozen=True)
class RoutedClaim:
    claim_id: str
    source_status: ClaimStatus
    relative_status: ClaimStatus
    detail: str


def route_claim(claim: Claim, profile: EvaluationProfile) -> RoutedClaim:
    if claim.claim_id not in profile.admitted_claims:
        return RoutedClaim(
            claim.claim_id,
            claim.status,
            ClaimStatus.OUTSIDE_PROFILE,
            f"claim is outside evaluator profile {profile.profile_id}",
        )
    return RoutedClaim(claim.claim_id, claim.status, claim.status, "claim is admitted without status promotion")


def attach_finite_witness(routed: RoutedClaim, witness_id: str) -> RoutedClaim:
    if not witness_id:
        raise ValueError("witness_id is required")
    if routed.relative_status is ClaimStatus.OUTSIDE_PROFILE:
        return RoutedClaim(
            routed.claim_id,
            routed.source_status,
            ClaimStatus.OUTSIDE_PROFILE,
            f"finite witness {witness_id} recorded outside profile; no refutation or promotion",
        )
    if routed.source_status is ClaimStatus.ESTABLISHED:
        status = ClaimStatus.ESTABLISHED
    elif routed.source_status is ClaimStatus.REFUTED:
        status = ClaimStatus.REFUTED
    else:
        status = routed.source_status
    return RoutedClaim(
        routed.claim_id,
        routed.source_status,
        status,
        f"finite witness {witness_id} attached; source status preserved",
    )
# Executable finite evidence; AuthorityEffect: None.
