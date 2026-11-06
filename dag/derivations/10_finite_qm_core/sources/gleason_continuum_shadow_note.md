# Phase 3 Research Note: The Gleason Continuum Shadow and Its Explicit Bridge

AuthorityEffect: None.

## 1. Purpose and Scope

This document records the Phase 3 formalization of the Gleason continuum-shadow model in
[`lean4/GleasonContinuumShadow.lean`](../../lean4/GleasonContinuumShadow.lean) and its exact rational
verifier [`scripts/verify_gleason_continuum_shadow.py`](../../scripts/verify_gleason_continuum_shadow.py)
(receipt: [`evidence/lean_receipts/gleason_continuum_shadow_receipt.json`](gleason_continuum_shadow_receipt.json)).

It establishes:
1. A complete crosswalk between the historical eight-layer continuum-shadow spine
   (`FOC`, `MUR`, `CS`, `CS_Q`, `Q`, `A`, `OR`, `FDA`) and the current repository's Rust modules,
   Lean 4 modules, and derivation DAG nodes.
2. Kernel-checked Lean 4 theorems separating:
   - exact descent on the realized observation image `Set.range p` (`fibreConstant_iff_factorsThroughOnRange`, `descendOnRange_unique`) from non-unique extensions on unrealized observation labels (`extendFromRange_nonunique_outside_range`);
   - approximate decoder collision bounds (`|q x - q y| ≤ 2 * ε` when `p x = p y`) and `ℓ¹` observation-pseudometric vanishing (`profileL1Dist p x y = 0 ↔ p x = p y`) from carrier or off-support query equality (`profileL1Dist_zero_not_eq_of_collision`);
   - exact 9-ray tomography reconstruction on the restricted quadratic ray class (`quadratic_ray_eq_decodeNineRayProfile`, `quadratic_fibreConstant_nineRayProfile`) from explicit nonquadratic frame-function aliasing (`exoticQi3_aliases_maximallyMixed_on_witness_111`, `s3_aliases_zero_on_witness_111`).
3. Quantitative 9-ray tomography stability under anchorwise `ε`-perturbations (`NineRayClose f g ε`),
   with sharp coefficient norm bound `27 * ε`, ray-probability stability `≤ 27 * ε`, trace stability
   `≤ 3 * ε`, approximate positivity lower bound `≥ -27 * ε`, and additive multi-stage error accumulation.
4. Quantitative Rayleigh-quotient continuity on `ℂ³` and `ℚ(i)³`:
   - `|Qc ρ v| ≤ (ρ.coeffNorm : ℝ) * nsq v` for all `v ∈ ℂ³`;
   - `(Qc ρ x - Qc ρ y)² ≤ (ρ.coeffNorm : ℝ)² * nsq (x - y) * nsq (x + y)` for all `x, y ∈ ℂ³`;
   - `(quadRay ρ u - quadRay ρ v)² ≤ 4 * ρ.coeffNorm² * raySinSq u v ≤ 8 * ρ.coeffNorm² * raySinSq u v` for all nonzero `u, v ∈ ℚ(i)³`;
   - `|(quadRay ρ u : ℝ) - (quadRay ρ v : ℝ)| ≤ 2 * (ρ.coeffNorm : ℝ) * √(raySinSq u v)`;
   - an explicit rational modulus `rationalRayModulus B ε := if B ≤ 0 then 1 else ε² / (8 * B²)` yielding a purely algebraic, constructive proof `isUniformlyRayContinuous_quadRay_constructive` of `IsUniformlyRayContinuous (quadRay ρ)` without invoking compactness of the complex unit sphere.

---

## 2. Historical-to-Current Crosswalk (`FOC / MUR / CS / CS_Q / Q / A / OR / FDA`)

