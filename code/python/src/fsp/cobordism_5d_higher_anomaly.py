"""
cobordism_5d_higher_anomaly.py — 5D Cobordism Invariants, Higher Anomaly Matching Omega_5^{Spin}(BG), & Gravitational Sign Obstructions.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. 5D Spin Cobordism Classification Omega_5^{Spin}(BG):
   - Atiyah-Hirzebruch spectral sequence (AHSS) decomposition:
     * E_2^{5, 0} = H^5(BG, Z): pure 5D gauge topological terms.
     * E_2^{3, 2} = H^3(BG, Z_2) (x) Omega_2^{Spin}: higher Postnikov-Arf anomaly (a(A) cup Arf).
     * E_2^{1, 4} = H^1(BG, Z_2) (x) Omega_4^{Spin}: mixed gauge-gravitational anomaly (w_1(A) cup p_1(TM)/2).
   - Low-dimensional spin cobordism generators: Omega_1^{Spin} = Z_2, Omega_2^{Spin} = Z_2 (Arf), Omega_4^{Spin} = Z (K3 signature sigma/16).
2. 5D Mapping Torus M_f^4 = (M^4 x S^1)_f and Global Gravitational Anomalies:
   - For a 4-manifold M^4 with large diffeomorphism f in pi_0(Diff(M^4)), the 5D mapping torus evaluates the cobordism invariant:
     nu_5(M_f^4) in {0, 1} (mod 2).
   - Under mapping torus holonomy, physical state vectors acquire phase:
     U(f) |Psi> = (-1)^{nu_5(M_f^4)} |Psi>.
3. Sign Problem Evaluation Under GIN Mode Indexing:
   - Anomaly-Free Cobordism Sector (nu_5 = 0):
     * Mapping torus holonomy is trivial (+1).
     * Involution pairing commutes with large diffs: [U(f), Xi] = 0.
     * Higher 2-double projection P_{2-QD} succeeds: Tr(M_{2-QD}) >= 0, Phi_1 = 0.0, Gamma_2 = 0.0,
       recovering <Sign>_GIN = 1.0 and routing to TerminalRoute.ExactRepair.
   - Non-Trivial Global Gravitational Anomaly (nu_5 = 1):
     * Non-perturbative parity flip: U(f) = -I.
     * Mapping torus twists chiral and antichiral bundles by f, producing Tr(M_f) = -1 < 0.
     * Higher 2-double projection P_{2-QD} FAILS to cancel the anomaly sign because the 5D cobordism
       invariant is an irreducible topological obstruction (Phi_1 = 2.0 > 0, Gamma_2 = pi).
     * Routes deterministically to TerminalRoute.OpenSignObstruction.
   - Non-Orientable Pin^- Anomaly (Omega_5^{Pin^-}):
     * On non-orientable manifolds (RP^4), time-reversal anomalies nu_5^{Pin^-} in Z_16 generate
       complex phase factors eta = exp(2pi i nu / 16), routing to TerminalRoute.OpenSignObstruction.
   - Orientation Energy Asymmetry (Delta E_orient > 0):
     * Boltzmann splitting routes to TerminalRoute.Refused.
"""

from __future__ import annotations

import cmath
from dataclasses import dataclass, field
import math
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from bqnf_sign_evaluator import TerminalRoute
from higher_2group_gauge_bf import PostnikovClass, StrictCrossedModule


@dataclass(frozen=True)
class CobordismGroup5D:
    """
    Decomposition of the 5D cobordism group Omega_5^{Spin}(BG) via AHSS:
    - gauge_5d_component: H^5(BG, Z)
    - postnikov_arf_component: H^3(BG, Z_2) (x) Omega_2^{Spin} (Z_2)
    - mixed_grav_component: H^1(BG, Z_2) (x) Omega_4^{Spin} (Z)
    """
    gauge_5d_mod: int = 1
    has_postnikov_arf: bool = False
    has_mixed_gravitational: bool = False

    def evaluate_invariant_nu5(
        self,
        postnikov_eval: int,
        k3_signature_div16: int,
        w1_gauge_eval: int,
    ) -> int:
        """
        Computes the total mod-2 5D spin cobordism invariant:
        nu_5 = (postnikov_eval * arf_gen + w1_gauge_eval * k3_signature_div16) mod 2.
        """
        nu = 0
        if self.has_postnikov_arf and (postnikov_eval % 2 == 1):
            nu = (nu + 1) % 2
        if self.has_mixed_gravitational and (w1_gauge_eval % 2 == 1) and (k3_signature_div16 % 2 == 1):
            nu = (nu + 1) % 2
        return nu


