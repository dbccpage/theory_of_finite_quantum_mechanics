"""Selected finite witness for the broader-work column of CH19-O01.

The §13.5 four-level sensor, a declared code partition, and a declared
within-context iid protocol are connected to the compatible-polytope repair.
The frequency table does not entail that protocol. AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product

from .empirical_repair import Scenario, iid_l1_failure, sampling_tolerance
from .obstruction import solve_standard_lp, verify_standard_lp
from .outcomes import Accepted

SCHEMA = "wdp.ch19_o01_sensor_repair.v1"
WITNESS_ID = "ch19-o01-sensor-repair"

# §13.5 intervals, written with rational endpoints. The cut used below is the
# declared code partition, not a theorem about these numerals.
CALIBRATION_S13_5 = {
    0: (Fraction(0), Fraction(2, 5)),
    1: (Fraction(2, 5), Fraction(9, 10)),
    2: (Fraction(9, 10), Fraction(3, 2)),
    3: (Fraction(3, 2), Fraction(2)),
}
CALIBRATION_SAME_CUT = {
    0: (Fraction(0), Fraction(1, 4)),
    1: (Fraction(1, 4), Fraction(9, 10)),
    2: (Fraction(9, 10), Fraction(5, 4)),
    3: (Fraction(5, 4), Fraction(2)),
}
PARTITION_P = {0: 0, 1: 0, 2: 1, 3: 1}
PARTITION_P_PRIME = {0: 0, 1: 1, 2: 1, 3: 1}

C0_ADMITTED = (0,) * 9 + (1,) * 3
C0_REFUSED = (3,)
C1_ADMITTED = (
    (0, 0),
    (0, 1),
    (1, 0),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 0),
    (2, 1),
    (3, 0),
    (3, 1),
    (2, 0),
    (3, 0),
)
C1_REFUSED = ((1, 1),)


def _frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _bin_one(code: int, partition: dict[int, int]) -> int:
    if code not in partition:
        raise ValueError("code outside the declared sensor alphabet")
    return partition[code]


def bin_context(trials: tuple, partition: dict[int, int]) -> tuple[tuple[int, ...], ...]:
    binned = []
    for trial in trials:
        if type(trial) is int:
            binned.append((_bin_one(trial, partition),))
        else:
            binned.append(tuple(_bin_one(code, partition) for code in trial))
    return tuple(binned)


def _frequency(binned: tuple[tuple[int, ...], ...], sections: tuple[tuple[int, ...], ...]) -> tuple[Fraction, ...]:
    counts = {section: 0 for section in sections}
    for trial in binned:
        if trial not in counts:
            raise ValueError("binned trial is not a section of the context")
        counts[trial] += 1
    total = len(binned)
    if total <= 0:
        raise ValueError("a context needs at least one admitted trial")
    return tuple(Fraction(counts[section], total) for section in sections)


def _l1(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    return sum((abs(a - b) for a, b in zip(left, right, strict=True)), Fraction(0))


def _scenario() -> Scenario:
    return Scenario(measurements=2, outcomes=2, contexts=((0,), (0, 1)))


def _pushforward_uniform() -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Independent uniform raw codes, binned by PARTITION_P."""
    single = [Fraction(0), Fraction(0)]
    for code in range(4):
        single[_bin_one(code, PARTITION_P)] += Fraction(1, 4)
    joint = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    sections = ((0, 0), (0, 1), (1, 0), (1, 1))
    index = {section: at for at, section in enumerate(sections)}
    for left, right in product(range(4), repeat=2):
        section = (_bin_one(left, PARTITION_P), _bin_one(right, PARTITION_P))
        joint[index[section]] += Fraction(1, 16)
    return (tuple(single), tuple(joint))


