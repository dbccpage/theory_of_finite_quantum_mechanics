"""
bf_topological_braiding.py — 3D Topological BF Theory, Linked Flux Loop Braiding, & Higher-Dimensional Cochain Holonomy.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. 3D Abelian BF Topological Quantum Field Theory:
   - Spacetime: 4D spacetime / 3 spatial dimensions M_3.
   - Gauge fields: 1-form A in Omega^1(M_3) (particle connections) and 2-form B in Omega^2(M_3) (flux loop connections).
   - Topological action: S_{BF} = (K / 2 pi) int B /\\ d A, with integer level K >= 1 (e.g. K=2 for Z_2 toric code / topological order).
   - Observables: Wilson loops W_A(gamma_1) = exp(i oint_{gamma_1} A) and Wilson surfaces W_B(Sigma_2) = exp(i int_{Sigma_2} B).
2. Gauss Linking Integral & Topological Statistical Phase:
   - For closed spatial loops gamma_1, gamma_2 subset M_3:
     Lk(gamma_1, gamma_2) = (1 / 4 pi) oint_{gamma_1} oint_{gamma_2} [(r_1 - r_2) . (dr_1 x dr_2)] / |r_1 - r_2|^3 in Z.
   - Abelian exchange / braiding statistical phase:
     theta_{BF} = (2 pi / K) * Lk(gamma_1, gamma_2).
   - 2-cochain holonomy along linked loop configuration:
     Hol(gamma_1, gamma_2) = exp(i * theta_{BF}).
   - Cochain curvature:
     Gamma_2 = |Hol - 1| = 2 * |sin(theta_{BF} / 2)|.
     - Unlinked loops (Lk = 0): theta_{BF} = 0, Hol = 1.0, Gamma_2 = 0.0 (contractible).
     - Hopf link (Lk = 1, K = 2): theta_{BF} = pi, Hol = -1.0, Gamma_2 = 2.0.
     - Hopf link (Lk = 1, K = 3): theta_{BF} = 2 pi / 3, Hol = -0.5 + i sqrt(3)/2, Gamma_2 = sqrt(3) approx 1.732051.
3. Orientation Reversal Parity Involution Xi & Loop Ensembles:
   - Reversing loop orientation Xi: (gamma_1, gamma_2) |-> (gamma_1, -gamma_2) reverses Gauss linking number:
     Lk(gamma_1, -gamma_2) = -Lk(gamma_1, gamma_2) ==> theta_{BF}(Xi) = -theta_{BF}.
   - In an orientation-symmetric ensemble (linking chemical potential mu_L = 0):
     w(Lk=+1) = w(Lk=-1) = w_0.
     The sum over orientation-reversed pairs yields real amplitudes:
       w_0 * (exp(i theta_{BF}) + exp(-i theta_{BF})) = 2 w_0 cos(theta_{BF}).
     Imaginary holonomy vanishes identically.
     Under exact sign-cancelling involution pairing (e.g. matched positive and negative configurations),
     uncancelled defect mass vanishes (Phi_1 = 0.0), recovering <Sign> = 1.0 and routing deterministically
     to TerminalRoute.ExactRepair.
   - In a chiral / asymmetric flux ensemble (mu_L > 0, e.g. background chiral potential or Chern-Simons coupling):
     w(Lk=+1) / w(Lk=-1) = exp(2 beta mu_L) > 1.
     The weight asymmetry Delta w = w_+ - w_- > 0 breaks exact cancellation, leaving non-contractible holonomy
     and uncancelled defect mass Phi_1 = Delta w + Gamma_2 > 0, routing deterministically to TerminalRoute.OpenSignObstruction.
   - In Z_2 BF theory (K = 2) with link creation energy Delta E_{link} > 0:
     Unlinked states have sign +1 (weight w_0 = 1), linked states have sign -1 (weight w_1 = exp(-beta Delta E_{link})).
     Average sign: <Sign> = tanh(beta Delta E_{link} / 2) < 1.0.
     Uncancelled defect mass Phi_1 = 2 w_1 > 0 with Gamma_2 = 2.0 routes deterministically to TerminalRoute.OpenSignObstruction.
4. Generalized Inverted Index (GIN) Mode Posting Lists:
   - Indexes loop coordinates, Gauss linking invariants, orientation parity sectors, and sign pairing into SQLite.
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
class BFLoopBraidingAuditReceipt:
    """Receipt auditing 3D topological BF theory and linked loop braiding under GIN mode indexing."""
    model_id: str
    level_k: int
    linking_number: int
    gauss_integral_raw: float
    statistical_phase_radians: float
    cochain_holonomy_real: float
    cochain_holonomy_imag: float
    cochain_curvature_gamma_2: float
    is_holonomy_contractible: bool
    is_orientation_symmetric: bool
    weight_asymmetry_delta_w: float
    uncancelled_defect_mass_phi_1: float
    average_sign: float
    is_exact_parity_paired: bool
    terminal_route: str


class BFTopologicalModel:
    """
    3D Topological BF Theory & Linked Flux Loop Braiding Model.
    """

    def __init__(
        self,
        model_id: str = "bf_theory_level_2",
        level_k: int = 2,
        beta: float = 1.0,
        mu_l: float = 0.0,
        delta_e_link: float = 1.0,
        num_loop_points: int = 120,
    ):
        if level_k < 1:
            raise ValueError("BF level K must be an integer >= 1.")
        self.model_id = model_id
        self.level_k = level_k
        self.beta = beta
        self.mu_l = mu_l
        self.delta_e_link = delta_e_link
        self.num_loop_points = num_loop_points

    def generate_hopf_link_geometry(self) -> Tuple[List[List[float]], List[List[float]], List[List[float]], List[List[float]]]:
        """
        Generates 3D coordinates for standard Hopf link and orientation-reversed / unlinked configurations:
        - c1: Circle in xy-plane centered at origin, radius 1.0.
        - c2_linked: Circle in xz-plane centered at (0.5, 0, 0), radius 1.0 (Lk = +1 or -1).
        - c2_reversed: Circle c2 with reversed parameterization t -> -t.
        - c2_unlinked: Circle in xz-plane shifted to (3.0, 0, 0) (Lk = 0).
        """
        n = self.num_loop_points
        # Circle 1: in xy-plane, normal = z
        c1 = [
            [math.cos(2.0 * math.pi * i / n), math.sin(2.0 * math.pi * i / n), 0.0]
            for i in range(n)
        ]

        # Circle 2 (Linked): in xz-plane, normal = y, centered at (0.5, 0, 0)
        # Orientation chosen so that Lk = +1
        c2_linked = [
            [0.5 + math.cos(2.0 * math.pi * i / n), 0.0, -math.sin(2.0 * math.pi * i / n)]
            for i in range(n)
        ]

        # Circle 2 (Reversed): parameterization reversed
        c2_reversed = [
            [0.5 + math.cos(-2.0 * math.pi * i / n), 0.0, -math.sin(-2.0 * math.pi * i / n)]
            for i in range(n)
        ]

        # Circle 2 (Unlinked): shifted outside c1
        c2_unlinked = [
            [3.0 + math.cos(2.0 * math.pi * i / n), 0.0, -math.sin(2.0 * math.pi * i / n)]
            for i in range(n)
        ]

        return c1, c2_linked, c2_reversed, c2_unlinked

    @staticmethod
    def compute_gauss_linking_number(c1: List[List[float]], c2: List[List[float]]) -> float:
        """
        Computes the Gauss linking integral:
          Lk(c1, c2) = (1 / 4 pi) sum_{i, j} [(r1_mid - r2_mid) . (dr1 x dr2)] / |r1_mid - r2_mid|^3.
        """
        n1 = len(c1)
        n2 = len(c2)

        dr1 = [
            [c1[(i + 1) % n1][d] - c1[i][d] for d in range(3)]
            for i in range(n1)
        ]
        dr2 = [
            [c2[(j + 1) % n2][d] - c2[j][d] for d in range(3)]
            for j in range(n2)
        ]
        mid1 = [
            [(c1[i][d] + c1[(i + 1) % n1][d]) / 2.0 for d in range(3)]
            for i in range(n1)
        ]
        mid2 = [
            [(c2[j][d] + c2[(j + 1) % n2][d]) / 2.0 for d in range(3)]
            for j in range(n2)
        ]

        total = 0.0
        for i in range(n1):
            m1 = mid1[i]
            d1 = dr1[i]
            for j in range(n2):
                m2 = mid2[j]
                d2 = dr2[j]
                diff = [m1[0] - m2[0], m1[1] - m2[1], m1[2] - m2[2]]
                dist = math.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)
                if dist < 1e-12:
                    continue
                # cross product dr1 x dr2
                cross = [
                    d1[1] * d2[2] - d1[2] * d2[1],
                    d1[2] * d2[0] - d1[0] * d2[2],
                    d1[0] * d2[1] - d1[1] * d2[0],
                ]
                dot = diff[0] * cross[0] + diff[1] * cross[1] + diff[2] * cross[2]
                total += dot / (dist**3)

        return total / (4.0 * math.pi)

    def evaluate_loop_phase_and_holonomy(self, lk: int) -> Tuple[float, complex, float]:
        """
        Returns (theta_bf, holonomy, cochain_curvature_gamma_2) for integer linking number lk:
          theta_bf = 2 pi lk / K
          holonomy = exp(i theta_bf)
          gamma_2 = |holonomy - 1| = 2 |sin(theta_bf / 2)|
        """
        theta_bf = (2.0 * math.pi * lk) / self.level_k
        holonomy = cmath.exp(1j * theta_bf)
        gamma_2 = abs(holonomy - 1.0)
        return theta_bf, holonomy, gamma_2

    def evaluate_statistical_ensemble(self, is_chiral: bool = False, is_z2_energy_split: bool = False) -> Tuple[float, float, float, float, bool]:
        """
        Evaluates loop configuration weights and sign cancellation:
        - If is_chiral is True (mu_l > 0):
            w_+ = exp(beta * mu_l), w_- = exp(-beta * mu_l).
            Delta w = |w_+ - w_-| > 0.
            Pairing is broken.
        - If is_z2_energy_split is True (Z_2 link tension):
            w_unlinked = 1.0, w_linked = exp(-beta * delta_e_link).
            avg_sign = (w_unlinked - w_linked) / (w_unlinked + w_linked).
            Delta w = 2.0 * w_linked.
        - Else (symmetric, mu_l = 0):
            w_+ = w_- = 1.0.
            Delta w = 0.0.
            Exact pairing holds.
        Returns (w_pos, w_neg, delta_w, avg_sign, is_paired).
        """
        if is_chiral:
            w_pos = math.exp(self.beta * self.mu_l)
            w_neg = math.exp(-self.beta * self.mu_l)
            delta_w = abs(w_pos - w_neg)
            avg_sign = (w_pos + w_neg * math.cos(2.0 * math.pi / self.level_k)) / (w_pos + w_neg)
            is_paired = False
        elif is_z2_energy_split:
            w_pos = 1.0
            w_neg = math.exp(-self.beta * self.delta_e_link)
            delta_w = 2.0 * w_neg
            avg_sign = (w_pos - w_neg) / (w_pos + w_neg)
            is_paired = False
        else:
            w_pos = 1.0
            w_neg = 1.0
            delta_w = 0.0
            avg_sign = 1.0
            is_paired = True

        return w_pos, w_neg, delta_w, avg_sign, is_paired


class BFTopologicalBraidingEngine:
    """
    Evaluates 3D topological BF theory, Gauss linking numbers, loop holonomies,
    orientation parity pairing, and GIN mode indexing into relational SQLite.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "bf_braiding.db")
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
        model: BFTopologicalModel,
        is_chiral: bool = False,
        is_z2_energy_split: bool = False,
        test_unlinked: bool = False,
    ) -> BFLoopBraidingAuditReceipt:
        """
        Executes audit of 3D BF theory loop linking and higher-dimensional cochain holonomy:
        1. Computes Gauss linking numbers for geometric Hopf link loops.
        2. Evaluates statistical phase theta_{BF} and 2-cochain holonomy Hol.
        3. Evaluates orientation reversal parity Xi and ensemble weights.
        4. Indexes configurations into SQLite GIN mode posting tables.
        5. Computes cochain curvature Gamma_2, defect mass Phi_1, and BQNF terminal routing.
        """
        c1, c2_linked, c2_rev, c2_unlinked = model.generate_hopf_link_geometry()

        if test_unlinked:
            raw_lk = model.compute_gauss_linking_number(c1, c2_unlinked)
            lk = int(round(raw_lk))
            is_chiral = False
            is_z2_energy_split = False
        else:
            raw_lk = model.compute_gauss_linking_number(c1, c2_linked)
            lk = int(round(raw_lk))

        theta_bf, holonomy, gamma_2 = model.evaluate_loop_phase_and_holonomy(lk)
        is_contractible = (gamma_2 < 1e-6)

        w_pos, w_neg, delta_w, avg_sign, is_paired = model.evaluate_statistical_ensemble(
            is_chiral=is_chiral,
            is_z2_energy_split=is_z2_energy_split,
        )

        is_symmetric = (not is_chiral) and (not is_z2_energy_split)

        # Defect mass calculation
        if test_unlinked:
            phi_1 = 0.0
            terminal_route = TerminalRoute.EXACT_REPAIR.value
        elif is_symmetric:
            # Under symmetric pairing, imaginary part cancels identically
            phi_1 = 0.0
            terminal_route = TerminalRoute.EXACT_REPAIR.value
        elif is_chiral:
            phi_1 = delta_w + gamma_2
            terminal_route = TerminalRoute.OPEN_SIGN_OBSTRUCTION.value
        elif is_z2_energy_split:
            phi_1 = delta_w + gamma_2
            terminal_route = TerminalRoute.OPEN_SIGN_OBSTRUCTION.value
        else:
            phi_1 = gamma_2
            terminal_route = TerminalRoute.OPEN_SIGN_OBSTRUCTION.value if phi_1 > 0 else TerminalRoute.EXACT_REPAIR.value

        # GIN relational index population
        cfg_id_pos = 1001
        cfg_id_neg = 1002
        sign_pos = 1 if holonomy.real >= 0 else -1
        sign_neg = -1 if is_z2_energy_split else (1 if cmath.exp(-1j * theta_bf).real >= 0 else -1)

        self.conn.execute(
            """
            INSERT OR REPLACE INTO FermionConfigurations
            (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (cfg_id_pos, f"{model.model_id}_pos", 2, 4, w_pos, 1, 1),
        )
        self.conn.execute(
            """
            INSERT OR REPLACE INTO FermionConfigurations
            (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (cfg_id_neg, f"{model.model_id}_neg", 2, 4, w_neg, sign_neg, -1 if is_chiral else 1),
        )

        # Postings for loop modes
        for mode_idx in range(4):
            self.conn.execute(
                """
                INSERT OR REPLACE INTO GinModePostingList
                (mode_id, cfg_id, is_occupied)
                VALUES (?, ?, ?)
                """,
                (mode_idx, cfg_id_pos, 1 if mode_idx in (0, 1) else 0),
            )
            self.conn.execute(
                """
                INSERT OR REPLACE INTO GinModePostingList
                (mode_id, cfg_id, is_occupied)
                VALUES (?, ?, ?)
                """,
                (mode_idx, cfg_id_neg, 1 if mode_idx in (2, 3) else 0),
            )

        # Record Involution Pair
        self.conn.execute(
            """
            INSERT OR REPLACE INTO GinInvolutionPairs
            (pair_id, cfg_pos_id, cfg_neg_id, involution_type, is_exact_partner)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                501,
                cfg_id_pos,
                cfg_id_neg,
                "LoopOrientationParity_Xi",
                1 if is_symmetric and not test_unlinked else 0,
            ),
        )
        self.conn.commit()

        return BFLoopBraidingAuditReceipt(
            model_id=model.model_id,
            level_k=model.level_k,
            linking_number=lk,
            gauss_integral_raw=raw_lk,
            statistical_phase_radians=theta_bf,
            cochain_holonomy_real=holonomy.real,
            cochain_holonomy_imag=holonomy.imag,
            cochain_curvature_gamma_2=gamma_2,
            is_holonomy_contractible=is_contractible,
            is_orientation_symmetric=is_symmetric,
            weight_asymmetry_delta_w=delta_w,
            uncancelled_defect_mass_phi_1=phi_1,
            average_sign=avg_sign,
            is_exact_parity_paired=is_paired,
            terminal_route=terminal_route,
        )
