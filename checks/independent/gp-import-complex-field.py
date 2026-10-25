"""Integer check of the 1+i product and one conjugate-symmetric Gauss-integer matrix."""

from __future__ import annotations

import sympy as sp


def gadd(z, w):
    return (sp.expand(z[0] + w[0]), sp.expand(z[1] + w[1]))


def gmul(z, w):
    return (
        sp.expand(z[0] * w[0] - z[1] * w[1]),
        sp.expand(z[0] * w[1] + z[1] * w[0]),
    )


def gconj(z):
    return (z[0], sp.expand(-z[1]))


def main() -> None:
    a, b, p, q, n = sp.symbols("a b p q n")
    xr, xi = sp.symbols("xr xi")
    failures = 0

    product = gmul((1, 1), (a, b))
    if product != (a - b, a + b):
        failures += 1
    swapped = gmul((a, b), (1, 1))
    if swapped != (a - b, a + b):
        failures += 1
    if sp.expand((a - b) + (a + b) - 2 * a) != 0:
        failures += 1
    parity_cases = 0
    for real in range(-12, 13):
        for imag_part in range(-12, 13):
            value = (real, imag_part)
            for sample in (gmul((1, 1), value), gmul(value, (1, 1))):
                if sample != (real - imag_part, real + imag_part):
                    failures += 1
                if sample[0] % 2 != sample[1] % 2 or sample == (1, 0):
                    failures += 1
                parity_cases += 1

    imag = sp.expand((p * q + q * p) - q - q * (2 * p - 1))
    if imag != 0:
        failures += 1
    reduction = sp.expand((2 * p - 1) ** 2 - 5 - 4 * (p * p - p - 1))
    if reduction != 0:
        failures += 1
    gap = sp.expand((n - 3) * (n + 3) - (n**2 - 9))
    if gap != 0:
        failures += 1
    small = [k * k for k in (-2, -1, 0, 1, 2)]
    if 5 in small:
        failures += 1

    c, d = sp.symbols("c d")
    norm_gap = sp.expand(
        (a * c - b * d) ** 2
        + (a * d + b * c) ** 2
        - (a * a + b * b) * (c * c + d * d)
    )
    if norm_gap != 0:
        failures += 1

    zero = (sp.Integer(0), sp.Integer(0))
    one = (sp.Integer(1), sp.Integer(0))
    column_x = (xr, xi)
    column_y = (a, b)
    top = gadd(gmul(zero, column_x), gmul(one, column_y))
    bot = gadd(gmul(one, column_x), gmul(one, column_y))
    if top != column_y or bot != gadd(column_x, column_y):
        failures += 1
    entries = ((zero, one), (one, one))
    if any(gconj(entries[i][j]) != entries[j][i] for i in range(2) for j in range(2)):
        failures += 1

    lam = (p, q)
    char_diff = gadd(
        gmul(gmul(lam, lam), column_x),
        gmul(gadd((sp.expand(-one[0]), sp.expand(-one[1])), (sp.expand(-lam[0]), sp.expand(-lam[1]))), column_x),
    )
    manual = sp.expand((p + q * sp.I) ** 2 - (p + q * sp.I) - 1)
    manual_x = sp.expand(manual * (xr + xi * sp.I))
    matrix = sp.Matrix([[0, 1], [1, 1]])
    if matrix.conjugate().T != matrix:
        failures += 1
    scalar = p + q * sp.I
    first_coord = xr + xi * sp.I
    eigen_column = sp.Matrix([first_coord, scalar * first_coord])
    residual = (matrix * eigen_column - scalar * eigen_column).applyfunc(sp.expand)
    if residual[0] != 0 or sp.expand(residual[1] + manual_x) != 0:
        failures += 1

    if sp.expand(char_diff[0] + sp.I * char_diff[1] - manual_x) != 0:
        failures += 1

    witness = gmul((1, 1), (1, 0))
    if witness != (1, 1):
        failures += 1
    image = gadd(gmul(zero, (1, 0)), gmul(one, (0, 0))), gadd(gmul(one, (1, 0)), gmul(one, (0, 0)))
    if image != ((0, 0), (1, 0)):
        failures += 1

    if failures:
        raise SystemExit(f"gp-import-complex-field failures={failures}")
    print(
        f"gp-import-complex-field failures=0 coords=2 parity_cases={parity_cases} "
        f"small_squares={','.join(str(v) for v in small)} char_gap=5 witness_product=1,1 witness_image=0,0,1,0"
    )


if __name__ == "__main__":
    main()
