"""Exact finite Hubbard pairing and witness audit. AuthorityEffect: None.

The original 64 attractive fields, 256 half-filled fields and both negative
witnesses are retained. This checks the declared transfer representation;
the cited Lean module proves only arithmetic consequences of supplied pairs.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import sys
import sympy as sp
from sympy import Rational

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from checker_support.bond_graph import BondGraph
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import rational
from checker_support.hubbard_determinants import HubbardDeterminants
from checker_support.hubbard_transfer import HubbardTransfer
from checker_support.outcome import Outcome


def _exact(value: object) -> Q:
    if isinstance(value,sp.Rational):
        numerator=rational(int(value.p),"symbolic numerator")
        denominator=rational(int(value.q),"symbolic denominator")
        value=numerator/denominator
    return rational(value)


def validate_bonds(sites: object,bonds: object) -> list[tuple[int,int]]:
    """Legacy snapshot adapter; expected refusals remain ValueError subclasses."""
    return list(BondGraph(sites,bonds).bonds)


def kinetic_matrix(sites: object,bonds: object,r: object) -> sp.Matrix:
    model=HubbardTransfer(BondGraph(sites,bonds),1,_exact(r),Q(1),Q(1))
    return sp.Matrix(model.kinetic.rows)


def _values(result: HubbardDeterminants) -> tuple[sp.Rational,sp.Rational,sp.Rational,int]:
    return Rational(result.d_up.numerator,result.d_up.denominator), \
           Rational(result.d_down.numerator,result.d_down.denominator), \
           Rational(result.weight.numerator,result.weight.denominator),result.total_s


def _field(model: HubbardTransfer,mask: object) -> tuple[sp.Rational,sp.Rational,sp.Rational,int]:
    return _values(model._determinants(mask))


def compute_hubbard_determinants(sites: object,bonds: object,slices: object,r: object,hs: object,
                               fugacity: object,mask: object,attractive: object=False
                               ) -> tuple[sp.Rational,sp.Rational,sp.Rational,int]:
    model=HubbardTransfer(BondGraph(sites,bonds),slices,_exact(r),_exact(hs),_exact(fugacity),attractive)
    return _field(model,mask)


@dataclass(frozen=True,slots=True,init=False)
class HubbardControls:
    """Owns the four declared finite models; no shared mutable census state."""
    attractive: HubbardTransfer
    half_filled: HubbardTransfer
    doped: HubbardTransfer
    triangle: HubbardTransfer

    def __init__(self) -> None:
        triangle=BondGraph(3,((0,1),(1,2),(0,2)))
        ring=BondGraph(4,((0,1),(1,2),(2,3),(0,3)))
        object.__setattr__(self,"attractive",HubbardTransfer(triangle,2,Q(3,2),Q(2),Q(3,2),True))
        object.__setattr__(self,"half_filled",HubbardTransfer(ring,2,Q(3,2),Q(2),Q(1)))
        object.__setattr__(self,"doped",HubbardTransfer(ring,4,Q(2),Q(8),Q(2)))
        object.__setattr__(self,"triangle",HubbardTransfer(triangle,4,Q(2),Q(8),Q(1)))

    def _attractive(self, cases: Cases, emit: bool) -> None:
        if emit:
            print('\n[1/4] Verifying attractive spin-balanced pairing across all 64 fields (triangle, 2 slices, z=3/2, hs=2, r=3/2)...')
        for mask in range(64):
            d_up, d_down, w, s = _field(self.attractive, mask)
            cases.require(bool(d_up == d_down), f'Attractive spin pairing failed at mask {mask}: {d_up} != {d_down}')
            cases.require(bool(w >= 0), f'Attractive weight negative at mask {mask}: {w} < 0')
        if emit:
            print('  ✓ All 64 fields satisfy d_up == d_down and W(s) >= 0.')

    def _half_filled(self, cases: Cases, emit: bool) -> None:
        if emit:
            print('\n[2/4] Verifying half-filled bipartite pairing across all 256 fields (4-site ring, 2 slices, z=1, hs=2, r=3/2)...')
        for mask in range(256):
            d_up, d_down, w, s = _field(self.half_filled, mask)
            expected_d_down = d_up / Rational(2) ** s
            cases.require(bool(d_down == expected_d_down), f'Half-filled pairing relation failed at mask {mask}: {d_down} != {expected_d_down}')
            cases.require(bool(w >= 0), f'Half-filled weight negative at mask {mask}: {w} < 0')
        if emit:
            print('  ✓ All 256 fields satisfy d_down == d_up / h^(sum s) and W(s) >= 0.')

    def _doped(self, cases: Cases, emit: bool) -> None:
        if emit:
            print('\n[3/4] Recomputing negative determinant witness 1: Doped 4-site ring (mask 15721)...')
        d_up1, d_down1, w1, s1 = _field(self.doped, 15721)
        expected_up1 = Rational(11072073737867929807204939234025, 2305843009213693952)
        expected_down1 = Rational(-1034021712177776419381618902295, 147573952589676412928)
        cases.require(bool(d_up1 == expected_up1), f'd_up mismatch: {d_up1} != {expected_up1}')
        cases.require(bool(d_down1 == expected_down1), f'd_down mismatch: {d_down1} != {expected_down1}')
        expected_w1 = Rational(-11448764643788789633389299083665210593647227349065798614587375, 340282366920938463463374607431768211456)
        cases.require(bool(w1 == d_up1 * d_down1 == expected_w1), f'W mismatch: {w1} != {expected_w1}')
        cases.require(bool(340282366920938463463374607431768211456 == 2 ** 128), 'exact witness denominator')
        cases.require(bool((d_up1.q, d_down1.q, w1.q) == (2 ** 61, 2 ** 67, 2 ** 128)), 'denominators of the ring witness')
        cases.require(bool(d_up1 > 0), 'd_up must be strictly positive')
        cases.require(bool(d_down1 < 0), 'd_down must be strictly negative')
        cases.require(bool(w1 < 0), 'determinant product weight must be strictly negative')
        cases.require(bool(d_down1 != d_up1 / Rational(8) ** s1), 'pairing relation unexpectedly holds at z=2')
        d_up1h, d_down1h, w1h, _ = _field(HubbardTransfer(self.doped.graph, 4, Q(2), Q(8), Q(1)), 15721)
        cases.require(bool(d_down1h == d_up1h / Rational(8) ** s1 and w1h >= 0), 'mask 15721 at z=1 must satisfy the pairing relation')
        if emit:
            print(f'  d_up   = {d_up1} > 0')
        if emit:
            print(f'  d_down = {d_down1} < 0')
        if emit:
            print(f'  W(15721) = {w1} < 0')
        if emit:
            print('  ✓ Witness 1 verified: strictly negative determinant weight outside half-filling protection.')

    def _triangle(self, cases: Cases, emit: bool) -> None:
        if emit:
            print('\n[4/4] Recomputing negative determinant witness 2: Frustrated 3-site triangle (mask 1281)...')
        d_up2, d_down2, w2, s2 = _field(self.triangle, 1281)
        expected_up2 = Rational(2661572208368287551525625, 9223372036854775808)
        expected_down2 = Rational(-323903084369592224375, 35184372088832)
        cases.require(bool(d_up2 == expected_up2), f'd_up mismatch: {d_up2} != {expected_up2}')
        cases.require(bool(d_down2 == expected_down2), f'd_down mismatch: {d_down2} != {expected_down2}')
        expected_w2 = Rational(-862091447562875338563475227905478168562109375, 324518553658426726783156020576256)
        cases.require(bool(w2 == d_up2 * d_down2 == expected_w2), f'W mismatch: {w2} != {expected_w2}')
        cases.require(bool(324518553658426726783156020576256 == 2 ** 108), 'exact witness denominator')
        cases.require(bool((d_up2.q, d_down2.q, w2.q) == (2 ** 63, 2 ** 45, 2 ** 108)), 'denominators of the triangle witness')
        cases.require(bool(d_up2 > 0), 'd_up must be strictly positive')
        cases.require(bool(d_down2 < 0), 'd_down must be strictly negative')
        cases.require(bool(w2 < 0), 'determinant product weight must be strictly negative')
        cases.require(bool(d_down2 != d_up2 / Rational(8) ** s2), 'pairing relation unexpectedly holds on the triangle')
        if emit:
            print(f'  d_up   = {d_up2} > 0')
        if emit:
            print(f'  d_down = {d_down2} < 0')
        if emit:
            print(f'  W(1281)  = {w2} < 0')
        if emit:
            print('  ✓ Witness 2 verified: strictly negative determinant weight outside bipartite protection.')

    def _verify(self,emit: bool=False) -> dict[str,object]:
        cases=Cases()
        if emit:
            print("=== Running Independent Check for FSP-HUBBARD-PROTECTED-REPRESENTATIONS ===")
        self._attractive(cases,emit)
        self._half_filled(cases,emit)
        self._doped(cases,emit)
        self._triangle(cases,emit)
        if emit:
            print("\n=== All independent checks passed successfully! ===")
        return {"attractive_fields":64,"half_filled_fields":256,"negative_witnesses":2,
                "checks":cases.checks,"failures":0}

    def verify(self) -> Outcome[dict[str,object]]:
        return evaluate(self._verify)


def _main() -> None:
    HubbardControls()._verify(True)


def main() -> int:
    return cli(_main)


if __name__=="__main__":
    raise SystemExit(main())