| Component | Meaning | Current Rust Modules | Current Lean 4 Modules | Gleason Continuum-Shadow Specializations (`GleasonContinuumShadow.lean`) | DAG Nodes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`FOC`** | Finite Observation Complex / Presheaf | `vendor/engine/engine_wdp/src/coda/layer1_foc.rs`, `vendor/engine/engine_category_theory/src/finite_report_query.rs` | `lean4/LggrFiniteResults.lean`, `lean4/BornGaussianFiniteModel.lean`, `lean4/GleasonContinuumShadow.lean` | `ObservationProfile`, `stageRayProfile`, `stageRefinement`, `stageRefinement_stageRayProfile`, `stageRefinement_trans` | `FOC-035`, `TFQ-1055`, `TFQ-1058` |
| **`MUR`** | Minimal Universal / Observational Quotient | `vendor/engine/engine_wdp/src/coda/layer2_mur.rs`, `vendor/engine/engine_category_theory/src/finite_report_query.rs` | `lean4/FiniteFunctionGtmur.lean`, `lean4/FiniteFunctionGtmurReceipt.lean`, `lean4/GleasonContinuumShadow.lean` | `FibreConstant`, `FactorsThroughOnRange`, `descendOnRange`, `descendOnRange_spec`, `descendOnRange_unique`, `fibreConstant_iff_factorsThroughOnRange` | `MUR-001`, `TFQ-1055` |
| **`CS`** | Continuum Shadow Carrier & Realized Image | `vendor/engine/engine_wdp/src/coda/layer3_cs.rs`, `vendor/engine/engine_wdp/src/coda/q/coda_cs_adapter.rs`, `vendor/engine/engine_category_theory/src/finite_section_separation.rs` | `lean4/ScopeFirebreak.lean`, `lean4/GleasonContinuumShadow.lean` | `FactorsThroughTotal`, `factorsThroughOnRange_of_factorsThroughTotal`, `extendFromRange_nonunique_outside_range`, `nineRayProfile`, `decodeNineRayProfile`, `nineRayProfile_quadRay_tomographyForm`, `nineRayProfile_quadRay_decode` | `CS-001`, `TFQ-1055`, `TFQ-1056` |
| **`CS_Q`** | Quantitative Continuum Shadow & Pseudometric | `vendor/engine/engine_wdp/src/coda/layer4_cs_q.rs`, `vendor/engine/engine_wdp/src/coda/q/finite_shadow_exact.rs` | `lean4/AlgebraicGtmurLossLedgerContract.lean`, `lean4/GleasonContinuumShadow.lean` | `ApproxDecodes`, `approxDecodes_query_diff_le`, `approxDecodes_collision_bound`, `approxDecodes_ne_of_gap_gt_two_eps`, `profileL1Dist`, `profileL1Dist_eq_zero_iff`, `profileL1Dist_zero_not_eq_of_collision` | `CSQ-001`, `TFQ-1055`, `TFQ-1056` |
| **`Q`** | Query Evaluation & Tomography Decoder | `vendor/engine/engine_wdp/src/coda/layer5_q.rs`, `vendor/engine/engine_wdp/src/coda/q/coda_stack.rs` | `lean4/BornGaussianTomographyReduction.lean`, `lean4/GleasonContinuumShadow.lean` | `IsQuadraticRayFunction`, `IsNormalizedQuadraticRayFunction`, `quadratic_ray_eq_decodeNineRayProfile`, `quadratic_fibreConstant_nineRayProfile`, `s3_aliases_zero_on_witness_111`, `exoticQi3_aliases_maximallyMixed_on_witness_111` | `Q-001`, `TFQ-1055` |
| **`A`** | Archimedean Stability & Continuity Bridge | `vendor/engine/engine_wdp/src/coda/layer6_a.rs` | `lean4/GleasonGaussianBridge.lean`, `lean4/GleasonContinuumShadow.lean` | `NineRayClose`, `tomography_diag_error_le`, `tomography_offdiag_error_le`, `tomography_coeffNorm_sub_le`, `tomography_quadRay_error_le`, `tomography_trace_error_le`, `tomography_approx_nonneg_of_nineRayClose`, `abs_Qc_le_coeffNorm_mul_nsq`, `sq_Qc_sub_le`, `sq_quadRay_sub_le` | `A-001`, `TFQ-1056`, `TFQ-1057` |
| **`OR`** | Operator Representation & Density Matrix | `vendor/engine/engine_wdp/src/coda/layer7_or.rs` | `lean4/GleasonBornCompletion.lean`, `lean4/GleasonContinuumShadow.lean` | `toMatrix`, `born_density_matrix_of_uniformlyRayContinuous`, `rationalRayModulus`, `quadRay_sub_lt_of_raySinSq_lt_modulus`, `isUniformlyRayContinuous_quadRay_constructive` | `OR-001`, `TFQ-1059`, `TFQ-1060` |
| **`FDA`** | Finite Directed Approximation & Error Accumulation | `vendor/engine/engine_wdp/src/coda/layer8_fda.rs`, `vendor/engine/engine_wdp/src/coda/layer9_coda_gtla.rs` | `lean4/BornGaussianFiniteModel.lean`, `lean4/GleasonContinuumShadow.lean` | `FixedAnchorCertificateAt`, `nineRayClose_trans`, `tomography_quadRay_error_trans`, `fibreConstant_mono_stage` | `FDA-001`, `TFQ-1056`, `TFQ-1057`, `TFQ-1060` |

---

## 3. Claim Hygiene Summary

1. **What it supports**:
   - Exact descent of fibre-constant queries to the realized observation image `Set.range p` (`fibreConstant_iff_factorsThroughOnRange`) and explicit non-uniqueness of total decoders outside `Set.range p` (`extendFromRange_nonunique_outside_range`).
   - The `2 * ε` collision bound for `ε`-approximate decoders (`approxDecodes_collision_bound`) and explicit separation between zero `ℓ¹` profile pseudometric distance and state/query equality (`profileL1Dist_zero_not_eq_of_collision`).
   - Exact 9-ray tomography section and factorization on the restricted quadratic ray class (`quadratic_ray_eq_decodeNineRayProfile`), together with explicit aliasing witnesses (`s3` and `exoticQi3`) showing that nonquadratic rational frame functions share the 9-ray profile of quadratic states while differing at `witness_111 = (1, 1, 1)`.
   - Quantitative stability of 9-ray tomography (`coeffNorm ≤ 27 * ε`, ray-probability error `≤ 27 * ε`, trace error `≤ 3 * ε`) and constructive uniform ray continuity of `quadRay ρ` with explicit rational modulus `rationalRayModulus B ε = if B ≤ 0 then 1 else ε² / (8 * B²)`.
2. **What it does not support**:
   - It does not claim that finite 9-ray tomography uniquely determines arbitrary rational frame functions outside the quadratic or uniformly continuous class.
   - It does not resolve the pointwise-to-uniform rational ray question (`TFQ-1057`) without an explicit regularity or certificate hypothesis.
3. **The narrowest defensible claim**:
   - Within the kernel-checked Lean 4 module `GleasonContinuumShadow` and exact rational verifier `verify_gleason_continuum_shadow.py`, 9-ray tomography forms an exact, `27 * ε`-stable section on the quadratic ray class with constructive rational continuity modulus `ε² / (8 * B²)`, while nonquadratic rational frame functions alias quadratic Born states on finite ray profiles.
4. **The next test needed**:
   - Phase 4: construct explicit Gaussian-rational factorized approximations `ρ_k = B_k B_k^* / tr(B_k B_k^*)` for arbitrary complex density matrices in `d = 3`, and formalize the continuum Gleason development across dimensions `d = 0, 1, 2`, `d ≥ 3`, and infinite-dimensional separable Hilbert spaces.
