"""Unit Tests: Discrete Fermionic Hamiltonian & Path Parities.
AuthorityEffect: None.
"""

from __future__ import annotations
from pathlib import Path
import sys
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    FockState,
    WheelerDeWittToyConstraint,
)


def test_bipartite_vs_frustrated_lattice():
    """Validates partition function evaluation on bipartite chain vs frustrated triangle."""
    chain2 = FermionicLattice.linear_chain(2)
    h_chain = DiscreteFermionicHamiltonian(chain2, t=1.0, u=2.0, num_up=1, num_down=1)
    assert h_chain.dim == 4
    res_chain = h_chain.compute_partition_functions(beta=1.0, trotter_steps=3)
    assert res_chain["z_bosonic"] > 0
    assert res_chain["z_fermionic"] > 0
    assert res_chain["average_sign"] > 0.5

    tri = FermionicLattice.triangle_cluster()
    h_tri = DiscreteFermionicHamiltonian(tri, t=1.0, u=0.0, num_up=2, num_down=0)
    assert h_tri.dim == 3
    res_tri = h_tri.compute_partition_functions(beta=2.0, trotter_steps=3)
    assert res_tri["z_bosonic"] > res_tri["z_fermionic"]
    assert 0.0 < res_tri["average_sign"] < 1.0
    assert res_tri["sign_problem_severity"] > 0.0


def test_path_generation():
    """Validates generation of Trotter paths with permutation signs."""
    chain2 = FermionicLattice.linear_chain(2)
    h_chain = DiscreteFermionicHamiltonian(chain2, t=1.0, u=0.5, num_up=1, num_down=1)
    paths = h_chain.generate_sample_paths(beta=0.5, trotter_steps=2)
    assert len(paths) > 0
    for p in paths:
        assert "signed_amplitude" in p
        assert "parity" in p
        assert abs(p["signed_amplitude"]) == pytest.approx(p["abs_weight"])


def test_wheeler_dewitt_toy_constraint():
    """Validates discrete Wheeler-DeWitt Hamiltonian scalar constraint evaluation."""
    wdw = WheelerDeWittToyConstraint(
        vertices=[0, 1, 2],
        momenta={0: 1.0, 1: 0.5},
        curvatures={0: 0.2, 1: -0.1, 2: 0.0},
        dual_volumes={0: 1.0, 1: 1.0, 2: 1.0},
    )
    violations = wdw.evaluate_scalar_violations()
    assert len(violations) == 3
    l1_defect = wdw.evaluate_l1_hamiltonian_defect()
    assert l1_defect > 0.0
