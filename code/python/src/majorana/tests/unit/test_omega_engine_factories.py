"""Unit tests for omega_engine interfaces, base classes, and factory adapters."""

import unittest
import numpy as np

from omega_engine.crates.solver import (
    BaseSolver,
    FunctionSolverAdapter,
    SolverDescriptor,
    SolverKernel,
    SolverResult,
    verify_solver_contract,
)
from omega_engine.crates.functional.factory import (
    evaluate_functional,
    list_available_functionals,
    Gamma2Kernel,
    Phi1Kernel,
    WignerYanaseKernel,
)
from omega_engine.crates.carrier.factory import CarrierFactory


class TestOmegaEngineFactories(unittest.TestCase):
    def test_solver_operation_adapters(self):
        descriptor = SolverDescriptor(
            solver_id="test:sum",
            version="1.0.0",
            implementation_hash="0" * 64,
            algorithm_ref="test:sum:v1",
        )

        adapter = FunctionSolverAdapter(
            lambda problem: {"sum": sum(problem)},
            descriptor,
        )
        result = adapter.solve((1, 2, 3))

        self.assertTrue(verify_solver_contract(adapter))
        self.assertIsInstance(adapter, SolverKernel)
        self.assertIsInstance(result, SolverResult)
        self.assertEqual(result.payload, {"sum": 6})
        self.assertEqual(result.evidence_class, "EvidenceOnly")
        self.assertEqual(result.authority_effect, "None")
        self.assertEqual(adapter.descriptor, descriptor)

        class StructuralSolver:
            def solve(self, problem):
                return SolverResult(payload=problem * 2, residual=0)

        structural = StructuralSolver()
        self.assertTrue(verify_solver_contract(structural))
        self.assertIsInstance(structural, SolverKernel)
        self.assertEqual(structural.solve(4).payload, 8)

        class BaseOnlySolver(BaseSolver):
            pass

        self.assertFalse(verify_solver_contract(StructuralSolver))
        self.assertFalse(verify_solver_contract(BaseSolver))
        self.assertFalse(verify_solver_contract(BaseOnlySolver))
        with self.assertRaises(TypeError):
            BaseOnlySolver()

    def test_functional_factory_evaluators(self):
        funcs = list_available_functionals()
        self.assertIn("gamma2", funcs)
        self.assertIn("phi1", funcs)
        self.assertIn("wigner_yanase", funcs)

        res_g2 = evaluate_functional("gamma2", [0.0, 0.0, 0.0])
        self.assertTrue(res_g2.is_closed)
        self.assertEqual(res_g2.value, 0.0)

        res_p1 = evaluate_functional("phi1", [1.0, 2.0])
        self.assertFalse(res_p1.is_closed)
        self.assertEqual(res_p1.value, 3.0)

        rho = np.array([[1.0, 0.0], [0.0, 0.0]])
        h_op = np.array([[0.0, 1.0], [1.0, 0.0]])
        res_wy = evaluate_functional("wigner_yanase", rho, h_op)
        self.assertGreater(res_wy.value, 0.0)

    def test_carrier_factory(self):
        checked_carrier = CarrierFactory.create_carrier(
            carrier_id="c_tri_01",
            carrier_kind="SimplicialTriangle",
            nodes=[0, 1, 2],
            edges=[(0, 1), (1, 2), (2, 0)],
            faces=[(0, 1, 2)],
        )
        self.assertTrue(checked_carrier.is_valid_chain_law)
        self.assertEqual(checked_carrier.authority_effect, "FactOnly")
        self.assertEqual(checked_carrier.artifact.carrier_id, "c_tri_01")


if __name__ == "__main__":
    unittest.main()


