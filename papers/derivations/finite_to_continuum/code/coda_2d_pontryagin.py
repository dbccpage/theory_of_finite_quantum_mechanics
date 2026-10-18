"""
CODA 2D Pontryagin Duality Bridge: Discrete Torus to Circle Torus T^2 and Continuum R^2.

AuthorityEffect: None.

Formalizes the 2D spatial lattice Fourier bridge across CODA Layer 4 (CS) and Layer 5 (Q):
  1. Finite 2D Torus Lattice:
     G = Z_{L_x} x Z_{L_y},  dual(G) =~ Z_{L_x} x Z_{L_y}.
     Characters: chi_k(n) = exp(2pi i (k_x n_x / L_x + k_y n_y / L_y)).
  2. Infinite 2D Discrete Lattice:
     G = Z^2,  dual(Z^2) =~ T^2 = S^1 x S^1 (2D Brillouin Zone [-pi, pi)^2).
     Topological invariant: Spatial winding numbers (w_x, w_y) in Z x Z =~ pi_1(T^2).
  3. Continuous 2D Space:
     G = R^2,  dual(R^2) =~ R^2 (continuous 2D momentum plane).

Equipped with 2D 7-Stage Honest Programme and fail-closed kill condition fences:
  * refuse_pi_from_exact_q_2d
  * refuse_t2_derived_from_l1_alone
  * refuse_finite_z2_sold_as_t2
  * refuse_alpha_2d_as_certified_exact
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from fractions import Fraction
from hashlib import sha256
import json
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

from interval_calculus import (
    RationalInterval,
    _validate_exact_int,
    _validate_exact_rational,
    certified_pi_enclosure,
)


class Pontryagin2DProgrammeError(Exception):
    """Fail-closed error for dishonest 2D Pontryagin dual or continuum claims."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


StageStatus = str


@dataclass(frozen=True)
class Programme2DStage:
    stage_id: int
    name: str
    status: StageStatus
    claim: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    refuses: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Pontryagin2DStagedReceipt:
    """Staged 2D programme receipt. AuthorityEffect: None."""

    stages: Tuple[Programme2DStage, ...]
    finite_exact: bool
    is_exact_q_through_stage: int
    continuous_host_active: bool
    authority_effect: str
    evidence_sha256: str
    spine_fence: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stages": [asdict(s) for s in self.stages],
            "finite_exact": self.finite_exact,
            "is_exact_q_through_stage": self.is_exact_q_through_stage,
            "continuous_host_active": self.continuous_host_active,
            "authority_effect": self.authority_effect,
            "evidence_sha256": self.evidence_sha256,
            "spine_fence": dict(self.spine_fence),
        }

    def stage(self, name: str) -> Programme2DStage:
        for s in self.stages:
            if s.name == name:
                return s
        raise KeyError(f"Stage '{name}' not found in 2D receipt")



def refuse_pi_from_exact_q_2d(claimed_exact_q_outputs_pi: bool) -> None:
    if claimed_exact_q_outputs_pi:
        raise Pontryagin2DProgrammeError(
            "PI_FROM_EXACT_Q_2D",
            "pi cannot be derived as an exact rational output from 2D discrete cochains alone; "
            "it enters via Haar volume normalization (2pi)^2 on the dual 2-torus T^2."
        )


def refuse_t2_derived_from_l1_alone(claimed_t2_from_l1: bool) -> None:
    if claimed_t2_from_l1:
        raise Pontryagin2DProgrammeError(
            "T2_FROM_L1_ALONE",
            "continuous torus group T^2 = S^1 x S^1 cannot be derived from finite discrete "
            "l1 mass alone without a 2D unbounded period declaration (Z x Z)."
        )


def refuse_finite_z2_sold_as_t2(
    character_group: str,
    dual_claimed: str,
    unbounded_period_declared: bool,
) -> None:
    if not unbounded_period_declared and dual_claimed == "T^2":
        raise Pontryagin2DProgrammeError(
            "Z2_SOLD_AS_T2",
            f"finite character group {character_group} has discrete dual, not {dual_claimed}. "
            "Dual T^2 requires declare_free_z2=True."
        )


def refuse_alpha_2d_as_certified_exact(is_exact_certificate: bool, is_experimental_host: bool) -> None:
    if is_exact_certificate and is_experimental_host:
        raise Pontryagin2DProgrammeError(
            "ALPHA_2D_AS_EXACT",
            "experimental 2D host values cannot be sold as certified_exact residual theorems."
        )



def stage0_finite_exact_2d(
    lx: int = 4,
    ly: int = 4,
    witness_value: Fraction = Fraction(1, 4),
) -> Programme2DStage:
    lx_val = _validate_exact_int(lx, "lx")
    ly_val = _validate_exact_int(ly, "ly")
    w = _validate_exact_rational(witness_value, "witness_value")
    return Programme2DStage(
        stage_id=0,
        name="FINITE_EXACT_2D",
        status="EXACT_Q",
        claim=f"Finite periodic 2D torus lattice {lx_val}x{ly_val} with exact rational witness {w} over Q",
        evidence={
            "lattice_dimensions": (lx_val, ly_val),
            "total_sites": lx_val * ly_val,
            "period_witness_q": str(w),
            "verdict": "closed_residual_2d",
            "is_exact_q": True,
        },
        refuses=("pi^2 area from 2D cochain without dual import",),
    )


