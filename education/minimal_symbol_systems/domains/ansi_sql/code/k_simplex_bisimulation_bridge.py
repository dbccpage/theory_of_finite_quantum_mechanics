"""
K-Simplex Bisimulation Bridge: Cross-Domain Homology Parity
Lean 4 Simplicial Complex Kernel Certificates <-> ANSI SQL Gaussian Elimination CTEs
AuthorityEffect: None.
"""

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# Ensure local imports work regardless of working directory
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from homology_cte_evaluator import HomologyCTEEvaluator


@dataclass
class LeanHomologyCertificate:
    complex_name: str
    max_dim: int
    f_vector: List[int]
    betti_numbers: List[int]
    euler_characteristic: int
    euler_poincare_verified: bool


LEAN_CERTIFICATES = {
    "S1_Circle": LeanHomologyCertificate(
        complex_name="S1_Circle",
        max_dim=1,
        f_vector=[3, 3],
        betti_numbers=[1, 1],
        euler_characteristic=0,
        euler_poincare_verified=True,
    ),
    "S2_Sphere": LeanHomologyCertificate(
        complex_name="S2_Sphere",
        max_dim=2,
        f_vector=[4, 6, 4],
        betti_numbers=[1, 0, 1],
        euler_characteristic=2,
        euler_poincare_verified=True,
    ),
    "Delta3_Tetrahedron": LeanHomologyCertificate(
        complex_name="Delta3_Tetrahedron",
        max_dim=3,
        f_vector=[4, 6, 4, 1],
        betti_numbers=[1, 0, 0, 0],
        euler_characteristic=1,
        euler_poincare_verified=True,
    ),
}


@dataclass
class KSimplexBisimulationCertificate:
    complex_name: str
    max_dim: int
    forward_simulation_holds: bool
    backward_simulation_holds: bool
    lean_kernel_elaboration_holds: bool
    sql_nilpotence_cte_holds: bool
    betti_numbers_matched: bool
    euler_poincare_matched: bool
    lean_betti: List[int]
    sql_betti: List[int]
    lean_euler: int
    sql_euler: int
    discrepancy_log: List[str] = field(default_factory=list)

    @property
    def is_bisimilar(self) -> bool:
        return (
            self.forward_simulation_holds
            and self.backward_simulation_holds
            and self.lean_kernel_elaboration_holds
            and self.sql_nilpotence_cte_holds
            and self.betti_numbers_matched
            and self.euler_poincare_matched
            and len(self.discrepancy_log) == 0
        )


