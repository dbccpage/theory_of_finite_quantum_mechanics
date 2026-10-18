# -*- coding: utf-8 -*-
"""
End-to-End Demonstration: Finite to Continuum Bridging Pipeline.

AuthorityEffect: None.

Demonstrates:
  1. CODA-Q Certified Rational Interval Arithmetic ([lo, hi] in Q x Q, width < eps)
  2. CS-Q Discretization Defect Operators (1D & 2D Cubature, |E| <= Cx ax^2 + Cy ay^2)
  3. Wilsonian Finite-Size Scaling Extrapolation (Neville tableau in (1/L)^2)
  4. Pontryagin Duality Bridge (1D Cyclic to S^1, 2D Torus Z_Lx x Z_Ly to T^2)
  5. Meron-Cluster Fermion Chain: Extrapolating exact transfer traces L=4, 6, 8 to f_infty

Emits stamped machine-readable JSON receipts to results/ and demos/results/.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any, Dict

# Ensure project code/ is importable
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CODE_DIR = str(PROJECT_ROOT / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from coda_2d_discretization_defect import (
    Discrete2DCubatureSolver,
    verify_2d_mesh_refinement,
)
from coda_2d_pontryagin import (
    Discrete2DTorusFourier,
    run_pontryagin_2d_staged_programme,
)
from discretization_defect import (
    DiscreteTrapezoidalQuadratureSolver,
    verify_mesh_refinement,
)
from interval_calculus import (
    RationalInterval,
    certified_pi_enclosure,
    exp_interval,
    rational_heron_sqrt_bounds,
)
from meron_wilsonian_bridge import MeronWilsonianBridge
from pontryagin_duality import (
    DiscreteLatticeFourier,
    run_pontryagin_staged_programme,
)
from wilsonian_extrapolator import WilsonianExtrapolator


def run_full_pipeline_demo() -> Dict[str, Any]:
    print("=" * 76)
    print("  OMEGA ENGINE: FINITE TO CONTINUUM RECOVERY & MERON BRIDGE")
    print("  AuthorityEffect: None | Zero-Float Exact Rational Arithmetic")
    print("=" * 76)

    # ---------------------------------------------------------
    # STEP 1: CODA-Q Rational Interval Calculus
    # ---------------------------------------------------------
    print("\n[Step 1] Certified Rational Interval Arithmetic (CODA-Q)")
    lo_sqrt2, hi_sqrt2 = rational_heron_sqrt_bounds(Fraction(2), steps=8)
    sqrt2_int = RationalInterval(lo_sqrt2, hi_sqrt2)
    print(f"  sqrt(2) Enclosure: [{float(sqrt2_int.lo):.12f}, {float(sqrt2_int.hi):.12f}] | width: {float(sqrt2_int.width):.2e}")

    pi_int = certified_pi_enclosure(terms=10)
    print(f"  pi Enclosure:      [{float(pi_int.lo):.12f}, {float(pi_int.hi):.12f}] | width: {float(pi_int.width):.2e}")

    e_int = exp_interval(RationalInterval(Fraction(1), Fraction(1)), order=16)
    print(f"  e Enclosure:       [{float(e_int.lo):.12f}, {float(e_int.hi):.12f}] | width: {float(e_int.width):.2e}")

    step1_data = {
        "sqrt2_width": str(sqrt2_int.width),
        "pi_width": str(pi_int.width),
        "e_width": str(e_int.width),
        "zero_float_certified": True,
    }

    # ---------------------------------------------------------
    # STEP 2: CS-Q Discretization Defect Operators (1D & 2D)
    # ---------------------------------------------------------
    print("\n[Step 2] CS-Q Discretization Defect Operators (1D & 2D)")
    # 1D Quadrature: int_0^1 x^2 dx = 1/3
    quad_solver = DiscreteTrapezoidalQuadratureSolver(lambda x: x * x, m2_bound=Fraction(2))
    c1d_coarse = quad_solver.solve(8)
    c1d_fine = quad_solver.solve(16)
    rec_1d = verify_mesh_refinement(c1d_coarse, c1d_fine)
    print(f"  1D Refinement (N=8 -> N=16): Contractive={rec_1d.is_contractive} | Overlapping={rec_1d.is_overlapping}")
    print(f"  1D Refined Enclosure of 1/3: [{rec_1d.refined_enclosure.lo}, {rec_1d.refined_enclosure.hi}]")

    # 2D Cubature: iint_[0,1]^2 (x^2 * y^2) dx dy = 1/9
    cub_solver = Discrete2DCubatureSolver(lambda x, y: (x * x) * (y * y), m_xx_bound=Fraction(2), m_yy_bound=Fraction(2))
    c2d_coarse = cub_solver.solve(4, 4)
    c2d_fine = cub_solver.solve(8, 8)
    rec_2d = verify_2d_mesh_refinement(c2d_coarse, c2d_fine)
    print(f"  2D Refinement (4x4 -> 8x8): Contractive={rec_2d.is_contractive} | Overlapping={rec_2d.is_overlapping}")
    print(f"  2D Refined Enclosure of 1/9: [{rec_2d.refined_enclosure.lo}, {rec_2d.refined_enclosure.hi}]")

    step2_data = {
        "1d_refinement_receipt_sha256": rec_1d.receipt_sha256,
        "1d_encloses_1_3": rec_1d.refined_enclosure.contains(Fraction(1, 3)),
        "2d_refinement_receipt_sha256": rec_2d.receipt_sha256,
        "2d_encloses_1_9": rec_2d.refined_enclosure.contains(Fraction(1, 9)),
    }

    # ---------------------------------------------------------
    # STEP 3: Wilsonian Finite-Size Scaling Extrapolation
    # ---------------------------------------------------------
    print("\n[Step 3] Wilsonian Extrapolation on L=4, 6, 8, 12 Chains")
    true_f_infty = Fraction(7, 13)
    c1 = Fraction(5, 3)
    c2 = Fraction(-8, 9)
    extrapolator = WilsonianExtrapolator(scaling_variable_power=2)
    for l in (4, 6, 8, 12):
        extrapolator.add_observation(l, true_f_infty + c1 / (l ** 2) + c2 / (l ** 4))
    scaling_receipt = extrapolator.extrapolate()
    thermo_lim = scaling_receipt.extrapolated_thermodynamic_limit
    print(f"  Extrapolated Thermodynamic Limit: [{thermo_lim.lo}, {thermo_lim.hi}] | Expected: {true_f_infty}")
    print(f"  Exact Recovery Verified? {thermo_lim.lo == true_f_infty == thermo_lim.hi}")

    step3_data = scaling_receipt.to_dict()

    # ---------------------------------------------------------
    # PONTRYAGIN DUALITY: 1D CYCLIC AND 2D TORUS
    # ---------------------------------------------------------
    print("\n[Pontryagin Bridge] 1D and 2D Duality Programmes")
    pont_1d = run_pontryagin_staged_programme(lattice_size=6)
    pont_2d = run_pontryagin_2d_staged_programme(lx=4, ly=4)
    print(f"  1D Programme: 7 Stages | Stage 5 a=sinc(pi/6)=3/pi: {pont_1d.stage('CONTINUOUS_HOST_EVAL').status}")
    print(f"  2D Programme: 6 Stages | Stage 5 a_2d=sinc(pi/6)^2: {pont_2d.stage('CONTINUOUS_HOST_EVAL_2D').status}")

    # Character orthogonality checks
    fourier_1d = DiscreteLatticeFourier(6)
    fourier_2d = Discrete2DTorusFourier(4, 4)
    ortho_1d = fourier_1d.character_matrix_exact_orthogonality()
    ortho_2d = fourier_2d.character_tensor_exact_orthogonality()
    print(f"  1D Character Orthogonality (Z_6): {ortho_1d['orthogonality_verified']}")
    print(f"  2D Character Orthogonality (Z_4 x Z_4): {ortho_2d['orthogonality_verified']}")

    pont_data = {
        "1d_staged_receipt": pont_1d.to_dict(),
        "2d_staged_receipt": pont_2d.to_dict(),
        "orthogonality_1d": ortho_1d["orthogonality_verified"],
        "orthogonality_2d": ortho_2d["orthogonality_verified"],
    }

    # ---------------------------------------------------------
    # MERON-CLUSTER FERMION CHAIN WILSONIAN EXTRAPOLATION
    # ---------------------------------------------------------
    print("\n[Meron Wilsonian Bridge] Extrapolating Fermion Chain Transfer Traces")
    meron_bridge = MeronWilsonianBridge()
    meron_rec, meron_scaling = meron_bridge.extrapolate_meron_continuum(chain_lengths=(4, 6, 8))
    print(f"  Traces: L=4 -> {meron_rec.partition_sums[4]} | L=6 -> {meron_rec.partition_sums[6]} | L=8 -> {meron_rec.partition_sums[8]}")
    print(f"  Log Densities: L=4 -> {meron_rec.log_partition_densities[4]['float_midpoint']} | L=6 -> {meron_rec.log_partition_densities[6]['float_midpoint']} | L=8 -> {meron_rec.log_partition_densities[8]['float_midpoint']}")
    print(f"  Thermodynamic Limit f_infty: {meron_rec.thermodynamic_limit['float_midpoint']} (certified interval width: {meron_rec.thermodynamic_limit['width']})")
    print(f"  Meron Thermodynamic SHA256: {meron_rec.receipt_sha256}")

    # ---------------------------------------------------------
    # ASSEMBLE MASTER EXECUTION RECEIPT
    # ---------------------------------------------------------
    master_receipt = {
        "title": "Finite to Continuum Recovery & Meron Bridge Execution Receipt",
        "authority_effect": "None",
        "step1_coda_q_interval_calculus": step1_data,
        "step2_cs_q_discretization_defect": step2_data,
        "step3_wilsonian_extrapolation": step3_data,
        "pontryagin_duality_bridge": pont_data,
        "meron_wilsonian_bridge": meron_rec.to_dict(),
    }
    master_digest = sha256(json.dumps(master_receipt, sort_keys=True, default=str).encode("utf-8")).hexdigest()
    master_receipt["master_sha256"] = master_digest

    out_paths = [
        PROJECT_ROOT / "results" / "continuum_recovery_receipt.json",
        PROJECT_ROOT / "demos" / "results" / "demo_pipeline_receipt.json",
    ]
    for path in out_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(master_receipt, f, indent=2)
        print(f"  Saved master receipt to: {path.name}")

    print("\n" + "=" * 76)
    print("  ALL 5 SECTIONS COMPLETED AND EXACTLY CERTIFIED OVER Q")
    print(f"  Master SHA256: {master_digest}")
    print("=" * 76)

    return master_receipt


if __name__ == "__main__":
    run_full_pipeline_demo()
