"""Owned nonzero orthogonal Gaussian vector pairs and norm-correct rotations.

AuthorityEffect: None. All values compose the bounded GaussianVector3 domain.
Expected input, arithmetic-budget and invariant refusals use typed Outcome.
"""
from __future__ import annotations

from dataclasses import dataclass

from .boundary import Violation, evaluate
from .gaussian_rational import GaussianRational as G
from .gaussian_vector3 import GaussianVector3, _scalar
from .outcome import Outcome


@dataclass(frozen=True, slots=True, init=False)
class OrthogonalGaussianPair:
    """Invariant: two owned nonzero vectors with conjugate-left inner product0."""
    first: GaussianVector3
    second: GaussianVector3

    def __init__(self, first: object, second: object) -> None:
        u, v = GaussianVector3._operand(first), GaussianVector3._operand(second)
        if u.squared_norm == 0 or v.squared_norm == 0:
            raise Violation('input', 'orthogonal pair requires two nonzero vectors')
        if u._inner(v) != G(0):
            raise Violation('input', 'vectors must be Hermitian orthogonal')
        object.__setattr__(self, 'first', u)
        object.__setattr__(self, 'second', v)

    def _completion(self) -> GaussianVector3:
        return self.first._cross(self.second)

    def completion(self) -> Outcome[GaussianVector3]:
        return evaluate(self._completion)

    def _rotate(self, alpha: object, beta: object) -> OrthogonalGaussianPair:
        a, b = _scalar(alpha), _scalar(beta)
        if a == b == G(0):
            raise Violation('input', 'rotation coefficients cannot both be zero')
        u, v = self.first, self.second
        rotated = u._scale(a)._add(v._scale(b))
        c1 = G(-v.squared_norm)*b.conj()
        c2 = G(u.squared_norm)*a.conj()
        partner = u._scale(c1)._add(v._scale(c2))
        return OrthogonalGaussianPair(rotated, partner)

    def rotate(self, alpha: object, beta: object) -> Outcome[OrthogonalGaussianPair]:
        return evaluate(self._rotate, alpha, beta)
