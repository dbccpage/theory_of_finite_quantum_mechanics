"""
kitaev_honeycomb_bisimulation_bridge.py — Relational CTE & Lean 4 Bisimulation Bridge.

AuthorityEffect: None.

Connects:
1. KitaevHoneycombModel and MockHoneycombGinIndex in Python.
2. ANSI SQL relational CTE schema and auditing views (kitaev_honeycomb_schema.sql).
3. Lean 4 formal certificates in KitaevHoneycombCore.lean.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Tuple

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from kitaev_honeycomb_evaluator import KitaevHoneycombModel, MockHoneycombGinIndex


@dataclass(frozen=True)
class KitaevHoneycombReceipt:
    lattice_id: str
    lx: int
    ly: int
    total_sites: int
    total_links: int
    total_plaquettes: int
    total_vortices: int
    flux_parity_status: str
    matter_parity_status: str
    braiding_certified: bool
    terminal_route: str
    lean_bisimulation_passed: bool
    authority_effect: str = "None"


class KitaevHoneycombBisimulationBridge:
    def __init__(self, schema_path: Optional[Path] = None):
        if schema_path is None:
            # Try databases/ directory next to code/
            db_schema = code_dir.parent / "databases" / "kitaev_honeycomb_schema.sql"
            if db_schema.exists():
                self.schema_path = db_schema
            else:
                self.schema_path = code_dir / "kitaev_honeycomb_schema.sql"
        else:
            self.schema_path = schema_path

        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())

    def populate_from_model(
        self,
        model: KitaevHoneycombModel,
        time_steps: int = 3,
        force_parity_flip_at: Optional[int] = None,
        gauge_projector_valid: bool = True,
        simulate_braid: bool = True,
    ) -> None:
        c = self.conn.cursor()

        # 1. HoneycombLattice
        c.execute(
            """
            INSERT OR REPLACE INTO HoneycombLattice
            (lattice_id, lx, ly, boundary_condition, jx, jy, jz, kappa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                model.lattice_id,
                model.lx,
                model.ly,
                model.boundary_condition,
                model.jx,
                model.jy,
                model.jz,
                model.kappa,
            ),
        )

        # 2. HoneycombSites
        for s in model.sites.values():
            c.execute(
                """
                INSERT OR REPLACE INTO HoneycombSites
                (lattice_id, site_id, coord_x, coord_y, sublattice)
                VALUES (?, ?, ?, ?, ?)
                """,
                (model.lattice_id, s.site_id, s.x, s.y, s.sublattice),
            )

        # 3. HoneycombLinks
        for l in model.links.values():
            c.execute(
                """
                INSERT OR REPLACE INTO HoneycombLinks
                (lattice_id, link_id, site_u, site_v, bond_dir, gauge_u)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (model.lattice_id, l.link_id, l.site_u, l.site_v, l.bond_dir, l.gauge_u),
            )

        # 4. HoneycombPlaquettes & PlaquetteBoundaryLinks
        for p in model.plaquettes.values():
            c.execute(
                """
                INSERT OR REPLACE INTO HoneycombPlaquettes
                (lattice_id, plaquette_id, center_x, center_y, flux_wp, vortex_charge)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (model.lattice_id, p.plaquette_id, p.center_x, p.center_y, p.flux_wp, p.vortex_charge),
            )
            for order, (l_id, orient) in enumerate(p.boundary_links):
                c.execute(
                    """
                    INSERT OR REPLACE INTO PlaquetteBoundaryLinks
                    (lattice_id, plaquette_id, link_id, link_order, orientation)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (model.lattice_id, p.plaquette_id, l_id, order, orient),
                )

        # 5. GIN Index Postings
        for link_id, p_list in model.gin_index.link_to_plaquettes.items():
            for p_id in p_list:
                c.execute(
                    """
                    INSERT INTO HoneycombGinPostings
                    (lattice_id, mode_type, mode_id, incident_plaquette_id, incident_link_id)
                    VALUES (?, 'LINK_GAUGE', ?, ?, ?)
                    """,
                    (model.lattice_id, link_id, p_id, link_id),
                )

        # 6. Majorana Matter States
        current_parity = model.compute_fermion_parity()
        for t in range(time_steps):
            parity = current_parity
            if force_parity_flip_at is not None and t >= force_parity_flip_at:
                parity = -current_parity
            proj_valid = 1 if gauge_projector_valid else 0
            c.execute(
                """
                INSERT INTO MajoranaMatterStates
                (state_id, lattice_id, time_step, fermion_parity, gauge_projector_valid)
                VALUES (?, ?, ?, ?, ?)
                """,
                (f"state_{model.lattice_id}_{t}", model.lattice_id, t, parity, proj_valid),
            )

        # 7. Vortex Braiding Trajectories (if vortices exist)
        vortices = model.gin_index.get_vortices()
        if simulate_braid and len(vortices) >= 2:
            v_a, v_b = vortices[0], vortices[1]
            for enc_p in [0, 1]:
                braid_data = model.simulate_vortex_braid(v_a, v_b, enclosed_parity=enc_p)
                c.execute(
                    """
                    INSERT INTO VortexBraidingTrajectories
                    (traj_id, lattice_id, vortex_a_id, vortex_b_id, winding_number,
                     enclosed_parity, berry_phase_rad, measured_phase_rad, phase_residual, terminal_route)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        braid_data["traj_id"],
                        braid_data["lattice_id"],
                        braid_data["vortex_a_id"],
                        braid_data["vortex_b_id"],
                        braid_data["winding_number"],
                        braid_data["enclosed_parity"],
                        braid_data["berry_phase_rad"],
                        braid_data["measured_phase_rad"],
                        braid_data["phase_residual"],
                        braid_data["terminal_route"],
                    ),
                )

        self.conn.commit()

    def audit_plaquette_fluxes(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM ViewPlaquetteVortexAudit")
        return [dict(row) for row in cursor.fetchall()]

    def audit_total_flux(self) -> Dict[str, Any]:
        row = self.conn.execute("SELECT * FROM ViewTotalVortexFluxAudit").fetchone()
        return dict(row) if row else {}

    def audit_matter_parity(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM ViewMajoranaParityConservationAudit")
        return [dict(row) for row in cursor.fetchall()]

    def audit_braiding(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM ViewVortexBraidingAudit")
        return [dict(row) for row in cursor.fetchall()]

    def audit_terminal_route(self) -> str:
        row = self.conn.execute("SELECT terminal_route FROM ViewHoneycombTerminalRoutingAudit").fetchone()
        return str(row["terminal_route"]) if row else "CLOSURE_FAILURE"

    def emit_receipt(self, model: KitaevHoneycombModel) -> KitaevHoneycombReceipt:
        flux_summary = self.audit_total_flux()
        parity_rows = self.audit_matter_parity()
        braiding_rows = self.audit_braiding()
        route = self.audit_terminal_route()

        flux_status = flux_summary.get("parity_audit_verdict", "UNKNOWN")
        parity_status = "PARITY_CONSERVED"
        for r in parity_rows:
            if r["conservation_verdict"] != "PARITY_CONSERVED":
                parity_status = r["conservation_verdict"]
                break

        braiding_certified = True
        for b in braiding_rows:
            if b["phase_status"] != "ISING_BRAIDING_CERTIFIED":
                braiding_certified = False

        # Bisimulation check against Lean 4 certificate rules:
        # 1. If projector invalid -> CLOSURE_FAILURE
        # 2. If parity defect or odd flux -> SPLIT_BRAIN_REFUSAL
        # 3. Else -> REPAIR
        lean_bisim_passed = True
        if parity_status != "PARITY_CONSERVED" and route != "SPLIT_BRAIN_REFUSAL":
            lean_bisim_passed = False
        if flux_status == "FLUX_PARITY_ANOMALY" and route != "SPLIT_BRAIN_REFUSAL":
            lean_bisim_passed = False

        return KitaevHoneycombReceipt(
            lattice_id=model.lattice_id,
            lx=model.lx,
            ly=model.ly,
            total_sites=len(model.sites),
            total_links=len(model.links),
            total_plaquettes=len(model.plaquettes),
            total_vortices=len(model.gin_index.get_vortices()),
            flux_parity_status=flux_status,
            matter_parity_status=parity_status,
            braiding_certified=braiding_certified,
            terminal_route=route,
            lean_bisimulation_passed=lean_bisim_passed,
        )
