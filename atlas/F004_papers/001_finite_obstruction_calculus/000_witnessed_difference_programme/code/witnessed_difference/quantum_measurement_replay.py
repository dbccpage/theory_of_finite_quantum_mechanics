"""Exact finite Q(i) instrument mirror connected to the paper's Measurement API.

The Rust quantum owner remains the reusable native implementation. This small
independent rational mirror replays square grouped instruments and finite
positive mixtures through existing registration/witness/observation/calibration
and documentary traceability checks. Selected outcomes are declared event data;
no physical occurrence, authentic document, Born-rule selection, or confidence
level follows from acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .calibration_composition import AffineCalibrationStage
from .exact import as_fraction
from .measurement import Measurement
from .measurement_replay import MeasurementReplay, replay_composed_measurement
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .receipts import Receipt, content_hash, make_receipt, verify_receipt


@dataclass(frozen=True)
class GaussianRational:
    re: Fraction
    im: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "re", as_fraction(self.re))
        object.__setattr__(self, "im", as_fraction(self.im))

    def __add__(self, other: GaussianRational) -> GaussianRational:
        return GaussianRational(self.re + other.re, self.im + other.im)

    def __mul__(self, other: GaussianRational) -> GaussianRational:
        return GaussianRational(self.re * other.re - self.im * other.im,
                                self.re * other.im + self.im * other.re)

    def conjugate(self) -> GaussianRational:
        return GaussianRational(self.re, -self.im)

    def norm_squared(self) -> Fraction:
        return self.re * self.re + self.im * self.im


Matrix = tuple[tuple[GaussianRational, ...], ...]
ZERO = GaussianRational(Fraction(0))
ONE = GaussianRational(Fraction(1))


def exact_matrix(rows: tuple[tuple[GaussianRational | int | Fraction, ...], ...]) -> Matrix:
    return tuple(tuple(value if isinstance(value, GaussianRational) else GaussianRational(value)
                       for value in row) for row in rows)


def _zero(n: int) -> Matrix:
    return tuple(tuple(ZERO for _ in range(n)) for _ in range(n))


def _identity(n: int) -> Matrix:
    return tuple(tuple(ONE if r == c else ZERO for c in range(n)) for r in range(n))


def _add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x + y for x, y in zip(ar, br, strict=True))
                 for ar, br in zip(a, b, strict=True))


def _mul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return tuple(tuple(sum((a[r][k] * b[k][c] for k in range(n)), start=ZERO)
                       for c in range(n)) for r in range(n))


def _adjoint(a: Matrix) -> Matrix:
    return tuple(tuple(a[c][r].conjugate() for c in range(len(a))) for r in range(len(a)))


def _scale(a: Matrix, q: Fraction) -> Matrix:
    return tuple(tuple(GaussianRational(q * x.re, q * x.im) for x in row) for row in a)


@dataclass(frozen=True)
class FiniteInstrumentModel:
    dimension: int
    groups: tuple[tuple[Matrix, ...], ...]

    def __post_init__(self) -> None:
        n = self.dimension
        if type(n) is not int or n <= 0 or type(self.groups) is not tuple or not self.groups:
            raise ValueError("positive finite dimension and explicit outcome groups are required")
        completeness = _zero(n)
        operators = 0
        for group in self.groups:
            if type(group) is not tuple:
                raise ValueError("Kraus groups must be immutable tuples")
            for k in group:
                if (type(k) is not tuple or len(k) != n
                        or any(type(row) is not tuple or len(row) != n
                               or any(not isinstance(x, GaussianRational) for x in row) for row in k)):
                    raise ValueError("Kraus operator has wrong exact square shape")
                completeness = _add(completeness, _mul(_adjoint(k), k))
                operators += 1
        if not operators or completeness != _identity(n):
            raise ValueError("Kraus completeness does not hold exactly")


@dataclass(frozen=True)
class FinitePositiveMixture:
    """Positivity is by a declared finite nonnegative mixture, never a float test."""

    components: tuple[tuple[Fraction, tuple[GaussianRational, ...]], ...]

    def density(self, n: int) -> Matrix:
        if type(self.components) is not tuple or not self.components:
            raise ValueError("nonempty immutable positive mixture required")
        rho = _zero(n)
        mass = Fraction(0)
        for weight, vector in self.components:
            weight = as_fraction(weight)
            if (weight < 0 or type(vector) is not tuple or len(vector) != n
                    or any(not isinstance(x, GaussianRational) for x in vector)):
                raise ValueError("mixture weight/vector is invalid")
            mass += weight * sum((x.norm_squared() for x in vector), start=Fraction(0))
            pure = tuple(tuple(x * y.conjugate() for y in vector) for x in vector)
            rho = _add(rho, _scale(pure, weight))
        if mass != 1:
            raise ValueError("mixture trace is not one")
        return rho


@dataclass(frozen=True)
class InstrumentOutcomeRecord:
    instrument_digest: str
    input_state_digest: str
    outcome: int
    probability: Fraction
    post_state: Matrix | None


def outcome_record(
    instrument: FiniteInstrumentModel, state: FinitePositiveMixture, outcome: int,
) -> InstrumentOutcomeRecord:
    if (not isinstance(instrument, FiniteInstrumentModel)
            or not isinstance(state, FinitePositiveMixture)
            or type(outcome) is not int or not 0 <= outcome < len(instrument.groups)):
        raise ValueError("instrument/state/outcome does not bind a finite problem")
    rho = state.density(instrument.dimension)
    unnormalized = _zero(instrument.dimension)
    for k in instrument.groups[outcome]:
        unnormalized = _add(unnormalized, _mul(_mul(k, rho), _adjoint(k)))
    trace = sum((unnormalized[r][r] for r in range(instrument.dimension)), start=ZERO)
    if trace.im != 0 or trace.re < 0:
        raise ValueError("non-real or negative probability")
    post = None if trace.re == 0 else _scale(unnormalized, 1 / trace.re)
    return InstrumentOutcomeRecord(content_hash(instrument), content_hash(rho), outcome, trace.re, post)


def is_outcome_repeatable(instrument: FiniteInstrumentModel) -> bool:
    """Exhaustive K_jb K_oa = 0, j != o; this decides the all-state criterion."""
    if not isinstance(instrument, FiniteInstrumentModel):
        raise ValueError("validated square instrument required")
    zero = _zero(instrument.dimension)
    return all(_mul(second, first) == zero
               for o, first_group in enumerate(instrument.groups)
               for j, second_group in enumerate(instrument.groups) if j != o
               for first in first_group for second in second_group)


@dataclass(frozen=True)
class QuantumMeasurementProblem:
    instrument: FiniteInstrumentModel
    state: FinitePositiveMixture
    outcome: int
    outcome_indications: tuple[Fraction, ...]
    measurement: Measurement
    stages: tuple[AffineCalibrationStage, ...]
    input_radius: Fraction
    require_outcome_repeatability: bool = True


@dataclass(frozen=True)
class QuantumMeasurementReplay:
    instrument_record: InstrumentOutcomeRecord
    measurement_replay: MeasurementReplay
    receipt: Receipt


def expected_instrument_mark(problem: QuantumMeasurementProblem) -> dict[str, object]:
    record = outcome_record(problem.instrument, problem.state, problem.outcome)
    if (type(problem.outcome_indications) is not tuple
            or len(problem.outcome_indications) != len(problem.instrument.groups)):
        raise ValueError("one indication per outcome required")
    indications = tuple(as_fraction(value) for value in problem.outcome_indications)
    return {"instrument_record": record, "indication": indications[problem.outcome]}


def replay_quantum_measurement(
    problem: QuantumMeasurementProblem, reaccessed_mark: object,
) -> Outcome[QuantumMeasurementReplay]:
    if not isinstance(problem, QuantumMeasurementProblem) or not isinstance(problem.measurement, Measurement):
        return Refused(RefusalCode.INVALID_INPUT, "independently supplied complete quantum measurement problem required")
    try:
        if type(problem.require_outcome_repeatability) is not bool:
            raise ValueError("repeatability requirement must be explicit boolean data")
        expected_mark = expected_instrument_mark(problem)
        record = expected_mark["instrument_record"]
        assert isinstance(record, InstrumentOutcomeRecord)
        if record.probability == 0:
            return Refused(RefusalCode.OUTSIDE_PROFILE, "selected event has zero declared probability")
        if problem.require_outcome_repeatability and not is_outcome_repeatable(problem.instrument):
            return Refused(RefusalCode.OUTSIDE_PROFILE, "required outcome repeatability does not hold")
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(RefusalCode.INVALID_INPUT, "invalid exact instrument/state/indication problem")
    if problem.measurement.observation.registration.mark != expected_mark:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "retained instrument record differs from recomputation on actual inputs")
    if problem.measurement.value_map.source_key != "indication":
        return Refused(RefusalCode.VALUE_MAP_MISMATCH, "measurement must read the instrument's retained indication")
    replayed = replay_composed_measurement(
        problem.measurement, problem.stages, problem.input_radius, reaccessed_mark,
    )
    if isinstance(replayed, Refused):
        return replayed
    receipt = make_receipt(
        "complete-declared-quantum-measurement", problem, (record, replayed.value),
        ("WDP-CH19-O04", "WDP-CH13-O01", "WDP-CH13-O02"),
    )
    if isinstance(receipt, Refused):
        return receipt
    return Accepted(QuantumMeasurementReplay(record, replayed.value, receipt.value))


def verify_quantum_measurement(
    candidate: QuantumMeasurementReplay, actual_problem: QuantumMeasurementProblem,
    reaccessed_mark: object,
) -> Outcome[bool]:
    if not isinstance(candidate, QuantumMeasurementReplay):
        return Refused(RefusalCode.INVALID_INPUT, "candidate has the wrong replay type")
    expected = replay_quantum_measurement(actual_problem, reaccessed_mark)
    if isinstance(expected, Refused):
        return expected
    bound = verify_receipt(candidate.receipt, actual_problem,
                           (candidate.instrument_record, candidate.measurement_replay))
    if isinstance(bound, Refused):
        return bound
    if candidate != expected.value:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "fresh hashes cannot replace full actual-problem recomputation")
    return Accepted(True)