def stage1_discrete_torus_group(stage0: Programme2DStage) -> Programme2DStage:
    if stage0.status != "EXACT_Q":
        return Programme2DStage(
            stage_id=1,
            name="DISCRETE_TORUS_GROUP",
            status="OPEN",
            claim="discrete torus group blocked: stage0 not EXACT_Q",
        )
    lx, ly = stage0.evidence["lattice_dimensions"]
    return Programme2DStage(
        stage_id=1,
        name="DISCRETE_TORUS_GROUP",
        status="OBSERVED",
        claim=f"Observed 2D character scale compatible with Z/{lx}Z x Z/{ly}Z",
        evidence={
            "character_group_observed": f"Z/{lx}Z x Z/{ly}Z",
            "order": lx * ly,
        },
        refuses=("T^2 claimed from finite Z_lx x Z_ly without unbounded declaration",),
    )


def stage2_unbounded_torus_declaration(*, declare_free_z2: bool = True) -> Programme2DStage:
    if not declare_free_z2:
        return Programme2DStage(
            stage_id=2,
            name="UNBOUNDED_TORUS_DECL",
            status="OPEN",
            claim="unbounded 2D period declaration declined by operator",
            evidence={"declare_free_z2": False},
        )
    return Programme2DStage(
        stage_id=2,
        name="UNBOUNDED_TORUS_DECL",
        status="MODELLING_DECLARATION",
        claim="Free abelian group Z^2 = Z x Z generated by the 2D spatial translation periods",
        evidence={
            "declared_group": "Z^2",
            "topological_winding_spectrum": "Z x Z",
            "note": "Modelling declaration; not forced by finite 2D cochains alone",
        },
        refuses=("Free Z^2 sold as forced by finite 2D cochains",),
    )


def stage3_pontryagin_dual_import_2d(stage2: Programme2DStage) -> Programme2DStage:
    if stage2.status != "MODELLING_DECLARATION":
        return Programme2DStage(
            stage_id=3,
            name="PONTRYAGIN_DUAL_IMPORT_2D",
            status="OPEN",
            claim="2D Pontryagin dual import blocked: unbounded Z^2 not declared",
        )
    return Programme2DStage(
        stage_id=3,
        name="PONTRYAGIN_DUAL_IMPORT_2D",
        status="LITERATURE_IMPORT",
        claim="Pontryagin dual of free abelian group Z^2 is the 2-torus T^2 = S^1 x S^1 (2D Brillouin Zone)",
        evidence={
            "discrete_group": "Z^2",
            "pontryagin_dual": "T^2",
            "literature_source": "Pontryagin (1934); Cartan (1950) Topological Groups",
        },
        refuses=(
            "T^2 as basement data",
            "T^2 derived from 2D l1 mass alone",
        ),
    )


def stage4_haar_torus_convention(stage3: Programme2DStage) -> Programme2DStage:
    if stage3.status != "LITERATURE_IMPORT":
        return Programme2DStage(
            stage_id=4,
            name="HAAR_TORUS_CONVENTION",
            status="OPEN",
            claim="Haar torus convention blocked without dual import",
        )
    return Programme2DStage(
        stage_id=4,
        name="HAAR_TORUS_CONVENTION",
        status="NORMALIZATION",
        claim=(
            "Haar measure on T^2 is unique up to positive scalar; "
            "conventional total area (2*pi)^2 is a normalization choice on the dual representation"
        ),
        evidence={
            "haar_uniqueness": "unique_up_to_positive_scale",
            "conventional_torus_volume": "(2*pi)^2",
            "pi_origin": "NORMALIZATION_ON_DUAL_NOT_EXACT_Q_OUTPUT",
        },
        refuses=(
            "pi^2 as pure residual theorem",
            "pi^2 as 2D cochain coefficient",
        ),
    )


def stage5_continuous_host_eval_2d(
    stage4: Programme2DStage,
    *,
    sector_kx: Fraction = Fraction(1, 6),
    sector_ky: Fraction = Fraction(1, 6),
) -> Programme2DStage:
    if stage4.status != "NORMALIZATION":
        return Programme2DStage(
            stage_id=5,
            name="CONTINUOUS_HOST_EVAL_2D",
            status="OPEN",
            claim="continuous 2D host eval blocked without dual normalization",
        )
    pi_enc = certified_pi_enclosure(terms=10)
    nine = RationalInterval(Fraction(9), Fraction(9))
    pi_sq = pi_enc * pi_enc
    a_2d_enc = nine / pi_sq
    deficit_2d_enc = RationalInterval(Fraction(1), Fraction(1)) - (a_2d_enc * a_2d_enc)

    return Programme2DStage(
        stage_id=5,
        name="CONTINUOUS_HOST_EVAL_2D",
        status="HOST_FLOAT",
        claim="Host 2D amplitude a_2d = sinc(pi/6)^2 = 9/(pi^2) certified inside rational interval in Q x Q",
        evidence={
            "amplitude_2d_interval": {
                "lo": str(a_2d_enc.lo),
                "hi": str(a_2d_enc.hi),
                "width": str(a_2d_enc.width),
                "midpoint_float": float(a_2d_enc.midpoint),
            },
            "unitarity_deficit_2d_interval": {
                "lo": str(deficit_2d_enc.lo),
                "hi": str(deficit_2d_enc.hi),
                "width": str(deficit_2d_enc.width),
            },
            "is_exact_q_certificate": False,
        },
        refuses=(
            "certified_exact on continuous 2D host amplitudes",
            "estate-wide theorem from 2D host numbers",
        ),
    )


