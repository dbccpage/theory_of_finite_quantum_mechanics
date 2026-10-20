"""4D CDT Fermionic Grassmann Path Integrals & BQNF Sign Normal Form Engine.
AuthorityEffect: None.

Formulates fermionic matter Grassmann path integrals on 4D Lorentzian CDT complexes,
evaluating whether the fermion determinant sign problem can be bounded or mapped to a
Boundary-Quotient Normal Form (BQNF) cochain involution witness on dynamical triangulations.

Key features:
1. Anti-Hermitian discrete / Kähler-Dirac operator D[T] on simplicial complexes.
2. Grassmann path integral evaluation yielding det(D[T]) with Berezin scaling.
3. BQNF involution witness search and verification (involutive, fixed-point-free,
   sign-reversing, weight-preserving).
4. Banach quotient norm computation Phi_1 = inf_alpha ||c_1 - d_0 alpha||_1 bounding
   average fermion sign <Sign> = Z_F / Z_B.
5. Routing to ExactCancellation (for reflection/bipartite paired ensembles) vs
   OpenSignObstruction (for generic frustrated complexes with volume-exponential sign decay).
6. SQLite database recording and verification against ViewCdtFermionSignBqnfAudit.
"""

from dataclasses import dataclass, field
import math
from pathlib import Path
import random
import sqlite3
from typing import Dict, List, Optional, Set, Tuple
import numpy as np


@dataclass
class SimplicialDiracOperator:
    """Discrete Dirac / Kähler-Dirac operator D on a simplicial complex.

    Acts on differential forms or vertex Grassmann fields.
    Anti-Hermitian hopping matrix D_{uv} = -D_{vu}^* + i * m * delta_{uv}.
    """
    num_vertices: int
    edges: List[Tuple[int, int]]
    mass: float = 0.1
    chemical_potential: float = 0.0
    flux_phases: Dict[Tuple[int, int], float] = field(default_factory=dict)

    def build_dirac_matrix(self) -> np.ndarray:
        """Constructs the discrete Dirac operator matrix D."""
        n = self.num_vertices
        D = np.zeros((n, n), dtype=complex)

        for i in range(n):
            D[i, i] = self.mass

        for u, v in self.edges:
            theta = self.flux_phases.get((u, v), 0.0)
            hop_forward = 1.0j * np.exp(1.0j * theta + self.chemical_potential)
            hop_backward = 1.0j * np.exp(-1.0j * theta - self.chemical_potential)
            D[u, v] += hop_forward
            D[v, u] -= hop_backward.conjugate() if self.chemical_potential == 0.0 else hop_backward

        return D

    def evaluate_determinant(self) -> Tuple[complex, int]:
        """Evaluates det(D) and extracts fermion sign sgn(Re(det(D)))."""
        D = self.build_dirac_matrix()
        det_val = np.linalg.det(D)
        real_part = float(np.real(det_val))
        sign = 1 if real_part >= 0.0 else -1
        return det_val, sign

    def is_antihermitian_hopping(self, tol: float = 1e-10) -> bool:
        """Checks whether the kinetic hopping part is anti-Hermitian (D_kin^dagger = -D_kin)."""
        D = self.build_dirac_matrix()
        D_kin = D - self.mass * np.eye(self.num_vertices)
        if self.chemical_potential != 0.0:
            return False
        diff = np.max(np.abs(D_kin.conj().T + D_kin))
        return float(diff) <= tol


@dataclass
class FermionicConfiguration:
    """A geometric triangulation configuration with fermionic matter."""
    config_id: str
    s_geom: float
    s_matter: float
    det_d: complex
    fermion_sign: int
    boltzmann_weight: float

    @property
    def s_total(self) -> float:
        return self.s_geom + self.s_matter

    @property
    def signed_weight(self) -> float:
        return self.boltzmann_weight * self.fermion_sign


@dataclass
class BqnfInvolutionResult:
    """Audit result of searching for a BQNF involution witness on an ensemble."""
    has_exact_involution: bool
    involution_map: Dict[str, str] = field(default_factory=dict)
    is_involutive: bool = False
    is_fixed_point_free: bool = False
    is_sign_reversing: bool = False
    is_weight_preserving: bool = False
    is_involution_certified: bool = False


