"""Independent exact witnesses for FSP-IMAGINARY-MU-REAL-DET.

AuthorityEffect: None. Imports no repository code. The model is a one-dimensional
even temporal cycle, three colors, antiperiodic fermions, and unrooted determinant.
All ordinary witnesses lie in Q(i); the center-orbit calculation uses Q(zeta_12).
This fixed, bounded verification program is not a QCD sampler or continuation tool.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import sympy as s


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def gaussian(value: s.Expr) -> s.Expr:
    require(type(value) is not bool, "boolean is outside the scalar domain")
    value = s.sympify(value)
    require(not value.has(s.Float), "binary floating point is outside Q(i)")
    require(s.re(value).is_Rational is True and s.im(value).is_Rational is True,
            "entry is outside Q(i)")
    return s.expand(value)


@dataclass(frozen=True)
class TemporalCycle:
    """Checked immutable links; dense matrices are bounded by six time sites."""

    links: tuple[s.ImmutableMatrix, ...]

    def __post_init__(self) -> None:
        require(type(self.links) is tuple, "links must be an immutable tuple")
        require(len(self.links) in (2, 4, 6), "need an even cycle of 2, 4, or 6 sites")
        for link in self.links:
            require(type(link) is s.ImmutableDenseMatrix, "link must be immutable")
            require(link.shape == (3, 3), "need three colors")
            for entry in link:
                gaussian(entry)
            require(link.H * link == s.eye(3), "link is not unitary")
            require(s.expand(link.det()) == 1, "link determinant is not one")

    def transport(self) -> s.ImmutableMatrix:
        n = len(self.links)
        matrix = s.zeros(3 * n)
        for x, link in enumerate(self.links):
            y = (x + 1) % n
            matrix[3*x:3*x+3, 3*y:3*y+3] = (-1 if x == n - 1 else 1) * link
        return s.ImmutableMatrix(matrix)

    def dirac(self, mass: s.Expr, fugacity: s.Expr) -> s.ImmutableMatrix:
        mass, fugacity = gaussian(mass), gaussian(fugacity)
        require(s.im(mass) == 0, "mass must be real")
        require(fugacity != 0, "zero fugacity has no inverse")
        t = self.transport()
        return s.ImmutableMatrix(mass * s.eye(t.rows) + (fugacity*t - t.H/fugacity)/2)


def equal_matrix(left: s.MatrixBase, right: s.MatrixBase) -> bool:
    return left.shape == right.shape and all(s.expand(e) == 0 for e in left - right)


def expect_rejection(name: str, operation: object) -> str:
    try:
        operation()
    except (ValueError, TypeError):
        return name
    raise RuntimeError("invalid input accepted: " + name)


def main() -> None:
    identity = s.ImmutableMatrix(s.eye(3))
    phase = s.ImmutableMatrix(s.diag(s.I, s.I, -1))
    rotation = s.ImmutableMatrix([[s.Rational(3, 5), s.Rational(4, 5), 0],
                                 [-s.Rational(4, 5), s.Rational(3, 5), 0], [0, 0, 1]])
    links = (phase, rotation, identity, phase * rotation)
    rows = []
    checks = 0
    for n in (2, 4, 6):
        lattice = TemporalCycle(tuple(links[j % len(links)] for j in range(n)))
        t = lattice.transport()
        gamma = s.diag(*[(-1)**(j // 3) for j in range(3*n)])
        require(equal_matrix(gamma*t*gamma, -t), "cycle is not bipartite")
        for z in (s.Integer(1), s.I, s.Rational(3, 5) + s.Rational(4, 5)*s.I):
            for mass in (s.Integer(0), s.Rational(1, 3), s.Integer(1)):
                d = lattice.dirac(mass, z)
                require(equal_matrix(gamma*d*gamma, d.H), "adjoint identity failed")
                det = s.expand(d.det(method="domain-ge"))
                require(det.is_Rational is True and det >= 0, "determinant is not nonnegative")
                if mass > 0:
                    require(det > 0, "positive-mass determinant is not positive")
                even = [3*x+c for x in range(n) if x % 2 == 0 for c in range(3)]
                odd = [3*x+c for x in range(n) if x % 2 == 1 for c in range(3)]
                x = d.extract(even, odd)
                if mass > 0:
                    gram = mass*s.eye(len(odd)) + x.H*x/mass
                    schur = mass**len(even) * gram.det(method="domain-ge")
                    require(s.expand(schur - det) == 0, "independent Schur determinant differs")
                if n == 2 and mass == 1:
                    rows.append({"sites": n, "mass": str(mass), "z": str(z), "det": str(det)})
                checks += 1

    # Hermiticity alone does not fix the sign, even with a nontrivial involution.
    g, negative = s.diag(1, -1), s.diag(-1, 1)
    require(g*g == s.eye(2) and g*negative*g == negative.H, "negative witness symmetry")
    require(negative.det() == -1 and s.diag(negative, negative).det() == 1,
            "single/two-flavor witness")

    # Zero mass can give zero; it is not covered by strict positive-mass positivity.
    zero = TemporalCycle((identity, identity)).dirac(s.Integer(0), s.I)
    require(zero.det() == 0, "zero-mass witness should be singular")

    # A positive nonunit fugacity is outside the imaginary-mu theorem.
    real_mu = TemporalCycle((identity, phase)).dirac(s.Integer(1), s.Integer(2))
    g6 = s.diag(1, 1, 1, -1, -1, -1)
    require(not equal_matrix(g6*real_mu*g6, real_mu.H), "nonunit fugacity guard is essential")
    require(s.im(s.expand(real_mu.det())) != 0, "real-mu complex determinant witness")

    # Boundary-twist Laurent polynomial. On a two-site cycle U0=1,U1=phase.
    # An algebraic t^-1 supplies the adjoint twist on |t|=1; no floating angle.
    t = s.Symbol("t", nonzero=True)
    forward = s.BlockMatrix([[s.zeros(3), s.eye(3)], [-t*phase, s.zeros(3)]]).as_explicit()
    backward = s.BlockMatrix([[s.zeros(3), -phase.H/t], [s.eye(3), s.zeros(3)]]).as_explicit()
    polynomial = s.expand((s.eye(6) + (forward-backward)/2).det())
    omega = (-1 + s.sqrt(3)*s.I)/2
    field = s.QQ.algebraic_field(s.I, s.sqrt(3))  # Q(zeta_12)
    canonical = lambda e: field.to_sympy(field.from_sympy(s.expand(e)))
    require(canonical(omega**3) == 1, "center root order")
    center = s.expand(sum(polynomial.subs(t, omega**k*t) for k in range(3)))
    residual = s.Poly(s.expand(t**3 * (center.subs(t, omega*t)-center)), t)
    require(all(canonical(c) == 0 for c in residual.all_coeffs()), "center-orbit periodicity")
    zsum = canonical(center.subs(t, 1))
    zshift = canonical(center.subs(t, omega))
    require(zsum == zshift and zsum > 0, "center orbit positive equal values")
    # Without the center sum a fixed configuration need not have this period.
    require(canonical(polynomial.subs(t, 1)-polynomial.subs(t, omega)) != 0,
            "fixed-background counterexample to inferred RW periodicity")

    rejected = [
        expect_rejection("odd cycle", lambda: TemporalCycle((identity,)*3)),
        expect_rejection("oversize cycle", lambda: TemporalCycle((identity,)*8)),
        expect_rejection("mutable links", lambda: TemporalCycle([identity, identity])),
        expect_rejection("nonunitary link", lambda: TemporalCycle((2*identity, identity))),
        expect_rejection("wrong determinant", lambda: TemporalCycle((-identity, identity))),
        expect_rejection("zero fugacity", lambda: TemporalCycle((identity,)*2).dirac(1, 0)),
        expect_rejection("nonreal mass", lambda: TemporalCycle((identity,)*2).dirac(s.I, 1)),
        expect_rejection("float entry", lambda: gaussian(s.Float("0.5"))),
        expect_rejection("boolean entry", lambda: gaussian(True)),
    ]
    print(json.dumps({"schema_version": "campaign_independent.v1", "AuthorityEffect": "None",
                      "node": "FSP-IMAGINARY-MU-REAL-DET", "field": "Q(i); Q(zeta_12) for center orbit",
                      "lattice_cases": checks, "determinant_examples": rows,
                      "gamma_only_determinant": "-1", "zero_mass_determinant": "0",
                      "real_fugacity_determinant": str(s.expand(real_mu.det())),
                      "boundary_polynomial": str(polynomial), "center_sum_at_one": str(zsum),
                      "rejected_inputs": rejected, "result": "PASS",
                      "scope": "Finite 1D cycles; finite center-orbit sum, not a QCD measure or continuation."}, indent=2))


if __name__ == "__main__":
    main()
