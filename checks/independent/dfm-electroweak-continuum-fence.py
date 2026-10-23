"""Independent check for DFM-ELECTROWEAK-CONTINUUM-FENCE.

Gaussian rationals and the algebraic dressing are recomputed with
fractions.Fraction. This file imports no repository code.
"""

from __future__ import annotations
from fractions import Fraction
from collections.abc import Callable


def exact(value: object) -> Fraction:
    if type(value) is int or type(value) is Fraction:
        return Fraction(value)
    raise TypeError("expected an integer or Fraction")


class GR:
    def __init__(self, re: int | Fraction, im: int | Fraction = 0) -> None:
        self.re = exact(re)
        self.im = exact(im)

    def conj(self) -> GR:
        return GR(self.re, -self.im)

    def mul(self, other: GR) -> GR:
        return GR(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def norm2(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def neg_conj(self) -> GR:
        return GR(-self.re, self.im)

    def div(self, s: int | Fraction) -> GR:
        s = exact(s)
        if not s:
            raise ValueError("normalization denominator must be nonzero")
        return GR(self.re / s, self.im / s)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GR) and self.re == other.re and self.im == other.im

    def __repr__(self) -> str:
        return f"{self.re}+{self.im}i"


def v2(p: GR, q: GR) -> Fraction:
    return p.norm2() + q.norm2()


def U(p: GR, q: GR) -> tuple[GR, GR, GR, GR]:
    return (q.conj(), p, p.neg_conj(), q)


def scale(z: GR, p: GR, q: GR) -> tuple[GR, GR]:
    return (z.mul(p), z.mul(q))


def right_diag(entries: tuple[GR, GR, GR, GR], c0: GR, c1: GR) -> tuple[GR, GR, GR, GR]:
    e00, e01, e10, e11 = entries
    return (e00.mul(c0), e01.mul(c1), e10.mul(c0), e11.mul(c1))


def scale_mat(entries: tuple[GR, GR, GR, GR], s: int | Fraction) -> tuple[GR, GR, GR, GR]:
    a, b, c, d = entries
    return a.div(s), b.div(s), c.div(s), d.div(s)


def check_unnormalized(z: GR, p: GR, q: GR) -> None:
    left = U(*scale(z, p, q))
    right = right_diag(U(p, q), z.conj(), z)
    if left != right:
        raise SystemExit(f"unnormalized mismatch {left} vs {right}")
    if v2(*scale(z, p, q)) != z.norm2() * v2(p, q):
        raise SystemExit("squared-norm multiplicativity failed")


class NormalizationError(ValueError):
    pass


def checked_normalize(p: GR, q: GR, root: object) -> tuple[GR, GR]:
    s = exact(root)
    if v2(p, q) == 0:
        raise NormalizationError("zeroNorm")
    if s <= 0:
        raise NormalizationError("nonpositiveScale")
    if s * s != v2(p, q):
        raise NormalizationError("mismatchedSquare")
    return p.div(s), q.div(s)


def unit_action(z: GR, phi: tuple[GR, GR]) -> tuple[GR, GR]:
    if z.norm2() != 1 or v2(*phi) != 1:
        raise NormalizationError("unit input required")
    return scale(z, *phi)


def check_action_case(phi: tuple[GR, GR], root: Fraction, phases: list[GR]) -> int:
    norm = checked_normalize(*phi, root)
    if v2(*norm) != 1:
        raise SystemExit("normalization has nonunit norm")
    if checked_normalize(*norm, Fraction(1)) != norm:
        raise SystemExit("normalization is not fixed on unit input")
    for z in phases:
        transformed = checked_normalize(*scale(z, *phi), root)
        if transformed != unit_action(z, norm):
            raise SystemExit("normalization covariance")
        if scale_mat(U(*scale(z, *phi)), root) != right_diag(scale_mat(U(*phi), root), z.conj(), z):
            raise SystemExit("typed matrix covariance")
        for w in phases:
            if unit_action(z, unit_action(w, norm)) != unit_action(z.mul(w), norm):
                raise SystemExit("unit action composition")
    return len(phases) ** 2


def check_normalization_api() -> None:
    ts = [Fraction(-2),Fraction(-1),Fraction(-1,2),Fraction(0),Fraction(1,2),Fraction(1),Fraction(2)]
    phases = [GR((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in ts] + [GR(-1)]
    base = [(GR(1), GR(0), Fraction(1)), (GR(3), GR(4), Fraction(5)), (GR(1,1), GR(1,1), Fraction(2))]
    count = 0
    for p, q, root in base:
        for factor in (Fraction(1), Fraction(2), Fraction(1,3)):
            phi = scale(GR(factor), p, q)
            count += check_action_case(phi, factor * root, phases)
    print(f"normalization API: 9 doublets, {len(phases)} phases, 72 covariance and {count} composition cases")
    cases: list[tuple[Callable[[], object], type[Exception], str]] = [
        (lambda: checked_normalize(GR(0),GR(0),1), NormalizationError, "zeroNorm"),
        (lambda: checked_normalize(GR(1),GR(0),0), NormalizationError, "nonpositiveScale"),
        (lambda: checked_normalize(GR(1),GR(0),-1), NormalizationError, "nonpositiveScale"),
        (lambda: checked_normalize(GR(1),GR(0),2), NormalizationError, "mismatchedSquare"),
        (lambda: checked_normalize(GR(1),GR(1),1), NormalizationError, "mismatchedSquare"),
        (lambda: checked_normalize(GR(1),GR(0),True), TypeError, "expected an integer or Fraction"),
        (lambda: checked_normalize(GR(1),GR(0),1.0), TypeError, "expected an integer or Fraction"),
        (lambda: checked_normalize(GR(1),GR(0),"1"), TypeError, "expected an integer or Fraction"),
        (lambda: unit_action(GR(2),(GR(1),GR(0))), NormalizationError, "unit input required"),
        (lambda: unit_action(GR(1),(GR(2),GR(0))), NormalizationError, "unit input required"),
    ]
    for action, error, message in cases:
        try:
            action()
        except error as exc:
            if str(exc) != message:
                raise SystemExit("wrong normalization failure class")
        else:
            raise SystemExit("invalid normalization input admitted")
    print(f"{len(cases)} invalid normalization/unit-action cases refused")


def main() -> None:
    check_normalization_api()
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
