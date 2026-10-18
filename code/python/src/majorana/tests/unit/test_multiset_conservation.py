from __future__ import annotations
"""M11 — Obligation conservation is a MULTISET law; the set validator's
multiplicity blind spot is documented, not repaired here.

THEORETICAL MINIMUM
  INVARIANT  Summary compression conserves each residual fingerprint and
             refusal route WITH multiplicity: a 2 -> 1 collapse (keep one
             copy, drop the duplicate) refuses exactly like erasure. Extra
             copies downward are not refused (duplication adds no
             discharge).
  BREAK      Multiplicity laundering: the set-based validator passes a
             compression that keeps one copy of a twice-carried obligation.
  WITNESS    ValueError token ..._MULTIPLICITY listing "item xN"; and the
             set validator PASSING the same laundering (the documented
             blind spot).
  MUTATION   Swap Counter subtraction for set subtraction in the multiset
             validator -> the collapse rows go red.

AuthorityEffect: None throughout.
"""


import pytest

from omega_engine.crates.discrete_deformation_algebra.tower_boundary import (
    validate_gtla_summary_compression,
    validate_gtla_summary_compression_multiset,
)


class TestMultisetCollapseRefused:
    def test_two_to_one_fingerprint_collapse_refused_with_counts(self) -> None:
        with pytest.raises(
            ValueError,
            match="OBLIGATION_COMPRESSION_LAUNDERING_REFUSED_MULTIPLICITY",
        ) as excinfo:
            validate_gtla_summary_compression_multiset(
                ["fp_dup", "fp_dup", "fp_other"],
                [],
                ["fp_dup", "fp_other"],
                [],
            )
        assert "fp_dup x1" in str(excinfo.value)

    def test_two_to_one_route_collapse_refused(self) -> None:
        with pytest.raises(
            ValueError,
            match="OBLIGATION_COMPRESSION_LAUNDERING_REFUSED_MULTIPLICITY",
        ):
            validate_gtla_summary_compression_multiset(
                [],
                ["ROUTE_A", "ROUTE_A"],
                [],
                ["ROUTE_A"],
            )

    def test_total_erasure_also_refused(self) -> None:
        with pytest.raises(
            ValueError,
            match="OBLIGATION_COMPRESSION_LAUNDERING_REFUSED_MULTIPLICITY",
        ):
            validate_gtla_summary_compression_multiset(["fp_gone"], [], [], [])

    def test_exact_conservation_passes(self) -> None:
        validate_gtla_summary_compression_multiset(
            ["fp_a", "fp_a", "fp_b"],
            ["R1"],
            ["fp_a", "fp_b", "fp_a"],
            ["R1"],
        )

    def test_extra_copies_in_the_summary_are_not_refused(self) -> None:
        validate_gtla_summary_compression_multiset(
            ["fp_a"], ["R1"], ["fp_a", "fp_a", "fp_a"], ["R1", "R1"]
        )


class TestSetValidatorBlindSpotIsDocumented:
    def test_set_validator_cannot_see_a_two_to_one_collapse_multiset_can(
        self,
    ) -> None:
        """The legacy SET validator passes multiplicity laundering — that is
        its documented blind spot (tower_boundary NOTE, Inspector M11) — and
        the multiset owner refuses the identical inputs."""
        original = ["fp_dup", "fp_dup"]
        compressed = ["fp_dup"]
        validate_gtla_summary_compression(set(original), set(), set(compressed), set())
        with pytest.raises(
            ValueError,
            match="OBLIGATION_COMPRESSION_LAUNDERING_REFUSED_MULTIPLICITY",
        ):
            validate_gtla_summary_compression_multiset(original, [], compressed, [])


