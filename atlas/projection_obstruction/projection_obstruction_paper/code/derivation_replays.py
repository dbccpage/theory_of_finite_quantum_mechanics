"""Exact finite examples for the metric, phase and connected-cumulant results.

These are replayable matrix calculations, not a verifier of the general proofs.
All calculations use SymPy exact arithmetic; no floating tolerance is used.
"""

from __future__ import annotations

from itertools import product
from math import factorial, prod

import sympy as sp
from short_time_jets import Y, Z, partial_trace, tensor


def _exact_scalar(value: object) -> sp.Expr:
    """Reject inexact inputs before any conversion can hide their provenance."""
    expression = sp.sympify(value)
    if not isinstance(expression, sp.Expr) or expression.has(sp.Float):
        raise TypeError("exact scalar required; floating-point inputs are not accepted")
    if expression.has(sp.nan, sp.oo, -sp.oo, sp.zoo):
        raise ValueError("finite exact scalar required")
    return expression


def _exact_matrix(matrix: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(matrix).applyfunc(_exact_scalar)


def _dimensions(dimensions: tuple[int, ...]) -> None:
    if not dimensions or any(type(d) is not int or d < 1 for d in dimensions):
        raise ValueError("nonempty positive integer tensor dimensions required")


def hermitian_trace_norm(matrix: sp.MatrixBase) -> sp.Expr:
    matrix = _exact_matrix(matrix).applyfunc(sp.simplify)
    if matrix != matrix.H:
        raise ValueError("Hermitian matrix required")
    return sp.simplify(sum(sp.Abs(value) * count for value, count in matrix.eigenvals().items()))


def mixed_certificate(p: sp.Rational, q: sp.Rational) -> dict[str, object]:
    """Primal/dual optimal-distance certificate for r_p tensor r_q and X tensor Z."""
    p, q = _exact_scalar(p), _exact_scalar(q)
    if not isinstance(p, sp.Rational) or not isinstance(q, sp.Rational):
        raise TypeError("exact rational factors required")
    if not (0 < p < 1 and 0 < q < 1):
        raise ValueError("full-rank rational factors required")
    r, s = sp.diag(p, 1 - p), sp.diag(q, 1 - q)
    a, b = 1 - 2 * p, 2 * q - 1
    derivative = a * tensor(Y, Z * s)
    normal = 2 * a * q * (1 - q) * tensor(Y, Z)
    c = 1 if q >= sp.Rational(1, 2) else -1
    diagonal = sp.diag((1 - q) / q, -1) if c == 1 else sp.diag(1, -q / (1 - q))
    witness = sp.sign(a) * tensor(Y, diagonal)
    tangent = a * c * tensor(Y, s)
    return dict(r=r, s=s, derivative=derivative, normal=normal,
                projected=a * b * tensor(Y, s), tangent=tangent, witness=witness,
                mu=4 * sp.Abs(a) * min(q, 1 - q), nu=8 * sp.Abs(a) * q * (1 - q))


def cycle_five_state() -> sp.Matrix:
    """Density at t=pi/4 for sum Z_j Z_(j+1) acting on |+>^5, up to global phase."""
    signs = []
    for bits in product((0, 1), repeat=5):
        parity = sum(bits) + sum(bits[j] * bits[(j + 1) % 5] for j in range(5))
        signs.append((-1) ** parity)
    vector = sp.Matrix(signs)
    return vector * vector.T / 32


def phase_envelope(lengths: tuple[sp.Expr, ...]) -> dict[str, sp.Expr]:
    """Full independent complex phases; lengths must be exactly ordered nonnegatives."""
    values = tuple(_exact_scalar(value) for value in lengths)
    if not values or any(value.is_nonnegative is not True for value in values):
        raise ValueError("a nonempty list of known nonnegative lengths is required")
    total = sum(values)
    lower = max(sp.S.Zero, 2 * max(values) - total)
    lo, hi = sp.simplify(lower**2), sp.simplify(total**2)
    return dict(minimum=lo, maximum=hi, midpoint=(lo + hi) / 2,
                radius=(hi - lo) / 2, mean=sum(value**2 for value in values))


def finite_sign_fiber(base: tuple[sp.Expr, ...], row: tuple[sp.Expr, ...]) -> dict[str, object]:
    """Enumerate a declared finite sign host, including endpoint witnesses."""
    if len(base) != len(row) or not base:
        raise ValueError("nonempty equally sized base and row required")
    base, row = tuple(map(_exact_scalar, base)), tuple(map(_exact_scalar, row))
    mass = sp.simplify(sum(sp.Abs(value)**2 for value in base))
    if mass.is_positive is not True:
        raise ValueError("positive total mass required")
    outcomes = []
    for signs in product((-1, 1), repeat=len(base)):
        amplitude = sum(a * z * sign for a, z, sign in zip(row, base, signs))
        outcomes.append((sp.simplify(sp.Abs(amplitude)**2 / mass), signs))
    minimum, min_signs = min(outcomes)
    maximum, max_signs = max(outcomes)
    return dict(values=tuple(sorted({value for value, _ in outcomes})),
                minimum=minimum, maximum=maximum, min_signs=min_signs, max_signs=max_signs,
                midpoint=(minimum + maximum) / 2, radius=(maximum - minimum) / 2,
                mean=sp.simplify(sum(value for value, _ in outcomes) / len(outcomes)))


def partitions(sites: tuple[int, ...]):
    """Each unordered set partition once, with blocks in canonical order."""
    if not sites:
        yield ()
        return
    head, *tail = sites
    for partition in partitions(tuple(tail)):
        yield ((head,),) + partition
        for j, block in enumerate(partition):
            yield partition[:j] + ((head,) + block,) + partition[j + 1:]


def compositions(total: int, count: int):
    if count == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, count - 1):
                yield (first,) + rest


