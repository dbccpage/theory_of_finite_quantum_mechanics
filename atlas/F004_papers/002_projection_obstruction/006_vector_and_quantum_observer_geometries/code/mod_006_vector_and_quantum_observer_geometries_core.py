"""
006 Vector And Quantum Observer Geometries Core Evaluator Module.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

from demonstrations import (
    demo_classical_triangle_separation,
    demo_quantum_triangle_uniform_z,
    demo_bloch_isometry_vs_qutrit_crosspolytope,
    demo_cptp_quotient_monotonicity,
)


@dataclass(frozen=True)
class PaperEvaluator:
    """Core evaluation and verification harness for Paper 006."""

    paper_id: str = "006_vector_and_quantum_observer_geometries"

    def evaluate(self) -> Dict[str, Any]:
        """
        Execute end-to-end evaluation across classical vector geometries,
        quantum trace obstruction, Bloch sphere vs qutrit isometry boundary,
        and CPTP quotient monotonicity.
        """
        demo1 = demo_classical_triangle_separation()
        demo2 = demo_quantum_triangle_uniform_z()
        demo3 = demo_bloch_isometry_vs_qutrit_crosspolytope()
        demo4 = demo_cptp_quotient_monotonicity()

        # Integrity checks
        assert abs(demo1["phi_1_1_primal"] - 2.0) < 1e-4
        assert abs(demo1["phi_2_1_primal"] - 1.41421356) < 1e-4
        assert abs(demo2["uniform_phi_q_primal"] - 1.5) < 1e-4
        assert demo2["telescoping_is_zero"]
        assert demo3["qubit_is_euclidean"]
        assert demo3["qutrit_is_non_euclidean"]
        assert demo4["depolarizing"]["is_monotone"]
        assert demo4["unitary_invariance"]["is_exact_invariant"]

        return {
            "paper_id": self.paper_id,
            "status": "EVALUATED_PASS",
            "authority": "None",
            "demonstrations": {
                "demo_1_classical_triangle": demo1,
                "demo_2_quantum_triangle": demo2,
                "demo_3_bloch_vs_qutrit": demo3,
                "demo_4_cptp_monotonicity": demo4,
            },
        }
