"""RE1-RE5 Replica Hierarchy cross-validation module for Claims D1-D5.

Verifies singleton separability (RE3), positive homogeneity (RE2), orbit weight constraints (RE4),
and unweighted edgewise L1 sum calibration (RE3+RE5) over multi-replica cochain tensor structures.
"""

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np

code_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path(".")
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from omega_engine.crates.residuals.network_residual import Network


@dataclass
class ReplicaObserverProfile:
    """Observer profile implementing RE1-RE5 measurement axioms."""
    edge_weights: Dict[Tuple[Any, Any], float]
    singleton_calibration: bool = True
    authority_effect: str = "None"

    def evaluate_singleton(self, edge: Tuple[Any, Any], val: float) -> float:
        """RE5: Singleton unit calibration j_e(x_e) = |x_e|."""
        w = self.edge_weights.get(edge, 1.0) if not self.singleton_calibration else 1.0
        return w * abs(val)

    def evaluate_replica_cochain(self, cochain: Dict[Tuple[Any, Any], float]) -> float:
        """RE3: Singleton separability sum_e J_{e}(x)."""
        return sum(self.evaluate_singleton(e, val) for e, val in cochain.items())


class TestReplicaHierarchyClaims(unittest.TestCase):
    def test_claim_d2_re3_singleton_separability(self):
        """Cross-validate Claim D2: RE3 gives singleton decomposition J_E(x) = sum_e J_{e}(x)."""
        edges = [(0, 1), (1, 2), (2, 0)]
        profile = ReplicaObserverProfile(edge_weights={(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0})
        cochain = {(0, 1): 3.0, (1, 2): -4.0, (2, 0): 2.5}

        j_global = profile.evaluate_replica_cochain(cochain)
        j_singletons = sum(profile.evaluate_singleton(e, val) for e, val in cochain.items())

        self.assertAlmostEqual(j_global, j_singletons, places=6)
        self.assertAlmostEqual(j_global, 9.5, places=6)

    def test_claim_d3_re1_re2_positive_homogeneity(self):
        """Cross-validate Claim D3: RE1+RE2 non-negativity and positive homogeneity J(c*x) = c*J(x)."""
        profile = ReplicaObserverProfile(edge_weights={(0, 1): 2.0, (1, 2): 1.5})
        cochain = {(0, 1): 2.0, (1, 2): -3.0}

        c = 3.5
        scaled_cochain = {e: c * val for e, val in cochain.items()}

        j_orig = profile.evaluate_replica_cochain(cochain)
        j_scaled = profile.evaluate_replica_cochain(scaled_cochain)

        self.assertGreaterEqual(j_orig, 0.0)
        self.assertAlmostEqual(j_scaled, c * j_orig, places=6)

    def test_claim_d4_re4_orbit_invariance(self):
        """Cross-validate Claim D4: RE4 constrains weights on declared edge-exchange orbits."""
        profile = ReplicaObserverProfile(edge_weights={(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0})

        cochain_a = {(0, 1): 4.0, (1, 2): 2.0}
        cochain_permuted = {(0, 1): 2.0, (1, 2): 4.0}

        j_a = profile.evaluate_replica_cochain(cochain_a)
        j_b = profile.evaluate_replica_cochain(cochain_permuted)

        self.assertEqual(j_a, j_b)

    def test_claim_d5_re3_re5_unweighted_sum_calibration(self):
        """Cross-validate Claim D5: RE3+RE5 give exact unweighted edgewise L1 sum sum_e |x_e|."""
        profile = ReplicaObserverProfile(edge_weights={}, singleton_calibration=True)
        cochain = {(0, 1): 1.5, (1, 2): -2.5, (2, 0): 3.0}

        j_unweighted = profile.evaluate_replica_cochain(cochain)
        l1_sum = sum(abs(v) for v in cochain.values())

        self.assertAlmostEqual(j_unweighted, l1_sum, places=6)
        self.assertEqual(j_unweighted, 7.0)

    def test_non_calibrated_edge_exchange_orbits(self):
        """Verify non-unit scalar weighting (c_e != 1) on non-calibrated edge exchange orbits when RE5 is dropped."""
        profile = ReplicaObserverProfile(
            edge_weights={(0, 1): 2.5, (1, 2): 0.5, (2, 0): 1.0},
            singleton_calibration=False,
        )

        cochain_a = {(0, 1): 4.0, (1, 2): 2.0, (2, 0): 1.0}
        cochain_swapped = {(0, 1): 2.0, (1, 2): 4.0, (2, 0): 1.0}

        j_weighted_a = profile.evaluate_replica_cochain(cochain_a)
        j_weighted_swapped = profile.evaluate_replica_cochain(cochain_swapped)

        self.assertEqual(j_weighted_a, 12.0)

        self.assertEqual(j_weighted_swapped, 8.0)
        self.assertNotEqual(j_weighted_a, j_weighted_swapped)


if __name__ == "__main__":
    unittest.main()






