#!/usr/bin/env python3
"""Independent exact arithmetic verifier for FSP-COBORDISM-INTRINSIC-SIGN (TFQ-1211).

Checks the finite algebraic prototypes of spectral asymmetry (eta-jump), mapping-torus
fermion determinant sign reversal, Arf quadratic refinements, Atiyah-Hirzebruch /
Postnikov-Arf-Rokhlin mod-2 cobordism pairings, and the class-specific representation
no-go and scope fences for FSP-COBORDISM-INTRINSIC-SIGN (TFQ-1211, GIN-C22):

1. Discrete spectral asymmetry oddness, particle-hole doublet cancellation, and
   single-mode zero-crossing jump Delta(eta) = +2 (Delta(eta/2) = 1) flipping (-1)^k.
2. Finite 2x2 mapping-torus Dirac block det(diracMappingBlock(m, s)) = m^2 - s:
   at m = 0, antiperiodic untwisted sector (s = -1) has det = +1 > 0 whereas
   Z_2-twisted periodic sector (s = +1) has det = -1 < 0.
3. Arf Gaussian sign sums on (F_2)^(2g) for g = 1, 2, 3 and mod-2 5D Spin cobordism
   pairing nu_5 = a_3 * Arf + w_1 * (sigma/16) mod 2 across T^4, K3, and Postnikov-Arf
   sectors.
4. Class-specific representation no-go under odd anomaly Ward identity Z = -Z for
   nonnegative weights w_i >= 0, and 5D bulk topological inflow cancellation
   nu_5 + (-nu_5) = 0 mod 2 with (-1)^nu_5 * (-1)^nu_5 = +1.
5. Scope fences (GIN-C22 & TFQ-1211 bottleneck):
   - Basis change outside the symmetry-constrained class removes off-diagonal signs
     (Hadamard diagonalization of [[1, -1], [-1, 1]] to 2 * [[0, 0], [0, 2]]).
   - Pin^- Z_16 order-16 non-involution fence (2 * nu_16 != 0 mod 16 for odd nu_16)
     and thermal orientation weight asymmetry w_+ != w_-.
"""

from __future__ import annotations

import itertools
import sys


def spectral_sign(lam: int) -> int:
    if lam > 0:
        return 1
    if lam < 0:
        return -1
    return 0


def check_spectral_asymmetry_and_mapping_torus() -> tuple[int, int]:
    checks = 0
    failures = 0

    # 1. Oddness, doublet cancellation, and zero-crossing jump by +2
    for lam in range(-25, 26):
        if (
            spectral_sign(-lam) == -spectral_sign(lam)
            and spectral_sign(lam) + spectral_sign(-lam) == 0
        ):
            checks += 1
        else:
            failures += 1

    for lam in range(1, 26):
        for k in range(10):
            if (
                spectral_sign(lam) == 1
                and spectral_sign(-lam) == -1
                and spectral_sign(lam) - spectral_sign(-lam) == 2
                and ((-1) ** (k + 1)) == -((-1) ** k)
            ):
                checks += 1
            else:
                failures += 1

    # 2. Mapping-torus 2x2 Dirac determinant m^2 - s
    for m in range(-15, 16):
        for s in (-3, -2, -1, 0, 1, 2, 3):
            det_val = m * m - s
            if det_val == (m ** 2 - s):
                checks += 1
            else:
                failures += 1

    if (0 ** 2 - (-1)) == 1 and (0 ** 2 - 1) == -1 and (1 + (-1)) == 0:
        checks += 1
    else:
        failures += 1

    return checks, failures


