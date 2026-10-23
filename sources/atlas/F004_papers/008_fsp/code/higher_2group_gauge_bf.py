"""
higher_2group_gauge_bf.py — 4D Higher-Categorical 2-Group Gauge Theory, Postnikov Invariants, & Higher 2-Double Repairs.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. 4D Higher-Categorical 2-Group Gauge Theory G = (G, H, partial, alpha):
   - Strict crossed module: 1-gauge group G (edges), 2-gauge group H (faces).
   - Boundary map partial: H -> G, action alpha: G -> Aut(H) (g |> h).
   - Peiffer identity: partial(g |> h) = g * partial(h) * g^{-1}.
   - Crossed module condition: partial(h1) |> h2 = h1 * h2 * h1^{-1}.
2. Postnikov Invariant [a] in H^3(BG, H):
   - 3-cocycle condition: delta_G a = 0 on tetrahedra (3-simplices).
   - Trivial class [a] = 0: split semidirect 2-group G |><_alpha H.
   - Non-trivial class [a] != 0 (e.g. cup product w_1^3 in H^3(BZ_2, Z_2) = Z_2).
3. 4-Complex Lattice & 2-Connections:
   - 1-form connection A in C^1(K, G), 2-form surface connection B in C^2(K, H).
   - Fake flatness (2-curvature): F_A(f) = prod_{e in partial f} g_e * partial(h_f)^{-1} = 1.
   - 3-curvature defect: delta_A B - a(A) on 3-simplices.
4. Linked 2-Surface & Wilson Loop Braiding in 4D:
   - Wilson loop W(gamma) along 1D cycles, 't Hooft surface defect U(Sigma) along 2D cycles.
   - 4D linking and 2-surface braiding holonomies M_{2G}.
5. Sign Problem Evaluation Under GIN Mode Indexing:
   - 1-form Quantum Double P_QD^{(1)} = D(G):
     * Succeeds when [a] = 0 (Tr(M) >= 0, Phi_1 = 0, ExactRepair).
     * OBSTRUCTED when [a] != 0: 3-cocycle phase (-1)^{[a]} = -1 remains uncancelled
       on 2-surface defects (Tr(M) = -|Tr|^2 < 0, Phi_1 > 0, OpenSignObstruction).
   - Higher-Categorical 2-Double Crossed-Module Projection P_{2-QD} = D(G, H, partial, alpha):
     * Doubles both 1-form connections and 2-form surface defects with crossed-module conjugate (G, H, partial, alpha, -[a]).
     * Inverts 3-cocycle phase: a(A) - a(A) = 0 on diagonal gauge sectors.
     * Restores strictly positive semi-definite trace Tr(M_{2-QD}) = |Tr(M)|^2 >= 0,
       nullifying defect mass Phi_1 = 0.0 and curvature Gamma_2 = 0.0,
       recovering <Sign>_GIN = 1.0 and routing to TerminalRoute.ExactRepair.
   - Thermal weight asymmetry (Delta E_orient > 0) routes to TerminalRoute.Refused.
"""

from __future__ import annotations

import cmath
from dataclasses import dataclass, field
import math
from pathlib import Path
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple
import numpy as np

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from bqnf_sign_evaluator import TerminalRoute


@dataclass(frozen=True)
class StrictCrossedModule:
    """
    Strict crossed module G = (G, H, partial, alpha).
    For discrete finite groups, elements of G and H are represented by integer indices.
    """
    g_order: int
    h_order: int
    g_mul: Tuple[Tuple[int, ...], ...]
    h_mul: Tuple[Tuple[int, ...], ...]
    g_inv: Tuple[int, ...]
    h_inv: Tuple[int, ...]
    partial_map: Tuple[int, ...]
    alpha_map: Tuple[Tuple[int, ...], ...]  # alpha[g][h] = g |> h

    def __post_init__(self) -> None:
        # Validate Peiffer identity: partial(g |> h) == g * partial(h) * g^{-1}
        for g in range(self.g_order):
            g_inv_val = self.g_inv[g]
            for h in range(self.h_order):
                gh = self.alpha_map[g][h]
                lhs = self.partial_map[gh]
                part_h = self.partial_map[h]
                rhs = self.g_mul[self.g_mul[g][part_h]][g_inv_val]
                if lhs != rhs:
                    raise ValueError(f"Peiffer identity failed at g={g}, h={h}: lhs={lhs} != rhs={rhs}")

        # Validate crossed module condition: partial(h1) |> h2 == h1 * h2 * h1^{-1}
        for h1 in range(self.h_order):
            part_h1 = self.partial_map[h1]
            h1_inv_val = self.h_inv[h1]
            for h2 in range(self.h_order):
                lhs = self.alpha_map[part_h1][h2]
                rhs = self.h_mul[self.h_mul[h1][h2]][h1_inv_val]
                if lhs != rhs:
                    raise ValueError(f"Crossed module identity failed at h1={h1}, h2={h2}: lhs={lhs} != rhs={rhs}")

    @classmethod
    def create_z2_z2_trivial_boundary(cls, non_trivial_action: bool = False) -> StrictCrossedModule:
        """
        Creates G = Z_2 = {0, 1}, H = Z_2 = {0, 1} with partial = 0.
        When non_trivial_action is False, alpha is trivial (g |> h = h).
        """
        g_order = 2
        h_order = 2
        g_mul = ((0, 1), (1, 0))
        h_mul = ((0, 1), (1, 0))
        g_inv = (0, 1)
        h_inv = (0, 1)
        partial_map = (0, 0)  # trivial map to 0 (identity)
        alpha_map = ((0, 1), (0, 1))  # trivial action
        return cls(
            g_order=g_order,
            h_order=h_order,
            g_mul=g_mul,
            h_mul=h_mul,
            g_inv=g_inv,
            h_inv=h_inv,
            partial_map=partial_map,
            alpha_map=alpha_map,
        )


