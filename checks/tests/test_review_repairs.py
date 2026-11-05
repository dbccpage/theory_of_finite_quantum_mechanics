"""Regression and independent-oracle checks through dfm-continuum-refinement-limit.

AuthorityEffect: None. Run this file with normal Python and with -O.
No production implementation is used as an oracle. The finite test populations
and mutation outcomes do not establish any continuum or physical theorem.
"""
from __future__ import annotations

import contextlib
import ast
from fractions import Fraction as Q
import importlib
import importlib.util
import io
from itertools import combinations, product
import json
from pathlib import Path
import random
import subprocess
import sys
import unittest
from collections.abc import Callable
from types import ModuleType
from typing import ParamSpec, TypeVar
from unittest.mock import patch

CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure
from checker_support.outcome import Outcome
from checker_support.boundary import Violation

SOURCES = tuple(p for p in sorted((CHECKS / "independent").glob("*.py"))
                if p.name <= "dfm-continuum-refinement-limit.py")


P = ParamSpec("P")
T = TypeVar("T")


def load(stem: str) -> ModuleType:
    """Load a reviewed local source, restoring any prior module registration."""
    if type(stem) is not str or stem not in {source.stem for source in SOURCES}:
        raise Violation("input", "checker is outside the reviewed source population")
    name = "reviewed_" + stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, CHECKS / "independent" / (stem + ".py"))
    if spec is None or spec.loader is None:
        raise Violation("resource", "checker import specification is unavailable")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(name)
    try:
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous


