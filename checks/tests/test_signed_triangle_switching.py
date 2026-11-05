"""Independent matrix and Boolean switching oracles. AuthorityEffect: None."""
from __future__ import annotations

import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import importlib.util
import io
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import TypeVar, cast
import unittest
from unittest.mock import Mock, patch

from hypothesis import given, settings, strategies as st
import sympy as sp

CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix
from checker_support.signed_triangle import SignedTriangle

APP=CHECKS/"independent/fsp-cobordism-intrinsic-sign.py"
PROPERTY=settings(max_examples=80,derandomize=True,deadline=None,database=None)
MATRIX=st.lists(st.integers(-100,100),min_size=9,max_size=9)
T=TypeVar("T")


def load() -> ModuleType:
    spec=importlib.util.spec_from_file_location("reviewed_triangle_switching",APP)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load triangle controls")
    module=importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules,{spec.name:module}):
        spec.loader.exec_module(module)
    return module


def rows(values: list[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(values[3*i+j] for j in range(3)) for i in range(3))


class SignedTriangleTests(unittest.TestCase):
    def accepted(self,result: Outcome[T]) -> T:
        self.assertIsNone(result.error)
        return cast(T,result.value)

    def refused(self,result: Outcome[T],kind: str="input") -> None:
        self.assertIsNotNone(result.error)
        if result.error is None:
            self.fail("Expected a typed refusal")
        self.assertEqual(result.error.kind,kind)

    def test_all_graphs_and_gauges_against_matrix_and_boolean_oracles(self) -> None:
        for edges in product((-1,1),repeat=3):
            triangle=SignedTriangle(edges)
            a,b,c=edges
            matrix=sp.ImmutableMatrix(((0,a,c),(a,0,b),(c,b,0)))
            self.assertEqual(sp.ImmutableMatrix(triangle.adjacency.rows),matrix)
            parity=sum(int(edge==-1) for edge in edges)%2
            self.assertEqual(triangle.cycle_product,1-2*parity)
            self.assertEqual(triangle.is_balanced,parity==0)
            for gauge in product((-1,1),repeat=3):
                switched=self.accepted(triangle.switch(gauge))
                diagonal=sp.diag(*gauge)
                self.assertEqual(sp.ImmutableMatrix(switched.adjacency.rows),diagonal*matrix*diagonal)
                bits=tuple(int(value==-1) for value in gauge)
                expected=tuple(1-2*((bits[i]+int(edge==-1)+bits[j])%2)
                               for edge,i,j in zip(edges,(0,1,2),(1,2,0)))
                self.assertEqual(switched.edges,expected)
                self.assertEqual(switched.cycle_product,triangle.cycle_product)
            self.assertEqual(triangle.normalizing_gauge,(1,a,a*b))
            self.assertEqual(self.accepted(triangle.switch(triangle.normalizing_gauge)).edges,(1,1,a*b*c))

    def test_group_action_orbits_and_positive_classification(self) -> None:
        gauges=tuple(product((-1,1),repeat=3))
        for edges in product((-1,1),repeat=3):
            triangle=SignedTriangle(edges)
            orbit=set()
            for first in gauges:
                moved=self.accepted(triangle.switch(first))
                orbit.add(moved.edges)
                self.assertEqual(self.accepted(moved.switch(first)),triangle)
                for second in gauges:
                    composite=tuple(a*b for a,b in zip(first,second))
                    self.assertEqual(self.accepted(moved.switch(second)),self.accepted(triangle.switch(composite)))
            self.assertEqual(len(orbit),4)
            self.assertEqual((1,1,1) in orbit,triangle.is_balanced)
            self.assertEqual(self.accepted(triangle.switch((-1,-1,-1))),triangle)

    @PROPERTY
    @given(MATRIX,MATRIX)
    def test_matrix_products_against_symbolic_oracle(self,first: list[int],second: list[int]) -> None:
        module=load()
        left,right=rows(first),rows(second)
        expected=sp.ImmutableMatrix(left)*sp.ImmutableMatrix(right)
        actual=module.multiply(left,right)
        self.assertEqual(sp.ImmutableMatrix(actual),expected)
        result=module.TriangleSwitchingControls.matrix_product(left,right)
        self.assertEqual(sp.ImmutableMatrix(self.accepted(result)),expected)
        self.assertTrue(all(type(value) is int for row in actual for value in row))

    def test_owned_edges_results_and_immutable_family(self) -> None:
        original=[-1,-1,1]
        triangle=SignedTriangle(original)
        original[0]=1
        self.assertEqual(triangle.edges,(-1,-1,1))
        gauge=[1,-1,1]
        switched=self.accepted(triangle.switch(gauge))
        gauge[0]=-1
        self.assertEqual(switched.edges,(1,1,1))
        self.assertEqual(triangle.edges,(-1,-1,1))
        with self.assertRaises(FrozenInstanceError):
            triangle.edges=(1,1,1)  # type: ignore[misc]
        controls=load().TriangleSwitchingControls()
        self.assertEqual(tuple(t.edges for t in controls.triangles),tuple(product((-1,1),repeat=3)))
        with self.assertRaises(FrozenInstanceError):
            controls.triangles=()

    def test_exact_triangle_and_gauge_admission(self) -> None:
        triangle=SignedTriangle((1,1,1))
        invalid=(None,(),(1,1),(True,1,1),(1.0,1,1),(Q(1),1,1),(0,1,1),(2,1,1),(-2,1,1),(1<<4096,1,1))
        for value in invalid:
            self.refused(evaluate(SignedTriangle,value))
            self.refused(triangle.switch(value))
        self.refused(evaluate(SignedTriangle,(1,)*4),"resource")
        self.refused(triangle.switch((1,)*4),"resource")
        with patch.dict(SignedTriangle.__init__.__globals__,_sign=Mock(side_effect=RuntimeError("must not map"))):
            self.refused(evaluate(SignedTriangle,(1,1)))

    def test_matrix_shapes_scalar_domains_and_preflight(self) -> None:
        controls=load().TriangleSwitchingControls()
        zero=((0,0,0),)*3
        invalid=(None,(),((1,),),((1,1),(1,1),(1,1)),((True,0,0),zero[0],zero[0]),
                 ((1.0,0,0),zero[0],zero[0]),((Q(1),0,0),zero[0],zero[0]))
        for value in invalid:
            self.refused(controls.matrix_product(value,zero))
            self.refused(controls.matrix_product(zero,value))
        self.refused(controls.matrix_product(((0,)*4,)*3,zero),"resource")
        self.refused(controls.matrix_product(((0,)*3,)*4,zero),"resource")
        with patch.object(RationalMatrix,"mul",side_effect=RuntimeError("must not multiply")):
            self.refused(controls.matrix_product(zero,invalid[-1]))
        with self.assertRaises(AssertionError):
            self.refused(controls.matrix_product(zero,zero))

    def test_matrix_budgets_cover_terms_and_prefix_cancellation(self) -> None:
        controls=load().TriangleSwitchingControls()
        maximum=(1<<4096)-1
        identity=((1,0,0),(0,1,0),(0,0,1))
        accepted=((maximum,0,0),(0,1,0),(0,0,1))
        self.assertEqual(self.accepted(controls.matrix_product(accepted,identity)),accepted)
        oversized=((1<<4096,0,0),(0,0,0),(0,0,0))
        self.refused(controls.matrix_product(oversized,identity),"resource")
        large=1<<2048
        self.refused(controls.matrix_product(((large,0,0),(0,0,0),(0,0,0)),((large,0,0),(0,0,0),(0,0,0))),"resource")
        # A large second term would cancel the admitted first prefix.
        self.refused(controls.matrix_product(((-maximum,large,0),(0,0,0),(0,0,0)),((1,0,0),(large,0,0),(0,0,0))),"resource")
        # The first two products overflow their prefix before the last cancels it.
        self.refused(controls.matrix_product(((maximum,1,-1),(0,0,0),(0,0,0)),((1,0,0),(1,0,0),(1,0,0))),"resource")

    def test_actual_per_run_counter_and_original_populations(self) -> None:
        controls=load().TriangleSwitchingControls()
        observed: list[str]=[]
        implementation=Cases.require
        def record(cases: Cases,condition: bool,label: str) -> None:
            observed.append(label)
            implementation(cases,condition,label)
        with patch.object(Cases,"require",record):
            result=self.accepted(controls.verify())
        self.assertEqual(result["checks"],len(observed))
        self.assertEqual(result["checks"],145)
        self.assertEqual(observed.count("matrix and edge switching agree"),64)
        self.assertEqual(observed.count("cycle invariant"),64)
        self.assertEqual(observed.count("constructive normal form"),8)
        self.assertEqual(observed.count("switching classification"),8)
        self.assertEqual((result["triangles"],result["switching_cases"],result["balanced"],result["obstructed"]),(8,64,4,4))
        self.assertEqual(result,self.accepted(controls.verify()))

    def test_failure_paths_and_cancellation_propagation(self) -> None:
        module=load()
        zero=((0,0,0),)*3
        with patch.dict(module.TriangleSwitchingControls._verify.__globals__,multiply=lambda *_:zero):
            self.refused(module.TriangleSwitchingControls().verify(),"check")
        for kind in ("check","resource"):
            with patch.dict(module.multiply.__globals__,_matrix=Mock(side_effect=Violation(kind,"injected"))):
                self.refused(module.TriangleSwitchingControls().verify(),kind)
                with contextlib.redirect_stderr(io.StringIO()) as output:
                    self.assertEqual(module.main(),1)
                self.assertEqual(json.loads(output.getvalue())["kind"],kind)
        triangle=SignedTriangle((1,1,1))
        for exception in (RuntimeError,KeyboardInterrupt,SystemExit):
            with patch.object(SignedTriangle,"_switch",side_effect=exception):
                with self.assertRaises(exception):
                    triangle.switch((1,1,1))
            with patch.dict(module.TriangleSwitchingControls._verify.__globals__,multiply=Mock(side_effect=exception)):
                with self.assertRaises(exception):
                    module.TriangleSwitchingControls().verify()

    def test_quiet_import_and_original_cli_output(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            module=load()
        self.assertEqual(output.getvalue(),"")
        for _ in range(2):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(module.main(),0)
            self.assertEqual(output.getvalue(),"triangles=8 switching_cases=64 balanced=4 obstructed=4 failures=0\n")
        result=subprocess.run([sys.executable,"-I","-B",str(APP)],capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout,output.getvalue())


if __name__=="__main__":
    unittest.main()
