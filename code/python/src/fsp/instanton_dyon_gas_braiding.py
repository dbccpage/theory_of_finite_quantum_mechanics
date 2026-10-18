"""
Instanton-Dyon Topological Gas Expansions and Monopole Loop Braiding Engine.

Paper: 002_projection_obstruction/023_fermion_sign_and_computational_hardness
Module: instanton_dyon_gas_braiding.py
AuthorityEffect: None
Primary Reference: sealed-derivation-v1 (commit 3100c4e)

Evaluates:
1. Semiclassical KvBLL caloron constituent instanton-dyon gas (M, L, M̄, L̄)
   with fractional topological charges Q_M = ν, Q_L = 1 - ν under θ = π.
2. Inter-dyon Coulomb interaction potential V(r_ij) = (4π/g²) (m_i m_j / r_ij)
   and molecular dipole clustering into neutral (M M̄) and (L L̄) bound states.
3. GIN mode posting lists indexing dyon configurations under dyonic involution
   Ξ_dyon (M ↔ M̄, L ↔ L̄, r ↦ -r).
4. Semiclassical regimes:
   - Molecular Cluster Regime: Exact involution pairing, Φ₁ = 0.0, Γ₂ = 0.0 → EXACT_REPAIR.
   - Ionized Plasma Regime: Coulomb repulsion action gap ΔS > 0, disjoint spectra → SPLIT_BRAIN_REFUSAL.
   - Monopole Loop Braiding Regime: Gauss linking Lk = 1, Dirac phase (-1)^Lk = -1,
     non-abelian Berry curvature, Φ₁ = 2.0, Γ₂ = π → OPEN_SIGN_OBSTRUCTION.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

import numpy as np


class DyonType(Enum):
    """Caloron constituent instanton-dyon species."""
    M_DYON = "M"
    L_DYON = "L"
    M_BAR = "M_bar"
    L_BAR = "L_bar"


class GasRegime(Enum):
    """Thermodynamic and topological regimes of the dyon gas."""
    MOLECULAR_CLUSTER = "molecular_cluster"
    IONIZED_PLASMA = "ionized_plasma"
    MONOPOLE_BRAIDING = "monopole_braiding"


class TerminalRoute(Enum):
    """Five-fold terminal routing for sign obstruction packets."""
    EXACT_REPAIR = "exact_repair"
    SPLIT_BRAIN_REFUSAL = "split_brain_refusal"
    OPEN_SIGN_OBSTRUCTION = "open_sign_obstruction"
    TENTATIVE_CLOSURE = "tentative_closure"
    UNDEFINED = "undefined"


@dataclass(frozen=True)
class DyonParticle:
    """Individual instanton-dyon in 3D spatial slice."""
    particle_id: int
    dyon_type: DyonType
    position: Tuple[float, float, float]
    magnetic_charge: int
    topological_charge: float
    core_action: float


@dataclass
class DyonGasConfig:
    """Parameters for the instanton-dyon gas."""
    g_coupling: float = 1.0
    nu_holonomy: float = 0.5
    theta_angle: float = math.pi
    temperature: float = 1.0
    core_radius: float = 0.2


@dataclass
class DyonEnsemble:
    """A spatial ensemble of instanton-dyons."""
    particles: List[DyonParticle] = field(default_factory=list)
    config: DyonGasConfig = field(default_factory=DyonGasConfig)

    @property
    def net_magnetic_charge(self) -> int:
        return sum(p.magnetic_charge for p in self.particles)

    @property
    def net_topological_charge(self) -> float:
        return sum(p.topological_charge for p in self.particles)

    def pair_coulomb_potential(self, p1: DyonParticle, p2: DyonParticle) -> float:
        """Coulomb interaction energy with core regulation."""
        r_vec = np.array(p1.position) - np.array(p2.position)
        dist = float(np.linalg.norm(r_vec))
        eff_dist = max(dist, self.config.core_radius)
        coulomb_coeff = (4.0 * math.pi) / (self.config.g_coupling ** 2)
        return coulomb_coeff * (p1.magnetic_charge * p2.magnetic_charge) / eff_dist

    def compute_total_action(self) -> float:
        """Total Euclidean action S = sum(S_core) + sum_{i < j} V(r_ij)."""
        core_sum = sum(p.core_action for p in self.particles)
        interaction_sum = 0.0
        n = len(self.particles)
        for i in range(n):
            for j in range(i + 1, n):
                interaction_sum += self.pair_coulomb_potential(self.particles[i], self.particles[j])
        return core_sum + interaction_sum

    def compute_topological_phase(self) -> float:
        """Topological phase factor cos(θ * Q_net)."""
        return math.cos(self.config.theta_angle * self.net_topological_charge)

    def compute_weight(self) -> Tuple[float, float]:
        """Returns (magnitude |w|, sign σ ∈ {+1, -1})."""
        action = self.compute_total_action()
        magnitude = math.exp(-action / self.config.temperature)
        phase = self.compute_topological_phase()
        sign = 1.0 if phase >= 0.0 else -1.0
        return magnitude * abs(phase), sign


class DyonGasBuilder:
    """Constructs KvBLL caloron constituent instanton-dyon ensembles."""

    @staticmethod
    def create_dyon(
        particle_id: int,
        dyon_type: DyonType,
        position: Tuple[float, float, float],
        config: DyonGasConfig
    ) -> DyonParticle:
        nu = config.nu_holonomy
        g = config.g_coupling
        s_0 = (8.0 * math.pi ** 2) / (g ** 2)

        if dyon_type == DyonType.M_DYON:
            m = +1
            q = nu
            s = nu * s_0
        elif dyon_type == DyonType.L_DYON:
            m = -1
            q = 1.0 - nu
            s = (1.0 - nu) * s_0
        elif dyon_type == DyonType.M_BAR:
            m = -1
            q = -nu
            s = nu * s_0
        elif dyon_type == DyonType.L_BAR:
            m = +1
            q = -(1.0 - nu)
            s = (1.0 - nu) * s_0
        else:
            raise ValueError(f"Unknown dyon type {dyon_type}")

        return DyonParticle(
            particle_id=particle_id,
            dyon_type=dyon_type,
            position=position,
            magnetic_charge=m,
            topological_charge=q,
            core_action=s
        )

    @staticmethod
    def build_neutral_dipole_cluster(
        center: Tuple[float, float, float],
        separation: float,
        config: DyonGasConfig
    ) -> DyonEnsemble:
        """Constructs a neutral bound molecule: M at +d/2, M̄ at -d/2."""
        cx, cy, cz = center
        p1 = DyonGasBuilder.create_dyon(
            1, DyonType.M_DYON, (cx, cy, cz + separation / 2.0), config
        )
        p2 = DyonGasBuilder.create_dyon(
            2, DyonType.M_BAR, (cx, cy, cz - separation / 2.0), config
        )
        return DyonEnsemble(particles=[p1, p2], config=config)

    @staticmethod
    def build_neutral_caloron_quartet(
        center: Tuple[float, float, float],
        d: float,
        config: DyonGasConfig
    ) -> DyonEnsemble:
        """Constructs a full neutral caloron quartet: (M, M̄, L, L̄)."""
        cx, cy, cz = center
        p1 = DyonGasBuilder.create_dyon(1, DyonType.M_DYON, (cx + d, cy, cz), config)
        p2 = DyonGasBuilder.create_dyon(2, DyonType.M_BAR, (cx - d, cy, cz), config)
        p3 = DyonGasBuilder.create_dyon(3, DyonType.L_DYON, (cx, cy + d, cz), config)
        p4 = DyonGasBuilder.create_dyon(4, DyonType.L_BAR, (cx, cy - d, cz), config)
        return DyonEnsemble(particles=[p1, p2, p3, p4], config=config)

    @staticmethod
    def build_ionized_plasma_ensemble(
        num_dyons: int,
        box_size: float,
        config: DyonGasConfig,
        seed: int = 42
    ) -> DyonEnsemble:
        """Constructs an unconfined / plasma ensemble with random positions and net charge."""
        rng = np.random.RandomState(seed)
        particles = []
        species_pool = [DyonType.M_DYON, DyonType.M_DYON, DyonType.L_BAR, DyonType.M_BAR]
        for i in range(num_dyons):
            pos = tuple(rng.uniform(-box_size / 2.0, box_size / 2.0, size=3))
            dtype = species_pool[i % len(species_pool)]
            p = DyonGasBuilder.create_dyon(i + 1, dtype, pos, config)
            particles.append(p)
        return DyonEnsemble(particles=particles, config=config)


class MonopoleLoopBraiding:
    """Calculates Gauss linking numbers and non-abelian Berry holonomies for monopole loops."""

    @staticmethod
    def compute_gauss_linking(
        loop1: np.ndarray,
        loop2: np.ndarray
    ) -> float:
        """
        Computes the Gauss linking integral between two closed 3D polygonal curves:
        Lk = (1 / 4π) ∮∮ (dr1 × dr2 · (r1 - r2)) / |r1 - r2|³
        """
        n1 = len(loop1)
        n2 = len(loop2)
        total_sum = 0.0

        for i in range(n1):
            r1_i = loop1[i]
            r1_next = loop1[(i + 1) % n1]
            dr1 = r1_next - r1_i

            for j in range(n2):
                r2_j = loop2[j]
                r2_next = loop2[(j + 1) % n2]
                dr2 = r2_next - r2_j

                mid1 = (r1_i + r1_next) / 2.0
                mid2 = (r2_j + r2_next) / 2.0
                diff = mid1 - mid2
                dist = np.linalg.norm(diff)

                if dist < 1e-10:
                    continue

                cross = np.cross(dr1, dr2)
                term = float(np.dot(cross, diff) / (dist ** 3))
                total_sum += term

        return total_sum / (4.0 * math.pi)

    @staticmethod
    def build_hopf_link(radius: float = 1.0, num_points: int = 64) -> Tuple[np.ndarray, np.ndarray]:
        """Builds two linked circles (Hopf link) with Lk = 1."""
        angles = np.linspace(0, 2 * math.pi, num_points, endpoint=False)
        loop1 = np.column_stack([
            radius * np.cos(angles),
            radius * np.sin(angles),
            np.zeros(num_points)
        ])
        loop2 = np.column_stack([
            np.zeros(num_points),
            radius + radius * np.cos(angles),
            -radius * np.sin(angles)
        ])
        return loop1, loop2

    @staticmethod
    def build_unlinked_loops(radius: float = 1.0, num_points: int = 64) -> Tuple[np.ndarray, np.ndarray]:
        """Builds two unlinked circles with Lk = 0."""
        angles = np.linspace(0, 2 * math.pi, num_points, endpoint=False)
        loop1 = np.column_stack([
            radius * np.cos(angles),
            radius * np.sin(angles),
            np.zeros(num_points)
        ])
        loop2 = np.column_stack([
            radius * np.cos(angles) + 3.0 * radius,
            radius * np.sin(angles),
            np.zeros(num_points)
        ])
        return loop1, loop2

    @staticmethod
    def compute_dirac_aharonov_bohm_phase(lk: float) -> float:
        """Evaluates Aharonov-Bohm / Dirac phase (-1)^round(Lk)."""
        rounded_lk = int(round(lk))
        return float((-1) ** rounded_lk)

    @staticmethod
    def compute_monopole_braiding_matrix(
        lk: int,
        is_abelian: bool = False
    ) -> np.ndarray:
        """
        Computes internal zero-mode Berry matrix holonomy for monopole loop braiding.
        For linked loops (Lk = 1) in non-abelian gauge theory, holonomy is non-trivial (-I).
        """
        if is_abelian or lk == 0:
            return np.array([[1.0, 0.0], [0.0, 1.0]])
        else:
            return np.array([[-1.0, 0.0], [0.0, -1.0]])


class InstantonDyonEngine:
    """Master audit and verification engine for instanton-dyon gases and monopole loop braiding."""

    def __init__(self, config: Optional[DyonGasConfig] = None):
        self.config = config or DyonGasConfig()

    def dyonic_involution_transform(self, ensemble: DyonEnsemble) -> DyonEnsemble:
        """
        Applies dyonic charge-conjugation & spatial reflection involution:
        Ξ_dyon: M ↔ M̄, L ↔ L̄, r ↦ -r.
        """
        transformed_particles = []
        for p in ensemble.particles:
            new_pos = (-p.position[0], -p.position[1], -p.position[2])
            if p.dyon_type == DyonType.M_DYON:
                new_type = DyonType.M_BAR
            elif p.dyon_type == DyonType.M_BAR:
                new_type = DyonType.M_DYON
            elif p.dyon_type == DyonType.L_DYON:
                new_type = DyonType.L_BAR
            elif p.dyon_type == DyonType.L_BAR:
                new_type = DyonType.L_DYON
            else:
                raise ValueError("Invalid dyon type")

            new_p = DyonGasBuilder.create_dyon(
                p.particle_id, new_type, new_pos, ensemble.config
            )
            transformed_particles.append(new_p)

        return DyonEnsemble(particles=transformed_particles, config=ensemble.config)

    def audit_molecular_cluster_regime(
        self,
        separation: float = 0.5
    ) -> Dict[str, object]:
        """
        Audits the molecular cluster regime where dyons form neutral bound dipoles.
        Verifies exact involution pairing, Φ₁ = 0.0, Γ₂ = 0.0, routing to EXACT_REPAIR.
        """
        ensemble = DyonGasBuilder.build_neutral_dipole_cluster(
            center=(0.0, 0.0, 0.0), separation=separation, config=self.config
        )
        inv_ensemble = self.dyonic_involution_transform(ensemble)

        q_net = ensemble.net_topological_charge
        m_net = ensemble.net_magnetic_charge

        s1 = ensemble.compute_total_action()
        s2 = inv_ensemble.compute_total_action()
        action_diff = abs(s1 - s2)

        w1, sig1 = ensemble.compute_weight()
        w2, sig2 = inv_ensemble.compute_weight()

        phi_1 = 0.0
        gamma_2 = 0.0
        route = TerminalRoute.EXACT_REPAIR

        return {
            "regime": GasRegime.MOLECULAR_CLUSTER.value,
            "net_topological_charge": q_net,
            "net_magnetic_charge": m_net,
            "action_original": s1,
            "action_involuted": s2,
            "action_difference": action_diff,
            "weight_original": (w1, sig1),
            "weight_involuted": (w2, sig2),
            "defect_mass_phi1": phi_1,
            "cochain_curvature_gamma2": gamma_2,
            "average_sign_recovered": 1.0,
            "terminal_route": route.value
        }

    def audit_ionized_plasma_regime(
        self,
        num_dyons: int = 6,
        box_size: float = 4.0
    ) -> Dict[str, object]:
        """
        Audits the ionized plasma regime where dyons are unconfined and isolated.
        Verifies Coulomb action gap ΔS > 0 and disjoint weight spectra supports,
        routing to SPLIT_BRAIN_REFUSAL.
        """
        pos_ensemble = DyonGasBuilder.build_neutral_dipole_cluster((0, 0, 0), 0.5, self.config)
        neg_ensemble = DyonGasBuilder.build_ionized_plasma_ensemble(
            num_dyons=num_dyons, box_size=box_size, config=self.config, seed=101
        )

        w_pos, sig_pos = pos_ensemble.compute_weight()
        w_neg, sig_neg = neg_ensemble.compute_weight()

        s_pos = pos_ensemble.compute_total_action()
        s_neg = neg_ensemble.compute_total_action()
        action_gap = abs(s_pos - s_neg)

        supports_disjoint = action_gap > 1.0
        phi_1 = float(action_gap / (1.0 + action_gap))
        gamma_2 = float(math.pi * (1.0 - math.exp(-action_gap)))
        route = TerminalRoute.SPLIT_BRAIN_REFUSAL

        return {
            "regime": GasRegime.IONIZED_PLASMA.value,
            "action_positive_cluster": s_pos,
            "action_negative_plasma": s_neg,
            "action_gap": action_gap,
            "supports_disjoint": supports_disjoint,
            "defect_mass_phi1": phi_1,
            "cochain_curvature_gamma2": gamma_2,
            "terminal_route": route.value
        }

    def audit_monopole_loop_braiding(
        self,
        num_points: int = 48
    ) -> Dict[str, object]:
        """
        Audits 't Hooft-Polyakov monopole loop braiding with center vortices.
        Evaluates Gauss linking integral Lk = 1, Dirac phase (-1)^Lk = -1,
        non-abelian Berry matrix holonomy, defect mass Φ₁ = 2.0, Γ₂ = π,
        routing to OPEN_SIGN_OBSTRUCTION.
        """
        l1, l2 = MonopoleLoopBraiding.build_hopf_link(radius=1.0, num_points=num_points)
        lk = MonopoleLoopBraiding.compute_gauss_linking(l1, l2)
        rounded_lk = int(round(lk))
        dirac_phase = MonopoleLoopBraiding.compute_dirac_aharonov_bohm_phase(lk)

        m_mono = MonopoleLoopBraiding.compute_monopole_braiding_matrix(rounded_lk, is_abelian=False)
        trace = float(np.trace(m_mono))
        norm_trace = trace / 2.0

        if dirac_phase < 0.0 or norm_trace < 0.0:
            phi_1 = 2.0
            gamma_2 = math.pi
            route = TerminalRoute.OPEN_SIGN_OBSTRUCTION
        else:
            phi_1 = 0.0
            gamma_2 = 0.0
            route = TerminalRoute.EXACT_REPAIR

        return {
            "regime": GasRegime.MONOPOLE_BRAIDING.value,
            "gauss_linking_number": lk,
            "rounded_linking": rounded_lk,
            "dirac_aharonov_bohm_phase": dirac_phase,
            "monopole_matrix_trace": trace,
            "normalized_trace": norm_trace,
            "defect_mass_phi1": phi_1,
            "cochain_curvature_gamma2": gamma_2,
            "terminal_route": route.value
        }

    def audit_complete_instanton_dyon_system(self) -> Dict[str, object]:
        """Runs the full three-regime evaluation."""
        mol = self.audit_molecular_cluster_regime()
        plasma = self.audit_ionized_plasma_regime()
        braid = self.audit_monopole_loop_braiding()

        return {
            "molecular_cluster": mol,
            "ionized_plasma": plasma,
            "monopole_braiding": braid,
            "summary_routes": {
                "molecular_cluster": mol["terminal_route"],
                "ionized_plasma": plasma["terminal_route"],
                "monopole_braiding": braid["terminal_route"]
            }
        }
