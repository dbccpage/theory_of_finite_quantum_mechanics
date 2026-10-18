"""
test_hamiltonian_gin_bridge.py — Integration Tests for Hamiltonian GIN Bridge
Status: Integration Test Suite
AuthorityEffect: None

Tests:
1. Bipartite 4-site Fermi-Hubbard Hamiltonian Trotter paths indexed into GIN cochains.
2. Complete pairing of all negative paths with exact equal-weight positive partners -> Repair.
3. Frustrated triangle Fermi-Hubbard Hamiltonian path generation and disjoint weight obstruction -> SplitBrainRefusal.
4. GIN mode posting lists resolve inverted mode presence queries across Hamiltonian paths.
"""

from __future__ import annotations

from pathlib import Path
import sys
import pytest

current_dir = Path(__file__).resolve().parent
pkg_dir = current_dir.parent.parent
if str(pkg_dir) not in sys.path:
    sys.path.insert(0, str(pkg_dir))

from src.fsp.fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
)
from src.fsp.hamiltonian_gin_bridge import HamiltonianGinBridge


def test_bipartite_hamiltonian_indexing_and_sign_repair():
    """This finite ring Euler ensemble has exact equal-weight partners."""
    # 4-site periodic ring with 2 identical spin-up fermions
    lattice = FermionicLattice.linear_chain(4, periodic=True)
    h_bip = DiscreteFermionicHamiltonian(lattice, t=1.0, u=0.0, num_up=2, num_down=0)

    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        index_res = bridge.index_hamiltonian_paths(
            h_bip,
            beta=1.5,
            trotter_steps=4,
            model_name="BipartiteRing4",
        )

        assert index_res["total_paths"] > 0
        assert index_res["negative_paths"] == 32
        assert index_res["matched_pairs"] == 32
        assert index_res["unpartnered_negatives"] == 0
        assert index_res["is_completely_paired"] is True
        assert index_res["preserves_general_observables"] is False

        receipt = bridge.audit_sign_resolution("BipartiteRing4")
        assert receipt.all_exact_cancellations is True
        assert receipt.exact_max_weight_defect == 0
        assert receipt.exact_unpaired_negative_mass == 0
        assert receipt.exact_residual_mass == receipt.exact_signed_sum > 0
        assert receipt.integrity_errors == ()
        assert receipt.gin_quotiented_average_sign == 1.0
        assert receipt.terminal_route == "Repair"
    finally:
        bridge.close()


def test_frustrated_triangle_hamiltonian_indexing_obstruction():
    """Validates that a frustrated triangle cluster leaves unpartnered negative paths routing to SplitBrainRefusal."""
    # 3-site triangle cluster with 2 identical spin-up fermions
    lattice = FermionicLattice.triangle_cluster()
    h_tri = DiscreteFermionicHamiltonian(lattice, t=1.0, u=0.0, num_up=2, num_down=0)

    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        index_res = bridge.index_hamiltonian_paths(
            h_tri,
            beta=2.0,
            trotter_steps=3,
            model_name="FrustratedTriangle3",
        )

        assert index_res["total_paths"] == 27
        assert index_res["negative_paths"] == 6
        # On a triangle cluster, positive weights are 0.4444 and 1.0; negative weights are 0.2963
        # No partner can have identical weight, so matched pairs must be 0
        assert index_res["matched_pairs"] == 0
        assert index_res["unpartnered_negatives"] == 6
        assert index_res["is_completely_paired"] is False

        receipt = bridge.audit_sign_resolution("FrustratedTriangle3")
        assert receipt.all_exact_cancellations is False
        assert receipt.total_uncancelled_mass > 0.0
        assert receipt.gin_quotiented_average_sign < 1.0
        assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        bridge.close()


def test_kitaev_chain_majorana_bridge():
    """Validates that Kitaev chain Majorana zero modes (1 and 2L) are isolated from bulk pairing."""
    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        mzm_rec = bridge.index_kitaev_chain_majorana(L=4, model_name="KitaevMajoranaL4")
        assert mzm_rec.is_boundary_isolated is True
        assert set(mzm_rec.unpaired_zero_modes) == {1, 8}
        assert len(mzm_rec.bulk_bonded_modes) == 6
        assert mzm_rec.mzm_status == "MZM_TOPOLOGICALLY_PROTECTED"
    finally:
        bridge.close()


def test_gin_posting_list_mode_query():
    """Validates that GIN mode posting lists resolve inverted mode presence queries."""
    lattice = FermionicLattice.linear_chain(2, periodic=False)
    h_chain = DiscreteFermionicHamiltonian(lattice, t=1.0, u=0.5, num_up=1, num_down=1)

    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        bridge.index_hamiltonian_paths(h_chain, beta=1.0, trotter_steps=2, model_name="Chain2")
        assert len(bridge.posting_index) > 0
        for m in (1, 2, 3, 4):
            assert len(bridge.posting_index[m]) > 0
    finally:
        bridge.close()
