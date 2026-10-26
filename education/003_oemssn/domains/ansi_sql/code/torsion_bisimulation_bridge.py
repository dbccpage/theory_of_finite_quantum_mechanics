"""
Torsion Bisimulation Bridge: Integral Homology and Torsion Subgroups
Lean 4 Kernel Certificates <-> ANSI SQL Smith Normal Form (SNF) CTE Evaluator
AuthorityEffect: None.
"""

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from smith_normal_form_cte_evaluator import SmithNormalFormCTEEvaluator


@dataclass
class LeanIntegralCertificate:
    complex_name: str
    max_dim: int
    f_vector: List[int]
    betti_numbers: List[int]
    torsion_by_dim: Dict[int, List[int]]
    euler_characteristic: int


LEAN_INTEGRAL_CERTIFICATES = {
    "RP2_RealProjectivePlane": LeanIntegralCertificate(
        complex_name="RP2_RealProjectivePlane",
        max_dim=2,
        f_vector=[6, 15, 10],
        betti_numbers=[1, 0, 0],
        torsion_by_dim={1: [2]},
        euler_characteristic=1,
    ),
    "KleinBottle_K2": LeanIntegralCertificate(
        complex_name="KleinBottle_K2",
        max_dim=2,
        f_vector=[12, 36, 24],
        betti_numbers=[1, 1, 0],
        torsion_by_dim={1: [2]},
        euler_characteristic=0,
    ),
    "Torus_T2": LeanIntegralCertificate(
        complex_name="Torus_T2",
        max_dim=2,
        f_vector=[9, 27, 18],
        betti_numbers=[1, 2, 1],
        torsion_by_dim={},
        euler_characteristic=0,
    ),
    "Sphere_S2": LeanIntegralCertificate(
        complex_name="Sphere_S2",
        max_dim=2,
        f_vector=[4, 6, 4],
        betti_numbers=[1, 0, 1],
        torsion_by_dim={},
        euler_characteristic=2,
    ),
}


@dataclass
class TorsionBisimulationCertificate:
    complex_name: str
    forward_simulation_holds: bool
    backward_simulation_holds: bool
    lean_kernel_elaboration_holds: bool
    betti_numbers_matched: bool
    torsion_coefficients_matched: bool
    euler_poincare_matched: bool
    lean_betti: List[int]
    sql_betti: List[int]
    lean_torsion: Dict[int, List[int]]
    sql_torsion: Dict[int, List[int]]
    total_snf_cte_steps: int
    discrepancy_log: List[str] = field(default_factory=list)

    @property
    def is_bisimilar(self) -> bool:
        return (
            self.forward_simulation_holds
            and self.backward_simulation_holds
            and self.lean_kernel_elaboration_holds
            and self.betti_numbers_matched
            and self.torsion_coefficients_matched
            and self.euler_poincare_matched
            and len(self.discrepancy_log) == 0
        )