def _exhaustive_binary_second_moment() -> tuple[Fraction, Fraction]:
    """n=2, m=2, p=(1/2,1/2). Returns (E||f-p||_2^2, E||f-p||_1^2)."""
    population = (Fraction(1, 2), Fraction(1, 2))
    squared_l2 = Fraction(0)
    squared_l1 = Fraction(0)
    weight = Fraction(1, 4)
    for draws in product(range(2), repeat=2):
        counts = [0, 0]
        for draw in draws:
            counts[draw] += 1
        frequency = (Fraction(counts[0], 2), Fraction(counts[1], 2))
        gap = tuple(frequency[i] - population[i] for i in range(2))
        squared_l2 += weight * sum((coordinate * coordinate for coordinate in gap), Fraction(0))
        distance = sum((abs(coordinate) for coordinate in gap), Fraction(0))
        squared_l1 += weight * distance * distance
    return squared_l2, squared_l1


def _repair_exact(scenario: Scenario, source: tuple[tuple[Fraction, ...], ...]):
    """Exact LP optimum with a pure primal/dual replay. No native functional."""
    program = scenario.repair_program(source)
    result = solve_standard_lp(*program)
    if not isinstance(result, Accepted):
        raise ValueError(f"compatible-polytope repair was refused: {result.detail}")
    solution = result.value
    if not verify_standard_lp(*program, solution):
        raise ValueError("primal/dual replay failed")
    repaired = scenario.unpack(solution.primal)
    distance = max(_l1(left, right) for left, right in zip(source, repaired, strict=True))
    if solution.value != distance or not scenario.compatible(repaired):
        raise ValueError("solver repair does not meet the minimax L1 claim")
    return repaired, solution


def _closed_form_repair() -> tuple[tuple[Fraction, ...], tuple[Fraction, ...], Fraction]:
    repaired_0 = (Fraction(3, 4), Fraction(1, 4))
    repaired_1 = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), Fraction(0))
    return repaired_0, repaired_1, Fraction(1, 2)


