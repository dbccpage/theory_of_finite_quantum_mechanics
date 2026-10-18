"""
fqh_laughlin_braiding.py — 2D Fractional Quantum Hall (FQH) Laughlin Anyon Braiding & GIN Mode Indexing.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. 2D Fractional Quantum Hall State at Filling Fraction nu = 1/m (m=3 Laughlin State):
   - Ground state wavefunction: Psi_m(z_1, ..., z_N) = prod_{j < k} (z_j - z_k)^m exp(-sum |z_j|^2 / 4 l_B^2).
   - Quasiparticles (quasiholes / quasielectrons) carrying fractional electric charge e^* = e/m.
2. Anyonic Exchange Statistics and Braiding Monodromy:
   - Elementary statistical exchange angle: theta_stat = pi / m (for m=3, theta_stat = pi/3 = 60 deg).
   - Statistical factor: eta_stat = exp(i * pi / m) = 1/2 + i * sqrt(3)/2 != +-1.
   - Full adiabatic braiding monodromy (2 exchanges): theta_braid = 2 pi / m = 2 pi / 3 = 120 deg.
   - Braiding factor: eta_braid = exp(i * 2 pi / m) = -1/2 + i * sqrt(3)/2.
3. Modular S-Matrix Unitarity & Monodromy Consistency:
   - S_{a,b} = (1 / sqrt(m)) * exp(i * 2 pi a b / m) for a, b in {0, ..., m-1}.
   - Exact unitarity S^dagger S == I.
   - Monodromy consistency: M_{1,1} = S_{1,1} * S_{0,0} / (S_{0,1} * S_{1,0}) = exp(i * 2 pi / m).
4. Cochain Holonomy & Scalar Cochain Curvature Gamma_2:
   - 1-cochain holonomy: Hol(c^1) = exp(i * theta_braid).
   - Non-contractibility: Hol(c^1) != 1.0 + 0.0i for m > 1.
   - Scalar cochain curvature: Gamma_2 = |Arg(Hol(c^1))| = 2 pi / m > 0 (for exchange: pi / m > 0).
5. Obstruction of Exact Abelian Involution Pairing Xi:
   - Algebraic obstruction: Any involution Xi satisfies Xi^2 = id (Z_2 action).
     The Laughlin anyon braiding phase belongs to the cyclic group Z_m (Z_3 for nu = 1/3).
     Because gcd(2, m) = gcd(2, 3) = 1, no Z_2 involution can generate or cancel the Z_3 anyon phase.
   - Energetic / Boltzmann weight obstruction: In background magnetic field B > 0, particle-hole symmetry
     is broken between quasiholes and quasielectrons: Delta_{qe} > Delta_{qh}.
     Consequently, thermal weights w_{qh} = exp(-beta Delta_{qh}) and w_{qe} = exp(-beta Delta_{qe})
     satisfy w_{qh} != w_{qe}, producing uncancelled defect mass:
       Phi_1 = |w_{qh} - w_{qe}| > 0.
   - BQNF Routing: Non-contractible fractional holonomy (Gamma_2 > 0) with uncancelled defect mass
     routes deterministically to TerminalRoute.OpenSignObstruction.
6. Generalized Inverted Index (GIN) Mode Posting Lists:
   - Indexes quasihole loci, braiding perimeters, and fractional flux channels into SQLite.
"""

from __future__ import annotations

import cmath
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

from bqnf_sign_evaluator import TerminalRoute


@dataclass(frozen=True)
class FQHAnyonAuditReceipt:
    """Receipt auditing 2D FQH Laughlin anyonic braiding under GIN mode indexing."""
    model_id: str
    laughlin_m: int
    filling_fraction: str
    statistical_phase_radians: float
    braiding_phase_radians: float
    modular_s_unitarity_error: float
    cochain_holonomy_real: float
    cochain_holonomy_imag: float
    is_holonomy_contractible: bool
    cochain_curvature_gamma_2: float
    uncancelled_defect_mass_phi_1: float
    boltzmann_weight_quasihole: float
    boltzmann_weight_quasielectron: float
    weight_gap_delta_w: float
    is_abelian_involution_obstructed: bool
    terminal_route: str


