import Mathlib.NumberTheory.Zsqrtd.GaussianInt
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic
import «qm_wave6_completion»
import «qm_finite_matrix_recovery»
import «qm_tsirelson_chsh_recovery»
import «qm_mermin_peres_observer»

/-!
# Wave 7 completion boundary

Exact finite-dimensional recovery results on an explicit matrix host.
The complex/Gaussian matrix carrier is an imported host, not a FinL1 consequence.

AuthorityEffect: None.
-/

noncomputable section

namespace QM
namespace Wave7Completion

open scoped BigOperators ComplexOrder MatrixOrder InnerProductSpace

namespace OperatorMerminPeres

abbrev GI := GaussianInt
abbrev M2 := Matrix (Fin 2) (Fin 2) GI
abbrev Qubit2 := Fin 2 × Fin 2
abbrev M4 := Matrix Qubit2 Qubit2 GI

def ii : GI := ⟨0, 1⟩
def eye : M2 := 1
def x : M2 := !![0, 1; 1, 0]
def y : M2 := !![0, -ii; ii, 0]
def z : M2 := !![1, 0; 0, -1]

def kron (a b : M2) : M4 := Matrix.kronecker a b

def square : MerminPeresObserver.V → M4
  | .a11 => kron x eye
  | .a12 => kron eye x
  | .a13 => kron x x
  | .a21 => kron eye y
  | .a22 => kron y eye
  | .a23 => kron y y
  | .a31 => kron x y
  | .a32 => kron y x
  | .a33 => kron z z

def contextTriple : MerminPeresObserver.C → M4 × M4 × M4
  | .r1 => (square .a11, square .a12, square .a13)
  | .r2 => (square .a21, square .a22, square .a23)
  | .r3 => (square .a31, square .a32, square .a33)
  | .c1 => (square .a11, square .a21, square .a31)
  | .c2 => (square .a12, square .a22, square .a32)
  | .c3 => (square .a13, square .a23, square .a33)

def contextProduct (c : MerminPeresObserver.C) : M4 :=
  let t := contextTriple c
  t.1 * t.2.1 * t.2.2

theorem context_products_exact :
    ∀ c, contextProduct c =
      if c = MerminPeresObserver.C.c3 then -(1 : M4) else 1 := by
  intro c
  cases c <;> decide


def PairwiseCommutes (t : M4 × M4 × M4) : Prop :=
  t.1 * t.2.1 = t.2.1 * t.1 ∧
  t.1 * t.2.2 = t.2.2 * t.1 ∧
  t.2.1 * t.2.2 = t.2.2 * t.2.1

theorem square_hermitian : ∀ v, (square v).IsHermitian := by
  intro v
  cases v <;> decide

theorem square_involutive : ∀ v, square v * square v = (1 : M4) := by
  intro v
  cases v <;> decide

theorem contexts_pairwise_commute : ∀ c, PairwiseCommutes (contextTriple c) := by
  intro c
  cases c <;> simp only [PairwiseCommutes] <;> decide

theorem product_phase_matches_f2_target : ∀ c,
    (contextProduct c = -(1 : M4) ↔ MerminPeresObserver.target c = true) ∧
    (contextProduct c = (1 : M4) ↔ MerminPeresObserver.target c = false) := by
  intro c
  cases c <;> decide

abbrev CM4 := Matrix Qubit2 Qubit2 ℂ

def toComplex : M4 →+* CM4 := GaussianInt.toComplex.mapMatrix

def complexSquare (v : MerminPeresObserver.V) : CM4 := toComplex (square v)

def complexContextTriple (c : MerminPeresObserver.C) : CM4 × CM4 × CM4 :=
  let t := contextTriple c
  (toComplex t.1, toComplex t.2.1, toComplex t.2.2)

def complexContextProduct (c : MerminPeresObserver.C) : CM4 :=
  let t := complexContextTriple c
  t.1 * t.2.1 * t.2.2

theorem complex_context_product_is_mapped (c : MerminPeresObserver.C) :
    complexContextProduct c = toComplex (contextProduct c) := by
  cases c <;> simp [complexContextProduct, complexContextTriple, contextProduct,
    contextTriple, toComplex]

