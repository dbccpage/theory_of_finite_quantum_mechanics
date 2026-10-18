"""test_su2_link_holonomy_4d.py: Tests for Non-Abelian SU(2) Link Holonomy & Gauge Updates on T^4 (L >= 8).

Validates:
1. Exact rational SU(2) quaternion arithmetic, group laws, non-abelian commutators, and center elements.
2. 4D lattice gauge field on L >= 8 tori (8x8x4x4 and 8x8x8x8).
3. Exact gauge invariance of Wilson action under local non-abelian gauge transformations Omega(x).
4. Local link holonomy updates with exact rational action changes Delta S_W.
5. Discrete second Chern topological charge density and orientation flip tau.
6. Coupling to 4D topological cluster solver with zero duality gap.
7. Zero-float enforcement and AST cleanliness.

AuthorityEffect: None.
"""

from __future__ import annotations

import ast
from fractions import Fraction
from pathlib import Path
import sys
import pytest

_CODE_DIR = Path(__file__).resolve().parent.parent / "code"
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))

from su2_link_holonomy_4d import (
    HalfInstantonCenter4D,
    HalfInstantonCluster4D,
    LatticeGaugeField4D,
    RationalSU2,
    SU2TopologicalClusterCoupler,
    orientation_flip,
)


def test_rational_su2_group_laws():
    """Validates quaternion group axioms, inverses, traces, and non-abelian algebra."""
    id_u = RationalSU2.identity()
    neg_id = RationalSU2.minus_identity()
    assert id_u.trace() == Fraction(2, 1)
    assert neg_id.trace() == Fraction(-2, 1)
    assert id_u.is_center()
    assert neg_id.is_center()

    # Generators
    ui = RationalSU2.from_generators(1)
    uj = RationalSU2.from_generators(2)
    uk = RationalSU2.from_generators(3)

    # Quaternion multiplication: i^2 = j^2 = k^2 = -1
    assert ui * ui == neg_id
    assert uj * uj == neg_id
    assert uk * uk == neg_id

    # Non-abelian algebra: i*j = k, j*i = -k
    assert ui * uj == uk
    assert uj * ui == RationalSU2.from_generators(3, sign=-1)

    # Commutator [i, j] != 0
    assert ui * uj != uj * ui

    # Inverses / Daggers
    assert ui * ui.dagger() == id_u
    assert uj * uj.dagger() == id_u
    assert uk * uk.dagger() == id_u


def test_rational_su2_stereographic_projection():
    """Validates stereographic construction from arbitrary rational 3-vectors."""
    u1 = RationalSU2.from_stereographic(Fraction(1, 2), Fraction(1, 3), Fraction(1, 4))
    assert u1 * u1.dagger() == RationalSU2.identity()
    assert isinstance(u1.a0, Fraction)
    assert isinstance(u1.a1, Fraction)
    assert isinstance(u1.a2, Fraction)
    assert isinstance(u1.a3, Fraction)

    # Origin maps to identity
    u_origin = RationalSU2.from_stereographic(0, 0, 0)
    assert u_origin == RationalSU2.identity()

    # Tetrahedral group elements
    u_tet = RationalSU2.from_tetrahedral(1, 1, 1, 1)
    assert u_tet * u_tet.dagger() == RationalSU2.identity()
    assert u_tet.trace() == Fraction(1, 1)


def test_lattice_gauge_field_dimensions_validation():
    """Validates that lattice requires max dimension >= 8 and 4-tuple of lengths."""
    # L < 8 must raise ValueError
    with pytest.raises(ValueError, match="At least one lattice dimension must be >= 8"):
        LatticeGaugeField4D((4, 4, 4, 4))

    # L >= 8 valid
    field_8844 = LatticeGaugeField4D((8, 8, 4, 4))
    assert field_8844.volume == 8 * 8 * 4 * 4  # 1024

    field_8888 = LatticeGaugeField4D((8, 8, 8, 8))
    assert field_8888.volume == 8 * 8 * 8 * 8  # 4096


def test_cold_start_wilson_action():
    """Validates that identity configuration has identically zero Wilson action."""
    field = LatticeGaugeField4D((8, 8, 4, 4))
    for x in [(0, 0, 0, 0), (7, 7, 3, 3), (4, 4, 2, 2)]:
        for mu in range(4):
            for nu in range(mu + 1, 4):
                assert field.plaquette(x, mu, nu) == RationalSU2.identity()
                assert field.plaquette_action(x, mu, nu) == Fraction(0, 1)

    assert field.total_wilson_action() == Fraction(0, 1)


