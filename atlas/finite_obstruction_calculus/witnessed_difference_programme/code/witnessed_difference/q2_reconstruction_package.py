"""Exact witness for the selected Q2 reconstruction package.

AuthorityEffect: None. The matrices below are a finite certificate for one
declared Hilbert/tensor/trace package. They do not derive that package from
signed block masses or from a classical instrument quotient.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Sequence

Matrix = tuple[tuple[Fraction, ...], ...]

SCHEMA = "wdp.q2_reconstruction_package.v1"
WITNESS_ID = "q2-reconstruction-package"


def _F(value: int | Fraction, denominator: int = 1) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(value, denominator)


def eye(size: int) -> Matrix:
    return tuple(
        tuple(_F(1 if row == column else 0) for column in range(size))
        for row in range(size)
    )


def scale(matrix: Matrix, factor: Fraction) -> Matrix:
    return tuple(tuple(factor * entry for entry in row) for row in matrix)


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def sub(left: Matrix, right: Matrix) -> Matrix:
    return add(left, scale(right, Fraction(-1)))


def mul(left: Matrix, right: Matrix) -> Matrix:
    width = len(right[0])
    return tuple(
        tuple(
            sum((left[row][k] * right[k][column] for k in range(len(right))), Fraction(0))
            for column in range(width)
        )
        for row in range(len(left))
    )


def kron(left: Matrix, right: Matrix) -> Matrix:
    left_n = len(left)
    right_n = len(right)
    size = left_n * right_n
    out = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for i, left_row in enumerate(left):
        for j, left_entry in enumerate(left_row):
            for k, right_row in enumerate(right):
                for ell, right_entry in enumerate(right_row):
                    out[i * right_n + k][j * right_n + ell] = left_entry * right_entry
    return tuple(tuple(row) for row in out)


def trace(matrix: Matrix) -> Fraction:
    return sum((matrix[i][i] for i in range(len(matrix))), Fraction(0))


def trace_product(state: Matrix, operator: Matrix) -> Fraction:
    return trace(mul(state, operator))


def comm(left: Matrix, right: Matrix) -> Matrix:
    return sub(mul(left, right), mul(right, left))


def equal(left: Matrix, right: Matrix) -> bool:
    return left == right


def pauli_x() -> Matrix:
    return ((_F(0), _F(1)), (_F(1), _F(0)))


def pauli_z() -> Matrix:
    return ((_F(1), _F(0)), (_F(0), _F(-1)))


def bell_density() -> Matrix:
    half = Fraction(1, 2)
    zero = Fraction(0)
    return (
        (half, zero, zero, half),
        (zero, zero, zero, zero),
        (zero, zero, zero, zero),
        (half, zero, zero, half),
    )


def local_directions() -> tuple[Matrix, Matrix, Matrix, Matrix]:
    z_matrix, x_matrix = pauli_z(), pauli_x()
    three, four, five = Fraction(3), Fraction(4), Fraction(5)
    b0 = scale(add(scale(z_matrix, three), scale(x_matrix, four)), Fraction(1, 5))
    b1 = scale(sub(scale(z_matrix, three), scale(x_matrix, four)), Fraction(1, 5))
    return z_matrix, x_matrix, b0, b1


def _effect(sign: int, observable: Matrix) -> Matrix:
    return scale(add(eye(2), scale(observable, Fraction(sign))), Fraction(1, 2))


def deterministic_chsh(assignment: Sequence[int]) -> int:
    a0, a1, b0, b1 = assignment
    return a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1


def canonical_payload(witness: dict[str, object]) -> str:
    return json.dumps(witness, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def problem_sha256(witness: dict[str, object]) -> str:
    return hashlib.sha256(canonical_payload(witness).encode("utf-8")).hexdigest()


def q2_representation_witness() -> dict[str, object]:
    """One rational Q2 representation and the two exclusions it certifies."""
    a0, a1, b0, b1 = local_directions()
    density = bell_density()
    for observable in (a0, a1, b0, b1):
        if not equal(mul(observable, observable), eye(2)):
            raise ValueError("local observable is not an involution")
    commutator_a = comm(a0, a1)
    commutator_b = comm(b0, b1)
    chsh_operator = add(
        kron(a0, add(b0, b1)),
        kron(a1, sub(b0, b1)),
    )
    square = mul(chsh_operator, chsh_operator)
    predicted = sub(scale(eye(4), Fraction(4)), kron(commutator_a, commutator_b))
    if not equal(square, predicted):
        raise ValueError("CHSH square identity failed")
    correlators = {
        "00": trace_product(density, kron(a0, b0)),
        "01": trace_product(density, kron(a0, b1)),
        "10": trace_product(density, kron(a1, b0)),
        "11": trace_product(density, kron(a1, b1)),
    }
    chsh = correlators["00"] + correlators["01"] + correlators["10"] - correlators["11"]
    if trace_product(density, chsh_operator) != chsh:
        raise ValueError("correlator sum disagrees with the operator trace")
    marginals = (
        trace_product(density, kron(a0, eye(2))),
        trace_product(density, kron(a1, eye(2))),
        trace_product(density, kron(eye(2), b0)),
        trace_product(density, kron(eye(2), b1)),
    )
    if marginals != (Fraction(0), Fraction(0), Fraction(0), Fraction(0)):
        raise ValueError("local marginals are not uniform")
    probabilities: dict[str, str] = {}
    for x_index, a_obs in enumerate((a0, a1)):
        for y_index, b_obs in enumerate((b0, b1)):
            correlator = correlators[f"{x_index}{y_index}"]
            for outcome_a in (1, -1):
                for outcome_b in (1, -1):
                    predicted_probability = Fraction(1, 4) * (
                        1 + Fraction(outcome_a * outcome_b) * correlator
                    )
                    effect = kron(_effect(outcome_a, a_obs), _effect(outcome_b, b_obs))
                    actual = trace_product(density, effect)
                    if actual != predicted_probability:
                        raise ValueError("Born table disagrees with the correlator formula")
                    key = f"{x_index}{y_index}:{outcome_a}:{outcome_b}"
                    probabilities[key] = f"{actual.numerator}/{actual.denominator}"
    assignments = [
        (a0_sign, a1_sign, b0_sign, b1_sign)
        for a0_sign in (1, -1)
        for a1_sign in (1, -1)
        for b0_sign in (1, -1)
        for b1_sign in (1, -1)
    ]
    local_values = {deterministic_chsh(assignment) for assignment in assignments}
    squared = chsh * chsh
    return {
        "schema": SCHEMA,
        "witness_id": WITNESS_ID,
        "package": "Q2",
        "carrier": "C^2 x C^2",
        "multiplicity": 1,
        "state": "bell-projector",
        "directions": "Z,X,(3Z+4X)/5,(3Z-4X)/5",
        "correlators": {key: f"{value.numerator}/{value.denominator}" for key, value in correlators.items()},
        "probabilities": probabilities,
        "chsh": f"{chsh.numerator}/{chsh.denominator}",
        "chsh_squared": f"{squared.numerator}/{squared.denominator}",
        "operator_square_slack": f"{(8 - squared).numerator}/{(8 - squared).denominator}",
        "trace_s_squared": f"{trace_product(density, square).numerator}/{trace_product(density, square).denominator}",
        "deterministic_chsh_values": sorted(local_values),
        "classical_joint_excluded": chsh > 2,
        "pr_chsh": "4/1",
        "pr_excluded_by_q2_bound": Fraction(16) > 8,
        "block_mass_not_sufficient": True,
        "instrument_quotient_not_used": True,
    }
