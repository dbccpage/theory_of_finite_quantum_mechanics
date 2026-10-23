"""Independent check for DFM-REGGE-GRAVITY-FENCE.

Cosine-law values for lengths 3, 4, 5 and the block trace at beta = 1/2
are recomputed with fractions.Fraction. This file imports no repository code.
"""

from fractions import Fraction


def cos_num(a, b, c):
    a, b, c = Fraction(a), Fraction(b), Fraction(c)
    return b * b + c * c - a * a


def cos_law(a, b, c):
    return cos_num(a, b, c) / (2 * b * c)


def gamma(beta):
    return (1 + beta * beta) / (1 - beta * beta)


def block_trace(beta):
    return gamma(beta) + gamma(beta) + 1 + 1


def main():
    samples = [
        (Fraction(3), Fraction(4), Fraction(5)),
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(-2), Fraction(7), Fraction(1, 3)),
        (Fraction(1, 2), Fraction(-3, 5), Fraction(8)),
    ]
    for a, b, c in samples:
        got = cos_num(a, b, c) + cos_num(b, a, c) + cos_num(c, a, b)
        if got != a * a + b * b + c * c:
            raise SystemExit(f"numerator sum {a} {b} {c}")
    n5, n3, n4 = cos_num(5, 3, 4), cos_num(3, 4, 5), cos_num(4, 3, 5)
    if (n5, n3, n4) != (0, 32, 18):
        raise SystemExit(f"numerators {n5} {n3} {n4}")
    if n5 + n3 + n4 != 9 + 16 + 25:
        raise SystemExit("numerator total")
    c5, c3, c4 = cos_law(5, 3, 4), cos_law(3, 4, 5), cos_law(4, 3, 5)
    if (c5, c3, c4) != (0, Fraction(4, 5), Fraction(3, 5)):
        raise SystemExit(f"cosines {c5} {c3} {c4}")
    cosine_sum = c5 + c3 + c4
    if cosine_sum != Fraction(7, 5):
        raise SystemExit(f"cosine sum {cosine_sum}")
    beta = Fraction(1, 2)
    if 1 - beta * beta == 0:
        raise SystemExit("denominator")
    if gamma(beta) != Fraction(5, 3):
        raise SystemExit("gamma")
    off = (2 * beta) / (1 - beta * beta)
    if off != Fraction(4, 3):
        raise SystemExit(f"off {off}")
    trace = block_trace(beta)
    if trace != Fraction(16, 3):
        raise SystemExit(f"trace {trace}")
    if trace == 4 or trace == cosine_sum:
        raise SystemExit("trace should differ")
    print("numerators 0, 32, 18; sum 50; cosines 0, 4/5, 3/5; cosine sum 7/5")
    print("gamma(1/2) = 5/3; off-diagonal 4/3; block trace 16/3")
    print("16/3 differs from 4 and from 7/5")
    print("checked: numerator sum on four triples, cosine law, block trace")


if __name__ == "__main__":
    main()