def test_local_gauge_invariance():
    """Validates that random non-abelian local gauge transformations leave action strictly invariant."""
    field = LatticeGaugeField4D((8, 8, 4, 4))

    # Set several non-trivial link holonomies
    u_rot = RationalSU2.from_stereographic(Fraction(1, 2), Fraction(0, 1), Fraction(1, 3))
    field.set_link((1, 1, 1, 1), 0, u_rot)
    field.set_link((1, 2, 1, 1), 1, RationalSU2.from_generators(2))

    action_before = field.total_wilson_action()
    assert action_before > Fraction(0, 1)

    # Define site gauge transformations Omega(x)
    omega_map = {
        (1, 1, 1, 1): RationalSU2.from_generators(1),
        (2, 1, 1, 1): RationalSU2.from_stereographic(Fraction(1, 4), Fraction(1, 2), Fraction(0, 1)),
        (1, 2, 1, 1): RationalSU2.from_tetrahedral(1, -1, 1, -1),
    }

    # Apply local gauge transformation
    field.local_gauge_transform(omega_map)

    action_after = field.total_wilson_action()
    # Gauge invariance: S_W[U'] == S_W[U]
    assert action_after == action_before


def test_link_holonomy_update_delta_action():
    """Validates that local link update computes exact change in action Delta S_W."""
    field = LatticeGaugeField4D((8, 8, 4, 4))
    action_initial = field.total_wilson_action()
    assert action_initial == Fraction(0, 1)

    # Propose rotation on link ((2, 3, 1, 0), 2)
    x_target = (2, 3, 1, 0)
    mu_target = 2
    rotation = RationalSU2.from_stereographic(Fraction(1, 3), Fraction(1, 3), Fraction(0, 1))

    delta_s = field.update_link(x_target, mu_target, rotation)

    action_updated = field.total_wilson_action()
    assert delta_s == action_updated - action_initial
    assert delta_s > Fraction(0, 1)


def test_topological_charge_density_and_involution_tau():
    """Validates discrete topological charge density and orientation reversal tau."""
    field = LatticeGaugeField4D((8, 8, 4, 4))

    # Insert localized half-instanton
    c_p = HalfInstantonCenter4D(coords=(2, 2, 1, 1), chirality=1)
    field.insert_localized_half_instanton(c_p)

    q_total = field.total_second_chern_number()
    assert q_total == Fraction(1, 2)

    # Orientation flip tau
    field_flipped = field.orientation_flip()
    q_flipped = field_flipped.total_second_chern_number()
    # Orientation flip must invert topological charge sign
    assert q_flipped == -Fraction(1, 2)


def test_topological_cluster_solver_coupling_on_8x8x4x4():
    """Validates coupling of 4D topological cluster solver to SU(2) gauge field on 8x8x4x4 lattice."""
    field = LatticeGaugeField4D((8, 8, 4, 4))
    coupler = SU2TopologicalClusterCoupler(field)

    # Construct paired centers: 3 odd pairs + 3 neutral clusters
    c1 = HalfInstantonCenter4D((0, 0, 0, 0), 1)
    pair1 = coupler.create_paired_odd_cluster(c1, Fraction(100, 1))

    c2 = HalfInstantonCenter4D((1, 1, 0, 0), 1)
    pair2 = coupler.create_paired_odd_cluster(c2, Fraction(60, 1))

    c3 = HalfInstantonCenter4D((2, 0, 1, 0), 1)
    pair3 = coupler.create_paired_odd_cluster(c3, Fraction(40, 1))

    # Neutral clusters
    c4 = HalfInstantonCluster4D(n_plus=1, n_minus=1, weight=Fraction(180, 1), centers=())
    c5 = HalfInstantonCluster4D(n_plus=2, n_minus=2, weight=Fraction(120, 1), centers=())
    c6 = HalfInstantonCluster4D(n_plus=0, n_minus=0, weight=Fraction(150, 1), centers=())

    ensemble = [pair1[0], pair1[1], pair2[0], pair2[1], pair3[0], pair3[1], c4, c5, c6]
    res = coupler.solve_gauge_coupled_cancellation(ensemble)

    assert res["status"] == "EXACT_REPAIR"
    assert res["duality_gap"] == Fraction(0, 1)
    assert res["total_partition_sum"] == 450
    assert res["pairs_cancelled"] == 3
    assert res["lattice_dimensions"] == (8, 8, 4, 4)
    assert res["lattice_volume"] == 1024


def test_zero_float_ast_cleanliness():
    """Scans su2_link_holonomy_4d.py AST to guarantee zero floating point usage."""
    src_file = Path(__file__).resolve().parent.parent / "code" / "su2_link_holonomy_4d.py"
    assert src_file.is_file(), f"Missing source file: {src_file}"

    tree = ast.parse(src_file.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            pytest.fail(f"Forbidden float constant {node.value} at line {node.lineno}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
            pytest.fail(f"Forbidden float() cast at line {node.lineno}")
