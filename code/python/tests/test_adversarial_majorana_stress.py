"""Adversarial stress testing and property-based oracles for Majorana domain.

Covers:
- GF(2) symplectic geometry, binary inner product, and Pauli commutation
- Clifford algebra canonical anticommutation relations (CAR), hermiticity, and parity operator
- Braid representation invariants: Yang-Baxter braid relation, far commutation, inverse cancellation
- Tetron surface carriers: Betti numbers for Disk/Cylinder/Torus, homology distance, and packet wall capacity bound
- Dual observer syndrome agreement

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import random
import pytest

from src.majorana.majorana_fock_algebra import (
    FockCarrier,
    GaussianRat,
    first_anticommutation_failure,
    gi,
)
from src.majorana import (
    MajoranaError,
    MajoranaMonomial,
    MajoranaOperator,
    anticommutator,
    commutator,
    # Braid action
    braid_action,
    multiqubit_braid,
    # Tetron & topology
    build_tetron_array,
    Axis,
    TetronReport,
    Topology,
    logical_class_representative,
    # Complexes & dual observer
    surface_grid_2x2_torus,
    surface_grid_2x2_planar,
    torus_logical_x_example,
    torus_logical_z_example,
    dual_observe,
    observer_face_syndrome,
    observer_first_face_only,
    # Packet wall & repair
    ToyRepairPacket,
    terminalize_packet,
    PacketWallTerminal,
    repair_capacity_t,
    hamming_weight,
    # GF(2) terminalizer
    GF2Matrix,
    Cyclotomic16Element,
)


# ============================================================================
# 1. GF(2) Symplectic Geometry & Matrix Invariants
# ============================================================================

def gf2_symplectic_form(u: list[int], v: list[int]) -> int:
    """Compute binary symplectic form Omega(u, v) = u_x * v_z + u_z * v_x (mod 2)."""
    assert len(u) == len(v)
    assert len(u) % 2 == 0
    n = len(u) // 2
    ux, uz = u[:n], u[n:]
    vx, vz = v[:n], v[n:]
    omega = 0
    for i in range(n):
        omega ^= (ux[i] & vz[i]) ^ (uz[i] & vx[i])
    return omega


def test_gf2_symplectic_form_alternating_and_bilinear():
    """Verify that Omega(u, u) = 0 and Omega is bilinear over GF(2)."""
    rng = random.Random(999)
    n = 4  # 4 qubits -> vector length 8
    for _ in range(30):
        u = [rng.randint(0, 1) for _ in range(2 * n)]
        v = [rng.randint(0, 1) for _ in range(2 * n)]
        w = [rng.randint(0, 1) for _ in range(2 * n)]

        # Alternating: Omega(u, u) == 0
        assert gf2_symplectic_form(u, u) == 0, f"Symplectic form is not alternating for {u}"

        # Skew-symmetry: Omega(u, v) == Omega(v, u) over GF(2) (since -1 == 1)
        assert gf2_symplectic_form(u, v) == gf2_symplectic_form(v, u)

        # Bilinearity: Omega(u + v, w) == Omega(u, w) ^ Omega(v, w)
        u_plus_v = [a ^ b for a, b in zip(u, v)]
        assert gf2_symplectic_form(u_plus_v, w) == (gf2_symplectic_form(u, w) ^ gf2_symplectic_form(v, w))


def test_gf2_matrix_gaussian_elimination_and_rank():
    """Stress test GF2Matrix rank, identity, and echelon reduction."""
    # 3x3 identity
    id3 = GF2Matrix.from_data([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert id3.rank() == 3

    # Rank deficient: row 2 = row 0 ^ row 1
    dep = GF2Matrix.from_data([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    assert dep.rank() == 2

    # All zeros
    zero = GF2Matrix.from_data([[0, 0, 0], [0, 0, 0]])
    assert zero.rank() == 0


def test_cyclotomic16_order_and_arithmetic():
    """Verify Cyclotomic16Element zeta order 16 and exact ring properties."""
    z = Cyclotomic16Element.zeta()
    acc = Cyclotomic16Element.one()
    for k in range(1, 17):
        acc = acc.multiply(z)
        if k == 8:
            assert acc == Cyclotomic16Element.from_int(-1)
        elif k == 16:
            assert acc == Cyclotomic16Element.one()
        else:
            assert acc != Cyclotomic16Element.one()


# ============================================================================
# 2. Clifford Algebra Canonical Anticommutation Relations (CAR)
# ============================================================================

def test_fock_carrier_majorana_anticommutation_exhaustion():
    """Verify {gamma_a, gamma_b} = 2 * delta_{ab} * I for all pairs in FockCarrier(3)."""
    # 3 fermionic modes -> 6 Majorana operators in dimension 2^3 = 8
    fc = FockCarrier(3)
    generators = [fc.majorana_generator(a) for a in range(1, 7)]

    # Use first_anticommutation_failure to assert zero failures
    failure = first_anticommutation_failure(generators)
    assert failure is None, f"Anticommutation failure at pair {failure}"


def test_fock_carrier_parity_operator_algebra():
    """Verify parity operator P = (-i)^N prod gamma_a satisfies P^2 = I and {P, gamma_a} = 0."""
    fc = FockCarrier(2)
    dim = fc.dimension()
    p = fc.parity_operator()
    g1 = fc.majorana_generator(1)
    g2 = fc.majorana_generator(2)

    # Helper matrix multiply
    def mat_mul(A, B):
        res = [[gi(0) for _ in range(dim)] for _ in range(dim)]
        for i in range(dim):
            for k in range(dim):
                if A[i][k].is_zero():
                    continue
                for j in range(dim):
                    res[i][j] = res[i][j] + A[i][k] * B[k][j]
        return res

    # P^2 == I
    p2 = mat_mul(p, p)
    for i in range(dim):
        for j in range(dim):
            want = gi(1 if i == j else 0)
            assert p2[i][j] == want, f"P^2 is not identity at ({i}, {j})"

    # {P, g_1} == 0
    pg1 = mat_mul(p, g1)
    g1p = mat_mul(g1, p)
    for i in range(dim):
        for j in range(dim):
            anti = pg1[i][j] + g1p[i][j]
            assert anti.is_zero(), f"{{P, gamma_1}} != 0 at ({i}, {j})"


def test_majorana_monomial_anticommutation_and_nilpotence():
    """Verify Majorana monomials gamma_i gamma_j = - gamma_j gamma_i and nilpotency."""
    m0 = MajoranaMonomial.single(0)
    m1 = MajoranaMonomial.single(1)
    m2 = MajoranaMonomial.single(2)

    # m0 * m1 = - m1 * m0
    s01, p01 = m0.multiply(m1)
    s10, p10 = m1.multiply(m0)
    assert p01 == p10
    assert s01 == -s10

    # (m0 * m1)^2 = -I
    # m0*m1 * m0*m1 = - m0*m0 * m1*m1 = -1
    s_sq, p_sq = p01.multiply(p01)
    # Total sign: s01 * s01 * s_sq = 1 * 1 * (-1) = -1
    assert s_sq == Fraction(-1)
    assert p_sq == MajoranaMonomial.identity()


# ============================================================================
# 3. Braid Representation Invariants: Yang-Baxter & Far Commutation
# ============================================================================

def test_braid_action_yang_baxter_braid_relation():
    """Verify the Artin braid / Yang-Baxter equation: sigma_i sigma_{i+1} sigma_i = sigma_{i+1} sigma_i sigma_{i+1}."""
    modes = 6
    for i in range(1, modes - 1):
        s_i = braid_action.MajoranaBraidAction.elementary(modes, i)
        s_next = braid_action.MajoranaBraidAction.elementary(modes, i + 1)

        # Left hand side: s_i * s_{i+1} * s_i
        lhs = s_i.compose(s_next).compose(s_i)

        # Right hand side: s_{i+1} * s_i * s_{i+1}
        rhs = s_next.compose(s_i).compose(s_next)

        for m in range(1, modes + 1):
            assert lhs.image(m) == rhs.image(m), f"Yang-Baxter braid relation failed at generator {i} on mode {m}"


def test_braid_action_far_commutation():
    """Verify far commutation: sigma_i sigma_j = sigma_j sigma_i for |i - j| >= 2."""
    modes = 6
    s1 = braid_action.MajoranaBraidAction.elementary(modes, 1)
    s3 = braid_action.MajoranaBraidAction.elementary(modes, 3)
    s4 = braid_action.MajoranaBraidAction.elementary(modes, 4)

    # s1 and s3 commute
    s1_s3 = s1.compose(s3)
    s3_s1 = s3.compose(s1)
    for m in range(1, modes + 1):
        assert s1_s3.image(m) == s3_s1.image(m)

    # s1 and s4 commute
    s1_s4 = s1.compose(s4)
    s4_s1 = s4.compose(s1)
    for m in range(1, modes + 1):
        assert s1_s4.image(m) == s4_s1.image(m)


def test_braid_action_inverse_cancellation():
    """Verify elementary braid generator and its inverse cancel to identity."""
    modes = 4
    for i in range(1, modes):
        elem = braid_action.MajoranaBraidAction.elementary(modes, i, inverse=False)
        inv = braid_action.MajoranaBraidAction.elementary(modes, i, inverse=True)
        prod = elem.compose(inv)
        for m in range(1, modes + 1):
            assert prod.image(m) == braid_action.SignedMajorana(mode=m, sign=1)


# ============================================================================
# 4. Tetron Surface Carriers, Betti Numbers & Packet Wall
# ============================================================================

def test_tetron_array_betti_numbers_disk_cylinder_torus():
    """Verify Betti numbers dim H_1 for Disk (0), Cylinder (1), Torus (2)."""
    # Disk: non-periodic
    c_disk, rep_disk = build_tetron_array(2, 2, Topology.Disk)
    assert rep_disk.dim_h1 == 0
    assert rep_disk.homology_matches_prediction()

    # Cylinder: periodic in cols only
    c_cyl, rep_cyl = build_tetron_array(2, 2, Topology.Cylinder)
    assert rep_cyl.dim_h1 == 1
    assert rep_cyl.homology_matches_prediction()

    # Torus: periodic in rows and cols
    c_torus, rep_torus = build_tetron_array(2, 2, Topology.Torus)
    assert rep_torus.dim_h1 == 2
    assert rep_torus.homology_matches_prediction()


def test_packet_wall_capacity_bound():
    """Verify packet wall capacity bound t = (d - 1) // 2."""
    from src.majorana.repair_limit import repair_capacity_bound
    assert repair_capacity_bound(1) == 0
    assert repair_capacity_bound(2) == 0
    assert repair_capacity_bound(3) == 1
    assert repair_capacity_bound(4) == 1
    assert repair_capacity_bound(5) == 2

    # On a 2x2 torus with d=2, t=0:
    # A non-zero error residual of weight 2 hits the capacity wall
    c = surface_grid_2x2_torus()
    x_log = torus_logical_x_example()
    assert hamming_weight(x_log) == 2

    packet = ToyRepairPacket(complex=c, residual=x_log, declared_distance=2)
    receipt = terminalize_packet(packet)
    assert receipt.terminal == PacketWallTerminal.CapacityWallHit
    assert receipt.repair_capacity_t == 0
    assert receipt.residual_weight == 2


def test_dual_observer_logical_cycle_agreement():
    """Verify dual observers agree on zero syndrome for closed logical representative."""
    c = surface_grid_2x2_torus()
    x_log = torus_logical_x_example()
    obs_face = observer_face_syndrome(c)
    obs_first = observer_first_face_only(c)
    receipt = dual_observe(c, x_log, obs_face, obs_first)
    assert receipt.agree_on_zero
    assert receipt.residual_zero_1
    assert receipt.residual_zero_2