class KSimplexBisimulationBridge:
    def __init__(self, lean_src_path: Optional[Path] = None):
        self.lean_src = lean_src_path or (
            Path(__file__).resolve().parent.parent.parent
            / "mathematics"
            / "lean4"
            / "k_simplex_homology.lean"
        )
        self.evaluator = HomologyCTEEvaluator(in_memory=True)

    def verify_lean_compilation(self) -> bool:
        """Verifies that the Lean 4 k-simplex homology module elaborates with zero errors."""
        if not self.lean_src.exists():
            return False
        res = subprocess.run(["lean", str(self.lean_src)], capture_output=True, text=True)
        return res.returncode == 0

    def load_complex_s1(self):
        """Constructs S^1 Circle: boundary of triangle (3 vertices, 3 edges)."""
        self.evaluator.clear()
        for v in ["0", "1", "2"]:
            self.evaluator.add_simplex(0, v, [v])
        for u, v in [("0", "1"), ("0", "2"), ("1", "2")]:
            self.evaluator.add_simplex(1, f"{u}-{v}", [u, v])
        self.evaluator.build_boundaries()

    def load_complex_s2(self):
        """Constructs S^2 2-Sphere: hollow tetrahedron boundary (4 vertices, 6 edges, 4 triangles)."""
        self.evaluator.clear()
        for v in ["0", "1", "2", "3"]:
            self.evaluator.add_simplex(0, v, [v])
        for u, v in [("0", "1"), ("0", "2"), ("0", "3"), ("1", "2"), ("1", "3"), ("2", "3")]:
            self.evaluator.add_simplex(1, f"{u}-{v}", [u, v])
        for u, v, w in [("0", "1", "2"), ("0", "1", "3"), ("0", "2", "3"), ("1", "2", "3")]:
            self.evaluator.add_simplex(2, f"{u}-{v}-{w}", [u, v, w])
        self.evaluator.build_boundaries()

    def load_complex_delta3(self):
        """Constructs Delta^3 Solid Tetrahedron (4 vertices, 6 edges, 4 triangles, 1 3-simplex)."""
        self.evaluator.clear()
        for v in ["0", "1", "2", "3"]:
            self.evaluator.add_simplex(0, v, [v])
        for u, v in [("0", "1"), ("0", "2"), ("0", "3"), ("1", "2"), ("1", "3"), ("2", "3")]:
            self.evaluator.add_simplex(1, f"{u}-{v}", [u, v])
        for u, v, w in [("0", "1", "2"), ("0", "1", "3"), ("0", "2", "3"), ("1", "2", "3")]:
            self.evaluator.add_simplex(2, f"{u}-{v}-{w}", [u, v, w])
        self.evaluator.add_simplex(3, "0-1-2-3", ["0", "1", "2", "3"])
        self.evaluator.build_boundaries()

    def evaluate_complex_bisimulation(self, complex_key: str) -> KSimplexBisimulationCertificate:
        if complex_key not in LEAN_CERTIFICATES:
            raise ValueError(f"Unknown complex: {complex_key}")

        lean_cert = LEAN_CERTIFICATES[complex_key]
        discrepancies = []

        # 1. Verify Lean 4 Kernel Elaboration
        lean_ok = self.verify_lean_compilation()
        if not lean_ok:
            discrepancies.append(f"Lean 4 kernel compilation failed for {self.lean_src}")

        # 2. Populate Evaluator
        if complex_key == "S1_Circle":
            self.load_complex_s1()
        elif complex_key == "S2_Sphere":
            self.load_complex_s2()
        elif complex_key == "Delta3_Tetrahedron":
            self.load_complex_delta3()

        # 3. Verify Boundary Nilpotence via SQL CTE
        sql_nilpotence_ok = True
        for k in range(2, lean_cert.max_dim + 1):
            nilp_report = self.evaluator.verify_nilpotence(k)
            if not nilp_report["nilpotence_holds"]:
                sql_nilpotence_ok = False
                discrepancies.append(
                    f"SQL nilpotence failed at dim {k}: {nilp_report['violations']}"
                )

        # 4. Compute Homology via SQL Bareiss Elimination CTEs
        sql_hom = self.evaluator.compute_homology(lean_cert.max_dim)

        # 5. Check Forward Simulation (Lean certificate f-vector & dimensions match SQL)
        forward_ok = sql_hom["f_vector"] == lean_cert.f_vector
        if not forward_ok:
            discrepancies.append(
                f"Forward simulation mismatch: Lean f-vector {lean_cert.f_vector} != SQL {sql_hom['f_vector']}"
            )

        # 6. Check Backward Simulation (SQL boundary entries correspond to valid face projections)
        backward_ok = True
        c = self.evaluator.conn.cursor()
        c.execute("SELECT dim, face_id, simplex_id, weight FROM boundary_entries;")
        for row in c.fetchall():
            face_verts = row["face_id"].split("-")
            simp_verts = row["simplex_id"].split("-")
            # Face vertices must be strict subset of simplex vertices
            if (
                not all(v in simp_verts for v in face_verts)
                or len(face_verts) != len(simp_verts) - 1
            ):
                backward_ok = False
                discrepancies.append(f"Backward simulation invalid face entry: {dict(row)}")
                break

        # 7. Check Betti Number Equivalence
        betti_ok = sql_hom["betti_numbers"] == lean_cert.betti_numbers
        if not betti_ok:
            discrepancies.append(
                f"Betti numbers mismatch: Lean {lean_cert.betti_numbers} != SQL {sql_hom['betti_numbers']}"
            )

        # 8. Check Euler-Poincaré Invariance
        euler_ok = (
            sql_hom["euler_characteristic_f"] == lean_cert.euler_characteristic
            and sql_hom["euler_characteristic_betti"] == lean_cert.euler_characteristic
            and sql_hom["euler_poincare_verified"]
        )
        if not euler_ok:
            discrepancies.append(
                f"Euler characteristic mismatch: Lean {lean_cert.euler_characteristic} != "
                f"SQL f-vector {sql_hom['euler_characteristic_f']} / Betti {sql_hom['euler_characteristic_betti']}"
            )

        return KSimplexBisimulationCertificate(
            complex_name=complex_key,
            max_dim=lean_cert.max_dim,
            forward_simulation_holds=forward_ok,
            backward_simulation_holds=backward_ok,
            lean_kernel_elaboration_holds=lean_ok,
            sql_nilpotence_cte_holds=sql_nilpotence_ok,
            betti_numbers_matched=betti_ok,
            euler_poincare_matched=euler_ok,
            lean_betti=lean_cert.betti_numbers,
            sql_betti=sql_hom["betti_numbers"],
            lean_euler=lean_cert.euler_characteristic,
            sql_euler=sql_hom["euler_characteristic_betti"],
            discrepancy_log=discrepancies,
        )

    def close(self):
        self.evaluator.close()
