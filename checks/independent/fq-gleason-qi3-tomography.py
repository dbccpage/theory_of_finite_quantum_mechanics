"""Exact nine-ray, inert-prime and equatorial-geometry controls on Q(i)^3.

AuthorityEffect: None. Symbolic identities are distinguished from the explicit
finite frame, perturbation and rotation samples. These controls do not prove
pointwise-to-uniform continuity or classify all frame functions.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import rational
from checker_support.equatorial_ray_geometry import EquatorialRayGeometry as E, NORTH
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.gaussian_vector3 import GaussianVector3 as V
from checker_support.hermitian_tomography import HermitianTomography as H, _symbolic_vector, _zero
from checker_support.inert_prime_residual import InertPrimeResidual as R
from checker_support.orthogonal_gaussian_pair import OrthogonalGaussianPair as P
from checker_support.outcome import Outcome

Weights = tuple[Q, ...]


def _vector(*coordinates: int) -> V:
    return V._integers(coordinates)


def _swap_equator(vector: V) -> V:
    x, y, z = vector.entries
    return V((x, z, y))


def _born(vector: V) -> Q:
    return E._born_weight(vector)


@dataclass(frozen=True, slots=True, init=False)
class GaussianTomographyControls:
    """Owns the fixed witness family; each verification owns its case recorder."""
    model: H
    residuals: tuple[R, ...]
    witnesses: tuple[V, ...]
    partners: tuple[V, ...]
    equators: tuple[V, ...]
    parallelograms: tuple[V, ...]
    kernels: tuple[Weights, ...]

    def __init__(self) -> None:
        object.__setattr__(self, 'model', H())
        object.__setattr__(self, 'residuals', tuple(R(p) for p in (3, 7, 11)))
        object.__setattr__(self, 'witnesses', (_vector(1, 0, 1, 0, 1, 0), _vector(1, 0, 2, 0, 1, 1), _vector(1, 0, 3, 0, 1, 0)))
        object.__setattr__(self, 'partners', (_vector(1, 0, -1, 0, 0, 0), _vector(2, 0, -1, 0, 0, 0), _vector(3, 0, -1, 0, 0, 0)))
        object.__setattr__(self, 'equators', (_vector(0, 0, 1, 0, 1, 1), _vector(0, 0, 1, 1, 2, 1), _vector(0, 0, 3, 0, 1, 1)))
        object.__setattr__(self, 'parallelograms', tuple(w._sub(NORTH) for w in self.witnesses))
        object.__setattr__(self, 'kernels', (
            tuple(Q(x, 3) for x in (1, 1, 1, -2, 0, -2, 0, -2, 0)),
            tuple(Q(x, 7) for x in (3, 2, 4, -4, 0, -2, -2, -4, -4)),
            tuple(Q(x, 11) for x in (3, -3, 3, -6, 0, -2, 0, -6, 0))))

    def _fixture_values(self, cases: Cases) -> None:
        for index, residual in enumerate(self.residuals):
            for ray in self.model.rays:
                cases.require(residual._residual(ray) == 0, 'residual vanishes on tomography ray')
                cases.require(residual._exotic(ray) == Q(1, 3), 'exotic tomography value')
            witness = self.witnesses[index]
            cases.require(witness._integer_primitive(), 'inert-prime witness is (1+i)-primitive')
            cases.require(witness.squared_norm == residual.prime, 'inert-prime witness norm')
            for other, vector in enumerate(self.witnesses):
                cases.require(residual._residual(vector) == int(index == other), 'three-prime witness duality')
        for vector, norm, sign in ((_vector(1, 2, 1, 2, 1, 1), 12, -1), (_vector(1, 4, 1, 2, 1, 1), 24, 1)):
            cases.require(vector._integer_primitive(), 'divisible-by-four norm witness is primitive')
            cases.require(vector.squared_norm == norm, 'divisible-by-four/eight squared norm')
            cases.require(self.residuals[0]._residual(vector) == sign, 'divisible-by-four/eight residual sign')

    def _frame(self, pair: P, cases: Cases) -> None:
        u, v, w = pair.first, pair.second, pair._completion()
        cases.require(w.squared_norm > 0, 'Hermitian completion is nonzero')
        cases.require(u._inner(v) == u._inner(w) == v._inner(w) == G(0), 'three Hermitian orthogonality equations')
        for residual in self.residuals:
            cases.require(sum(residual._valuation(x.squared_norm) for x in (u, v, w)) % 2 == 0, 'even frame norm-valuation sum')
            cases.require(sum(residual._residual(x) for x in (u, v, w)) == 0, 'sampled zero-weight frame sum')
            cases.require(sum(residual._exotic(x) for x in (u, v, w)) == 1, 'sampled exotic frame sum')

    def _frames(self, cases: Cases) -> None:
        pairs = tuple(P(u, v) for u, v in zip(self.witnesses, self.partners))
        extras = (P(self.witnesses[0], _vector(1, 0, 1, 0, -2, 0)),
                  P(_vector(1, 2, 1, 2, 1, 1), _vector(1, 0, -1, 0, 0, 0)),
                  P(_vector(1, 4, 1, 2, 1, 1), _vector(0, 0, 2, 4, -5, -5)))
        for pair in pairs+extras:
            self._frame(pair, cases)
        first = pairs[0]
        cases.require(sum(abs(self.residuals[0]._residual(x)) for x in (first.first, first.second, first._completion())) == 2,
                      'unsigned residual negative control fails zero-weight sum')

    def _kernel_value(self, index: int, function: Callable[[V], Q]) -> Q:
        total = rational(function(self.witnesses[index]), 'kernel witness value')
        for weight, ray in zip(self.kernels[index], self.model.rays):
            total = rational(total+rational(weight*function(ray), 'kernel term'), 'kernel prefix')
        return total

    def _combination(self, coefficients: Weights, vector: V) -> Q:
        return sum((weight*residual._residual(vector) for weight, residual in zip(coefficients, self.residuals)), Q(0))

    def _kernel_controls(self, cases: Cases) -> None:
        for index, (vector, weights) in enumerate(zip(self.witnesses, self.kernels)):
            cases.require(self.model._kernel_relation(vector, weights), 'symbolic projector kernel identity')
            for other, residual in enumerate(self.residuals):
                cases.require(self._kernel_value(index, residual._residual) == int(index == other), 'residual separates its kernel relation')
            cases.require(self._kernel_value(index, self.residuals[index]._exotic) == Q(1, 3), 'exotic separates its kernel relation')
        coefficients = ((Q(2, 5), Q(-3, 7), Q(0)), (Q(1, 5), Q(-2, 7), Q(4, 11)))
        for index, weights in zip((1, 2), coefficients):
            cases.require(self._kernel_value(index, lambda vector: self._combination(weights, vector)) == weights[index],
                          'mixed residual kernel extracts selected coefficient')

    def _mixture_controls(self, cases: Cases) -> None:
        residual = self.residuals[1]
        cases.require(residual._exotic(self.witnesses[1]) == Q(2, 3), 's7 exotic witness value')
        cases.require(residual._exotic(self.witnesses[0]) == Q(1, 3), 's7 exotic at s3 witness')
        pair = P(self.witnesses[1], self.partners[1]); frame = (pair.first, pair.second, pair._completion())
        weights = (Q(2, 5), Q(-3, 5), Q(0))
        values = tuple((1+self._combination(weights, vector))/3 for vector in frame)
        cases.require(sum(values) == 1, 'mixed exotic sampled frame sum')
        cases.require(all(0 <= value <= 1 for value in values), 'mixed exotic sampled nonnegativity')

    def _oscillation(self, index: int, denominator: int, cases: Cases) -> tuple[V, V]:
        equator = self.equators[index]; residual = self.residuals[index]
        positive_integer = NORTH._scale(G(denominator))._add(equator)
        negative_integer = NORTH._scale(G(denominator))._add(_swap_equator(equator))
        positive = positive_integer._scale(G(Q(1, denominator)))
        negative = negative_integer._scale(G(Q(1, denominator)))
        cases.require(residual._residual(positive_integer) == residual._residual(positive) == 1, 'positive sampled oscillation and scaling')
        cases.require(residual._residual(negative_integer) == residual._residual(negative) == -1, 'negative sampled oscillation and scaling')
        cases.require(residual._exotic(positive) == Q(2, 3), 'positive oscillation exotic value')
        cases.require(residual._exotic(negative) == 0, 'negative oscillation exotic value')
        distance = Q(residual.prime, denominator*denominator)
        cases.require(positive._sub(NORTH).squared_norm == distance, 'positive sampled oscillation distance')
        cases.require(negative._sub(NORTH).squared_norm == distance, 'negative sampled oscillation distance')
        return positive, negative

    def _oscillations(self, cases: Cases) -> None:
        for k in range(1, 8):
            self._oscillation(0, 3*k, cases)
            seven = self._oscillation(1, 7*k, cases)
            three_subsequence = self._oscillation(0, 21*k, cases)
            cases.require(all(self.residuals[0]._residual(v) == 0 for v in seven), 's7 oscillation is s3-null')
            cases.require(all(self.residuals[1]._residual(v) == 0 for v in three_subsequence), 's3 subsequence is s7-null')
        for k in range(1, 5):
            for index in range(3):
                rays = self._oscillation(index, 231*k, cases)
                for other, residual in enumerate(self.residuals):
                    expected = (Q(1), Q(-1)) if index == other else (Q(0), Q(0))
                    cases.require(tuple(residual._residual(ray) for ray in rays) == expected, 'three-prime selective oscillation samples')

    def _quadratic_extensions(self, cases: Cases) -> tuple[tuple[int, int, int], ...]:
        coefficients = ((sp.Integer(1), 1+sp.I), (1+sp.I, 2+sp.I), (sp.Integer(3), 1+sp.I))
        expected = (18, 245, 1210); results = []
        for index, (alpha, beta) in enumerate(coefficients):
            pair = P(self.witnesses[index], self.partners[index]); prime = self.residuals[index].prime
            u = _symbolic_vector(pair.first)
            v = sp.sqrt(prime)*_symbolic_vector(pair.second)
            w = _symbolic_vector(pair._completion())
            p, q = alpha*v+beta*w, sp.conjugate(beta)*v-sp.conjugate(alpha)*w
            cases.require(all(_zero((a.conjugate().T*b)[0]) for a, b in ((u, p), (u, q), (p, q))), 'quadratic-extension frame orthogonality')
            norms = tuple(sp.expand((x.conjugate().T*x)[0]) for x in (u, p, q))
            cases.require(norms == (prime, expected[index], expected[index]), 'quadratic-extension exact rational norms')
            for other, residual in enumerate(self.residuals):
                valuation = 2 if index == other else 0
                cases.require(residual._valuation(Q(expected[index])) == valuation, 'quadratic-extension partner exact selected valuation')
            results.append((int(norms[0]), int(norms[1]), int(norms[2])))
        return tuple(results)

    def _equator_witnesses(self, cases: Cases) -> None:
        for index, vector in enumerate(self.equators):
            for sign, witness in ((1, vector), (-1, _swap_equator(vector))):
                cases.require(_born(witness) == 0, 'equatorial witness has zero north-pole weight')
                expected = tuple(sign if index == other else 0 for other in range(3))
                cases.require(tuple(residual._residual(witness) for residual in self.residuals) == expected, 'signed three-prime equatorial witness table')

    def _rotated_pair(self, pair: P, alpha: G, beta: G, cases: Cases) -> None:
        rotated = pair._rotate(alpha, beta); u, v = pair.first, pair.second
        cases.require(rotated.first._inner(rotated.second) == G(0), 'planar rotation orthogonality')
        cases.require(rotated.first.squared_norm == alpha.norm_sq()*u.squared_norm+beta.norm_sq()*v.squared_norm, 'first rotated norm identity')
        cases.require(rotated.second.squared_norm == u.squared_norm*v.squared_norm*rotated.first.squared_norm, 'second rotated norm identity')
        cases.require(_born(rotated.first)+_born(rotated.second) == _born(u)+_born(v), 'planar Born subspace sum')
        for residual in self.residuals:
            cases.require(residual._residual(rotated.first)+residual._residual(rotated.second) == residual._residual(u)+residual._residual(v), 'sampled planar residual subspace sum')

    def _rotation_controls(self, cases: Cases) -> None:
        for u, v in zip(self.witnesses, self.partners):
            pair = P(u, v)
            cases.require(self.model._parallelogram(pair), 'symbolic orthogonal projector parallelogram')
            for alpha, beta in ((G(2, -1), G(1, 2)), (G(Q(1, 3), Q(-2, 3)), G(Q(3, 5)))):
                self._rotated_pair(pair, alpha, beta, cases)

    def _parallelogram_counterexamples(self, cases: Cases) -> tuple[int, ...]:
        results = []
        for residual, equator in zip(self.residuals, self.parallelograms):
            plus, minus = NORTH._add(equator), NORTH._sub(equator)
            cases.require(NORTH._inner(equator) == G(0), 'counterexample pair is orthogonal')
            cases.require(residual._residual(NORTH) == residual._residual(equator) == 0, 'counterexample summands are residual-null')
            cases.require(residual._residual(plus) == residual._residual(minus) == 1, 'both counterexample sums have value one')
            total = residual._residual(plus)+residual._residual(minus)
            cases.require(total == 2, 'orthogonal parallelogram residual counterexample')
            results.append(int(total))
        return tuple(results)

    def _piron_sample(self, geometry: E, k: int, cases: Cases) -> None:
        scalar = G(Q(1, k)); v = geometry.quarter_turn._scale(scalar)
        pair = geometry._piron(scalar); meridian = geometry._meridian()
        cases.require(geometry.base._inner(v) == geometry.base._inner(meridian) == v._inner(meridian) == G(0), 'Piron base frame orthogonality')
        cases.require(pair.first._inner(pair.second) == G(0), 'Piron rotated pair orthogonality')
        cases.require(_born(pair.first)+_born(pair.second) == _born(geometry.base)+_born(v), 'Piron Born subspace sum')
        cases.require(_born(pair.first) <= _born(geometry.base), 'Piron north-pole descent')
        cases.require(_born(geometry.base)+_born(meridian) == 1, 'meridian complement')
        cases.require(pair.first._sub(geometry.base).squared_norm == geometry.vector.squared_norm/Q(k*k), 'Piron step distance')
        rotated = geometry._pythagorean(k)
        cases.require(rotated.entries[0] == G(0), 'Pythagorean rotation stays equatorial')
        cases.require(rotated.squared_norm == geometry.vector.squared_norm, 'Pythagorean norm preservation')
        cases.require(E(rotated).base.squared_norm == geometry.base.squared_norm, 'rotated pole-sum norm')
        cases.require(_born(E(rotated).base) == _born(geometry.base), 'Pythagorean north-pole weight')

    def _quarter_kelvin(self, geometry: E, cases: Cases) -> None:
        y, turned = geometry.vector, geometry.quarter_turn
        negative = y._scale(G(-1))
        cases.require(E(turned).quarter_turn == negative, 'equatorial quarter-turn squares to negation')
        cases.require(geometry._pythagorean(1) == turned, 'Pythagorean k=1 is quarter-turn')
        cases.require(E(turned)._pythagorean(1) == negative, 'two Pythagorean quarter-turns')
        cases.require(E(geometry._tangent(Q(1)))._tangent(Q(1)) == turned._scale(G(2)), 'two unit tangent steps')
        kelvin = geometry._kelvin()
        cases.require(kelvin.entries[0] == G(0), 'Kelvin remains equatorial')
        cases.require(kelvin.squared_norm == 1/y.squared_norm, 'Kelvin norm inversion')
        cases.require(geometry._meridian()._scale(G(-1/y.squared_norm)) == E(kelvin).base, 'Kelvin meridian ray identity')
        cases.require(_born(geometry.base)+_born(E(kelvin).base) == 1, 'Kelvin Born complement')
        step = geometry._piron(G(1)).first
        cases.require(_born(E(turned._scale(G(2))).base) <= _born(step) <= _born(geometry.base), 'two-step north-pole descent')

    def _tangent_sample(self, geometry: E, parameter: Q, cases: Cases) -> None:
        y = geometry.vector; t = parameter; stepped = geometry._tangent(t)
        for s in (Q(1, 3), -t):
            actual = E(stepped)._tangent(s)
            expected = y._scale(G(1-t*s))._add(geometry.quarter_turn._scale(G(t+s)))
            cases.require(actual == expected, 'two-step tangent composition')
        outward = 1+t*t; inward = 1/outward
        cases.require(geometry._piron(G(t)).first == E(stepped).base, 'Piron and tangent pole sums agree')
        cases.require(stepped.squared_norm == outward*y.squared_norm, 'tangent norm identity')
        cases.require(E(stepped).quarter_turn == y._scale(G(-t))._add(geometry.quarter_turn), 'quarter-turn of tangent step')
        cases.require(E(stepped)._tangent(-t) == y._scale(G(outward)), 'tangent cancellation gives radial dilation')
        weights = (_born(E(y._scale(G(outward))).base), _born(E(stepped).base), _born(geometry.base), _born(E(y._scale(G(inward))).base))
        cases.require(all(a <= b for a, b in zip(weights, weights[1:])), 'outward/inward radial monotonicity')

    def _sandwich_sample(self, geometry: E, k: int, cases: Cases) -> None:
        inside, outside, tangent = Q(k*k-1, k*k+1), Q(k*k+1, k*k-1), Q(2*k, k*k-1)
        inner = E(geometry.vector._scale(G(inside))); outer = E(geometry.vector._scale(G(outside)))
        rotated = E(geometry._pythagorean(k))
        cases.require(inner._tangent(tangent) == rotated.vector, 'inner tangent is Pythagorean rotation')
        cases.require(rotated._tangent(-tangent) == outer.vector, 'inverse tangent is outer radius')
        cases.require(_born(outer.base) <= _born(rotated.base) <= _born(inner.base), 'two-sided Pythagorean sandwich')
        cases.require(inner.base._sub(geometry.base).squared_norm == (inside-1)**2*geometry.vector.squared_norm, 'inner radial distance')
        cases.require(outer.base._sub(geometry.base).squared_norm == (outside-1)**2*geometry.vector.squared_norm, 'outer radial distance')

    @staticmethod
    def _squeeze_sample(geometry: E, k: int, epsilon: Q) -> bool:
        inside, outside = Q(k*k-1, k*k+1), Q(k*k+1, k*k-1)
        gap = _born(E(geometry.vector._scale(G(inside))).base)-_born(E(geometry.vector._scale(G(outside))).base)
        rotated_gap = abs(_born(E(geometry._pythagorean(k)).base)-_born(geometry.base))
        return gap < epsilon and rotated_gap < epsilon

    def _equatorial_controls(self, cases: Cases) -> None:
        for vector in self.equators:
            for k in range(1, 5):
                self._piron_sample(E(vector), k, cases)
        for vector in self.equators+self.parallelograms:
            geometry = E(vector); self._quarter_kelvin(geometry, cases)
            for t in (Q(1, 2), Q(2, 3), Q(-3, 4)):
                self._tangent_sample(geometry, t, cases)
            for k in range(2, 6):
                self._sandwich_sample(geometry, k, cases)
            for epsilon in (Q(1, 5), Q(1, 25), Q(1, 100)):
                cases.require(any(self._squeeze_sample(geometry, k, epsilon) for k in range(2, 40)), 'finite sampled epsilon sandwich')
            cases.require(_born(vector) == _born(geometry.quarter_turn) == 0, 'equatorial north-pole weights vanish')

    def _symmetry_samples(self, cases: Cases) -> tuple[int, ...]:
        results = []
        for residual, vector in zip(self.residuals, self.parallelograms):
            geometry = E(vector); swapped = _swap_equator(vector)
            cases.require(swapped.squared_norm == vector.squared_norm, 'swapped equator norm')
            cases.require(residual._residual(E(swapped).base) == residual._residual(geometry.base) == 1, 'sampled equatorial norm invariance')
            for k in range(1, 6):
                cases.require(residual._residual(E(geometry._pythagorean(k)).base) == 1, 'sampled Pythagorean residual invariance')
            twice = E(geometry._pythagorean(1))._pythagorean(1)
            cases.require(twice == vector._scale(G(-1)), 'sampled half-turn is negation')
            cases.require(residual._residual(geometry.base)+residual._residual(E(twice).base) == 2, 'rotation invariance does not imply residual parallelogram law')
            results.append(int(residual._residual(E(geometry._pythagorean(1)).base)))
        return tuple(results)

    def _verify(self) -> dict[str, object]:
        cases = Cases(); symbolic = self.model._verify()
        self._fixture_values(cases); self._frames(cases); self._kernel_controls(cases)
        self._mixture_controls(cases); self._oscillations(cases)
        extensions = self._quadratic_extensions(cases)
        self._equator_witnesses(cases); self._rotation_controls(cases)
        sums = self._parallelogram_counterexamples(cases)
        self._equatorial_controls(cases); symmetries = self._symmetry_samples(cases)
        return {'status': 'PASS', 'authority_effect': 'None', 'sympy_version': sp.__version__,
                'checks': cases.checks+symbolic['checks'], 'tomography_rank': symbolic['tomography_rank'],
                's3_witness_111': int(self.residuals[0]._residual(self.witnesses[0])),
                's3_witness_div4': int(self.residuals[0]._residual(_vector(1, 2, 1, 2, 1, 1))),
                's3_witness_div8': int(self.residuals[0]._residual(_vector(1, 4, 1, 2, 1, 1))),
                's7_witness_p7': int(self.residuals[1]._residual(self.witnesses[1])),
                'sp11_witness_p11': int(self.residuals[2]._residual(self.witnesses[2])),
                'exotic_qi7_witness_p7': str(self.residuals[1]._exotic(self.witnesses[1])),
                'sqrt3_frame_norms': list(extensions[0]), 'sqrt7_frame_norms': list(extensions[1]),
                'sqrt11_frame_norms': list(extensions[2]), 'piron_ortho_parallelogram_sums': list(sums),
                'pythag_rot_invariance_3_7_11': list(symmetries),
                'scope': 'Fixed symbolic algebra identities and explicit finite frame, perturbation, rotation and epsilon samples; no pointwise-to-uniform continuity implication or global rigidity conclusion.'}

    def verify(self) -> Outcome[dict[str, object]]:
        return evaluate(self._verify)


def verify() -> Outcome[dict[str, object]]:
    return evaluate(GaussianTomographyControls).bind(lambda controls: controls.verify())


def _main() -> None:
    print(json.dumps(GaussianTomographyControls()._verify(), sort_keys=True))


def main() -> int:
    return cli(_main)


if __name__ == '__main__':
    raise SystemExit(main())
