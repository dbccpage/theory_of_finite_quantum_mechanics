"""PD → Regge walk: 0-simplex to leftovers, one admission at a time.

Same cadence as the primitive-difference walk, on a simplicial complex.
AuthorityEffect: None. Stdlib only (math for regular-simplex dihedrals).

Toy model. Consistency is the contract: later rungs consume earlier
state. Nothing is PDG. When we cannot continue without a new extra,
that extra is named as a lift and the walk stops or records it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


def l1(v: tuple[int, ...]) -> int:
    return sum(abs(x) for x in v)


def d0(alpha: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = alpha
    return (b - a, c - b, a - c)


def phi_triangle(omega: tuple[int, int, int]) -> int:
    """Exact integer quotient residual for the oriented triangle.

    ``im(d0)`` is the set of integer triples with zero oriented sum,
    hence the quotient residual is exactly ``abs(sum(omega))``.
    """
    return abs(sum(omega))


@dataclass(frozen=True)
class Rung:
    index: int
    name: str
    simplex_dim: int
    admitted: tuple[str, ...]
    lifts_not_taken: tuple[str, ...]
    payload: dict[str, Any]


@dataclass
class Walk:
    rungs: list[Rung] = field(default_factory=list)

    def last(self) -> Rung:
        return self.rungs[-1]

    def payload(self, key: str) -> Any:
        for rung in reversed(self.rungs):
            if key in rung.payload:
                return rung.payload[key]
        raise KeyError(key)


def rung0_two_points() -> Rung:
    """Challenge 0: two 0-simplices, a primitive difference, no geometry."""
    left, right = 1, -1
    delta = right - left
    return Rung(
        index=0,
        name="0-simplex: primitive difference",
        simplex_dim=0,
        admitted=("two loci", "integer values"),
        lifts_not_taken=("metric", "Hilbert space", "continuum"),
        payload={
            "left": left,
            "right": right,
            "delta": delta,
            "first_fire": l1((delta,)),
        },
    )


def rung1_edge(prev: Rung) -> Rung:
    """1-simplex: the two loci become the boundary of an edge. Φ is |delta|."""
    delta = int(prev.payload["delta"])
    first_fire = int(prev.payload["first_fire"])
    omega_edge = (delta,)
    phi = l1(omega_edge)
    assert phi == first_fire
    return Rung(
        index=1,
        name="1-simplex: transport and residual",
        simplex_dim=1,
        admitted=("edge", "coboundary as difference"),
        lifts_not_taken=("connection", "Lie algebra"),
        payload={
            "omega_edge": omega_edge,
            "phi_edge": phi,
            "unit": first_fire,
        },
    )


def lr_reachable(n_vertices: int, source: int, ticks: int) -> frozenset[int]:
    """Local update of radius 1: after t ticks, graph-distance ≤ t.

    Companion GR-001 Proposition 3.1. This is the Lieb-Robinson cone
    on a path. v_LR = 1 edge per tick. Not Lorentz invariance.
    """
    return frozenset(
        i for i in range(n_vertices) if abs(i - source) <= ticks
    )


def causal_speed_analogy(unit: int, holonomy: int, loop_inertia: int) -> dict[str, Any]:
    """Record assigned toy speeds and dimensionless comparisons.

    The graph cone proves only a speed bound of one edge per tick.  This
    function does not construct photon or W/Z dynamics, a dispersion
    relation, or an electromagnetic coupling.  Its speed assignments and
    inverse-coupling expressions are explicitly interpretive inputs.
    """
    v_lr = 1
    inertia_edge = loop_inertia // 3
    v_massive_num = unit
    v_massive_den = unit + inertia_edge
    d = 1.0 - 9.0 / (math.pi ** 2)
    alpha_inv_4pi = (4.0 * math.pi) / d
    return {
        "lr_speed_bound": v_lr,
        "propagation_dynamics_constructed": False,
        "assigned_massless_mode_speed": v_lr,
        "assigned_massless_mode_mass": 0,
        "assigned_inertial_mode_per_edge": inertia_edge,
        "assigned_inertial_mode_speed_num": v_massive_num,
        "assigned_inertial_mode_speed_den": v_massive_den,
        "named_inverse_coupling_lattice": 6 * v_lr,
        "named_inverse_coupling_3cycle_4pi": alpha_inv_4pi,
        "inverse_fine_structure_reference_2022": 137.035999177,
        "coupling_identification_proved": False,
        "phase_class": holonomy,
    }


def d1(omega: tuple[int, int, int]) -> int:
    """Filled face: coboundary of a 1-cochain is the sum of oriented edges."""
    return omega[0] + omega[1] + omega[2]


def face_inertia(omega: tuple[int, int, int]) -> int:
    """||d1* d1 ω||_1. Zero on coboundaries (sum 0). Positive on the loop (1,1,1)."""
    s = d1(omega)
    return l1((s, s, s))


def rung2_triangle(prev: Rung) -> Rung:
    """2-simplex face-attachment fixture with explicit interpretation fences.

    The checked facts are the H1 rank drop and positive loop stiffness.
    Historical Higgs/W/Z/photon names are retained only as analogy labels;
    no electroweak fields, representations, or dynamics are constructed.
    """
    unit = int(prev.payload["unit"])
    omega = (unit, 0, 0)
    phi = phi_triangle(omega)
    exact = (unit, unit, -2 * unit)
    phi_exact = phi_triangle(exact)
    deficit_k5 = 6 - 5
    holonomy = deficit_k5 % 6
    loop = (1, 1, 1)
    return Rung(
        index=2,
        name="2-simplex: face attachment and edge-loop stiffness",
        simplex_dim=2,
        admitted=("face", "d0", "d1", "2d equilateral deficit"),
        lifts_not_taken=("Hermitian SU(3)", "Higgs quartic"),
        payload={
            "omega_triangle": omega,
            "phi_triangle": phi,
            "phi_exact": phi_exact,
            "mass_gap": phi - phi_exact,
            "deficit_2d_units": deficit_k5,
            "u1_holonomy": holonomy,
            "unit": unit,
            "hollow_h1_rank": 1,
            "filled_h1_rank": 0,
            "face_attachment_increases_loop_stiffness": True,
            "physical_identifications_proved": False,
            "analogy_labels": {
                "face": "Higgs",
                "edges": ("W+", "W-", "Z"),
                "deficit_phase": "photon",
            },
            "loop_inertia_hollow": 0,
            "loop_inertia_filled": face_inertia(loop),
            "exact_inertia_filled": face_inertia(exact),
            **causal_speed_analogy(unit, holonomy, face_inertia(loop)),
        },
    )


def rung3_tetrahedron(prev: Rung) -> Rung:
    """3-simplex: SU(2) kinematics + 3d hinge deficit. Regular tetra extra."""
    unit = int(prev.payload["unit"])
    spins = (2, 2, 2, 2, 2, 2)
    from regge_climb import su2_tetra_admissible

    admissible = su2_tetra_admissible(spins)
    theta = math.acos(1.0 / 3.0)
    k_flat = 2.0 * math.pi / theta
    k = 5
    epsilon_3d = 2.0 * math.pi - k * theta
    return Rung(
        index=3,
        name="3-simplex: SU(2) and 3d deficit",
        simplex_dim=3,
        admitted=("tetrahedron", "SU(2) face triads", "regular tetra dihedral"),
        lifts_not_taken=("Ponzano-Regge continuum limit", "SU(3) Hermitian"),
        payload={
            "su2_spins": spins,
            "su2_admissible": admissible,
            "dihedral_cos": (1, 3),
            "k_flat_3d": k_flat,
            "epsilon_3d": epsilon_3d,
            "unit": unit,
        },
    )


def rung4_four_simplex(prev: Rung) -> Rung:
    """4-simplex: 4d hinge deficit. Λ_toy = mean |ε| in first-fire units."""
    unit = int(prev.payload["unit"])
    eps3 = float(prev.payload["epsilon_3d"])
    theta4 = math.acos(1.0 / 4.0)
    k_flat4 = 2.0 * math.pi / theta4
    k = 5
    epsilon_4d = 2.0 * math.pi - k * theta4
    n_under, n_flat = 5, 5
    mean_abs_eps = (n_under * abs(epsilon_4d) + n_flat * 0.0) / (n_under + n_flat)
    lambda_toy = mean_abs_eps / unit
    return Rung(
        index=4,
        name="4-simplex: 4d deficit and cosmological constant leftover",
        simplex_dim=4,
        admitted=("4-simplex", "regular 4-simplex dihedral"),
        lifts_not_taken=("Einstein equation", "continuum volume form"),
        payload={
            "epsilon_4d": epsilon_4d,
            "k_flat_4d": k_flat4,
            "lambda_toy": lambda_toy,
            "epsilon_3d_replayed": eps3,
            "unit": unit,
        },
    )


def leftovers(walk: Walk) -> dict[str, Any]:
    """Toy residuals plus non-derivational historical analogy labels."""
    unit = int(walk.payload("unit"))
    phi_tri = int(walk.payload("phi_triangle"))
    phi_exact = int(walk.payload("phi_exact"))
    holonomy = int(walk.payload("u1_holonomy"))
    lambda_toy = float(walk.payload("lambda_toy"))
    inexact_residual = phi_tri / unit
    isolated_edge_residual = unit / unit
    return {
        "inexact_cochain_residual_natural": inexact_residual,
        "inexact_cochain_residual_raw": phi_tri,
        "exact_cochain_residual": phi_exact,
        "isolated_edge_residual_natural": isolated_edge_residual,
        "isolated_edge_residual_raw": unit,
        "deficit_phase_class": holonomy,
        "mean_4d_deficit_natural": lambda_toy,
        "unit_first_fire": unit,
        "h1_rank_drop": (1, 0),
        "physical_identifications_proved": False,
        "analogy_labels": {
            "inexact_cochain": "neutrino",
            "isolated_edge": "dark matter",
            "mean_4d_deficit": "dark energy",
            "face": "Higgs",
            "edges": ("W+", "W-", "Z"),
            "deficit_phase": "photon",
        },
        "lr_speed_bound": int(walk.payload("lr_speed_bound")),
        "propagation_dynamics_constructed": bool(
            walk.payload("propagation_dynamics_constructed")
        ),
        "assigned_massless_mode_speed": int(
            walk.payload("assigned_massless_mode_speed")
        ),
        "assigned_inertial_mode_speed_num": int(
            walk.payload("assigned_inertial_mode_speed_num")
        ),
        "assigned_inertial_mode_speed_den": int(
            walk.payload("assigned_inertial_mode_speed_den")
        ),
        "named_inverse_coupling_lattice": int(
            walk.payload("named_inverse_coupling_lattice")
        ),
        "named_inverse_coupling_3cycle_4pi": float(
            walk.payload("named_inverse_coupling_3cycle_4pi")
        ),
        "coupling_identification_proved": False,
        "next_lifts": (
            "Hermitian SU(3)",
            "Higgs quartic",
            "continuum Einstein",
            "MSSM superpartners",
        ),
    }


def run_walk() -> tuple[Walk, dict[str, Any]]:
    w = Walk()
    w.rungs.append(rung0_two_points())
    w.rungs.append(rung1_edge(w.last()))
    w.rungs.append(rung2_triangle(w.last()))
    w.rungs.append(rung3_tetrahedron(w.last()))
    w.rungs.append(rung4_four_simplex(w.last()))
    return w, leftovers(w)


def walk_is_consistent(w: Walk) -> bool:
    """Later rungs replay the first-fire unit. No 246, no 360."""
    unit = w.rungs[0].payload["first_fire"]
    if unit != 2:
        return False
    if w.rungs[1].payload["phi_edge"] != unit:
        return False
    if w.rungs[2].payload["unit"] != unit:
        return False
    if w.rungs[3].payload["unit"] != unit:
        return False
    if w.rungs[4].payload["unit"] != unit:
        return False
    blob = str(w)
    return not ("246" in blob or "360" in blob)
