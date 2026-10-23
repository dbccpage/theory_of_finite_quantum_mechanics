"""Selected admission witness for the broader-work column of CH19-O02.

Positive Hilbert density, local Hermitian involutions, and tensor trace pairing
are declared inputs. Clauses (T), (NS), and classical (B) of CP do not choose
them. AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product

from .q2_reconstruction_package import (
    add,
    bell_density,
    comm,
    deterministic_chsh,
    equal,
    eye,
    kron,
    local_directions,
    mul,
    scale,
    sub,
    trace,
    trace_product,
)

SCHEMA = "wdp.ch19_o02_composition_admission.v1"
WITNESS_ID = "ch19-o02-composition-admission"


def _frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _transpose(matrix: tuple[tuple[Fraction, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(row[column] for row in matrix) for column in range(len(matrix)))


def _determinant(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    total = Fraction(0)
    for column in range(size):
        minor = tuple(
            tuple(row[index] for index in range(size) if index != column)
            for row in matrix[1:]
        )
        sign = Fraction(1 if column % 2 == 0 else -1)
        total += sign * matrix[0][column] * _determinant(minor)
    return total


def _principal_minors(matrix: tuple[tuple[Fraction, ...], ...]) -> tuple[Fraction, ...]:
    size = len(matrix)
    minors = []
    for mask in range(1, 1 << size):
        indices = tuple(index for index in range(size) if mask & (1 << index))
        block = tuple(tuple(matrix[row][column] for column in indices) for row in indices)
        minors.append(_determinant(block))
    return tuple(minors)


def _gram(vector: tuple[Fraction, ...]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(left * right for right in vector) for left in vector)


def _injective(images: tuple[object, ...]) -> bool:
    return len(set(images)) == len(images)


def _pr_probability(outcome_a: int, outcome_b: int, setting_x: int, setting_y: int) -> Fraction:
    correlated = outcome_a * outcome_b == (1 if setting_x * setting_y == 0 else -1)
    return Fraction(1, 2) if correlated else Fraction(0)


def _correlator(probabilities: dict[tuple[int, int, int, int], Fraction], setting_x: int, setting_y: int) -> Fraction:
    return sum(
        (
            Fraction(outcome_a * outcome_b) * probabilities[(outcome_a, outcome_b, setting_x, setting_y)]
            for outcome_a in (1, -1)
            for outcome_b in (1, -1)
        ),
        Fraction(0),
    )


def canonical_payload(witness: dict[str, object]) -> str:
    return json.dumps(witness, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def problem_sha256(witness: dict[str, object]) -> str:
    return hashlib.sha256(canonical_payload(witness).encode("utf-8")).hexdigest()


def composition_admission_witness() -> dict[str, object]:
    """Admit the CHSH package and separate it from CP."""
    left_carrier = (0, 1)
    right_carrier = (0, 1)
    identity_images = tuple((left, right) for left in left_carrier for right in right_carrier)
    dumped_images = tuple(right for _left in left_carrier for right in right_carrier)
    identity_injective = _injective(identity_images)
    dump_right_injective = _injective(dumped_images)

    joint = {
        (0, 0): Fraction(1, 2),
        (0, 1): Fraction(0),
        (1, 0): Fraction(0),
        (1, 1): Fraction(1, 2),
    }

    def omega(left_effect: tuple[Fraction, Fraction], right_effect: tuple[Fraction, Fraction]) -> Fraction:
        return sum(
            (
                left_effect[left] * right_effect[right] * joint[(left, right)]
                for left in left_carrier
                for right in right_carrier
            ),
            Fraction(0),
        )

    recovered = {
        (left, right): omega(
            (Fraction(1 if left == 0 else 0), Fraction(1 if left == 1 else 0)),
            (Fraction(1 if right == 0 else 0), Fraction(1 if right == 1 else 0)),
        )
        for left in left_carrier
        for right in right_carrier
    }
    classical_bilinear_recovers_joint = recovered == joint
    deterministic_values = sorted(
        {deterministic_chsh(assignment) for assignment in product((1, -1), repeat=4)}
    )
    deterministic_bound = max(abs(value) for value in deterministic_values) == 2

    pr = {
        (outcome_a, outcome_b, setting_x, setting_y): _pr_probability(
            outcome_a, outcome_b, setting_x, setting_y
        )
        for setting_x in (0, 1)
        for setting_y in (0, 1)
        for outcome_a in (1, -1)
        for outcome_b in (1, -1)
    }
    pr_normalized = all(
        sum(
            (pr[(outcome_a, outcome_b, setting_x, setting_y)] for outcome_a in (1, -1) for outcome_b in (1, -1)),
            Fraction(0),
        )
        == 1
        for setting_x in (0, 1)
        for setting_y in (0, 1)
    )
    pr_marginals = []
    for setting_x in (0, 1):
        for setting_y in (0, 1):
            for outcome_a in (1, -1):
                pr_marginals.append(
                    sum(
                        (pr[(outcome_a, outcome_b, setting_x, setting_y)] for outcome_b in (1, -1)),
                        Fraction(0),
                    )
                )
            for outcome_b in (1, -1):
                pr_marginals.append(
                    sum(
                        (pr[(outcome_a, outcome_b, setting_x, setting_y)] for outcome_a in (1, -1)),
                        Fraction(0),
                    )
                )
    pr_no_signalling = pr_normalized and all(marginal == Fraction(1, 2) for marginal in pr_marginals)
    pr_correlators = {
        f"{setting_x}{setting_y}": _correlator(pr, setting_x, setting_y)
        for setting_x in (0, 1)
        for setting_y in (0, 1)
    }
    pr_chsh = pr_correlators["00"] + pr_correlators["01"] + pr_correlators["10"] - pr_correlators["11"]

    factor = (Fraction(1), Fraction(0), Fraction(0), Fraction(1))
    factor_norm = sum((entry * entry for entry in factor), Fraction(0))
    density = scale(_gram(factor), Fraction(1, factor_norm))
    density_is_gram = equal(density, bell_density()) and trace(density) == 1 and equal(density, _transpose(density))
    a0, a1, b0, b1 = local_directions()
    locals_are_hermitian_involutions = all(
        equal(mul(observable, observable), eye(2)) and equal(observable, _transpose(observable))
        for observable in (a0, a1, b0, b1)
    )
    commutator_a = comm(a0, a1)
    commutator_b = comm(b0, b1)
    chsh_operator = add(kron(a0, add(b0, b1)), kron(a1, sub(b0, b1)))
    square_identity = equal(
        mul(chsh_operator, chsh_operator),
        sub(scale(eye(4), Fraction(4)), kron(commutator_a, commutator_b)),
    )
    operator_gap = sub(scale(eye(4), Fraction(8)), mul(chsh_operator, chsh_operator))
    operator_gap_psd = all(minor >= 0 for minor in _principal_minors(operator_gap))
    correlators = {
        "00": trace_product(density, kron(a0, b0)),
        "01": trace_product(density, kron(a0, b1)),
        "10": trace_product(density, kron(a1, b0)),
        "11": trace_product(density, kron(a1, b1)),
    }
    quantum_chsh = correlators["00"] + correlators["01"] + correlators["10"] - correlators["11"]
    quantum_trace = trace_product(density, chsh_operator)
    squared = quantum_chsh * quantum_chsh
    trace_square = trace_product(density, mul(chsh_operator, chsh_operator))
    return {
        "schema": SCHEMA,
        "witness_id": WITNESS_ID,
        "authority_effect": "none",
        "admitted": ["positive-hilbert-density", "local-hermitian-involutions", "tensor-trace-pairing"],
        "derived_from_cp": False,
        "cp_clauses": ["T-injective-tagging", "NS-no-signalling", "B-classical-bilinear"],
        "identity_tagging_injective": identity_injective,
        "dump_right_injective": dump_right_injective,
        "classical_bilinear_recovers_joint": classical_bilinear_recovers_joint,
        "deterministic_chsh_values": deterministic_values,
        "deterministic_absolute_bound_2": deterministic_bound,
        "pr_no_signalling": pr_no_signalling,
        "pr_chsh": _frac(pr_chsh),
        "pr_squared_exceeds_8": pr_chsh * pr_chsh > 8,
        "density_is_rational_gram": density_is_gram,
        "local_hermitian_involutions": locals_are_hermitian_involutions,
        "square_identity": square_identity,
        "operator_gap_principal_minors_nonnegative": operator_gap_psd,
        "correlators": {key: _frac(value) for key, value in correlators.items()},
        "quantum_chsh": _frac(quantum_chsh),
        "quantum_trace_matches_correlators": quantum_trace == quantum_chsh,
        "quantum_chsh_squared": _frac(squared),
        "trace_s_squared": _frac(trace_square),
        "scalar_variance_slack": _frac(trace_square - squared),
        "operator_bound_slack": _frac(Fraction(8) - squared),
        "above_classical_joint_bound": quantum_chsh > 2,
        "admitted_multiplicity": 1,
        "admitted_hilbert_dimension": 4,
        "cp_binary_carrier_atoms": 4,
        "multiplicity_named_by_cp": False,
    }
