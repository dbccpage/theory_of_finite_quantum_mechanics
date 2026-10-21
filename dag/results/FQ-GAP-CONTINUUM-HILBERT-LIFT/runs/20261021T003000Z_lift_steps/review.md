# Mathematical review and boundaries

AuthorityEffect: None. This file states what the three new modules prove, how the DAG record was split,
and what is not claimed. The four re-replayed modules are reviewed in
[runs/20261020T230000Z_completion/review.md](../20261020T230000Z_completion/review.md).

## 1. The intrinsic uniformity (item 2)

`instUniformSpaceCarrier` puts on `Carrier := ℕ →₀ ℚ` the pullback of the real pre-Hilbert metric along
`castSeq ℝ`. Two theorems make this intrinsic. `uniformity_hasBasis_sqdist` shows that the sets
`{(f, g) | sqdist f g < ε}`, `ε : ℚ`, `ε > 0`, form a basis of the uniformity (the real tolerance `ε` is
exchanged for a rational `δ < ε²` in one direction and for `√ε` in the other), and
`uniformity_eq_iInf_sqdist` concludes that the uniformity filter equals the infimum of the principal
filters of those sets. A uniform structure is determined by its uniformity filter, so the structure is
the one generated intrinsically by rational squared-distance balls, with no real number in its
description; the pullback is only the route by which the uniform-space axioms were obtained.
`cauchySeq_iff_isCauchyL2` then says that Cauchy sequences for this structure are exactly the
rational ℓ²-Cauchy sequences, and `exists_limit_in_completion` that each converges in
`Completion Carrier`.

`completionEquivLift` is built from the extension of `lift ℝ` to `Completion Carrier`: it is uniform
inducing (Mathlib's `isUniformInducing_extension`), injective because `Completion Carrier` is T0, and
surjective because its range is complete (hence closed) and contains the dense range of `lift ℝ`.
The theorem `completionEquivLift_coe` says it restricts to `lift ℝ` on exact vectors. So the real
Hilbert lift of the first run is, up to a unique uniform isomorphism over the exact vectors, the
completion of the exact carrier under its own rational uniformity. The real numbers no longer appear in
the domain; they still appear in the target, which is why the scalar field stays a named hypothesis.

## 2. The ℓ² model (item 3)

`toL2` sends a finitely supported `𝕜`-sequence to itself as an element of `lp (fun _ : ℕ => 𝕜) 2`
(`memℓp_coe`). It is linear, preserves the inner product (`inner_toL2`, from `lp.inner_eq_tsum` and
`tsum_eq_sum` on the finite support) and hence the norm, and has dense range (`denseRange_toL2`, from
`lp.hasSum_single`: the partial sums of `lp.single` converge to any element of `ℓ²`, and each partial
sum is the image of a finitely supported sequence). Its extension to the completion is an isometry by
closedness of the norm identity on a dense set, linear by the same argument, uniform inducing, and
surjective by the closed-and-dense argument; `LinearIsometryEquiv.ofSurjective` packages
`liftEquivL2 : HilbertLiftSpace 𝕜 ≃ₗᵢ[𝕜] ℓ²(ℕ, 𝕜)`. `liftEquivL2_lift_apply` identifies the model of an
exact vector with its coordinate sequence. This is the concrete model promised in the first run; it is
proved for every `RCLike` field, so for both `ℝ` and `ℂ`.

## 3. Lifting bounded exact operators (item 4)

A `BoundedExactOperator` is a `ℚ`-linear map `A` of the exact carrier with a rational bound `C ≥ 0`
such that `qinner (A f) (A f) ≤ C qinner f f`. Linearity converts this into
`sqdist (A f) (A g) ≤ C sqdist f g` (`sqdist_map_le`), which gives uniform continuity for the intrinsic
uniformity (`uniformContinuous_A`, through the sqdist basis on both sides) and preservation of rational
ℓ²-Cauchy sequences (`isCauchyL2_map`, with the explicit tolerance `ε / (C + 1)`). The lifted map
`liftOp` is `Completion.map A` transported through `completionEquivLift`; it is continuous, agrees with
`A` on exact vectors (`liftOp_lift`), and is the unique continuous map doing so (`liftOp_unique`, from
`ext_of_lift`). Additivity, `ℚ`-homogeneity and then `ℝ`-homogeneity are obtained by density
(`DenseRange.induction_on` on pairs, on vectors, and on `ℚ ⊆ ℝ`), so `toCLM` is a continuous `ℝ`-linear
map; the quadratic bound passes to the closure (`norm_liftOp_sq_le`) and gives `‖toCLM‖ ≤ √C`.

Examples: `proj n` (stage projection, bound 1 by `finInner_trunc_le`) lifts to `liftFin ∘ trunc n`;
`shift` (`Finsupp.lmapDomain ℚ ℚ Nat.succ`) preserves `qinner` exactly (`qinner_shift`, by reindexing
the finite sum along the injection `Nat.succ`) and lifts to an isometry of the real lift. The negative
example is the coordinate sum `coordSum f = Σ_i f i`: it is `ℚ`-linear, but
`coordSum (harmonic 2n) − coordSum (harmonic n) ≥ 1/2` while the harmonic vectors are ℓ²-Cauchy and
have squared norm at most 2; a continuous real functional on the lift restricting to it would make the
real sequence `coordSum (harmonic n)` convergent, hence Cauchy, contradicting the gap
(`no_continuous_extension_coordSum`). So linearity on exact vectors is not enough; the quadratic bound
is the hypothesis the lift consumes.

## 4. The DAG split (item 5)

`tools/dag_update.py` adds `FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION` with status `PROVED_LEAN`, whose
statement begins "With the scalar field and the ℓ² uniformity supplied as named hypotheses" and whose
`imported_structure` lists exactly those two items; a route `FQ-R-CONTINUUM-HILBERT-LIFT-CONSTRUCTION`
(`CONDITIONAL_ON_IMPORT`, input `FQ-CARRIER-CONTRACT-V2`) leads to it, and a `GAP_NO_DERIVATION` route
`FQ-R-GAP-CONTINUUM-FROM-CONSTRUCTION` leads from it to `FQ-GAP-CONTINUUM-HILBERT-LIFT`, whose record now
says that what remains there is the selection of the two hypotheses from finite-theory primitives.
The status legend's reading of `PROVED_LEAN` ("a named Lean declaration exists in the checkout and the
source cites it") is met; the hypotheses are visible on the node rather than hidden in the proof.
The gap node keeps `CONDITIONAL`.

## 5. Item 6

The Python twin exposes `certify()` with the shared refusal boundary (float, boolean and non-rational
probes are refused with the harness's invariant strings) and returns the locked value `1/2`; the
harness row cites `theorem coordSum_harmonic_gap` in `lean4/HilbertLiftOperators.lean` and mutates the
subtraction in `coord_sum_gap`. The atlas row is not added (the atlas verifier fixes 65 questions).

## 6. What is not claimed

- The scalar field `ℝ`/`ℂ` and the ℓ² uniformity are supplied. The intrinsic-uniformity theorem
  removes `ℝ` from the domain of the completion only.
- The operator lift is proved over `ℝ`; the complex case for Gaussian-rational pairs, and the
  intrinsic uniformity on pairs, are left to `next_steps.md`.
- No dynamics, generator, spectrum, Born pairing or tensor structure is lifted; the bound `C` on an
  exact operator is a hypothesis and nothing selects physical operators.
- The uniform structure on `ℕ →₀ ℚ` and the inner-product structure on `ℕ →₀ 𝕜` are global instances
  on abbreviations; no other module of the repository places such structures on `Finsupp` today.
