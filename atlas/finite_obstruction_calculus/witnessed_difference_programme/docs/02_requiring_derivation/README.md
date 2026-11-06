# Quadrant 2: Open Derivations, Conjectures & Research Targets

**Dimension 2 (Requires Derivation)**: This directory collects active research targets, unclosed mathematical conjectures, partially verified formulations, and open proof obligations across the Witnessed Difference Programme.

## Epistemic Posture
Nothing in this quadrant is claimed as a proven theorem. Automated tooling and human investigators MUST treat every document in this directory as an open conjecture or unverified target.

## Active Research Clusters

### 1. The Five Outstanding Derivation Targets (`five_outstanding_derivations.md`)
Records the 5 derivation targets bridging finite obstruction calculus to physical operational systems (with all finite theorems mechanized in `WdpBatch2.lean` and `WdpBatch3.lean`, and external physical/institutional components remaining open):
- **Target 1 (`TFQ-0571` — Finite Proof Discharged):** Sharp Observer Completion with Distinct Realization and Repair Images (`WdpBatch2.lean::sharp_observer_completion_formula_gen_wdp_70`; physical laboratory repair actuation `O02` remains open).
- **Target 2 (`TFQ-0572`, `TFQ-0568` — Finite Proof Discharged):** Coherence inside Guarded Five-Edit Model Swap Components (`WdpBatch3.lean::star_shaped_swap_complex_connected`, `WdpBatch6.lean::guarded_3cube_all_six_paths_equal`; global infinite-history site remains open).
- **Target 3 (`TFQ-0573` — Finite Proof Discharged):** Minimum-Cost Realizable Observation for Future Operations (`WdpBatch3.lean::eight_state_realizable_observation_gen_wdp_71`; physical laboratory instrument realization outside declared tables remains open).
- **Target 4 (`TFQ-0574`, `TFQ-0570` — Finite Proof Discharged):** Rejection-Rule Reuse across Changing Representations and Tasks (`WdpBatch3.lean::reuse_soundness_iff`, `reuse_coverage_iff`; external institutional grant jurisdiction `O05` remains open).
- **Target 5 (`TFQ-0575` — Finite Proof Discharged):** Future-Faithful Native Five-Edit Model Compression (`WdpBatch3.lean::general_horizon_clipped_signed_counts_unique`, `general_horizon_sharp_collision`; unrestricted source/world correspondence remains open).

### 2. Meron Field-Limit Continuum Targets (`meron_field_limit_derivations/`)
Collects research notes on non-perturbative Euclidean spacetime field limits (Targets M4 `TFQ-0585` and M5 `TFQ-0586` have finite $\mathbb{Z}_2$ plaquette and $2 \times 2$ toric-code completions in `WdpBatch6.lean`; continuum Targets M1–M3 `TFQ-0582..0584` and `TFQ-0587` remain open):
- `meron_field_limit_derivations/README.md`: Index of Targets M1–M5.
- `meron_analytic_response.md`: Analytic response bounds.
- `meron_coda_continuum_bridge.md`: Bridge from discrete cochains to continuum fields.
- `meron_euclidean_covariance_positivity.md`: Reflection positivity and Euclidean covariance.
- `meron_euclidean_thermodynamic_limit.md`: Thermodynamic limit estimates.
- `meron_source_field_response.md`, `meron_spatial_gaussian_source.md`: Gaussian field response.
- `meron_spin_and_observable_transport.md`: Spin transport bounds.
- `meron_time_and_volume_refinement.md`, `meron_time_dependent_analyticity.md`: Time-dependent analyticity.
- `open_derivations/meron_spacetime_limit/`: In-progress proof draft (`meron_spacetime_proof.md`) and computational checks (`meron_spacetime_finite_checks.py`).

### 3. Affine Support Noise Thickening (`affine_thickening_conjecture.md`)
Formalizes the question of constructing recovery cost witnesses for affine supports thickened by bounded independent measurement error $\varepsilon > 0$. The finite 1D rational interval cell partition, `ABSTAIN_NO_RULE` boundary soundness, and dyadic covering bound (`TFQ-0581`) are mechanized in `WdpBatch6.lean`; higher-dimensional and continuum measure extensions remain open.

### 4. WD2 Distinction Carrier General Proofs (`wd2_open_targets.md`)
All 6 general Lean 4 formalization targets for finite Moore machine distinguishability (`TFQ-0559`, `TFQ-0561..0565`) are now discharged in `lean4/WitnessedDifference/FiniteDistinction.lean`:
- `WD2-DERIV-01` (`TFQ-0559`): Word kernel representation lemma (`Wd2.word_kernel_agreement`, `Wd2.poly_word_kernel_agreement`).
- `WD2-DERIV-02` (`TFQ-0561`): General pigeonhole stabilization bound (`Wd2.stabilization_horizon_le_card_sub_b0`, `Wd2.sharp_chain_general_witness`).
- `WD2-DERIV-03` (`TFQ-0562`): No-escape four-way characterization (`Wd2.no_escape_equivalence`, `Wd2.isUpdateCongruence_iff_r1_eq_r0`).
- `WD2-DERIV-04` (`TFQ-0563`): Shortest separating word length (`Wd2.shortest_separating_word`).
- `WD2-DERIV-05` (`TFQ-0564`): Report factorization preservation (`Wd2.factored_report_preserves_related`, `Wd2.unfactored_report_splits_r0`).
- `WD2-DERIV-06` (`TFQ-0565`): Universal Nerode/Moore coarsest quotient mapping (`Wd2.rInfinity_coarsest_congruence`, `Wd2.minimal_deterministic_quotient_factorization`).
