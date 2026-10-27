from fractions import Fraction as Q
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from residual_error_budget import advance_budget, waiting_window, product_defect_interval, onset_lower_bound


def test_all_error_sources_and_correction_window():
    assert advance_budget(Q(1,100), Q(1,10), Q(1,2), Q(1,200), Q(1,100)) == Q(3,40)
    window = waiting_window(Q(1,10), Q(1,100), Q(3,200), Q(1,10), 1)
    assert window == Q(3,4)
    assert advance_budget(Q(1,100), Q(1,10), window, Q(3,200)) == Q(1,10)
    assert advance_budget(Q(1,100), Q(1,10), window+Q(1,100), Q(3,200)) > Q(1,10)


def test_zero_rate_keeps_the_declared_horizon_without_division():
    assert waiting_window(1, Q(1,2), Q(1,2), 0, 7) == 7
    assert waiting_window(1, 1, 0, 1, 7) == 0
    with pytest.raises(ValueError):
        waiting_window(1, 1, Q(1,100), 0, 7)


def test_uncertainty_can_explain_the_entire_observed_defect():
    assert product_defect_interval(2, Q(1,50), Q(1,150)) == (0, Q(1,25))
    assert product_defect_interval(2, Q(1,50), Q(1,300)) == (Q(1,100), Q(3,100))
    assert product_defect_interval(3, Q(1,2), Q(1,100), Q(1,100)) == (Q(9,20), Q(11,20))


def test_onset_requires_positive_margin_and_remainder_control():
    assert onset_lower_bound(Q(1,50), Q(1,50), 1, Q(1,100)) == 0
    assert onset_lower_bound(2, Q(1,2), 3, Q(1,4)) == Q(3,16)
    assert onset_lower_bound(2, Q(1,2), 3, 1) == 0


@pytest.mark.parametrize("bad", [True, 0.1, float("nan"), float("inf"), "1/2"])
def test_nonexact_budget_inputs_are_refused(bad):
    with pytest.raises(TypeError): advance_budget(0, bad, 1)
    with pytest.raises(TypeError): waiting_window(1, 0, 0, bad, 1)
    with pytest.raises(TypeError): product_defect_interval(2, 1, bad)


def test_negative_allowances_and_invalid_carriers_are_refused():
    with pytest.raises(ValueError): advance_budget(0, 1, 1, jump=-1)
    with pytest.raises(ValueError): waiting_window(1, 0, 0, 1, -1)
    for factors in [0, -1, True, 2.0]:
        with pytest.raises(ValueError): product_defect_interval(factors, 1, 0)