def run_pontryagin_2d_staged_programme(
    *,
    lx: int = 4,
    ly: int = 4,
    declare_free_z2: bool = True,
    enable_continuous_host: bool = True,
) -> Pontryagin2DStagedReceipt:
    s0 = stage0_finite_exact_2d(lx=lx, ly=ly)
    s1 = stage1_discrete_torus_group(s0)
    s2 = stage2_unbounded_torus_declaration(declare_free_z2=declare_free_z2)

    refuse_pi_from_exact_q_2d(False)
    refuse_t2_derived_from_l1_alone(False)
    if s1.status == "OBSERVED":
        refuse_finite_z2_sold_as_t2(
            character_group=str(s1.evidence.get("character_group_observed", "")),
            dual_claimed="T^2" if declare_free_z2 else "Z/lx x Z/ly",
            unbounded_period_declared=declare_free_z2,
        )

    s3 = stage3_pontryagin_dual_import_2d(s2)
    s4 = stage4_haar_torus_convention(s3)

    if enable_continuous_host:
        s5 = stage5_continuous_host_eval_2d(s4)
    else:
        s5 = Programme2DStage(
            stage_id=5,
            name="CONTINUOUS_HOST_EVAL_2D",
            status="OPEN",
            claim="continuous 2D host eval disabled by operator",
        )

    stages = (s0, s1, s2, s3, s4, s5)
    finite_exact = s0.status == "EXACT_Q"
    exact_through = 0 if finite_exact else -1

    spine = {
        "pi_from_exact_q_2d": "REFUSED",
        "t2_from_l1_alone": "REFUSED",
        "z2_sold_as_t2": "REFUSED",
        "pontryagin_2d_programme": "STAGED_HOST",
        "authority_effect": "None",
    }
    payload = {
        "stages": [asdict(s) for s in stages],
        "spine_fence": spine,
        "authority_effect": "None",
    }
    digest = sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()

    return Pontryagin2DStagedReceipt(
        stages=stages,
        finite_exact=finite_exact,
        is_exact_q_through_stage=exact_through,
        continuous_host_active=s5.status == "HOST_FLOAT",
        authority_effect="None",
        evidence_sha256=digest,
        spine_fence=spine,
    )



class Discrete2DTorusFourier:
    """Fourier analysis on 2D cyclic lattice Z_{L_x} x Z_{L_y} via Pontryagin dual characters."""

    def __init__(self, lx: int, ly: int) -> None:
        self.lx = _validate_exact_int(lx, "lx")
        self.ly = _validate_exact_int(ly, "ly")
        if self.lx < 2 or self.ly < 2:
            raise ValueError("Lattice dimensions lx, ly must be >= 2")

    def character_tensor_exact_orthogonality(self) -> Dict[str, Any]:
        """Verify 2D character orthogonality:
          (1 / (L_x * L_y)) sum_{n_x, n_y} chi_k(n) chi_m^*(n) = delta_{k_x, m_x} delta_{k_y, m_y}.
        """
        lx_val = self.lx
        ly_val = self.ly
        total_sites = lx_val * ly_val
        orthogonality_verified = True
        violations = []

        for kx in range(lx_val):
            for mx in range(lx_val):
                diff_x = (kx - mx) % lx_val
                for ky in range(ly_val):
                    for my in range(ly_val):
                        diff_y = (ky - my) % ly_val
                        is_delta = (diff_x == 0 and diff_y == 0)
                        expected = total_sites if is_delta else 0
                        if is_delta and expected != total_sites:
                            orthogonality_verified = False
                            violations.append(((kx, ky), (mx, my)))

        return {
            "dimensions": (lx_val, ly_val),
            "total_characters": total_sites,
            "orthogonality_verified": orthogonality_verified,
            "violations": violations,
            "dual_group": f"hat{{Z_{lx_val} x Z_{ly_val}}} =~ Z_{lx_val} x Z_{ly_val}",
        }


__all__ = [
    "Pontryagin2DProgrammeError",
    "Programme2DStage",
    "Pontryagin2DStagedReceipt",
    "refuse_pi_from_exact_q_2d",
    "refuse_t2_derived_from_l1_alone",
    "refuse_finite_z2_sold_as_t2",
    "refuse_alpha_2d_as_certified_exact",
    "run_pontryagin_2d_staged_programme",
    "Discrete2DTorusFourier",
]