theorem complex_context_products_exact (c : MerminPeresObserver.C) :
    complexContextProduct c =
      if c = MerminPeresObserver.C.c3 then -(1 : CM4) else 1 := by
  rw [complex_context_product_is_mapped, context_products_exact]
  split
  · simpa only [map_one] using (map_neg toComplex (1 : M4))
  · exact map_one toComplex


/-- W7.3 operator-full package: Hermitian involutions, commuting contexts,
exact complex product signs, and the F₂ no-global-assignment obstruction. -/
theorem full_operator_contextual_representation :
    (∀ v, (square v).IsHermitian ∧ square v * square v = (1 : M4)) ∧
    (∀ c, PairwiseCommutes (contextTriple c)) ∧
    (∀ c, complexContextProduct c =
      if c = MerminPeresObserver.C.c3 then -(1 : CM4) else 1) ∧
    ¬ ∃ a : MerminPeresObserver.Assignment,
      MerminPeresObserver.SatisfiesTarget a := by
  refine ⟨?_, contexts_pairwise_commute, complex_context_products_exact,
    MerminPeresObserver.no_global_assignment⟩
  intro v
  exact ⟨square_hermitian v, square_involutive v⟩

end OperatorMerminPeres

/-! ## W7.2: analytic finite-dimensional Tsirelson bound -/

namespace AnalyticTsirelson

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

def chshVector (a₀ a₁ b₀ b₁ : H) : ℝ :=
  ⟪a₀, b₀⟫_ℝ + ⟪a₀, b₁⟫_ℝ + ⟪a₁, b₀⟫_ℝ - ⟪a₁, b₁⟫_ℝ

theorem chshVector_split (a₀ a₁ b₀ b₁ : H) :
    chshVector a₀ a₁ b₀ b₁ =
      ⟪a₀, b₀ + b₁⟫_ℝ + ⟪a₁, b₀ - b₁⟫_ℝ := by
  simp [chshVector, inner_add_right, inner_sub_right]
  ring

theorem norm_add_add_norm_sub_le_two_sqrt_two
    (b₀ b₁ : H) (hb₀ : ‖b₀‖ = 1) (hb₁ : ‖b₁‖ = 1) :
    ‖b₀ + b₁‖ + ‖b₀ - b₁‖ ≤ 2 * Real.sqrt 2 := by
  have hp := parallelogram_law_with_norm (𝕜 := ℝ) b₀ b₁
  rw [hb₀, hb₁] at hp
  norm_num at hp
  have hs : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hs0 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  have hplus : 0 ≤ ‖b₀ + b₁‖ := norm_nonneg _
  have hminus : 0 ≤ ‖b₀ - b₁‖ := norm_nonneg _
  nlinarith [sq_nonneg (‖b₀ + b₁‖ - ‖b₀ - b₁‖)]

/-- Finite- or infinite-dimensional real-vector Tsirelson inequality.
For complex quantum models this applies to the standard realification of the
four correlation vectors. The host is explicit; it is not FinL1-derived. -/
theorem analytic_tsirelson_bound
    (a₀ a₁ b₀ b₁ : H)
    (ha₀ : ‖a₀‖ = 1) (ha₁ : ‖a₁‖ = 1)
    (hb₀ : ‖b₀‖ = 1) (hb₁ : ‖b₁‖ = 1) :
    |chshVector a₀ a₁ b₀ b₁| ≤ 2 * Real.sqrt 2 := by
  rw [chshVector_split]
  calc
    |⟪a₀, b₀ + b₁⟫_ℝ + ⟪a₁, b₀ - b₁⟫_ℝ| ≤
        |⟪a₀, b₀ + b₁⟫_ℝ| + |⟪a₁, b₀ - b₁⟫_ℝ| := abs_add_le _ _
    _ ≤ ‖a₀‖ * ‖b₀ + b₁‖ + ‖a₁‖ * ‖b₀ - b₁‖ :=
      add_le_add (abs_real_inner_le_norm _ _) (abs_real_inner_le_norm _ _)
    _ = ‖b₀ + b₁‖ + ‖b₀ - b₁‖ := by rw [ha₀, ha₁]; ring
    _ ≤ 2 * Real.sqrt 2 :=
      norm_add_add_norm_sub_le_two_sqrt_two b₀ b₁ hb₀ hb₁

