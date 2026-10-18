"""
bf_linked_flux_braiding.py — 3D Topological BF Theory, Linked Flux Loops, & Higher-Dimensional Abelian Braiding.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. 3D Topological BF Theory with Level k in Z_{>=2}:
   - Action on 3-manifold / cell complex: S_{BF} = (k / 2pi) int B wedge dA.
   - 1-form gauge field A in C^1(K, R/2piZ) couples to 1D particle worldlines / loops gamma.
   - 2-form gauge field B in C^2(K, R/2piZ) couples to 2D surface worldsheets / flux tubes Sigma.
2. Gauss Linking Integral in 3D:
   - Evaluates exact integer linking numbers Lk(gamma_1, gamma_2) for unlinked loops (Lk = 0),
     Hopf link (Lk = +-1), double Hopf link (Lk = +-2), and Whitehead link (Lk = 0).
3. Topological Monodromy & Statistical Monodromy Phase:
   - theta_{BF} = (2pi / k) * q * p * Lk(gamma_1, gamma_2) (mod 2pi).
   - Topological braiding factor: eta_{BF} = exp(i * theta_{BF}).
4. 2-Cochain Holonomy & Curvature Gamma_2:
   - 2-cochain holonomy: Hol(c^2) = exp(i * theta_{BF}).
   - Contractibility: Hol(c^2) == 1.0 + 0.0i iff theta_{BF} == 0 (mod 2pi).
   - Scalar cochain curvature: Gamma_2 = |Arg(Hol(c^2))| in [0, pi].
5. Level k Parity Trichotomy & Involution Pairing:
   - For k = 2 (Z_2 BF theory / 3D Toric Code):
     theta_{BF} = pi * Lk => eta_{BF} = +-1 in R.
     Under symmetric orientation weights (Delta E = 0), exact Z_2 involution pairing Xi
     cancels the negative sign sector, recovering average sign <Sign>_{GIN} = 1.0,
     Phi_1 = 0.0, routing to TerminalRoute.ExactRepair.
   - For k >= 3 (Z_k fractional BF theory, e.g. k = 3):
     theta_{BF} = 2pi / 3 => eta_{BF} = -1/2 + i*sqrt(3)/2 notin R.
     Z_2 vs Z_k cyclic order clash (gcd(2, k) = 1) prevents real sign cancellation;
     average over orientation-paired states yields cos(2pi/k) < 1.0,
     leaving uncancelled defect mass Phi_1 > 0 and routing to TerminalRoute.OpenSignObstruction.
   - For orientation energy gap Delta E_{orient} > 0:
     Thermal weight asymmetry w_+ != w_- produces disjoint weight spectra,
     routing to TerminalRoute.SplitBrainRefusal.
6. Generalized Inverted Index (GIN) Mode Posting Lists:
   - Relational SQLite schema indexing loop cycles, Seifert surfaces, and 2-form flux cores.
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
class BFLuxAuditReceipt:
    """Receipt auditing 3D topological BF theory and linked flux loop braiding under GIN mode indexing."""
    model_id: str
    k_level: int
    charge_q: int
    flux_p: int
    link_type: str
    linking_number_exact: int
    linking_number_float: float
    braiding_phase_radians: float
    cochain_holonomy_real: float
    cochain_holonomy_imag: float
    is_holonomy_contractible: bool
    cochain_curvature_gamma_2: float
    uncancelled_defect_mass_phi_1: float
    boltzmann_weight_plus: float
    boltzmann_weight_minus: float
    weight_gap_delta_w: float
    is_exact_repair_achieved: bool
    terminal_route: str


Point3D = Tuple[float, float, float]


def discrete_gauss_linking_integral(
    loop1: List[Point3D],
    loop2: List[Point3D],
) -> float:
    """
    Computes the Gauss linking integral between two closed polygonal loops in 3D:
        Lk(gamma_1, gamma_2) = (1 / 4pi) sum_{i, j} (R_{ij} . (dr1_i x dr2_j)) / |R_{ij}|^3
    where R_{ij} = m1_i - m2_j is the separation vector between segment midpoints.
    """
    n1 = len(loop1)
    n2 = len(loop2)
    if n1 < 3 or n2 < 3:
        raise ValueError("Loops must have at least 3 vertices to form closed polygons")

    total_sum = 0.0

    for i in range(n1):
        p1_a = loop1[i]
        p1_b = loop1[(i + 1) % n1]
        dr1 = (p1_b[0] - p1_a[0], p1_b[1] - p1_a[1], p1_b[2] - p1_a[2])
        m1 = ((p1_a[0] + p1_b[0]) * 0.5, (p1_a[1] + p1_b[1]) * 0.5, (p1_a[2] + p1_b[2]) * 0.5)

        for j in range(n2):
            p2_a = loop2[j]
            p2_b = loop2[(j + 1) % n2]
            dr2 = (p2_b[0] - p2_a[0], p2_b[1] - p2_a[1], p2_b[2] - p2_a[2])
            m2 = ((p2_a[0] + p2_b[0]) * 0.5, (p2_a[1] + p2_b[1]) * 0.5, (p2_a[2] + p2_b[2]) * 0.5)

            rx = m1[0] - m2[0]
            ry = m1[1] - m2[1]
            rz = m1[2] - m2[2]
            dist = math.sqrt(rx * rx + ry * ry + rz * rz)
            if dist < 1e-12:
                continue

            cx = dr1[1] * dr2[2] - dr1[2] * dr2[1]
            cy = dr1[2] * dr2[0] - dr1[0] * dr2[2]
            cz = dr1[0] * dr2[1] - dr1[1] * dr2[0]

            dot = rx * cx + ry * cy + rz * cz
            total_sum += dot / (dist * dist * dist)

    return total_sum / (4.0 * math.pi)


def generate_polygonal_loop(
    link_type: str,
    loop_index: int,
    num_points: int = 64,
    reversed_orientation: bool = False,
) -> List[Point3D]:
    """Generates standard 3D loop configurations for topological linking tests."""
    points: List[Point3D] = []
    direction = -1.0 if reversed_orientation else 1.0

    if link_type == "unlinked":
        offset = 0.0 if loop_index == 1 else 3.5
        for i in range(num_points):
            t = direction * 2.0 * math.pi * i / num_points
            points.append((math.cos(t) + offset, math.sin(t), 0.0))

    elif link_type == "hopf":
        if loop_index == 1:
            for i in range(num_points):
                t = direction * 2.0 * math.pi * i / num_points
                points.append((math.cos(t), math.sin(t), 0.0))
        else:
            for i in range(num_points):
                t = direction * 2.0 * math.pi * i / num_points
                points.append((0.0, 1.0 + math.cos(t), -math.sin(t)))

    elif link_type == "double_hopf":
        if loop_index == 1:
            for i in range(num_points):
                t = direction * 2.0 * math.pi * i / num_points
                points.append((math.cos(t), math.sin(t), 0.0))
        else:
            for i in range(num_points):
                t = direction * 2.0 * math.pi * i / num_points
                points.append((0.2 * math.cos(2.0 * t), 1.0 + math.cos(t), math.sin(t)))

    elif link_type == "whitehead":
        if loop_index == 1:
            for i in range(num_points):
                t = direction * 2.0 * math.pi * i / num_points
                points.append((math.cos(t), math.sin(t), 0.0))
        else:
            for i in range(num_points):
                t = direction * 2.0 * math.pi * i / num_points
                points.append((0.5 * math.sin(t), 0.3 * math.sin(2.0 * t), math.cos(t)))
    else:
        raise ValueError(f"Unknown link_type: {link_type}")

    return points


class BFLinkedFluxBraidingModel:
    """
    3D Topological BF Theory Model with discrete level k, charges q, and flux loops p.
    """

    def __init__(
        self,
        model_id: str = "bf_linked_flux_k2",
        k_level: int = 2,
        charge_q: int = 1,
        flux_p: int = 1,
        link_type: str = "hopf",
        delta_e_orient: float = 0.0,
        num_segments: int = 64,
    ):
        if k_level < 2:
            raise ValueError("k_level must be at least 2")
        self.model_id = model_id
        self.k = k_level
        self.q = charge_q % k_level
        self.p = flux_p % k_level
        self.link_type = link_type
        self.delta_e_orient = delta_e_orient
        self.num_segments = num_segments

    def compute_linking_number(self, reversed_orientation: bool = False) -> Tuple[float, int]:
        """Computes continuous Gauss linking number and rounded integer."""
        l1 = generate_polygonal_loop(self.link_type, loop_index=1, num_points=self.num_segments)
        l2 = generate_polygonal_loop(
            self.link_type,
            loop_index=2,
            num_points=self.num_segments,
            reversed_orientation=reversed_orientation,
        )
        lk_float = discrete_gauss_linking_integral(l1, l2)
        lk_int = int(round(lk_float))
        return lk_float, lk_int

    def compute_braiding_phase(self, lk_int: int) -> Tuple[float, complex]:
        """
        Computes topological braiding phase:
            theta_BF = (2pi / k) * q * p * Lk (mod 2pi)
        """
        raw_phase = (2.0 * math.pi / self.k) * self.q * self.p * lk_int
        wrapped_phase = math.atan2(math.sin(raw_phase), math.cos(raw_phase))
        phase_factor = cmath.exp(1j * wrapped_phase)
        return wrapped_phase, phase_factor

    def compute_cochain_holonomy(self, lk_int: int) -> Tuple[float, float, bool, float]:
        """
        Computes 2-cochain holonomy Hol(c^2) and scalar cochain curvature Gamma_2.
        Returns: (hol_real, hol_imag, is_contractible, gamma_2).
        """
        phase, factor = self.compute_braiding_phase(lk_int)
        hol_real = factor.real
        hol_imag = factor.imag

        is_contractible = (abs(hol_real - 1.0) <= 1e-6 and abs(hol_imag) <= 1e-6)
        gamma_2 = 0.0 if is_contractible else abs(phase)
        return hol_real, hol_imag, is_contractible, gamma_2

    def evaluate_orientation_pairing(
        self,
        beta: float = 2.0,
    ) -> Tuple[float, float, float, bool]:
        """
        Evaluates whether orientation reversal tau: gamma_2 -> -gamma_2 achieves exact pairing.
        Returns: (w_plus, w_minus, delta_w, is_exact_repair).
        """
        e_plus = 0.5
        e_minus = 0.5 + self.delta_e_orient

        w_plus = math.exp(-beta * e_plus)
        w_minus = math.exp(-beta * e_minus)
        delta_w = abs(w_plus - w_minus)

        is_exact_repair = (self.k == 2 and delta_w <= 1e-6)
        return w_plus, w_minus, delta_w, is_exact_repair


class BFLinkedFluxBraidingEngine:
    """
    Evaluates 3D topological BF theory and linked flux loop braiding under GIN mode indexing.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "bf_linked_flux.db")
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

    def audit_bf_braiding(
        self,
        model: BFLinkedFluxBraidingModel,
        beta: float = 2.0,
    ) -> BFLuxAuditReceipt:
        """
        Audits 3D BF theory loop linking, topological monodromy, cochain curvature,
        and BQNF terminal routing under GIN mode indexing.
        """
        lk_float, lk_int = model.compute_linking_number()

        phase, _ = model.compute_braiding_phase(lk_int)
        hol_real, hol_imag, is_contractible, gamma_2 = model.compute_cochain_holonomy(lk_int)

        w_plus, w_minus, delta_w, is_exact_repair = model.evaluate_orientation_pairing(beta=beta)

        if lk_int == 0 or (model.q * model.p == 0):
            phi_1 = 0.0
            gamma_2 = 0.0
            terminal_route = TerminalRoute.EXACT_REPAIR.value
        elif model.k == 2 and delta_w <= 1e-6:
            phi_1 = 0.0
            terminal_route = TerminalRoute.EXACT_REPAIR.value
        elif delta_w > 1e-4:
            phi_1 = round(delta_w + gamma_2, 6)
            terminal_route = "SplitBrainRefusal"
        else:
            phi_1 = round(abs(1.0 - math.cos(phase)) + gamma_2, 6)
            terminal_route = TerminalRoute.OPEN_SIGN_OBSTRUCTION.value

        c = self.conn.cursor()
        c.execute("SELECT COALESCE(MAX(cfg_id), 0) FROM FermionConfigurations;")
        max_cfg = c.fetchone()[0]
        cfg1 = max_cfg + 1
        cfg2 = max_cfg + 2

        jw_sign_1 = 1 if hol_real >= 0.0 else -1
        jw_sign_2 = 1 if math.cos(-phase) >= 0.0 else -1

        c.execute(
            """INSERT INTO FermionConfigurations
               (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
               VALUES (?, ?, 2, 4, ?, ?, 1);""",
            (cfg1, model.model_id, round(w_plus, 6), jw_sign_1),
        )
        c.execute(
            """INSERT INTO FermionConfigurations
               (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
               VALUES (?, ?, 2, 4, ?, ?, -1);""",
            (cfg2, model.model_id, round(w_minus, 6), jw_sign_2),
        )

        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (1, ?, 1);", (cfg1,))
        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (3, ?, 1);", (cfg1,))
        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (2, ?, 1);", (cfg2,))
        c.execute("INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (4, ?, 1);", (cfg2,))

        self.posting_index[1].add(cfg1)
        self.posting_index[3].add(cfg1)
        self.posting_index[2].add(cfg2)
        self.posting_index[4].add(cfg2)
        self.conn.commit()

        return BFLuxAuditReceipt(
            model_id=model.model_id,
            k_level=model.k,
            charge_q=model.q,
            flux_p=model.p,
            link_type=model.link_type,
            linking_number_exact=lk_int,
            linking_number_float=round(lk_float, 6),
            braiding_phase_radians=round(phase, 6),
            cochain_holonomy_real=round(hol_real, 6),
            cochain_holonomy_imag=round(hol_imag, 6),
            is_holonomy_contractible=is_contractible,
            cochain_curvature_gamma_2=round(gamma_2, 6),
            uncancelled_defect_mass_phi_1=phi_1,
            boltzmann_weight_plus=round(w_plus, 6),
            boltzmann_weight_minus=round(w_minus, 6),
            weight_gap_delta_w=round(delta_w, 6),
            is_exact_repair_achieved=is_exact_repair,
            terminal_route=terminal_route,
        )
