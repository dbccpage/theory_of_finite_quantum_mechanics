"""Executable witness for PROD-P5-NEXT-1 (15 ClaimStatus values to Chapter 20 Status)."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_paths() -> Path:
    here = Path(__file__).resolve()
    repo_root = next((p for p in here.parents if (p / ".git").exists()), None)
    if repo_root is None:
        raise FileNotFoundError("repository root not found")
    for candidate in (
        repo_root,
        repo_root
        / "omega_engine_atlas"
        / "coda_atlas"
        / "F004_papers"
        / "001_finite_obstruction_calculus"
        / "000_witnessed_difference_programme"
        / "code",
    ):
        s = str(candidate)
        if s not in sys.path:
            sys.path.insert(0, s)
    return repo_root


_ensure_paths()

from omega_engine_applications.wdp_products.kernel.contracts import TypedRefusal  # noqa: E402
from omega_engine_applications.wdp_products.p5_claim_certification.adapter import (  # noqa: E402
    WdpCertificationService,
    map_claim_status,
    route_claim_to_ch20_status,
)
from omega_engine_applications.wdp_products.p5_claim_certification.contracts import (  # noqa: E402
    ClaimNode,
    EvidencePointers,
    Status,
)
from witnessed_difference.relative_status import (  # noqa: E402
    Claim,
    ClaimStatus,
    EvaluationProfile,
)


def witness() -> dict[str, object]:
    if len(ClaimStatus) != 15:
        raise RuntimeError(f"expected 15 ClaimStatus values, found {len(ClaimStatus)}")

    mapped: dict[str, str] = {}
    refused: list[str] = []
    for cs in ClaimStatus:
        res = map_claim_status(cs)
        if isinstance(res, Status):
            mapped[cs.value] = res.value
        elif isinstance(res, TypedRefusal):
            refused.append(cs.value)
        else:
            raise RuntimeError(f"unexpected result for {cs}")

    profile = EvaluationProfile(
        profile_id="profile-finite-q",
        admitted_claims=frozenset({"c.proved", "c.refuted", "c.open", "c.def"}),
    )
    routed_statuses = {
        route_claim_to_ch20_status(Claim("c.proved", ClaimStatus.FINITE_PROPOSITION), profile),
        route_claim_to_ch20_status(Claim("c.refuted", ClaimStatus.REFUTED), profile),
        route_claim_to_ch20_status(Claim("c.open", ClaimStatus.OPEN_CLAIM), profile),
        route_claim_to_ch20_status(Claim("c.unadmitted", ClaimStatus.ESTABLISHED), profile),
        route_claim_to_ch20_status(
            Claim("c.proved", ClaimStatus.FINITE_PROPOSITION),
            profile,
            policy_refused=True,
        ),
    }
    if routed_statuses != set(Status):
        raise RuntimeError("route_claim_to_ch20_status did not cover all 5 Chapter 20 Status values")

    service = WdpCertificationService()
    c1 = ClaimNode(
        claim_id="C1",
        status=Status.PROVED,
        evidence=EvidencePointers(prose_statement="sec 4.1"),
        depends_on=(),
    )
    recomputed = service.certify((c1,), changed=("C1",))
    if not isinstance(recomputed, tuple) or recomputed[0].status is not Status.UNDETERMINED:
        raise RuntimeError("expected incomplete evidence pointers to demote PROVED to UNDETERMINED")

    return {
        "goal_id": "PROD-P5-NEXT-1",
        "total_claim_statuses": len(ClaimStatus),
        "mapped_count": len(mapped),
        "refused_count": len(refused),
        "refused_statuses": sorted(refused),
        "ch20_statuses_covered": sorted(s.value for s in routed_statuses if isinstance(s, Status)),
        "recomputed_status": recomputed[0].status.value,
        "authority_effect": recomputed[0].authority_effect,
    }


def refuse_unmapped_definition_status() -> None:
    res = map_claim_status(ClaimStatus.DEFINITION)
    if isinstance(res, TypedRefusal):
        raise ValueError(f"{res.code}: {res.reason}")
