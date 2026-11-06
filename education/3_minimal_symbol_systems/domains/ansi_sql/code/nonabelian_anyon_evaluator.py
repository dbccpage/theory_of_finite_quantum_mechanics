"""Non-Abelian Anyon Fusion, Braiding & Topological Quantum Compiling Evaluator.
AuthorityEffect: None.

Evaluates Unitary Modular Tensor Category (UMTC) anyon models (Fibonacci & Ising),
auditing fusion associativity, F-matrix involution / B3 relations, and topological
quantum compiling using ANSI SQL relational Common Table Expressions (CTEs).
"""

from __future__ import annotations

import cmath
import math
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class AnyonModelReceipt:
    model: str
    num_species: int
    is_associative: bool
    involution_residual_max: float
    is_involution_consistent: bool
    is_b3_consistent: bool


@dataclass(frozen=True)
class TopologicalCompilingReceipt:
    compilation_id: int
    model: str
    target_gate: str
    braid_word: str
    word_length: int
    approximation_error: float
    compilation_fidelity: float
    is_strictly_unitary: bool
    terminal_route: str
    compilation_status: str


class NonAbelianAnyonEvaluator:
    """Relational SQL & Algebraic Evaluator for Non-Abelian Anyons & Topological Quantum Compiling."""

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "nonabelian_anyons.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        schema_path = (
            Path(__file__).resolve().parent.parent / "databases" / "nonabelian_anyon_schema.sql"
        )
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent / "nonabelian_anyon_schema.sql"
        if schema_path.exists():
            self.conn.executescript(schema_path.read_text(encoding="utf-8"))
        self.conn.commit()

    # ------------------------------------------------------------------------
    # Fibonacci Anyon Model Initialization
    # ------------------------------------------------------------------------
    def populate_fibonacci_model(self) -> None:
        """Populates species, fusion rules, F-matrix, and R-matrix for Fibonacci anyons."""
        c = self.conn.cursor()
        c.execute("DELETE FROM AnyonSpecies WHERE model = 'FIBONACCI';")
        c.execute("DELETE FROM AnyonFusionRules WHERE model = 'FIBONACCI';")
        c.execute("DELETE FROM AnyonFSymbols WHERE model = 'FIBONACCI';")
        c.execute("DELETE FROM AnyonRMatrices WHERE model = 'FIBONACCI';")

        phi = (1.0 + math.sqrt(5.0)) / 2.0  # ~ 1.6180339887

        # 1. Species
        c.execute(
            "INSERT INTO AnyonSpecies (model, label, qdim, topological_spin) VALUES ('FIBONACCI', '1', 1.0, 0.0);"
        )
        c.execute(
            "INSERT INTO AnyonSpecies (model, label, qdim, topological_spin) VALUES ('FIBONACCI', 'tau', ?, ?);",
            (phi, 0.2),
        )

        # 2. Fusion rules: 1 x 1 -> 1, 1 x tau -> tau, tau x 1 -> tau, tau x tau -> 1 + tau
        fusions = [
            ("1", "1", "1", 1),
            ("1", "1", "tau", 0),
            ("1", "tau", "1", 0),
            ("1", "tau", "tau", 1),
            ("tau", "1", "1", 0),
            ("tau", "1", "tau", 1),
            ("tau", "tau", "1", 1),
            ("tau", "tau", "tau", 1),
        ]
        for a, b, ch, mult in fusions:
            c.execute(
                "INSERT INTO AnyonFusionRules (model, a, b, c, multiplicity) VALUES ('FIBONACCI', ?, ?, ?, ?);",
                (a, b, ch, mult),
            )

        # 3. F-symbols (Associator) for tau x tau x tau -> tau in basis {1, tau}
        # F^{tau,tau,tau;tau} = [[phi^-1, phi^-1/2], [phi^-1/2, -phi^-1]]
        f_11 = 1.0 / phi
        f_1tau = 1.0 / math.sqrt(phi)
        f_tau1 = 1.0 / math.sqrt(phi)
        f_tautau = -1.0 / phi

        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('FIBONACCI', 'tau', 'tau', 'tau', 'tau', '1', '1', ?);",
            (f_11,),
        )
        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('FIBONACCI', 'tau', 'tau', 'tau', 'tau', '1', 'tau', ?);",
            (f_1tau,),
        )
        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('FIBONACCI', 'tau', 'tau', 'tau', 'tau', 'tau', '1', ?);",
            (f_tau1,),
        )
        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('FIBONACCI', 'tau', 'tau', 'tau', 'tau', 'tau', 'tau', ?);",
            (f_tautau,),
        )

        # 4. R-matrices: R^{tau,tau}_1 = e^{-i 4pi/5}, R^{tau,tau}_tau = e^{i 3pi/5}
        theta_1 = -4.0 * math.pi / 5.0
        r_1 = cmath.exp(1j * theta_1)
        theta_tau = 3.0 * math.pi / 5.0
        r_tau = cmath.exp(1j * theta_tau)

        c.execute(
            "INSERT INTO AnyonRMatrices (model, a, b, c, val_re, val_im, phase_rad) VALUES ('FIBONACCI', 'tau', 'tau', '1', ?, ?, ?);",
            (r_1.real, r_1.imag, theta_1),
        )
        c.execute(
            "INSERT INTO AnyonRMatrices (model, a, b, c, val_re, val_im, phase_rad) VALUES ('FIBONACCI', 'tau', 'tau', 'tau', ?, ?, ?);",
            (r_tau.real, r_tau.imag, theta_tau),
        )
        self.conn.commit()

    # ------------------------------------------------------------------------
    # Ising Anyon Model Initialization
    # ------------------------------------------------------------------------
    def populate_ising_model(self) -> None:
        """Populates species, fusion rules, F-matrix, and R-matrix for Ising anyons."""
        c = self.conn.cursor()
        c.execute("DELETE FROM AnyonSpecies WHERE model = 'ISING';")
        c.execute("DELETE FROM AnyonFusionRules WHERE model = 'ISING';")
        c.execute("DELETE FROM AnyonFSymbols WHERE model = 'ISING';")
        c.execute("DELETE FROM AnyonRMatrices WHERE model = 'ISING';")

        # 1. Species
        c.execute(
            "INSERT INTO AnyonSpecies (model, label, qdim, topological_spin) VALUES ('ISING', '1', 1.0, 0.0);"
        )
        c.execute(
            "INSERT INTO AnyonSpecies (model, label, qdim, topological_spin) VALUES ('ISING', 'sigma', ?, ?);",
            (math.sqrt(2.0), 0.0625),
        )
        c.execute(
            "INSERT INTO AnyonSpecies (model, label, qdim, topological_spin) VALUES ('ISING', 'psi', 1.0, 0.5);"
        )

        # 2. Fusion rules
        species = ["1", "sigma", "psi"]
        for a in species:
            for b in species:
                for ch in species:
                    mult = 0
                    if a == "1" and b == ch:
                        mult = 1
                    elif b == "1" and a == ch:
                        mult = 1
                    elif a == "psi" and b == "psi" and ch == "1":
                        mult = 1
                    elif (a == "psi" and b == "sigma" and ch == "sigma") or (
                        a == "sigma" and b == "psi" and ch == "sigma"
                    ):
                        mult = 1
                    elif a == "sigma" and b == "sigma" and (ch == "1" or ch == "psi"):
                        mult = 1
                    c.execute(
                        "INSERT INTO AnyonFusionRules (model, a, b, c, multiplicity) VALUES ('ISING', ?, ?, ?, ?);",
                        (a, b, ch, mult),
                    )

        # 3. F-symbols for sigma x sigma x sigma -> sigma (Hadamard matrix / sqrt(2))
        inv_sqrt2 = 1.0 / math.sqrt(2.0)
        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('ISING', 'sigma', 'sigma', 'sigma', 'sigma', '1', '1', ?);",
            (inv_sqrt2,),
        )
        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('ISING', 'sigma', 'sigma', 'sigma', 'sigma', '1', 'psi', ?);",
            (inv_sqrt2,),
        )
        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('ISING', 'sigma', 'sigma', 'sigma', 'sigma', 'psi', '1', ?);",
            (inv_sqrt2,),
        )
        c.execute(
            "INSERT INTO AnyonFSymbols (model, a, b, c, d, e, f, val) VALUES ('ISING', 'sigma', 'sigma', 'sigma', 'sigma', 'psi', 'psi', ?);",
            (-inv_sqrt2,),
        )

        # 4. R-matrices
        r_1 = cmath.exp(-1j * math.pi / 8.0)
        r_psi = cmath.exp(1j * 3.0 * math.pi / 8.0)
        c.execute(
            "INSERT INTO AnyonRMatrices (model, a, b, c, val_re, val_im, phase_rad) VALUES ('ISING', 'sigma', 'sigma', '1', ?, ?, ?);",
            (r_1.real, r_1.imag, -math.pi / 8.0),
        )
        c.execute(
            "INSERT INTO AnyonRMatrices (model, a, b, c, val_re, val_im, phase_rad) VALUES ('ISING', 'sigma', 'sigma', 'psi', ?, ?, ?);",
            (r_psi.real, r_psi.imag, 3.0 * math.pi / 8.0),
        )
        self.conn.commit()

    # ------------------------------------------------------------------------
    # Braid Representation & Topological Compiling
    # ------------------------------------------------------------------------
    def get_fibonacci_braid_generators(self) -> Tuple[List[List[complex]], List[List[complex]]]:
        """Returns the unitary 2x2 matrix representations of braid generators sigma_1 and sigma_2

        in the fusion space V^{tau,tau,tau}_tau.
        """
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        r1 = cmath.exp(-1j * 4.0 * math.pi / 5.0)
        rtau = cmath.exp(1j * 3.0 * math.pi / 5.0)

        # sigma_1 = diag(r1, rtau)
        s1 = [[r1, 0.0j], [0.0j, rtau]]

        # F matrix: real orthogonal
        f = [[1.0 / phi, 1.0 / math.sqrt(phi)], [1.0 / math.sqrt(phi), -1.0 / phi]]

        # sigma_2 = F^dagger * sigma_1 * F
        # Matrix multiply: s2 = F * s1 * F
        temp = [
            [f[0][0] * s1[0][0] + f[0][1] * s1[1][0], f[0][0] * s1[0][1] + f[0][1] * s1[1][1]],
            [f[1][0] * s1[0][0] + f[1][1] * s1[1][0], f[1][0] * s1[0][1] + f[1][1] * s1[1][1]],
        ]
        s2 = [
            [
                temp[0][0] * f[0][0] + temp[0][1] * f[1][0],
                temp[0][0] * f[0][1] + temp[0][1] * f[1][1],
            ],
            [
                temp[1][0] * f[0][0] + temp[1][1] * f[1][0],
                temp[1][0] * f[0][1] + temp[1][1] * f[1][1],
            ],
        ]
        return s1, s2

    @staticmethod
    def _mat_mul_2x2(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
        ]

    @staticmethod
    def _mat_inv_2x2(A: List[List[complex]]) -> List[List[complex]]:
        """Conjugate transpose for unitary matrix."""
        return [
            [A[0][0].conjugate(), A[1][0].conjugate()],
            [A[0][1].conjugate(), A[1][1].conjugate()],
        ]

    def evaluate_braid_word(self, word: Sequence[int]) -> List[List[complex]]:
        """Multiplies a sequence of braid generators in B_3:

        1: sigma_1, -1: sigma_1^-1, 2: sigma_2, -2: sigma_2^-1.
        """
        s1, s2 = self.get_fibonacci_braid_generators()
        gens = {
            1: s1,
            -1: self._mat_inv_2x2(s1),
            2: s2,
            -2: self._mat_inv_2x2(s2),
        }
        res: List[List[complex]] = [[1.0 + 0j, 0j], [0j, 1.0 + 0j]]
        for g in word:
            res = self._mat_mul_2x2(res, gens[g])
        return res

    def compile_topological_gate(
        self,
        target_name: str,
        target_unitary: List[List[complex]],
        candidate_words: Sequence[Sequence[int]],
        tolerance: float = 0.05,
    ) -> TopologicalCompilingReceipt:
        """Finds the candidate braid word minimizing trace distance to target_unitary

        and records it into the SQL database.
        """
        best_word: Optional[Sequence[int]] = None
        best_mat: Optional[List[List[complex]]] = None
        best_err: float = float("inf")

        for w in candidate_words:
            mat = self.evaluate_braid_word(w)
            # Hilbert-Schmidt trace distance / fidelity:
            # F(U, V) = 1/2 |Tr(U^dagger V)|
            u_dag = self._mat_inv_2x2(target_unitary)
            prod = self._mat_mul_2x2(u_dag, mat)
            tr = prod[0][0] + prod[1][1]
            fid = 0.5 * abs(tr)
            err = max(0.0, 1.0 - fid)
            if err < best_err:
                best_err = err
                best_word = w
                best_mat = mat

        assert best_word is not None and best_mat is not None
        return self.record_compilation(
            target_name=target_name,
            braid_word=best_word,
            matrix=best_mat,
            approximation_error=best_err,
            model="FIBONACCI",
            tolerance=tolerance,
        )

    def record_compilation(
        self,
        target_name: str,
        braid_word: Sequence[int],
        matrix: List[List[complex]],
        approximation_error: float,
        model: str = "FIBONACCI",
        tolerance: float = 0.05,
    ) -> TopologicalCompilingReceipt:
        """Records a compilation matrix and word into the SQL database,

        evaluating braid alphabet validity, matrix unitarity, and tolerance thresholding.
        """
        c = self.conn.cursor()
        is_valid = len(braid_word) > 0 and all(g in (-2, -1, 1, 2) for g in braid_word)
        if not is_valid:
            terminal_route = "ClosureFailure"
            is_unitary = 0
        else:
            u_dag = self._mat_inv_2x2(matrix)
            u_u = self._mat_mul_2x2(u_dag, matrix)
            unitarity_defect = max(
                abs(u_u[0][0] - 1.0),
                abs(u_u[0][1]),
                abs(u_u[1][0]),
                abs(u_u[1][1] - 1.0),
            )
            is_unitary = 1 if unitarity_defect < 1e-9 else 0
            terminal_route = (
                "Repair"
                if (is_unitary == 1 and approximation_error <= tolerance)
                else "SplitBrainRefusal"
            )

        c.execute(
            """INSERT INTO CompiledBraidWords
               (model, target_gate, braid_word, word_length, approximation_error, is_unitary, terminal_route)
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (
                model,
                target_name,
                str(list(braid_word)),
                len(braid_word),
                approximation_error,
                is_unitary,
                terminal_route,
            ),
        )
        comp_id = c.lastrowid
        assert comp_id is not None

        for r in range(2):
            for col in range(2):
                c.execute(
                    """INSERT INTO BraidMatrixEntries (compilation_id, row_idx, col_idx, val_re, val_im)
                       VALUES (?, ?, ?, ?, ?);""",
                    (comp_id, r, col, matrix[r][col].real, matrix[r][col].imag),
                )
        self.conn.commit()

        return self.verify_topological_compiling(comp_id)

    # ------------------------------------------------------------------------
    # Relational Auditing Verification Queries
    # ------------------------------------------------------------------------
    def verify_fusion_associativity(self, model: str = "FIBONACCI") -> Dict[str, Any]:
        """Audits fusion associativity across ViewFusionAssociativityAudit."""
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM ViewFusionAssociativityAudit WHERE model = ? AND associativity_status != 'ASSOCIATIVE';",
            (model,),
        )
        breaches = c.fetchall()
        c.execute("SELECT COUNT(*) FROM ViewFusionAssociativityAudit WHERE model = ?;", (model,))
        total = c.fetchone()[0]
        return {
            "model": model,
            "is_associative": len(breaches) == 0 and total == {"FIBONACCI": 16, "ISING": 81}.get(model, -1),
            "quadruples_checked": total,
            "defect_count": len(breaches),
        }

    def verify_f_matrix_involution(self, model="FIBONACCI"):
        """Check the complete declared 2x2 real F block; this is not the pentagon."""
        block = self._stored_braid_matrices(model)
        if block is None:
            return {"model": model, "max_residual": float("inf"), "is_consistent": False, "violations_count": 1}
        f, _ = block
        product = self._mat_mul_2x2(f, f)
        residual = max(abs(product[i][j] - int(i == j)) for i in range(2) for j in range(2))
        return {"model": model, "max_residual": residual, "is_consistent": residual < 1e-10, "violations_count": int(residual >= 1e-10)}

    def _stored_braid_matrices(self, model):
        if model not in ("FIBONACCI", "ISING"):
            return None
        label = "tau" if model == "FIBONACCI" else "sigma"
        channels = ["1", "tau" if model == "FIBONACCI" else "psi"]
        rows = self.conn.execute("SELECT e,f,val FROM AnyonFSymbols WHERE model=? AND a=? AND b=? AND c=? AND d=?", (model, label, label, label, label)).fetchall()
        values = {(row["e"], row["f"]): row["val"] for row in rows}
        phases = self.conn.execute("SELECT c,val_re,val_im FROM AnyonRMatrices WHERE model=? AND a=? AND b=?", (model, label, label)).fetchall()
        r = {row["c"]: complex(row["val_re"], row["val_im"]) for row in phases}
        if set(values) != {(i,j) for i in channels for j in channels} or set(r) != set(channels):
            return None
        f = [[complex(values[i,j]) for j in channels] for i in channels]
        diagonal = [[r[i] if i == j else 0j for j in channels] for i in channels]
        if any(not (math.isfinite(v.real) and math.isfinite(v.imag)) for matrix in (f, diagonal) for row in matrix for v in row):
            return None
        return f, diagonal

    def verify_braid_relation(self, model="FIBONACCI"):
        """Check stored F/R unitarity and the B3 relation; no hexagon theorem is claimed."""
        block = self._stored_braid_matrices(model)
        if block is None:
            return {"model": model, "sectors_checked": 0, "is_consistent": False}
        f, r = block
        mul = self._mat_mul_2x2
        dagger = self._mat_inv_2x2
        unitary_error = max(abs(mul(dagger(m), m)[i][j] - int(i == j))
                            for m in (f, r) for i in range(2) for j in range(2))
        s2 = mul(dagger(f), mul(r, f))
        left = mul(mul(r, s2), r)
        right = mul(mul(s2, r), s2)
        residual = max(abs(left[i][j] - right[i][j]) for i in range(2) for j in range(2))
        return {"model": model, "sectors_checked": 1, "max_residual": residual,
                "is_consistent": unitary_error < 1e-10 and residual < 1e-10}

    def verify_topological_compiling(self, compilation_id: int) -> TopologicalCompilingReceipt:
        """Audits compiled quantum gate across ViewTopologicalCompilingAudit."""
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM ViewTopologicalCompilingAudit WHERE compilation_id = ?;",
            (compilation_id,),
        )
        row = c.fetchone()
        assert row is not None, f"Compilation id {compilation_id} not found"
        return TopologicalCompilingReceipt(
            compilation_id=row["compilation_id"],
            model=row["model"],
            target_gate=row["target_gate"],
            braid_word=row["braid_word"],
            word_length=row["word_length"],
            approximation_error=row["approximation_error"],
            compilation_fidelity=row["compilation_fidelity"],
            is_strictly_unitary=bool(row["is_strictly_unitary"]),
            terminal_route=row["terminal_route"],
            compilation_status=row["compilation_status"],
        )

    def close(self) -> None:
        self.conn.close()
