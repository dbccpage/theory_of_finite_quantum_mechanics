"""Exact Gaussian-rational finite process model."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from typing import Iterable

from hermitianization.model import GaussianRational
from state_effect_readout.model import (
    GMatrix,
    add,
    dagger,
    frobenius_square,
    gmatrix,
    gram,
    identity,
    matmul,
    scale_real,
    shape,
)


def zero_matrix(rows: int, cols: int) -> GMatrix:
    if rows <= 0 or cols <= 0:
        raise ValueError("matrix dimensions must be positive")
    return tuple(tuple(GaussianRational.of(0) for _ in range(cols)) for _ in range(rows))


def sum_matrices(matrices: Iterable[GMatrix], dimension: int) -> GMatrix:
    result = zero_matrix(dimension, dimension)
    for value in matrices:
        result = add(result, value)
    return result


@dataclass(frozen=True)
class EnsembleState:
    factors: tuple[GMatrix, ...]

    def __post_init__(self) -> None:
        if not self.factors:
            raise ValueError("ensemble must contain at least one factor")
        dimension = shape(self.factors[0])[0]
        if any(shape(factor) != (dimension, dimension) for factor in self.factors):
            raise ValueError("ensemble factors must be square with equal dimensions")
        if self.total_mass <= 0:
            raise ValueError("ensemble must have positive total mass")

    @property
    def dimension(self) -> int:
        return shape(self.factors[0])[0]

    @property
    def total_mass(self) -> Fraction:
        return sum((frobenius_square(factor) for factor in self.factors), Fraction(0))

    @property
    def density(self) -> GMatrix:
        numerator = sum_matrices((gram(factor) for factor in self.factors), self.dimension)
        return scale_real(Fraction(1, 1) / self.total_mass, numerator)


@dataclass(frozen=True)
class KrausProcess:
    operators: tuple[GMatrix, ...]

    def __post_init__(self) -> None:
        if not self.operators:
            raise ValueError("process must contain at least one operator")
        dimension = shape(self.operators[0])[0]
        if any(shape(operator) != (dimension, dimension) for operator in self.operators):
            raise ValueError("process operators must be square with equal dimensions")
        completeness = sum_matrices((gram(operator) for operator in self.operators), dimension)
        if completeness != identity(dimension):
            raise ValueError("process operators do not resolve the identity")

    @property
    def dimension(self) -> int:
        return shape(self.operators[0])[0]


def post_factor(factor: GMatrix, operator: GMatrix) -> GMatrix:
    return matmul(factor, dagger(operator))


def apply_process(state: EnsembleState, process: KrausProcess) -> EnsembleState:
    if state.dimension != process.dimension:
        raise ValueError("state/process dimension mismatch")
    return EnsembleState(tuple(
        post_factor(factor, operator)
        for factor in state.factors
        for operator in process.operators
    ))


def branch_factors(state: EnsembleState, operator: GMatrix) -> tuple[GMatrix, ...]:
    if shape(operator) != (state.dimension, state.dimension):
        raise ValueError("state/operator dimension mismatch")
    return tuple(post_factor(factor, operator) for factor in state.factors)


def branch_mass(state: EnsembleState, operator: GMatrix) -> Fraction:
    return sum((frobenius_square(factor) for factor in branch_factors(state, operator)), Fraction(0))


def branch_probability(state: EnsembleState, process: KrausProcess, index: int) -> Fraction:
    return branch_mass(state, process.operators[index]) / state.total_mass


def conditioned_branch(
    state: EnsembleState, process: KrausProcess, index: int
) -> EnsembleState | None:
    factors = branch_factors(state, process.operators[index])
    if all(frobenius_square(factor) == 0 for factor in factors):
        return None
    return EnsembleState(factors)


def compose_process(first: KrausProcess, second: KrausProcess) -> KrausProcess:
    if first.dimension != second.dimension:
        raise ValueError("process dimension mismatch")
    return KrausProcess(tuple(
        matmul(later, earlier)
        for earlier in first.operators
        for later in second.operators
    ))


def kronecker(a: GMatrix, b: GMatrix) -> GMatrix:
    ar, ac = shape(a)
    br, bc = shape(b)
    return tuple(
        tuple(a[i // br][j // bc] * b[i % br][j % bc] for j in range(ac * bc))
        for i in range(ar * br)
    )


def tensor_process(left: KrausProcess, right: KrausProcess) -> KrausProcess:
    return KrausProcess(tuple(
        kronecker(a, b) for a in left.operators for b in right.operators
    ))


def unitary_process(operator: GMatrix) -> KrausProcess:
    return KrausProcess((operator,))


def scaled_identity(dimension: int, scale: Fraction) -> GMatrix:
    return scale_real(scale, identity(dimension))


def rational_square_root(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator_root = isqrt(value.numerator)
    denominator_root = isqrt(value.denominator)
    if numerator_root * numerator_root != value.numerator:
        return None
    if denominator_root * denominator_root != value.denominator:
        return None
    return Fraction(numerator_root, denominator_root)


def exact_standard_real_hadamard_available() -> bool:
    """Only the standard real representative; a Gaussian-rational phase multiple exists."""
    return rational_square_root(Fraction(1, 2)) is not None


def x_gate() -> GMatrix:
    return gmatrix([[0, 1], [1, 0]])


def phase_s_gate() -> GMatrix:
    return gmatrix([[1, 0], [0, [0, 1]]])


def identity_instrument_single(dimension: int) -> KrausProcess:
    return KrausProcess((identity(dimension),))


def identity_instrument_split(dimension: int) -> KrausProcess:
    return KrausProcess((
        scaled_identity(dimension, Fraction(3, 5)),
        scaled_identity(dimension, Fraction(4, 5)),
    ))
