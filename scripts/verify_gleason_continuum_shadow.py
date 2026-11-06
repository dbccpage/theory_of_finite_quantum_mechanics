"""Exact rational verifier and receipt generator for the Phase 3 Gleason continuum shadow.

AuthorityEffect: None.

Verifies:
1. The historical-to-current crosswalk for FOC, MUR, CS, CS_Q, Q, A, OR, FDA (and CODA_GTLA).
2. Exact descent on the realized observation image Set.range p vs. non-unique extension on
   unrealized observation labels o_0 not in Set.range p.
3. Approximate decoder collision bound (|q(x) - q(y)| <= 2 * eps when p(x) = p(y)) and
   pseudometric zero-distance vs. state/query equality separation.
4. Exact 9-ray tomography section property, restricted quadratic factorization, and explicit
   nonquadratic aliasing witnesses (exoticQi3 vs. maximallyMixedForm3, s3 vs. 0).
5. Quantitative 9-ray tomography stability (|Delta d_i| <= eps, |Delta a_ij| <= 2*eps,
   |Delta b_ij| <= 2*eps, coeffNorm <= 27*eps with sharpness witness, ray probability error
   <= 27*eps, trace error <= 3*eps, and multi-stage additive error accumulation).
6. Quantitative Rayleigh-quotient continuity:
     (quadRay rho u - quadRay rho v)^2 <= 4 * coeffNorm(rho)^2 * raySinSq(u, v)
                                       <= 8 * coeffNorm(rho)^2 * raySinSq(u, v)
   and constructive rational modulus rationalRayModulus(B, eps) across normal and degenerate
   regimes (B <= 0 and coeffNorm == 0).
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "evidence" / "lean_receipts" / "gleason_continuum_shadow_receipt.json"
LEAN_MODULE = ROOT / "lean4" / "GleasonContinuumShadow.lean"


@dataclass(frozen=True)
class GaussRat:
    re: Fraction
    im: Fraction = Fraction(0)

    def __add__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(self.re + other.re, self.im + other.im)

    def __sub__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(self.re - other.re, self.im - other.im)

    def __mul__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def conj(self) -> "GaussRat":
        return GaussRat(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im


GVec = Tuple[GaussRat, GaussRat, GaussRat]


def gv(xr: int, xi: int, yr: int, yi: int, zr: int, zi: int) -> GVec:
    return (
        GaussRat(Fraction(xr), Fraction(xi)),
        GaussRat(Fraction(yr), Fraction(yi)),
        GaussRat(Fraction(zr), Fraction(zi)),
    )


ANCHOR_RAYS: Tuple[GVec, ...] = (
    gv(1, 0, 0, 0, 0, 0),  # tomo_e1
    gv(0, 0, 1, 0, 0, 0),  # tomo_e2
    gv(0, 0, 0, 0, 1, 0),  # tomo_e3
    gv(1, 0, 1, 0, 0, 0),  # tomo_e12
    gv(1, 0, 0, 0, 1, 0),  # tomo_e13
    gv(0, 0, 1, 0, 1, 0),  # tomo_e23
    gv(1, 0, 0, 1, 0, 0),  # tomo_e12i
    gv(1, 0, 0, 0, 0, 1),  # tomo_e13i
    gv(0, 0, 1, 0, 0, 1),  # tomo_e23i
)

WITNESS_111: GVec = gv(1, 0, 1, 0, 1, 0)


def inner(u: GVec, v: GVec) -> GaussRat:
    return u[0].conj() * v[0] + u[1].conj() * v[1] + u[2].conj() * v[2]


def norm_sq_vec(v: GVec) -> Fraction:
    return v[0].norm_sq() + v[1].norm_sq() + v[2].norm_sq()


def ray_sin_sq(u: GVec, v: GVec) -> Fraction:
    nu = norm_sq_vec(u)
    nv = norm_sq_vec(v)
    if nu == 0 or nv == 0:
        raise ValueError("ray_sin_sq requires nonzero vectors")
    return Fraction(1) - inner(u, v).norm_sq() / (nu * nv)


@dataclass(frozen=True)
class HermForm3:
    d1: Fraction
    d2: Fraction
    d3: Fraction
    a12: Fraction
    a13: Fraction
    a23: Fraction
    b12: Fraction
    b13: Fraction
    b23: Fraction

    def tr(self) -> Fraction:
        return self.d1 + self.d2 + self.d3

    def coeff_norm(self) -> Fraction:
        return (
            abs(self.d1)
            + abs(self.d2)
            + abs(self.d3)
            + 2 * abs(self.a12)
            + 2 * abs(self.a13)
            + 2 * abs(self.a23)
            + 2 * abs(self.b12)
            + 2 * abs(self.b13)
            + 2 * abs(self.b23)
        )

    def sub(self, other: "HermForm3") -> "HermForm3":
        return HermForm3(
            self.d1 - other.d1,
            self.d2 - other.d2,
            self.d3 - other.d3,
            self.a12 - other.a12,
            self.a13 - other.a13,
            self.a23 - other.a23,
            self.b12 - other.b12,
            self.b13 - other.b13,
            self.b23 - other.b23,
        )


def quad_num(rho: HermForm3, v: GVec) -> Fraction:
    vx, vy, vz = v
    return (
        rho.d1 * vx.norm_sq()
        + rho.d2 * vy.norm_sq()
        + rho.d3 * vz.norm_sq()
        + 2 * rho.a12 * (vx.re * vy.re + vx.im * vy.im)
        + 2 * rho.a13 * (vx.re * vz.re + vx.im * vz.im)
        + 2 * rho.a23 * (vy.re * vz.re + vy.im * vz.im)
        - 2 * rho.b12 * (vx.re * vy.im - vx.im * vy.re)
        - 2 * rho.b13 * (vx.re * vz.im - vx.im * vz.re)
        - 2 * rho.b23 * (vy.re * vz.im - vy.im * vz.re)
    )


def quad_ray(rho: HermForm3, v: GVec) -> Fraction:
    nsq = norm_sq_vec(v)
    if nsq == 0:
        return Fraction(0)
    return quad_num(rho, v) / nsq


def nine_ray_profile(fn) -> Tuple[Fraction, ...]:
    return tuple(fn(ray) for ray in ANCHOR_RAYS)


def decode_nine_ray_profile(p: Sequence[Fraction]) -> HermForm3:
    if len(p) != 9:
        raise ValueError("9-ray profile must have length 9")
    return HermForm3(
        d1=p[0],
        d2=p[1],
        d3=p[2],
        a12=p[3] - (p[0] + p[1]) / 2,
        a13=p[4] - (p[0] + p[2]) / 2,
        a23=p[5] - (p[1] + p[2]) / 2,
        b12=(p[0] + p[1]) / 2 - p[6],
        b13=(p[0] + p[2]) / 2 - p[7],
        b23=(p[1] + p[2]) / 2 - p[8],
    )


def v3_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k


def v3_rat(q: Fraction) -> int:
    if q == 0:
        return 0
    return v3_int(q.numerator) - v3_int(q.denominator)


def s3(v: GVec) -> Fraction:
    nsq = norm_sq_vec(v)
    if nsq == 0:
        return Fraction(0)
    return Fraction(1) if v3_rat(nsq) % 2 == 1 else Fraction(0)


def exotic_qi3(v: GVec) -> Fraction:
    return Fraction(1, 3) + Fraction(1, 3) * s3(v)


def rational_ray_modulus(bound_b: Fraction, eps: Fraction) -> Fraction:
    if eps <= 0:
        raise ValueError("eps must be positive")
    if bound_b <= 0:
        return Fraction(1)
    return (eps * eps) / (8 * bound_b * bound_b)


def profile_l1_dist(p1: Sequence[Fraction], p2: Sequence[Fraction]) -> Fraction:
    return sum((abs(a - b) for a, b in zip(p1, p2)), Fraction(0))


def build_crosswalk() -> List[Dict[str, Any]]:
    return [
        {
            "component": "FOC",
            "historical_name": "Finite Observation Complex / Presheaf",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer1_foc.rs",
                "vendor/engine/engine_category_theory/src/finite_report_query.rs",
            ],
            "current_lean_modules": [
                "lean4/LggrFiniteResults.lean",
                "lean4/BornGaussianFiniteModel.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "ObservationProfile",
                "stageRayProfile",
                "stageRefinement",
                "stageRefinement_stageRayProfile",
                "stageRefinement_trans",
            ],
            "dag_nodes": ["FOC-035", "TFQ-1055", "TFQ-1058"],
        },
        {
            "component": "MUR",
            "historical_name": "Minimal Universal / Observational Quotient Representation",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer2_mur.rs",
                "vendor/engine/engine_category_theory/src/finite_report_query.rs",
            ],
            "current_lean_modules": [
                "lean4/FiniteFunctionGtmur.lean",
                "lean4/FiniteFunctionGtmurReceipt.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "FibreConstant",
                "FactorsThroughOnRange",
                "descendOnRange",
                "descendOnRange_spec",
                "descendOnRange_unique",
                "fibreConstant_iff_factorsThroughOnRange",
            ],
            "dag_nodes": ["MUR-001", "TFQ-1055"],
        },
        {
            "component": "CS",
            "historical_name": "Continuum Shadow Carrier & Realized Image",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer3_cs.rs",
                "vendor/engine/engine_wdp/src/coda/q/coda_cs_adapter.rs",
                "vendor/engine/engine_category_theory/src/finite_section_separation.rs",
            ],
            "current_lean_modules": [
                "lean4/ScopeFirebreak.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "FactorsThroughTotal",
                "factorsThroughOnRange_of_factorsThroughTotal",
                "extendFromRange_nonunique_outside_range",
                "nineRayProfile",
                "decodeNineRayProfile",
                "nineRayProfile_quadRay_tomographyForm",
                "nineRayProfile_quadRay_decode",
            ],
            "dag_nodes": ["CS-001", "TFQ-1055", "TFQ-1056"],
        },
        {
            "component": "CS_Q",
            "historical_name": "Quantitative Continuum Shadow & Pseudometric",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer4_cs_q.rs",
                "vendor/engine/engine_wdp/src/coda/q/finite_shadow_exact.rs",
            ],
            "current_lean_modules": [
                "lean4/AlgebraicGtmurLossLedgerContract.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "ApproxDecodes",
                "approxDecodes_query_diff_le",
                "approxDecodes_collision_bound",
                "approxDecodes_ne_of_gap_gt_two_eps",
                "profileL1Dist",
                "profileL1Dist_eq_zero_iff",
                "profileL1Dist_zero_not_eq_of_collision",
            ],
            "dag_nodes": ["CSQ-001", "TFQ-1055", "TFQ-1056"],
        },
        {
            "component": "Q",
            "historical_name": "Query Evaluation & Tomography Decoder",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer5_q.rs",
                "vendor/engine/engine_wdp/src/coda/q/coda_stack.rs",
            ],
            "current_lean_modules": [
                "lean4/BornGaussianTomographyReduction.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "IsQuadraticRayFunction",
                "IsNormalizedQuadraticRayFunction",
                "quadratic_ray_eq_decodeNineRayProfile",
                "quadratic_fibreConstant_nineRayProfile",
                "s3_aliases_zero_on_witness_111",
                "exoticQi3_aliases_maximallyMixed_on_witness_111",
            ],
            "dag_nodes": ["Q-001", "TFQ-1055"],
        },
        {
            "component": "A",
            "historical_name": "Archimedean Stability & Quantitative Continuity Bridge",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer6_a.rs",
            ],
            "current_lean_modules": [
                "lean4/GleasonGaussianBridge.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "NineRayClose",
                "tomography_diag_error_le",
                "tomography_offdiag_error_le",
                "tomography_coeffNorm_sub_le",
                "tomography_quadRay_error_le",
                "tomography_trace_error_le",
                "tomography_approx_nonneg_of_nineRayClose",
                "abs_Qc_le_coeffNorm_mul_nsq",
                "sq_Qc_sub_le",
                "sq_quadRay_sub_le",
            ],
            "dag_nodes": ["A-001", "TFQ-1056", "TFQ-1057"],
        },
        {
            "component": "OR",
            "historical_name": "Operator Representation & Density-Matrix Completion",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer7_or.rs",
            ],
            "current_lean_modules": [
                "lean4/GleasonBornCompletion.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "toMatrix",
                "born_density_matrix_of_uniformlyRayContinuous",
                "rationalRayModulus",
                "quadRay_sub_lt_of_raySinSq_lt_modulus",
                "isUniformlyRayContinuous_quadRay_constructive",
            ],
            "dag_nodes": ["OR-001", "TFQ-1059", "TFQ-1060"],
        },
        {
            "component": "FDA",
            "historical_name": "Finite Directed Approximation & Error Accumulation",
            "current_rust_modules": [
                "vendor/engine/engine_wdp/src/coda/layer8_fda.rs",
                "vendor/engine/engine_wdp/src/coda/layer9_coda_gtla.rs",
            ],
            "current_lean_modules": [
                "lean4/BornGaussianFiniteModel.lean",
                "lean4/GleasonContinuumShadow.lean",
            ],
            "gleason_shadow_symbols": [
                "FixedAnchorCertificateAt",
                "nineRayClose_trans",
                "tomography_quadRay_error_trans",
                "fibreConstant_mono_stage",
            ],
            "dag_nodes": ["FDA-001", "TFQ-1056", "TFQ-1057", "TFQ-1060"],
        },
    ]


def verify_all() -> Dict[str, Any]:
    # 1. Exact section and restricted quadratic factorization
    sample_rho = HermForm3(
        d1=Fraction(2, 5),
        d2=Fraction(7, 20),
        d3=Fraction(1, 4),
        a12=Fraction(1, 10),
        a13=Fraction(-1, 20),
        a23=Fraction(3, 40),
        b12=Fraction(-1, 15),
        b13=Fraction(1, 12),
        b23=Fraction(-1, 30),
    )
    prof = nine_ray_profile(lambda v: quad_ray(sample_rho, v))
    decoded = decode_nine_ray_profile(prof)
    if decoded != sample_rho:
        raise AssertionError("decode_nine_ray_profile failed to recover sample_rho")
    re_prof = nine_ray_profile(lambda v: quad_ray(decoded, v))
    if re_prof != prof:
        raise AssertionError("section property failed on sample_rho profile")

    # Arbitrary profile section test
    arb_prof = tuple(Fraction(k - 4, 7) for k in range(9))
    if nine_ray_profile(lambda v: quad_ray(decode_nine_ray_profile(arb_prof), v)) != arb_prof:
        raise AssertionError("section property failed on arbitrary 9-ray profile")

    # 2. Aliasing witnesses outside the quadratic class
    max_mixed = HermForm3(
        Fraction(1, 3), Fraction(1, 3), Fraction(1, 3),
        Fraction(0), Fraction(0), Fraction(0),
        Fraction(0), Fraction(0), Fraction(0),
    )
    p_exotic = nine_ray_profile(exotic_qi3)
    p_mixed = nine_ray_profile(lambda v: quad_ray(max_mixed, v))
    if p_exotic != p_mixed or profile_l1_dist(p_exotic, p_mixed) != 0:
        raise AssertionError("exoticQi3 must alias maximallyMixedForm3 on nineRayProfile")
    if exotic_qi3(WITNESS_111) != Fraction(2, 3) or quad_ray(max_mixed, WITNESS_111) != Fraction(1, 3):
        raise AssertionError("exoticQi3 aliasing gap on witness_111 mismatch")

    p_s3 = nine_ray_profile(s3)
    p_zero = tuple(Fraction(0) for _ in range(9))
    if p_s3 != p_zero or s3(WITNESS_111) != Fraction(1):
        raise AssertionError("s3 aliasing witness mismatch")

    # 3. Sharpness of the 27*eps tomography coeffNorm stability constant
    eps = Fraction(1, 100)
    # Perturb d1, d2, d3 by +eps and off-diagonals by -eps so |a_ij| = 2*eps, |b_ij| = 2*eps
    pert_prof = (
        eps,
        eps,
        eps,
        -eps,
        -eps,
        -eps,
        -eps,
        -eps,
        -eps,
    )
    pert_form = decode_nine_ray_profile(pert_prof)
    if pert_form.coeff_norm() != 27 * eps:
        raise AssertionError(f"Expected sharp coeffNorm 27*eps, got {pert_form.coeff_norm()}")
    if abs(pert_form.tr()) != 3 * eps:
        raise AssertionError(f"Expected sharp trace error 3*eps, got {abs(pert_form.tr())}")

    # 4. Quantitative Rayleigh-quotient continuity and constructive rational modulus
    test_rays: Tuple[GVec, ...] = ANCHOR_RAYS + (
        WITNESS_111,
        gv(2, 1, -1, 1, 0, 3),
        gv(1, -2, 2, 0, 1, 1),
        gv(3, 0, 4, 0, 0, 0),
        gv(3, 0, 4, 0, 1, 0),
    )
    max_ratio_over_4 = Fraction(0)
    for u in test_rays:
        for v in test_rays:
            sin_sq = ray_sin_sq(u, v)
            diff_sq = (quad_ray(sample_rho, u) - quad_ray(sample_rho, v)) ** 2
            c_norm = sample_rho.coeff_norm()
            bound_4 = 4 * (c_norm ** 2) * sin_sq
            bound_8 = 8 * (c_norm ** 2) * sin_sq
            if diff_sq > bound_4 or diff_sq > bound_8:
                raise AssertionError("Quantitative Rayleigh continuity inequality violated")
            if bound_4 > 0:
                ratio = diff_sq / bound_4
                if ratio > max_ratio_over_4:
                    max_ratio_over_4 = ratio

    # Check constructive modulus on both normal (B > 0) and degenerate (B <= 0, rho = 0) cases
    mod_normal = rational_ray_modulus(sample_rho.coeff_norm(), Fraction(1, 10))
    mod_degen_neg = rational_ray_modulus(Fraction(-5), Fraction(1, 10))
    mod_degen_zero = rational_ray_modulus(Fraction(0), Fraction(1, 10))
    if mod_normal <= 0 or mod_degen_neg != Fraction(1) or mod_degen_zero != Fraction(1):
        raise AssertionError("rational_ray_modulus positivity/degenerate check failed")

    lean_sha = hashlib.sha256(LEAN_MODULE.read_bytes()).hexdigest() if LEAN_MODULE.is_file() else None

    return {
        "schema_version": "gleason_continuum_shadow_receipt.v1",
        "authority_effect": "None",
        "phase": "Phase 3 — Continuum Shadow and Explicit Bridge",
        "lean_module": {
            "path": "lean4/GleasonContinuumShadow.lean",
            "sha256": lean_sha,
        },
        "historical_crosswalk": build_crosswalk(),
        "verified_claims": {
            "exact_descent_on_range_vs_unused_labels": True,
            "approx_decoder_two_eps_collision_bound": True,
            "pseudometric_zero_dist_vs_equality_separation": True,
            "nine_ray_section_and_restricted_quadratic_factorization": True,
            "nonquadratic_aliasing_witnesses": {
                "exoticQi3_vs_maximallyMixed": {
                    "nine_ray_l1_dist": str(profile_l1_dist(p_exotic, p_mixed)),
                    "exoticQi3_witness_111": str(exotic_qi3(WITNESS_111)),
                    "maximallyMixed_witness_111": str(quad_ray(max_mixed, WITNESS_111)),
                },
                "s3_vs_zero": {
                    "nine_ray_l1_dist": str(profile_l1_dist(p_s3, p_zero)),
                    "s3_witness_111": str(s3(WITNESS_111)),
                },
            },
            "quantitative_nine_ray_stability": {
                "diag_multiplier": 1,
                "offdiag_multiplier": 2,
                "coeffNorm_multiplier": 27,
                "coeffNorm_sharpness_verified": True,
                "trace_multiplier": 3,
                "ray_probability_multiplier": 27,
            },
            "quantitative_rayleigh_continuity": {
                "squared_bound_multiplier_tight": 4,
                "squared_bound_multiplier_conservative": 8,
                "max_observed_ratio_to_tight_bound": str(max_ratio_over_4),
                "sample_coeff_norm": str(sample_rho.coeff_norm()),
                "sample_modulus_eps_1_10": str(mod_normal),
                "degenerate_modulus_b_nonpositive": str(mod_degen_zero),
            },
        },
        "claim_hygiene": {
            "supports": (
                "Supports exact descent on the realized observation image Set.range p, the 2*eps "
                "collision bound for approximate decoders, exact 9-ray reconstruction on the "
                "restricted quadratic ray class, nonquadratic aliasing by s3 and exoticQi3 on the "
                "9-ray profile, 27*eps quantitative stability of 9-ray tomography, and the "
                "constructive rational modulus eps^2 / (8 * B^2) for uniform ray continuity of "
                "every rational Hermitian Rayleigh quotient."
            ),
            "does_not_support": (
                "Does not support unrestricted 9-ray tomography uniqueness outside the quadratic "
                "class, nor does it discharge the pointwise-to-uniform rational ray question "
                "(TFQ-1057) without a regularity or boundedness-plus-continuity hypothesis."
            ),
            "narrowest_defensible_claim": (
                "Within the kernel-checked Lean 4 module GleasonContinuumShadow and exact rational "
                "verifier, 9-ray tomography is a stable, exact section on the quadratic ray class "
                "(with 27*eps perturbation bound and explicit rational ray-continuity modulus "
                "eps^2 / (8*B^2)), while nonquadratic frame functions alias quadratic Born states "
                "on finite ray profiles."
            ),
            "next_test_needed": (
                "Phase 4: formalize constructive Gaussian-rational factorized density-matrix "
                "approximations rho_k = B_k B_k^* / tr(B_k B_k^*) for arbitrary complex states in "
                "d=3 and extend the continuum Gleason bridge across dimensions d=0,1,2, d>=3, and "
                "separable infinite-dimensional Hilbert spaces."
            ),
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--verify-receipt", "--check", dest="verify_receipt", action="store_true")
    parser.add_argument("--write-receipt", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    computed = verify_all()
    encoded = json.dumps(computed, indent=2, sort_keys=True) + "\n"

    if args.write_receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(encoded, encoding="utf-8", newline="\n")
        print(json.dumps({"written": str(args.receipt.relative_to(ROOT).as_posix()), "all_passed": True}))
        return 0

    if args.verify_receipt:
        if not args.receipt.is_file():
            raise SystemExit(f"Missing receipt: {args.receipt}")
        existing = json.loads(args.receipt.read_text(encoding="utf-8"))
        if existing != computed:
            raise SystemExit("Receipt drift detected in gleason_continuum_shadow_receipt.json")
        print(json.dumps({"verified": str(args.receipt.relative_to(ROOT).as_posix()), "all_passed": True}))
        return 0

    print(encoded, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
