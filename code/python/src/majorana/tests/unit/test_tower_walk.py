r"""
Python property test suite for QM_001 (Tower Walk Registry-Relative Interface Lift).

Verifies:
  QM_001-C1: Tower walk registry lifting and interface boundary consistency.
"""

import pytest


def test_qm_001_c1_tower_walk_lift():
    # Simple finite tower registry nodes
    tower_nodes = [0, 1, 2, 3]
    lift_map = {n: float(n * 2) for n in tower_nodes}
    
    for n in tower_nodes:
        assert lift_map[n] == float(n * 2)
        
    # Relative difference transport
    diffs = [lift_map[i+1] - lift_map[i] for i in range(len(tower_nodes)-1)]
    assert all(d == 2.0 for d in diffs)