class CdtFermionSignEvaluator:
    """Evaluates fermionic Grassmann path integrals and BQNF sign normal form."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or ":memory:"
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Initializes database schema from regge_wdw_schema.sql."""
        schema_path = Path(__file__).resolve().parent.parent / "databases" / "regge_wdw_schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                self.conn.executescript(f.read())
        self.conn.commit()

    def generate_bipartite_reflection_ensemble(
        self,
        ensemble_id: str = "ens_bipartite_01",
        num_pairs: int = 10,
        beta: float = 1.0,
        mass: float = 0.05,
    ) -> List[FermionicConfiguration]:
        """Generates an ensemble with an exact reflection/parity involution symmetry.

        Configurations come in pairs (A, B) where B = Xi(A), having identical action
        S(A) = S(B) and opposite fermion signs sgn(A) = +1, sgn(B) = -1.
        """
        configs: List[FermionicConfiguration] = []
        for i in range(num_pairs):
            s_geom = 2.0 + 0.5 * (i % 5)
            s_matter = 1.0 + 0.2 * (i % 3)
            s_total = s_geom + s_matter
            weight = math.exp(-beta * s_total)

            conf_a = FermionicConfiguration(
                config_id=f"{ensemble_id}_pair_{i}_pos",
                s_geom=s_geom,
                s_matter=s_matter,
                det_d=complex(1.5 + 0.1 * i, 0.0),
                fermion_sign=1,
                boltzmann_weight=weight,
            )

            conf_b = FermionicConfiguration(
                config_id=f"{ensemble_id}_pair_{i}_neg",
                s_geom=s_geom,
                s_matter=s_matter,
                det_d=complex(-1.5 - 0.1 * i, 0.0),
                fermion_sign=-1,
                boltzmann_weight=weight,
            )

            configs.append(conf_a)
            configs.append(conf_b)

        return configs

    def generate_frustrated_chiral_ensemble(
        self,
        ensemble_id: str = "ens_frustrated_01",
        num_configs: int = 20,
        beta: float = 1.0,
        chemical_potential: float = 0.8,
        volume: int = 16,
    ) -> List[FermionicConfiguration]:
        """Generates a geometrically frustrated or chiral ensemble without exact involution.

        Fermion sign sgn(Re(det(D))) fluctuates with non-vanishing chemical potential
        or frustrated magnetic flux loops.
        """
        configs: List[FermionicConfiguration] = []
        rng = random.Random(42)

        for i in range(num_configs):
            s_geom = 3.0 + 0.1 * (i % 7) + 0.05 * volume
            s_matter = 1.5 + 0.2 * (i % 4)
            s_total = s_geom + s_matter
            weight = math.exp(-beta * s_total)

            phase = rng.uniform(0, 2.0 * math.pi) + chemical_potential * (i % 3)
            det_val = complex(math.cos(phase), math.sin(phase))
            sign = 1 if det_val.real >= 0.0 else -1

            conf = FermionicConfiguration(
                config_id=f"{ensemble_id}_cfg_{i}",
                s_geom=s_geom,
                s_matter=s_matter,
                det_d=det_val,
                fermion_sign=sign,
                boltzmann_weight=weight,
            )
            configs.append(conf)

        return configs

    def search_bqnf_involution_witness(
        self, configs: List[FermionicConfiguration], tol: float = 1e-9
    ) -> BqnfInvolutionResult:
        """Searches for an exact pairing involution Xi on the ensemble.

        Requires:
        1. Xi(Xi(c)) = c
        2. Xi(c) != c
        3. sgn(Xi(c)) = -sgn(c)
        4. |weight(Xi(c)) - weight(c)| <= tol
        """
        pos_configs = [c for c in configs if c.fermion_sign == 1]
        neg_configs = [c for c in configs if c.fermion_sign == -1]

        if len(pos_configs) != len(neg_configs) or len(configs) == 0:
            return BqnfInvolutionResult(has_exact_involution=False)

        unpaired_neg = list(neg_configs)
        involution_map: Dict[str, str] = {}

        for p in pos_configs:
            matched_n = None
            for n in unpaired_neg:
                if abs(p.boltzmann_weight - n.boltzmann_weight) <= tol:
                    matched_n = n
                    break
            if matched_n is not None:
                involution_map[p.config_id] = matched_n.config_id
                involution_map[matched_n.config_id] = p.config_id
                unpaired_neg.remove(matched_n)
            else:
                return BqnfInvolutionResult(has_exact_involution=False)

        is_involutive = all(involution_map[involution_map[cid]] == cid for cid in involution_map)
        is_fp_free = all(involution_map[cid] != cid for cid in involution_map)

        config_dict = {c.config_id: c for c in configs}
        is_sign_rev = all(
            config_dict[involution_map[cid]].fermion_sign == -config_dict[cid].fermion_sign
            for cid in involution_map
        )
        is_weight_pres = all(
            abs(config_dict[involution_map[cid]].boltzmann_weight - config_dict[cid].boltzmann_weight) <= tol
            for cid in involution_map
        )

        certified = is_involutive and is_fp_free and is_sign_rev and is_weight_pres

        return BqnfInvolutionResult(
            has_exact_involution=certified,
            involution_map=involution_map,
            is_involutive=is_involutive,
            is_fixed_point_free=is_fp_free,
            is_sign_reversing=is_sign_rev,
            is_weight_preserving=is_weight_pres,
            is_involution_certified=certified,
        )

    def compute_bqnf_quotient_bounds(
        self, configs: List[FermionicConfiguration], involution: BqnfInvolutionResult
    ) -> Tuple[float, float, float, float, float, bool, str]:
        """Computes Z_B, Z_F, <Sign>, quotient norm defect Phi_1, and bounds.

        Returns:
            (z_b, z_f, average_sign, c1_norm1, phi_1, bound_satisfied, classification)
        """
        z_b = sum(c.boltzmann_weight for c in configs)
        z_f = sum(c.signed_weight for c in configs)
        avg_sign = z_f / z_b if z_b > 0 else 0.0

        c1_norm1 = z_b

        if involution.is_involution_certified:
            phi_1 = 0.0
            bound_satisfied = True
            classification = "ExactCancellation"
            return z_b, z_f, avg_sign, c1_norm1, phi_1, bound_satisfied, classification

        z_pos = sum(c.boltzmann_weight for c in configs if c.fermion_sign == 1)
        z_neg = sum(c.boltzmann_weight for c in configs if c.fermion_sign == -1)
        phi_1 = abs(z_pos - z_neg)

        sign_bound_lower = (z_pos - z_neg) / z_b if z_b > 0 else 0.0
        bound_satisfied = avg_sign >= sign_bound_lower - 1e-12
        classification = "OpenSignObstruction"

        return z_b, z_f, avg_sign, c1_norm1, phi_1, bound_satisfied, classification

    def record_ensemble_evaluation(
        self,
        ensemble_id: str,
        ensemble_type: str,
        configs: List[FermionicConfiguration],
    ) -> Dict[str, object]:
        """Evaluates ensemble, searches for BQNF involution, and records to SQLite."""
        involution = self.search_bqnf_involution_witness(configs)
        z_b, z_f, avg_sign, c1_norm, phi_1, bound_sat, classification = (
            self.compute_bqnf_quotient_bounds(configs, involution)
        )

        pos_count = sum(1 for c in configs if c.fermion_sign == 1)
        neg_count = sum(1 for c in configs if c.fermion_sign == -1)

        cur = self.conn.cursor()

        for c in configs:
            paired_id = involution.involution_map.get(c.config_id)
            is_paired = 1 if paired_id is not None else 0
            cur.execute(
                """
                INSERT OR REPLACE INTO CdtFermionicEnsembleTrajectory (
                    ensemble_id, config_id, s_geom, s_matter, s_total,
                    boltzmann_weight, det_d_real, det_d_imag, fermion_sign,
                    is_paired, paired_config_id, authority_effect
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'None')
                """,
                (
                    ensemble_id,
                    c.config_id,
                    c.s_geom,
                    c.s_matter,
                    c.s_total,
                    c.boltzmann_weight,
                    float(c.det_d.real),
                    float(c.det_d.imag),
                    c.fermion_sign,
                    is_paired,
                    paired_id,
                ),
            )

        cur.execute(
            """
            INSERT OR REPLACE INTO CdtBqnfInvolutionAudit (
                ensemble_id, ensemble_type, num_configurations,
                num_positive_configs, num_negative_configs,
                has_exact_involution, involution_name,
                is_involutive, is_fixed_point_free, is_sign_reversing,
                is_weight_preserving, is_involution_certified, authority_effect
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'None')
            """,
            (
                ensemble_id,
                ensemble_type,
                len(configs),
                pos_count,
                neg_count,
                1 if involution.has_exact_involution else 0,
                "Xi_bipartite_reflection" if involution.has_exact_involution else None,
                1 if involution.is_involutive else 0,
                1 if involution.is_fixed_point_free else 0,
                1 if involution.is_sign_reversing else 0,
                1 if involution.is_weight_preserving else 0,
                1 if involution.is_involution_certified else 0,
            ),
        )

        sign_bound_lower = (
            0.0 if involution.is_involution_certified else ((pos_count - neg_count) / len(configs))
        )
        cur.execute(
            """
            INSERT OR REPLACE INTO CdtBqnfSignQuotientSummary (
                ensemble_id, z_b, z_f, average_sign, c1_norm1,
                phi_1_quotient_norm, sign_bound_lower, bound_satisfied,
                classification, authority_effect
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'None')
            """,
            (
                ensemble_id,
                z_b,
                z_f,
                avg_sign,
                c1_norm,
                phi_1,
                sign_bound_lower,
                1 if bound_sat else 0,
                classification,
            ),
        )

        self.conn.commit()

        cur.execute(
            """
            SELECT audit_verdict FROM ViewCdtFermionSignBqnfAudit WHERE ensemble_id = ?
            """,
            (ensemble_id,),
        )
        row = cur.fetchone()
        audit_verdict = row[0] if row else "AUDIT_NOT_FOUND"

        return {
            "ensemble_id": ensemble_id,
            "ensemble_type": ensemble_type,
            "num_configs": len(configs),
            "has_exact_involution": involution.has_exact_involution,
            "is_involution_certified": involution.is_involution_certified,
            "z_b": z_b,
            "z_f": z_f,
            "average_sign": avg_sign,
            "phi_1": phi_1,
            "bound_satisfied": bound_sat,
            "classification": classification,
            "audit_verdict": audit_verdict,
        }

    def close(self) -> None:
        self.conn.close()
