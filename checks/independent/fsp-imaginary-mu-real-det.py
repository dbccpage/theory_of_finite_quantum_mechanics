"""Finite imaginary-fugacity matrix audit. AuthorityEffect: None.

The model is a one-dimensional even temporal cycle, three colors,
antiperiodic fermions and an unrooted determinant. Ordinary matrix witnesses
lie in Q(i); the declared center orbit lies in Q(i,sqrt(3)).
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import cast
import sympy as s

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate, require as _require
from checker_support.cases import Cases
from checker_support.domains import integer
from checker_support.center_orbit import LaurentCenterPolynomial
from checker_support.gaussian_expression import _decode, _encode
from checker_support.gaussian_matrix import GaussianMatrix as M
from checker_support.outcome import Outcome
from checker_support.temporal_cycle import TemporalCycle


def _condition(value: object) -> bool:
    if type(value) is bool:
        return value
    if value is s.true:
        return True
    if value is s.false:
        return False
    raise Violation("input","verification condition requires an exact boolean")


def require(condition: object,message: str) -> None:
    _require(_condition(condition),message)


def _guard(cases: Cases,condition: object,message: str) -> None:
    cases.require(_condition(condition),message)


def gaussian(value: object) -> s.Expr:
    return _encode(_decode(value))


def _matrix(value: object) -> M:
    if type(value) is M:
        return value
    if type(value) not in (s.MutableDenseMatrix,s.ImmutableDenseMatrix):
        raise Violation("input","matrix comparison requires a dense exact matrix")
    matrix=cast(s.MatrixBase,value)
    integer(matrix.rows,"comparison rows",1,18)
    integer(matrix.cols,"comparison columns",1,18)
    return M.from_sympy(s.ImmutableMatrix(matrix))


def equal_matrix(left: object,right: object) -> bool:
    return _matrix(left)==_matrix(right)


def matrix_equal(left: object,right: object) -> Outcome[bool]:
    return evaluate(equal_matrix,left,right)


def expect_rejection(name: str,operation: Callable[[],object]) -> str:
    if not callable(operation):
        raise Violation("input","rejection probe requires a callable")
    result=evaluate(operation)
    if result.error is None:
        raise Violation("check","invalid input accepted: "+name)
    if result.error.kind not in ("input","resource"):
        raise Violation("check","rejection probe did not produce a domain refusal: "+name)
    return name


@dataclass(frozen=True,slots=True,init=False)
class ImaginaryMuControls:
    """Owns the three declared cycles and fixed boundary; counters are per run."""
    cycles: tuple[TemporalCycle,...]
    identity: M
    boundary: M

    def __init__(self) -> None:
        identity=s.ImmutableMatrix(s.eye(3))
        phase=s.ImmutableMatrix(s.diag(s.I,s.I,-1))
        rotation=s.ImmutableMatrix([[s.Rational(3,5),s.Rational(4,5),0],
                                    [-s.Rational(4,5),s.Rational(3,5),0],[0,0,1]])
        links=(phase,rotation,identity,phase*rotation)
        cycles=tuple(TemporalCycle(tuple(links[j%len(links)] for j in range(n))) for n in (2,4,6))
        object.__setattr__(self,"cycles",cycles)
        object.__setattr__(self,"identity",M.from_sympy(identity))
        object.__setattr__(self,"boundary",M.from_sympy(phase))

    def _case(self,lattice: TemporalCycle,mass: s.Expr,z: s.Expr,
              rows: list[dict[str,object]],cases: Cases) -> None:
        n=lattice.sites
        native=lattice._dirac(mass,z)
        d=native.to_sympy()
        gamma=s.diag(*[(-1)**(j//3) for j in range(3*n)])
        _guard(cases,equal_matrix(gamma*d*gamma,d.H),"adjoint identity failed")
        det=s.expand(d.det(method="domain-ge"))
        _guard(cases,det.is_Rational is True and det>=0,"determinant is not nonnegative")
        _guard(cases,s.expand(_encode(native.determinant())-det)==0,"native determinant differs")
        if mass>0:
            _guard(cases,det>0,"positive-mass determinant is not positive")
        even=[3*x+c for x in range(n) if x%2==0 for c in range(3)]
        odd=[3*x+c for x in range(n) if x%2==1 for c in range(3)]
        x=d.extract(even,odd)
        if mass>0:
            gram=mass*s.eye(len(odd))+x.H*x/mass
            schur=mass**len(even)*gram.det(method="domain-ge")
            _guard(cases,s.expand(schur-det)==0,"independent Schur determinant differs")
        if n==2 and mass==1:
            rows.append({"sites":n,"mass":str(mass),"z":str(z),"det":str(det)})

    def _lattices(self,cases: Cases,rows: list[dict[str,object]]) -> int:
        population=0
        for lattice in self.cycles:
            n=lattice.sites
            t=lattice.transport()
            gamma=s.diag(*[(-1)**(j//3) for j in range(3*n)])
            _guard(cases,equal_matrix(gamma*t*gamma,-t),"cycle is not bipartite")
            for z in (s.Integer(1),s.I,s.Rational(3,5)+s.Rational(4,5)*s.I):
                for mass in (s.Integer(0),s.Rational(1,3),s.Integer(1)):
                    self._case(lattice,mass,z,rows,cases)
                    population+=1
        return population

    def _witnesses(self,cases: Cases) -> s.Expr:
        identity=self.identity.to_sympy()
        phase=self.boundary.to_sympy()
        g,negative=s.diag(1,-1),s.diag(-1,1)
        _guard(cases,g*g==s.eye(2) and g*negative*g==negative.H,"negative witness symmetry")
        _guard(cases,negative.det()==-1 and s.diag(negative,negative).det()==1,"single/two-flavor witness")
        zero=TemporalCycle((identity,identity)).dirac(s.Integer(0),s.I)
        _guard(cases,zero.det()==0,"zero-mass witness should be singular")
        real_mu=TemporalCycle((identity,phase)).dirac(s.Integer(1),s.Integer(2))
        g6=s.diag(1,1,1,-1,-1,-1)
        _guard(cases,not equal_matrix(g6*real_mu*g6,real_mu.H),"nonunit fugacity guard is essential")
        determinant=s.expand(real_mu.det())
        _guard(cases,s.im(determinant)!=0,"real-mu complex determinant witness")
        return determinant

    def _center(self,cases: Cases) -> tuple[s.Expr,s.Expr]:
        polynomial_value=LaurentCenterPolynomial._from_boundary(self.boundary)
        centered=polynomial_value._center()
        polynomial=polynomial_value.expression()
        center=centered.expression()
        t=s.Symbol("t",nonzero=True)
        omega=(-1+s.sqrt(3)*s.I)/2
        field=s.QQ.algebraic_field(s.I,s.sqrt(3))
        def canonical(value: s.Expr) -> s.Expr:
            return field.to_sympy(field.from_sympy(s.expand(value)))
        _guard(cases,canonical(omega**3)==1,"center root order")
        independent=s.expand(sum(polynomial.subs(t,omega**k*t) for k in range(3)))
        difference=s.Poly(s.cancel(t**3*(center-independent),extension=(s.I,s.sqrt(3))),t)
        _guard(cases,all(canonical(c)==0 for c in difference.all_coeffs()),"independent center sum differs")
        residual=s.Poly(s.expand(t**3*(center.subs(t,omega*t)-center)),t)
        _guard(cases,all(canonical(c)==0 for c in residual.all_coeffs()),"center-orbit periodicity")
        zsum=canonical(center.subs(t,1))
        zshift=canonical(center.subs(t,omega))
        _guard(cases,zsum==zshift and zsum>0,"center orbit positive equal values")
        _guard(cases,all(centered._evaluate(k)==zsum for k in range(3)),"owned center evaluations differ")
        _guard(cases,canonical(polynomial.subs(t,1)-polynomial.subs(t,omega))!=0,
               "fixed-background counterexample to inferred RW periodicity")
        return polynomial,zsum

    def _rejected(self,cases: Cases) -> list[str]:
        identity=self.identity.to_sympy()
        probes: tuple[tuple[str,Callable[[],object]],...]=(
            ("odd cycle",lambda:TemporalCycle((identity,)*3)),
            ("oversize cycle",lambda:TemporalCycle((identity,)*8)),
            ("mutable links",lambda:TemporalCycle([identity,identity])),
            ("nonunitary link",lambda:TemporalCycle((2*identity,identity))),
            ("wrong determinant",lambda:TemporalCycle((-identity,identity))),
            ("zero fugacity",lambda:TemporalCycle((identity,)*2).dirac(1,0)),
            ("nonreal mass",lambda:TemporalCycle((identity,)*2).dirac(s.I,1)),
            ("float entry",lambda:gaussian(s.Float("0.5"))),
            ("boolean entry",lambda:gaussian(True)))
        rejected=[]
        for name,operation in probes:
            rejection=expect_rejection(name,operation)
            _guard(cases,rejection==name,"expected domain refusal: "+name)
            rejected.append(rejection)
        return rejected

    def _verify(self) -> dict[str,object]:
        cases=Cases()
        rows: list[dict[str,object]]=[]
        population=self._lattices(cases,rows)
        real_mu=self._witnesses(cases)
        polynomial,zsum=self._center(cases)
        rejected=self._rejected(cases)
        payload={"schema_version":"campaign_independent.v1","AuthorityEffect":"None",
                 "node":"FSP-IMAGINARY-MU-REAL-DET","field":"Q(i); Q(zeta_12) for center orbit",
                 "lattice_cases":population,"determinant_examples":rows,
                 "gamma_only_determinant":"-1","zero_mass_determinant":"0",
                 "real_fugacity_determinant":str(real_mu),"boundary_polynomial":str(polynomial),
                 "center_sum_at_one":str(zsum),"rejected_inputs":rejected,"result":"PASS",
                 "scope":"Finite 1D cycles; finite center-orbit sum, not a QCD measure or continuation."}
        return {"payload":payload,"checks":cases.checks,"failures":0}

    def verify(self) -> Outcome[dict[str,object]]:
        return evaluate(self._verify)


def _main() -> None:
    print(json.dumps(ImaginaryMuControls()._verify()["payload"],indent=2))


def main() -> int:
    return cli(_main)


if __name__=="__main__":
    raise SystemExit(main())