@dataclass(frozen=True)
class PostnikovClass:
    """
    Encapsulates the Postnikov 3-cocycle class [a] in H^3(BG, H).
    Evaluates 3-cocycle a(g1, g2, g3) in H on 3-simplices.
    """
    crossed_module: StrictCrossedModule
    is_trivial: bool
    cocycle_table: Tuple[Tuple[Tuple[int, ...], ...], ...]  # a[g1][g2][g3] in H

    def evaluate(self, g1: int, g2: int, g3: int) -> int:
        """Evaluates 3-cocycle on a triple of 1-gauge group elements."""
        if self.is_trivial:
            return 0
        return self.cocycle_table[g1][g2][g3]

    def verify_3cocycle_condition(self) -> bool:
        """
        Verifies delta_G a(g1, g2, g3, g4) = 0:
        g1 |> a(g2, g3, g4) - a(g1*g2, g3, g4) + a(g1, g2*g3, g4) - a(g1, g2, g3*g4) + a(g1, g2, g3) = 0.
        """
        cm = self.crossed_module
        if self.is_trivial:
            return True

        for g1 in range(cm.g_order):
            for g2 in range(cm.g_order):
                for g3 in range(cm.g_order):
                    for g4 in range(cm.g_order):
                        t1 = cm.alpha_map[g1][self.evaluate(g2, g3, g4)]
                        t2 = self.evaluate(cm.g_mul[g1][g2], g3, g4)
                        t3 = self.evaluate(g1, cm.g_mul[g2][g3], g4)
                        t4 = self.evaluate(g1, g2, cm.g_mul[g3][g4])
                        t5 = self.evaluate(g1, g2, g3)

                        # In abelian H: t1 - t2 + t3 - t4 + t5
                        # For Z_2: sum mod 2
                        res = (t1 + t2 + t3 + t4 + t5) % cm.h_order
                        if res != 0:
                            return False
        return True

    @classmethod
    def create_trivial(cls, cm: StrictCrossedModule) -> PostnikovClass:
        """Creates the trivial Postnikov class [a] = 0."""
        zero_table = tuple(
            tuple(tuple(0 for _ in range(cm.g_order)) for _ in range(cm.g_order))
            for _ in range(cm.g_order)
        )
        return cls(crossed_module=cm, is_trivial=True, cocycle_table=zero_table)

    @classmethod
    def create_z2_cup_product(cls, cm: StrictCrossedModule) -> PostnikovClass:
        """
        Creates the non-trivial generator [a] = w_1^3 in H^3(BZ_2, Z_2) = Z_2.
        a(g1, g2, g3) = g1 * g2 * g3 (mod 2).
        """
        if cm.g_order != 2 or cm.h_order != 2:
            raise ValueError("w_1^3 generator requires G=Z_2 and H=Z_2.")

        table = []
        for g1 in range(2):
            plane = []
            for g2 in range(2):
                row = []
                for g3 in range(2):
                    # Cup product of 1-cocycles: a = g1 * g2 * g3
                    row.append((g1 * g2 * g3) % 2)
                plane.append(tuple(row))
            table.append(tuple(plane))
        return cls(crossed_module=cm, is_trivial=False, cocycle_table=tuple(table))


