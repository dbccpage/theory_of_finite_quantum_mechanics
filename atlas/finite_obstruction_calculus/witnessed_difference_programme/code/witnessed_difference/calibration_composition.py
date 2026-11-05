"""Exact deterministic uncertainty bounds for sequential affine calibrations.

All error bounds are declared hypotheses. No independence, distribution,
confidence level, or physical traceability is inferred from these witnesses.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .exact import as_fraction


@dataclass(frozen=True)
class BoundedReading:
    center: Fraction
    radius: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "center", as_fraction(self.center))
        object.__setattr__(self, "radius", as_fraction(self.radius))
        if self.radius < 0:
            raise ValueError("reading radius must be nonnegative")

    def contains(self, value: int | str | Fraction) -> bool:
        return abs(as_fraction(value) - self.center) <= self.radius


@dataclass(frozen=True)
class AffineCalibrationStage:
    stage_id: str
    gain: Fraction
    offset: Fraction
    gain_error: Fraction = Fraction(0)
    offset_error: Fraction = Fraction(0)
    residual_error: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        if not isinstance(self.stage_id, str) or not self.stage_id:
            raise ValueError("a calibration stage needs an identity")
        for field in ("gain", "offset", "gain_error", "offset_error", "residual_error"):
            object.__setattr__(self, field, as_fraction(getattr(self, field)))
        if min(self.gain_error, self.offset_error, self.residual_error) < 0:
            raise ValueError("calibration error bounds must be nonnegative")

    def propagate(self, reading: BoundedReading) -> BoundedReading:
        """Contain (gain+da)*true_input+offset+db+e exactly in a rational interval.

        Hypotheses: |true_input-x|<=r, |da|<=alpha, |db|<=beta,
        |e|<=eta. Subtracting ax+b gives a*d+da*x+da*d+db+e;
        triangle inequalities give (|a|+alpha)r+alpha|x|+beta+eta.
        The proof allows adversarially correlated errors at every stage.
        """
        if not isinstance(reading, BoundedReading):
            raise TypeError("a calibration stage needs a bounded reading")
        return BoundedReading(
            self.gain * reading.center + self.offset,
            (abs(self.gain) + self.gain_error) * reading.radius
            + self.gain_error * abs(reading.center)
            + self.offset_error
            + self.residual_error,
        )


def compose_nominal(stages: tuple[AffineCalibrationStage, ...]) -> tuple[Fraction, Fraction]:
    """Return A,B with f_n(...f_1(x))=A*x+B; the empty chain is identity.

    Induction step: a*(A*x+B)+b=(a*A)*x+(a*B+b).
    """
    if not isinstance(stages, tuple) or any(not isinstance(stage, AffineCalibrationStage) for stage in stages):
        raise TypeError("stages must be a tuple of declared affine calibrations")
    gain, offset = Fraction(1), Fraction(0)
    for stage in stages:
        gain, offset = stage.gain * gain, stage.gain * offset + stage.offset
    return gain, offset


def propagate_chain(
    reading: BoundedReading,
    stages: tuple[AffineCalibrationStage, ...],
) -> tuple[BoundedReading, ...]:
    """Return input and every intermediate enclosure, preserving all stages.

    Inductively apply the one-stage containment lemma, so the final interval
    contains every admissible sequential realization, without independent errors.
    With exact gains/offsets, r_n=|product a_i|r_0+
    sum_i eta_i*product_{j>i}|a_j| (eta includes declared offset error).
    """
    compose_nominal(stages)
    if not isinstance(reading, BoundedReading):
        raise TypeError("the input must be a bounded reading")
    states = [reading]
    for stage in stages:
        states.append(stage.propagate(states[-1]))
    return tuple(states)


def nominal_update_bound(
    old: AffineCalibrationStage,
    new: AffineCalibrationStage,
    reading: BoundedReading,
) -> Fraction:
    """Exact sup of |new_nominal(t)-old_nominal(t)| on the input interval.

    Delta(t)=da*x+db+da*d for |d|<=r. The endpoint maximizing the
    absolute value attains |da*x+db|+|da|r; coefficient-error envelopes
    are separate from this bound on a nominal calibration update.
    """
    if not isinstance(old, AffineCalibrationStage) or not isinstance(new, AffineCalibrationStage):
        raise TypeError("calibration updates need two declared stages")
    if not isinstance(reading, BoundedReading):
        raise TypeError("calibration updates need a bounded input")
    gain_delta = new.gain - old.gain
    offset_delta = new.offset - old.offset
    return abs(gain_delta * reading.center + offset_delta) + abs(gain_delta) * reading.radius