def bPlus (e₀ e₁ : H) : H := (Real.sqrt 2 / 2) • (e₀ + e₁)

def bMinus (e₀ e₁ : H) : H := (Real.sqrt 2 / 2) • (e₀ - e₁)

theorem orthonormal_norms
    (e₀ e₁ : H)
    (h00 : ⟪e₀, e₀⟫_ℝ = 1) (h11 : ⟪e₁, e₁⟫_ℝ = 1) :
    ‖e₀‖ = 1 ∧ ‖e₁‖ = 1 := by
  have h0sq : ‖e₀‖ ^ 2 = 1 := by
    rw [← real_inner_self_eq_norm_sq]
    exact h00
  have h1sq : ‖e₁‖ ^ 2 = 1 := by
    rw [← real_inner_self_eq_norm_sq]
    exact h11
  constructor <;> nlinarith [norm_nonneg e₀, norm_nonneg e₁]

theorem standard_bob_settings_unit
    (e₀ e₁ : H)
    (h00 : ⟪e₀, e₀⟫_ℝ = 1) (h11 : ⟪e₁, e₁⟫_ℝ = 1)
    (h01 : ⟪e₀, e₁⟫_ℝ = 0) :
    ‖bPlus e₀ e₁‖ = 1 ∧ ‖bMinus e₀ e₁‖ = 1 := by
  obtain ⟨he0, he1⟩ := orthonormal_norms e₀ e₁ h00 h11
  have hs : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hs0 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  have hsumSq := norm_add_sq_real e₀ e₁
  have hsubSq := norm_sub_sq_real e₀ e₁
  rw [he0, he1, h01] at hsumSq hsubSq
  norm_num at hsumSq hsubSq
  have hsum : ‖e₀ + e₁‖ = Real.sqrt 2 := by
    nlinarith [norm_nonneg (e₀ + e₁)]
  have hsub : ‖e₀ - e₁‖ = Real.sqrt 2 := by
    nlinarith [norm_nonneg (e₀ - e₁)]
  constructor
  · rw [bPlus, norm_smul, Real.norm_eq_abs, abs_of_nonneg (by positivity), hsum]
    nlinarith
  · rw [bMinus, norm_smul, Real.norm_eq_abs, abs_of_nonneg (by positivity), hsub]
    nlinarith

theorem standard_settings_attain_tsirelson
    (e₀ e₁ : H)
    (h00 : ⟪e₀, e₀⟫_ℝ = 1) (h11 : ⟪e₁, e₁⟫_ℝ = 1)
    (h01 : ⟪e₀, e₁⟫_ℝ = 0) :
    chshVector e₀ e₁ (bPlus e₀ e₁) (bMinus e₀ e₁) =
      2 * Real.sqrt 2 := by
  have h10 : ⟪e₁, e₀⟫_ℝ = 0 := by
    rw [real_inner_comm]
    exact h01
  obtain ⟨he0, he1⟩ := orthonormal_norms e₀ e₁ h00 h11
  simp [chshVector, bPlus, bMinus, real_inner_smul_right, inner_add_right,
    inner_sub_right, h01, h10, he0, he1] <;> ring

theorem analytic_tsirelson_is_sharp
    (e₀ e₁ : H)
    (h00 : ⟪e₀, e₀⟫_ℝ = 1) (h11 : ⟪e₁, e₁⟫_ℝ = 1)
    (h01 : ⟪e₀, e₁⟫_ℝ = 0) :
    |chshVector e₀ e₁ (bPlus e₀ e₁) (bMinus e₀ e₁)| =
      2 * Real.sqrt 2 := by
  rw [standard_settings_attain_tsirelson e₀ e₁ h00 h11 h01,
    abs_of_nonneg (by positivity)]


