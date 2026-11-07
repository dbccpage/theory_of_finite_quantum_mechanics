"""Temporal-cycle scalar and matrix regression checks. AuthorityEffect: None."""
from __future__ import annotations

import builtins
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType, SimpleNamespace
from typing import Any, TypeVar, cast
import unittest
from unittest.mock import Mock, PropertyMock, patch

from hypothesis import given, settings, strategies as st
import sympy as sp

CHECKS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(CHECKS))
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases
from checker_support.center_orbit import LaurentCenterPolynomial as P
from checker_support.gaussian_expression import decode, encode
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.gaussian_matrix import GaussianMatrix
from checker_support.outcome import Outcome
from checker_support.temporal_cycle import TemporalCycle

APP=CHECKS/'independent/fsp-imaginary-mu-real-det.py'
PROPERTY=settings(max_examples=60,derandomize=True,deadline=None,database=None)
POSITIVE=st.builds(Q,st.integers(1,8),st.integers(1,7))
SCALAR=st.builds(Q,st.integers(-8,8),st.integers(1,7))
T=TypeVar('T')
SMALL_PROPERTY=settings(max_examples=20,derandomize=True,deadline=None,database=None)
ORACLE_FIELD=sp.QQ.algebraic_field(sp.I,sp.sqrt(3))


def load() -> ModuleType:
    spec=importlib.util.spec_from_file_location('reviewed_temporal_cycle',APP)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load temporal-cycle controls')
    module=importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules,{spec.name:module}):
        spec.loader.exec_module(module)
    return module


def rotation(parameter: Q) -> sp.ImmutableMatrix:
    cosine=(1-parameter*parameter)/(1+parameter*parameter)
    sine=2*parameter/(1+parameter*parameter)
    return sp.ImmutableMatrix(((cosine,sine,0),(-sine,cosine,0),(0,0,1)))


def transport_oracle(links: tuple[sp.ImmutableMatrix,...]) -> sp.ImmutableMatrix:
    matrix=sp.zeros(3*len(links))
    for site,link in enumerate(links):
        target=(site+1)%len(links)
        matrix[3*site:3*site+3,3*target:3*target+3]=link if site+1<len(links) else -link
    return sp.ImmutableMatrix(matrix)


def field_value(expression: sp.Expr) -> sp.Expr:
    return ORACLE_FIELD.to_sympy(ORACLE_FIELD.from_sympy(sp.expand_complex(expression).expand()))