def silent(operation: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return operation(*args, **kwargs)


def _collision_free(p1: int, p2: int, hops: tuple[tuple[int, int], ...]) -> bool:
    """Independent simultaneous-hop oracle for the enumerated integer fixtures."""
    x, y = p1, p2
    for dx, dy in hops:
        nx, ny = x+dx, y+dy
        if nx == ny or (x-y)*(nx-ny) < 0:
            return False
        x, y = nx, ny
    return True


class ReviewedCheckerRegressionTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object) -> Failure:
        result = evaluate(operation, *args)
        self.assertFalse(result.ok, (operation, args))
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("expected a typed failure")
        return result.error

    def test_every_checker_cli(self) -> None:
        self.assertEqual(len(SOURCES), 20)
        for source in SOURCES:
            with self.subTest(source=source.name):
                command = [sys.executable, "-I", "-B", "-X", "utf8"]
                if sys.flags.optimize:
                    command.append("-O")
                result = subprocess.run(command + [str(source)], text=True,
                                        capture_output=True, timeout=45)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")

    def test_checker_structure_stays_within_reviewed_bounds(self) -> None:
        # Radon has no typing metadata; its dynamic output is validated below.
        cc_visit = importlib.import_module("radon.complexity").cc_visit
        sources = SOURCES + tuple(sorted((CHECKS / "checker_support").glob("*.py")))
        for source in sources:
            with self.subTest(source=source.name):
                text = source.read_text(encoding="utf-8")
                tree = ast.parse(text)
                self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
                self.assertLessEqual(sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)), 1)
                for block in cc_visit(text):
                    self.assertLessEqual(block.complexity, 15, (source.name, block.name))

    def test_imports_do_not_execute_checks(self) -> None:
        for source in SOURCES:
            with self.subTest(source=source.name):
                output = io.StringIO()
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    load(source.stem)
                self.assertEqual(output.getvalue(), "")

    def test_railway_result_short_circuits(self) -> None:
        error = Failure("input", "invalid fixture")
        result: Outcome[object] = Outcome(error=error).bind(lambda value: self.fail("failure branch executed"))
        self.assertEqual(result.error, error)
        self.assertEqual(Outcome(value=3).bind(lambda x: Outcome(value=x+2)).value, 5)
        self.refused(Outcome, 3, error)
        self.assertEqual(silent(cli, lambda: 1), 1)
        self.assertEqual(silent(cli, lambda: None), 0)
        def failing() -> None:
            raise Violation("check", "mutation")
        self.assertEqual(silent(cli, failing), 1)

    def test_duplicate_case_ids_are_refused(self) -> None:
        cases = Cases()
        cases.append(("one", True))
        self.assertEqual(self.refused(cases.append, ("one", False)).kind, "duplicate")
        self.assertEqual(len(cases), 1)

    def test_assertion_stripping_mutants_are_killed(self) -> None:
        module = load("ads-cft-duality-import")
        with patch.object(module, "gkpw_mass_sq", lambda *_: Q(12345)):
            self.assertEqual(self.refused(module.check_gkpw_identities).kind, "check")
        module = load("ct-information-media-interoperability")
        with patch.object(module, "controlled", lambda x: x):
            self.assertEqual(silent(self.refused, module.main).kind, "check")
        module = load("ct-local-mediator-entanglement-import")
        with patch.object(module.sp, "simplify", lambda *_: 1):
            self.assertEqual(self.refused(module.check_symbolic_local_action_determinant).kind, "check")

    def test_causal_matrix_inverse_boundary(self) -> None:
        module = load("cqft-causal-factorization-import")
        for matrix in (((2, 0), (0, 1)), ((1,), (0, 1)), (), ((True, 0), (0, 1)), ((1.0, 0), (0, 1))):
            self.refused(module.mat2_inv_unimodular, matrix)
        for a,b,c,d in product(range(-2,3), repeat=4):
            if a*d-b*c in (-1,1):
                matrix=((a,b),(c,d))
                self.assertEqual(module.mat2_mul(matrix,module.mat2_inv_unimodular(matrix)),module.I2)

    def test_local_net_boundaries(self) -> None:
        module=load("cqft-local-net-axioms-import")
        for bad in ((), (1,2), (1,2,3,4,5), None):
            self.refused(module.add2, (1,2,3,4), bad)
        for x in (-1,4,True,0.0):
            self.refused(module.spacelike,x,1)
        self.assertEqual(module.add2((1,2,3,4),(10,20,30,40)),(11,22,33,44))

    def test_reeh_matrix_and_site_boundaries(self) -> None:
        module=load("cqft-reeh-schlieder-theorem-import")
        for left,right in (([[1]],[[1],[2]]),([],[[1]]),([[1,2],[3]],[[1],[1]]),([[True]],[[1]])):
            self.refused(module.mat_mul,left,right)
        for site in (-1,3,True):
            self.refused(module.single_site_matrix,[1]*8,site)
        self.refused(module.pair_site_matrix,[1]*7,0)
        self.assertEqual(module.mat_mul([[1,2]],[[3],[4]]),[[11]])

    def test_normalized_concurrence_off_unit_circle(self) -> None:
        module=load("ct-local-mediator-entanglement-import")
        self.assertEqual(module.normalized_concurrence_squared(0,0),Q(4,9))
        self.assertEqual(module.normalized_concurrence_squared(Q(3,5),Q(4,5)),Q(1,5))
        self.assertEqual(module.normalized_concurrence_squared(1,0),0)
        for re,im in product(range(-4,5),repeat=2):
            c=module.normalized_concurrence_squared(re,im)
            self.assertLessEqual(c,1)
            self.assertGreaterEqual(c,0)
        self.refused(module.normalized_concurrence_squared,0.1,0)

    def test_rice_and_rewrite_invalid_inputs(self) -> None:
        module=load("auth-rice-theorem-import")
        for code,index in ((-1,0),(3,0),(0,2),(True,0),(0,False)):
            self.refused(module.beh,code,index)
        module=load("comp-finite-model-controls")
        self.refused(module.hole,[9],[],[1],[0],[])
        self.assertEqual(module.hole([4,1,5],[4],[1],[2,3],[5]),[4,2,3,5])

    def test_happy_regions_and_independent_rank(self) -> None:
        module=load("ads-happy-toy-not-duality-gap")
        gens=module.build_boundary_gens_20()
        for region in ([20],[0,0,0],[-1],[True]):
            self.refused(module.region_entropy,gens,region)
        self.refused(module.region_mutual_information,gens,[0],[0])
        for start,length in ((0,-1),(20,1),(0,21),(True,1)):
            self.refused(module.interval_entropy,gens,start,length)
        rng=random.Random(20261102)
        for _ in range(160):
            rows=[rng.randrange(1<<12) for _ in range(rng.randrange(14))]
            span={0}
            for row in rows:
                span |= {x^row for x in tuple(span)}
            self.assertEqual(1<<module.gf2_rank(rows),len(span))

    def test_happy_mincut_independent_graph_enumeration(self) -> None:
        module=load("ads-happy-toy-not-duality-gap")
        # Enumerate all six internal vertex assignments; never call the cut implementation.
        for start,length in product(range(20),range(1,20)):
            region={(start+i)%20 for i in range(length)}
            costs=[]
            for central,*outer in product((0,1),repeat=6):
                bonds=sum(central!=side for side in outer)
                boundary=sum(outer[q//4] != int(q in region) for q in range(20))
                costs.append(bonds+boundary)
            self.assertEqual(module.interval_mincut(start,length),min(costs))

    def test_rt_exact_certificates_and_subdivision(self) -> None:
        rt=load("ads-rt-formula-import")
        self.assertFalse(rt.has_rational_square_root(Q(3,4)))
        self.assertTrue(rt.has_rational_square_root(Q(9,16)))
        for g in (0,-1,0.5,True):
            self.refused(rt.rt_leading_entropy,Q(1),g)
        regge=load("ads-regge-area-rt-gap")
        for m in (0,-1,Q(3,2),True):
            self.refused(regge.sq_area_subdivision_sum,Q(1),m)
        for area,m in product((Q(1,3),Q(3,2)),range(1,9)):
            self.assertEqual(regge.sq_area_subdivision_sum(area,m),area**2/m)

    def test_wilson_determinant_against_bareiss(self) -> None:
        import sympy as sp
        module=load("check_tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity")
        for bad in (0.1,True,"1"):
            self.refused(module.direct_wilson_determinant,bad,Q(1))
        for m,r in product((Q(-2),Q(-1),Q(0),Q(1,3)),(Q(0),Q(1,2),Q(1),Q(3,2))):
            s=m+2*r
            matrix=sp.Matrix([[s,0,-r,0,-r,0,0,0],[0,s,0,-r,0,-r,0,0],
                              [-r,0,s,0,0,0,0,1],[0,-r,0,s,0,0,1,0],
                              [-r,0,0,0,s,0,0,1],[0,-r,0,0,0,s,-1,0],
                              [0,0,0,-1,0,1,s,0],[0,0,-1,0,-1,0,0,s]])
            self.assertEqual(module.direct_wilson_determinant(m,r),matrix.det(method="bareiss"))
        receipt=module.check()
        self.assertEqual(receipt["total_checks"],110)
        self.assertTrue(receipt["all_passed"])

    def test_chirality_mutant_is_killed(self) -> None:
        from checker_support.wilson_operator import gamma_matrices, clifford_relations, assembled_operator, gamma5_hermitian
        wrong_signs=(1,1,1,1)
        self.assertFalse(clifford_relations(gamma_matrices(),wrong_signs))
        self.assertFalse(gamma5_hermitian(assembled_operator(Q(1,2)),wrong_signs))

    def test_strong_coupling_phase_and_domains(self) -> None:
        import sympy as sp
        module=load("check_tfq_1052_fqcd_strong_coupling_area_law")
        c,s=Q(3,5),Q(4,5)
        for q in range(-10,11):
            re,im=module.theta_phase(c,s,q)
            expected=sp.expand((sp.Rational(3,5)-sp.I*sp.Rational(4,5))**q)
            self.assertEqual(re,sp.re(expected))
            self.assertEqual(im,sp.im(expected))
        self.assertEqual(module.theta_phase(c,s,4),(Q(-527,625),Q(336,625)))
        for action,args in ((module.delta_coordination,(2.5,)),(module.cluster_sum_rational,(0.2,1)),
                            (module.spanning_area,(True,2)),(module.theta_phase,(c,s,True)),
                            (module.theta_phase,(1,1,2)),(module.direct_modified_chirality_square,(0,1,0))):
            self.refused(action,*args)
        receipt=module.run_checks()
        self.assertEqual(receipt["total_checks"],250)
        self.assertTrue(receipt["all_passed"])
        self.assertLess(Q(30911071,559872000),Q(3,50))
        self.assertLess(Q(3,50),Q(14411,194400))
        if module.__file__ is None:
            self.fail("loaded checker has no source path")
        source=Path(module.__file__).read_text(encoding="utf-8")
        self.assertIn("M_3(Sigma(1080)) - 1 < 3/50 < (1/9)(M_2 - 1)", source)

    def test_lineon_invalid_domains_and_exact_curvature(self) -> None:
        import sympy as sp
        module=load("check_tfq_1219_fsp_hinge_lineon_sign_claim")
        for hop in ((2,0),(0.5,0),(True,0)):
            self.refused(module.compute_lineon_permutation_parity,0,2,[hop])
        self.refused(module.compute_lineon_permutation_parity,0,1,[(1,-1)])
        self.refused(module.verify_discrete_ivt_collision_site,0,2,[0,2],[2,0])
        self.refused(module.compute_curvature_gamma2,Q(3))
        self.assertEqual(module.compute_curvature_gamma2(Q(-2)),sp.pi)
        self.assertEqual(module.compute_curvature_gamma2(Q(0)),sp.pi/2)
        self.assertEqual(module.compute_curvature_gamma2(Q(2)),0)
        self.refused(module.ComplexRat,0.1,0)
        self.refused(module.ComplexRat(0).inv)
        self.refused(module.Mat2x2,1,0,0,1)
        self.assertTrue(module.run_checks()["all_passed"])

    def test_lineon_8200_paths_against_collision_oracle(self) -> None:
        module=load("check_tfq_1219_fsp_hinge_lineon_sign_claim")
        compared=0
        hop_options = tuple((dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        for p1,p2 in combinations(range(-2,3),2):
            for length in range(4):
                for hops in product(hop_options, repeat=length):
                    valid = _collision_free(p1, p2, hops)
                    self.assertEqual(module.verify_1d_lineon_collision_avoidance(p1,p2,list(hops)),valid)
                    compared+=1
        self.assertEqual(compared,8200)

    def test_bphz_shape_and_forest_boundaries(self) -> None:
        module=load("dfm-bphz-continuum-fence")
        for matrix in ((Q(1),)*3,(Q(1),)*5,None):
            self.refused(module.checked_reduce,(matrix,))
        for names in (("L","L"),("missing",)):
            self.refused(module.forests,names,module.OVERLAP)
        self.assertEqual(len(module.forests(("L","R","G"),module.OVERLAP)),6)

    def test_bphz_joint_kernel_converse_1925_cases(self) -> None:
        module=load("dfm-bphz-continuum-fence")
        def apply(matrix: tuple[Q, ...], vector: tuple[Q, ...]) -> tuple[Q, Q]:
            a,b,c,d=matrix;x,y=vector
            return a*x+b*y,c*x+d*y
        matrices=[tuple(map(Q,x)) for x in product((-1,0,1),repeat=4)]
        projectors=[m for m in matrices if module.multiply(m,m)==m]
        count=0
        for size in range(3):
            for family in product(projectors,repeat=size):
                if any(module.multiply(p,q)!=module.multiply(q,p) for p in family for q in family):
                    continue
                reduction=module.checked_reduce(family)
                for vector in product(tuple(map(Q, range(-2,3))),repeat=2):
                    self.assertEqual(apply(reduction,vector)==vector,
                                     all(apply(p,vector)==(Q(0),Q(0)) for p in family))
                    count+=1
        self.assertEqual(count,1925)

    def test_ckm_immutable_exact_labels_and_budget(self) -> None:
        from dataclasses import FrozenInstanceError
        module=load("dfm-ckm-physics-fence")
        label=module.GR(1)
        with self.assertRaises(FrozenInstanceError):
            label.re=0.1
        self.assertEqual(module.shape(((label,),)),(1,1))
        for height,width in ((0,1),(-1,2),(True,1),(3,3),(1000000,1)):
            self.refused(module.sign_tables,height,width)
        self.assertEqual(len(module.sign_tables(2,3)),64)

    def test_continuum_matrix_bypass_is_refused(self) -> None:
        import sympy as sp
        module=load("dfm-continuum-interface")
        for matrix in (sp.Matrix([[2,0],[0,1]]),sp.Matrix([[1.0,0],[0,1]]),sp.zeros(2),sp.eye(3)):
            for sign in (-1,1):
                self.refused(module.path_transport,{"x":matrix},(("x",sign),))
        self.refused(module.transport,{},("missing",))
        self.refused(module.dress,{},"missing")
        x=module.mat([[1,1],[0,1]])
        self.assertIsInstance(x,sp.ImmutableMatrix)
        self.assertEqual(module.path_transport({"x":x},(("x",-1),)),x.inv())

    def test_refinement_bounds_group_and_repeatability(self) -> None:
        module=load("dfm-continuum-refinement-limit")
        for word in ((2,),(1,),(False,0)):
            self.refused(module.endpoints,word)
        for depth in (-1,True,1.5,13):
            self.refused(module.leaves,(),depth)
        for permutation in ((0,1),(0,0,2),(False,1,2),(1,2,3)):
            self.refused(module.inv,permutation)
        results=[]
        for _ in range(2):
            output=io.StringIO()
            with contextlib.redirect_stdout(output):
                module.main()
            results.append(json.loads(output.getvalue())["checks"])
        self.assertEqual(results,[14642,14642])
        with patch.object(module,"scalar_controls",side_effect=Violation("check","forced failure")):
            self.assertFalse(evaluate(module.main).ok)
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            module.main()
        self.assertEqual(json.loads(output.getvalue())["checks"],14642)
        for depth in range(9):
            intervals=[module.endpoints(word) for word in module.leaves((),depth)]
            self.assertEqual(intervals[0][0],0)
            self.assertEqual(intervals[-1][1],1)
            self.assertTrue(all(left[1]==right[0] for left,right in zip(intervals,intervals[1:])))


if __name__ == "__main__":
    unittest.main(verbosity=2)