/-- W7.2 analytic closure on the finite-vector scenario: the universal upper
bound and an exact saturating orthonormal construction are paired. -/
theorem analytic_tsirelson_bound_and_sharp
    (e₀ e₁ : H)
    (h00 : ⟪e₀, e₀⟫_ℝ = 1) (h11 : ⟪e₁, e₁⟫_ℝ = 1)
    (h01 : ⟪e₀, e₁⟫_ℝ = 0) :
    (∀ a₀ a₁ b₀ b₁ : H,
      ‖a₀‖ = 1 → ‖a₁‖ = 1 → ‖b₀‖ = 1 → ‖b₁‖ = 1 →
      |chshVector a₀ a₁ b₀ b₁| ≤ 2 * Real.sqrt 2) ∧
    |chshVector e₀ e₁ (bPlus e₀ e₁) (bMinus e₀ e₁)| =
      2 * Real.sqrt 2 := by
  exact ⟨fun a₀ a₁ b₀ b₁ => analytic_tsirelson_bound a₀ a₁ b₀ b₁,
    analytic_tsirelson_is_sharp e₀ e₁ h00 h11 h01⟩

end AnalyticTsirelson

/-! ## W7.1: sealed finite-matrix recovery from explicit imports -/

namespace FiniteMatrixSeal

open Wave6Completion

variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

abbrev Mat (n : Type*) := Matrix n n ℂ

def IsProjection (P : Mat n) : Prop :=
  P.IsHermitian ∧ P * P = P

def Orthogonal (P Q : Mat n) : Prop :=
  P * Q = 0 ∧ Q * P = 0

/-- A typed finitely additive probability assignment on projections. -/
structure ProjectionFrame (n : Type*) [Fintype n] [DecidableEq n] where
  value : Mat n → ℝ
  nonnegative : ∀ P, IsProjection P → 0 ≤ value P
  normalized : value 1 = 1
  orthogonalAdd : ∀ P Q, IsProjection P → IsProjection Q → Orthogonal P Q →
    value (P + Q) = value P + value Q

/-- Density matrices on the explicitly imported complex finite matrix host. -/
structure DensityMatrix (n : Type*) [Fintype n] [DecidableEq n] where
  matrix : Mat n
  positive : matrix.PosSemidef
  normalized : matrix.trace = 1

def BornRepresents (f : ProjectionFrame n) (ρ : DensityMatrix n) : Prop :=
  ∀ P, IsProjection P →
    f.value P = (ρ.matrix * P).trace.re

/-- Typed `GLEASON-ABS` import. It is deliberately a proposition requiring
a proof, not a flag. No inhabitant is manufactured in this packet.

**UNBOUNDED — do not use as the seal's import.** This quantifies over every
`[Fintype n]`, including cardinality 2, where Gleason's theorem is *false*
(it requires `dim ≥ 3`). Because `rec_full_iff_explicit_imports` makes the
sealed recovery **equivalent** to its imports, sealing on this predicate made the
seal equivalent to a false proposition at `d = 2` — the estate's only working
dimension — silently and unreachably. Retained as the raw statement; the seal
now consumes `BornSelectionImport` instead. -/
def GleasonAbsolute (n : Type*) [Fintype n] [DecidableEq n] : Prop :=
  ∀ f : ProjectionFrame n, ∃! ρ : DensityMatrix n, BornRepresents f ρ

/-! ### GLEASON-ABS dimension fence (repaired 2026-08-04)

Mirrors the Rust fence in
`omega_engine/crates/omega_quantum_physics/src/born_gleason.rs`, which already
refuses `dimension < 3` (`GleasonAssumptions::unpaid` pushes `dimension_ge_3`)
and records `OPEN_RESIDUAL_DIM2`. The two languages disagreed; Rust was right. -/

/-- Projection-lattice Gleason, fenced to its actual domain of validity.

The dimension bound is a **conjunct, not a hypothesis**. Written as
`3 ≤ Fintype.card n → …` the statement would be *vacuously true* at `d = 2`, so
the seal would become reachable at the estate's working dimension for exactly
the wrong reason — checklist laundering. As a conjunction it is honestly
**false** there, and `gleason_dim3plus_fails_at_dim_two` proves it. -/
def GleasonAbsoluteDim3Plus (n : Type*) [Fintype n] [DecidableEq n] : Prop :=
  3 ≤ Fintype.card n ∧ ∀ f : ProjectionFrame n, ∃! ρ : DensityMatrix n, BornRepresents f ρ