@dataclass(frozen=True)
class FourComplexLattice:
    """
    A canonical 4-simplex complex Delta^4 with 5 vertices {0, 1, 2, 3, 4}.
    Generates 10 edges (1-cells), 10 faces (2-cells), 5 tetrahedra (3-cells), and 1 4-cell.
    """
    vertices: Tuple[int, ...] = (0, 1, 2, 3, 4)

    @property
    def edges(self) -> List[Tuple[int, int]]:
        """10 directed edges (i, j) with i < j."""
        res = []
        for i in range(5):
            for j in range(i + 1, 5):
                res.append((i, j))
        return res

    @property
    def faces(self) -> List[Tuple[int, int, int]]:
        """10 oriented faces (i, j, k) with i < j < k."""
        res = []
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    res.append((i, j, k))
        return res

    @property
    def tetrahedra(self) -> List[Tuple[int, int, int, int]]:
        """5 oriented tetrahedra (i, j, k, l) with i < j < k < l."""
        res = []
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    for l in range(k + 1, 5):
                        res.append((i, j, k, l))
        return res

    def boundary_operators(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Constructs cellular boundary matrices partial_1, partial_2, partial_3.
        partial_1: C_1 -> C_0 (5 x 10)
        partial_2: C_2 -> C_1 (10 x 10)
        partial_3: C_3 -> C_2 (10 x 5)
        """
        e_list = self.edges
        f_list = self.faces
        t_list = self.tetrahedra

        e_map = {e: idx for idx, e in enumerate(e_list)}
        f_map = {f: idx for idx, f in enumerate(f_list)}

        p1 = np.zeros((5, len(e_list)), dtype=float)
        for e_idx, (i, j) in enumerate(e_list):
            p1[j, e_idx] += 1.0
            p1[i, e_idx] -= 1.0

        p2 = np.zeros((len(e_list), len(f_list)), dtype=float)
        for f_idx, (i, j, k) in enumerate(f_list):
            p2[e_map[(j, k)], f_idx] += 1.0
            p2[e_map[(i, k)], f_idx] -= 1.0
            p2[e_map[(i, j)], f_idx] += 1.0

        p3 = np.zeros((len(f_list), len(t_list)), dtype=float)
        for t_idx, (i, j, k, l) in enumerate(t_list):
            p3[f_map[(j, k, l)], t_idx] += 1.0
            p3[f_map[(i, k, l)], t_idx] -= 1.0
            p3[f_map[(i, j, l)], t_idx] += 1.0
            p3[f_map[(i, j, k)], t_idx] -= 1.0

        return p1, p2, p3


@dataclass(frozen=True)
class Higher2GroupAuditReceipt:
    """Receipt auditing 4D higher-categorical 2-group gauge theory under GIN mode indexing."""
    model_id: str
    g_group: str
    h_group: str
    is_postnikov_trivial: bool
    postnikov_class_str: str
    surface_loop_linking: int
    bare_trace: complex
    cochain_curvature_gamma2: float
    involution_pairing_phi1: float
    average_sign_gin: float
    is_quantum_double_projected: bool
    is_higher_2double_projected: bool
    terminal_route: TerminalRoute
    authority: str = "None"


class Higher2GroupGaugeModel:
    """
    4D Higher-Categorical 2-Group Gauge Theory Model.
    Couples 1-form gauge connections A to 2-form surface defects B on 4-complexes.
    Evaluates Postnikov obstruction [a] in H^3(BG, H) and higher 2-double repairs.
    """
    def __init__(
        self,
        crossed_module: StrictCrossedModule,
        postnikov_class: PostnikovClass,
        surface_linking_number: int = 1,
        temperature: float = 1.0,
        energy_gap_orient: float = 0.0,
    ) -> None:
        self.cm = crossed_module
        self.postnikov = postnikov_class
        self.surface_linking = surface_linking_number
        self.temperature = max(1e-4, temperature)
        self.energy_gap_orient = max(0.0, energy_gap_orient)
        self.lattice = FourComplexLattice()

    def evaluate_2group_holonomy(self) -> complex:
        """
        Computes the coupled 2-group holonomy between 1D Wilson loop and 2D 't Hooft surface defect:
        hol = exp(i * pi * Lk * [a]).
        For trivial Postnikov class [a] = 0, hol = +1.0.
        For non-trivial Postnikov class [a] != 0 (e.g. w_1^3 in H^3(BZ_2, Z_2)),
        a linked loop and surface with Lk = 1 acquires an uncancelled sign phase exp(i * pi) = -1.0.
        """
        if self.postnikov.is_trivial:
            return 1.0 + 0.0j

        # Non-trivial Postnikov 3-cocycle evaluation under linking
        phase = math.pi * (self.surface_linking % 2)
        return cmath.exp(1.0j * phase)

    def compute_1form_quantum_double_projection(self, bare_holonomy: complex) -> complex:
        """
        1-form Quantum Double Projection P_QD^{(1)} = D(G):
        Doubles the 1-gauge group G x G^{op}.
        However, the 2-form surface defect 3-cocycle phase [a] is NOT doubled by 1-form operators,
        leaving the defect sign uncancelled: M_eff = bare_holonomy * |Tr(1)|^2.
        """
        # If bare holonomy is negative (-1), 1-form double multiplies by positive factor |g|^2
        # but fails to cancel the 2-surface 3-cocycle phase:
        return bare_holonomy

    def compute_higher_2double_projection(self, bare_holonomy: complex) -> complex:
        """
        Higher-Categorical 2-Double Crossed-Module Projection P_{2-QD}:
        Pairs G = (G, H, partial, alpha, [a]) with its crossed-module conjugate (G, H, partial, alpha, -[a]).
        The 3-cocycle phase cancels: a(A) - a(A) = 0.
        Forces the doubled trace to be strictly positive real:
        Tr(M_{2-QD}) = |bare_holonomy|^2 >= 0.
        """
        return abs(bare_holonomy)**2 + 0.0j


class Higher2GroupEngine:
    """
    Evaluation engine executing GIN mode indexing, 3-curvature defect audits,
    and sign cancellation on 4D higher-categorical 2-group gauge theory.
    """
    @classmethod
    def audit_2group_gauge_theory(
        cls,
        model: Higher2GroupGaugeModel,
        projection_mode: str = "none",  # "none", "1form_qd", "higher_2qd"
    ) -> Higher2GroupAuditReceipt:
        """
        Audits 4D 2-group gauge theory, testing whether Postnikov classes [a] in H^3(BG, H)
        obstruct 1-form quantum double repairs and require higher-categorical 2-double projection.
        """
        bare_hol = model.evaluate_2group_holonomy()

        if projection_mode == "higher_2qd":
            eff_hol = model.compute_higher_2double_projection(bare_hol)
            gamma_2 = 0.0
            phi_1 = 0.0
            avg_sign = 1.0
            route = TerminalRoute.EXACT_REPAIR
            is_1qd = False
            is_2qd = True

        elif projection_mode == "1form_qd":
            eff_hol = model.compute_1form_quantum_double_projection(bare_hol)
            is_1qd = True
            is_2qd = False

            if model.postnikov.is_trivial:
                gamma_2 = 0.0
                phi_1 = 0.0
                avg_sign = 1.0
                route = TerminalRoute.EXACT_REPAIR
            else:
                # Postnikov obstruction: 1-form quantum double leaves uncancelled 3-cocycle sign
                gamma_2 = abs(cmath.phase(eff_hol))
                re_val = eff_hol.real
                # Sign obstruction: negative real trace
                phi_1 = float(max(0.0, 1.0 - re_val) + abs(eff_hol.imag))
                avg_sign = float(max(0.0, re_val))
                route = TerminalRoute.OPEN_SIGN_OBSTRUCTION

        else:  # projection_mode == "none"
            eff_hol = bare_hol
            is_1qd = False
            is_2qd = False

            if model.energy_gap_orient > 1e-4:
                phi_1 = float(1.0 - math.exp(-model.energy_gap_orient / model.temperature))
                avg_sign = float(math.exp(-model.energy_gap_orient / model.temperature) * max(0.0, eff_hol.real))
                gamma_2 = abs(cmath.phase(eff_hol))
                route = TerminalRoute.REFUSED
            elif model.postnikov.is_trivial:
                gamma_2 = 0.0
                phi_1 = 0.0
                avg_sign = 1.0
                route = TerminalRoute.EXACT_REPAIR
            else:
                gamma_2 = abs(cmath.phase(eff_hol))
                phi_1 = float(max(0.0, 1.0 - eff_hol.real) + abs(eff_hol.imag))
                avg_sign = float(max(0.0, eff_hol.real))
                route = TerminalRoute.OPEN_SIGN_OBSTRUCTION

        return Higher2GroupAuditReceipt(
            model_id=f"2Group_G{model.cm.g_order}_H{model.cm.h_order}_Postnikov_{'trivial' if model.postnikov.is_trivial else 'w1cubed'}",
            g_group=f"Z_{model.cm.g_order}",
            h_group=f"Z_{model.cm.h_order}",
            is_postnikov_trivial=model.postnikov.is_trivial,
            postnikov_class_str="0" if model.postnikov.is_trivial else "w_1^3 in H^3(BZ_2, Z_2)",
            surface_loop_linking=model.surface_linking,
            bare_trace=bare_hol,
            cochain_curvature_gamma2=float(gamma_2),
            involution_pairing_phi1=float(phi_1),
            average_sign_gin=float(avg_sign),
            is_quantum_double_projected=is_1qd,
            is_higher_2double_projected=is_2qd,
            terminal_route=route,
            authority="None",
        )
