#!/usr/bin/env python3
"""Independent check for FQ-PRIM-TO-QM-SELECTION-OPEN.

AuthorityEffect: None.

Recomputes one two-amplitude witness with Fraction. No repository imports.
"""

from fractions import Fraction


def main() -> None:
    amp0 = 1
    amp1 = 2
    quad0 = amp0 * amp0
    quad1 = amp1 * amp1
    quad_den = quad0 + quad1
    quart0 = quad0 * quad0
    quart1 = quad1 * quad1
    quart_den = quart0 + quart1
    if (quad0, quad1, quad_den) != (1, 4, 5):
        raise SystemExit("quadratic numerators")
    if (quart0, quart1, quart_den) != (1, 16, 17):
        raise SystemExit("quartic numerators")
    if not (quad0 > 0 and quad1 > 0 and quart0 > 0 and quart1 > 0):
        raise SystemExit("positivity")
    if quad0 + quad1 != quad_den or quart0 + quart1 != quart_den:
        raise SystemExit("normalization sums")
    n_quad = Fraction(quad0, quad_den)
    n_quart = Fraction(quart0, quart_den)
    if n_quad != Fraction(1, 5) or Fraction(quad1, quad_den) != Fraction(4, 5):
        raise SystemExit("quadratic weights 1/5 and 4/5")
    if n_quart != Fraction(1, 17) or Fraction(quart1, quart_den) != Fraction(16, 17):
        raise SystemExit("quartic weights 1/17 and 16/17")
    if n_quad == n_quart or quad0 * quart_den == quart0 * quad_den:
        raise SystemExit("weights should differ")
    if quad0 * quart_den != 17 or quart0 * quad_den != 5:
        raise SystemExit("cross products 17 and 5")
    s0 = 1 * 1
    s1 = 1 * 1
    t0 = s0 * s0
    t1 = s1 * s1
    if (s0, s1, s0 + s1, t0, t1, t0 + t1) != (1, 1, 2, 1, 1, 2):
        raise SystemExit("symmetric numerators")
    if Fraction(s0, s0 + s1) != Fraction(1, 2):
        raise SystemExit("symmetric weight 1/2")
    if Fraction(t0, t0 + t1) != Fraction(1, 2):
        raise SystemExit("symmetric quartic weight 1/2")
    print("checked amplitudes 1 and 2")
    print("quadratic weights 1/5 and 4/5")
    print("quartic weights 1/17 and 16/17")
    print("cross products 17 and 5")
    print("symmetric amplitudes 1 and 1 give weight 1/2")
    print("failures=0")


if __name__ == "__main__":
    main()