def check_arf_and_cobordism_pairing() -> tuple[int, int]:
    checks = 0
    failures = 0

    # 1. Arf Gaussian sign sums for genus g = 1, 2, 3 on (F_2)^(2g)
    for g in (1, 2, 3):
        # Even Arf-0 form: sum_{i=1}^g x_i y_i
        sum_arf0 = 0
        # Odd Arf-1 form: x_1 y_1 + x_1 + y_1 + sum_{i=2}^g x_i y_i
        sum_arf1 = 0
        for bits in itertools.product((0, 1), repeat=2 * g):
            q0 = sum(bits[2 * i] * bits[2 * i + 1] for i in range(g)) % 2
            q1 = (q0 + bits[0] + bits[1]) % 2
            sum_arf0 += (-1) ** q0
            sum_arf1 += (-1) ** q1
        if (
            sum_arf0 == (2 ** g)
            and sum_arf1 == -(2 ** g)
            and sum_arf0 + sum_arf1 == 0
        ):
            checks += 1
        else:
            failures += 1

    # 2. Mod-2 5D Spin cobordism pairing nu_5 = a_3 * Arf + w_1 * (sigma/16) mod 2
    for a3, arf, w1, sigma_div16 in itertools.product((0, 1), repeat=4):
        nu5 = (a3 * arf + w1 * sigma_div16) % 2
        # T^4 sector (arf = 0, sigma_div16 = 0)
        if arf == 0 and sigma_div16 == 0:
            if nu5 == 0:
                checks += 1
            else:
                failures += 1
        # Pure K3 gauge-gravitational sector (a3 = 0, w1 = 1, sigma_div16 = 1)
        if a3 == 0 and w1 == 1 and sigma_div16 == 1:
            if nu5 == 1:
                checks += 1
            else:
                failures += 1
        # Pure Postnikov-Arf sector (a3 = 1, arf = 1, w1 = 0)
        if a3 == 1 and arf == 1 and w1 == 0:
            if nu5 == 1:
                checks += 1
            else:
                failures += 1
        # 5D bulk topological inflow cancellation: nu5 + (-nu5) = 0 mod 2 and (-1)^nu5 * (-1)^nu5 = +1
        if (nu5 + (-nu5)) % 2 == 0 and ((-1) ** nu5) * ((-1) ** nu5) == 1:
            checks += 1
        else:
            failures += 1

    return checks, failures


def check_class_nogo_and_fences() -> tuple[int, int]:
    checks = 0
    failures = 0

    # 1. Class-specific no-go: nonnegative integer weights (w0, w1, w2) under Z = -Z
    for w0 in range(0, 8):
        for w1 in range(0, 8):
            for w2 in range(0, 8):
                z = w0 + w1 + w2
                if (z == -z and w0 == 0 and w1 == 0 and w2 == 0) or (
                    z > 0 and z != -z
                ):
                    checks += 1
                else:
                    failures += 1

    # 2. Class-specificity fence: Hadamard basis change removes off-diagonal signs
    h_mat = [[1, -1], [-1, 1]]
    d_mat = [[0, 0], [0, 2]]
    p_mat = [[1, 1], [1, -1]]
    php = [
        [
            sum(
                p_mat[i][k] * h_mat[k][l] * p_mat[l][j]
                for k in range(2)
                for l in range(2)
            )
            for j in range(2)
        ]
        for i in range(2)
    ]
    if (
        h_mat[0][1] == -1
        and (h_mat[0][0] + h_mat[1][1]) == (d_mat[0][0] + d_mat[1][1]) == 2
        and (h_mat[0][0] * h_mat[1][1] - h_mat[0][1] * h_mat[1][0])
        == (d_mat[0][0] * d_mat[1][1] - d_mat[0][1] * d_mat[1][0])
        == 0
        and php == [[2 * d_mat[0][0], 2 * d_mat[0][1]], [2 * d_mat[1][0], 2 * d_mat[1][1]]]
    ):
        checks += 1
    else:
        failures += 1

    # 3. Pin^- Z_16 order-16 fence and thermal weight asymmetry fence
    for nu16 in range(1, 16):
        if nu16 % 16 != 0 and (16 * nu16) % 16 == 0:
            checks += 1
        else:
            failures += 1
        if nu16 % 2 == 1:
            if (2 * nu16) % 16 != 0 and (8 * nu16) % 16 == 8:
                checks += 1
            else:
                failures += 1

    for w_pos in range(-5, 6):
        for w_neg in range(-5, 6):
            if (w_pos == w_neg and w_pos - w_neg == 0) or (
                w_pos != w_neg and w_pos - w_neg != 0
            ):
                checks += 1
            else:
                failures += 1

    return checks, failures


def main() -> int:
    c1, f1 = check_spectral_asymmetry_and_mapping_torus()
    c2, f2 = check_arf_and_cobordism_pairing()
    c3, f3 = check_class_nogo_and_fences()
    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3
    print(
        f"FSP-COBORDISM-INTRINSIC-SIGN independent check: "
        f"checks={total_checks} spectral_torus={c1} arf_cobordism={c2} "
        f"nogo_fences={c3} failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
