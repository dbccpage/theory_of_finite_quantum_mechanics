# Independent review of PR #324

Scope: original head e73dd03100c180846e47f09307f825c19fba08cb. Exact source lean4/CampaignFspDiscreteWdwConstraint.lean, SHA-256 b9c0facb18d974145f514cc8e47133efd525444aee3830a67cedd19b989644e3.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Rational residuals obey elementary norm bounds, and a zero-edge/sign-vertex witness has the displayed norm bound and objective equality. No incidence operator, transpose annihilation proposition, optimizer API, or general strong-duality theorem is constructed. A rank-one quadratic form, two supplied 2x2 projectors and a swap constraint have the stated identities. The thermal values 8 and 5 are second-order polynomial traces, not Gibbs exponential traces. The indefinite rational two-variable form is supplied and not derived from continuum DeWitt geometry; no physical Wheeler-DeWitt projector or fermion-sign mechanism follows.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspDiscreteWdwConstraint.lean:33 dJoint_linear_and_constant_kernel` | `{n : ℕ} (u v : Fin n) (a b c : ℚ) (alpha beta : Fin n → ℚ) : d0Edge u v (fun w => a * alpha w + b * beta w) = a * d0Edge u v alpha + b * d0Edge u v beta ∧ d0Edge u v (fun _ => c) = 0 ∧ dJointScalar alpha v = 0` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:50 primal_l1_edge_and_vertex_residual_lower_bound` | `{m n : ℕ} (p d0alpha : Fin m → ℚ) (hPerp : Fin n → ℚ) (v0 : Fin n) (hv0 : hPerp v0 ≠ 0) : (∑ v : Fin n, &#124;hPerp v&#124;) ≤ totalJointResidualL1 p d0alpha hPerp ∧ totalJointResidualL1 d0alpha d0alpha hPerp = ∑ v : Fin n, &#124;hPerp v&#124; ∧ &#124;hPerp v0&#124; ≤ totalJointResidualL1 p d0alpha hPerp ∧ 0 < totalJointResidualL1 p d0alpha hPerp` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:95 strong_duality_direct_sum_wdw_exact_coboundary` | `{m n : ℕ} (d0alpha : Fin m → ℚ) (hPerp : Fin n → ℚ) : (∀ v : Fin n, &#124;ratSign (hPerp v)&#124; ≤ 1) ∧ dualObjective (fun _ => 0) (fun v => ratSign (hPerp v)) d0alpha hPerp = totalJointResidualL1 d0alpha d0alpha hPerp` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:111 s4_seed_flat_vs_curved_wdw_defect_mass` | `: let hFlat : Fin 6 → ℚ := fun _ => 0 let hCurved : Fin 6 → ℚ := fun _ => (15 : ℚ) / 2 let pZero : Fin 15 → ℚ := fun _ => 0 totalJointResidualL1 pZero pZero hFlat = 0 ∧ routeFromDefectMass (totalJointResidualL1 pZero pZero hFlat) = .ExactRepair ∧ totalJointResidualL1 pZero pZero hCurved = 45 ∧ routeFromDefectMass (totalJointResidualL1 pZero pZero hCurved) = .SplitBrainRefusal` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:128 quadratic_constraint_psd_and_null_kernel_iff` | `(a b x0 x1 : ℚ) : quadraticConstraintForm a b x0 x1 = (a * x0 + b * x1) ^ 2 ∧ 0 ≤ quadraticConstraintForm a b x0 x1 ∧ (quadraticConstraintForm a b x0 x1 = 0 ↔ a * x0 + b * x1 = 0)` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:151 diffeomorphism_averaging_projector_and_constraint_complement` | `(x0 x1 : ℚ) : diffInvProjector * diffInvProjector = diffInvProjector ∧ wdwDiffConstraint * wdwDiffConstraint = wdwDiffConstraint ∧ diffInvProjectorᵀ = diffInvProjector ∧ wdwDiffConstraint * diffInvProjector = 0 ∧ (wdwDiffConstraint.mulVec ![x0, x1] = 0 ↔ x0 = x1) ∧ (diffInvProjector.mulVec ![x0, x1] = ![x0, x1] ↔ x0 = x1)` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:206 page_wootters_clock_system_conditioned_evolution` | `(psi0 psi1 : Fin 2 → ℚ) : pwStepMatrix * pwStepMatrix = 1 ∧ (pwConstraintResidual psi0 psi1 = (0, 0) ↔ psi1 = pwStepMatrix.mulVec psi0) ∧ pwConstraintResidual ![1, 0] ![0, 1] = (0, 0) ∧ (![(0 : ℚ), 1] : Fin 2 → ℚ) ≠ ![(1 : ℚ), 0]` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:242 dewitt_supermetric_indefinite_signature_fence` | `: dewittSupermetricForm 1 0 = -1 ∧ dewittSupermetricForm 1 0 < 0 ∧ dewittSupermetricForm 0 1 = 1 ∧ 0 < dewittSupermetricForm 0 1 ∧ dewittSupermetricForm 1 1 = 0 ∧ ((1 : ℚ), (1 : ℚ)) ≠ ((0 : ℚ), (0 : ℚ))` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:260 wdw_constraint_kernel_vs_thermal_gibbs_trace_fence` | `: (∀ i : Fin 4, (hubbardFourStateSpectrum 1 i = 0 ↔ hubbardFourStateSpectrum (1 / 2) i = 0)) ∧ secondOrderThermalTrace (hubbardFourStateSpectrum 1) 1 = 8 ∧ secondOrderThermalTrace (hubbardFourStateSpectrum (1 / 2)) 1 = 5 ∧ secondOrderThermalTrace (hubbardFourStateSpectrum 1) 1 ≠ secondOrderThermalTrace (hubbardFourStateSpectrum (1 / 2)) 1` |
| `lean4/CampaignFspDiscreteWdwConstraint.lean:278 wdw_constraint_projection_preserves_fermion_sign_cancellation_fence` | `(v : Fin 2 → ℚ) : (1 : ℚ) * (v ⬝ᵥ diffInvProjector.mulVec v) + (-1 : ℚ) * (v ⬝ᵥ diffInvProjector.mulVec v) = 0` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_324_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
