# Mathematical review and boundaries

AuthorityEffect: None. This file states what the four kernel-checked modules prove, what they
assume, and what they do not say.

## 1. What is constructed

The node asked for "a controlled completion from exact finite carriers, with explicit
embeddings, topology, and convergence hypotheses". The run supplies each item by name.

**Carriers.** The exact finite carrier at report size `n` is `FinCarrier n := Fin n → ℚ` with
the rational inner product `finInner x y = Σ x i * y i`. Report sizes are ordered by zero
padding `pad h : FinCarrier n → FinCarrier m` for `h : n ≤ m`, which is functorial, `ℚ`-linear,
injective and inner-product preserving (`pad_refl`, `pad_trans`, `pad_add`, `pad_smul`,
`pad_injective`, `finInner_pad`). The directed union is `Carrier := ℕ →₀ ℚ`, the finitely
supported rational sequences, with canonical injections `ofFin` satisfying the cocone identity
`ofFin (pad h x) = ofFin x`; `exhaustion` says every exact sequence is `ofFin` of some finite
stage and `trunc` is a left inverse. The inner product `qinner` restricts to `finInner`
(`qinner_ofFin`), is positive definite, and satisfies Cauchy–Schwarz over `ℚ` (`qinner_sq_le`).
Nothing in this module uses a real number.

**Topology.** The uniformity is named explicitly and intrinsically: the squared distance
`sqdist f g = qinner (f − g) (f − g)` with rational tolerances. `IsCauchyL2 x` means
`∀ ε : ℚ > 0, ∃ N, ∀ m n ≥ N, sqdist (x m) (x n) < ε`; `HasModulusL2 x μ` is the explicit-modulus
form, equivalent to it (`isCauchyL2_of_hasModulus`, `exists_hasModulus_of_isCauchyL2`). The
doubling triangle inequality `sqdist f h ≤ 2 (sqdist f g + sqdist g h)` (`sqdist_le_two_mul`)
is the square-root-free form of the triangle inequality; it is proved from the arithmetic–
quadratic bound `2 qinner f g ≤ qinner f f + qinner g g`. The competing uniformities ℓ¹ and sup
are also named; ℓ¹-Cauchy implies ℓ²-Cauchy implies sup-Cauchy.

**Completion.** For `𝕜 = ℝ` or `ℂ` (any `RCLike` field), `PreH 𝕜 := ℕ →₀ 𝕜` carries the inner
product `Σ conj (f i) * g i`; the inner-product core is verified field by field and Mathlib's
`InnerProductSpace.Core.toNormedAddCommGroup` and `InnerProductSpace.ofCore` make it a normed
inner product space. The Hilbert lift is `HilbertLiftSpace 𝕜 := UniformSpace.Completion (PreH 𝕜)`,
the Hausdorff completion; Mathlib provides `CompleteSpace` and `InnerProductSpace 𝕜` instances
on it (`hilbertLiftSpace_complete`, `hilbertLiftSpace_innerProductSpace`).

**Embeddings.** `castSeq 𝕜 : Carrier → PreH 𝕜` casts coordinates; `lift 𝕜 f := ↑(castSeq 𝕜 f)` and
`liftFin 𝕜 x := lift 𝕜 (ofFin x)`. They are additive, `ℚ`-homogeneous, injective, compatible with
padding (`liftFin_pad`), and inner-product preserving: `⟪lift f, lift g⟫ = (qinner f g : 𝕜)`
(`inner_lift`), hence `dist (lift f) (lift g) ^ 2 = (sqdist f g : ℝ)` (`dist_lift_sq`).

**Convergence hypotheses.** `cauchySeq_lift_iff`: a sequence of exact vectors is Cauchy in the
lift exactly when it is `IsCauchyL2` with rational tolerances. `exists_limit_of_isCauchyL2`:
every such sequence has a limit in the lift, unique by `limit_unique`. `tendsto_lift_iff`:
convergence to an exact vector in the lift is the rational `TendsToL2`. So the only convergence
hypothesis ever used is the rational ℓ² Cauchy condition, and it is discharged inside the lift,
never on the exact carrier.

