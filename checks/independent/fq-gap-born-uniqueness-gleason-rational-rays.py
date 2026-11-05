"""Finite rational-ray obstruction controls with owned canonical integer rays.

AuthorityEffect: None. Completes distinct orthogonal ray pairs represented in
the radius-six integer box; the completing vector may lie outside that box.
Checks all64 parity-admitted mod4 tuples and a seven-ray quadratic obstruction.
No Gaussian-ray, continuum or physical conclusion is inferred.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import sys
from typing import cast

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, rational, sequence
from checker_support.outcome import Outcome
from checker_support.rational_inverse import _inverse
from checker_support.rational_matrix import RationalMatrix

Coordinates=tuple[int,int,int]


def _integer(value: object) -> int:
    number=integer(value,'ray integer')
    if number.bit_length()>4096:
        raise Violation('resource','ray input/intermediate exceeds4096 bits')
    return number


def _coordinates(value: object) -> Coordinates:
    return cast(Coordinates,tuple(_integer(x) for x in sequence(value,'ray vector',3,3)))


def _dot(left: Coordinates,right: Coordinates) -> int:
    total=0
    for a,b in zip(left,right):
        total=_integer(total+_integer(a*b))
    return total


def _cross(left: Coordinates,right: Coordinates) -> Coordinates:
    return cast(Coordinates,tuple(_integer(_integer(left[j]*right[k])-_integer(left[k]*right[j]))
                                  for j,k in ((1,2),(2,0),(0,1))))


def _pair_sign(left: object,right: object) -> int:
    a,b=_integer(left),_integer(right)
    if a % 2 != 1 or b % 2 != 1:
        raise Violation('input','pair sign requires two odd integers')
    return -1 if a % 4 == b % 4 else 1


def pair_sign(left: object,right: object) -> Outcome[int]:
    return evaluate(_pair_sign,left,right)


@dataclass(frozen=True,slots=True,init=False)
class IntegerRay3:
    """Owned primitive integer representative with positive first nonzero entry."""
    coordinates: Coordinates

    def __init__(self,value: object) -> None:
        coordinates=_coordinates(value)
        content=gcd(*coordinates)
        if content==0:
            raise Violation('input','the zero vector has no rational ray')
        leading=next(x for x in coordinates if x)
        divisor=-content if leading<0 else content
        object.__setattr__(self,'coordinates',cast(Coordinates,tuple(x//divisor for x in coordinates)))

    @property
    def value(self) -> Q:
        odd=tuple(x for x in self.coordinates if x % 2)
        sign=_pair_sign(odd[0],odd[1]) if len(odd)==2 else 0
        return Q(1+sign,3)

    @staticmethod
    def _other(value: object) -> IntegerRay3:
        if type(value) is not IntegerRay3:
            raise Violation('input','ray operation requires IntegerRay3')
        return value

    def dot(self,other: object) -> Outcome[int]:
        return evaluate(lambda: _dot(self.coordinates,self._other(other).coordinates))

    def _complete(self,other: object) -> IntegerRay3:
        right=self._other(other)
        if _dot(self.coordinates,right.coordinates)!=0:
            raise Violation('input','frame completion requires orthogonal rays')
        return IntegerRay3(_cross(self.coordinates,right.coordinates))

    def complete(self,other: object) -> Outcome[IntegerRay3]:
        return evaluate(self._complete,other)

    def _scale(self,factor: object) -> IntegerRay3:
        scalar=_integer(factor)
        if scalar==0:
            raise Violation('input','ray scaling requires a nonzero integer')
        return IntegerRay3(tuple(_integer(scalar*x) for x in self.coordinates))

    def scale(self,factor: object) -> Outcome[IntegerRay3]:
        return evaluate(self._scale,factor)

    def _quadratic_row(self) -> tuple[Q,...]:
        a,b,c=self.coordinates
        squares=tuple(_integer(x*x) for x in self.coordinates)
        cross=tuple(_integer(2*_integer(x*y)) for x,y in ((a,b),(a,c),(b,c)))
        norm=_dot(self.coordinates,self.coordinates)
        return tuple(Q(x) for x in squares+cross)+(rational(self.value*norm),)

    def quadratic_row(self) -> Outcome[tuple[Q,...]]:
        return evaluate(self._quadratic_row)


def exotic(value: object) -> Outcome[Q]:
    """Canonical ray value, including even representatives after normalization."""
    return evaluate(lambda: IntegerRay3(value).value)


def _box(radius: object) -> tuple[IntegerRay3,...]:
    bound=integer(radius,'ray box radius',1,6)
    rays={IntegerRay3(vector) for vector in product(range(-bound,bound+1),repeat=3) if any(vector)}
    return tuple(sorted(rays,key=lambda ray:ray.coordinates))


def ray_box(radius: object) -> Outcome[tuple[IntegerRay3,...]]:
    return evaluate(_box,radius)


def _frames(rays: tuple[IntegerRay3,...],cases: Cases) -> int:
    count=0
    for left,right in combinations(rays,2):
        if _dot(left.coordinates,right.coordinates)==0:
            third=left._complete(right)
            cases.require(_dot(left.coordinates,third.coordinates)==0,'completion perpendicular to first ray')
            cases.require(_dot(right.coordinates,third.coordinates)==0,'completion perpendicular to second ray')
            cases.require(left.value+right.value+third.value==1,'exotic frame sum')
            count+=1
    return count


def _congruence(cases: Cases) -> int:
    count=0
    for a,b,c,d in product((1,3),repeat=4):
        for e,f in product((0,2),repeat=2):
            if (a*c+b*d+e*f) % 4==0:
                cases.require(_pair_sign(a,b)+_pair_sign(c,d)==0,'modulo-four cancellation')
                count+=1
    cases.require(count==32,'all32 compatible tuples among64 parity-admitted tuples')
    return count


def _obstruction(cases: Cases) -> None:
    seven=((1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1))
    rows=tuple(IntegerRay3(vector)._quadratic_row() for vector in seven)
    coefficients=RationalMatrix(tuple(row[:6] for row in rows))
    target=RationalMatrix(tuple((row[6],) for row in rows))
    basis=RationalMatrix(coefficients.rows[:6])
    solution=_inverse(basis).mul(RationalMatrix(target.rows[:6]))
    fitted=coefficients.mul(solution)
    cases.require(fitted.rows[:6]==target.rows[:6],'rank-six basis interpolation')
    cases.require(fitted.rows[6]!=target.rows[6],'seventh ray contradicts quadratic interpolation')
    cases.require(solution==RationalMatrix(((Q(1,3),),)*3+((Q(-1,3),),)*3),'forced symmetric coefficients')
    witness=RationalMatrix(((-1,-1,-1,1,1,1,-1),))
    cases.require(witness.mul(coefficients)==RationalMatrix(((0,)*6,)),'left-null certificate annihilates coefficients')
    cases.require(witness.mul(target)==RationalMatrix(((-2,),)),'left-null certificate contradicts target')
    cases.require(IntegerRay3((1,1,0)).value==0,'zero exotic value witness')
    cases.require(IntegerRay3((1,-1,0)).value==Q(2,3),'two-thirds exotic value witness')
    cases.require(IntegerRay3((1,1,1)).value==Q(1,3),'one-third exotic value witness')


def _values(rays: tuple[IntegerRay3,...],cases: Cases) -> None:
    for ray in rays:
        cases.require(ray.value in (Q(0),Q(1,3),Q(2,3)),'three-valued range')
        cases.require(ray._scale(-1).value==ray.value,'negation invariance')
        for factor in (3,5,-3):
            cases.require(ray._scale(factor).value==ray.value,'odd-scaling invariance')


def _verify(cases: Cases,radius: object=6) -> dict[str,int]:
    if type(cases) is not Cases:
        raise Violation('input','per-run Cases recorder required')
    rays=_box(radius)
    frames=_frames(rays,cases)
    key=_congruence(cases)
    _obstruction(cases)
    _values(rays,cases)
    return {'checks':cases.checks,'distinct_box_rays':len(rays),'completed_orthogonal_pairs':frames,'compatible_mod4_tuples':key}


def verify(cases: Cases,radius: object=6) -> Outcome[dict[str,int]]:
    return evaluate(_verify,cases,radius)


def main() -> None:
    print(json.dumps({'status':'passed',**_verify(Cases())},sort_keys=True))


if __name__=='__main__':
    raise SystemExit(cli(main))
