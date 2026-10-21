# Next derivations after review

1. Gaussian-rational carrier for `𝕜 = ℂ`: embed pairs `(a, b)` of exact rational sequences as
   `a + i b` into `PreH ℂ`, prove the inner-product identity
   `⟪lift (a,b), lift (c,d)⟫ = (qinner a c + qinner b d) + i (qinner a d − qinner b c)` and the
   density of such pairs (ℚ + iℚ is dense in ℂ); the rest of `HilbertLiftCompletion` already
   holds for `𝕜 = ℂ`.
2. Intrinsic uniformity on the exact carrier: put `UniformSpace.ofFun sqdist` on `Carrier`
   (the doubling triangle inequality `sqdist_le_two_mul` is the hypothesis it needs), show that
   `castSeq ℝ` is uniform inducing with dense range, and obtain
   `UniformSpace.Completion Carrier ≃ᵤ HilbertLiftSpace ℝ` from `Completion.extension`; this
   restates the universal property on the exact carrier itself, with no real number in the
   domain.
3. Identification with `ℓ²(ℕ)`: build the isometry `HilbertLiftSpace 𝕜 ≃ₗᵢ lp (fun _ => 𝕜) 2`
   from `lp.hasSum_single` (finitely supported vectors are dense in `ℓ²`) and the uniqueness of
   completions.
4. Lifting finite operators: a family of rational matrices on the stages that is compatible with
   padding and uniformly bounded in the quadratic-form order defines a bounded operator on the
   lift; the harmonic witness shows that unbounded coordinate functionals do not extend.  This
   is the hypothesis the dynamics node (FQ-GAP-STONE-CONTINUOUS-TIME) would consume.
5. DAG status split: the node may be divided into the construction (kernel-checked, with the
   hypotheses `𝕜` and ℓ² explicit) and the selection of those hypotheses from finite-theory
   primitives (open; `harmonic_separates_uniformities` shows ℓ¹ and ℓ² are genuinely different
   choices).
6. Python mutation harness: add a `Certificate` row for `hilbert_lift_completion.py` in
   `code/python/src/qm/tests/test_isolated_certificates.py` if the campaign banner convention is
   adopted for it; optional atlas row in `docs/QM_PROBLEM_AND_PROOF_ATLAS.md`.