class TemporalCycleTests(unittest.TestCase):
    def accepted(self,result: Outcome[T]) -> T:
        self.assertIsNone(result.error)
        return cast(T,result.value)

    def refused(self,result: Outcome[Any],kind: str='input') -> None:
        self.assertIsNotNone(result.error)
        if result.error is None:
            self.fail('Expected typed refusal')
        self.assertEqual(result.error.kind,kind)

    def test_native_and_symbolic_exact_atoms(self) -> None:
        for value in (0,1,-1,2,Q(1,2),sp.Integer(3),sp.Rational(-1,2),sp.I,-sp.I,G(Q(2,3),Q(-1,4))):
            decoded=self.accepted(decode(value))
            self.assertEqual(self.accepted(decode(self.accepted(encode(decoded)))),decoded)
        self.assertEqual(self.accepted(decode(sp.I)),G(0,1))
        self.refused(encode((1,0)))

    def test_text_and_foreign_hooks_are_never_executed(self) -> None:
        probe=Mock(return_value=sp.Integer(3))
        text="__import__('builtins')._tfq_scalar_probe()"
        with patch.object(builtins,'_tfq_scalar_probe',probe,create=True):
            self.refused(decode(text))
            with self.assertRaises(Violation):
                load().gaussian(text)
        probe.assert_not_called()
        hook=Mock(return_value=sp.Integer(3))
        self.refused(decode(SimpleNamespace(_sympy_=hook)))
        hook.assert_not_called()
        for value in (True,False,1.0,complex(1),b'1','1',[1],None):
            self.refused(decode(value))

    @PROPERTY
    @given(POSITIVE,SCALAR,SCALAR,SCALAR,st.integers(-3,3))
    def test_expression_arithmetic_against_symbolic_oracle(self,a: Q,b: Q,c: Q,d: Q,power: int) -> None:
        left=sp.Rational(a.numerator,a.denominator)+sp.I*sp.Rational(b.numerator,b.denominator)
        right=sp.Rational(c.numerator,c.denominator)+sp.I*sp.Rational(d.numerator,d.denominator)
        expressions=(sp.Add(left,right,evaluate=False),sp.Mul(left,right,evaluate=False),
                     sp.Pow(left,power,evaluate=False))
        for expression in expressions:
            actual=self.accepted(encode(self.accepted(decode(expression))))
            self.assertEqual(sp.expand_complex(actual-sp.expand_complex(expression)),0)

    def test_grammar_refusals_and_zero_negative_power(self) -> None:
        expressions=(sp.Symbol('x'),sp.sqrt(2),sp.sin(sp.Integer(1),evaluate=False),sp.Float('0.5'),
                     sp.Pow(1+sp.I,sp.I,evaluate=False),sp.Pow(1+sp.I,sp.Rational(1,2),evaluate=False),
                     sp.Pow(1+sp.I,sp.Add(1,1,evaluate=False),evaluate=False),sp.Pow(0,-1,evaluate=False))
        for expression in expressions:
            self.refused(decode(expression))
        self.assertEqual(self.accepted(decode(sp.Pow(0,0,evaluate=False))),G(1))
        self.assertEqual(self.accepted(decode(sp.Pow(sp.I,-3,evaluate=False))),G(0,1))

    def test_shape_preflight_before_expression_evaluation(self) -> None:
        oversized=sp.Add(*([sp.Integer(1)]*64),evaluate=False)
        invalid=sp.Add(sp.Integer(1),sp.Symbol('x'),evaluate=False)
        with patch.dict(decode.__globals__,_value=Mock(side_effect=RuntimeError('must not evaluate'))):
            self.refused(decode(oversized),'resource')
            self.refused(decode(invalid))

    def test_node_depth_power_and_component_budgets(self) -> None:
        self.assertEqual(self.accepted(decode(sp.Add(*([sp.Integer(1)]*63),evaluate=False))),G(63))
        self.refused(decode(sp.Add(*([sp.Integer(1)]*64),evaluate=False)),'resource')
        expression=sp.I
        for _ in range(9):
            expression=sp.Pow(expression,1,evaluate=False)
        self.refused(decode(expression),'resource')
        for expression in (sp.Pow(1,17,evaluate=False),sp.Pow(1,-17,evaluate=False),
                           sp.Integer(1<<4096),sp.Rational(1,1<<4096),
                           sp.Pow(sp.Integer(1<<2048),2,evaluate=False)):
            self.refused(decode(expression),'resource')
        maximum=(1<<4096)-1
        self.assertEqual(self.accepted(decode(sp.Rational(1,maximum))),G(Q(1,maximum)))
        oversized=(sp.Integer(1<<4096),sp.Rational(1,1<<4096))
        with patch.dict(decode.__globals__,Q=Mock(side_effect=RuntimeError('must not construct Fraction'))):
            for expression in oversized:
                self.refused(decode(expression),'resource')

    def test_owned_values_reentrancy_and_refusal_helper(self) -> None:
        original=G(Q(3,5),Q(4,5))
        decoded=self.accepted(decode(original))
        self.assertEqual(decoded,original)
        self.assertIsNot(decoded,original)
        self.assertEqual(self.accepted(decode(self.accepted(encode(original)))),original)
        with self.assertRaises(FrozenInstanceError):
            decoded.re=Q(0)  # type: ignore[misc]
        with self.assertRaises(AssertionError):
            self.refused(decode(1))

    def test_unexpected_failures_and_cancellation_propagate(self) -> None:
        for exception in (RuntimeError,KeyboardInterrupt,SystemExit):
            with patch.dict(decode.__globals__,_shape=Mock(side_effect=exception)):
                with self.assertRaises(exception):
                    decode(sp.I)

    @PROPERTY
    @given(st.integers(1,4),st.lists(SCALAR,min_size=32,max_size=32))
    def test_gaussian_matrix_determinant_and_adjoint(self,size: int,values: list[Q]) -> None:
        rows=tuple(tuple(G(values[2*(i*size+j)],values[2*(i*size+j)+1]) for j in range(size))
                   for i in range(size))
        matrix=GaussianMatrix(rows)
        symbolic=matrix.to_sympy()
        actual=self.accepted(encode(self.accepted(matrix.determinant_result())))
        self.assertEqual(sp.expand(actual-symbolic.det(method='domain-ge')),0)
        self.assertEqual(matrix.adjoint().to_sympy(),symbolic.H)
        self.assertEqual(matrix.rows,rows)
        self.assertEqual(GaussianMatrix.from_sympy(symbolic),matrix)

    @PROPERTY
    @given(st.lists(SCALAR,min_size=16,max_size=16))
    def test_gaussian_matrix_products_and_scaling(self,values: list[Q]) -> None:
        left=GaussianMatrix(tuple(tuple(G(values[2*(i*2+j)],values[2*(i*2+j)+1]) for j in range(2)) for i in range(2)))
        right=GaussianMatrix(tuple(tuple(G(values[8+2*(i*2+j)],values[9+2*(i*2+j)]) for j in range(2)) for i in range(2)))
        symbolic_left,symbolic_right=left.to_sympy(),right.to_sympy()
        self.assertEqual((left.mul(right).to_sympy()-symbolic_left*symbolic_right).applyfunc(sp.expand),sp.zeros(2))
        self.assertEqual(left.add(right).to_sympy(),symbolic_left+symbolic_right)
        self.assertEqual((left.scale(sp.I).to_sympy()-sp.I*symbolic_left).applyfunc(sp.expand),sp.zeros(2))
        self.assertEqual((left.neg().to_sympy()+symbolic_left).applyfunc(sp.expand),sp.zeros(2))

    def test_gaussian_matrix_shape_domain_preflight(self) -> None:
        from checker_support.boundary import evaluate
        invalid: object
        for invalid in (None,[],[[]],[[1],[1,2]],[[True]],[[1.0]],[["1"]]):
            self.refused(evaluate(GaussianMatrix,invalid))
        for invalid_budget in ([[1]]*19,[[1]*19],[[1<<4096]]):
            self.refused(evaluate(GaussianMatrix,invalid_budget),'resource')
        with patch.dict(GaussianMatrix.__init__.__globals__,_decode=Mock(side_effect=RuntimeError)):
            self.refused(evaluate(GaussianMatrix,[[1],[1,2]]))
        for foreign in (sp.eye(2),None,[[1]]):
            self.refused(evaluate(GaussianMatrix.from_sympy,foreign))
        self.refused(evaluate(GaussianMatrix.from_sympy,sp.ImmutableMatrix(sp.eye(19))),'resource')

    def test_gaussian_matrix_boundaries_and_ownership(self) -> None:
        from checker_support.boundary import evaluate
        rows=[[1,2],[3,4]]
        matrix=GaussianMatrix(rows)
        rows[0][0]=9
        self.assertEqual(matrix.rows[0][0],G(1))
        with self.assertRaises(FrozenInstanceError):
            matrix.rows=()  # type: ignore[misc]
        self.assertEqual(self.accepted(GaussianMatrix.eye(18).determinant_result()),G(1))
        for size in (True,0,1.0):
            self.refused(evaluate(GaussianMatrix.eye,size))
        self.refused(evaluate(GaussianMatrix.eye,19),'resource')
        self.refused(evaluate(matrix.mul,[]))
        self.refused(evaluate(matrix.mul,GaussianMatrix(((1,),))))
        self.refused(evaluate(matrix.add,GaussianMatrix(((1,),))))
        self.refused(GaussianMatrix(((1,2),)).determinant_result())

    def test_gaussian_matrix_intermediate_budget_cancellation(self) -> None:
        from checker_support.boundary import evaluate
        maximum=(1<<4096)-1
        term=GaussianMatrix(((maximum,maximum),))
        self.refused(evaluate(term.mul,GaussianMatrix(((2,),(-2,)))),'resource')
        prefix=GaussianMatrix(((maximum,maximum,maximum),))
        self.refused(evaluate(prefix.mul,GaussianMatrix(((1,),(1,),(-1,)))),'resource')
        imaginary_prefix=GaussianMatrix(((G(0,maximum),G(0,maximum),G(0,maximum)),))
        self.refused(evaluate(imaginary_prefix.mul,GaussianMatrix(((1,),(1,),(-1,)))),'resource')
        for rows in (((maximum,0),(0,2)),((Q(1,maximum),0),(maximum,1)),
                     ((Q(1,2),-maximum,0),(Q(1,2),maximum,1),(0,0,Q(1,2))),
                     ((maximum,0,0),(0,2,0),(0,0,Q(1,2)))):
            self.refused(GaussianMatrix(rows).determinant_result(),'resource')
        self.assertEqual(self.accepted(GaussianMatrix(((maximum,),)).determinant_result()),G(maximum))

    def test_gaussian_matrix_pivots_and_complex_phase(self) -> None:
        complex_matrix=GaussianMatrix(((sp.I,1+sp.I),(0,2-sp.I)))
        self.assertEqual(complex_matrix.adjoint().rows,((G(0,-1),G(0)),(G(1,-1),G(2,1))))
        for rows,expected in ((((0,1),(1,0)),G(-1)),(((1,1),(1,1)),G(0)),
                              (((sp.I,0),(0,1)),G(0,1)),(((2+sp.I,1),(1,3)),G(5,3))):
            self.assertEqual(self.accepted(GaussianMatrix(rows).determinant_result()),expected)

    @SMALL_PROPERTY
    @given(st.sampled_from((2,4,6)),SCALAR,SCALAR,st.sampled_from((1,2,sp.I,sp.Rational(3,5)+4*sp.I/5)))
    def test_cycle_transport_and_dirac_against_block_oracle(self,sites: int,parameter: Q,mass: Q,z: object) -> None:
        phase=sp.ImmutableMatrix(sp.diag(sp.I,sp.I,-1))
        real_rotation=rotation(parameter)
        links=tuple(real_rotation if i%2 else phase*real_rotation for i in range(sites))
        cycle=TemporalCycle(links)
        expected=transport_oracle(links)
        self.assertEqual((cycle.transport()-expected).applyfunc(sp.expand),sp.zeros(3*sites))
        self.assertEqual(self.accepted(cycle.transport_result()).to_sympy(),cycle.transport())
        activity=self.accepted(encode(self.accepted(decode(z))))
        expected_dirac=mass*sp.eye(3*sites)+(activity*expected-expected.H/activity)/2
        actual=self.accepted(cycle.dirac_result(mass,z)).to_sympy()
        self.assertEqual((actual-expected_dirac).applyfunc(sp.expand),sp.zeros(3*sites))
        self.assertEqual(cycle.dirac(mass,z),actual)
        self.assertEqual(cycle.sites,sites)

    def test_cycle_input_domains_preflight_and_immutable_state(self) -> None:
        identity=sp.ImmutableMatrix(sp.eye(3))
        for invalid in ([identity,identity],(),(identity,)*3,(2*identity,identity),(-identity,identity),
                        (sp.ImmutableMatrix(sp.diag(2,sp.Rational(1,2),1)),identity),
                        (sp.eye(3),identity),(sp.ImmutableMatrix(sp.eye(2)),identity)):
            self.refused(evaluate(TemporalCycle,invalid))
        self.refused(evaluate(TemporalCycle,(identity,)*8),'resource')
        with patch.object(GaussianMatrix,'mul',side_effect=RuntimeError('must not multiply')):
            self.refused(evaluate(TemporalCycle,(identity,sp.ImmutableMatrix(sp.eye(2)))))
        cycle=TemporalCycle((identity,identity))
        for mass,z in ((sp.I,1),(True,1),(1.0,1),(1,0),(1,'1')):
            self.refused(cycle.dirac_result(mass,z))
        mutable=cycle.transport().as_mutable()
        mutable[0,0]=9
        self.assertEqual(cycle.transport()[0,0],0)
        self.assertEqual(cycle.links,(identity,identity))
        self.assertEqual(cycle.dirac(1,1),cycle.dirac(1,1))
        with self.assertRaises(FrozenInstanceError):
            cycle._links=()  # type: ignore[misc]

    def test_fixed_cycle_hopping_scale_and_activity(self) -> None:
        identity=sp.ImmutableMatrix(sp.eye(3))
        cycle=TemporalCycle((identity,identity))
        unit=self.accepted(cycle.dirac_result(1,1))
        self.assertEqual((unit.rows[0][0],unit.rows[0][3],unit.rows[3][0]),(G(1),G(1),G(-1)))
        self.assertEqual(self.accepted(unit.determinant_result()),G(8))
        nonunit=self.accepted(cycle.dirac_result(1,2))
        self.assertEqual((nonunit.rows[0][3],nonunit.rows[3][0]),(G(Q(5,4)),G(Q(-5,4))))
        singular=self.accepted(cycle.dirac_result(0,sp.I))
        self.assertEqual(singular,GaussianMatrix(((0,)*6,)*6))

    @SMALL_PROPERTY
    @given(st.lists(SCALAR,min_size=14,max_size=14))
    def test_center_projection_and_values_against_root_sum(self,values: list[Q]) -> None:
        coefficients=tuple(G(values[2*i],values[2*i+1]) for i in range(7))
        polynomial=P(coefficients)
        t=sp.Symbol('t',nonzero=True)
        expression=sum((sp.Rational(v.re.numerator,v.re.denominator)+sp.I*sp.Rational(v.im.numerator,v.im.denominator))*t**(i-3)
                       for i,v in enumerate(coefficients))
        self.assertEqual(sp.expand(polynomial.expression()-expression),0)
        centered=self.accepted(polynomial.center())
        expected=tuple(value.mul(G(3)) if (i-3)%3==0 else G(0) for i,value in enumerate(coefficients))
        self.assertEqual(centered.coefficients,expected)
        omega=(-1+sp.sqrt(3)*sp.I)/2
        roots=(sp.Integer(1),omega,sp.conjugate(omega))
        expected_sum=field_value(sum(expression.subs(t,root) for root in roots))
        for k,root in enumerate(roots):
            self.assertEqual(self.accepted(polynomial.evaluate(k)),field_value(expression.subs(t,root)))
            self.assertEqual(self.accepted(centered.evaluate(k)),expected_sum)

    def test_boundary_polynomial_against_full_six_by_six_determinant(self) -> None:
        t=sp.Symbol('t',nonzero=True)
        identity=sp.ImmutableMatrix(sp.eye(3))
        phase=sp.ImmutableMatrix(sp.diag(sp.I,sp.I,-1))
        for link in (identity,phase,rotation(Q(1,2)),phase*rotation(Q(2,3))):
            polynomial=self.accepted(P.from_boundary(GaussianMatrix.from_sympy(link)))
            forward=sp.BlockMatrix([[sp.zeros(3),sp.eye(3)],[-t*link,sp.zeros(3)]]).as_explicit()
            backward=sp.BlockMatrix([[sp.zeros(3),-link.H/t],[sp.eye(3),sp.zeros(3)]]).as_explicit()
            expected=(sp.eye(6)+(forward-backward)/2).det(method='domain-ge')
            self.assertEqual(sp.cancel(polynomial.expression()-expected),0)

    def test_center_domains_budgets_and_reentrancy(self) -> None:
        invalid: object
        for invalid in (None,(),(0,)*6,(True,)*7,(1.0,)*7):
            self.refused(evaluate(P,invalid))
        self.refused(evaluate(P,(0,)*8),'resource')
        polynomial=P((0,0,0,1,0,0,0))
        for operation in (polynomial.add,polynomial.mul):
            self.refused(evaluate(operation,None))
        with patch.dict(P.__init__.__globals__,_decode=Mock(side_effect=RuntimeError('must not decode'))):
            self.refused(evaluate(P,(0,)*6))
        for invalid in (True,-1,1.0,sp.Integer(1)):
            self.refused(polynomial.evaluate(invalid))
        self.refused(polynomial.evaluate(3),'resource')
        self.refused(P.from_boundary(None))
        self.refused(P.from_boundary(GaussianMatrix.eye(2)))
        self.refused(P.from_boundary(GaussianMatrix(((2,0,0),(0,1,0),(0,0,1)))))
        self.refused(P.from_boundary(GaussianMatrix(((2,0,0),(0,Q(1,2),0),(0,0,1)))))
        self.refused(P.from_boundary(GaussianMatrix(((-1,0,0),(0,-1,0),(0,0,-1)))))
        maximum=(1<<4096)-1
        huge=P((0,0,0,maximum,0,0,0))
        self.refused(huge.center(),'resource')
        self.refused(evaluate(huge.scale,2),'resource')
        self.refused(evaluate(huge.add,huge),'resource')
        self.refused(P((maximum,0,0,maximum,0,0,-maximum)).evaluate(0),'resource')
        self.refused(P((0,0,0,G(0,Q(1,maximum)),0,0,0)).evaluate(0),'resource')
        self.refused(evaluate(P((0,0,0,0,0,0,1)).mul,P((0,0,0,0,1,0,0))),'resource')
        self.assertEqual(P((0,)*7).mul(P((0,0,0,0,0,0,1))).coefficients,(G(0),)*7)
        self.assertEqual(self.accepted(polynomial.evaluate(1)),self.accepted(polynomial.evaluate(1)))
        coefficients=[0,0,0,1,0,0,0]
        owned=P(coefficients)
        coefficients[3]=9
        self.assertEqual(owned.coefficients[3],G(1))
        with self.assertRaises(FrozenInstanceError):
            owned.coefficients=()  # type: ignore[misc]

    def test_center_basis_phases_and_convolution(self) -> None:
        fractional=P((0,0,0,G(Q(1,2),Q(2,3)),0,0,0))
        self.assertEqual(self.accepted(fractional.evaluate(0)),field_value(sp.Rational(1,2)+2*sp.I/3))
        omega=(-1+sp.sqrt(3)*sp.I)/2
        for i in range(7):
            entries=[G(0) for _ in range(7)]
            entries[i]=G(1,2)
            polynomial=P(entries)
            for k in range(3):
                expected=field_value((1+2*sp.I)*omega**((i-3)*k))
                self.assertEqual(self.accepted(polynomial.evaluate(k)),expected)
            expected_coefficients=tuple(value.mul(G(3)) if (j-3)%3==0 else G(0) for j,value in enumerate(entries))
            self.assertEqual(self.accepted(polynomial.center()).coefficients,expected_coefficients)
        left=P((0,0,G(1,1),2,G(0,-1),0,0))
        right=P((0,0,3,G(0,1),-2,0,0))
        self.assertEqual(sp.expand(left.mul(right).expression()-left.expression()*right.expression()),0)
        self.assertEqual(sp.expand(left.add(right).expression()-left.expression()-right.expression()),0)
        self.assertEqual(sp.expand(left.scale(sp.I).expression()-sp.I*left.expression()),0)

    def test_application_original_payload_and_live_case_counter(self) -> None:
        controls=load().ImaginaryMuControls()
        observed: list[str]=[]
        original=Cases.require
        def record(cases: Cases,condition: bool,message: str) -> None:
            observed.append(message)
            original(cases,condition,message)
        with patch.object(Cases,'require',record):
            result=self.accepted(controls.verify())
        self.assertEqual(result['checks'],140)
        self.assertEqual(result['checks'],len(observed))
        self.assertEqual(observed.count('native determinant differs'),27)
        baseline=CHECKS/'review_ledger/2026-11-05-temporal-cycle-initial-review.json'
        expected=json.loads(json.loads(baseline.read_bytes())['runs'][0]['stdout'])
        self.assertEqual(result['payload'],expected)
        self.assertEqual(self.accepted(controls.verify()),result)
        with patch.object(Cases,'checks',new_callable=PropertyMock,return_value=907):
            self.assertEqual(self.accepted(controls.verify())['checks'],907)
        with self.assertRaises(FrozenInstanceError):
            controls.cycles=()

    def test_legacy_booleans_matrix_comparison_and_rejection_adapters(self) -> None:
        module=load()
        for condition in (True,sp.true):
            module.require(condition,'admitted true condition')
        for condition in (False,sp.false):
            self.refused(evaluate(module.require,condition,'false condition'),'check')
        for invalid in (1,'true',sp.Symbol('x')):
            self.refused(evaluate(module.require,invalid,'invalid condition'))
        self.assertTrue(module.equal_matrix(sp.eye(2),sp.ImmutableMatrix(sp.eye(2))))
        self.assertFalse(self.accepted(module.matrix_equal(sp.eye(2),-sp.eye(2))))
        self.refused(module.matrix_equal(None,sp.eye(2)))
        oversized=sp.eye(19)
        with patch.object(module.s,'ImmutableMatrix',side_effect=RuntimeError('must not copy')):
            self.refused(module.matrix_equal(oversized,oversized),'resource')
        self.refused(evaluate(module.expect_rejection,'not callable',None))
        self.refused(evaluate(module.expect_rejection,'accepted',lambda:1),'check')
        self.refused(evaluate(module.expect_rejection,'wrong refusal',lambda:(_ for _ in ()).throw(Violation('check','injected'))),'check')

    def test_application_failure_translation_and_cancellation(self) -> None:
        module=load()
        controls=module.ImaginaryMuControls()
        with patch.object(GaussianMatrix,'determinant',return_value=G(0)):
            self.refused(controls.verify(),'check')
        with patch.object(TemporalCycle,'_dirac',side_effect=Violation('resource','injected')):
            self.refused(controls.verify(),'resource')
            with contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(module.main(),1)
            self.assertEqual(json.loads(output.getvalue())['kind'],'resource')
        for exception in (RuntimeError,KeyboardInterrupt,SystemExit):
            with patch.object(TemporalCycle,'_dirac',side_effect=exception):
                with self.assertRaises(exception):
                    controls.verify()
                with self.assertRaises(exception):
                    controls.cycles[0].dirac_result(1,1)

    def test_quiet_import_and_original_cli(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            module=load()
        self.assertEqual(output.getvalue(),'')
        baseline=CHECKS/'review_ledger/2026-11-05-temporal-cycle-initial-review.json'
        expected=json.loads(baseline.read_bytes())['runs'][0]['stdout']
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(module.main(),0)
        self.assertEqual(output.getvalue(),expected)
        result=subprocess.run([sys.executable,'-I','-B','-X','utf8',str(APP)],capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout,expected)


if __name__=='__main__':
    unittest.main()
