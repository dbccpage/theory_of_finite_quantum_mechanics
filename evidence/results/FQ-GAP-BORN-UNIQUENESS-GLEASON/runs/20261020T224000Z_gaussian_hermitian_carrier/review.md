# Mathematical review and boundaries

AuthorityEffect: None.

## What is established

Scalars are the Gaussian rationals ℚ(i), realised as pairs of rationals with conjugation as `star`.
The carrier is the set of all n×n matrices over ℚ(i) with the preorder `A ≤ B :⇔ ∀ x, 0 ≤ re(x*(B−A)x)`
(x ranging over Gaussian-rational vectors) and unit the identity. This is an `OrderedQUnit`, so the
abstract effect-valuation results of the earlier run apply verbatim.

1. **Order unit.** `|re(x* A x)| ≤ (Σ(|re A_ij| + |im A_ij|))·⟨x,x⟩`, using
   `|re(ā c b)| ≤ (|c.re| + |c.im|)(|a|² + |b|²)/2`; hence `−k·1 ≤ A ≤ k·1` for a natural `k`.
2. **Rank-one effects.** Complex Cauchy–Schwarz over ℚ(i), `|x* y|² ≤ ⟨x,x⟩⟨y,y⟩`, is proved by
   expanding `0 ≤ ⟨N y − c x, N y − c x⟩` with `N = ⟨x,x⟩`, `c = x* y` componentwise. So
   `P x = x x*/⟨x,x⟩` is an effect for `x ≠ 0`.
3. **Trace representation.** A ℚ-linear, real-valued functional `L` on the 2n²-dimensional ℚ-space
   of Gaussian-rational matrices is `L A = re trace (ρ A)` for the unique matrix
   `ρ_ji = (L(E_ij), −L(i·E_ij))`; the proof expands `A = Σ E_ij (A_ij)` and
   `E_ij z = (re z)·E_ij 1 + (im z)·E_ij i` over ℚ.
4. **Born representation.** For every effect valuation `W` there is a unique `ρ` with
   `W.v E = re trace (ρ E)` on effects. `ρ` is Hermitian because the extension vanishes on the
   skew-Hermitian matrices `E_ji − E_ij` and `i(E_ji + E_ij)` (both are `≤ 0` and `≥ 0` in the
   preorder), positive semidefinite because `re(x* ρ x) = ⟨x,x⟩·W.v(P x) ≥ 0`, and of trace one
   (the real part is `W.v 1 = 1`; the imaginary part vanishes because each `i·E_ii` is
   skew-Hermitian). For `x ≠ 0`, `W.v (P x) = re(x* ρ x)/⟨x,x⟩`.
5. **Converse for every state.** Every Hermitian matrix positive on Gaussian-rational vectors is a
   nonnegative rational combination of rank-one Hermitian squares `w w*` (`gram_of_psd`, induction on
   the support with real pivots; a zero pivot with a nonzero off-diagonal entry yields an explicit
   negative witness). Hence `re trace (ρ E) ≥ 0` for Hermitian PSD `E`, and since a Hermitian `ρ`
   only sees the Hermitian part of an effect, `E ↦ re trace (ρ E)` is an effect valuation for every
   Hermitian rational-PSD trace-one `ρ`, with density `ρ`. The pure state `e₀` is a witness.

The Python and Rust twins replay the chain exactly (Gram certificates with conjugate lifting of
witnesses, the order-unit bound, the extension and its bound-independence, the representing matrix,
the Born certificate) and add the `imaginary_leak` control.

## What is supplied, not derived

- The Gaussian-rational matrix algebra, its order and the unit are inputs; nothing derives a Hilbert
  space from primitives, and the choice ℚ(i) (rather than another quadratic field or a cyclotomic
  field) is a choice of carrier, not a result.
- Effect additivity, positivity and normalisation are hypotheses (see the effect-valuation run).
- Valuations are real-valued and ℚ-linear. The representing matrix is unique as a matrix over ℚ(i)
  because the ℚ-dual of the matrix space is parametrised by Gaussian-rational matrices through the
  real-part trace; no ℚ(i)-linearity is claimed or needed.
- "PSD" is tested on Gaussian-rational vectors; no complex numbers, eigenvalues or continuity enter.

## Mechanical notes

Lean 4.33.1, pinned Mathlib cache, targeted imports; accepted receipts `gauss_rat_01`,
`hermitian_carrier_01`, `hermitian_psd_01`, `trace_01` by `tools/replay.py` (see
`accepted_modules.json`; the directory `verification/hermitian_trace_01` is a retained *failed*
attempt — the compiler could not open its snapshot because the path reached the Windows
260-character limit — superseded by `trace_01` for the byte-identical source); `tools/seal.py receipts` checks exit
codes, custody digests, absence of `sorry`/`axiom`/`opaque`/`unsafe`, absence of diagnostics, and
that every printed axiom list is within `{propext, Classical.choice, Quot.sound}`. The Field
instance of `GaussRat` is computable (`z⁻¹ = (normSq z)⁻¹ • star z`); the only noncomputable
definitions are the extension and the density, which use the order-unit choice.
