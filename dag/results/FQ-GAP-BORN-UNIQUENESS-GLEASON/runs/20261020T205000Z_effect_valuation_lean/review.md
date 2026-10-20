# Mathematical review and boundaries

AuthorityEffect: None.

## What is established

Let `V` be a ℚ-module with a preorder compatible with addition and nonnegative rational scaling,
and a distinguished `u ≥ 0` (`OrderedQUnit`, verbatim from the frozen `contract.lean`). An
effect is `0 ≤ a ≤ u`; an effect valuation `v` is normalised (`v u = 1`), nonnegative on effects
and additive on pairs of effects whose sum is an effect (`EffectValuation`, verbatim).

1. **Eight frozen targets** (`BornEffectValuation.lean`). `v 0 = 0`; `b - a` is an effect when
   `a ≤ b`; monotonicity; `v a ≤ 1`; `q • a` is an effect for `q ∈ [0,1]`; `v (k • a) = k v a`
   for natural `k` with `k • a` an effect; `v (q • a) = q v a` for rational `q ∈ [0,1]` (the
   "first missing lemma" named by the Fable 5.1 checkpoint); and `|v a - v b| ≤ ε` when
   `-(ε • u) ≤ a - b ≤ ε • u`. Rational homogeneity uses only additivity and rational
   divisibility of `V`; monotonicity is derived, not assumed.
2. **Linear extension** (`BornLinearExtension.lean`). If `u` is an order unit (every element is
   bounded by a natural multiple of `u`), the value `2t·v((1/2t)•(a + t•u)) − t` is independent
   of the admissible bound `t`, additive, equal to `v` on effects, nonnegative on the positive
   cone, and `1` at `u`. Additivity on a ℚ-module already gives ℚ-linearity
   (`AddMonoidHom.toRatLinearMap`); the extension is the unique ℚ-linear functional agreeing with
   `v` on effects (`linear_extension`, an `∃!`).
3. **Rational matrix carrier** (`BornMatrixCarrier.lean`). Rational `n×n` matrices with
   `A ≤ B :⇔ ∀ x, 0 ≤ xᵀ(B−A)x` on rational vectors and `u = 1` form an `OrderedQUnit`; the
   relation is a preorder only (skew matrices are null). The identity is an order unit with the
   explicit bound `⌈∑|A i j|⌉`. For `x ≠ 0`, `P x = x xᵀ/(x⬝x)` is an effect by Cauchy–Schwarz
   over ℚ. Every ℚ-linear functional `L` is `A ↦ trace (repMatrix L * A)` with a unique
   representing matrix.
4. **Born representation** (`BornTraceRepresentation.lean`). For every effect valuation `W` on
   rational `n×n` matrices there is a unique `ρ` with `W.v E = trace (ρ * E)` on all effects;
   `ρ` is symmetric (the extension vanishes on skew matrices), PSD on rational vectors (from the
   rank-one effects) and has trace one; and `W.v (P x) = ⟨x, ρ x⟩ / ⟨x, x⟩` for `x ≠ 0`.
5. **Converse for every state** (`BornPsdDecomposition.lean`, `BornTraceRepresentation.lean`).
   Every symmetric rational-PSD matrix is a nonnegative rational combination of rank-one squares
   (`gram_of_psd`, induction on the support with explicit rational witnesses for zero pivots), so
   `trace (ρ * E) ≥ 0` for symmetric PSD `E`; the trace against a symmetric `ρ` only sees the
   symmetric part of an effect, hence `E ↦ trace (ρ * E)` is an effect valuation for every
   symmetric rational-PSD trace-one `ρ`, with density `ρ` (`state_valuation_correspondence`).
   The pure state `e₀` witnesses nonvacuity in every dimension `n + 1`.
6. **Rational-sphere obstruction** (`BornRationalSphereObstruction.lean`). On integer triples
   that are not all even and have square norm (the rational points of `S²`), the function
   "third coordinate odd" is two-valued, sums to one on every orthogonal triple
   (`parity_frame_function`; the mod-8 analysis gives exactly one odd coordinate per ray and
   orthogonality separates the odd positions), and agrees with no rational quadratic form on
   six explicit rays (`parity_not_quadratic`). Additivity on orthogonal triples of rational rays
   therefore does not select the quadratic form in `d = 3`.

Exact replays: the Python module computes Gram certificates with negative witnesses, effects,
the order-unit bound, the extension and its bound-independence, the representing matrix and
the Born certificate, the parity sweep over the box `|coords| ≤ 5`, and the inconsistent
six-ray system; the two mutation controls (a non-additive and a non-positive valuation) fail
exactly where the theorems say they must. The Rust module mirrors it on `BigRational`.

## What is supplied, not derived

- The rational matrix algebra, its quadratic-form order and the identity as unit are inputs.
  Nothing here derives a Hilbert space or a projection lattice from primitives.
- Effect additivity (on effects, not only on projections), positivity and normalisation are
  hypotheses. Their operational justification is a separate obligation
  (`L1-QM020-THM6-P2-GLEASON` assumptions, GF-5).
- The carrier is real-symmetric over ℚ. The Gaussian-rational Hermitian carrier is not treated;
  the same arguments are expected to go through with `ℚ(i)` entries, but that is unchecked.
- "PSD" means nonnegative on rational vectors. By the Gram decomposition this coincides with the
  usual notion for symmetric rational matrices, but no real spectral theory is used.

## Relation to the Gleason import

The projection-lattice route (Gleason for `n ≥ 3`) is not used. Item 6 shows that on the
rational carrier the projection-only hypothesis cannot yield the quadratic form, so some
stronger hypothesis is needed there: either the continuum (all real orthonormal bases) or, as
here, additivity on effects. The DAG node keeps status `CONDITIONAL`; its bottleneck now names
the supplied structure and the open complex and operational obligations instead of the
continuum theorem.

## Mechanical notes

- Lean 4.33.1, pinned Mathlib cache (`lean4/lake-manifest.json`), targeted imports (a full
  `import Mathlib` costs about ten minutes on this machine; the frozen `contract.lean` header is
  the only textual difference from the reproduced interface).
- `BornLinearExtension.lean` disables three style-only linters (`unnecessarySeqFocus`,
  `unusedTactic`, `unreachableTactic`) for the uniform `match_scalars <;> field_simp <;> ring`
  blocks; no proof content is affected. No other option is changed in any file.
- Receipts: `tools/replay.py` (byte-identical to the Jordan-catalogue run's tool), one label per
  source, in dependency order; `tools/seal.py receipts` checks exit codes, custody digests, the
  absence of `sorry`/`axiom`/`opaque`/`unsafe`, the absence of diagnostics, and that every
  printed axiom list is within `{propext, Classical.choice, Quot.sound}`.
