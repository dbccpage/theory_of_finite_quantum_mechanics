"""Quantum State Transfer, Teleportation & Entanglement Distillation Evaluator.
AuthorityEffect: None.

Evaluates Categorical Quantum State Transfer Cochains:
1. Bell and GHZ states with Entanglement Witness inequalities (Tr(W ρ) < 0).
2. Quantum teleportation protocol execution, feedforward correction, and fidelity audits.
3. Entanglement distillation purification (Bennett/Deutsch protocol).
4. BQNF terminal routing via ANSI SQL relational CTEs.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class WitnessAuditResult:
    witness_id: str
    target_state: str
    state_id: str
    state_name: str
    separable_bound: float
    computed_trace_val: float
    is_entangled: bool
    witness_status: str


@dataclass(frozen=True)
class TeleportationAuditResult:
    run_id: int
    input_state: str
    m1: int
    m2: int
    applied_correction: str
    expected_correction: str
    output_fidelity: float
    is_valid_protocol: bool
    terminal_route: str
    audit_status: str


@dataclass(frozen=True)
class DistillationAuditResult:
    distillation_id: int
    pair_label: str
    round_num: int
    input_fidelity: float
    output_fidelity: float
    fidelity_gain: float
    is_coincident: bool
    distillation_status: str


class QuantumStateTransferEvaluator:
    """Relational SQL & Algebraic Evaluator for Quantum State Transfer Cochains."""

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "quantum_state_transfer.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        schema_path = (
            Path(__file__).resolve().parent.parent
            / "databases"
            / "quantum_state_transfer_schema.sql"
        )
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent / "quantum_state_transfer_schema.sql"
        if schema_path.exists():
            self.conn.executescript(schema_path.read_text(encoding="utf-8"))
        self.conn.commit()

    # ------------------------------------------------------------------------
    # State & Density Matrix Population
    # ------------------------------------------------------------------------
    def populate_bell_and_ghz_states(self) -> None:
        """Populates Bell states (|Phi+>), separable states, and 3-qubit GHZ states."""
        c = self.conn.cursor()
        c.execute("DELETE FROM DensityMatrixEntries;")
        c.execute("DELETE FROM DensityMatrices;")

        # 1. Bell State |Phi+> = (|00> + |11>) / sqrt(2)
        # Density matrix rho = 0.5 |00><00| + 0.5 |00><11| + 0.5 |11><00| + 0.5 |11><11|
        c.execute("INSERT INTO DensityMatrices VALUES ('state_phi_plus', 'Bell_PhiPlus', 2, 4, 1);")
        entries_phi_plus = [
            (0, 0, 0.5, 0.0),
            (0, 3, 0.5, 0.0),
            (3, 0, 0.5, 0.0),
            (3, 3, 0.5, 0.0),
        ]
        for r, col, re, im in entries_phi_plus:
            c.execute(
                "INSERT INTO DensityMatrixEntries VALUES ('state_phi_plus', ?, ?, ?, ?);",
                (r, col, re, im),
            )

        # 2. Separable 2-Qubit State |00><00|
        c.execute(
            "INSERT INTO DensityMatrices VALUES ('state_separable_00', 'Separable_00', 2, 4, 1);"
        )
        c.execute("INSERT INTO DensityMatrixEntries VALUES ('state_separable_00', 0, 0, 1.0, 0.0);")

        # 3. Partially Entangled / Noisy Werner State (F = 0.75 > 0.5)
        # rho = 0.75 |Phi+><Phi+| + 0.25 (I/4)
        c.execute(
            "INSERT INTO DensityMatrices VALUES ('state_werner_entangled', 'Werner_F075', 2, 4, 0);"
        )
        werner_entries = [
            (0, 0, 0.75 * 0.5 + 0.25 * 0.25, 0.0),
            (0, 3, 0.75 * 0.5, 0.0),
            (1, 1, 0.25 * 0.25, 0.0),
            (2, 2, 0.25 * 0.25, 0.0),
            (3, 0, 0.75 * 0.5, 0.0),
            (3, 3, 0.75 * 0.5 + 0.25 * 0.25, 0.0),
        ]
        for r, col, re, im in werner_entries:
            c.execute(
                "INSERT INTO DensityMatrixEntries VALUES ('state_werner_entangled', ?, ?, ?, ?);",
                (r, col, re, im),
            )

        # 4. Tripartite GHZ State |GHZ> = (|000> + |111>) / sqrt(2) in C^8
        c.execute("INSERT INTO DensityMatrices VALUES ('state_ghz_3', 'GHZ_3Qubit', 3, 8, 1);")
        ghz_entries = [
            (0, 0, 0.5, 0.0),
            (0, 7, 0.5, 0.0),
            (7, 0, 0.5, 0.0),
            (7, 7, 0.5, 0.0),
        ]
        for r, col, re, im in ghz_entries:
            c.execute(
                "INSERT INTO DensityMatrixEntries VALUES ('state_ghz_3', ?, ?, ?, ?);",
                (r, col, re, im),
            )

        # 5. Tripartite Separable State |000><000|
        c.execute(
            "INSERT INTO DensityMatrices VALUES ('state_separable_000', 'Separable_000', 3, 8, 1);"
        )
        c.execute(
            "INSERT INTO DensityMatrixEntries VALUES ('state_separable_000', 0, 0, 1.0, 0.0);"
        )

        self.conn.commit()

    # ------------------------------------------------------------------------
    # Witness Operator Population
    # ------------------------------------------------------------------------
    def populate_witness_operators(self) -> None:
        """Populates Entanglement Witness operators W_Bell and W_GHZ."""
        c = self.conn.cursor()
        c.execute("DELETE FROM WitnessEntries;")
        c.execute("DELETE FROM WitnessOperators;")

        # W_Bell = 0.5 I_4 - |Phi+><Phi+|
        # Diagonal: 0.5 - 0.5 = 0.0 at (0,0) and (3,3); 0.5 at (1,1) and (2,2)
        # Off-diagonal: -0.5 at (0,3) and (3,0)
        c.execute("INSERT INTO WitnessOperators VALUES ('wit_bell', 'Bell_PhiPlus', 4, 0.0);")
        w_bell_entries = [
            (0, 0, 0.0, 0.0),
            (0, 3, -0.5, 0.0),
            (1, 1, 0.5, 0.0),
            (2, 2, 0.5, 0.0),
            (3, 0, -0.5, 0.0),
            (3, 3, 0.0, 0.0),
        ]
        for r, col, re, im in w_bell_entries:
            c.execute(
                "INSERT INTO WitnessEntries VALUES ('wit_bell', ?, ?, ?, ?);", (r, col, re, im)
            )

        # W_GHZ = 0.5 I_8 - |GHZ><GHZ|
        c.execute("INSERT INTO WitnessOperators VALUES ('wit_ghz', 'GHZ_3Qubit', 8, 0.0);")
        for i in range(8):
            val = 0.0 if i in (0, 7) else 0.5
            c.execute(
                "INSERT INTO WitnessEntries VALUES ('wit_ghz', ?, ?, ?, ?);", (i, i, val, 0.0)
            )
        c.execute("INSERT INTO WitnessEntries VALUES ('wit_ghz', 0, 7, -0.5, 0.0);")
        c.execute("INSERT INTO WitnessEntries VALUES ('wit_ghz', 7, 0, -0.5, 0.0);")

        self.conn.commit()

    # ------------------------------------------------------------------------
    # Protocol Logging Methods
    # ------------------------------------------------------------------------
    def record_teleportation_run(
        self,
        run_id: int,
        input_state: str,
        m1: int,
        m2: int,
        applied_correction: str,
        output_fidelity: float,
        is_valid_protocol: int = 1,
    ) -> None:
        """Records a single teleportation run."""
        c = self.conn.cursor()
        c.execute(
            """INSERT INTO TeleportationRuns
               (run_id, input_state, m1, m2, applied_correction, output_fidelity, is_valid_protocol)
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (run_id, input_state, m1, m2, applied_correction, output_fidelity, is_valid_protocol),
        )
        self.conn.commit()

    def record_distillation_run(
        self,
        distillation_id: int,
        pair_label: str,
        round_num: int,
        input_fidelity: float,
        output_fidelity: float,
        is_coincident: int = 1,
    ) -> None:
        """Records an entanglement distillation purification round."""
        c = self.conn.cursor()
        c.execute(
            """INSERT INTO DistillationRuns
               (distillation_id, pair_label, round_num, input_fidelity, output_fidelity, is_coincident)
               VALUES (?, ?, ?, ?, ?, ?);""",
            (
                distillation_id,
                pair_label,
                round_num,
                input_fidelity,
                output_fidelity,
                is_coincident,
            ),
        )
        self.conn.commit()

    # ------------------------------------------------------------------------
    # Auditing Query Methods
    # ------------------------------------------------------------------------
    def verify_entanglement_witness(self) -> List[WitnessAuditResult]:
        """Audits all states against witness operators via ViewEntanglementWitnessAudit."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewEntanglementWitnessAudit ORDER BY witness_id, state_id;")
        rows = c.fetchall()
        return [
            WitnessAuditResult(
                witness_id=r["witness_id"],
                target_state=r["target_state"],
                state_id=r["state_id"],
                state_name=r["state_name"],
                separable_bound=r["separable_bound"],
                computed_trace_val=r["computed_trace_val"],
                is_entangled=bool(r["is_entangled"]),
                witness_status=r["witness_status"],
            )
            for r in rows
        ]

    def verify_teleportation_runs(self) -> List[TeleportationAuditResult]:
        """Audits teleportation runs via ViewTeleportationFidelityAudit."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewTeleportationFidelityAudit ORDER BY run_id;")
        rows = c.fetchall()
        return [
            TeleportationAuditResult(
                run_id=r["run_id"],
                input_state=r["input_state"],
                m1=r["m1"],
                m2=r["m2"],
                applied_correction=r["applied_correction"],
                expected_correction=r["expected_correction"],
                output_fidelity=r["output_fidelity"],
                is_valid_protocol=bool(r["is_valid_protocol"]),
                terminal_route=r["terminal_route"],
                audit_status=r["audit_status"],
            )
            for r in rows
        ]

    def verify_distillation_runs(self) -> List[DistillationAuditResult]:
        """Audits distillation rounds via ViewDistillationEfficiencyAudit."""
        c = self.conn.cursor()
        c.execute("SELECT * FROM ViewDistillationEfficiencyAudit ORDER BY distillation_id;")
        rows = c.fetchall()
        return [
            DistillationAuditResult(
                distillation_id=r["distillation_id"],
                pair_label=r["pair_label"],
                round_num=r["round_num"],
                input_fidelity=r["input_fidelity"],
                output_fidelity=r["output_fidelity"],
                fidelity_gain=r["fidelity_gain"],
                is_coincident=bool(r["is_coincident"]),
                distillation_status=r["distillation_status"],
            )
            for r in rows
        ]

    def close(self) -> None:
        self.conn.close()
