"""
chiral_superconductor_bisimulation_bridge.py — Relational CTE & Lean 4 Bisimulation Bridge.

AuthorityEffect: None.

Connects:
1. ChiralSuperconductor3DModel and MockChiralSuperconductorGinIndex in Python.
2. ANSI SQL relational CTE schema and auditing views (chiral_superconductor_schema.sql).
3. Lean 4 formal certificates in ChiralSuperconductorCore.lean.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Tuple

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from chiral_superconductor_evaluator import ChiralSuperconductor3DModel, MockChiralSuperconductorGinIndex


@dataclass(frozen=True)
class ChiralSuperconductorReceipt:
    lattice_id: str
    lx: int
    ly: int
    lz: int
    k0: float
    total_bulk_nodes: int
    net_chirality: int
    anomaly_status: str
    recorded_arcs: int
    expected_arcs: int
    bulk_boundary_status: str
    majorana_status: str
    inflow_verdict: str
    terminal_route: str
    lean_bisimulation_passed: bool
    authority_effect: str = "None"


class ChiralSuperconductorBisimulationBridge:
    def __init__(self, schema_path: Optional[Path] = None):
        if schema_path is None:
            # Try databases/ directory next to code/
            db_schema = code_dir.parent / "databases" / "chiral_superconductor_schema.sql"
            if db_schema.exists():
                self.schema_path = db_schema
            else:
                self.schema_path = code_dir / "chiral_superconductor_schema.sql"
        else:
            self.schema_path = schema_path

        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())

    def populate_from_model(self, model: ChiralSuperconductor3DModel) -> None:
        c = self.conn.cursor()
        data = model.export_relational_tuples()

        # 1. WeylSuperconductorLattice
        c.executemany(
            """
            INSERT OR REPLACE INTO WeylSuperconductorLattice
            (lattice_id, lx, ly, lz, k0, delta_0, mu, phs_symmetric)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data["WeylSuperconductorLattice"],
        )

        # 2. WeylBulkNodes
        c.executemany(
            """
            INSERT OR REPLACE INTO WeylBulkNodes
            (lattice_id, node_id, kx, ky, kz, chirality, monopole_charge)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            data["WeylBulkNodes"],
        )

        # 3. KzSliceTopologicalInvariants
        c.executemany(
            """
            INSERT OR REPLACE INTO KzSliceTopologicalInvariants
            (lattice_id, slice_id, kz_index, kz_val, chern_number, bulk_gap)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            data["KzSliceTopologicalInvariants"],
        )

        # 4. SurfaceMajoranaFermiArcs
        c.executemany(
            """
            INSERT OR REPLACE INTO SurfaceMajoranaFermiArcs
            (lattice_id, arc_id, node_start_id, node_end_id, surface_orientation,
             arc_length, is_self_conjugate, spectral_residual)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data["SurfaceMajoranaFermiArcs"],
        )

        # 5. SurfaceBulkSpectralFlowTrajectory
        c.executemany(
            """
            INSERT OR REPLACE INTO SurfaceBulkSpectralFlowTrajectory
            (step_id, lattice_id, time_step, flux_theta, bulk_pumped_charge,
             surface_pumped_charge, net_anomaly)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            data["SurfaceBulkSpectralFlowTrajectory"],
        )

        # 6. ChiralSuperconductorGinPostings
        c.executemany(
            """
            INSERT INTO ChiralSuperconductorGinPostings
            (lattice_id, mode_type, mode_id, target_id)
            VALUES (?, ?, ?, ?)
            """,
            data["ChiralSuperconductorGinPostings"],
        )

        self.conn.commit()

    def audit_chiral_anomaly(self) -> Dict[str, Any]:
        cursor = self.conn.execute("SELECT * FROM ViewChiralAnomalyCancellationAudit")
        row = cursor.fetchone()
        return dict(row) if row else {}

    def audit_surface_bulk_spectral_flow(self) -> Dict[str, Any]:
        cursor = self.conn.execute("SELECT * FROM ViewSurfaceBulkSpectralFlowAudit")
        row = cursor.fetchone()
        return dict(row) if row else {}

    def audit_majorana_arcs(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM ViewMajoranaFermiArcAudit")
        return [dict(row) for row in cursor.fetchall()]

    def audit_anomaly_inflow(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM ViewSurfaceAnomalyInflowAudit")
        return [dict(row) for row in cursor.fetchall()]

    def audit_terminal_route(self) -> str:
        row = self.conn.execute("SELECT terminal_route FROM ViewChiralSuperconductorTerminalRoutingAudit").fetchone()
        return str(row["terminal_route"]) if row else "CLOSURE_FAILURE"

    def emit_receipt(self, model: ChiralSuperconductor3DModel) -> ChiralSuperconductorReceipt:
        anomaly_dict = self.audit_chiral_anomaly()
        flow_dict = self.audit_surface_bulk_spectral_flow()
        arc_rows = self.audit_majorana_arcs()
        inflow_rows = self.audit_anomaly_inflow()
        route = self.audit_terminal_route()

        anomaly_status = anomaly_dict.get("anomaly_status", "CHIRAL_ANOMALY_DEFECT")
        bulk_boundary_status = flow_dict.get("bulk_boundary_status", "BULK_BOUNDARY_DISCREPANCY")
        
        majorana_status = "MAJORANA_SELF_CONJUGATE_VALID"
        for a in arc_rows:
            if a["majorana_status"] != "MAJORANA_SELF_CONJUGATE_VALID":
                majorana_status = a["majorana_status"]
                break

        inflow_verdict = "ANOMALY_INFLOW_CONSERVED"
        for i in inflow_rows:
            if i["inflow_verdict"] != "ANOMALY_INFLOW_CONSERVED":
                inflow_verdict = i["inflow_verdict"]
                break

        # Bisimulation verification against Lean 4 ChiralSuperconductorCore rules:
        # 1. Broken PHS or broken Majorana conjugacy -> CLOSURE_FAILURE
        # 2. Chiral anomaly defect or bulk-boundary discrepancy or inflow leak -> SPLIT_BRAIN_REFUSAL
        # 3. Else -> REPAIR
        lean_bisim_passed = True
        if not model.phs_symmetric and route != "CLOSURE_FAILURE":
            lean_bisim_passed = False
        if majorana_status != "MAJORANA_SELF_CONJUGATE_VALID" and route != "CLOSURE_FAILURE":
            lean_bisim_passed = False
        if anomaly_status != "ANOMALY_CANCELLED_VALID" and route != "SPLIT_BRAIN_REFUSAL":
            lean_bisim_passed = False
        if bulk_boundary_status != "BULK_BOUNDARY_MATCH" and route != "SPLIT_BRAIN_REFUSAL":
            lean_bisim_passed = False
        if inflow_verdict != "ANOMALY_INFLOW_CONSERVED" and route != "SPLIT_BRAIN_REFUSAL":
            lean_bisim_passed = False

        return ChiralSuperconductorReceipt(
            lattice_id=model.lattice_id,
            lx=model.lx,
            ly=model.ly,
            lz=model.lz,
            k0=model.k0,
            total_bulk_nodes=len(model.nodes),
            net_chirality=anomaly_dict.get("net_chirality", sum(n.chirality for n in model.nodes)),
            anomaly_status=anomaly_status,
            recorded_arcs=flow_dict.get("recorded_arcs", len(model.arcs)),
            expected_arcs=flow_dict.get("expected_total_arcs", 2),
            bulk_boundary_status=bulk_boundary_status,
            majorana_status=majorana_status,
            inflow_verdict=inflow_verdict,
            terminal_route=route,
            lean_bisimulation_passed=lean_bisim_passed,
        )
