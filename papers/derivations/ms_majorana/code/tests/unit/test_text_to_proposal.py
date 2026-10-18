"""Tests for the WIT-OBS-001 increment B text -> ResearchProposal extraction
layer (`omega_engine.crates.pipeline.text_to_proposal`).

These are the unit-scale healing receipt: they prove page-anchored text can
now reach `universal_solver.parse_research_proposal` in typed, ACCEPTED form
-- something the W-WITTEN baseline could only reach as a 13-field typed
refusal (`baseline_receipt.json`, attempt
`universal_solver.parse_research_proposal(paper_as_payload)`). Acceptance
here is a schema fact only; nothing in this module or these tests validates
any mathematical claim.
"""

from pathlib import Path

import pytest

from omega_engine.crates.pipeline.research_pipeline import OmegaResearchPipeline
from omega_engine.crates.pipeline.text_to_proposal import (
    NoClaimCandidatesFoundError,
    ProposalPacketBindingError,
    extract_research_proposal,
)
from omega_engine.crates.runtime.rt_universal_obstruction import (
    UniversalSolverRefusal,
    parse_research_proposal,
)

from omega_engine_pfp.domain.entities.research_packets import ClaimKind, ResearchMode

OBJECTIVE = "Test the text-to-proposal extraction layer without promoting any paper claim"
PROPOSER = "test-provider:witten2-incB"


def _packet(tmp_path: Path, objective: str = OBJECTIVE):
    paper = tmp_path / "paper.md"
    paper.write_text(
        "# Paper\n\nPlaceholder corpus file for text_to_proposal tests.\n",
        encoding="utf-8",
    )
    engine = OmegaResearchPipeline()
    return engine.start(paper, objective, PROPOSER, mode=ResearchMode.FAST)


def _page_anchored_text(pages: dict[int, str]) -> str:
    parts: list[str] = []
    for page_number in sorted(pages):
        parts.append(f"===PDFPAGE {page_number}===")
        parts.append(pages[page_number])
    return "\n".join(parts)


def test_round_trip_extraction_is_accepted_at_the_solver_front_door(tmp_path: Path):
    """The unit-scale healing receipt: page-anchored text -> extraction ->
    the exact payload the universal solver's front door ACCEPTS, where the
    W-WITTEN baseline recorded only a 13-field typed refusal."""
    packet = _packet(tmp_path)
    text = _page_anchored_text(
        {
            1: (
                "A Paper About Boundary Maps.\n"
                "We show that the boundary map vanishes on this cycle."
            ),
            2: (
                "We expect this pattern to generalize to higher degree.\n"
                "Unrelated neutral prose with no markers at all."
            ),
        }
    )

    proposal = extract_research_proposal(
        packet, text, target_path="paper.md", objective=OBJECTIVE
    )

    assert len(proposal.claims) == 2
    parsed = parse_research_proposal(packet, proposal.canonical_payload())
    assert parsed.proposal_sha256 == proposal.proposal_sha256
    assert [c.canonical_payload() for c in parsed.claims] == [
        c.canonical_payload() for c in proposal.claims
    ]


def test_schema_law_intact_removing_a_field_still_refuses(tmp_path: Path):
    """Negative control: this module cannot accidentally widen the front
    door -- a payload missing one required field must still hit the same
    typed refusal the baseline recorded."""
    packet = _packet(tmp_path)
    text = _page_anchored_text({1: "We show that X holds for every finite n."})
    proposal = extract_research_proposal(
        packet, text, target_path="paper.md", objective=OBJECTIVE
    )

    payload = dict(proposal.canonical_payload())
    del payload["summary"]

    with pytest.raises(UniversalSolverRefusal, match="missing"):
        parse_research_proposal(packet, payload)


def test_extraction_is_deterministic(tmp_path: Path):
    packet = _packet(tmp_path)
    text = _page_anchored_text(
        {
            1: "We show that the map is injective.",
            2: "We expect the converse to hold too. Nothing notable here.",
        }
    )

    first = extract_research_proposal(
        packet, text, target_path="paper.md", objective=OBJECTIVE
    )
    second = extract_research_proposal(
        packet, text, target_path="paper.md", objective=OBJECTIVE
    )

    assert first.canonical_payload() == second.canonical_payload()
    assert first.proposal_sha256 == second.proposal_sha256


def test_claims_carry_the_correct_page_anchor(tmp_path: Path):
    packet = _packet(tmp_path)
    text = _page_anchored_text(
        {
            6: "Neutral filler with no marker phrase on this page at all.",
            7: "We prove that the sequence terminates for every finite input.",
        }
    )

    proposal = extract_research_proposal(
        packet, text, target_path="paper.md", objective=OBJECTIVE
    )

    assert len(proposal.claims) == 1
    [claim] = proposal.claims
    assert claim.evidence_refs == ("PDFPAGE 7",)
    assert claim.kind is ClaimKind.THEOREM_CANDIDATE


def test_degenerate_text_with_no_markers_refuses_rather_than_inventing_a_claim(
    tmp_path: Path,
):
    """Designed degenerate-text behavior: `ResearchProposal` refuses a zero
    -claim payload (`"a research proposal must declare at least one typed
    claim"`), and this module does not paper over that by inventing a
    placeholder claim -- it raises before ever constructing a proposal."""
    packet = _packet(tmp_path)
    text = _page_anchored_text(
        {
            1: "This page states an observation with no marker phrase at all.",
            2: "Neither does this one; it just continues the plain prose.",
        }
    )

    with pytest.raises(NoClaimCandidatesFoundError):
        extract_research_proposal(
            packet, text, target_path="paper.md", objective=OBJECTIVE
        )


def test_marker_tier_assignment_theorem_candidate_vs_conjecture(tmp_path: Path):
    packet = _packet(tmp_path)
    text = _page_anchored_text(
        {
            1: (
                "We show that the invariant is well-defined. "
                "We expect a similar bound to hold in general."
            ),
        }
    )

    proposal = extract_research_proposal(
        packet, text, target_path="paper.md", objective=OBJECTIVE
    )

    kinds_by_text = {claim.text: claim.kind for claim in proposal.claims}
    assert kinds_by_text["We show that the invariant is well-defined."] is (
        ClaimKind.THEOREM_CANDIDATE
    )
    assert kinds_by_text["We expect a similar bound to hold in general."] is (
        ClaimKind.CONJECTURE
    )


def test_objective_mismatch_refuses_before_any_extraction(tmp_path: Path):
    """The extraction call is bound to the seed packet it declares itself
    to be operating under; a caller passing a mismatched `objective` is
    refused rather than silently extracted against the wrong packet."""
    packet = _packet(tmp_path)
    text = _page_anchored_text(
        {1: "We show that this text is irrelevant since the call is refused first."}
    )

    with pytest.raises(ProposalPacketBindingError):
        extract_research_proposal(
            packet,
            text,
            target_path="paper.md",
            objective="a completely different, unbound objective",
        )


