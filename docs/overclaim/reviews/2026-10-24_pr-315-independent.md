# Independent review of PR #315

Scope: original head 52e575312947290aba839ce04859965f55ac78f3. Exact source lean4/CampaignCtInformationMediaInteroperability.lean, SHA-256 4f150b51c5e3dba2813c52d547e9b5dbff1420a6477ab31bc3bfab3498d258d4.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Modular-addition maps have explicit inverses; finite-set cardinalities multiply; supplied integer CNOT/Bell/partial-transpose models obey the displayed polynomial identities. ZMod 0 is infinite, so the arbitrary-n theorem is algebraic rather than an exclusively finite-carrier theorem. The dimension functions are declared formulas, not constructed state spaces; normalized and unnormalized dimensions must not be conflated. The integer quadratic-form example does not construct two full physical cone theories satisfying all constructor axioms.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignCtInformationMediaInteroperability.lean:27 cnotClone_bijective_and_clones_zero` | `(n : ℕ) : (∀ p : ZMod n × ZMod n, cnotUnclone n (cnotClone n p) = p) ∧ (∀ p : ZMod n × ZMod n, cnotClone n (cnotUnclone n p) = p) ∧ Function.Bijective (cnotClone n) ∧ (∀ x : ZMod n, cnotClone n (x, 0) = (x, x))` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:45 cnotClone_zmod2_involutive` | `(p : ZMod 2 × ZMod 2) : cnotClone 2 (cnotClone 2 p) = p` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:51 singleton_not_computation_variable_fence` | `(n : ℕ) : (∀ x y : Fin 1, x = y) ∧ Fintype.card (Equiv.Perm (Fin 1)) = 1 ∧ ((0 : Fin (n + 2)) ≠ (1 : Fin (n + 2))) ∧ Equiv.swap (0 : Fin (n + 2)) (1 : Fin (n + 2)) (0 : Fin (n + 2)) = (1 : Fin (n + 2))` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:64 clonable_computation_implies_distinguishable` | `{X Y : Type*} (n : ℕ) (f : X → ZMod n) (g : ZMod n → Y) (x y : X) : (Function.Injective f → x ≠ y → cnotClone n (f x, 0) ≠ cnotClone n (f y, 0)) ∧ (f x = f y → g (f x) = g (f y))` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:90 principle_III_composite_cloning_and_cardinality` | `(n₁ n₂ d₁ d₂ : ℕ) : Function.Bijective (compositeClone n₁ n₂) ∧ (∀ x₁ : ZMod n₁, ∀ x₂ : ZMod n₂, compositeClone n₁ n₂ ((x₁, x₂), (0, 0)) = ((x₁, x₂), (x₁, x₂))) ∧ Fintype.card (Fin d₁ × Fin d₂) = d₁ * d₂` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:109 cross_medium_copy_transfer` | `(n : ℕ) (π : Equiv.Perm (ZMod n)) (x₁ : ZMod n) : Function.Bijective (crossCopy n) ∧ crossCopy n (x₁, 0) = (x₁, x₁) ∧ Prod.map id π (crossCopy n (x₁, 0)) = (x₁, π x₁)` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:127 unitary_cnot_clones_computational_basis_not_superposition_fence` | `(u0 u1 v0 v1 : ℤ) : cnot4 (1, 0, 0, 0) = (1, 0, 0, 0) ∧ cnot4 (0, 0, 1, 0) = (0, 0, 0, 1) ∧ cnot4 (1, 0, 1, 0) = (1, 0, 0, 1) ∧ cnot4 (1, 0, 1, 0) ≠ (1, 1, 1, 1) ∧ schmidtDet4 (cnot4 (1, 0, 1, 0)) = 1 ∧ schmidtDet4 (u0 * v0, u0 * v1, u1 * v0, u1 * v1) = 0` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:152 composite_state_space_dimension_trichotomy_fence` | `: Fintype.card (Fin 2 × Fin 2) = 4 ∧ classicalSimplexDim 2 2 = 3 ∧ realLocalProductDim 2 2 = 9 ∧ realQuantumDim 2 2 = 10 ∧ complexHermitianDim 2 2 = 16 ∧ classicalSimplexDim 2 2 < realLocalProductDim 2 2 ∧ realLocalProductDim 2 2 < realQuantumDim 2 2 ∧ realQuantumDim 2 2 < complexHermitianDim 2 2` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:164 real_vs_complex_bilinear_tomography_fence` | `(d₁ d₂ : ℕ) (z₁ z₂ : ℤ) : complexHermitianDim d₁ d₂ = complexHermitianDim d₁ 1 * complexHermitianDim 1 d₂ ∧ (z₁ * z₂ * (z₁ * z₂ + 1) * 2 - z₁ * (z₁ + 1) * (z₂ * (z₂ + 1)) = z₁ * z₂ * (z₁ - 1) * (z₂ - 1))` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:188 psd_vs_pt_cone_classical_interoperability_agreement_fence` | `(d : Fin 4 → ℤ) : partialTranspose4 (Matrix.diagonal d) = Matrix.diagonal d` |
| `lean4/CampaignCtInformationMediaInteroperability.lean:212 psd_vs_pt_cone_bell_witness_separation_fence` | `(w : Fin 4 → ℤ) (u0 u1 v0 v1 : ℤ) : dotProduct w (bellState4.mulVec w) = (w 0 + w 3) ^ 2 ∧ 0 ≤ dotProduct w (bellState4.mulVec w) ∧ dotProduct (prodVec4 u0 u1 v0 v1) (swapWitness4.mulVec (prodVec4 u0 u1 v0 v1)) = (u0 * v0 + u1 * v1) ^ 2 ∧ dotProduct singletVec (bellState4.mulVec singletVec) = 0 ∧ dotProduct singletVec (swapWitness4.mulVec singletVec) = -2` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_315_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
