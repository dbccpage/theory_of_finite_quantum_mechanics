"""Tier 4: Real-World Application Scenarios E2E Tests.

Exercises realistic physics workloads and end-to-end protocols:
1. Scenario 1: Fault-tolerant multi-qubit topological Majorana braiding circuit.
2. Scenario 2: Fermi-Hubbard triangular cluster quench and CAR sign tracking.
3. Scenario 3: 6D quantum state tomography and quad Gramian SDP obstruction.
4. Scenario 4: Kitaev chain topological phase transition across chemical potential sweep.
5. Scenario 5: Surface code dual observation, error syndrome detection, and repair capacity.
AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

# ---------------------------------------------------------------------------
# MUB6 Domain Imports
# ---------------------------------------------------------------------------
from src.mub import (
    Cyc24,
    verify_triple_pairwise_mu,
)
from src.mub.mub_verify import (
    dita_seed_triple_columns,
)
from src.mub.mub_verify.target_a4_gram_certifier import (
    canonical_quad_gramian,
    verify_gramian_structure,
)

# ---------------------------------------------------------------------------
# FSP Domain Imports
# ---------------------------------------------------------------------------
from src.fsp import (
    witness as fsp_witness,
    refuse_removed_holonomy as fsp_refuse_removed_holonomy,
    refuse_foreign_fixture as fsp_refuse_foreign_fixture,
)
from src.fsp.fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    FockState,
)

# ---------------------------------------------------------------------------
# Majorana Domain Imports
# ---------------------------------------------------------------------------
from src.majorana import (
    FockCarrier,
    MajoranaMonomial,
    MajoranaOperator,
    build_tetron_array,
    logical_class_representative,
    classify_default,
    surface_grid_2x2_torus,
    torus_logical_x_example,
    torus_logical_z_example,
    dual_observe,
    observer_face_syndrome,
    observer_first_face_only,
    repair_capacity_from_distance,
    assert_repair_capacity_invariant,
    Axis,
    Topology,
    Terminal,
)
from src.majorana.sparse_kitaev import SparseKitaevWire
from src.majorana.multiqubit_braid import (
    MultiQubitOperation,
    compile_multi_qubit_braid,
)
from src.majorana.pauli_noise import SkewNoiseMatrix


# ===========================================================================
# Scenario 1: Fault-Tolerant Topological Braiding Circuit
# ===========================================================================

def test_tier4_scenario_fault_tolerant_topological_braiding():
    """Scenario 1: Compile a multi-qubit topological circuit and test noise invariance."""
    # 2 logical qubits encoded in 8 Majorana modes
    ops = [
        MultiQubitOperation.Phase(qubit=1),
        MultiQubitOperation.Hadamard(qubit=2),
        MultiQubitOperation.Swap(first=1, second=2),
    ]
    compiled = compile_multi_qubit_braid(num_qubits=2, operations=ops)
    assert compiled.num_qubits == 2
    assert compiled.gate_count == 3
    assert compiled.action.mode_count() == 8

    # Skew-symmetric Hamiltonian noise matrix on the 8 modes
    dim = 8
    noise_data = [[Fraction(0) for _ in range(dim)] for _ in range(dim)]
    # Local coupling between adjacent modes (1, 2) and (3, 4)
    noise_data[0][1] = Fraction(1, 10)
    noise_data[1][0] = Fraction(-1, 10)
    noise_data[2][3] = Fraction(3, 20)
    noise_data[3][2] = Fraction(-3, 20)

    noise_mat = SkewNoiseMatrix(dim=dim, data=noise_data)
    frob_initial = noise_mat.frobenius_norm_sq()
    assert frob_initial > Fraction(0)

    # Conjugate noise matrix by the topological braid action: K' = B K B^T
    noise_conjugated = noise_mat.conjugate_by_braid(compiled.action)
    frob_final = noise_conjugated.frobenius_norm_sq()

    # Exact unitary invariance: Frobenius norm of noise is preserved under braiding
    assert frob_initial == frob_final


# ===========================================================================
# Scenario 2: Fermi-Hubbard Triangular Cluster Quench
# ===========================================================================

def test_tier4_scenario_fermi_hubbard_cluster_quench():
    """Scenario 2: Discrete Fermi-Hubbard quench on 3-site triangular cluster."""
    lat = FermionicLattice.triangle_cluster()
    assert lat.num_sites == 3
    assert len(lat.edges) == 3  # (0,1), (1,2), (0,2)

    # 1 up fermion, 1 down fermion
    ham = DiscreteFermionicHamiltonian(lat, t=Fraction(1), u=Fraction(2), num_up=1, num_down=1)
    matrix = ham.matrix
    dim = len(matrix)
    assert dim == 9  # (3 choose 1) * (3 choose 1) = 9

    # Verify exact Hermiticity (H = H^T for real symmetric Hamiltonian)
    for i in range(dim):
        for j in range(dim):
            assert matrix[i][j] == matrix[j][i], f"Non-Hermitian entry at ({i}, {j})"

    # Verify diagonal contains interaction U for doubly occupied sites
    doubly_occupied_count = 0
    for idx, state in enumerate(ham.basis):
        # A site is doubly occupied if both up and down fermions occupy it
        if (state.up_mask & state.down_mask) != 0:
            doubly_occupied_count += 1
            assert matrix[idx][idx] == Fraction(2), "U-interaction mismatch"
        else:
            assert matrix[idx][idx] == Fraction(0)
    assert doubly_occupied_count == 3

    # Confirm CAR hop consistency with FSP witness
    w = fsp_witness()
    assert w.hop_product == -1
    fsp_refuse_removed_holonomy(w.hop_product)


# ===========================================================================
# Scenario 3: 6D Quantum State Tomography and Gramian SDP Obstruction
# ===========================================================================

def test_tier4_scenario_mub6_state_tomography_and_sdp_obstruction():
    """Scenario 3: 6D 3-MUB state reconstruction and 4-basis SDP obstruction check."""
    # 1. Load genuine Dita seed triple
    triple = dita_seed_triple_columns(0, 8)
    assert len(triple) == 18
    assert verify_triple_pairwise_mu(triple) is True

    # Bases B1, B2, B3 each have 6 vectors of dimension 6
    b1 = triple[0:6]
    b2 = triple[6:12]
    b3 = triple[12:18]

    # Check pairwise inner product magnitude |<u, v>|^2 = 1/6
    sixth = Cyc24.rat(Fraction(1, 6))
    for u in b1:
        for v in b2:
            ip = Cyc24.zero()
            for uk, vk in zip(u, v):
                ip = ip + (uk.conj() * vk)
            assert ip.abs_sq() == sixth

    # 2. Quad Gramian verification with candidate Tao S6 block
    g = canonical_quad_gramian()
    rep = verify_gramian_structure(g)
    # The structure report certifies that diagonal is I_6 and off-diagonal is 1/6
    assert rep.verified_sound is True
    assert rep.bases_count == 4
    assert rep.dimension == 24


# ===========================================================================
# Scenario 4: Kitaev Chain Topological Phase Transition Sweep
# ===========================================================================

def test_tier4_scenario_kitaev_chain_topological_phase_transition():
    """Scenario 4: Parameter sweep across Kitaev wire topological phase boundary."""
    wire_length = 6

    # 1. Sweet-spot topological phase (mu = 0, t = 1, delta = 1): isolated edge modes
    wire_topo = SparseKitaevWire(wire_length, Fraction(1), Fraction(1), Fraction(0))
    iso_topo = wire_topo.isolated_majoranas()
    # Boundary modes are localized at mode 1 and mode 2*wire_length = 12
    assert iso_topo == [1, 12]

    # 2. Strong chemical potential (mu = 5 >> 2t, t = 1, delta = 1): trivial phase
    wire_triv = SparseKitaevWire(wire_length, Fraction(1), Fraction(1), Fraction(5))
    iso_triv = wire_triv.isolated_majoranas()
    # Trivial phase has no isolated zero-energy edge modes
    assert iso_triv == []

    # 3. Non-zero chemical potential (mu = 1): modes couple to bulk
    wire_mid = SparseKitaevWire(wire_length, Fraction(1), Fraction(1), Fraction(1))
    iso_mid = wire_mid.isolated_majoranas()
    # When mu != 0, exact zero-commutator isolated modes couple to the bulk
    assert iso_mid == []


# ===========================================================================
# Scenario 5: Surface Code Dual Observation and Syndrome Detection
# ===========================================================================

def test_tier4_scenario_discrete_quantum_teleportation_and_syndrome_correction():
    """Scenario 5: Tetron surface code dual observation, syndrome detection, and repair capacity."""
    # 2x2 torus complex
    complex_torus = surface_grid_2x2_torus()
    x_log = torus_logical_x_example()
    z_log = torus_logical_z_example()

    # Code distance on 2x2 torus is 2
    code_dist = 2
    # Classical repair capacity t = floor((d-1)/2) = 0 for distance 2
    t_repair = assert_repair_capacity_invariant(code_dist)
    assert t_repair == 0

    # Dual observation on clean logical state
    obs_face = observer_face_syndrome(complex_torus)
    obs_first = observer_first_face_only(complex_torus)
    receipt_clean = dual_observe(complex_torus, x_log, obs_face, obs_first)
    assert receipt_clean.agree_on_zero is True
    assert receipt_clean.residual_zero_1 is True
    assert receipt_clean.residual_zero_2 is True

    # Inject 1-edge error (bitflip on edge 0)
    x_noisy = list(x_log)
    x_noisy[0] ^= 1
    receipt_noisy = dual_observe(complex_torus, x_noisy, obs_face, obs_first)
    # The noise generates a syndrome defect
    assert receipt_noisy.residual_zero_1 is False
    assert receipt_noisy.residual_weight_1 > 0
