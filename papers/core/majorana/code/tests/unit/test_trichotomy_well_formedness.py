from __future__ import annotations
"""M4 — Trichotomy well-formedness + exact-rail input discipline (OD-3).

THEORETICAL MINIMUM
  INVARIANT  Gamma2 is a norm of a boundary of the same cochain, so
             Gamma2 > 0 => Phi1 > 0; the pair (0, gamma>0) must refuse, never
             classify ExactRepair. Masses live on the exact rail: floats and
             bools refuse outright (no limit_denominator rounding — 1e-30 can
             never become zero mass), negatives refuse, unparsable strings
             refuse, exact rational strings classify exactly.
  BREAK      Pre-repair OD-3: classify(0, 1) -> ExactRepair (laundered
             closure defect); float 1e-30 silently rounded to zero mass.
  WITNESS    TerminalizerRefusal.token per input class; the exact-string
             1e-30 case classifies POSITIVE (ClosedSurvivor).
  MUTATION   Delete the (p == 0 and g > 0) inconsistency gate in
             classify_trichotomy -> the INCONSISTENT_WITNESS rows go red.

AuthorityEffect: None throughout.
"""


import time
from fractions import Fraction

import pytest

from omega_engine.crates.type.runtime_axes import CohomologicalStatus
from omega_engine.crates.type.terminalizers import TerminalizerRefusal, classify_phi_gamma
from omega_engine.crates.type.terminalizers.termz_finite_obstruction_calculus import classify_trichotomy


class TestInconsistentWitnessRefusal:
    @pytest.mark.parametrize("gamma2", [1, "1/3", Fraction(2, 5)])
    def test_zero_phi_with_positive_gamma_refuses_on_core(self, gamma2) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="INCONSISTENT_WITNESS"
        ) as excinfo:
            classify_trichotomy(0, gamma2)
        assert excinfo.value.token == "INCONSISTENT_WITNESS"

    def test_zero_phi_with_positive_gamma_refuses_on_full_classifier(self) -> None:
        # Must never emit ExactRepair over an inconsistent witness pair.
        with pytest.raises(TerminalizerRefusal, match="INCONSISTENT_WITNESS"):
            classify_phi_gamma(0, "1/7")


class TestExactRailInputDiscipline:
    @pytest.mark.parametrize("bad_mass", [0.5, 1e-30, 0.0, True, False])
    def test_floats_and_bools_refused_outright(self, bad_mass) -> None:
        with pytest.raises(TerminalizerRefusal, match="FLOAT_MASS_REFUSED") as excinfo:
            classify_trichotomy(bad_mass, 0)
        assert excinfo.value.token == "FLOAT_MASS_REFUSED"

    def test_float_gamma_also_refused(self) -> None:
        with pytest.raises(TerminalizerRefusal, match="FLOAT_MASS_REFUSED"):
            classify_trichotomy(1, 1e-30)

    def test_tiny_float_never_rounds_to_zero_mass(self) -> None:
        # The OD-3 regression: 1e-30 via Fraction(float).limit_denominator()
        # rounded to zero mass and classified ExactRepair. Now the float
        # refuses; there is no rounding path left.
        with pytest.raises(TerminalizerRefusal, match="FLOAT_MASS_REFUSED"):
            classify_phi_gamma(1e-30, 0)

    def test_exact_string_1e30_is_positive_mass_closed_survivor(self) -> None:
        # The exact-string spelling of the same magnitude is a legal exact
        # rational and must classify as POSITIVE mass — never ExactRepair.
        assert classify_trichotomy("1e-30", 0) is CohomologicalStatus.ClosedSurvivor
        verdict = classify_phi_gamma("1e-30", 0)
        assert verdict.cohomological is CohomologicalStatus.ClosedSurvivor
        assert verdict.phi1 == Fraction(1, 10**30)
        assert verdict.phi1 > 0

    @pytest.mark.parametrize("negative", [-1, "-1/2", Fraction(-3, 7)])
    def test_negative_masses_refused_as_norm_violation(self, negative) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="NEGATIVE_MASS_REFUSED"
        ) as excinfo:
            classify_trichotomy(negative, 0)
        assert excinfo.value.token == "NEGATIVE_MASS_REFUSED"

    @pytest.mark.parametrize("unparsable", ["not_a_number", "1/0", "one third"])
    def test_unparsable_strings_refused(self, unparsable) -> None:
        with pytest.raises(TerminalizerRefusal, match="MASS_PARSE_REFUSED") as excinfo:
            classify_trichotomy(unparsable, 0)
        assert excinfo.value.token == "MASS_PARSE_REFUSED"

    @pytest.mark.parametrize("wrong_type", [None, [], {}, object()])
    def test_wrong_types_refused(self, wrong_type) -> None:
        with pytest.raises(TerminalizerRefusal, match="MASS_TYPE_REFUSED") as excinfo:
            classify_trichotomy(wrong_type, 0)
        assert excinfo.value.token == "MASS_TYPE_REFUSED"


