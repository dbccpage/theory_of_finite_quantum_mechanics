"""SPRINT-001: exactness is a decision, not a tolerance.

Four sites decided a mathematical question with an epsilon. Each test below
pins one of them and names the mutation that breaks it, so that reintroducing
the tolerance is a red test rather than a silent regression.

The standing ruling these enforce: *it either is or is not exact*.

AuthorityEffect: None.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

import pytest

import omega_engine_pfp
from omega_engine_pfp.domain import CandidateProposal, CoboundaryScoreResult
from omega_engine_pfp.domain.exceptions import CanonicalizationError
from omega_engine_pfp.domain.shared_kernel.exact import (
    NotExactError,
    parse_exact,
    to_canonical_string,
)
from omega_engine_pfp.fixtures.gate11_residual_dual import (
    REFUSAL_PHI1_NOT_CERTIFIED,
    contract_bound_holds,
    frozen_fixtures,
    project_fixture_phi_gamma,
)
from omega_engine_pfp.use_cases import score_cochain_proposal, score_discrete_proposal

DUAL = "a" * 64

# One thousandth of the old 1e-9 threshold: comfortably "zero" to a tolerance,
# unambiguously non-zero over Q.
TINY = Fraction(1, 10**12)

# The swept files are the real package's, wherever it is imported from.
REPO_ROOT = Path(omega_engine_pfp.__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# STORY-001-001: carry an exact residual norm into the scoring decision
# ---------------------------------------------------------------------------


def test_a_residual_below_the_old_tolerance_is_not_exact() -> None:
    """Mutation: restore `post_norm < 1e-9` at scoring.py:373 -> this flips to exact."""
    res = score_cochain_proposal(
        {"e1": TINY},
        CandidateProposal(proposal_id="tiny", dual_witness_ref=DUAL),
    )
    assert res.is_legal
    assert res.post_residual_norm == TINY
    assert not res.is_exact_candidate, "a non-zero residual is not exact, however small"


def test_many_small_components_do_not_vanish_when_summed() -> None:
    """Mutation: restore the `if abs(value) > 1e-9` filter at scoring.py:363.

    The filter dropped each term *before* summing, so a thousand of them
    summed to zero instead of to a billionth.
    """
    omega = {f"e{i}": TINY for i in range(1000)}
    res = score_cochain_proposal(
        omega, CandidateProposal(proposal_id="thousand", dual_witness_ref=DUAL)
    )
    assert res.post_residual_norm == Fraction(1000, 10**12)
    assert not res.is_exact_candidate


def test_an_exactly_cancelled_cochain_is_exact() -> None:
    """A genuinely zero residual is exact. 3/7 is not representable in binary."""
    res = score_cochain_proposal(
        {"e1": Fraction(3, 7)},
        CandidateProposal(
            proposal_id="cancel",
            cochain_delta=(("e1", Fraction(3, 7)),),
            dual_witness_ref=DUAL,
        ),
    )
    assert res.post_residual_norm == 0
    assert res.is_exact_candidate, "3/7 - 3/7 is exactly zero"


def test_thirds_sum_to_one_where_binary_floats_do_not() -> None:
    """0.1+0.2 != 0.3 in f64; 1/3 three times is exactly 1 over Q."""
    res = score_cochain_proposal(
        {f"e{i}": Fraction(1, 3) for i in range(3)},
        CandidateProposal(proposal_id="thirds"),
    )
    assert res.prior_residual_norm == 1


def test_zero_residual_without_a_dual_witness_is_still_not_exact() -> None:
    """Exactness is residual-zero AND a named witness. Neither alone."""
    res = score_discrete_proposal(
        ("OBS-01",),
        CandidateProposal(
            proposal_id="no-witness", repaired_obstruction_ids=("OBS-01",), dual_witness_ref=None
        ),
    )
    assert res.post_residual_norm == 0
    assert not res.is_exact_candidate


def test_discrete_counts_are_carried_exactly_not_as_floats() -> None:
    """Mutation: restore `float(len(current))` -> the norm is a float again."""
    res = score_discrete_proposal(
        ("A", "B", "C"),
        CandidateProposal(proposal_id="counts", repaired_obstruction_ids=("A",)),
    )
    assert isinstance(res.prior_residual_norm, Fraction)
    assert isinstance(res.post_residual_norm, Fraction)
    assert res.post_residual_norm == 2


# ---------------------------------------------------------------------------
# STORY-001-002: refuse rather than approximate where exactness is unavailable
# ---------------------------------------------------------------------------


def test_a_float_in_the_cochain_is_refused_not_converted() -> None:
    """Mutation: coerce with `Fraction(value)` instead of refusing -> becomes legal.

    Converting at the boundary would succeed (every finite float is a dyadic
    rational) and would preserve the upstream rounding error exactly. That is
    the defect one layer up, not a repair.
    """
    res = score_cochain_proposal({"e1": 2.0}, CandidateProposal(proposal_id="floaty"))
    assert not res.is_legal
    assert "INEXACT_COCHAIN" in (res.refusal_reason or "")
    assert "FLOAT_REFUSED" in (res.refusal_reason or "")


def test_a_float_cochain_delta_is_refused_at_construction() -> None:
    """Mutation: drop the coerce_exact loop in CandidateProposal.__post_init__."""
    with pytest.raises(CanonicalizationError, match="INEXACT_COCHAIN_DELTA"):
        CandidateProposal(proposal_id="floaty-delta", cochain_delta=(("e1", 1.5),))


def test_an_exactness_claim_over_a_float_is_refused() -> None:
    """STORY-001-002's decisive mutation, stated directly.

    Return a float from the residual path and the refusal fires rather than
    the value being coerced. Ordering matters: the type check must precede the
    comparison, or `0.0 == 0` passes and the claim stands on a float.
    """
    with pytest.raises(CanonicalizationError, match="INEXACT_EXACTNESS_CLAIM"):
        CoboundaryScoreResult(
            proposal_id="float-claim",
            prior_residual_norm=Fraction(1),
            post_residual_norm=0.0,  # a float that happens to equal zero
            residual_drop=Fraction(1),
            structural_cost=0.0,
            normalized_efficiency=1.0,
            is_legal=True,
            is_exact_candidate=True,
            dual_witness_ref=DUAL,
        )


def test_a_tiny_exact_residual_cannot_be_claimed_exact() -> None:
    """Mutation: restore `> 1e-9` at coboundary_score.py:84 -> construction succeeds."""
    with pytest.raises(CanonicalizationError, match="post_residual_norm == 0"):
        CoboundaryScoreResult(
            proposal_id="tiny-claim",
            prior_residual_norm=Fraction(1),
            post_residual_norm=TINY,
            residual_drop=Fraction(1) - TINY,
            structural_cost=0.0,
            normalized_efficiency=1.0,
            is_legal=True,
            is_exact_candidate=True,
            dual_witness_ref=DUAL,
        )


def test_score_result_still_asserts_authority_effect_none() -> None:
    """The exactness work must not have loosened the authority fence."""
    with pytest.raises(CanonicalizationError, match="AuthorityEffect None"):
        CoboundaryScoreResult(
            proposal_id="promoted",
            prior_residual_norm=Fraction(0),
            post_residual_norm=Fraction(0),
            residual_drop=Fraction(0),
            structural_cost=0.0,
            normalized_efficiency=0.0,
            is_legal=True,
            authority_effect="Promote",
        )


def test_exact_norms_cross_the_wire_as_canonical_strings() -> None:
    """Mutation: `float(self.post_residual_norm)` in to_dict -> 1/3 stops round-tripping."""
    res = score_cochain_proposal(
        {"e1": Fraction(1, 3)}, CandidateProposal(proposal_id="wire")
    )
    wire = res.to_dict()
    assert wire["post_residual_norm"] == "1/3"
    assert CoboundaryScoreResult.from_dict(wire).post_residual_norm == Fraction(1, 3)


@pytest.mark.parametrize(
    "wire",
    ("01", "+1", "-0", " 1", "1 ", "1/02", "1/+2", "1/-2"),
)
def test_noncanonical_exact_wire_spellings_are_refused(wire: str) -> None:
    """A rational has one wire spelling.  Otherwise equal values can acquire
    distinct digests and slip through byte-level agreement checks."""
    with pytest.raises(NotExactError, match="canonical rational form"):
        parse_exact(wire, field="wire")


def test_the_exact_wire_renderer_refuses_a_float() -> None:
    """The renderer is another boundary: accepting 0.1 here would preserve an
    upstream binary rounding error as a very large but misleading rational."""
    with pytest.raises(NotExactError, match="never float"):
        to_canonical_string(0.1)  # type: ignore[arg-type]


def test_a_non_exact_score_is_refused_at_construction() -> None:
    """The exact boundary applies before serialization too; a float must not
    survive in memory until ``to_dict`` discovers it far from the caller."""
    with pytest.raises(CanonicalizationError, match="INEXACT_RESIDUAL_NORM"):
        CoboundaryScoreResult(
            proposal_id="float-score",
            prior_residual_norm=1.0,
            post_residual_norm=1.0,
            residual_drop=0.0,
            structural_cost=0.0,
            normalized_efficiency=0.0,
            is_legal=True,
        )


# ---------------------------------------------------------------------------
# STORY-001-003: evaluate the Gamma2 <= Phi1 bound exactly
# ---------------------------------------------------------------------------


def test_a_gamma2_excess_below_the_old_epsilon_is_a_violation() -> None:
    """STORY-001-003's decisive mutation.

    Reintroduce the epsilon (`gamma2 <= phi1 + Fraction(1, 10**9)`) and this
    case reports as holding.
    """
    phi1 = Fraction(1)
    assert contract_bound_holds(phi1 + TINY, phi1) is False
    assert contract_bound_holds(phi1, phi1) is True
    assert contract_bound_holds(phi1 - TINY, phi1) is True


def test_an_uncertified_phi1_leaves_the_bound_undetermined_not_satisfied() -> None:
    """Mutation: `return True` when phi1 is None -> a fail-open."""
    assert contract_bound_holds(Fraction(5), None) is None


def test_the_frozen_fixtures_project_exactly() -> None:
    """The projector could not previously run at all: it imported a module that
    does not exist in this repository. These are the values it now reports."""
    by_name = {fx.name: project_fixture_phi_gamma(fx) for fx in frozen_fixtures()}
    assert set(by_name) == {"Exact", "StabilizedSurvivor", "OpenObstruction"}

    exact = by_name["Exact"]
    assert exact["phi1"] == 0 and exact["gamma2"] == 0 and exact["is_exact"]

    survivor = by_name["StabilizedSurvivor"]
    assert survivor["phi1"] == 2 and survivor["gamma2"] == 0
    assert not survivor["is_exact"]

    for projection in by_name.values():
        assert projection["authority_effect"] == "None"
        if projection["phi1"] is not None:
            assert isinstance(projection["phi1"], Fraction)
        assert isinstance(projection["gamma2"], Fraction)


def test_phi1_is_refused_where_only_a_bound_is_carried() -> None:
    """OpenObstruction names Phi1 = 1 but carries no dual witness pinning it.

    Mutation: return `fx.phi` instead of refusing -> phi1 becomes 1 and the
    refusal disappears. Echoing a fixture's declared value is a lookup, not a
    projection.
    """
    open_obstruction = next(fx for fx in frozen_fixtures() if fx.name == "OpenObstruction")
    assert open_obstruction.phi == 1, "the fixture does declare a value"

    projection = project_fixture_phi_gamma(open_obstruction)
    assert projection["phi1"] is None
    assert REFUSAL_PHI1_NOT_CERTIFIED in projection["phi1_refusal"]
    assert projection["gamma2"] == 1


# ---------------------------------------------------------------------------
# STORY-001-004: record what could not be made exact
# ---------------------------------------------------------------------------

SWEPT_FILES = (
    "omega_engine_pfp/use_cases/scoring.py",
    "omega_engine_pfp/domain/entities/coboundary_score.py",
    "omega_engine_pfp/entrypoints/cli/gate11_commands.py",
    "omega_engine_pfp/fixtures/gate11_residual_dual.py",
)

# The old threshold written as a literal, in any spelling. `#` comment lines
# are exempt so that a note recording what the code used to do can name it;
# nothing else in these files may, docstrings included.
_EPSILON_LITERAL = re.compile(r"(?<![\w.])1e-0*9\b", re.IGNORECASE)


@pytest.mark.parametrize("relative_path", SWEPT_FILES)
def test_no_epsilon_literal_survives_in_a_swept_file(relative_path: str) -> None:
    """STORY-001-004's decisive mutation: add one back and the scan names the line."""
    path = REPO_ROOT / relative_path
    assert path.is_file(), f"{relative_path} moved; update SWEPT_FILES"

    offenders = [
        f"{relative_path}:{number}: {line.strip()}"
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if _EPSILON_LITERAL.search(line) and not line.lstrip().startswith("#")
    ]
    assert offenders == [], "\n".join(offenders)


def test_the_scan_would_actually_catch_a_reintroduced_epsilon() -> None:
    """A negative control for the scan above.

    Without this, a regex that matched nothing would pass the parametrized test
    on every file and look like proof.
    """
    assert _EPSILON_LITERAL.search("is_exact = post_norm < 1e-9")
    assert _EPSILON_LITERAL.search("bound = gamma2 <= phi1 + 1E-9")
    assert not _EPSILON_LITERAL.search("residual = Fraction(1, 10**9)")
