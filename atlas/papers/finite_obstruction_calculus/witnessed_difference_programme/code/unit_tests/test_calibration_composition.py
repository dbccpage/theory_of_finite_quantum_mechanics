from fractions import Fraction
from itertools import product

import pytest
from witnessed_difference.calibration_composition import (
    AffineCalibrationStage,
    BoundedReading,
    compose_nominal,
    nominal_update_bound,
    propagate_chain,
)


def test_two_stage_containment_for_adversarial_coefficient_errors() -> None:
    reading = BoundedReading(Fraction(2), Fraction(1, 10))
    stages = (
        AffineCalibrationStage("first", 2, 1, Fraction(1, 10), Fraction(1, 20), Fraction(1, 25)),
        AffineCalibrationStage("second", -3, 2, Fraction(1, 5), Fraction(1, 50), Fraction(1, 100)),
    )
    states = propagate_chain(reading, stages)
    assert compose_nominal(stages) == (-6, -1)
    assert states[-1].center == -13
    choices = (-1, 0, 1)
    # Includes correlated error realizations: no probabilistic independence.
    for signs in product(choices, repeat=7):
        true_value = reading.center + signs[0] * reading.radius
        for i, stage in enumerate(stages):
            da, db, residual = signs[1 + 3 * i:4 + 3 * i]
            true_value = (stage.gain + da * stage.gain_error) * true_value + stage.offset + db * stage.offset_error + residual * stage.residual_error
            assert states[i + 1].contains(true_value)


def test_fixed_coefficient_composition_has_weighted_error_formula() -> None:
    reading = BoundedReading(2, Fraction(1, 10))
    stages = (
        AffineCalibrationStage("a", 2, 1, residual_error=Fraction(1, 20)),
        AffineCalibrationStage("b", -3, 2, offset_error=Fraction(1, 50)),
        AffineCalibrationStage("c", Fraction(1, 2), 5, residual_error=Fraction(1, 100)),
    )
    states = propagate_chain(reading, stages)
    assert states[-1].radius == 3 * reading.radius + Fraction(3, 2) * Fraction(1, 20) + Fraction(1, 2) * Fraction(1, 50) + Fraction(1, 100)
    gain, offset = compose_nominal(stages)
    assert states[-1].center == gain * reading.center + offset
    assert compose_nominal(()) == (1, 0)
    assert propagate_chain(reading, ()) == (reading,)


def test_nominal_calibration_update_bound_is_exact_on_both_endpoints() -> None:
    for old_gain, new_gain, center in product((-2, 0, 3), repeat=3):
        old = AffineCalibrationStage("old", old_gain, Fraction(1, 3))
        new = AffineCalibrationStage("new", new_gain, Fraction(-1, 5))
        reading = BoundedReading(center, Fraction(1, 7))
        endpoint_differences = (
            abs((new.gain - old.gain) * value + new.offset - old.offset)
            for value in (reading.center - reading.radius, reading.center + reading.radius)
        )
        assert nominal_update_bound(old, new, reading) == max(endpoint_differences)


def test_gain_uncertainty_needs_input_magnitude_and_cross_term() -> None:
    stage = AffineCalibrationStage("gain-only", 0, 0, gain_error=1)
    propagated = stage.propagate(BoundedReading(10, 2))
    assert propagated.radius == 12
    assert propagated.contains(12)
    assert not BoundedReading(0, 10).contains(12)
    assert not BoundedReading(0, 2).contains(12)


@pytest.mark.parametrize("bad", (True, 0.5, "not-exact"))
def test_exact_firewall(bad: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        BoundedReading(bad, 0)
    with pytest.raises((TypeError, ValueError)):
        AffineCalibrationStage("stage", 1, 0, gain_error=bad)


def test_negative_bounds_and_malformed_chains_refused() -> None:
    with pytest.raises(ValueError):
        BoundedReading(1, -1)
    with pytest.raises(ValueError):
        AffineCalibrationStage("", 1, 0)
    with pytest.raises(ValueError):
        AffineCalibrationStage("a", 1, 0, residual_error=-1)
    with pytest.raises(TypeError):
        compose_nominal((object(),))
    with pytest.raises(TypeError):
        compose_nominal([])
    with pytest.raises(TypeError):
        propagate_chain(object(), ())
    stage = AffineCalibrationStage("stage", 1, 0)
    with pytest.raises(TypeError):
        stage.propagate(object())
    with pytest.raises(TypeError):
        nominal_update_bound(object(), stage, BoundedReading(0, 0))
    with pytest.raises(TypeError):
        nominal_update_bound(stage, stage, object())
