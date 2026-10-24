"""Independent check for LQG-EPRL-VERTEX-IMPORT.

Recomputes the rational Euclidean and Lorentzian label identities with
fractions.Fraction. This file imports no repository code. It does not
evaluate a 15j symbol, a booster, or a limit.
"""

from fractions import Fraction


def j_plus(gamma, k):
    return abs(1 + gamma) * k / 2


def j_minus(gamma, k):
    return abs(1 - gamma) * k / 2


def main():
    samples = (
        Fraction(1, 2),
        Fraction(1, 3),
        Fraction(2, 3),
        Fraction(3, 2),
        Fraction(3, 1),
        Fraction(5, 2),
    )
    spins = (Fraction(1, 2), Fraction(1), Fraction(2), Fraction(4))
    for gamma in samples:
        for k in spins:
            plus = j_plus(gamma, k)
            minus = j_minus(gamma, k)
            if gamma < 1:
                if plus != (1 + gamma) * k / 2 or minus != (1 - gamma) * k / 2:
                    raise SystemExit(f"below shape {gamma} {k}")
                if plus + minus != k or plus - minus != gamma * k:
                    raise SystemExit(f"below recovery {gamma} {k}")
            elif gamma > 1:
                if plus != (1 + gamma) * k / 2 or minus != (gamma - 1) * k / 2:
                    raise SystemExit(f"above shape {gamma} {k}")
                if plus - minus != k or plus + minus != gamma * k:
                    raise SystemExit(f"above recovery {gamma} {k}")
            n_label = 2 * k
            rho = 2 * gamma * k
            if n_label / 2 != k or rho != gamma * n_label or rho != 2 * gamma * (n_label / 2):
                raise SystemExit(f"lorentz {gamma} {k}")

    half_plus = j_plus(Fraction(1, 2), 2)
    half_minus = j_minus(Fraction(1, 2), 2)
    if (half_plus, half_minus) != (Fraction(3, 2), Fraction(1, 2)):
        raise SystemExit(f"half {half_plus} {half_minus}")
    if half_plus + half_minus != 2 or half_plus - half_minus != 1:
        raise SystemExit("half recovery")
    if half_plus - half_minus == 2:
        raise SystemExit("half difference should not be k")

    three_plus = j_plus(Fraction(3), 2)
    three_minus = j_minus(Fraction(3), 2)
    if (three_plus, three_minus) != (Fraction(4), Fraction(2)):
        raise SystemExit(f"three {three_plus} {three_minus}")
    if three_plus - three_minus != 2 or three_plus + three_minus != 6:
        raise SystemExit("three recovery")
    if three_plus + three_minus == 2:
        raise SystemExit("three sum should not be k")

    one_plus = j_plus(Fraction(1), 2)
    one_minus = j_minus(Fraction(1), 2)
    if (one_plus, one_minus) != (Fraction(2), Fraction(0)):
        raise SystemExit(f"one {one_plus} {one_minus}")
    if one_plus + one_minus != 2 or one_plus - one_minus != 2:
        raise SystemExit("boundary gamma")

    n_label = 2 * 2
    rho = 2 * Fraction(1, 2) * 2
    j_index = n_label / 2
    gamma_j = Fraction(1, 2) * j_index
    if (n_label, rho, j_index, gamma_j) != (4, 2, 2, 1):
        raise SystemExit(f"lorentz point {(n_label, rho, j_index, gamma_j)}")
    if rho != 2 * gamma_j:
        raise SystemExit("rho versus gamma j")

    pairs = 5 * (5 - 1) // 2
    if pairs != 10:
        raise SystemExit(f"pairs {pairs}")

    print("euclidean gamma=1/2 k=2: j+ = 3/2, j- = 1/2, sum = 2, difference = 1")
    print("euclidean gamma=3 k=2: j+ = 4, j- = 2, difference = 2, sum = 6")
    print("euclidean gamma=1 k=2: j+ = 2, j- = 0, sum = 2, difference = 2")
    print("lorentzian gamma=1/2 k=2: (n, rho) = (4, 2), j = 2, gamma j = 1")
    print("unordered pairs among 5 indices: 10")
    print("checked: below and above recoveries, boundary point, lorentzian labels, pair count")


if __name__ == "__main__":
    main()
