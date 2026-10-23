"""Exact rational and F_2 witness for WDP-21-16-WDP (`derivation.md`).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def _trace_product(a: list[list[Fraction]], b: list[list[Fraction]]) -> Fraction:
    return sum(
        (a[i][k] * b[k][i] for i in range(4) for k in range(4)),
        Fraction(0),
    )


def _marginal_a(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [mat[0][0] + mat[1][1], mat[0][2] + mat[1][3]],
        [mat[2][0] + mat[3][1], mat[2][2] + mat[3][3]],
    ]


def _marginal_b(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [mat[0][0] + mat[2][2], mat[0][1] + mat[2][3]],
        [mat[1][0] + mat[3][2], mat[1][1] + mat[3][3]],
    ]


def witness() -> dict[str, Any]:
    zero = Fraction(0)
    half = Fraction(1, 2)
    neg_half = Fraction(-1, 2)
    one = Fraction(1)
    neg_one = Fraction(-1)
    beta = Fraction(1, 8)

    rho = [
        [half, zero, zero, half],
        [zero, zero, zero, zero],
        [zero, zero, zero, zero],
        [half, zero, zero, half],
    ]
    sigma = [
        [half, zero, zero, neg_half],
        [zero, zero, zero, zero],
        [zero, zero, zero, zero],
        [neg_half, zero, zero, half],
    ]
    r_mat = [[rho[i][j] - sigma[i][j] for j in range(4)] for i in range(4)]

    o_r = [
        [one, zero, zero, zero],
        [zero, one, zero, zero],
        [zero, zero, neg_one, zero],
        [zero, zero, zero, neg_one],
    ]
    zz = [
        [one, zero, zero, zero],
        [zero, neg_one, zero, zero],
        [zero, zero, neg_one, zero],
        [zero, zero, zero, one],
    ]
    o_mat = [row[:] for row in o_r]
    for i, j in ((0, 3), (3, 0), (1, 2), (2, 1)):
        o_mat[i][j] += beta

    half_id_2 = [[half, zero], [zero, half]]
    marginals_equal_half_id = (
        _marginal_a(rho) == half_id_2
        and _marginal_b(rho) == half_id_2
        and _marginal_a(sigma) == half_id_2
        and _marginal_b(sigma) == half_id_2
    )

    # Product residuals rho - I/4 and sigma - I/4 at |01> have expectation -1/4 < 0
    prod_res_01_expectation = rho[1][1] - Fraction(1, 4)

    supp_xx = (1, 1, 0, 0)
    supp_yy = (1, 1, 1, 1)
    f2_support_sum = tuple(a ^ b for a, b in zip(supp_xx, supp_yy))

    kernel_q = tuple(
        (x, y, z)
        for x in (0, 1)
        for y in (0, 1)
        for z in (0, 1)
        if (x ^ y) == 0
    )
    repair_b = ((0, 0, 0), (1, 1, 0))
    unrepaired = tuple(v for v in kernel_q if v not in repair_b)

    return {
        "marginals_equal_half_id": marginals_equal_half_id,
        "prod_residual_01_expectation": prod_res_01_expectation,
        "r_03": r_mat[0][3],
        "r_30": r_mat[3][0],
        "trace_r": sum((r_mat[i][i] for i in range(4)), Fraction(0)),
        "trace_r_or": _trace_product(r_mat, o_r),
        "trace_r_zz": _trace_product(r_mat, zz),
        "trace_rho_or": _trace_product(rho, o_r),
        "trace_sigma_or": _trace_product(sigma, o_r),
        "trace_rho_o": _trace_product(rho, o_mat),
        "trace_sigma_o": _trace_product(sigma, o_mat),
        "trace_r_o": _trace_product(r_mat, o_mat),
        "beta": beta,
        "r_schatten_1_norm": Fraction(2),
        "l4_alpha_lower_bound": Fraction(1, 8),
        "f2_support_sum_xx_yy": f2_support_sum,
        "packet_s_kernel": kernel_q,
        "packet_s_repair": repair_b,
        "packet_s_unrepaired": unrepaired,
        "packet_s_quotient_dim": 1,
        "authority_effect": "None",
    }


def reject_packet_conjunction_or_lr_adapter(claim: str) -> None:
    if (
        "R_{0,3} == dim(ker Q / B)" in claim
        or "Lieb-Robinson" in claim
        or "T >= r/v" in claim
    ):
        raise ValueError(
            "Packet L and Packet S have no cross-carrier adapter or Lieb-Robinson triple in WDP-21-16-WDP"
        )


if __name__ == "__main__":
    print(witness())
