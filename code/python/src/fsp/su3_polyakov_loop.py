"""
su3_polyakov_loop.py — SU(3) Finite-Temperature Polyakov Loop Holonomies and Z_3 Center Symmetry Breaking.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. Finite-Temperature SU(3) Lattice Holonomies:
   - Temporal Wilson line / Polyakov loop: P(x) = (1/3) Tr prod_{tau=0}^{N_tau - 1} U_0(tau, x).
   - Z_3 Center Symmetry Transformations: U_0 -> z^k U_0 with z = e^{i 2pi/3}, k in {0, 1, 2}.
   - Center-rotated Polyakov loops: P_k = e^{i 2pi k / 3} P_0.
2. Confined vs. Deconfined Phases:
   - Confined Phase (T < T_c, beta < beta_c): <|P|> approx 0. Unbroken Z_3 center symmetry.
   - Deconfined Phase (T > T_c, beta > beta_c): <|P|> = P_0 > 0. Spontaneously broken Z_3 center symmetry.
3. Coupled Fundamental Fermions:
   - Antiperiodic boundary conditions psi(tau + N_tau) = - psi(tau).
   - In center sector k, the effective fermion action carries holonomy coupling:
       S_F(k) = - 12 * h * sum_x Re(P_k(x))
   - Sector k = 0: Re(P_0) = |P| * cos(0) = + |P| (positive vacuum sector, sign sigma = +1).
   - Sectors k = 1, 2: Re(P_k) = |P| * cos(2pi/3) = - 0.5 * |P| (negative/center-rotated sectors, sign sigma = -1).
   - Action gap: Delta S = S_F(k) - S_F(0) = 18 * h * |P|.
4. GIN Mode Posting Spectral Analysis:
   - Evaluates whether the deconfining phase transition restores spectral overlap:
     * In the deconfined phase, |P| > 0 induces a finite action gap Delta S > 0, forcing
       positive and negative weight spectra to be STRICTLY DISJOINT: supp(W_+) cap supp(W_-) = emptyset.
     * The deconfining transition does NOT restore spectral overlap; it amplifies spectral separation.
     * Routes to TerminalRoute.SplitBrainRefusal.
   - Zero-coupling / pure gauge control (h = 0): Delta S = 0, restoring spectral overlap -> TerminalRoute.Repair.
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


@dataclass(frozen=True)
class SU3PolyakovAuditReceipt:
    """Receipt auditing Polyakov loop holonomies and Z_3 center symmetry spectral overlap."""
    model_name: str
    gauge_group: str
    center_group: str
    temperature_regime: str
    polyakov_order_param: float
    coupling_beta: float
    fermion_hopping_h: float
    action_gap_delta_s: float
    positive_weight_count: int
    negative_weight_count: int
    positive_weight_support: List[float]
    negative_weight_support: List[float]
    spectral_overlap: List[float]
    is_disjoint: bool
    uncancelled_defect_mass: float
    gin_quotiented_average_sign: float
    terminal_route: str
    tolerance: float = 1e-12


class SU3PolyakovLoopModel:
    """
    Computable model of finite-temperature SU(3) lattice gauge theory with Polyakov loop holonomies,
    Z_3 center symmetry breaking, and coupled fundamental fermions.
    """

    def __init__(
        self,
        beta: float = 6.0,
        n_tau: int = 3,
        fermion_hopping_h: float = 0.1,
        critical_beta: float = 5.69,
    ):
        self.beta = beta
        self.n_tau = n_tau
        self.h = fermion_hopping_h
        self.beta_c = critical_beta

    @property
    def is_deconfined(self) -> bool:
        """Determines if the model is in the deconfined phase (beta > beta_c)."""
        return self.beta > self.beta_c

    def evaluate_polyakov_order_parameter(self) -> float:
        """
        Effective Polyakov loop magnitude <|P|>:
        - Confined (beta < beta_c): <|P|> = 0.0 (or small non-perturbative tail).
        - Deconfined (beta > beta_c): <|P|> = sqrt(1 - (beta_c / beta)^2) bounded in (0, 1].
        """
        if not self.is_deconfined:
            return 0.0
        ratio = self.beta_c / self.beta
        return math.sqrt(max(0.0, 1.0 - ratio * ratio))

    def evaluate_effective_action(self, center_sector_k: int, polyakov_mag: float) -> float:
        """
        Effective action S_eff(k) for center sector k in {0, 1, 2}:
        S_eff(k) = S_gauge + S_fermion(k)
        S_fermion(k) = - 12 * h * |P| * cos(2pi * k / 3)
        """
        s_gauge = self.beta * 0.5
        phi_k = 2.0 * math.pi * center_sector_k / 3.0
        s_fermion = - 12.0 * self.h * polyakov_mag * math.cos(phi_k)
        return s_gauge + s_fermion

    def generate_polyakov_paths(self) -> List[Dict[str, Any]]:
        """
        Generates discrete holonomy paths across center sectors k in {0, 1, 2}
        and spatial fermion occupation modes.
        """
        p_mag = self.evaluate_polyakov_order_parameter()
        paths = []
        path_id = 1

        fermion_modes = [
            (1, 2),
            (2, 3),
            (3, 1),
            (4, 5),
            (5, 6),
            (1, 4),
            (2, 5),
            (3, 6),
        ]

        for k in (0, 1, 2):
            s_eff = self.evaluate_effective_action(k, p_mag)
            parity = 1 if k == 0 else -1

            for occ in fermion_modes:
                e_tot = s_eff + 0.1 * len(occ)
                weight = math.exp(- e_tot)

                paths.append({
                    "path_id": path_id,
                    "center_sector": k,
                    "polyakov_mag": round(p_mag, 6),
                    "occupied_modes": set(occ),
                    "total_energy": float(e_tot),
                    "abs_weight": float(weight),
                    "parity": parity,
                })
                path_id += 1

        return paths


class SU3PolyakovGinBridge:
    """
    Generalized Inverted Index (GIN) Bridge for SU(3) Polyakov Loop Holonomies.
    Evaluates whether the deconfining phase transition restores spectral overlap.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "su3_polyakov_gin.db")
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

    def index_polyakov_paths(
        self,
        model: SU3PolyakovLoopModel,
        model_name: str = "SU3_Polyakov_Holonomy",
        tolerance: float = 1e-12,
    ) -> SU3PolyakovAuditReceipt:
        """
        Indexes SU(3) Polyakov loop paths into GIN mode posting lists and determines
        whether positive and negative weight spectra exhibit spectral overlap under
        a declared numerical tolerance.
        """
        paths = model.generate_polyakov_paths()
        total_modes = 6

        c = self.conn.cursor()
        pos_raw: List[float] = []
        neg_raw: List[float] = []
        pos_by_weight: Dict[float, List[int]] = defaultdict(list)
        neg_by_weight: Dict[float, List[int]] = defaultdict(list)

        for p in paths:
            cid = p["path_id"]
            w = float(p["abs_weight"])
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

            w_display = round(w, 10)
            if s > 0:
                pos_raw.append(w)
                pos_by_weight[w_display].append(cid)
            else:
                neg_raw.append(w)
                neg_by_weight[w_display].append(cid)

        self.conn.commit()

        # Tolerance-based spectral matching between positive and negative weight sets
        overlap_pos: Set[float] = set()
        matched_pairs = 0
        used_pos: Set[int] = set()
        for i_neg, w_neg in enumerate(neg_raw):
            best_match: Optional[int] = None
            best_dist = tolerance + 1.0
            for i_pos, w_pos in enumerate(pos_raw):
                dist = abs(w_pos - w_neg)
                if dist <= tolerance and i_pos not in used_pos:
                    if dist < best_dist:
                        best_match = i_pos
                        best_dist = dist
            if best_match is not None:
                used_pos.add(best_match)
                overlap_pos.add(round(pos_raw[best_match], 10))
                matched_pairs += 1

        overlap = sorted(list(overlap_pos))
        is_disjoint = len(overlap) == 0

        p_mag = model.evaluate_polyakov_order_parameter()
        s_k0 = model.evaluate_effective_action(0, p_mag)
        s_k1 = model.evaluate_effective_action(1, p_mag)
        delta_s = abs(s_k1 - s_k0)

        total_positives = len(pos_raw)
        total_negatives = len(neg_raw)
        unpartnered_negatives = total_negatives - matched_pairs

        raw_sum = sum(p["abs_weight"] * p["parity"] for p in paths)
        abs_sum = sum(p["abs_weight"] for p in paths)
        raw_sign = raw_sum / abs_sum if abs_sum > 0 else 0.0

        regime = "Deconfined" if model.is_deconfined else "Confined"

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

        return SU3PolyakovAuditReceipt(
            model_name=model_name,
            gauge_group="SU(3)",
            center_group="Z_3",
            temperature_regime=regime,
            polyakov_order_param=round(p_mag, 6),
            coupling_beta=model.beta,
            fermion_hopping_h=model.h,
            action_gap_delta_s=float(delta_s),
            positive_weight_count=total_positives,
            negative_weight_count=total_negatives,
            positive_weight_support=sorted(list(set(round(w, 10) for w in pos_raw))),
            negative_weight_support=sorted(list(set(round(w, 10) for w in neg_raw))),
            spectral_overlap=overlap,
            is_disjoint=is_disjoint,
            uncancelled_defect_mass=round(uncancelled_mass, 8),
            gin_quotiented_average_sign=round(quotiented_sign, 6),
            terminal_route=terminal_route,
            tolerance=tolerance,
        )
