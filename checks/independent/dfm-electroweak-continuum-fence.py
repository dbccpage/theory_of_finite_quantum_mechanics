"""Independent check for DFM-ELECTROWEAK-CONTINUUM-FENCE.

Gaussian rationals and the algebraic dressing are recomputed with
fractions.Fraction. This file imports no repository code.
"""

from fractions import Fraction


class GR:
    def __init__(self, re, im=0):
        self.re = Fraction(re)
        self.im = Fraction(im)

    def conj(self):
        return GR(self.re, -self.im)

    def mul(self, other):
        return GR(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def norm2(self):
        return self.re * self.re + self.im * self.im

    def neg_conj(self):
        return GR(-self.re, self.im)

    def div(self, s):
        s = Fraction(s)
        return GR(self.re / s, self.im / s)

    def __eq__(self, other):
        return self.re == other.re and self.im == other.im

    def __repr__(self):
        return f"{self.re}+{self.im}i"


def v2(p, q):
    return p.norm2() + q.norm2()


def U(p, q):
    return (q.conj(), p, p.neg_conj(), q)


def scale(z, p, q):
    return (z.mul(p), z.mul(q))


def right_diag(entries, c0, c1):
    e00, e01, e10, e11 = entries
    return (e00.mul(c0), e01.mul(c1), e10.mul(c0), e11.mul(c1))


def scale_mat(entries, s):
    return tuple(entry.div(s) for entry in entries)


def check_unnormalized(z, p, q):
    left = U(*scale(z, p, q))
    right = right_diag(U(p, q), z.conj(), z)
    if left != right:
        raise SystemExit(f"unnormalized mismatch {left} vs {right}")
    if v2(*scale(z, p, q)) != z.norm2() * v2(p, q):
        raise SystemExit("squared-norm multiplicativity failed")


def main():
    z_sample = GR(Fraction(1, 2), Fraction(1, 3))
    p_sample = GR(Fraction(2, 7), Fraction(1, 5))
    q_sample = GR(Fraction(3, 11), 4)
    check_unnormalized(z_sample, p_sample, q_sample)
    print("unnormalized sample z=1/2+1/3i entries match")

    z_unit = GR(Fraction(3, 5), Fraction(4, 5))
    phi_p, phi_q = GR(1, 0), GR(0, 0)
    if z_unit.norm2() != 1:
        raise SystemExit(f"unit norm {z_unit.norm2()}")
    if v2(phi_p, phi_q) != 1:
        raise SystemExit("axis squared norm")
    s = 1
    if s * s != v2(phi_p, phi_q):
        raise SystemExit("s root")
    scaled = scale(z_unit, phi_p, phi_q)
    if s * s != v2(*scaled):
        raise SystemExit("shared root")
    left = scale_mat(U(*scaled), s)
    right = right_diag(scale_mat(U(phi_p, phi_q), s), z_unit.conj(), z_unit)
    if left != right:
        raise SystemExit(f"unit normalized mismatch {left} vs {right}")
    if left[1] != z_unit:
        raise SystemExit(f"entry01 {left[1]}")
    print("unit z=3/5+4/5i norm2=1 entry01=3/5+4/5i")

    z_two = GR(2, 0)
    if z_two.norm2() != 4:
        raise SystemExit("z=2 norm")
    scaled_two = scale(z_two, phi_p, phi_q)
    if v2(*scaled_two) != 4:
        raise SystemExit("scaled squared norm")
    if 2 * 2 != v2(*scaled_two) or 1 * 1 != v2(phi_p, phi_q):
        raise SystemExit("own roots")
    own_left = scale_mat(U(*scaled_two), 2)[1]
    own_right = right_diag(scale_mat(U(phi_p, phi_q), 1), z_two.conj(), z_two)[1]
    if own_left != GR(1, 0) or own_right != GR(2, 0):
        raise SystemExit(f"own-root entries {own_left} {own_right}")
    if own_left == own_right:
        raise SystemExit("own-root entries should differ")
    shared_left = scale_mat(U(*scaled_two), 1)
    shared_right = right_diag(scale_mat(U(phi_p, phi_q), 1), z_two.conj(), z_two)
    if shared_left != shared_right:
        raise SystemExit("shared denominator on z=2 failed")
    print("nonunit z=2 own-root entries 1 and 2 differ")
    print("shared denominator on z=2 still matches")
    print("checked: unnormalized sample, unit witness, own-root split")


if __name__ == "__main__":
    main()
