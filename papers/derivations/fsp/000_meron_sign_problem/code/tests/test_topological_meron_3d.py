"""Unit tests for 3D topological meron string loops, winding parity, and linking pairing.

Verifies:
1. 3D spatial lattice on 3-torus T^3 (periodic boundary conditions, L=4, V=64 sites).
2. Closed 1D loop curves composed of oriented directed edges with periodic coordinates.
3. Exact winding vector W(c) in Z^3 by tracking coordinate boundary wraparounds.
4. Topological winding parity I(c) = (Wx + Wy + Wz) mod 2 in {0, 1}.
5. Exact integer linking pairing Lk(c1, c2) in Z via discrete Gauss linking and
   oriented cross-facet intersection counting (symmetry Lk(c2, c1) == Lk(c1, c2),
   orientation reversal Lk(c1, -c2) == -Lk(c1, c2), Lk=0 for unlinked loops).
6. Cluster involution tau flipping orientation on odd-winding loops c -> -c with
   sigma(tau(c)) = -sigma(c), w(tau(c)) = w(c), and (1 + (-1)) w(c) = 0.
7. Zero floats: int and fractions.Fraction exclusively.

AuthorityEffect: None.
"""

from __future__ import annotations

import ast
from fractions import Fraction
from pathlib import Path

import pytest

from topological_meron_3d import (
    ClosedStringLoop3D,
    Lattice3D,
    build_hopf_link_pair,
    build_plaquette_loop,
    build_unlinked_pair,
    build_winding_loop,
    cluster_involution_tau,
    create_meron_cluster_configuration,
    discrete_gauss_linking_number,
    evaluate_cluster_partition_sum,
    exact_linking_matrix,
    facet_intersection_linking_number,
    linking_number,
    loop_involution_tau,
    verify_involution_cancellation,
    winding_parity,
)


def test_lattice_3d_geometry_and_wrapping():
    """Verify 3D lattice dimensions, volume, and minimal coordinate step unwrapping."""
    lattice = Lattice3D((4, 4, 4))
    assert lattice.lx == 4
    assert lattice.ly == 4
    assert lattice.lz == 4
    assert lattice.volume == 64

    assert lattice.wrap_coordinate((4, 0, 0)) == (0, 0, 0)
    assert lattice.wrap_coordinate((-1, 5, 8)) == (3, 1, 0)

    step_fwd = lattice.nearest_neighbor_step((3, 1, 2), (0, 1, 2))
    assert step_fwd == (1, 0, 0)

    step_bwd = lattice.nearest_neighbor_step((0, 1, 2), (3, 1, 2))
    assert step_bwd == (-1, 0, 0)

    step_norm = lattice.nearest_neighbor_step((1, 2, 3), (2, 2, 3))
    assert step_norm == (1, 0, 0)


def test_contractible_plaquette_loops():
    """Verify that planar plaquette loops have zero winding W = (0, 0, 0) and parity I = 0."""
    loop_xy = build_plaquette_loop("xy", origin=(0, 0, 0), size=1, lattice_dim=(4, 4, 4))
    assert loop_xy.winding_vector == (0, 0, 0)
    assert loop_xy.winding_parity == 0
    assert loop_xy.is_contractible is True
    assert winding_parity(loop_xy) == 0

    loop_yz = build_plaquette_loop("yz", origin=(1, 1, 1), size=2, lattice_dim=(4, 4, 4))
    assert loop_yz.winding_vector == (0, 0, 0)
    assert loop_yz.winding_parity == 0
    assert loop_yz.is_contractible is True

    loop_zx = build_plaquette_loop("zx", origin=(2, 0, 1), size=1, lattice_dim=(4, 4, 4))
    assert loop_zx.winding_vector == (0, 0, 0)
    assert loop_zx.winding_parity == 0


def test_winding_loops_along_axes():
    """Verify loops winding around T^3 axes have non-trivial winding W in Z^3 and correct parity I(c)."""
    wx_loop = build_winding_loop("x", offset=(0, 1, 1), steps=4, direction=1)
    assert wx_loop.winding_vector == (1, 0, 0)
    assert wx_loop.winding_parity == 1
    assert wx_loop.is_contractible is False

    wy_loop = build_winding_loop("y", offset=(2, 0, 1), steps=4, direction=1)
    assert wy_loop.winding_vector == (0, 1, 0)
    assert wy_loop.winding_parity == 1

    wz_loop = build_winding_loop("z", offset=(1, 2, 0), steps=4, direction=1)
    assert wz_loop.winding_vector == (0, 0, 1)
    assert wz_loop.winding_parity == 1

    wx_rev = build_winding_loop("x", offset=(0, 1, 1), steps=4, direction=-1)
    assert wx_rev.winding_vector == (-1, 0, 0)
    assert wx_rev.winding_parity == 1

    diag_pts = [(k % 4, k % 4, 0) for k in range(4)]
    diag_loop = ClosedStringLoop3D(id="diag_loop", coordinates=diag_pts, lattice_dim=(4, 4, 4))
    assert diag_loop.winding_vector == (1, 1, 0)
    assert diag_loop.winding_parity == 0


