"""Exact symbolic controls for the nine-ray Q(i)^3 rigidity reduction.

No repository code is imported. This checks reconstruction signs, uniqueness,
quadratic expansion, a generic matrix inverse identity used in the paper
proof, and the rational rescaling bounds. It does not prove global rigidity
or verify the whole paper proof in a formal proof assistant.
"""

from __future__ import annotations

import json

import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def zero(expression: sp.Expr) -> bool:
    return sp.expand(expression) == 0


def main() -> None:
    diagonal = sp.symbols("d0:3", real=True)
    real_part = sp.symbols("a01 a02 a12", real=True)
    imag_part = sp.symbols("b01 b02 b12", real=True)
    pairs = [(0, 1), (0, 2), (1, 2)]
    rho = sp.diag(*diagonal)
    for pair, a, b in zip(pairs, real_part, imag_part):
        j, k = pair
        rho[j, k] = a + sp.I * b
        rho[k, j] = a - sp.I * b
    require(rho == rho.conjugate().T, "candidate is Hermitian")

    basis = [sp.eye(3)[:, j] for j in range(3)]
    rays = basis[:]
    for j, k in pairs:
        rays.extend([basis[j] + basis[k], basis[j] + sp.I * basis[k]])
    values = [sp.expand((v.conjugate().T * rho * v)[0]
                        / (v.conjugate().T * v)[0]) for v in rays]
    expected = list(diagonal)
    for (j, k), a, b in zip(pairs, real_part, imag_part):
        expected.extend([(diagonal[j] + diagonal[k]) / 2 + a,
                         (diagonal[j] + diagonal[k]) / 2 - b])
    require(all(zero(x - y) for x, y in zip(values, expected)),
            "all nine evaluations, including imaginary signs")
    coefficients = list(diagonal) + list(real_part) + list(imag_part)
    tomography = sp.Matrix(values).jacobian(coefficients)
    require(tomography.det() != 0, "tomography has exact rank nine")

    measurements = sp.symbols("m0:9", real=True)
    reconstructed = list(measurements[:3])
    reconstructed_real = []
    reconstructed_imag = []
    for index, (j, k) in enumerate(pairs):
        mean = (measurements[j] + measurements[k]) / 2
        reconstructed_real.append(measurements[3 + 2 * index] - mean)
        reconstructed_imag.append(mean - measurements[4 + 2 * index])
    substitution = dict(zip(coefficients,
                            reconstructed + reconstructed_real + reconstructed_imag))
    require(all(zero(value.subs(substitution) - measurement)
                for value, measurement in zip(values, measurements)),
            "candidate recovers arbitrary rational measurements")

    x = sp.symbols("x0:3", real=True)
    y = sp.symbols("y0:3", real=True)
    v = sp.Matrix([a + sp.I * b for a, b in zip(x, y)])
    numerator = sp.expand((v.conjugate().T * rho * v)[0])
    expansion = sum(diagonal[j] * (x[j] ** 2 + y[j] ** 2) for j in range(3))
    for (j, k), a, b in zip(pairs, real_part, imag_part):
        expansion += 2 * a * (x[j] * x[k] + y[j] * y[k])
        expansion -= 2 * b * (x[j] * y[k] - y[j] * x[k])
    require(zero(numerator - expansion), "generic quadratic expansion")
    require(zero(sp.im(numerator)), "quadratic numerator is rational over Q(i)")

    # Polynomial identity underlying U D^(-1) U* = I when U*U=D.
    # The premise U*U=D and the nonzero determinant are proved in the note;
    # this calculation does not assert those premises for arbitrary matrices.
    entries = sp.symbols("u0:9")
    matrix = sp.Matrix(3, 3, entries)
    identity_residual = matrix * matrix.adjugate() - matrix.det() * sp.eye(3)
    require(all(zero(entry) for entry in identity_residual),
            "generic three by three adjugate identity")

    bound = sp.symbols("B", nonnegative=True)
    epsilon = 1 / (3 * (bound + 1))
    require(sp.cancel(sp.Rational(1, 3) - epsilon * bound - epsilon) == 0,
            "rescaled lower bound")
    require(sp.cancel(sp.Rational(1, 3) + epsilon * bound
                      - (2 * bound + 1) / (3 * (bound + 1))) == 0,
            "rescaled upper bound")
    require(sp.cancel(sp.Rational(2, 3)
                      - (2 * bound + 1) / (3 * (bound + 1)) - epsilon) == 0,
            "upper bound is strictly below two thirds")
    require(epsilon.is_positive is True, "rescaling is positive, including B=0")
    require(epsilon.subs(bound, 0) == sp.Rational(1, 3), "zero-bound control")

    # A wrong sign on an imaginary off-diagonal must fail the same evaluation.
    require(not zero(values[4] - ((diagonal[0] + diagonal[1]) / 2 + imag_part[0])),
            "negative control rejects reversed imaginary sign")
    print(json.dumps({"status": "PASS", "sympy_version": sp.__version__,
                      "tomography_rank": tomography.rank(),
                      "scope": "symbolic algebra controls; no global rigidity claim"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
