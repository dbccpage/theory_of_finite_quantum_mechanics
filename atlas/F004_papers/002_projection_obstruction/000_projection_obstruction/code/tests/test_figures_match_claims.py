"""The figures must depict the claims they name.

Added 2026-09-03 after an external review found both non-figure-1 plots
misrepresenting their captions:

* **Figure 2** shaded a region it labelled "Certificate Validity Domain" out to
  t = 0.05, while for its own parameters (nu_e = 2, g = 3) the certified
  half-slope window ends at nu_e/(48 g^2) ~ 0.00463 and the signed bound
  reaches zero at nu_e/(24 g^2) ~ 0.00926. Roughly nine tenths of the shaded
  span was outside anything Theorem 5.1 certifies.
* **Figure 3** plotted invented bars (2.5e against 1.8e) and called their
  difference the visibility gap. Section 7.4 defines that gap as
  Lambda_max = I - max_alpha J^alpha over a declared observer family, and no
  observer family appeared in the plot at all.

A picture cannot be unit-tested for looking right, but it can be tested for
being built from the right numbers. These tests pin the arithmetic the figures
are drawn from, so a caption cannot drift away from its claim again.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_CODE = str(Path(__file__).resolve().parents[1])
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from observer_carriers import scaling_family_certificate, three_patch_certificate

# Figure 2's declared parameters, kept here so a change to the figure that does
# not change these constants still has to face the thresholds below.
NU_E = 2.0
G = 3.0


# ---------------------------------------------------------------------------
# Figure 2: the two thresholds must be what the theorem says they are
# ---------------------------------------------------------------------------

def test_half_slope_window_threshold():
    """The certified window ends at nu_e/(48 g^2), not at an arbitrary constant."""
    assert NU_E / (48.0 * G**2) == pytest.approx(0.0046296296, rel=1e-6)


def test_signed_bound_zero_crossing():
    """nu_e t - 24 g^2 t^2 = 0 at t = nu_e/(24 g^2), twice the window."""
    zero_cross = NU_E / (24.0 * G**2)
    assert zero_cross == pytest.approx(0.0092592593, rel=1e-6)
    assert zero_cross == pytest.approx(2.0 * NU_E / (48.0 * G**2), rel=1e-12)
    value = NU_E * zero_cross - 24.0 * G**2 * zero_cross**2
    assert value == pytest.approx(0.0, abs=1e-15)


def test_the_old_plot_range_was_mostly_uncertified():
    """Records why the figure changed: 0.05 was about eleven windows wide."""
    window = NU_E / (48.0 * G**2)
    assert 0.05 / window > 10.0


def test_bound_is_positive_inside_the_window_and_negative_past_the_crossing():
    window = NU_E / (48.0 * G**2)
    zero_cross = NU_E / (24.0 * G**2)

    def bound(t: float) -> float:
        return NU_E * t - 24.0 * G**2 * t**2

    assert bound(window * 0.5) > 0.0
    assert bound(window) > 0.0
    assert bound(zero_cross * 1.5) < 0.0


def test_half_slope_conclusion_holds_exactly_at_the_window_edge():
    """At t = nu_e/(48 g^2) the bound equals nu_e t / 2, which is what makes it
    the half-slope window rather than a round number."""
    window = NU_E / (48.0 * G**2)
    bound = NU_E * window - 24.0 * G**2 * window**2
    assert bound == pytest.approx(NU_E * window / 2.0, rel=1e-12)


# ---------------------------------------------------------------------------
# Figure 3: the numbers must come from the actual witness
# ---------------------------------------------------------------------------

def test_three_patch_witness_supplies_figure_3_left_panel():
    """Every observer reads zero while the raw tally is exactly six."""
    cert = three_patch_certificate()
    assert cert.full_edge_coverage is True
    assert cert.tallies.I == 6
    assert all(value == 0 for value in cert.tallies.J.values())
    assert len(cert.tallies.J) == 3


def test_visibility_gap_is_I_minus_max_J_not_I_minus_a_sum():
    """The definition the old figure got wrong.

    Lambda_max = I - max_alpha J^alpha.  With every J^alpha zero the gap equals
    the raw tally, which is the whole point of the witness.
    """
    cert = three_patch_certificate()
    lambda_max = cert.tallies.I - max(cert.tallies.J.values())
    assert lambda_max == cert.tallies.I == 6
    assert cert.tallies.Lambda == lambda_max


@pytest.mark.parametrize("scale", [1, 2, 3, 4, 5, 6])
def test_scaling_family_supplies_figure_3_right_panel(scale):
    """I(s_lambda) = 6|lambda| with every observer still reading zero."""
    family = scaling_family_certificate([scale])
    instance = family.instances[0]
    assert instance.tallies.I == 6 * abs(scale)
    assert max(instance.tallies.J.values()) == 0
    assert instance.tallies.I - max(instance.tallies.J.values()) == 6 * abs(scale)


def test_scaling_is_exactly_linear_so_the_gap_is_unbounded():
    family = scaling_family_certificate([1, 2, 3, 4, 5, 6])
    assert family.exact_linear_scaling is True
    raws = [inst.tallies.I for inst in family.instances]
    assert raws == [6, 12, 18, 24, 30, 36]


# ---------------------------------------------------------------------------
# (retired) rendering
#
# 2026-09-03: the render test went out with public_export/ and the figure
# generator. The arithmetic guards above are the part that mattered: they
# check the paper's numbers, not a PNG.
# ---------------------------------------------------------------------------
