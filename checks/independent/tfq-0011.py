"""Independent check for the narrowed TFQ-0011 finite QCD certificate.

Recomputes the rational identities in lean4/CampaignTfq0011FiniteQcd.lean
with the fractions module. Imports nothing from this repository.
"""

from __future__ import annotations

from fractions import Fraction


def cF(nc: Fraction) -> Fraction:
    return (nc * nc - 1) / (2 * nc)


def cA(nc: Fraction) -> Fraction:
    return nc


def singlet(nc: Fraction) -> Fraction:
    return -cF(nc)


def octet(nc: Fraction) -> Fraction:
    return cA(nc) / 2 - cF(nc)


def sextet(nc: Fraction) -> Fraction:
    return Fraction(1, 2) - 1 / (2 * nc)


def antitriplet(nc: Fraction) -> Fraction:
    return -Fraction(1, 2) - 1 / (2 * nc)


def beta0(nc: int, nf: int) -> Fraction:
    return Fraction(11 * nc, 3) - Fraction(2 * nf, 3)


def beta1(nc: int, nf: int) -> Fraction:
    c_a = Fraction(nc, 1)
    c_f = Fraction(nc * nc - 1, 2 * nc)
    t_f = Fraction(1, 2)
    return Fraction(34, 3) * c_a * c_a - (Fraction(20, 3) * c_a + 4 * c_f) * t_f * nf


def beta1_reduced(nc: int, nf: int) -> Fraction:
    return Fraction(34, 3) * (nc * nc) - (Fraction(10, 3) * nc + Fraction(nc * nc - 1, nc)) * nf


def creutz(w_rt: Fraction, w_prev: Fraction, w_rt1: Fraction, w_r1t: Fraction) -> Fraction:
    return (w_rt * w_prev) / (w_rt1 * w_r1t)


def area(b: Fraction, r: int, t: int) -> Fraction:
    return b ** (r * t)


def perim(b: Fraction, r: int, t: int) -> Fraction:
    return b ** (2 * (r + t))


def main() -> None:
    checks = 0

    def expect(name: str, got: object, want: object) -> None:
        nonlocal checks
        checks += 1
        if got != want:
            raise SystemExit(f"FAIL {name}: got {got}, want {want}")

    nc = Fraction(3, 1)
    expect("cF", cF(nc), Fraction(4, 3))
    expect("cA", cA(nc), Fraction(3, 1))
    expect("singlet", singlet(nc), Fraction(-4, 3))
    expect("octet", octet(nc), Fraction(1, 6))
    expect("sextet", sextet(nc), Fraction(1, 3))
    expect("antitriplet", antitriplet(nc), Fraction(-2, 3))
    expect("singlet_neg", singlet(nc) < 0, True)
    expect("octet_pos", octet(nc) > 0, True)

    expect("gluon_split", 4 * cA(nc) + Fraction(-1, 3) * cA(nc), Fraction(11, 1))
    expect("one_flavor", Fraction(-4, 3) * Fraction(1, 2), Fraction(-2, 3))
    expect("abelian_coeff_neg", Fraction(-4, 3) < 0, True)

    for nf, want in (
        (0, Fraction(11, 1)),
        (3, Fraction(9, 1)),
        (5, Fraction(23, 3)),
        (6, Fraction(7, 1)),
        (16, Fraction(1, 3)),
        (17, Fraction(-1, 3)),
    ):
        expect(f"beta0_{nf}", beta0(3, nf), want)

    for nf in range(0, 17):
        expect(f"beta0_pos_{nf}", beta0(3, nf) > 0, True)
        expect(f"window_{nf}", Fraction(nf, 1) < Fraction(33, 2), True)
    expect("beta0_17_neg", beta0(3, 17) < 0, True)
    expect("window_edge", not (Fraction(33, 2) < Fraction(33, 2)), True)
    expect("beta0_at_33_2", beta0(3, 0) * 0 + (Fraction(11, 1) - Fraction(2, 3) * Fraction(33, 2)), Fraction(0, 1))

    for nf in (0, 5, 16, 17, 4):
        expect(f"beta1_forms_{nf}", beta1(3, nf), beta1_reduced(3, nf))

    expect("beta1_0", beta1(3, 0), Fraction(102, 1))
    expect("beta1_5", beta1(3, 5), Fraction(116, 3))
    expect("beta1_16", beta1(3, 16), Fraction(-302, 3))
    expect("beta1_reduced_form", beta1_reduced(3, 16), Fraction(102, 1) - Fraction(38, 3) * 16)
    expect("banks_zaks", (-beta0(3, 16)) / beta1(3, 16), Fraction(1, 302))

    b = Fraction(1, 9)
    for r, t in ((2, 2), (3, 3), (2, 3), (4, 5)):
        expect(
            f"area_{r}_{t}",
            creutz(area(b, r, t), area(b, r - 1, t - 1), area(b, r, t - 1), area(b, r - 1, t)),
            b,
        )
        expect(
            f"perim_{r}_{t}",
            creutz(perim(b, r, t), perim(b, r - 1, t - 1), perim(b, r, t - 1), perim(b, r - 1, t)),
            Fraction(1, 1),
        )
        exp_area = r * t + (r - 1) * (t - 1)
        exp_den = r * (t - 1) + (r - 1) * t
        expect(f"area_exp_{r}_{t}", exp_area, exp_den + 1)
        exp_p = 2 * (r + t) + 2 * ((r - 1) + (t - 1))
        exp_pd = 2 * (r + (t - 1)) + 2 * ((r - 1) + t)
        expect(f"perim_exp_{r}_{t}", exp_p, exp_pd)

    expect("area_ne_perim", Fraction(1, 9) != 1, True)
    expect("tree", 9 - 1, 8)
    expect("cycle", 12 - 9 + 1, 4)
    expect("residual_edges", 12 - 8, 4)

    # S3 on {0,1,2}: swaps (0 1) and (1 2) do not commute, and their product is not id.
    def swap01(x: int) -> int:
        return {0: 1, 1: 0, 2: 2}[x]

    def swap12(x: int) -> int:
        return {0: 0, 1: 2, 2: 1}[x]

    def comp(f, g, x: int) -> int:
        return f(g(x))

    left = [comp(swap12, swap01, i) for i in range(3)]
    right = [comp(swap01, swap12, i) for i in range(3)]
    expect("s3_noncommute", left != right, True)
    expect("s3_product_ne_id", left != [0, 1, 2], True)

    print(f"tfq-0011 independent check: {checks} checks, 0 failures")


if __name__ == "__main__":
    main()