def canonical_payload(witness: dict[str, object]) -> str:
    return json.dumps(witness, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def problem_sha256(witness: dict[str, object]) -> str:
    return hashlib.sha256(canonical_payload(witness).encode("utf-8")).hexdigest()


def sensor_repair_witness() -> dict[str, object]:
    """One selected sensor pair, its repair, and the sampling fence."""
    scenario = _scenario()
    sections = scenario.sections()
    binned_0 = bin_context(C0_ADMITTED, PARTITION_P)
    binned_1 = bin_context(C1_ADMITTED, PARTITION_P)
    if bin_context(C0_ADMITTED + C0_REFUSED, PARTITION_P) == binned_0:
        raise ValueError("a refused trial must be able to change the bin list")
    if bin_context(C1_ADMITTED + C1_REFUSED, PARTITION_P) == binned_1:
        raise ValueError("a refused joint trial must be able to change the bin list")
    source = (
        _frequency(binned_0, sections[0]),
        _frequency(binned_1, sections[1]),
    )
    if source != (
        (Fraction(1), Fraction(0)),
        (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2), Fraction(0)),
    ):
        raise ValueError("admitted bins do not match the selected table")
    same_cut = (
        _frequency(bin_context(C0_ADMITTED, PARTITION_P), sections[0]),
        _frequency(bin_context(C1_ADMITTED, PARTITION_P), sections[1]),
    )
    if same_cut != source:
        raise ValueError("partition, not the volt numerals, is the repair input")
    if CALIBRATION_S13_5 == CALIBRATION_SAME_CUT:
        raise ValueError("the alternate calibration must differ as an interval table")
    shifted = (
        _frequency(bin_context(C0_ADMITTED, PARTITION_P_PRIME), sections[0]),
        _frequency(bin_context(C1_ADMITTED, PARTITION_P_PRIME), sections[1]),
    )
    if shifted == source:
        raise ValueError("redeclaring the code cut must change the frequency table")
    if shifted[0] != (Fraction(3, 4), Fraction(1, 4)):
        raise ValueError("redeclared single-sensor frequency is wrong")

    closed_0, closed_1, closed_radius = _closed_form_repair()
    if _l1(closed_0, source[0]) != closed_radius or _l1(closed_1, source[1]) != closed_radius:
        raise ValueError("closed-form repair misses the claimed radius")
    if (closed_0[0], closed_1[0] + closed_1[1]) != (Fraction(3, 4), Fraction(3, 4)):
        raise ValueError("closed-form repair is not compatible on v")
    repaired, solution = _repair_exact(scenario, source)
    if solution.value != closed_radius:
        raise ValueError("solver radius disagrees with the closed form")

    population = _pushforward_uniform()
    if population != ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 4),) * 4):
        raise ValueError("uniform raw codes do not push forward as claimed")
    if not scenario.compatible(population):
        raise ValueError("shared uniform preparation is not compatible after binning")
    _population_repaired, population_solution = _repair_exact(scenario, population)
    if population_solution.value != 0:
        raise ValueError("a compatible population must have repair radius zero")

    incompatible = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    )
    _incompatible_repaired, incompatible_solution = _repair_exact(scenario, incompatible)
    if incompatible_solution.value != 1:
        raise ValueError("distinct preparations of the same sensor need not be compatible")

    squared_l2, squared_l1 = _exhaustive_binary_second_moment()
    if squared_l2 != Fraction(1, 4) or squared_l1 != Fraction(1, 2):
        raise ValueError("binary second-moment identity failed")
    formula = (1 - (Fraction(1, 2) ** 2 + Fraction(1, 2) ** 2)) / 2
    if formula != squared_l2:
        raise ValueError("variance formula disagrees with the exhaustive average")
    empirical = source[1]
    sum_squares = sum((coordinate * coordinate for coordinate in empirical), Fraction(0))
    iid_at_table = (1 - sum_squares) / len(C1_ADMITTED)
    if iid_at_table != Fraction(5, 96):
        raise ValueError("iid formula at the recorded joint table is wrong")
    if iid_at_table == 0:
        raise ValueError("the fence requires a non-Dirac table")

    radii = (Fraction(1, 2), Fraction(1))
    runs = (binned_0, binned_1)
    pairs, union_bound = sampling_tolerance(scenario, runs, radii)
    if pairs != ((0, 1, Fraction(3, 2)),) or union_bound != Fraction(7, 12):
        raise ValueError("declared trial-count tolerance is wrong")
    if iid_l1_failure(12, 2, Fraction(1, 2)) != Fraction(1, 3):
        raise ValueError("single-context Markov bound is wrong")
    if iid_l1_failure(12, 4, Fraction(1)) != Fraction(1, 4):
        raise ValueError("joint-context Markov bound is wrong")

    return {
        "schema": SCHEMA,
        "witness_id": WITNESS_ID,
        "package": "sensor-pair-P",
        "authority_effect": "none",
        "premises_from_table": False,
        "calibration": "S13.5",
        "partition": "codes {0,1}->0, {2,3}->1",
        "contexts": ["v", "v,w"],
        "admitted_trials": [len(C0_ADMITTED), len(C1_ADMITTED)],
        "refused_trials_excluded": [len(C0_REFUSED), len(C1_REFUSED)],
        "frequency": [_frac(value) for row in source for value in row],
        "closed_form_frequency_l1": _frac(closed_radius),
        "repair_radius": _frac(solution.value),
        "repaired": [_frac(value) for row in repaired for value in row],
        "primal": [_frac(value) for value in solution.primal],
        "dual": [_frac(value) for value in solution.dual],
        "lp_value": _frac(solution.value),
        "uniform_population_radius": "0/1",
        "incompatible_preparation_radius": "1/1",
        "same_partition_ignores_volt_endpoints": True,
        "redeclared_partition_changes_frequency": True,
        "exhaustive_binary_l2": _frac(squared_l2),
        "exhaustive_binary_l1_squared": _frac(squared_l1),
        "fixed_multiset_squared_error": "0/1",
        "iid_formula_at_recorded_joint": _frac(iid_at_table),
        "declared_radii": [_frac(radius) for radius in radii],
        "pair_tolerance": "3/2",
        "union_bound": _frac(union_bound),
    }
