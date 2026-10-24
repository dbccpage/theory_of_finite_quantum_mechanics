# Independent review of PR #317

Scope: original head 4cf11aa307e142a6b7ef5222a1a07e7a208af596. Exact source lean4/CampaignFspBf2GroupSignClaim.lean, SHA-256 2ecf83152cc14542336d294520b8d3e727d8b134273e05fa2421a3d5acd66843.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Explicit low-degree simplicial coboundaries on Fin 5 compose to zero and preserve the displayed curvatures under exact shifts. The ZMod 2 product cocycle is not any displayed 2-coboundary, as detected by the explicit three-term functional. Two supplied integer involutions have commutator -I. Crossed-module identity formulas reduce to reflexivity and do not construct an arbitrary crossed module. There is no identification with Wang-Levin braiding, a path integral, or a unique physical cancellation mechanism.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspBf2GroupSignClaim.lean:37 simplicial_coboundary_nilpotence_d1d0_d2d1_d3d2` | `{A : Type*} [AddCommGroup A] (c0 : Fin 5 → A) (c1 : Fin 5 → Fin 5 → A) (c2 : Fin 5 → Fin 5 → Fin 5 → A) (i j k l m : Fin 5) : d1 (d0 c0) i j k = 0 ∧ d2 (d1 c1) i j k l = 0 ∧ d3 (d2 c2) i j k l m = 0` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:49 bf_cochain_gauge_invariance` | `{A : Type*} [AddCommGroup A] (A1 : Fin 5 → Fin 5 → A) (lam : Fin 5 → A) (B2 : Fin 5 → Fin 5 → Fin 5 → A) (eta : Fin 5 → Fin 5 → A) (i j k l : Fin 5) : d1 (fun u v => A1 u v + d0 lam u v) i j k = d1 A1 i j k ∧ d2 (fun u v w => B2 u v w + d1 eta u v w) i j k l = d2 B2 i j k l` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:60 bf_z2_level_hopf_link_sign_and_weight_trichotomy` | `(q p lk w_pos w_neg : ℤ) : q * p * (-lk) = -(q * p * lk) ∧ (-1 : ℤ) ^ (1 : ℕ) = -1 ∧ (w_pos = w_neg → w_pos * 1 + w_neg * (-1) = 0) ∧ (w_pos ≠ w_neg → w_pos * 1 + w_neg * (-1) ≠ 0)` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:78 bf_z3_level_non_involution_and_cos_sum_fence` | `: omega3Mat ^ 3 = (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧ omega3Mat ^ 2 ≠ (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧ omega3Mat + omega3Mat ^ 2 = -(1 : Matrix (Fin 2) (Fin 2) ℤ) ∧ Matrix.trace (omega3Mat + omega3Mat ^ 2) = -2` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:107 wang_levin_ising_commutator_negative_trace_and_abelian_commutation` | `(d1_vec d2_vec : Fin 2 → ℤ) : b1Ising * b1Ising = 1 ∧ b2Ising * b2Ising = 1 ∧ wangLevinCommutator = -(1 : Matrix (Fin 2) (Fin 2) ℤ) ∧ Matrix.trace wangLevinCommutator = -2 ∧ Matrix.diagonal d1_vec * Matrix.diagonal d2_vec = Matrix.diagonal d2_vec * Matrix.diagonal d1_vec` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:125 crossed_module_conjugation_peiffer_and_identity` | `{G : Type*} [Group G] (g h h1 h2 : G) : (fun x : G => x) (g * h * g⁻¹) = g * (fun x : G => x) h * g⁻¹ ∧ ((fun x : G => x) h1) * h2 * ((fun x : G => x) h1)⁻¹ = h1 * h2 * h1⁻¹` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:146 postnikov_cup3_is_3cocycle_on_zmod2` | `: (∀ g1 g2 g3 g4 : ZMod 2, groupCoboundary3 postnikovCup3 g1 g2 g3 g4 = 0) ∧ postnikovCup3 1 1 1 = 1 ∧ postnikovCup3 1 1 1 ≠ 0` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:157 postnikov_cup3_not_coboundary_in_H3_zmod2` | `: (∀ b : ZMod 2 → ZMod 2 → ZMod 2, rp3CyclePairing (groupCoboundary2 b) = 0) ∧ rp3CyclePairing postnikovCup3 = 1 ∧ (∀ b : ZMod 2 → ZMod 2 → ZMod 2, groupCoboundary2 b ≠ postnikovCup3)` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:170 two_connection_postnikov_3curvature_bianchi` | `(phi : Fin 5 → ZMod 2) (i j k l m : Fin 5) : let g := d0 phi let C3 (u v w x : Fin 5) : ZMod 2 := postnikovCup3 (g u v) (g v w) (g w x) d3 C3 i j k l m = 0` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:185 one_form_double_vs_conjugate_two_group_postnikov_cancellation` | `(g1 g2 g3 : ZMod 2) (n : ℕ) : postnikovCup3 1 1 1 + 0 = 1 ∧ postnikovCup3 g1 g2 g3 - postnikovCup3 g1 g2 g3 = 0 ∧ ((-1 : ℤ) ^ n) * ((-1 : ℤ) ^ n) = 1` |
| `lean4/CampaignFspBf2GroupSignClaim.lean:195 doubled_partition_function_changes_target_model_fence` | `: ((2 : ℤ) ≠ (-2 : ℤ) ∧ (2 : ℤ) ^ 2 = (-2 : ℤ) ^ 2) ∧ ((1 : ℤ) + (-1 : ℤ) = 0 ∧ (1 : ℤ) ^ 2 + (-1 : ℤ) ^ 2 = 2 ∧ ((1 : ℤ) + (-1 : ℤ)) ^ 2 ≠ (1 : ℤ) ^ 2 + (-1 : ℤ) ^ 2)` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_317_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
