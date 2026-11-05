"""Owned nine-ray Hermitian tomography model and exact symbolic certificates.

AuthorityEffect: None. Symbolic variables and polynomial sizes are fixed here;
query vectors and relation coefficients use bounded exact domains. These are
algebraic identities and finite controls, not a global frame rigidity proof.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .boundary import Violation, evaluate
from .cases import Cases
from .domains import rational, sequence
from .gaussian_vector3 import GaussianVector3 as V
from .orthogonal_gaussian_pair import OrthogonalGaussianPair
from .outcome import Outcome


def _symbolic_vector(vector: V) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix([sp.Rational(x.re.numerator, x.re.denominator)
                               + sp.I*sp.Rational(x.im.numerator, x.im.denominator)
                               for x in vector.entries])


def _zero(expression: object) -> bool:
    return bool(sp.expand(expression) == 0)


@dataclass(frozen=True, slots=True, init=False)
class HermitianTomography:
    """Owns a generic Hermitian form and its ordered nine fixed measurement rays."""
    form: sp.ImmutableMatrix
    rays: tuple[V, ...]
    values: tuple[sp.Expr, ...]
    coefficients: tuple[sp.Expr, ...]

    def __init__(self) -> None:
        diagonal = sp.symbols('d0:3', real=True)
        real = sp.symbols('a01 a02 a12', real=True)
        imag = sp.symbols('b01 b02 b12', real=True)
        form = sp.diag(*diagonal)
        for (j, k), a, b in zip(((0, 1), (0, 2), (1, 2)), real, imag):
            form[j, k] = a+sp.I*b
            form[k, j] = a-sp.I*b
        rays = tuple(V._integers(row) for row in (
            (1, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 0),
            (1, 0, 1, 0, 0, 0), (1, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0), (1, 0, 0, 0, 0, 1),
            (0, 0, 1, 0, 1, 0), (0, 0, 1, 0, 0, 1)))
        object.__setattr__(self, 'form', sp.ImmutableMatrix(form))
        object.__setattr__(self, 'rays', rays)
        object.__setattr__(self, 'coefficients', tuple(diagonal)+tuple(real)+tuple(imag))
        object.__setattr__(self, 'values', tuple(self._evaluate(ray) for ray in rays))

    def _evaluate(self, value: object) -> sp.Expr:
        vector = V._operand(value)
        if vector.squared_norm == 0:
            raise Violation('input', 'tomography evaluation requires a nonzero vector')
        symbolic = _symbolic_vector(vector)
        norm = sp.Rational(vector.squared_norm.numerator, vector.squared_norm.denominator)
        result: sp.Expr = sp.expand((symbolic.conjugate().T*self.form*symbolic)[0]/norm)
        return result

    def evaluate(self, value: object) -> Outcome[sp.Expr]:
        return evaluate(self._evaluate, value)

    def _reconstruction(self, cases: Cases) -> int:
        diagonal = self.coefficients[:3]; real = self.coefficients[3:6]; imag = self.coefficients[6:]
        expected = list(diagonal)
        for (j, k), a, b in zip(((0, 1), (0, 2), (1, 2)), real, imag):
            expected.extend(((diagonal[j]+diagonal[k])/2+a, (diagonal[j]+diagonal[k])/2-b))
        cases.require(self.form == self.form.conjugate().T, 'candidate is Hermitian')
        cases.require(all(_zero(x-y) for x, y in zip(self.values, expected)), 'nine-ray reconstruction signs')
        matrix = sp.Matrix(self.values).jacobian(self.coefficients)
        cases.require(matrix.det() != 0, 'tomography has exact rank nine')
        measurements = sp.symbols('m0:9', real=True)
        reals = []; imags = []
        for index, (j, k) in enumerate(((0, 1), (0, 2), (1, 2))):
            mean = (measurements[j]+measurements[k])/2
            reals.append(measurements[3+2*index]-mean)
            imags.append(mean-measurements[4+2*index])
        substitution = dict(zip(self.coefficients, list(measurements[:3])+reals+imags))
        cases.require(all(_zero(value.subs(substitution)-measurement) for value, measurement in zip(self.values, measurements)),
                'candidate recovers arbitrary rational measurements')
        cases.require(not _zero(self.values[4]-(diagonal[0]+diagonal[1])/2-imag[0]),
                'negative control rejects reversed imaginary sign')
        return int(matrix.rank())

    def _expansion(self, cases: Cases) -> None:
        x = sp.symbols('x0:3', real=True); y = sp.symbols('y0:3', real=True)
        vector = sp.Matrix([a+sp.I*b for a, b in zip(x, y)])
        numerator = sp.expand((vector.conjugate().T*self.form*vector)[0])
        diagonal = self.coefficients[:3]; real = self.coefficients[3:6]; imag = self.coefficients[6:]
        expansion = sum(diagonal[j]*(x[j]**2+y[j]**2) for j in range(3))
        for (j, k), a, b in zip(((0, 1), (0, 2), (1, 2)), real, imag):
            expansion += 2*a*(x[j]*x[k]+y[j]*y[k])-2*b*(x[j]*y[k]-y[j]*x[k])
        cases.require(_zero(numerator-expansion), 'generic quadratic expansion')
        cases.require(_zero(sp.im(numerator)), 'quadratic numerator is real over Q(i)')

    @staticmethod
    def _adjugate(cases: Cases) -> None:
        matrix = sp.Matrix(3, 3, sp.symbols('u0:9'))
        residual = matrix*matrix.adjugate()-matrix.det()*sp.eye(3)
        cases.require(all(_zero(entry) for entry in residual), 'generic three-by-three adjugate identity')

    @staticmethod
    def _rescaling(cases: Cases) -> None:
        bound = sp.symbols('B', nonnegative=True); epsilon = 1/(3*(bound+1))
        cases.require(sp.cancel(sp.Rational(1, 3)-epsilon*bound-epsilon) == 0, 'rescaled lower bound')
        cases.require(sp.cancel(sp.Rational(1, 3)+epsilon*bound-(2*bound+1)/(3*(bound+1))) == 0, 'rescaled upper bound')
        cases.require(sp.cancel(sp.Rational(2, 3)-(2*bound+1)/(3*(bound+1))-epsilon) == 0, 'strict upper bound gap')
        cases.require(epsilon.is_positive is True, 'positive rescaling including zero bound')
        cases.require(epsilon.subs(bound, 0) == sp.Rational(1, 3), 'zero-bound rescaling control')

    def _kernel_relation(self, value: object, coefficients: object) -> bool:
        vector = V._operand(value)
        weights = tuple(rational(x, 'kernel coefficient') for x in sequence(coefficients, 'nine coefficients', 9))
        expression = self._evaluate(vector)
        for weight, measurement in zip(weights, self.values):
            expression += sp.Rational(weight.numerator, weight.denominator)*measurement
        return _zero(expression)

    def kernel_relation(self, value: object, coefficients: object) -> Outcome[bool]:
        return evaluate(self._kernel_relation, value, coefficients)

    def _parallelogram(self, value: object) -> bool:
        if type(value) is not OrthogonalGaussianPair:
            raise Violation('input', 'parallelogram requires an owned orthogonal pair')
        u, v = value.first, value.second
        total = rational(u.squared_norm+v.squared_norm, 'parallelogram norm sum')
        nu, nv = (rational(2*x/total, 'parallelogram weight') for x in (u.squared_norm, v.squared_norm))
        expression = self._evaluate(u._add(v))+self._evaluate(u._sub(v))
        expression -= sp.Rational(nu.numerator, nu.denominator)*self._evaluate(u)
        expression -= sp.Rational(nv.numerator, nv.denominator)*self._evaluate(v)
        return _zero(expression)

    def parallelogram(self, value: object) -> Outcome[bool]:
        return evaluate(self._parallelogram, value)

    def _verify(self) -> dict[str, int]:
        cases = Cases()
        rank = self._reconstruction(cases)
        self._expansion(cases); self._adjugate(cases); self._rescaling(cases)
        return {'tomography_rank': rank, 'checks': cases.checks}

    def verify(self) -> Outcome[dict[str, int]]:
        return evaluate(self._verify)
