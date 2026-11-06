"""Toric and Surface Code Topological Quantum Error-Correcting Cochain Evaluator.
AuthorityEffect: None.

Evaluates 2D topological quantum error-correcting codes (Kitaev Toric Code and planar Surface Codes)
using relational ANSI SQL Common Table Expressions (CTEs) against Lean 4 chain complex certificates.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class QecSyndromeReceipt:
    round_id: int
    cell_type: str
    cell_id: int
    syndrome_val: int
    is_verified: bool


@dataclass(frozen=True)
class AnyonBraidingReceipt:
    braid_run_id: int
    winding_number: int
    topological_berry_phase: int  # +1 or -1
    is_non_trivial: bool


@dataclass(frozen=True)
class QecRecoveryReceipt:
    round_id: int
    horizontal_crossings: int
    vertical_crossings: int
    logical_z_flip: int
    logical_x_flip: int
    terminal_route: str  # Repair or SplitBrainRefusal
    status: str


class ToricSurfaceCodeEvaluator:
    """Relational SQL & Discrete Topology Evaluator for Toric and Surface Codes."""

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "toric_qec.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        self.L_x = 0
        self.L_y = 0
        self.topology = "TORUS"

    def _init_schema(self) -> None:
        schema_path = (
            Path(__file__).resolve().parent.parent / "databases" / "toric_surface_code_schema.sql"
        )
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent / "toric_surface_code_schema.sql"
        if schema_path.exists():
            self.conn.executescript(schema_path.read_text(encoding="utf-8"))
        self.conn.commit()

    def build_torus_lattice(self, L: int = 3) -> Dict[str, int]:
        """Scaffolds an L x L square torus lattice with periodic boundary conditions."""
        self.L_x = L
        self.L_y = L
        self.topology = "TORUS"
        c = self.conn.cursor()

        # Clear existing lattice relvars
        c.execute("DELETE FROM ToricBoundary2;")
        c.execute("DELETE FROM ToricBoundary1;")
        c.execute("DELETE FROM ToricEdges;")
        c.execute("DELETE FROM ToricPlaquettes;")
        c.execute("DELETE FROM ToricVertices;")
        c.execute("DELETE FROM ToricLattice;")

        c.execute(
            "INSERT INTO ToricLattice (lattice_id, L_x, L_y, topology) VALUES (1, ?, ?, 'TORUS');",
            (L, L),
        )

        # 1. Vertices: (x, y) for x, y in [0, L-1]
        for y in range(L):
            for x in range(L):
                vid = y * L + x
                c.execute(
                    "INSERT INTO ToricVertices (vertex_id, x, y) VALUES (?, ?, ?);", (vid, x, y)
                )

        # Helper to get vertex ID with periodic wrapping
        def v_id(vx: int, vy: int) -> int:
            return (vy % L) * L + (vx % L)

        # 2. Edges: Horizontal (H) and Vertical (V)
        # Each vertex (x, y) anchors one H edge and one V edge
        for y in range(L):
            for x in range(L):
                u = v_id(x, y)
                # Horizontal edge: (x, y) -> ((x+1)%L, y)
                e_h_id = 2 * (y * L + x)
                v_h = v_id(x + 1, y)
                c.execute(
                    "INSERT INTO ToricEdges (edge_id, orientation, u, v, x, y) VALUES (?, 'H', ?, ?, ?, ?);",
                    (e_h_id, u, v_h, x + 0.5, float(y)),
                )
                # Incidence d1 for H edge
                c.execute(
                    "INSERT INTO ToricBoundary1 (edge_id, vertex_id, coeff) VALUES (?, ?, 1);",
                    (e_h_id, u),
                )
                c.execute(
                    "INSERT INTO ToricBoundary1 (edge_id, vertex_id, coeff) VALUES (?, ?, 1);",
                    (e_h_id, v_h),
                )

                # Vertical edge: (x, y) -> (x, (y+1)%L)
                e_v_id = 2 * (y * L + x) + 1
                v_v = v_id(x, y + 1)
                c.execute(
                    "INSERT INTO ToricEdges (edge_id, orientation, u, v, x, y) VALUES (?, 'V', ?, ?, ?, ?);",
                    (e_v_id, u, v_v, float(x), y + 0.5),
                )
                # Incidence d1 for V edge
                c.execute(
                    "INSERT INTO ToricBoundary1 (edge_id, vertex_id, coeff) VALUES (?, ?, 1);",
                    (e_v_id, u),
                )
                c.execute(
                    "INSERT INTO ToricBoundary1 (edge_id, vertex_id, coeff) VALUES (?, ?, 1);",
                    (e_v_id, v_v),
                )

        # Helper to get edge IDs
        def eh_id(ex: int, ey: int) -> int:
            return 2 * ((ey % L) * L + (ex % L))

        def ev_id(ex: int, ey: int) -> int:
            return 2 * ((ey % L) * L + (ex % L)) + 1

        # 3. Plaquettes: unit square cells
        for y in range(L):
            for x in range(L):
                pid = y * L + x
                c.execute(
                    "INSERT INTO ToricPlaquettes (plaquette_id, x, y) VALUES (?, ?, ?);",
                    (pid, x, y),
                )
                # Plaquette boundary consists of 4 edges:
                # bottom: eh_id(x, y)
                # top: eh_id(x, y + 1)
                # left: ev_id(x, y)
                # right: ev_id(x + 1, y)
                for eid in [eh_id(x, y), eh_id(x, y + 1), ev_id(x, y), ev_id(x + 1, y)]:
                    c.execute(
                        "INSERT INTO ToricBoundary2 (plaquette_id, edge_id, coeff) VALUES (?, ?, 1);",
                        (pid, eid),
                    )

        self.conn.commit()
        return {"vertices": L * L, "edges": 2 * L * L, "plaquettes": L * L}

    # ------------------------------------------------------------------------
    # Error Injection & Syndrome Extraction
    # ------------------------------------------------------------------------
    def inject_pauli_errors(self, round_id: int, errors: Sequence[Tuple[int, str]]) -> None:
        """Injects Pauli X, Z, or Y errors on specific edge (qubit) IDs."""
        c = self.conn.cursor()
        c.execute("DELETE FROM ToricPauliErrors WHERE round_id = ?;", (round_id,))
        for edge_id, pauli_type in errors:
            c.execute(
                "INSERT INTO ToricPauliErrors (round_id, edge_id, pauli_type) VALUES (?, ?, ?);",
                (round_id, edge_id, pauli_type),
            )
        self.conn.commit()

    def measure_syndromes(self, round_id: int) -> List[Dict[str, Any]]:
        """Calculates and stores syndromes in ToricSyndromes from ViewComputedSyndromes."""
        c = self.conn.cursor()
        c.execute("DELETE FROM ToricSyndromes WHERE round_id = ?;", (round_id,))
        c.execute(
            """INSERT INTO ToricSyndromes (round_id, cell_type, cell_id, syndrome_val)
               SELECT round_id, cell_type, cell_id, computed_syndrome
               FROM ViewComputedSyndromes
               WHERE round_id = ?;""",
            (round_id,),
        )
        self.conn.commit()

        c.execute(
            "SELECT * FROM ToricSyndromes WHERE round_id = ? AND syndrome_val = 1;", (round_id,)
        )
        return [dict(row) for row in c.fetchall()]

    def apply_recovery_chain(self, round_id: int, corrections: Sequence[Tuple[int, str]]) -> None:
        """Applies decoded recovery operations onto ToricRecoveryChains."""
        c = self.conn.cursor()
        c.execute("DELETE FROM ToricRecoveryChains WHERE round_id = ?;", (round_id,))
        for edge_id, corr_type in corrections:
            c.execute(
                "INSERT INTO ToricRecoveryChains (round_id, edge_id, correction_type) VALUES (?, ?, ?);",
                (round_id, edge_id, corr_type),
            )
        self.conn.commit()

    # ------------------------------------------------------------------------
    # Anyonic Defect Braiding Simulation
    # ------------------------------------------------------------------------
    def simulate_anyon_braiding(
        self,
        braid_run_id: int,
        enclosing: bool = True,
        flux_pos: Tuple[float, float] = (1.5, 1.5),
    ) -> None:
        """Simulates anyon motion: an electric anyon (e) is transported along a path

        while a magnetic anyon (m) remains static at flux_pos.
        If enclosing is True, the e-loop encircles flux_pos; otherwise it does not.
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM ToricAnyonWorldlines WHERE braid_run_id = ?;", (braid_run_id,))

        # Stationary magnetic flux m
        c.execute(
            """INSERT INTO ToricAnyonWorldlines (braid_run_id, anyon_id, anyon_type, step_t, cell_id, x, y)
               VALUES (?, 1, 'm', 0, 0, ?, ?);""",
            (braid_run_id, flux_pos[0], flux_pos[1]),
        )

        if enclosing:
            # Loop encircling (1.5, 1.5): (1, 1) -> (2, 1) -> (2, 2) -> (1, 2) -> (1, 1)
            e_coords = [(1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (1.0, 2.0), (1.0, 1.0)]
        else:
            # Trivial loop outside (1.5, 1.5): (0, 0) -> (1, 0) -> (1, 1) -> (0, 1) -> (0, 0)
            e_coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]

        for t, (ex, ey) in enumerate(e_coords):
            c.execute(
                """INSERT INTO ToricAnyonWorldlines (braid_run_id, anyon_id, anyon_type, step_t, cell_id, x, y)
                   VALUES (?, 2, 'e', ?, 0, ?, ?);""",
                (braid_run_id, t, ex, ey),
            )
        self.conn.commit()

    # ------------------------------------------------------------------------
    # Relational Auditing Verification Methods
    # ------------------------------------------------------------------------
    def verify_chain_complex_nilpotence(self) -> Dict[str, Any]:
        """Audits d1 ∘ d2 = 0 mod 2 inside ViewChainComplexNilpotence."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewChainComplexNilpotence WHERE residual_mod2 != 0;")
        defects = c.fetchall()
        c.execute("SELECT COUNT(*) FROM ViewChainComplexNilpotence;")
        total_tested = c.fetchone()[0]
        return {
            "is_nilpotent": len(defects) == 0,
            "total_pairs_tested": total_tested,
            "defects_count": len(defects),
        }

    def verify_stabilizer_commutation(self) -> Dict[str, Any]:
        """Audits [A_s, B_p] = 0 inside ViewStabilizerCommutation."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewStabilizerCommutation WHERE commutes = 0;")
        non_commuting = c.fetchall()
        c.execute("SELECT COUNT(*) FROM ViewStabilizerCommutation;")
        total_stabilizers = c.fetchone()[0]
        return {
            "all_stabilizers_commute": len(non_commuting) == 0,
            "total_pairs_tested": total_stabilizers,
            "violations_count": len(non_commuting),
        }

    def verify_syndrome_audit(self, round_id: int) -> Dict[str, Any]:
        """Audits syndrome integrity in ViewSyndromeAudit."""
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM ViewSyndromeAudit WHERE round_id = ? AND audit_disposition != 'SYNDROME_VERIFIED';",
            (round_id,),
        )
        mismatches = c.fetchall()
        c.execute("SELECT COUNT(*) FROM ViewSyndromeAudit WHERE round_id = ?;", (round_id,))
        total = c.fetchone()[0]
        return {
            "all_syndromes_verified": len(mismatches) == 0,
            "total_syndromes_checked": total,
            "mismatch_count": len(mismatches),
        }

    def verify_anyon_conservation(self, round_id: int) -> Dict[str, Any]:
        """Audits even parity of anyon charges in ViewAnyonConservation."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewAnyonConservation WHERE round_id = ?;", (round_id,))
        row = c.fetchone()
        if not row:
            return {"parity_status": "NO_SYNDROMES", "is_conserved": True}
        return {
            "round_id": row["round_id"],
            "total_e_anyons": row["total_e_anyons"],
            "total_m_anyons": row["total_m_anyons"],
            "e_parity_even": bool(row["e_parity_even"]),
            "m_parity_even": bool(row["m_parity_even"]),
            "parity_status": row["parity_status"],
            "is_conserved": row["parity_status"] == "PARITY_CONSERVED",
        }

    def verify_anyonic_braiding_phase(self, braid_run_id: int) -> AnyonBraidingReceipt:
        """Audits anyonic Berry phase in ViewAnyonicBraidingAudit."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewAnyonicBraidingAudit WHERE braid_run_id = ?;", (braid_run_id,))
        row = c.fetchone()
        assert row is not None, f"Braid run {braid_run_id} not found"
        return AnyonBraidingReceipt(
            braid_run_id=row["braid_run_id"],
            winding_number=row["winding_number"],
            topological_berry_phase=row["topological_berry_phase"],
            is_non_trivial=row["braid_classification"] == "NON_TRIVIAL_BRAID_PHASE",
        )

    def verify_homological_recovery(self, round_id: int) -> QecRecoveryReceipt:
        """Audits residual chain homology in ViewLogicalHomologyAudit."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewLogicalHomologyAudit WHERE round_id = ?;", (round_id,))
        row = c.fetchone()
        if not row:
            # Empty residual chain (exact recovery)
            return QecRecoveryReceipt(
                round_id=round_id,
                horizontal_crossings=0,
                vertical_crossings=0,
                logical_z_flip=0,
                logical_x_flip=0,
                terminal_route="Repair",
                status="EXACT_HOMOLOGICAL_REPAIR",
            )
        return QecRecoveryReceipt(
            round_id=row["round_id"],
            horizontal_crossings=row["horizontal_meridian_crossings"],
            vertical_crossings=row["vertical_parallel_crossings"],
            logical_z_flip=row["logical_z_flip"],
            logical_x_flip=row["logical_x_flip"],
            terminal_route=row["terminal_route"],
            status=row["qec_recovery_status"],
        )

    def close(self) -> None:
        self.conn.close()