**Density and control (ℝ).** `denseRange_castSeq_real` and `denseRange_lift_real`: the exact
carrier is dense; `exists_exact_tendsto`: every element of the real lift is the limit of an
ℓ²-Cauchy exact sequence; `ext_of_lift`: two continuous maps out of the real lift that agree on
exact vectors are equal. The quantitative content of density is the rational approximation
`Σ_{i ∈ s} (f i − q i)² < |s| · (r/(|s|+1))² < r²`, replayed exactly in the twins.

**Strictness.** The harmonic witness `h_N = Σ_{i<N} e_i / (i+1)` is ℓ²-Cauchy with the explicit
modulus `k ↦ k+1` (from the telescoping bound `Σ_{n≤i<m} 1/(i+1)² ≤ 1/n − 1/m`), is not
ℓ¹-Cauchy (`l1dist (h_{2n}) (h_n) ≥ 1/2`), and converges to no exact vector
(`sqdist (h_N) f ≥ 1/(M+1)²` for `N > M`, `M` the support bound of `f`). Hence
`lift_not_surjective`: the lift is a genuine extension, and `harmonic_separates_uniformities`:
the ℓ¹ and ℓ² uniformities on the same exact carrier have different Cauchy sequences, so the
choice of uniformity is a hypothesis with observable consequences, not a convention.

**Complex case.** Pairs `(a, b)` of exact sequences, read as `a + i b`, embed into `PreH ℂ` with
the exact identity `⟪a+ib, c+id⟫ = (⟨a,c⟩ + ⟨b,d⟩) + i(⟨a,d⟩ − ⟨b,c⟩)` (`inner_castPair`), are dense
in the complex lift (`denseRange_liftPair`), and the lift is strictly larger
(`liftPair_not_surjective`). The packaged statements are `controlled_completion` (ℝ, six clauses)
and `controlled_completion_complex` (ℂ, four clauses).

## 2. What is assumed

1. The scalar field `𝕜 ∈ {ℝ, ℂ}` is supplied. Since `ℝ` is the completion of `ℚ` and `ℂ` of
   `ℚ(i)`, this is itself a completion hypothesis, of the scalars rather than of the vectors.
   The modules do not select it; a rational-scalar completion of the exact carrier with its
   intrinsic ℓ² uniformity (next step 2) would make the dependence on `ℝ` a theorem rather than
   an input, but it has not been done here.
2. The ℓ² uniformity is supplied. The run proves that this is a real choice (ℓ¹ differs) and
   that the completion depends on it; it does not derive ℓ² from finite-theory primitives. The
   standard inner product on the finite stages is likewise supplied.
3. Mathlib's completion is used as a black box with its universal property. The identification
   of `HilbertLiftSpace 𝕜` with `ℓ²(ℕ, 𝕜)` is not proved (next step 3); nothing in the run depends
   on it.

## 3. What is not claimed

- No operator, dynamics, Born pairing, tensor structure, measurement or physical interpretation
  is lifted; the modules build the space only. The dynamics node
  (FQ-GAP-STONE-CONTINUOUS-TIME) is untouched.
- No claim that the physical state space of the finite theory is this lift; the construction
  shows what the continuum interface costs when it is paid in the ℓ² currency, and nothing
  about whether it should be paid.
- The Gaussian-rational pairs are not given a field structure; complex multiplication enters
  only through the inner-product identity.
- The inner-product fluctuation bound used by the twins to make modulus-based completion points
  computable is a native estimate (from Cauchy–Schwarz and `(a+b)² ≤ 2(a²+b²)`), not a kernel
  receipt; it is labelled as such in `claim_status.json`.
- The instances on `PreH 𝕜` are declared on the abbreviation `ℕ →₀ 𝕜`, following Mathlib's own
  pattern for `H₀` in `Mathlib.Analysis.InnerProductSpace.Reproducing`; no other module of this
  repository places a norm on `Finsupp`, so no instance diamond arises today, but a future module
  that does so must be checked against these instances.

## 4. Relation to the node record

The node statement said that the transition to a continuous infinite-dimensional Hilbert space
"is not constructed in any source". After this run it is constructed, with three named
hypotheses (scalar field, ℓ² uniformity, rational ℓ² Cauchy condition on exact sequences). The
status stays `CONDITIONAL` because the first two hypotheses are supplied; `imported_structure`
now names exactly them. The earlier `Z[i]` non-field obstruction and discriminant-5 spectral exit
remain mechanized and untouched; they concern algebraic closure of finite matrix algebras, which
is a different question from completeness and is not addressed here.