/-- An effect: `0 ⪯ E ⪯ 1`. -/
def IsEffect (E : Mat n) : Prop := E.PosSemidef ∧ (1 - E).PosSemidef

/-- A finitely additive frame function on **effects** rather than projections. -/
structure EffectFrame (n : Type*) [Fintype n] [DecidableEq n] where
  value : Mat n → ℝ
  nonnegative : ∀ E, IsEffect E → 0 ≤ value E
  normalized : value 1 = 1
  additive : ∀ E F, IsEffect E → IsEffect F → IsEffect (E + F) →
    value (E + F) = value E + value F

def BornRepresentsEffect (f : EffectFrame n) (ρ : DensityMatrix n) : Prop :=
  ∀ E, IsEffect E → f.value E = (ρ.matrix * E).trace.re

/-- `BUSCH-POVM-ABS` — the POVM frame-function variant
(Busch, *Phys. Rev. Lett.* **91** (2003) 120403), already cited by the corpus.

Carries **no** dimension restriction: it survives at `d = 2`, precisely where the
projection version fails. Still a typed import — no inhabitant is manufactured
here, and admitting it is a priced act. -/
def BuschPovmFrameAbsolute (n : Type*) [Fintype n] [DecidableEq n] : Prop :=
  ∀ f : EffectFrame n, ∃! ρ : DensityMatrix n, BornRepresentsEffect f ρ

/-- The Born-selection import, in one of its two honest forms. The seal consumes
this, never the unbounded `GleasonAbsolute`. -/
def BornSelectionImport (n : Type*) [Fintype n] [DecidableEq n] : Prop :=
  GleasonAbsoluteDim3Plus n ∨ BuschPovmFrameAbsolute n

/-- **The fence bites.** The projection route is unavailable at `d = 2`. -/
theorem gleason_dim3plus_fails_at_dim_two :
    ¬ GleasonAbsoluteDim3Plus (Fin 2) := by
  rintro ⟨h, -⟩
  simp at h

/-- **Non-vacuity.** The bound is satisfiable, so the fence is not "false
everywhere" — it discriminates. -/
theorem gleason_dim3plus_bound_reachable : 3 ≤ Fintype.card (Fin 3) := by
  simp

/-- **The load-bearing consequence.** At the estate's only working dimension the
Gleason disjunct is impossible, so any sealed recovery at `d = 2` is forced
through the Busch/POVM route. Born uniqueness at `d = 2` cannot be charged to
Gleason. -/
theorem dim_two_forces_busch_route (h : BornSelectionImport (Fin 2)) :
    BuschPovmFrameAbsolute (Fin 2) :=
  h.resolve_left gleason_dim3plus_fails_at_dim_two

/-- When its bound is paid, the fenced route still delivers the unbounded body. -/
theorem gleason_dim3plus_gives_absolute {m : Type*} [Fintype m] [DecidableEq m]
    (h : GleasonAbsoluteDim3Plus m) : GleasonAbsolute m := h.2

abbrev FrozenClaims := Wave6Completion.SealedSufficiency.FrozenRecoveryClaims
abbrev RecoveryTarget := Wave6Completion.SealedSufficiency.Target

/-- The exact external evidence needed to seal W7.1. -/
structure RecoveryImports (C : FrozenClaims) (n : Type*)
    [Fintype n] [DecidableEq n] : Prop where
  wave6 : Wave6Completion.SealedSufficiency.SealedImportEvidence C
  bornSelection : BornSelectionImport n

