# Independent review of PR #322

Scope: original head ca9f2aeed9cd0140798d76d627ed560897d8145a. Exact source lean4/CampaignFspReggeDeficitAction.lean, SHA-256 37bbdca7459fc734d959bd223bdd3655f253e32800e9d50712c37c3241c6d91e.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

The declared rational Heron polynomial is symmetric and has the displayed evaluations; a supplied rational dot product is bilinear and an additive four-step telescoping sum is zero. Schlaefli cancellation is an explicit hypothesis, not derived geometry. The face vector and its interpretation as a sphere are supplied. No edge-length geometry, noncommutative Bianchi identity, continuum refinement theorem or actual Lorentzian exponential is constructed. The -I matrix and w-w identity do not identify a gravitational phase or resolve fermion signs.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspReggeDeficitAction.lean:25 heronAreaSq_symmetric_and_orthogonal_pentatope_hinges` | `(a b c : ℚ) : heronAreaSq a b c = heronAreaSq b a c ∧ heronAreaSq a b c = heronAreaSq a c b ∧ heronAreaSq 1 1 2 = 1 / 4 ∧ heronAreaSq 2 2 2 = 3 / 4 ∧ 6 * heronAreaSq 1 1 2 + 4 * heronAreaSq 2 2 2 = 9 / 2 ∧ heronAreaSq 1 1 4 = 0` |
| `lean4/CampaignFspReggeDeficitAction.lean:49 hingeDeficit_flat_sum_zero_and_reggeAction_bilinear` | `(fullTurn : ℚ) (dihedrals : List ℚ) {n : ℕ} (areas eps1 eps2 : Fin n → ℚ) (c : ℚ) : (hingeDeficit fullTurn dihedrals = 0 ↔ dihedrals.sum = fullTurn) ∧ reggeAction areas (fun _ => 0) = 0 ∧ reggeAction areas (fun h => eps1 h + eps2 h) = reggeAction areas eps1 + reggeAction areas eps2 ∧ reggeAction (fun h => c * areas h) eps1 = c * reggeAction areas eps1` |
| `lean4/CampaignFspReggeDeficitAction.lean:64 reggeAction_positive_vs_mixed_deficit_sign` | `{n : ℕ} (areas eps : Fin n → ℚ) (hA : ∀ h, 0 ≤ areas h) (hE : ∀ h, 0 ≤ eps h) : 0 ≤ reggeAction areas eps ∧ reggeAction ![1, 1] ![1, -2] = -1 ∧ reggeAction ![1, 1] ![1, -2] < 0 ∧ reggeAction ![1, 1] ![1, -1] = 0 ∧ (![(1 : ℚ), -1] : Fin 2 → ℚ) 0 ≠ 0` |
| `lean4/CampaignFspReggeDeficitAction.lean:86 s4_boundary_delta5_face_counts_and_euler_characteristic` | `: Nat.choose 6 1 = s4BoundaryFaceVector 0 ∧ Nat.choose 6 2 = s4BoundaryFaceVector 1 ∧ Nat.choose 6 3 = s4BoundaryFaceVector 2 ∧ Nat.choose 6 4 = s4BoundaryFaceVector 3 ∧ Nat.choose 6 5 = s4BoundaryFaceVector 4 ∧ (s4BoundaryFaceVector 0 : ℤ) - s4BoundaryFaceVector 1 + s4BoundaryFaceVector 2 - s4BoundaryFaceVector 3 + s4BoundaryFaceVector 4 = 2 ∧ 6 * Nat.choose 5 3 = 20 * 3` |
| `lean4/CampaignFspReggeDeficitAction.lean:98 discrete_bianchi_cyclic_holonomy_telescoping` | `(A f0 f1 f2 f3 : ℚ) : (f1 - f0) + (f2 - f1) + (f3 - f2) + (f0 - f3) = 0 ∧ A * (f1 - f0) + A * (f2 - f1) + A * (f3 - f2) + A * (f0 - f3) = 0` |
| `lean4/CampaignFspReggeDeficitAction.lean:108 schlaefli_variation_reduces_regge_variation_to_area_term` | `{n : ℕ} (A dA eps dTheta : Fin n → ℚ) (hSchlaefli : ∑ h : Fin n, A h * dTheta h = 0) : reggeFullVariation A dA eps dTheta = reggeAction dA eps` |
| `lean4/CampaignFspReggeDeficitAction.lean:120 defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit` | `(sRegge sEh c : ℚ) : defectBoundHolds (1 / 3) (1 / 4) 2 (1 / 16) ∧ ¬ defectBoundHolds 1 0 1 (1 / 4) ∧ ¬ defectBoundHolds 1 0 (-1) 1 ∧ (defectBoundHolds sRegge sEh c 0 → sRegge = sEh)` |
| `lean4/CampaignFspReggeDeficitAction.lean:138 regge_action_independent_of_fermion_occupation_fence` | `{n : ℕ} (areas eps : Fin n → ℚ) (w : ℚ) (hw : 0 < w) : (1 : ℚ) * w > 0 ∧ (-1 : ℚ) * w < 0 ∧ (1 : ℚ) * w + (-1 : ℚ) * w = 0 ∧ reggeAction areas eps = reggeAction areas eps` |
| `lean4/CampaignFspReggeDeficitAction.lean:152 euclidean_vs_lorentzian_regge_phase_fence` | `: Matrix.trace lorentzianHalfTurnMat = -2 ∧ lorentzianHalfTurnMat * lorentzianHalfTurnMat = 1 ∧ (1 : Matrix (Fin 2) (Fin 2) ℤ) + lorentzianHalfTurnMat = 0` |
| `lean4/CampaignFspReggeDeficitAction.lean:159 flat_vertex_sum_vs_signed_cancellation_fence` | `(d1 d2 : ℕ) : (sumDeficits [d1, d2] = 0 ↔ d1 = 0 ∧ d2 = 0) ∧ ((1 : ℚ) + (-1 : ℚ) = 0 ∧ (1 : ℚ) ≠ 0 ∧ (-1 : ℚ) ≠ 0)` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_322_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
