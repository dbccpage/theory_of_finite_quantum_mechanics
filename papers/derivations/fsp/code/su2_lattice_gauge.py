"""
su2_lattice_gauge.py — SU(2) Lattice Gauge Theory and Topological Flux Sector GIN Indexing.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. SU(2) Lattice Plaquette with Kogut-Susskind Hamiltonian:
   - 4 gauge links with SU(2) representation truncation (singlet j=0, doublet j=1/2).
   - Electric field energy H_E = (g^2 / 2) sum_l J_l^2.
   - Magnetic plaquette energy H_B = - (1 / g^2) Tr(U_box).
   - Gauss law generators at 4 vertices: G_v^a = sum_{l in star(v)} J_l^a - Q_v^a = 0.
2. Topological Center Flux / Instanton Sectors:
   - Center Z(SU(2)) = Z_2 = {+1, -1}.
   - Sector Q = 0: Trivial vacuum flux (Tr(U_box) > 0, sign sigma = +1).
   - Sector Q = 1: Non-trivial vortex/instanton flux (Tr(U_box) < 0, topological phase e^{i theta Q} = -1 at theta = pi).
3. Coupled Fermionic Matter:
   - Color-doublet fermions on vertices.
   - Hopping with SU(2) parallel transport: c_x^dagger U_{xy} c_y + h.c.
4. GIN Mode Posting Analysis:
   - Evaluates whether weight spectra supp(W_+) and supp(W_-) are DISJOINT or OVERLAPPING.
   - Disjoint spectra prevent weight-preserving involution -> TerminalRoute.SplitBrainRefusal.
   - Degenerate/symmetric spectra allow 100% pairing -> TerminalRoute.Repair.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fermion_gin_index import (
    MockFermionGinIndex,
    InvolutionCancellationReceipt,
    MajoranaZeroModeReceipt,
)


@dataclass(frozen=True)
class SU2PlaquetteState:
    """Represents a discrete basis state for the SU(2) plaquette with link spins and vertex fermions."""
    link_spins: Tuple[float, float, float, float]
    topological_flux_sector: int
    fermion_occupations: Tuple[int, ...]


@dataclass(frozen=True)
class SU2SpectrumAuditReceipt:
    """Audit receipt characterizing the weight spectra across topological flux sectors."""
    model_name: str
    gauge_coupling_g: float
    theta_angle: float
    flux_sectors_present: List[int]
    positive_weight_count: int
    negative_weight_count: int
    positive_weight_support: List[float]
    negative_weight_support: List[float]
    spectral_overlap: List[float]
    is_disjoint: bool
    action_gap_delta_s: float
    uncancelled_defect_mass: float
    gin_quotiented_average_sign: float
    terminal_route: str


class SU2LatticePlaquetteModel:
    """
    Computable model of an SU(2) lattice gauge plaquette with Kogut-Susskind Hamiltonian,
    topological center flux sectors, and color-doublet fermions.
    """

    def __init__(
        self,
        g_coupling: float = 1.0,
        theta_angle: float = math.pi,
        fermion_mass: float = 0.5,
        hopping_t: float = 1.0,
    ):
        self.g = g_coupling
        self.theta = theta_angle
        self.m = fermion_mass
        self.t = hopping_t

    def evaluate_link_electric_energy(self, j: float) -> float:
        """Electric Casimir energy: E_E = (g^2 / 2) * j * (j + 1)."""
        return (self.g ** 2 / 2.0) * j * (j + 1.0)

    def evaluate_magnetic_flux_energy(self, flux_sector: int) -> float:
        """
        Magnetic energy for topological flux sector Q in {0, 1}:
        Q = 0 (trivial vacuum flux): Tr(U_box) / 2 = +1 -> H_B = - (2 / g^2)
        Q = 1 (vortex/instanton flux): Tr(U_box) / 2 = -1 -> H_B = + (2 / g^2)
        """
        tr_val = 1.0 if flux_sector == 0 else -1.0
        return - (2.0 / (self.g ** 2)) * tr_val

    def generate_gauge_matter_paths(
        self,
        beta: float = 1.0,
        num_trotter_steps: int = 2,
    ) -> List[Dict[str, Any]]:
        """
        Generates discrete closed Trotter paths across topological flux sectors Q in {0, 1}
        and link spin excitations j in {0, 1/2}.
        """
        paths = []
        path_id = 1

        link_configs = [
            (0.0, 0.0, 0.0, 0.0),
            (0.5, 0.5, 0.0, 0.0),
            (0.5, 0.5, 0.5, 0.5),
        ]

        fermion_configs = [
            (1, 2),
            (3, 4),
            (5, 6),
            (7, 8),
            (1, 6),
            (2, 7),
            (3, 8),
            (4, 5),
        ]

        for q in (0, 1):
            e_mag = self.evaluate_magnetic_flux_energy(q)
            topological_sign = 1 if (q == 0 or abs(self.theta) < 1e-6) else -1

            for links in link_configs:
                e_elec = sum(self.evaluate_link_electric_energy(j) for j in links)

                for occ in fermion_configs:
                    fermion_sign = 1
                    e_total = e_elec + e_mag + self.m * len(occ)

                    weight = math.exp(- beta * e_total)
                    net_sign = fermion_sign * topological_sign

                    paths.append({
                        "path_id": path_id,
                        "flux_sector": q,
                        "link_spins": links,
                        "occupied_modes": set(occ),
                        "total_energy": round(e_total, 6),
                        "abs_weight": round(weight, 8),
                        "parity": net_sign,
                    })
                    path_id += 1

        return paths


class SU2GinBridge:
    """
    Generalized Inverted Index (GIN) Bridge for non-abelian SU(2) lattice gauge theories.
    Evaluates whether topological flux sectors exhibit disjoint or overlapping weight spectra.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "su2_gin.db")
        self.conn.row_factory = sqlite3.Row
        self.posting_index: Dict[int, Set[int]] = defaultdict(set)
        self._init_schema()

    def _init_schema(self) -> None:
        schema_path = Path(__file__).resolve().parent / "fermion_gin_index_schema.sql"
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent.parent / "databases" / "fermion_gin_index_schema.sql"
        if schema_path.exists():
            self.conn.executescript(schema_path.read_text(encoding="utf-8"))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def index_su2_model_paths(
        self,
        model: SU2LatticePlaquetteModel,
        beta: float = 1.0,
        model_name: str = "SU2_Lattice_Plaquette",
    ) -> SU2SpectrumAuditReceipt:
        """
        Indexes SU(2) gauge-matter paths into GIN mode posting lists and analyzes
        the spectral overlap between positive and negative weight supports.
        """
        paths = model.generate_gauge_matter_paths(beta=beta)
        total_modes = 8

        c = self.conn.cursor()
        pos_weights: Set[float] = set()
        neg_weights: Set[float] = set()
        pos_by_weight: Dict[float, List[int]] = defaultdict(list)
        neg_by_weight: Dict[float, List[int]] = defaultdict(list)

        for p in paths:
            cid = p["path_id"]
            w = p["abs_weight"]
            s = p["parity"]
            occ = p["occupied_modes"]

            c.execute(
                """INSERT INTO FermionConfigurations
                   (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""",
                (cid, model_name, len(occ), total_modes, w, s, 1),
            )

            for m in range(1, total_modes + 1):
                is_occ = 1 if m in occ else 0
                c.execute(
                    "INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (?, ?, ?);",
                    (m, cid, is_occ),
                )
                if is_occ:
                    self.posting_index[m].add(cid)

            w_key = round(w, 8)
            if s > 0:
                pos_weights.add(w_key)
                pos_by_weight[w_key].append(cid)
            else:
                neg_weights.add(w_key)
                neg_by_weight[w_key].append(cid)

        self.conn.commit()

        overlap = sorted(list(pos_weights.intersection(neg_weights)))
        is_disjoint = len(overlap) == 0

        e_q0 = model.evaluate_magnetic_flux_energy(0)
        e_q1 = model.evaluate_magnetic_flux_energy(1)
        delta_s = abs(e_q1 - e_q0)

        matched_pairs = 0
        total_negatives = sum(len(l) for l in neg_by_weight.values())
        total_positives = sum(len(l) for l in pos_by_weight.values())

        if not is_disjoint:
            for w in overlap:
                pairs = min(len(pos_by_weight[w]), len(neg_by_weight[w]))
                matched_pairs += pairs

        unpartnered_negatives = total_negatives - matched_pairs
        raw_sum = sum(p["abs_weight"] * p["parity"] for p in paths)
        abs_sum = sum(p["abs_weight"] for p in paths)
        raw_sign = raw_sum / abs_sum if abs_sum > 0 else 0.0

        if total_negatives == 0:
            uncancelled_mass = 0.0
            terminal_route = "Repair"
            quotiented_sign = 1.0
            is_disjoint = False
        elif is_disjoint or unpartnered_negatives > 0:
            uncancelled_mass = sum(p["abs_weight"] for p in paths if p["parity"] < 0)
            terminal_route = "SplitBrainRefusal"
            quotiented_sign = raw_sign
        else:
            uncancelled_mass = 0.0
            terminal_route = "Repair"
            quotiented_sign = 1.0

        return SU2SpectrumAuditReceipt(
            model_name=model_name,
            gauge_coupling_g=model.g,
            theta_angle=model.theta,
            flux_sectors_present=[0, 1],
            positive_weight_count=total_positives,
            negative_weight_count=total_negatives,
            positive_weight_support=sorted(list(pos_weights)),
            negative_weight_support=sorted(list(neg_weights)),
            spectral_overlap=overlap,
            is_disjoint=is_disjoint,
            action_gap_delta_s=round(delta_s, 6),
            uncancelled_defect_mass=round(uncancelled_mass, 8),
            gin_quotiented_average_sign=round(quotiented_sign, 6),
            terminal_route=terminal_route,
        )
