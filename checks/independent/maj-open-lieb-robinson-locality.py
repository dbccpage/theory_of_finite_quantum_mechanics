"""Independent verification check for MAJ-OPEN-LIEB-ROBINSON-LOCALITY (TFQ-1149).

Verifies:
1. One-sided Lieb-Robinson causal radius r0 + vLR * t additivity and monotonicity.
2. Two-sided 1D support weight w0 + 2 * vLR * t additivity and strict growth for vLR > 0.
3. Propagated error-pair difference weight bound wDiff <= 2 * w0 + 4 * vLR * t.
4. Syndrome recovery viability within the Lieb-Robinson horizon:
   2 * lrSupportWeight1D(w0, vLR, t) < d => wDiff < d (no non-stabilizer logical cycle collision).
5. Critical repair horizon monotonicity in tLo < tHi and margin 4 * vLR * (tHi - tLo).
6. Horizon overflow logical collision: d <= 2 * lrSupportWeight1D(w0, vLR, t) =>
   a weight-d logical cycle splits into w1 = d // 2 and w2 = d - d // 2 inside the ball.
7. Discrete Lieb-Robinson commutator tail decay c0 * g^t < c0 * mu^dist outside the causal cone (t < dist).
8. Classical syndrome-routing communication delay constraint 2 * w0 * vCl + 4 * vLR * L < d * vCl.
9. Torus tetron viability window comparisons (L=4 vs L=7) and open-scope fences.
"""

from __future__ import annotations

import sys


def lr_causal_radius(r0: int, v_lr: int, t: int) -> int:
    return r0 + v_lr * t


def lr_support_weight_1d(w0: int, v_lr: int, t: int) -> int:
    return w0 + 2 * v_lr * t


def lr_tail_num(c0: int, g: int, t: int) -> int:
    return c0 * (g**t)


def lr_space_denom(mu: int, dist: int) -> int:
    return mu**dist


def main() -> int:
    failures = 0
    cone_checks = 0
    viability_checks = 0
    tail_checks = 0
    scope_checks = 0

    # 1. Causal radius & 1D support diameter additivity and strict growth
    for r0 in range(0, 6):
        for v_lr in range(0, 5):
            for t1 in range(0, 5):
                for t2 in range(0, 5):
                    lhs_r = lr_causal_radius(lr_causal_radius(r0, v_lr, t1), v_lr, t2)
                    rhs_r = lr_causal_radius(r0, v_lr, t1 + t2)
                    if lhs_r != rhs_r or lr_causal_radius(r0, v_lr, t1) < r0:
                        failures += 1
                    cone_checks += 1

                    lhs_w = lr_support_weight_1d(
                        lr_support_weight_1d(r0, v_lr, t1), v_lr, t2
                    )
                    rhs_w = lr_support_weight_1d(r0, v_lr, t1 + t2)
                    if lhs_w != rhs_w:
                        failures += 1
                    cone_checks += 1

                    if v_lr > 0:
                        if not (
                            lr_support_weight_1d(r0, v_lr, t1)
                            < lr_support_weight_1d(r0, v_lr, t1 + 1)
                        ):
                            failures += 1
                        cone_checks += 1

    # 2. Propagated pair difference weight, viability horizon, monotonicity, and collision split
    for w0 in range(1, 5):
        for v_lr in range(1, 4):
            for t in range(0, 5):
                wt_ball = lr_support_weight_1d(w0, v_lr, t)
                if 2 * wt_ball != 2 * w0 + 4 * v_lr * t:
                    failures += 1
                viability_checks += 1

                for d in range(2, 28):
                    if 2 * wt_ball < d:
                        # Viable: no pair w1, w2 <= wt_ball can sum to >= d
                        for w1 in (0, wt_ball // 2, wt_ball):
                            for w2 in (0, wt_ball // 2, wt_ball):
                                w_diff = w1 + w2
                                if not (w_diff < d):
                                    failures += 1
                                viability_checks += 1
                    else:
                        # Overflow: d <= 2 * wt_ball => logical of weight d splits into w1, w2 <= wt_ball
                        w1 = d // 2
                        w2 = d - d // 2
                        if w1 + w2 != d or w1 > wt_ball or w2 > wt_ball:
                            failures += 1
                        viability_checks += 1

                # Monotonicity across t_lo < t_hi
                for t_hi in range(t + 1, 6):
                    wt_hi = lr_support_weight_1d(w0, v_lr, t_hi)
                    if 2 * wt_hi - 2 * wt_ball != 4 * v_lr * (t_hi - t):
                        failures += 1
                    viability_checks += 1

    # 3. Discrete Lieb-Robinson commutator tail suppression outside the light cone
    for c0 in range(1, 4):
        for g in range(2, 5):
            for mu in range(g, 6):
                for t in range(0, 5):
                    for dist in range(t + 1, 6):
                        if not (
                            lr_tail_num(c0, g, t) < c0 * lr_space_denom(mu, dist)
                        ):
                            failures += 1
                        tail_checks += 1

    # 4. Classical syndrome-routing communication delay & torus window witnesses
    for w0 in range(1, 4):
        for v_lr in range(1, 4):
            for v_cl in range(1, 5):
                for t_comm in range(1, 5):
                    for length in range(1, v_cl * t_comm + 1):
                        wt_comm = lr_support_weight_1d(w0, v_lr, t_comm)
                        lhs = 2 * w0 * v_cl + 4 * v_lr * length
                        rhs = 2 * wt_comm * v_cl
                        if lhs > rhs:
                            failures += 1
                        scope_checks += 1
                        for d in (2 * wt_comm + 1, 2 * wt_comm + 3):
                            if not (lhs < d * v_cl):
                                failures += 1
                            scope_checks += 1

    # Torus L=4 (d=4) vs L=7 (d=7) witness
    if not (
        2 * lr_support_weight_1d(1, 1, 1) == 6
        and 4 < 2 * lr_support_weight_1d(1, 1, 1) < 7
        and 7 < 2 * lr_support_weight_1d(1, 1, 2) == 10
        and 2 * lr_support_weight_1d(1, 1, 2) - 2 * lr_support_weight_1d(1, 1, 1) == 4
    ):
        failures += 1
    scope_checks += 4

    total = cone_checks + viability_checks + tail_checks + scope_checks
    if failures > 0:
        print(
            f"FAIL: checks={total} cone={cone_checks} viability={viability_checks} "
            f"tail={tail_checks} scope_fences={scope_checks} failures={failures}"
        )
        return 1

    print(
        f"PASS: checks={total} cone={cone_checks} viability={viability_checks} "
        f"tail={tail_checks} scope_fences={scope_checks} failures=0"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