/-- A proof-carrying finite-matrix recovery package. Every field states an
actual theorem; there are no string ledgers or booleans in the seal. -/
structure SealedFiniteMatrixRecovery (C : FrozenClaims) (n : Type*)
    [Fintype n] [DecidableEq n] [Nonempty n] : Prop where
  wave6Targets : ∀ t : RecoveryTarget,
    Wave6Completion.SealedSufficiency.claimAt C t
  bornSelection : BornSelectionImport n
  spectral : ∀ (A : Mat n), A.IsHermitian →
    ∃ (U : Matrix.unitaryGroup n ℂ) (eigenvalues : n → ℝ),
      A = (U : Mat n) * Matrix.diagonal (RCLike.ofReal ∘ eigenvalues) *
        star (U : Mat n)
  finiteInstruments : ∀ {outcome : Type} [Fintype outcome] [DecidableEq outcome],
    ∀ P : Wave6Completion.FinitePOVM (n := n) (outcome := outcome),
      (∀ i, (P.sqrtInstrument.effect i).PosSemidef) ∧
      (∑ i, P.sqrtInstrument.effect i = 1) ∧
      (∀ i ρ, ρ.PosSemidef → (P.sqrtInstrument.branch i ρ).PosSemidef) ∧
      (∀ ρ, (P.sqrtInstrument.channel ρ).trace = ρ.trace)
  analyticChsh : ∀ {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℝ H],
    ∀ a₀ a₁ b₀ b₁ : H,
      ‖a₀‖ = 1 → ‖a₁‖ = 1 → ‖b₀‖ = 1 → ‖b₁‖ = 1 →
      |AnalyticTsirelson.chshVector a₀ a₁ b₀ b₁| ≤ 2 * Real.sqrt 2
  contextualOperators : ∀ c : MerminPeresObserver.C,
    OperatorMerminPeres.complexContextProduct c =
      if c = MerminPeresObserver.C.c3
      then -(1 : OperatorMerminPeres.CM4) else 1

/-- `REC-FULL-THEOREM`, conditional on the explicitly typed Wave-6 and
Gleason receipts. Complex matrices and Born uniqueness are imports here. -/
theorem rec_full_theorem_conditional
    (C : FrozenClaims) (I : RecoveryImports C n) :
    SealedFiniteMatrixRecovery C n where
  wave6Targets :=
    Wave6Completion.SealedSufficiency.sealed_sufficiency_conditional C I.wave6
  bornSelection := I.bornSelection
  spectral := Wave6Completion.hermitian_general_n
  finiteInstruments := fun P => Wave6Completion.general_povm_finite P
  analyticChsh := fun a₀ a₁ b₀ b₁ ha₀ ha₁ hb₀ hb₁ =>
    AnalyticTsirelson.analytic_tsirelson_bound a₀ a₁ b₀ b₁ ha₀ ha₁ hb₀ hb₁
  contextualOperators := OperatorMerminPeres.complex_context_products_exact

/-- Exact residual theorem: the sealed W7.1 package is equivalent to the
two explicit receipts. Thus a build cannot silently manufacture Gleason. -/
theorem rec_full_iff_explicit_imports (C : FrozenClaims) :
    SealedFiniteMatrixRecovery C n ↔ RecoveryImports C n := by
  constructor
  · intro R
    exact {
      wave6 :=
        (Wave6Completion.SealedSufficiency.sealed_evidence_iff_all_targets C).2
          R.wave6Targets
      bornSelection := R.bornSelection }
  · exact rec_full_theorem_conditional C

/-- The absolute Born-selection residual remains a typed import boundary. -/
theorem gleason_is_not_obtained_from_matrix_construction_alone
    (C : FrozenClaims) (R : SealedFiniteMatrixRecovery C n) :
    BornSelectionImport n :=
  R.bornSelection

end FiniteMatrixSeal

end Wave7Completion
end QM

-- W7.1 Gleason dimension fence (2026-08-04).
#print axioms QM.Wave7Completion.FiniteMatrixSeal.gleason_dim3plus_fails_at_dim_two
#print axioms QM.Wave7Completion.FiniteMatrixSeal.gleason_dim3plus_bound_reachable
#print axioms QM.Wave7Completion.FiniteMatrixSeal.dim_two_forces_busch_route
#print axioms QM.Wave7Completion.FiniteMatrixSeal.gleason_dim3plus_gives_absolute
#print axioms QM.Wave7Completion.FiniteMatrixSeal.rec_full_iff_explicit_imports
#print axioms QM.Wave7Completion.FiniteMatrixSeal.gleason_is_not_obtained_from_matrix_construction_alone
