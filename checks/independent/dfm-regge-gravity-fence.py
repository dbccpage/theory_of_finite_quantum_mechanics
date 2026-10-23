"""Independent check for DFM-REGGE-GRAVITY-FENCE.

Cosine-law values for lengths 3, 4, 5 and the block trace at beta = 1/2
are recomputed with fractions.Fraction. This file imports no repository code.
"""

from fractions import Fraction


def exact(value: int | Fraction) -> Fraction:
    """Admit integers and rational values; reject approximate/coercible inputs."""
    if type(value) not in (int, Fraction):
        raise TypeError("expected an integer or Fraction")
    return Fraction(value)


def cos_num(a: int | Fraction, b: int | Fraction, c: int | Fraction) -> Fraction:
    a, b, c = exact(a), exact(b), exact(c)
    return b * b + c * c - a * a


def cos_law(a: int | Fraction, b: int | Fraction, c: int | Fraction) -> Fraction:
    a, b, c = exact(a), exact(b), exact(c)
    denominator = 2 * b * c
    if denominator == 0:
        raise ValueError("cosine-law denominator must be nonzero")
    return cos_num(a, b, c) / denominator


def gamma(beta: int | Fraction) -> Fraction:
    beta = exact(beta)
    if 1 - beta * beta == 0:
        raise ValueError("gamma denominator must be nonzero")
    return (1 + beta * beta) / (1 - beta * beta)


def block_trace(beta: int | Fraction) -> Fraction:
    return gamma(beta) + gamma(beta) + 1 + 1


def main() -> None:
    from sympy import expand, symbols  # type: ignore[import-untyped]

    a_sym, b_sym, c_sym = symbols("a b c")
    residual = ((b_sym**2 + c_sym**2 - a_sym**2)
                + (a_sym**2 + c_sym**2 - b_sym**2)
                + (a_sym**2 + b_sym**2 - c_sym**2)
                - (a_sym**2 + b_sym**2 + c_sym**2))
    if expand(residual) != 0:
        raise SystemExit("symbolic numerator identity")
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
    if (n5, n3, n4) != (Fraction(0), Fraction(32), Fraction(18)):
        raise SystemExit(f"numerators {n5} {n3} {n4}")
    if n5 + n3 + n4 != 9 + 16 + 25:
        raise SystemExit("numerator total")
    c5, c3, c4 = cos_law(5, 3, 4), cos_law(3, 4, 5), cos_law(4, 3, 5)
    if (c5, c3, c4) != (Fraction(0), Fraction(4, 5), Fraction(3, 5)):
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
    print("checked: independent SymPy polynomial residual is zero")


if __name__ == "__main__":
    main()
