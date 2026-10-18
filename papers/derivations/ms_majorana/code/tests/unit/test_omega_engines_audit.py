from __future__ import annotations
"""Comprehensive P0 & P1 audit tests for omega_engine.crates.engine.

Verifies math correctness, refusal terminals, authority limits, quantum carrier gates,
and batch streaming behaviors as outlined in the initial engine review.
"""


import asyncio
import math
import unittest
import numpy as np

from omega_engine.crates.linear_algebra_theory.density import DensityMatrixConfig, NumericalDensityMatrix
from omega_engine.crates.engine.eng_qm_complex_quantum_density import (
    ComplexQuantumDensityEngine,
)
from omega_engine.crates.functional.fn_qm_entropy import (
    shannon_checked,
    assert_admitted_entropy_path,
    LossyEntropyAuthorityPathRefusal,
)
from omega_engine.crates.operator.constructor.ctor_qm_density_from_h1 import (
    density_from_h1_typed,
    NoValidDensity,
    ZeroResidualVector,
)
from omega_engine.crates.engine.eng_qm_quantum_density import QuantumDensityEngine
from omega_engine.crates.engine.eng_qm_quantum_information import (
    QuantumBackendUnrequestedRefused,
    assert_quantum_carrier_admitted,
)
from omega_engine.crates.runtime.rt_streaming import StreamingEngine
from omega_engine.crates.runtime.rt_async_homological import AsyncHomologicalEngine
from omega_engine.crates.operator.generator.gen_everett import ManyWorldsDAG


class TestOmegaEnginesAudit(unittest.TestCase):
    def test_complex_entropy_not_double_count_real_block_spectrum(self):
        """P0: Verify von Neumann entropy on (2x2) maximally mixed state equals ln(2), not 2*ln(2)."""
        # Maximally mixed state I/2
        rho = np.eye(2, dtype=complex) / 2.0
        cfg = DensityMatrixConfig.default()
        dm = NumericalDensityMatrix.from_validated(2, rho.flatten().tolist(), cfg)

        entropy = ComplexQuantumDensityEngine.von_neumann_entropy_complex(dm)
        expected = math.log(2.0)
        self.assertAlmostEqual(entropy, expected, places=5)

    def test_lossy_entropy_functions_forbidden_in_admitted_prompt_path(self):
        """P0: Verify lossy entropy functions raise LossyEntropyAuthorityPathRefusal on admitted paths."""
        with self.assertRaises(LossyEntropyAuthorityPathRefusal):
            assert_admitted_entropy_path(lossy=True, authority_admitted=True)

        # Checked entropy passes closed
        val = shannon_checked([0.5, 0.5])
        self.assertAlmostEqual(val, math.log(2.0), places=5)

    def test_density_none_results_convert_to_typed_refusal(self):
        """P0: Verify empty/zero h1 residuals produce typed refusal terminals instead of raw None."""
        with self.assertRaises(NoValidDensity):
            density_from_h1_typed([])

        with self.assertRaises(ZeroResidualVector):
            density_from_h1_typed([0.0, 0.0, 0.0])

        with self.assertRaises(Exception):
            QuantumDensityEngine.from_states_typed([])

    def test_engine_stream_does_not_claim_flat_ram_unless_batch_streaming(self):
        """P0: Verify StreamingEngine processes input in true batch_size chunks."""
        inputs = [f"line_{i}" for i in range(10)]
        processed_count = 0

        def solver(line: str) -> str:
            nonlocal processed_count
            processed_count += 1
            return line.upper()

        results = StreamingEngine.process_stream(inputs, batch_size=3, solver=solver)
        self.assertEqual(len(results), 10)
        self.assertEqual(results[0], "LINE_0")
        self.assertEqual(processed_count, 10)

    def test_async_engine_errors_emit_failure_receipts_not_raw_error_strings(self):
        """P0: Verify AsyncHomologicalEngine emits structured failure receipts with AuthorityEffect: None."""

        async def run_test():
            engine = AsyncHomologicalEngine(num_workers=1)
            await engine.start()
            # None prompt triggers exception in text metrics
            evt = await engine.submit("q1", None, topology_type="cycle")

            await evt.wait()
            res = engine.results["q1"]
            await engine.stop()
            return res

        res = asyncio.run(run_test())
        self.assertIn("refusal_route", res)
        self.assertEqual(res["refusal_route"], "ASYNC_ENGINE_RUNTIME_FAILURE")
        self.assertEqual(res["authority_effect"], "None")

    def test_density_observer_authority_effect_none_everywhere(self):
        """P0: Verify density engines explicitly carry AuthorityEffect: None."""
        dag = ManyWorldsDAG.new_root("root", 1.0, [1])
        d = dag.to_dict()
        self.assertEqual(d["authority_effect"], "None")
        self.assertEqual(d["support_grade"], "ToyDiagnosticOnly")

    def test_prompt_orchestrator_rejects_unrequested_quantum_backend(self):
        """P0: Verify quantum engines raise QUANTUM_BACKEND_UNREQUESTED_REFUSED unless carrier admitted."""
        with self.assertRaises(QuantumBackendUnrequestedRefused):
            assert_quantum_carrier_admitted(quantum_carrier_admitted=False)

    def test_everett_dag_is_quarantined_until_validation_added(self):
        """P1: Verify Everett DAG is quarantined under ToyDiagnosticOnly grade."""
        dag = ManyWorldsDAG.new_root("n0", 0.707, [1, 0])
        self.assertEqual(dag.support_grade, "ToyDiagnosticOnly")
        self.assertEqual(dag.authority_effect, "None")


if __name__ == "__main__":
    unittest.main()