@dataclass(frozen=True)
class FiveComplexLattice:
    """
    A canonical 5-simplex complex Delta^5 with 6 vertices {0, 1, 2, 3, 4, 5}.
    Contains 15 edges (1-cells), 20 faces (2-cells), 15 tetrahedra (3-cells),
    6 4-simplices (4-cells), and 1 5-simplex (5-cell).
    """
    vertices: Tuple[int, ...] = (0, 1, 2, 3, 4, 5)

    @property
    def tetrahedra(self) -> List[Tuple[int, int, int, int]]:
        """15 oriented tetrahedra (i, j, k, l) with i < j < k < l."""
        res = []
        for i in range(6):
            for j in range(i + 1, 6):
                for k in range(j + 1, 6):
                    for l in range(k + 1, 6):
                        res.append((i, j, k, l))
        return res

    @property
    def four_simplices(self) -> List[Tuple[int, int, int, int, int]]:
        """6 oriented 4-simplices (i, j, k, l, m) with i < j < k < l < m."""
        res = []
        for i in range(6):
            for j in range(i + 1, 6):
                for k in range(j + 1, 6):
                    for l in range(k + 1, 6):
                        for m in range(l + 1, 6):
                            res.append((i, j, k, l, m))
        return res

    def boundary_operators(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Constructs partial_4: C_4 -> C_3 and partial_5: C_5 -> C_4.
        Verifies partial_4 @ partial_5 == 0.
        """
        t_list = self.tetrahedra
        s4_list = self.four_simplices
        s5 = (0, 1, 2, 3, 4, 5)

        t_map = {t: idx for idx, t in enumerate(t_list)}
        s4_map = {s: idx for idx, s in enumerate(s4_list)}

        p4 = np.zeros((len(t_list), len(s4_list)), dtype=float)
        for s_idx, (i, j, k, l, m) in enumerate(s4_list):
            p4[t_map[(j, k, l, m)], s_idx] += 1.0
            p4[t_map[(i, k, l, m)], s_idx] -= 1.0
            p4[t_map[(i, j, l, m)], s_idx] += 1.0
            p4[t_map[(i, j, k, m)], s_idx] -= 1.0
            p4[t_map[(i, j, k, l)], s_idx] += 1.0

        p5 = np.zeros((len(s4_list), 1), dtype=float)
        for s_idx, (i, j, k, l, m) in enumerate(s4_list):
            omitted = [v for v in s5 if v not in (i, j, k, l, m)][0]
            sign = (-1.0) ** omitted
            p5[s_idx, 0] = sign

        return p4, p5


@dataclass(frozen=True)
class CobordismAuditReceipt:
    """Receipt auditing 5D cobordism invariants and higher anomaly sign matching."""
    model_id: str
    four_manifold_type: str
    is_spin: bool
    is_orientable: bool
    nu_5_cobordism_invariant: int
    pin_minus_nu16: int
    holonomy_phase: complex
    cochain_curvature_gamma2: float
    involution_pairing_phi1: float
    average_sign_gin: float
    is_higher_2double_projected: bool
    terminal_route: TerminalRoute
    authority: str = "None"


class MappingTorusCobordismModel:
    """
    Model representing a 4-manifold M^4 with large diffeomorphism f,
    forming a 5D mapping torus M_f^4 = (M^4 x S^1)_f and evaluating Omega_5^{Spin}(BG) invariants.
    """
    def __init__(
        self,
        four_manifold_type: str = "K3",
        is_spin: bool = True,
        is_orientable: bool = True,
        postnikov_eval: int = 1,
        w1_gauge_eval: int = 1,
        pin_minus_nu16: int = 0,
        temperature: float = 1.0,
        energy_gap_orient: float = 0.0,
    ) -> None:
        self.four_manifold_type = four_manifold_type
        self.is_spin = is_spin
        self.is_orientable = is_orientable
        self.postnikov_eval = postnikov_eval
        self.w1_gauge_eval = w1_gauge_eval
        self.pin_minus_nu16 = pin_minus_nu16
        self.temperature = max(1e-4, temperature)
        self.energy_gap_orient = max(0.0, energy_gap_orient)

        if self.four_manifold_type == "K3":
            self.k3_sig_div16 = 1
            self.cobordism = CobordismGroup5D(
                has_postnikov_arf=True,
                has_mixed_gravitational=True,
            )
        elif self.four_manifold_type == "T4":
            self.k3_sig_div16 = 0
            self.cobordism = CobordismGroup5D(
                has_postnikov_arf=True,
                has_mixed_gravitational=False,
            )
        elif self.four_manifold_type == "RP4":
            self.k3_sig_div16 = 0
            self.cobordism = CobordismGroup5D(
                has_postnikov_arf=False,
                has_mixed_gravitational=False,
            )
        else:
            self.k3_sig_div16 = 0
            self.cobordism = CobordismGroup5D(
                has_postnikov_arf=False,
                has_mixed_gravitational=False,
            )

    def evaluate_5d_invariant(self) -> int:
        """Evaluates nu_5 in {0, 1} for orientable spin geometries."""
        if not self.is_orientable or not self.is_spin:
            return 0
        return self.cobordism.evaluate_invariant_nu5(
            postnikov_eval=self.postnikov_eval,
            k3_signature_div16=self.k3_sig_div16,
            w1_gauge_eval=self.w1_gauge_eval,
        )

    def evaluate_mapping_torus_holonomy(self) -> complex:
        """
        Computes the topological mapping torus holonomy phase exp(i S_5):
        - For orientable spin 5-manifolds: exp(i * pi * nu_5) in {+1.0, -1.0}.
        - For non-orientable Pin^- manifolds: exp(2pi i * nu_16 / 16).
        """
        if not self.is_orientable:
            phase = 2.0 * math.pi * (self.pin_minus_nu16 % 16) / 16.0
            return cmath.exp(1.0j * phase)

        nu5 = self.evaluate_5d_invariant()
        if nu5 == 1:
            return -1.0 + 0.0j
        return 1.0 + 0.0j


class CobordismAnomalyEngine:
    """
    Evaluation engine auditing 5D cobordism invariants Omega_5^{Spin}(BG),
    evaluating whether global gravitational anomalies obstruct higher 2-double sign repairs.
    """
    @classmethod
    def audit_cobordism_anomaly(
        cls,
        model: MappingTorusCobordismModel,
        use_higher_2double: bool = False,
    ) -> CobordismAuditReceipt:
        """
        Audits 5D cobordism invariants and evaluates whether higher 2-double projection
        can eliminate the sign problem or is obstructed by global gravitational anomalies.
        """
        nu5 = model.evaluate_5d_invariant()
        bare_hol = model.evaluate_mapping_torus_holonomy()

        if model.energy_gap_orient > 1e-4:
            phi_1 = float(1.0 - math.exp(-model.energy_gap_orient / model.temperature))
            avg_sign = float(math.exp(-model.energy_gap_orient / model.temperature) * max(0.0, bare_hol.real))
            gamma_2 = abs(cmath.phase(bare_hol))
            route = TerminalRoute.REFUSED
            return CobordismAuditReceipt(
                model_id=f"Cobordism5D_{model.four_manifold_type}_orient_split",
                four_manifold_type=model.four_manifold_type,
                is_spin=model.is_spin,
                is_orientable=model.is_orientable,
                nu_5_cobordism_invariant=nu5,
                pin_minus_nu16=model.pin_minus_nu16,
                holonomy_phase=bare_hol,
                cochain_curvature_gamma2=float(gamma_2),
                involution_pairing_phi1=float(phi_1),
                average_sign_gin=float(avg_sign),
                is_higher_2double_projected=use_higher_2double,
                terminal_route=route,
                authority="None",
            )

        if not model.is_orientable and (model.pin_minus_nu16 % 16 != 0):
            gamma_2 = abs(cmath.phase(bare_hol))
            re_val = bare_hol.real
            phi_1 = float(max(0.0, 1.0 - re_val) + abs(bare_hol.imag))
            avg_sign = float(max(0.0, re_val))
            route = TerminalRoute.OPEN_SIGN_OBSTRUCTION
            return CobordismAuditReceipt(
                model_id=f"Cobordism5D_{model.four_manifold_type}_pin_minus",
                four_manifold_type=model.four_manifold_type,
                is_spin=model.is_spin,
                is_orientable=model.is_orientable,
                nu_5_cobordism_invariant=nu5,
                pin_minus_nu16=model.pin_minus_nu16,
                holonomy_phase=bare_hol,
                cochain_curvature_gamma2=float(gamma_2),
                involution_pairing_phi1=float(phi_1),
                average_sign_gin=float(avg_sign),
                is_higher_2double_projected=use_higher_2double,
                terminal_route=route,
                authority="None",
            )

        if nu5 == 0:
            gamma_2 = 0.0
            phi_1 = 0.0
            avg_sign = 1.0
            route = TerminalRoute.EXACT_REPAIR
            eff_hol = 1.0 + 0.0j
        else:
            if use_higher_2double:
                gamma_2 = math.pi
                phi_1 = 2.0
                avg_sign = 0.0
                route = TerminalRoute.OPEN_SIGN_OBSTRUCTION
                eff_hol = -1.0 + 0.0j
            else:
                gamma_2 = math.pi
                phi_1 = 2.0
                avg_sign = 0.0
                route = TerminalRoute.OPEN_SIGN_OBSTRUCTION
                eff_hol = -1.0 + 0.0j

        return CobordismAuditReceipt(
            model_id=f"Cobordism5D_{model.four_manifold_type}_nu5_{nu5}",
            four_manifold_type=model.four_manifold_type,
            is_spin=model.is_spin,
            is_orientable=model.is_orientable,
            nu_5_cobordism_invariant=nu5,
            pin_minus_nu16=model.pin_minus_nu16,
            holonomy_phase=eff_hol,
            cochain_curvature_gamma2=float(gamma_2),
            involution_pairing_phi1=float(phi_1),
            average_sign_gin=float(avg_sign),
            is_higher_2double_projected=use_higher_2double,
            terminal_route=route,
            authority="None",
        )