def placed_tensor(blocks: tuple[tuple[int, ...], ...], matrices: tuple[sp.MatrixBase, ...],
                  dimensions: tuple[int, ...]) -> sp.Matrix:
    """Tensor disjoint blocks, restoring the original site order (also noncontiguous)."""
    _dimensions(dimensions)
    if (any(not block or any(type(site) is not int for site in block) for block in blocks)
            or sorted(site for block in blocks for site in block) != list(range(len(dimensions)))):
        raise ValueError("blocks must partition the sites")
    if len(matrices) != len(blocks):
        raise ValueError("one matrix per tensor block required")
    matrices = tuple(_exact_matrix(matrix) for matrix in matrices)
    if any(matrix.shape != (prod(dimensions[site] for site in block),) * 2
           for block, matrix in zip(blocks, matrices)):
        raise ValueError("matrix shape must match its tensor block")
    coordinates = list(product(*(range(d) for d in dimensions)))

    def index(values, block):
        result = 0
        for site in block:
            result = result * dimensions[site] + values[site]
        return result

    return sp.Matrix(len(coordinates), len(coordinates), lambda i, j: prod(
        matrix[index(coordinates[i], block), index(coordinates[j], block)]
        for block, matrix in zip(blocks, matrices)))


def cumulant_jets(derivatives: list[sp.MatrixBase], dimensions: tuple[int, ...],
                  keep: tuple[int, ...]) -> list[sp.Matrix]:
    """Connected cumulant derivatives from full state derivatives, not Taylor coefficients."""
    _dimensions(dimensions)
    derivatives = [_exact_matrix(derivative) for derivative in derivatives]
    if not keep or tuple(sorted(set(keep))) != keep or any(i < 0 or i >= len(dimensions) for i in keep):
        raise ValueError("nonempty ordered retained support required")
    local_dims = tuple(dimensions[i] for i in keep)
    order = len(derivatives) - 1
    if order < 0:
        raise ValueError("at least a zeroth derivative required")
    result = [sp.zeros(prod(local_dims)) for _ in derivatives]
    marginals = {}
    for partition in partitions(tuple(range(len(keep)))):
        weight = (-1)**(len(partition) - 1) * factorial(len(partition) - 1)
        for block in partition:
            if block not in marginals:
                marginals[block] = [partial_trace(d, dimensions, tuple(keep[i] for i in block))
                                    for d in derivatives]
        for j in range(order + 1):
            for degrees in compositions(j, len(partition)):
                coefficient = weight * factorial(j) // prod(factorial(n) for n in degrees)
                factors = tuple(marginals[block][n] for block, n in zip(partition, degrees))
                result[j] += coefficient * placed_tensor(partition, factors, local_dims)
    return [matrix.applyfunc(sp.simplify) for matrix in result]


def support_component(rho: sp.MatrixBase, dimensions: tuple[int, ...],
                      support: tuple[int, ...]) -> sp.Matrix:
    """T_S rho using the fixed current one-site marginals as references."""
    _dimensions(dimensions)
    rho = _exact_matrix(rho)
    count = len(dimensions)
    if tuple(sorted(set(support))) != support or any(i < 0 or i >= count for i in support):
        raise ValueError("ordered support required")
    references = [partial_trace(rho, dimensions, (i,)) for i in range(count)]
    value = sp.Matrix(rho)
    for site in range(count):
        remaining = tuple(i for i in range(count) if i != site)
        if remaining:
            replaced = placed_tensor((remaining, (site,)),
                                     (partial_trace(value, dimensions, remaining), references[site]),
                                     dimensions)
        else:
            replaced = sp.trace(value) * references[site]
        value = value - replaced if site in support else replaced
    return value.applyfunc(sp.simplify)


def cumulant_constants(size: int) -> tuple[int, int]:
    if size < 1:
        raise ValueError("positive support size required")
    sizes = [len(partition) for partition in partitions(tuple(range(size)))]
    return sum(factorial(n - 1) for n in sizes), sum(factorial(n) for n in sizes)


def exact_summary() -> dict[str, object]:
    certificate = mixed_certificate(sp.Rational(3, 4), sp.Rational(3, 4))
    cycle = cycle_five_state()
    return {
        "scope": "Exact finite examples only; general theorems have written proofs.",
        "mixed_mu": str(hermitian_trace_norm(certificate['derivative'] - certificate['tangent'])),
        "mixed_dual": str(sp.trace(certificate['witness'] * certificate['derivative'])),
        "mixed_nu": str(hermitian_trace_norm(certificate['normal'])),
        "cycle_purity": cycle * cycle == cycle,
        "cycle_pair_marginals_maximally_mixed": all(
            partial_trace(cycle, (2,) * 5, (a, b)) == sp.eye(4) / 4
            for a in range(5) for b in range(a + 1, 5)),
        "sign_fixture": {key: str(value) for key, value in
                         finite_sign_fiber((2, 1, 1), (sp.Rational(1, 2), sp.Rational(1, 4),
                                                       sp.Rational(1, 8))).items()},
        "cumulant_constants": [cumulant_constants(k) for k in range(1, 7)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(exact_summary(), indent=2))