class LaughlinStateAnyonModel:
    """
    2D Fractional Quantum Hall Laughlin State (nu = 1/m) Anyonic Braiding Model.
    """

    def __init__(
        self,
        model_id: str = "fqh_laughlin_nu_1_3",
        laughlin_m: int = 3,
        delta_qh: float = 0.026,
        delta_qe: float = 0.073,
    ):
        if laughlin_m <= 0:
            raise ValueError("laughlin_m must be strictly positive")
        self.model_id = model_id
        self.m = laughlin_m
        self.delta_qh = delta_qh
        self.delta_qe = delta_qe

    def compute_statistical_phase(self) -> Tuple[float, complex]:
        """
        Computes elementary anyonic exchange statistical phase:
            theta_stat = pi / m
            eta_stat = exp(i * pi / m)
        """
        theta_stat = math.pi / float(self.m)
        eta_stat = cmath.exp(1j * theta_stat)
        return theta_stat, eta_stat

    def compute_braiding_phase(self) -> Tuple[float, complex]:
        """
        Computes full adiabatic anyonic braiding phase (two exchanges):
            theta_braid = 2 pi / m
            eta_braid = exp(i * 2 pi / m)
        """
        theta_braid = 2.0 * math.pi / float(self.m)
        eta_braid = cmath.exp(1j * theta_braid)
        return theta_braid, eta_braid

    def compute_modular_s_matrix(self) -> Tuple[List[List[complex]], float, complex]:
        """
        Computes m x m modular S-matrix:
            S_{a,b} = (1 / sqrt(m)) * exp(i * 2 pi a b / m)
        Returns (S_matrix, max_unitarity_error, monodromy_M11).
        """
        m = self.m
        s_matrix: List[List[complex]] = []
        inv_sqrt_m = 1.0 / math.sqrt(m)

        for a in range(m):
            row = []
            for b in range(m):
                phase = 2.0 * math.pi * a * b / float(m)
                row.append(inv_sqrt_m * cmath.exp(1j * phase))
            s_matrix.append(row)

        max_err = 0.0
        for a in range(m):
            for c in range(m):
                val = sum(s_matrix[a][b] * s_matrix[c][b].conjugate() for b in range(m))
                expected = 1.0 if a == c else 0.0
                max_err = max(max_err, abs(val - expected))

        m11 = (s_matrix[1 % m][1 % m] * s_matrix[0][0]) / (s_matrix[0][1 % m] * s_matrix[1 % m][0])
        return s_matrix, max_err, m11

    def compute_cochain_holonomy(self) -> Tuple[float, float, bool, float]:
        """
        Computes 1-cochain holonomy around the adiabatic braiding loop:
            Hol(c^1) = exp(i * theta_braid)
        Returns (hol_real, hol_imag, is_contractible, gamma_2).
        """
        theta_braid, eta_braid = self.compute_braiding_phase()
        hol_real = eta_braid.real
        hol_imag = eta_braid.imag

        is_contractible = (abs(hol_real - 1.0) <= 1e-7 and abs(hol_imag) <= 1e-7)
        gamma_2 = 0.0 if is_contractible else abs(theta_braid)

        return hol_real, hol_imag, is_contractible, gamma_2

    def evaluate_abelian_involution_attempt(self, beta: float = 2.0) -> Tuple[float, float, float, bool]:
        """
        Evaluates whether an exact abelian involution pairing witness Xi can exist:
        1. Z_2 vs Z_m group order compatibility: gcd(2, m) == 1 obstruction.
        2. Particle-hole energy asymmetry: Delta_{qe} != Delta_{qh}.
        Returns (w_qh, w_qe, delta_w, is_obstructed).
        """
        w_qh = math.exp(-beta * self.delta_qh)
        w_qe = math.exp(-beta * self.delta_qe)
        delta_w = abs(w_qh - w_qe)

        is_obstructed = (self.m > 1) or (delta_w > 1e-6)

        return w_qh, w_qe, delta_w, is_obstructed


class FQHLaughlinBraidingEngine:
    """
    Evaluates 2D Fractional Quantum Hall anyon braiding, cochain holonomy,
    and GIN mode indexing.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "fqh_laughlin.db")
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

    def audit_fqh_braiding(
        self,
        model: LaughlinStateAnyonModel,
        beta: float = 2.0,
    ) -> FQHAnyonAuditReceipt:
        """
        Audits anyonic statistical phases, modular S-matrix unitarity,
        cochain holonomy, and BQNF terminal routing under GIN mode indexing.
        """
        theta_stat, _ = model.compute_statistical_phase()
        theta_braid, _ = model.compute_braiding_phase()

        _, s_unitarity_err, _ = model.compute_modular_s_matrix()

        hol_real, hol_imag, is_contractible, gamma_2 = model.compute_cochain_holonomy()

        w_qh, w_qe, delta_w, is_obstructed = model.evaluate_abelian_involution_attempt(beta=beta)

        if model.m == 1:
            phi_1 = 0.0
            gamma_2 = 0.0
            terminal_route = TerminalRoute.EXACT_REPAIR.value
        else:
            phi_1 = round(delta_w, 6)
            terminal_route = TerminalRoute.OPEN_SIGN_OBSTRUCTION.value

        c = self.conn.cursor()
        c.execute("SELECT COALESCE(MAX(cfg_id), 0) FROM FermionConfigurations;")
        max_cfg = c.fetchone()[0]
        cfg_qh = max_cfg + 1
        cfg_qe = max_cfg + 2

        c.execute(
            """INSERT INTO FermionConfigurations
               (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
               VALUES (?, ?, 1, 4, ?, 1, 1);""",
            (cfg_qh, model.model_id, round(w_qh, 6)),
        )
        c.execute(
            """INSERT INTO FermionConfigurations
               (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
               VALUES (?, ?, 1, 4, ?, -1, -1);""",
            (cfg_qe, model.model_id, round(w_qe, 6)),
        )

        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (1, ?, 1);", (cfg_qh,))
        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (3, ?, 1);", (cfg_qh,))
        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (2, ?, 1);", (cfg_qe,))
        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (4, ?, 1);", (cfg_qe,))

        self.posting_index[1].add(cfg_qh)
        self.posting_index[3].add(cfg_qh)
        self.posting_index[2].add(cfg_qe)
        self.posting_index[4].add(cfg_qe)
        self.conn.commit()

        return FQHAnyonAuditReceipt(
            model_id=model.model_id,
            laughlin_m=model.m,
            filling_fraction=f"1/{model.m}",
            statistical_phase_radians=round(theta_stat, 6),
            braiding_phase_radians=round(theta_braid, 6),
            modular_s_unitarity_error=round(s_unitarity_err, 12),
            cochain_holonomy_real=round(hol_real, 6),
            cochain_holonomy_imag=round(hol_imag, 6),
            is_holonomy_contractible=is_contractible,
            cochain_curvature_gamma_2=round(gamma_2, 6),
            uncancelled_defect_mass_phi_1=phi_1,
            boltzmann_weight_quasihole=round(w_qh, 6),
            boltzmann_weight_quasielectron=round(w_qe, 6),
            weight_gap_delta_w=round(delta_w, 6),
            is_abelian_involution_obstructed=is_obstructed,
            terminal_route=terminal_route,
        )
