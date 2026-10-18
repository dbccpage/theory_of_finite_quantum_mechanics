from __future__ import annotations
"""M13 — Evidence ceiling gates fail closed on unknown tokens (OD-6).

THEORETICAL MINIMUM
  INVARIANT  Only the registered 5-rung lattice (and explicitly typed
             EvidenceLevel values) have ranks; an unknown token refuses in
             every gate instead of silently ranking 0 and passing under
             every ceiling. Equal-or-lower evidence is allowed; raising a
             ceiling refuses.
  BREAK      Pre-repair OD-6: EVIDENCE_RANK.get(token, 0) — garbage ranked
             bottom-rung and passed every gate.
  WITNESS    ValueError with token UNKNOWN_EVIDENCE_TOKEN_REFUSED from each
             of the three gates.
  MUTATION   Restore the .get(token, 0) default in evidence_rank -> the
             unknown-token rows go red.

AuthorityEffect: None throughout.
"""


import pytest

from omega_engine_governance.contracts.evidence import (
    EVIDENCE_RANK,
    EvidenceCeiling,
    EvidenceLevel,
    allowed_evidence,
    assert_no_ceiling_raise,
    evidence_rank,
)


class TestUnknownTokensRefuseInEveryGate:
    @pytest.mark.parametrize(
        "unknown", ["TotallyMadeUp", "LocalGreen", "", "boundarychecked"]
    )
    def test_evidence_rank_refuses_unknown_tokens(self, unknown: str) -> None:
        with pytest.raises(ValueError, match="UNKNOWN_EVIDENCE_TOKEN_REFUSED"):
            evidence_rank(unknown)

    def test_allowed_evidence_refuses_unknown_route(self) -> None:
        with pytest.raises(ValueError, match="UNKNOWN_EVIDENCE_TOKEN_REFUSED"):
            allowed_evidence("GarbageRoute", EvidenceCeiling.BOUNDARY_CHECKED)

    def test_allowed_evidence_refuses_unknown_ceiling(self) -> None:
        with pytest.raises(ValueError, match="UNKNOWN_EVIDENCE_TOKEN_REFUSED"):
            allowed_evidence(EvidenceCeiling.SHAPE_ONLY, "GarbageCeiling")

    def test_assert_no_ceiling_raise_refuses_unknown_ceiling_object(self) -> None:
        # Construction of an unregistered EvidenceCeiling is permitted (for
        # display/serialization); the GATE is where it must refuse.
        unknown = EvidenceCeiling("NotARealRung")
        with pytest.raises(ValueError, match="UNKNOWN_EVIDENCE_TOKEN_REFUSED"):
            assert_no_ceiling_raise(unknown, EvidenceCeiling.SHAPE_ONLY)
        with pytest.raises(ValueError, match="UNKNOWN_EVIDENCE_TOKEN_REFUSED"):
            assert_no_ceiling_raise(EvidenceCeiling.SHAPE_ONLY, unknown)


class TestRegisteredLatticeStillWorks:
    def test_registered_tokens_rank_by_the_declared_total_order(self) -> None:
        assert evidence_rank("ShapeOnly") == 0
        assert evidence_rank("SchemaChecked") == 1
        assert evidence_rank("LocalReplay") == 2
        assert evidence_rank("BoundaryChecked") == 3
        assert evidence_rank("ExternalOracleRequired") == 4
        assert evidence_rank("EmpiricalOracleRequired") == 5

    def test_equal_and_lower_evidence_allowed_higher_refused(self) -> None:
        assert allowed_evidence("ShapeOnly", "BoundaryChecked") is True
        assert allowed_evidence("LocalReplay", "LocalReplay") is True
        assert allowed_evidence("BoundaryChecked", "ShapeOnly") is False

    def test_ceiling_cannot_be_raised_but_can_be_held_or_lowered(self) -> None:
        with pytest.raises(ValueError, match="Evidence ceiling violation"):
            assert_no_ceiling_raise(
                EvidenceCeiling.LOCAL_REPLAY, EvidenceCeiling.BOUNDARY_CHECKED
            )
        # Holding and lowering return None (no raise).
        assert (
            assert_no_ceiling_raise(
                EvidenceCeiling.LOCAL_REPLAY, EvidenceCeiling.LOCAL_REPLAY
            )
            is None
        )
        assert (
            assert_no_ceiling_raise(
                EvidenceCeiling.BOUNDARY_CHECKED, EvidenceCeiling.SHAPE_ONLY
            )
            is None
        )

    def test_explicit_evidence_level_is_a_deliberate_typed_rank(self) -> None:
        assert evidence_rank(EvidenceLevel(2, "custom local replay")) == 2
        ceiling = EvidenceCeiling(EvidenceLevel(3, "custom boundary"))
        assert evidence_rank(ceiling) == 3

    def test_registry_is_the_declared_five_rung_lattice(self) -> None:
        # Census tripwire: ranks 0..5 with the declared synonyms only.
        assert sorted(set(EVIDENCE_RANK.values())) == [0, 1, 2, 3, 4, 5]
        assert set(EVIDENCE_RANK) == {
            "GrammarOnly",
            "ShapeOnly",
            "SchemaChecked",
            "LocalReplay",
            "BoundaryChecked",
            "ExternalOracle",
            "ExternalOracleRequired",
            "EmpiricalOracleRequired",
        }