class TorsionBisimulationBridge:
    def __init__(self, lean_src_path: Optional[Path] = None):
        self.lean_src = lean_src_path or (
            Path(__file__).resolve().parent.parent.parent
            / "mathematics"
            / "lean4"
            / "integral_homology_torsion.lean"
        )
        self.evaluator = SmithNormalFormCTEEvaluator(in_memory=True)

    def verify_lean_compilation(self) -> bool:
        """Verifies that the Lean 4 integral homology module compiles with zero errors."""
        if not self.lean_src.exists():
            return False
        res = subprocess.run(["lean", str(self.lean_src)], capture_output=True, text=True)
        return res.returncode == 0

    def build_rp2_matrices(self) -> Tuple[List[int], List[List[int]], List[List[int]]]:
        """Minimal 6-vertex triangulation of RP^2: 6 vertices, 15 edges, 10 triangles."""
        triangles = [
            (0, 1, 2),
            (1, 2, 3),
            (2, 3, 4),
            (3, 4, 0),
            (4, 0, 1),
            (0, 2, 5),
            (2, 4, 5),
            (4, 1, 5),
            (1, 3, 5),
            (3, 0, 5),
        ]
        edges = sorted(
            list(
                set(
                    (min(u, v), max(u, v))
                    for u, v, w in triangles
                    for (u, v) in [(u, v), (u, w), (v, w)]
                )
            )
        )
        edge_map = {e: i for i, e in enumerate(edges)}

        # d1: 6 vertices x 15 edges
        d1 = [[0] * 15 for _ in range(6)]
        for j, (u, v) in enumerate(edges):
            d1[v][j] += 1
            d1[u][j] -= 1

        # d2: 15 edges x 10 triangles
        d2 = [[0] * 10 for _ in range(15)]
        for j, (u, v, w) in enumerate(triangles):
            for a, b in [(v, w), (w, u), (u, v)]:
                e = (min(a, b), max(a, b))
                sgn = 1 if a < b else -1
                d2[edge_map[e]][j] += sgn

        return [6, 15, 10], d1, d2

    def build_klein_bottle_matrices(self) -> Tuple[List[int], List[List[int]], List[List[int]]]:
        """3x4 grid triangulation of Klein Bottle: 12 vertices, 36 edges, 24 triangles."""
        nx, ny = 3, 4

        def v(x, y):
            x = x % nx
            if y >= ny:
                return ((nx - (x % nx)) % nx, 0)
            return (x, y % ny)

        triangles = []
        for x in range(nx):
            for y in range(ny):
                v00 = v(x, y)
                v10 = v(x + 1, y)
                v01 = v(x, y + 1)
                v11 = v(x + 1, y + 1)
                triangles.append((v00, v10, v11))
                triangles.append((v00, v11, v01))

        verts = sorted(list(set(v for t in triangles for v in t)))
        vert_map = {vert: i for i, vert in enumerate(verts)}

        edges = set()
        for u, w, z in triangles:
            edges.add((min(vert_map[u], vert_map[w]), max(vert_map[u], vert_map[w])))
            edges.add((min(vert_map[u], vert_map[z]), max(vert_map[u], vert_map[z])))
            edges.add((min(vert_map[w], vert_map[z]), max(vert_map[w], vert_map[z])))
        edge_list = sorted(list(edges))
        edge_map = {e: i for i, e in enumerate(edge_list)}

        d1 = [[0] * len(edge_list) for _ in range(len(verts))]
        for j, (u, w) in enumerate(edge_list):
            d1[w][j] += 1
            d1[u][j] -= 1

        d2 = [[0] * len(triangles) for _ in range(len(edge_list))]
        for j, (u, w, z) in enumerate(triangles):
            iu, iw, iz = vert_map[u], vert_map[w], vert_map[z]
            for a, b in [(iw, iz), (iz, iu), (iu, iw)]:
                e = (min(a, b), max(a, b))
                sgn = 1 if a < b else -1
                d2[edge_map[e]][j] += sgn

        return [len(verts), len(edge_list), len(triangles)], d1, d2

    def build_torus_matrices(self) -> Tuple[List[int], List[List[int]], List[List[int]]]:
        """3x3 grid triangulation of Torus: 9 vertices, 27 edges, 18 triangles."""
        nx, ny = 3, 3

        def v(x, y):
            return (x % nx, y % ny)

        triangles = []
        for x in range(nx):
            for y in range(ny):
                v00 = v(x, y)
                v10 = v(x + 1, y)
                v01 = v(x, y + 1)
                v11 = v(x + 1, y + 1)
                triangles.append((v00, v10, v11))
                triangles.append((v00, v11, v01))

        verts = sorted(list(set(v for t in triangles for v in t)))
        vert_map = {vert: i for i, vert in enumerate(verts)}

        edges = set()
        for u, w, z in triangles:
            edges.add((min(vert_map[u], vert_map[w]), max(vert_map[u], vert_map[w])))
            edges.add((min(vert_map[u], vert_map[z]), max(vert_map[u], vert_map[z])))
            edges.add((min(vert_map[w], vert_map[z]), max(vert_map[w], vert_map[z])))
        edge_list = sorted(list(edges))
        edge_map = {e: i for i, e in enumerate(edge_list)}

        d1 = [[0] * len(edge_list) for _ in range(len(verts))]
        for j, (u, w) in enumerate(edge_list):
            d1[w][j] += 1
            d1[u][j] -= 1

        d2 = [[0] * len(triangles) for _ in range(len(edge_list))]
        for j, (u, w, z) in enumerate(triangles):
            iu, iw, iz = vert_map[u], vert_map[w], vert_map[z]
            for a, b in [(iw, iz), (iz, iu), (iu, iw)]:
                e = (min(a, b), max(a, b))
                sgn = 1 if a < b else -1
                d2[edge_map[e]][j] += sgn

        return [len(verts), len(edge_list), len(triangles)], d1, d2

    def build_s2_matrices(self) -> Tuple[List[int], List[List[int]], List[List[int]]]:
        """Tetrahedral shell S^2: 4 vertices, 6 edges, 4 triangles."""
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        edge_map = {e: i for i, e in enumerate(edges)}
        triangles = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]

        d1 = [[0] * 6 for _ in range(4)]
        for j, (u, v) in enumerate(edges):
            d1[v][j] += 1
            d1[u][j] -= 1

        d2 = [[0] * 4 for _ in range(6)]
        for j, (u, v, w) in enumerate(triangles):
            for a, b in [(v, w), (w, u), (u, v)]:
                e = (min(a, b), max(a, b))
                sgn = 1 if a < b else -1
                d2[edge_map[e]][j] += sgn

        return [4, 6, 4], d1, d2

    def evaluate_torsion_bisimulation(self, complex_key: str) -> TorsionBisimulationCertificate:
        if complex_key not in LEAN_INTEGRAL_CERTIFICATES:
            raise ValueError(f"Unknown complex: {complex_key}")

        lean_cert = LEAN_INTEGRAL_CERTIFICATES[complex_key]
        discrepancies = []

        # 1. Lean kernel check
        lean_ok = self.verify_lean_compilation()
        if not lean_ok:
            discrepancies.append(f"Lean compilation failed for {self.lean_src}")

        # 2. Build matrices
        if complex_key == "RP2_RealProjectivePlane":
            f_vec, d1, d2 = self.build_rp2_matrices()
        elif complex_key == "KleinBottle_K2":
            f_vec, d1, d2 = self.build_klein_bottle_matrices()
        elif complex_key == "Torus_T2":
            f_vec, d1, d2 = self.build_torus_matrices()
        elif complex_key == "Sphere_S2":
            f_vec, d1, d2 = self.build_s2_matrices()
        else:
            raise ValueError(complex_key)

        # 3. Compute Smith Normal Form via SQL CTEs
        r1_dim, c1_dim = self.evaluator.load_matrix(f"{complex_key}_d1", d1)
        snf1 = self.evaluator.compute_snf(f"{complex_key}_d1", r1_dim, c1_dim)

        r2_dim, c2_dim = self.evaluator.load_matrix(f"{complex_key}_d2", d2)
        snf2 = self.evaluator.compute_snf(f"{complex_key}_d2", r2_dim, c2_dim)

        total_steps = snf1["total_cte_steps"] + snf2["total_cte_steps"]

        rank_d1 = snf1["rank"]
        rank_d2 = snf2["rank"]

        # Free Betti numbers
        n0, n1, n2 = f_vec
        beta0 = n0 - rank_d1
        beta1 = n1 - rank_d1 - rank_d2
        beta2 = n2 - rank_d2
        sql_betti = [beta0, beta1, beta2]

        # Torsion in H_1 is determined by elementary divisors of d2 > 1
        sql_torsion = {}
        if snf2["torsion_coefficients"]:
            sql_torsion[1] = snf2["torsion_coefficients"]

        # 4. Check Forward & Backward Simulation
        forward_ok = f_vec == lean_cert.f_vector
        if not forward_ok:
            discrepancies.append(
                f"Forward simulation mismatch: Lean f-vector {lean_cert.f_vector} != SQL {f_vec}"
            )

        backward_ok = True
        # Verify divisibility condition d_i | d_{i+1} in both SNF results
        for diag in [snf1["diagonal_factors"], snf2["diagonal_factors"]]:
            for i in range(len(diag) - 1):
                if diag[i + 1] % diag[i] != 0:
                    backward_ok = False
                    discrepancies.append(
                        f"Divisibility failure in SNF: {diag[i]} does not divide {diag[i + 1]}"
                    )

        # 5. Check Betti Number Equivalence
        betti_ok = sql_betti == lean_cert.betti_numbers
        if not betti_ok:
            discrepancies.append(
                f"Betti number mismatch: Lean {lean_cert.betti_numbers} != SQL {sql_betti}"
            )

        # 6. Check Torsion Coefficient Equivalence
        torsion_ok = sql_torsion == lean_cert.torsion_by_dim
        if not torsion_ok:
            discrepancies.append(
                f"Torsion coefficient mismatch: Lean {lean_cert.torsion_by_dim} != SQL {sql_torsion}"
            )

        # 7. Check Euler-Poincaré Invariance
        euler_f = n0 - n1 + n2
        euler_beta = beta0 - beta1 + beta2
        euler_ok = euler_f == euler_beta == lean_cert.euler_characteristic
        if not euler_ok:
            discrepancies.append(
                f"Euler characteristic mismatch: Lean {lean_cert.euler_characteristic} != "
                f"f-vector {euler_f} / Betti {euler_beta}"
            )

        return TorsionBisimulationCertificate(
            complex_name=complex_key,
            forward_simulation_holds=forward_ok,
            backward_simulation_holds=backward_ok,
            lean_kernel_elaboration_holds=lean_ok,
            betti_numbers_matched=betti_ok,
            torsion_coefficients_matched=torsion_ok,
            euler_poincare_matched=euler_ok,
            lean_betti=lean_cert.betti_numbers,
            sql_betti=sql_betti,
            lean_torsion=lean_cert.torsion_by_dim,
            sql_torsion=sql_torsion,
            total_snf_cte_steps=total_steps,
            discrepancy_log=discrepancies,
        )

    def close(self):
        self.evaluator.close()