class TestMassExponentBound:
    """P2 repair: unbounded scientific-notation exponent parsing.

    Before this repair, ``Fraction("1e-2000000")`` parsed in ~1s while
    materializing a ~2,000,000-digit denominator; Python's
    ``sys.int_max_str_digits`` (default 4300) does not guard this path
    (it only guards digit-string-to-int conversion, and ``Fraction``
    builds the scientific-notation numerator/denominator via ``10 **
    abs(exponent)``, a power, not a string conversion).
    """

    @pytest.mark.parametrize(
        "huge_exponent_mass", ["1e-2000000", "1e2000000", "1E-999999999"]
    )
    def test_huge_scientific_exponent_refused_before_fraction_construction(
        self, huge_exponent_mass: str
    ) -> None:
        start = time.monotonic()
        with pytest.raises(
            TerminalizerRefusal, match="MASS_EXPONENT_OUT_OF_RANGE_REFUSED"
        ) as excinfo:
            classify_trichotomy(huge_exponent_mass, 0)
        elapsed = time.monotonic() - start
        assert excinfo.value.token == "MASS_EXPONENT_OUT_OF_RANGE_REFUSED"
        # The refusal must fire BEFORE Fraction() would materialize the
        # giant numerator/denominator (that construction alone took ~1s
        # pre-repair for a single ~2,000,000-digit literal).
        assert elapsed < 0.1

    def test_full_classifier_also_refuses_huge_exponent(self) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="MASS_EXPONENT_OUT_OF_RANGE_REFUSED"
        ):
            classify_phi_gamma("1e-2000000", 0)

    @pytest.mark.parametrize("boundary_exponent", ["1e10000", "1e-10000"])
    def test_exponent_exactly_at_the_bound_is_still_accepted(
        self, boundary_exponent: str
    ) -> None:
        # abs(exponent) > bound refuses; == bound is legal (fence-post).
        result = classify_trichotomy(boundary_exponent, 0)
        assert result is CohomologicalStatus.ClosedSurvivor

    def test_exponent_one_past_the_bound_is_refused(self) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="MASS_EXPONENT_OUT_OF_RANGE_REFUSED"
        ):
            classify_trichotomy("1e10001", 0)

    def test_small_exponent_masses_are_unaffected(self) -> None:
        # Regression guard: the bound must not disturb ordinary literals.
        assert classify_trichotomy("1e-30", 0) is CohomologicalStatus.ClosedSurvivor
        assert classify_trichotomy("1e4", 0) is CohomologicalStatus.ClosedSurvivor

    def test_non_exponent_strings_are_unaffected(self) -> None:
        # No 'e'/'E' present -> the exponent regex must not fire at all.
        assert classify_trichotomy("1/3", 0) is CohomologicalStatus.ClosedSurvivor


class TestExactStringsClassifyExactly:
    def test_fraction_strings_carry_exact_values_into_the_verdict(self) -> None:
        verdict = classify_phi_gamma("1/3", "0")
        assert verdict.cohomological is CohomologicalStatus.ClosedSurvivor
        assert verdict.phi1 == Fraction(1, 3)
        assert verdict.gamma2 == Fraction(0)

    def test_consistent_positive_pair_is_active_closure_failure(self) -> None:
        assert (
            classify_trichotomy(Fraction(1, 3), Fraction(1, 9))
            is CohomologicalStatus.ActiveClosureFailure
        )


