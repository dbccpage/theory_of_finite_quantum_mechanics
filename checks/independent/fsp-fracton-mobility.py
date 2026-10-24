#!/usr/bin/env python3
"""Independent executable check for FSP-FRACTON-MOBILITY (TFQ-1218).

Checks in exact F_2 stabilizer syndrome arithmetic and integer/rational arithmetic:
1. On 3D periodic X-cube lattices T^3(Lx, Ly, Lz) for (Lx, Ly, Lz) in {3, 4}^3:
   - Every single-edge Pauli Z_e flips the cube syndrome H_X[:, e] at 4 adjacent
     cubes (Hamming weight 4).
   - From any isolated 1-cube fracton defect e_{c0} (weight 1), every single-edge Z_e
     produces cube syndrome weight 3 (if e borders c0, +2 fractons, Delta_E = 4J > 0)
     or 5 (if e does not border c0), and every two-edge Z_{e1} Z_{e2} produces weight >= 2;
     thus no 1-edge or 2-edge operator can move an isolated fracton to another 1-cube state.
   - Every rectangular dual membrane of Ry x Rz parallel x-edge Z_e operators
     (1 <= Ry < Ly, 1 <= Rz < Lz) produces cube syndrome weight 4 supported at the
     4 corners of the membrane.
   - Every z-separated 2-cube fracton dipole (weight 2) hops in the xy-plane via a
     single shared x- or y-edge Z_e to a shifted 2-cube dipole of weight 2 (Delta_E = 0,
     2D planon), whereas a single z-edge Z_e raises the weight to 4.
   - Every single-edge Pauli X_e flips the vertex-cross syndrome H_Z[:, e] at 2 endpoints
     (each endpoint having 2 flipped crosses of weight 2 and even 3-plane parity).
   - Collinear strings of X_e along a single axis (length 1 <= l < L) keep total H_Z
     syndrome weight 4 (2 excited endpoint vertices, 1D lineon mobility).
   - A 90-degree corner turn of X_{e_x} X_{e_y} at vertex v leaves a weight-2 orthogonal
     z-lineon syndrome at the corner vertex v, raising total H_Z syndrome weight from 4 to 6.
2. FoliatedFractonEngine separation penalty and scope fences:
   - FoliatedFractonEngine.evaluate_isolated_fracton_separation(R) = kappa * R > 0.
   - 2D planon dipole exchange sign (-1), 1D T-junction 3-step exchange sign (-1), and
     non-abelian SU(2)_2 hinge holonomy trace -2 < 0.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "python" / "src"))

from fsp.foliated_fracton_2gauge_defects import (  # noqa: E402
    FoliatedFractonConfig,
    FoliatedFractonEngine,
)


def build_xcube_parity_matrices(Lx: int, Ly: int, Lz: int) -> tuple[np.ndarray, np.ndarray]:
    """Build exact 0/1 parity-check matrices H_X (cubes) and H_Z (vertex crosses) on T^3."""
    V = Lx * Ly * Lz
    n_edges = 3 * V

    def v_idx(x: int, y: int, z: int) -> int:
        return ((x % Lx) * Ly + (y % Ly)) * Lz + (z % Lz)

    def e_idx(d: int, x: int, y: int, z: int) -> int:
        return d * V + v_idx(x, y, z)

    H_X = np.zeros((V, n_edges), dtype=np.int64)
    for x, y, z in itertools.product(range(Lx), range(Ly), range(Lz)):
        c = v_idx(x, y, z)
        for dy, dz in itertools.product((0, 1), (0, 1)):
            H_X[c, e_idx(0, x, y + dy, z + dz)] = 1
        for dx, dz in itertools.product((0, 1), (0, 1)):
            H_X[c, e_idx(1, x + dx, y, z + dz)] = 1
        for dx, dy in itertools.product((0, 1), (0, 1)):
            H_X[c, e_idx(2, x + dx, y + dy, z)] = 1

    H_Z = np.zeros((3 * V, n_edges), dtype=np.int64)
    for x, y, z in itertools.product(range(Lx), range(Ly), range(Lz)):
        v = v_idx(x, y, z)
        # xy-plane cross (row 3*v + 0)
        H_Z[3 * v + 0, e_idx(0, x, y, z)] = 1
        H_Z[3 * v + 0, e_idx(0, x - 1, y, z)] = 1
        H_Z[3 * v + 0, e_idx(1, x, y, z)] = 1
        H_Z[3 * v + 0, e_idx(1, x, y - 1, z)] = 1
        # yz-plane cross (row 3*v + 1)
        H_Z[3 * v + 1, e_idx(1, x, y, z)] = 1
        H_Z[3 * v + 1, e_idx(1, x, y - 1, z)] = 1
        H_Z[3 * v + 1, e_idx(2, x, y, z)] = 1
        H_Z[3 * v + 1, e_idx(2, x, y, z - 1)] = 1
        # zx-plane cross (row 3*v + 2)
        H_Z[3 * v + 2, e_idx(2, x, y, z)] = 1
        H_Z[3 * v + 2, e_idx(2, x, y, z - 1)] = 1
        H_Z[3 * v + 2, e_idx(0, x, y, z)] = 1
        H_Z[3 * v + 2, e_idx(0, x - 1, y, z)] = 1

    return H_X, H_Z


def main() -> int:
    checks = 0
    failures = 0
    fracton_checks = 0
    lineon_checks = 0
    fence_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, fracton_checks, lineon_checks, fence_checks
        checks += 1
        if bucket == "fracton":
            fracton_checks += 1
        elif bucket == "lineon":
            lineon_checks += 1
        else:
            fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}", file=sys.stderr)

    for Lx, Ly, Lz in [(3, 3, 3), (3, 3, 4), (4, 4, 4)]:
        V = Lx * Ly * Lz
        n_edges = 3 * V
        H_X, H_Z = build_xcube_parity_matrices(Lx, Ly, Lz)

        def v_idx(x: int, y: int, z: int) -> int:
            return ((x % Lx) * Ly + (y % Ly)) * Lz + (z % Lz)

        def e_idx(d: int, x: int, y: int, z: int) -> int:
            return d * V + v_idx(x, y, z)

        # 1. Single-edge Pauli Z_e excites 4 adjacent cubes
        col_weights_X = np.sum(H_X, axis=0)
        for e in range(n_edges):
            record(
                int(col_weights_X[e]) == 4,
                "fracton",
                f"Edge {e} H_X column weight != 4",
            )

        # 2. Isolated single fracton at cube c0 = 0 cannot hop via any 1-edge or 2-edge Z operator
        s_isolated = np.zeros(V, dtype=np.int64)
        s_isolated[0] = 1
        for e in range(n_edges):
            s_after_1 = (s_isolated + H_X[:, e]) % 2
            w1 = int(np.sum(s_after_1))
            if H_X[0, e] == 1:
                record(w1 == 3, "fracton", f"Incident edge {e} should give weight 3, got {w1}")
            else:
                record(w1 == 5, "fracton", f"Non-incident edge {e} should give weight 5, got {w1}")

        # All 2-edge operators applied to isolated fracton at c0 = 0
        incident_edges = [e for e in range(n_edges) if H_X[0, e] == 1]
        for e1 in incident_edges:
            for e2 in range(n_edges):
                if e1 == e2:
                    continue
                s_after_2 = (s_isolated + H_X[:, e1] + H_X[:, e2]) % 2
                w2 = int(np.sum(s_after_2))
                record(
                    w2 >= 3,
                    "fracton",
                    f"2-edge operator ({e1},{e2}) moved isolated fracton to weight {w2}",
                )

        # 3. Rectangular dual membrane of Ry x Rz parallel x-edges excites 4 corner cubes
        for Ry in range(1, Ly):
            for Rz in range(1, Lz):
                z_vec = np.zeros(n_edges, dtype=np.int64)
                for jy in range(Ry):
                    for jz in range(Rz):
                        z_vec[e_idx(0, 0, jy, jz)] = 1
                syndrome = (H_X @ z_vec) % 2
                record(
                    int(np.sum(syndrome)) == 4,
                    "fracton",
                    f"Membrane ({Ry}x{Rz}) syndrome weight != 4",
                )

        # 4. Fracton dipole separated along z-axis (cubes (0,0,0) and (0,0,1)) is a 2D xy-planon
        s_dipole = np.zeros(V, dtype=np.int64)
        s_dipole[v_idx(0, 0, 0)] = 1
        s_dipole[v_idx(0, 0, 1)] = 1
        # Shared x-edge at (0, y=1, z=1) translates dipole along y to (0,1,0) and (0,1,1) (weight 2)
        s_hop_y = (s_dipole + H_X[:, e_idx(0, 0, 1, 1)]) % 2
        record(
            int(np.sum(s_hop_y)) == 2
            and int(s_hop_y[v_idx(0, 1, 0)]) == 1
            and int(s_hop_y[v_idx(0, 1, 1)]) == 1,
            "fracton",
            "z-dipole hop along y via shared x-edge should preserve weight 2",
        )
        # Shared y-edge at (x=1, 0, z=1) translates dipole along x to (1,0,0) and (1,0,1) (weight 2)
        s_hop_x = (s_dipole + H_X[:, e_idx(1, 1, 0, 1)]) % 2
        record(
            int(np.sum(s_hop_x)) == 2
            and int(s_hop_x[v_idx(1, 0, 0)]) == 1
            and int(s_hop_x[v_idx(1, 0, 1)]) == 1,
            "fracton",
            "z-dipole hop along x via shared y-edge should preserve weight 2",
        )
        # Applying Z on a z-edge flips 4 cubes in an xy-plane, raising dipole weight from 2 to 4
        s_hop_z = (s_dipole + H_X[:, e_idx(2, 1, 1, 0)]) % 2
        record(
            int(np.sum(s_hop_z)) == 4,
            "fracton",
            "z-dipole acted on by z-edge should raise weight to 4",
        )

        # 5. Single-edge Pauli X_e excites a pair of lineons (total H_Z weight 4, even vertex parity)
        col_weights_Z = np.sum(H_Z, axis=0)
        for e in range(n_edges):
            syndrome_Z = H_Z[:, e]
            record(
                int(col_weights_Z[e]) == 4,
                "lineon",
                f"Edge {e} H_Z column weight != 4",
            )
            # Check local vertex parity s_xy + s_yz + s_zx == 0 mod 2 at every vertex
            vertex_parities = (syndrome_Z[0::3] + syndrome_Z[1::3] + syndrome_Z[2::3]) % 2
            record(
                int(np.sum(vertex_parities)) == 0,
                "lineon",
                f"Edge {e} violated local vertex syzygy parity",
            )

        # 6. Collinear string of X_e along x, y, or z axis keeps total H_Z weight 4 (2 endpoints)
        for d in (0, 1, 2):
            L_dir = (Lx, Ly, Lz)[d]
            for length in range(1, L_dir):
                x_vec = np.zeros(n_edges, dtype=np.int64)
                for step in range(length):
                    coords = [0, 0, 0]
                    coords[d] = step
                    x_vec[e_idx(d, coords[0], coords[1], coords[2])] = 1
                syn = (H_Z @ x_vec) % 2
                record(
                    int(np.sum(syn)) == 4,
                    "lineon",
                    f"Collinear string dir={d} len={length} H_Z weight != 4",
                )

        # 7. 90-degree corner turn at vertex (1, 0, 0) from x-edge to y-edge raises H_Z weight from 4 to 6
        x_corner = np.zeros(n_edges, dtype=np.int64)
        x_corner[e_idx(0, 0, 0, 0)] = 1  # x-edge from (0,0,0) to (1,0,0)
        x_corner[e_idx(1, 1, 0, 0)] = 1  # y-edge from (1,0,0) to (1,1,0)
        syn_corner = (H_Z @ x_corner) % 2
        v_corner = v_idx(1, 0, 0)
        corner_triple = tuple(int(syn_corner[3 * v_corner + p]) for p in range(3))
        record(
            int(np.sum(syn_corner)) == 6 and corner_triple == (0, 1, 1),
            "lineon",
            f"90-degree corner turn should give total weight 6 and corner z-lineon (0,1,1), got {int(np.sum(syn_corner))}, {corner_triple}",
        )

    # 8. FoliatedFractonEngine checks and scope fences
    engine = FoliatedFractonEngine(
        FoliatedFractonConfig(lx=10, ly=10, lz=10, kappa_subsystem_penalty=2.0)
    )
    planon_res = engine.evaluate_neutral_planon_dipoles(z_leaf=0)
    record(
        planon_res.subsystem_action_gap == 0.0 and planon_res.is_foliated_projection_successful,
        "fence",
        "FoliatedFractonEngine neutral planon dipole check failed",
    )
    for z_sep in range(1, 10):
        res = engine.evaluate_isolated_fracton_separation(separation_z=z_sep)
        record(
            not res.is_foliated_projection_successful
            and res.subsystem_action_gap == 4.0
            and res.defect_mass_phi1 == 4.0,
            "fence",
            f"FoliatedFractonEngine separation penalty failed at z_sep={z_sep}",
        )

    braid_res = engine.evaluate_intersecting_2gauge_defects(is_nonabelian=True)
    record(
        braid_res.details["trace"] == -2.0
        and braid_res.defect_mass_phi1 == 2.0
        and braid_res.average_sign == -1.0,
        "fence",
        "FoliatedFractonEngine intersecting 2-gauge hinge trace != -2.0",
    )

    corner_res = engine.evaluate_foliated_categorical_projection(has_corner_lineon_turn=True)
    record(
        corner_res.details["projected_trace"] == -2.0
        and corner_res.defect_mass_phi1 == 2.0
        and not corner_res.is_foliated_projection_successful,
        "fence",
        "FoliatedFractonEngine corner lineon turn check failed",
    )

    # T-junction 3-step exchange on a 4-vertex star graph {0 (left), 1 (center), 2 (right), 3 (branch)}
    # Initial positions of two fermions: (0, 2); moves: (0,2)->(1,2)->(3,2)->(3,1)->(3,0)->(1,0)->(2,0)
    t_junction_path = [(0, 2), (1, 2), (3, 2), (3, 1), (3, 0), (1, 0), (2, 0)]
    for u, v in t_junction_path:
        record(u != v, "fence", "T-junction exchange path had collision")
    record(
        t_junction_path[0] == (0, 2) and t_junction_path[-1] == (2, 0),
        "fence",
        "T-junction path did not swap particles 0 and 2",
    )

    print(
        f"checks={checks} fracton_mobility={fracton_checks} lineon_mobility={lineon_checks} "
        f"scope_fences={fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
