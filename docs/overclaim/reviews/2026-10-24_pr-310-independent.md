# Independent review of PR #310

Scope: original head c33626590fe0bdd3977f82d0251890267f83020f. Exact source lean4/CampaignFspWittenIndexInvariance.lean, SHA-256 6935af1b664bfdfcaebc654abe377c8b99414758b128c692e40c4902db40183b.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

For arbitrary finite rectangular matrix blocks over a commutative ring, positive-power block traces agree and the graded supertrace vanishes. The cubic polynomial follows. The paired-list model explicitly subtracts each weight from itself; it does not derive spectral pairing. B is independent of A and is not proved to be its adjoint. Zero-mode counts are supplied; the rectangular vector may be zero at a=b=0. There is no analytic exponential, ground-state existence proof, or sign-free sampler.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspWittenIndexInvariance.lean:46 susyHamiltonian_eq_fromBlocks` | `{nB nF R : Type*} [Fintype nB] [Fintype nF] [CommRing R] (A : Matrix nF nB R) (B : Matrix nB nF R) : susyHamiltonian A B = fromBlocks (B * A) 0 0 (A * B)` |
| `lean4/CampaignFspWittenIndexInvariance.lean:53 boson_fermion_block_pow_intertwine` | `{nB nF R : Type*} [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R] (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) : (B * A) ^ (k + 1) = B * (A * B) ^ k * A` |
| `lean4/CampaignFspWittenIndexInvariance.lean:68 susyHamiltonian_pow_eq_fromBlocks` | `{nB nF R : Type*} [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R] (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) : (susyHamiltonian A B) ^ k = fromBlocks ((B * A) ^ k) 0 0 ((A * B) ^ k)` |
| `lean4/CampaignFspWittenIndexInvariance.lean:80 boson_eq_fermion_pow_succ_trace` | `{nB nF R : Type*} [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R] (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) : trace ((B * A) ^ (k + 1)) = trace ((A * B) ^ (k + 1))` |
| `lean4/CampaignFspWittenIndexInvariance.lean:93 supertrace_susyHamiltonian_pow_succ_eq_zero` | `{nB nF R : Type*} [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R] (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) : trace (fermionParity nB nF R * (susyHamiltonian A B) ^ (k + 1)) = 0` |
| `lean4/CampaignFspWittenIndexInvariance.lean:108 supertrace_fermionParity_fin_eq_sub` | `(nB nF : ℕ) {R : Type*} [CommRing R] : trace (fermionParity (Fin nB) (Fin nF) R) = (nB : R) - (nF : R)` |
| `lean4/CampaignFspWittenIndexInvariance.lean:113 supertrace_cubic_boltzmann_poly_independent_of_beta` | `{nB nF : ℕ} {R : Type*} [CommRing R] (A : Matrix (Fin nF) (Fin nB) R) (B : Matrix (Fin nB) (Fin nF) R) (c0 c1 c2 c3 : R) : let H := susyHamiltonian A B let Γ := fermionParity (Fin nB) (Fin nF) R trace (Γ * (c0 • (1 : Matrix (Fin nB ⊕ Fin nF) (Fin nB ⊕ Fin nF) R) + c1 • H + c2 • (H ^ 2) + c3 • (H ^ 3))) = c0 * ((nB : R) - (nF : R))` |
| `lean4/CampaignFspWittenIndexInvariance.lean:146 wittenIndexPaired_eq_zero_mode_diff_for_all_weights` | `(nB0 nF0 : ℕ) (weights : List ℚ) : wittenIndexPaired nB0 nF0 weights = (nB0 : ℚ) - (nF0 : ℚ)` |
| `lean4/CampaignFspWittenIndexInvariance.lean:156 nonzero_witten_index_implies_zero_mode_ground_state` | `(nB0 nF0 : ℕ) (weights : List ℚ) (hW : wittenIndexPaired nB0 nF0 weights ≠ 0) : 0 < nB0 + nF0` |
| `lean4/CampaignFspWittenIndexInvariance.lean:171 rectangular_2x1_supercharge_forced_zero_mode_and_index_one` | `(a b : ℚ) : let A := rect2x1Block a b trace (Aᵀ * A) = a ^ 2 + b ^ 2 ∧ trace (A * Aᵀ) = a ^ 2 + b ^ 2 ∧ (A.mulVec ![-b, a]) 0 = 0 ∧ ((Aᵀ * A).mulVec ![-b, a]) 0 = 0 ∧ ((Aᵀ * A).mulVec ![-b, a]) 1 = 0 ∧ trace (fermionParity (Fin 2) (Fin 1) ℚ) = 1` |
| `lean4/CampaignFspWittenIndexInvariance.lean:197 witten_index_vs_partition_function_and_average_sign_fence` | `(nB0 nF0 : ℕ) (w1 w2 : ℚ) (hw1 : 0 < w1) (hw2 : 0 < w2) : wittenIndexPaired nB0 nF0 [w1, w2] = (nB0 : ℚ) - (nF0 : ℚ) ∧ partitionFunctionPaired nB0 nF0 [w1, w2] = (nB0 : ℚ) + (nF0 : ℚ) + 2 * (w1 + w2) ∧ (nB0 : ℚ) + (nF0 : ℚ) < partitionFunctionPaired nB0 nF0 [w1, w2] ∧ wittenIndexPaired nB0 nF0 [w1, w2] < partitionFunctionPaired nB0 nF0 [w1, w2]` |
| `lean4/CampaignFspWittenIndexInvariance.lean:211 broken_lattice_susy_destroys_supertrace_cancellation_fence` | `{nB nF R : Type*} [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R] (A : Matrix nF nB R) (B : Matrix nB nF R) (Δ : Matrix nF nF R) : trace (fermionParity nB nF R * fromBlocks (B * A) 0 0 (A * B + Δ)) = -trace Δ` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_310_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