def test_unwrapped_path_and_homology():
    """Verify unwrapped path displacements in Z^3 match winding vector W * L."""
    plaq = build_plaquette_loop("xy", origin=(1, 1, 1), size=2, lattice_dim=(4, 4, 4))
    unwrapped_plaq = plaq.unwrapped_coordinates()
    assert unwrapped_plaq[0] == (1, 1, 1)
    assert unwrapped_plaq[-1] == (1, 1, 1)

    w_loop = build_winding_loop("x", offset=(0, 0, 0), steps=4, lattice_dim=(4, 4, 4))
    unwrapped_w = w_loop.unwrapped_coordinates()
    assert unwrapped_w[0] == (0, 0, 0)
    assert unwrapped_w[-1] == (4, 0, 0)


def test_linking_number_unlinked_loops():
    """Verify unlinked disjoint loops evaluate to Lk = 0 symmetrically."""
    l1, l2 = build_unlinked_pair(lattice_dim=(6, 6, 6))

    lk_12 = linking_number(l1, l2)
    lk_21 = linking_number(l2, l1)

    assert lk_12 == 0
    assert lk_21 == 0
    assert isinstance(lk_12, int)


def test_linking_number_hopf_link_and_symmetries():
    """Verify discrete Hopf link evaluates to Lk = +/- 1 with exact integer symmetry and orientation flip."""
    h1, h2 = build_hopf_link_pair(origin=(1, 1, 1), lattice_dim=(6, 6, 6))

    lk_12 = linking_number(h1, h2)
    lk_21 = linking_number(h2, h1)

    assert abs(lk_12) == 1
    assert isinstance(lk_12, int)

    assert lk_12 == lk_21

    h2_rev = h2.reversed()
    lk_rev2 = linking_number(h1, h2_rev)
    assert lk_rev2 == -lk_12

    h1_rev = h1.reversed()
    lk_rev1 = linking_number(h1_rev, h2)
    assert lk_rev1 == -lk_12

    lk_rev_both = linking_number(h1_rev, h2_rev)
    assert lk_rev_both == lk_12


def test_facet_intersection_linking_number():
    """Verify oriented cross-facet intersection counting matches discrete Gauss linking."""
    h1, h2 = build_hopf_link_pair(origin=(1, 1, 1), lattice_dim=(6, 6, 6))

    lk_facet = facet_intersection_linking_number(h1, h2)
    lk_gauss = discrete_gauss_linking_number(h1, h2)

    assert abs(lk_facet) == 1
    assert lk_facet == lk_gauss

    h2_rev = h2.reversed()
    lk_facet_rev = facet_intersection_linking_number(h1, h2_rev)
    assert lk_facet_rev == -lk_facet

    u1, u2 = build_unlinked_pair(lattice_dim=(6, 6, 6))
    assert facet_intersection_linking_number(u1, u2) == 0


def test_exact_linking_matrix_symmetry():
    """Verify that exact_linking_matrix produces a symmetric integer matrix with zero diagonal."""
    h1, h2 = build_hopf_link_pair(origin=(1, 1, 1), lattice_dim=(6, 6, 6))
    u1, u2 = build_unlinked_pair(lattice_dim=(6, 6, 6))

    loops = [h1, h2, u1, u2]
    mat = exact_linking_matrix(loops)

    assert len(mat) == 4
    for i in range(4):
        assert len(mat[i]) == 4
        assert mat[i][i] == 0
        for j in range(4):
            assert mat[i][j] == mat[j][i]
            assert isinstance(mat[i][j], int)

    assert abs(mat[0][1]) == 1
    assert abs(mat[1][0]) == 1

    assert mat[0][2] == 0
    assert mat[0][3] == 0
    assert mat[1][2] == 0
    assert mat[1][3] == 0
    assert mat[2][3] == 0


def test_loop_involution_tau_single_meron():
    """Verify that loop involution tau: c -> -c reverses orientation and inverts winding vector."""
    meron_loop = build_winding_loop("x", offset=(0, 1, 2), steps=4, direction=1)
    assert meron_loop.winding_vector == (1, 0, 0)
    assert meron_loop.winding_parity == 1

    tau_loop = loop_involution_tau(meron_loop)
    assert tau_loop.winding_vector == (-1, 0, 0)
    assert tau_loop.winding_parity == 1

    tau_tau_loop = loop_involution_tau(tau_loop)
    assert tau_tau_loop.winding_vector == (1, 0, 0)
    assert tau_tau_loop.winding_parity == 1


def test_cluster_involution_pairwise_cancellation():
    """Verify cluster involution tau satisfies sigma(tau(C)) = -sigma(C), w(tau(C)) = w(C), and (1 + (-1)) w(C) = 0."""
    m_loop = build_winding_loop("x", offset=(0, 0, 0), steps=4)
    p_loop = build_plaquette_loop("xy", origin=(1, 1, 1), size=1)

    weight = Fraction(3, 4)
    config = create_meron_cluster_configuration([m_loop, p_loop], orientations=[1, 1], base_weight=weight)

    assert config.has_meron is True
    assert config.sign == 1
    assert config.base_weight == Fraction(3, 4)

    receipt = verify_involution_cancellation(config)
    assert receipt["has_meron"] is True
    assert receipt["cancelling"] is True
    assert receipt["is_involution"] is True
    assert receipt["sign_reverses"] is True
    assert receipt["weight_preserved"] is True
    assert receipt["pair_sum"] == "0"
    assert receipt["zero_gap_certified"] is True
    assert receipt["status"] == "EXACT_REPAIR"

    partner = cluster_involution_tau(config)
    assert partner.sign == -1
    assert partner.base_weight == config.base_weight
    zero_sum = config.sign * config.base_weight + partner.sign * partner.base_weight
    assert zero_sum == Fraction(0)


def test_cluster_partition_sum_odd_sector_vanishing():
    """Verify partition sum over all 2^k configurations vanishes in odd sector and remains strictly positive in even sector."""
    m1 = build_winding_loop("x", offset=(0, 0, 0), steps=4)
    m2 = build_winding_loop("y", offset=(0, 0, 1), steps=4)
    p1 = build_plaquette_loop("xy", origin=(2, 2, 2), size=1)

    result_odd = evaluate_cluster_partition_sum([m1, m2, p1], base_weight=Fraction(5, 2))
    assert result_odd["total_configurations"] == 8
    assert result_odd["has_meron"] is True
    assert result_odd["positive_configurations"] == 4
    assert result_odd["negative_configurations"] == 4
    assert result_odd["odd_sector_vanishes"] is True
    assert result_odd["odd_sector_sum"] == "0"
    assert result_odd["exact_partition_z"] == "0"

    p_a = build_plaquette_loop("xy", origin=(0, 0, 0), size=1)
    p_b = build_plaquette_loop("yz", origin=(2, 2, 2), size=1)

    result_even = evaluate_cluster_partition_sum([p_a, p_b], base_weight=Fraction(3, 1))
    assert result_even["total_configurations"] == 4
    assert result_even["has_meron"] is False
    assert result_even["positive_configurations"] == 4
    assert result_even["negative_configurations"] == 0
    assert result_even["even_sector_sum"] == "12"
    assert result_even["exact_partition_z"] == "12"


def test_zero_floats_enforcement():
    """Assert ZERO float conversions exist in topological_meron_3d.py via AST analysis and runtime type auditing."""
    src_path = Path(__file__).resolve().parents[1] / "topological_meron_3d.py"
    with src_path.open("r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(src_path))

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            assert not isinstance(node.value, float), f"Forbidden float literal found: {node.value}"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "float":
                pytest.fail("Forbidden call to float() constructor found in topological_meron_3d.py")

    h1, h2 = build_hopf_link_pair(origin=(1, 1, 1), lattice_dim=(6, 6, 6))
    lk = linking_number(h1, h2)
    assert isinstance(lk, int) and not isinstance(lk, float)

    wp = winding_parity(h1)
    assert isinstance(wp, int) and not isinstance(wp, float)

    config = create_meron_cluster_configuration([h1, h2], orientations=[1, 1], base_weight=Fraction(1, 2))
    assert isinstance(config.base_weight, Fraction) and not isinstance(config.base_weight, float)
    assert isinstance(config.sign, int) and not isinstance(config.sign, float)
