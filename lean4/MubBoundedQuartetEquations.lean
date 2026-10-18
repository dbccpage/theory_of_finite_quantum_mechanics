import MubBoundedBlockChart

/-!
# Division-free equations on the bounded block chart

AuthorityEffect: None.

Determinant denominators are cleared only under the proved positive bound.
The displayed matrix equations are not an infeasibility certificate.
-/

noncomputable section
namespace MUB.BoundedQuartetEquations
open BoundedBlockChart MonomialTransport

def detNorm (B : Mat3) : ℝ := Complex.normSq B.det
def denominator (B : Mat3) : ℂ := star B.det
def numerator (E B C : Mat3) : Mat3 := -(C * E.conjTranspose * B.adjugate.conjTranspose)

theorem denominator_ne_zero (B : Mat3) (hb : (54 / 5 : ℝ) ≤ detNorm B) :
    denominator B ≠ 0 := by
  have hd : B.det ≠ 0 := by
    intro hz
    norm_num [detNorm, hz] at hb
  simpa [denominator] using hd

theorem detNorm_pos (B : Mat3) (hb : (54 / 5 : ℝ) ≤ detNorm B) : 0 < detNorm B :=
  lt_of_lt_of_le (by norm_num) hb

theorem forcedD_eq_inv_smul (E B C : Mat3) :
    forcedD E B C = (denominator B)⁻¹ • numerator E B C := by
  simp [forcedD, numerator, denominator, Matrix.inv_def, Ring.inverse_eq_inv,
    Matrix.conjTranspose_smul, smul_neg]

theorem scaled_forcedD (E B C : Mat3) (hb : (54 / 5 : ℝ) ≤ detNorm B) :
    denominator B • forcedD E B C = numerator E B C := by
  rw [forcedD_eq_inv_smul, smul_smul, mul_inv_cancel₀ (denominator_ne_zero B hb), one_smul]

theorem numerator_entry_normSq (E B C : Mat3) (hb : (54 / 5 : ℝ) ≤ detNorm B)
    (i j : I3) :
    Complex.normSq (numerator E B C i j) = detNorm B * Complex.normSq (forcedD E B C i j) := by
  rw [← scaled_forcedD E B C hb, Matrix.smul_apply, smul_eq_mul, Complex.normSq_mul]
  simp [denominator, detNorm]

theorem numerator_gram (E B C : Mat3) (hb : (54 / 5 : ℝ) ≤ detNorm B) :
    numerator E B C * (numerator E B C).conjTranspose =
      (detNorm B : ℂ) • (forcedD E B C * (forcedD E B C).conjTranspose) := by
  have hs : denominator B * star (denominator B) = (detNorm B : ℂ) := by
    simpa [denominator, detNorm, Complex.star_def] using
      (Complex.normSq_eq_conj_mul_self (z := B.det)).symm
  rw [← scaled_forcedD E B C hb, Matrix.conjTranspose_smul, Matrix.smul_mul,
    Matrix.mul_smul, smul_smul, hs]

structure BlockEquations (E B C : Mat3) : Prop where
  unitE : UnitEntries E
  unitB : UnitEntries B
  unitC : UnitEntries C
  rowE : ∀ j, E 0 j = 1
  columnE : ∀ i, E i 0 = 1
  rowB : ∀ j, B 0 j = 1
  columnC : ∀ i, C i 0 = 1
  determinant_bound : (54 / 5 : ℝ) ≤ detNorm B
  topGram : E * E.conjTranspose + B * B.conjTranspose = (6 : ℂ) • (1 : Mat3)
  bottomGram : (detNorm B : ℂ) • (C * C.conjTranspose) +
    numerator E B C * (numerator E B C).conjTranspose =
      (6 * (detNorm B : ℂ)) • (1 : Mat3)
  numeratorNorm : ∀ i j, Complex.normSq (numerator E B C i j) = detNorm B

theorem blockEquations_iff_admissible (E B C : Mat3) :
    BlockEquations E B C ↔ Admissible E B C := by
  constructor
  · intro h
    have hq : (detNorm B : ℂ) ≠ 0 := by exact_mod_cast (detNorm_pos B h.determinant_bound).ne'
    refine ⟨h.unitE, h.unitB, h.unitC, h.rowE, h.columnE, h.rowB, h.columnC,
      h.determinant_bound, h.topGram, ?_, ?_⟩
    · apply smul_right_injective Mat3 hq
      dsimp only
      rw [smul_add, ← numerator_gram E B C h.determinant_bound]
      simpa [smul_smul, mul_comm] using h.bottomGram
    · intro i j
      apply mul_left_cancel₀ (detNorm_pos B h.determinant_bound).ne'
      rw [← numerator_entry_normSq E B C h.determinant_bound, h.numeratorNorm, mul_one]
  · intro h
    refine ⟨h.unitE, h.unitB, h.unitC, h.rowE, h.columnE, h.rowB, h.columnC,
      h.determinant_bound, h.topGram, ?_, ?_⟩
    · rw [numerator_gram E B C h.determinant_bound, ← smul_add, h.bottomGram, smul_smul]
      congr 1
      ring
    · intro i j
      rw [numerator_entry_normSq E B C h.determinant_bound, h.unitD, mul_one]

def scaledCompletion (E B C : Mat3) : Mat6 :=
  Matrix.fromBlocks (denominator B • E) (denominator B • B)
    (denominator B • C) (numerator E B C)

theorem scaled_completion (E B C : Mat3) (hb : (54 / 5 : ℝ) ≤ detNorm B) :
    denominator B • completion E B C = scaledCompletion E B C := by
  rw [completion, Matrix.fromBlocks_smul, scaled_forcedD E B C hb]
  rfl

theorem scaled_transition_normSq (E B C : Mat3) (U : Mat6)
    (hb : (54 / 5 : ℝ) ≤ detNorm B) (i j : I6) :
    Complex.normSq (((scaledCompletion E B C).conjTranspose * U) i j) =
      detNorm B * Complex.normSq (((completion E B C).conjTranspose * U) i j) := by
  rw [← scaled_completion E B C hb, Matrix.conjTranspose_smul, Matrix.smul_mul,
    Matrix.smul_apply, smul_eq_mul, Complex.normSq_mul]
  simp [denominator, detNorm]

theorem scaled_mu_iff (E B C : Mat3) (U : Mat6)
    (hb : (54 / 5 : ℝ) ≤ detNorm B) :
    (∀ i j, Complex.normSq (((scaledCompletion E B C).conjTranspose * U) i j) =
      6 * detNorm B) ↔ RawMU (completion E B C) U := by
  have hcard : (Fintype.card I6 : ℝ) = 6 := by norm_num [Fintype.card_sum]
  simp only [RawMU, hcard]
  constructor
  · intro h i j
    apply mul_left_cancel₀ (detNorm_pos B hb).ne'
    rw [← scaled_transition_normSq E B C U hb, h, mul_comm]
  · intro h i j
    rw [scaled_transition_normSq E B C U hb, h, mul_comm]

def candidateGauge (U : Mat6) : Mat6 :=
  action U (Equiv.refl _) (Equiv.refl _) (fun _ => 1) (fun j => star (U (Sum.inl 0) j))

def FirstRow (U : Mat6) : Prop := ∀ j, U (Sum.inl 0) j = 1

theorem candidateGauge_firstRow (U : Mat6) (hU : RawHadamard U) : FirstRow (candidateGauge U) := by
  intro j
  have h := congrArg (fun x : ℝ => (x : ℂ)) (hU.1 (Sum.inl 0) j)
  simpa [candidateGauge, action, Complex.normSq_eq_conj_mul_self,
    Complex.star_def, mul_comm] using h

theorem hasRawQuartet_iff_gauged (H : Mat6) :
    HasRawQuartet H ↔ RawHadamard H ∧ ∃ U V : Mat6,
      RawHadamard U ∧ RawHadamard V ∧ RawMU H U ∧ RawMU H V ∧ RawMU U V ∧
      FirstRow U ∧ FirstRow V := by
  constructor
  · rintro ⟨hH, U, V, hU, hV, hHU, hHV, hUV⟩
    have hone : ∀ j : I6, Complex.normSq (1 : ℂ) = 1 := by intro j; simp
    have hc : ∀ j, Complex.normSq (star (U (Sum.inl 0) j)) = 1 := by
      intro j
      simpa using hU.1 (Sum.inl 0) j
    have hd : ∀ j, Complex.normSq (star (V (Sum.inl 0) j)) = 1 := by
      intro j
      simpa using hV.1 (Sum.inl 0) j
    have hHid : action H (Equiv.refl _) (Equiv.refl _) (fun _ => 1) (fun _ => 1) = H := by
      ext i j
      simp [action]
    refine ⟨hH, candidateGauge U, candidateGauge V,
      action_hadamard _ _ _ _ _ hone hc hU,
      action_hadamard _ _ _ _ _ hone hd hV, ?_, ?_, ?_,
      candidateGauge_firstRow U hU, candidateGauge_firstRow V hV⟩
    · simpa only [candidateGauge, hHid] using
        action_mu H U (Equiv.refl _) (Equiv.refl _) (Equiv.refl _) _ _ _ hone hone hc hHU
    · simpa only [candidateGauge, hHid] using
        action_mu H V (Equiv.refl _) (Equiv.refl _) (Equiv.refl _) _ _ _ hone hone hd hHV
    · exact action_mu U V _ _ _ _ _ _ hone hc hd hUV
  · rintro ⟨hH, U, V, hU, hV, hHU, hHV, hUV, _, _⟩
    exact ⟨hH, U, V, hU, hV, hHU, hHV, hUV⟩

/-- Only addition, multiplication, conjugation, determinant, adjugate and norm-square
occur in these fields; the forced inverse block is absent. -/
structure QuartetEquations (E B C : Mat3) (U V : Mat6) : Prop extends BlockEquations E B C where
  rawU : RawHadamard U
  rawV : RawHadamard V
  rowU : FirstRow U
  rowV : FirstRow V
  scaledMU_U : ∀ i j, Complex.normSq (((scaledCompletion E B C).conjTranspose * U) i j) =
    6 * detNorm B
  scaledMU_V : ∀ i j, Complex.normSq (((scaledCompletion E B C).conjTranspose * V) i j) =
    6 * detNorm B
  muUV : RawMU U V

theorem equations_iff_admissible_quartet (E B C : Mat3) :
    (∃ U V : Mat6, QuartetEquations E B C U V) ↔
      Admissible E B C ∧ HasRawQuartet (completion E B C) := by
  constructor
  · rintro ⟨U, V, h⟩
    have ha := (blockEquations_iff_admissible E B C).mp h.toBlockEquations
    exact ⟨ha, ha.hadamard, U, V, h.rawU, h.rawV,
      (scaled_mu_iff E B C U h.determinant_bound).mp h.scaledMU_U,
      (scaled_mu_iff E B C V h.determinant_bound).mp h.scaledMU_V, h.muUV⟩
  · rintro ⟨ha, hQ⟩
    obtain ⟨_, U, V, hU, hV, hHU, hHV, hUV, hrU, hrV⟩ := hasRawQuartet_iff_gauged _ |>.mp hQ
    exact ⟨U, V, {
      toBlockEquations := (blockEquations_iff_admissible E B C).mpr ha
      rawU := hU, rawV := hV, rowU := hrU, rowV := hrV
      scaledMU_U := (scaled_mu_iff E B C U ha.determinant_bound).mpr hHU
      scaledMU_V := (scaled_mu_iff E B C V ha.determinant_bound).mpr hHV
      muUV := hUV }⟩

theorem exists_quartet_iff_equations :
    (∃ Q : Fin 4 → Mat (Fin 6), SzollosiQuartetSystem.Quartet Q) ↔
      ∃ (E B C : Mat3) (U V : Mat6), QuartetEquations E B C U V := by
  rw [exists_quartet_iff_bounded_completion]
  constructor
  · rintro ⟨E, B, C, ha, hQ⟩
    obtain ⟨U, V, h⟩ := (equations_iff_admissible_quartet E B C).mpr ⟨ha, hQ⟩
    exact ⟨E, B, C, U, V, h⟩
  · rintro ⟨E, B, C, U, V, h⟩
    exact ⟨E, B, C, (equations_iff_admissible_quartet E B C).mp ⟨U, V, h⟩⟩

theorem no_quartet_iff_no_equations :
    (∀ Q : Fin 4 → Mat (Fin 6), ¬ SzollosiQuartetSystem.Quartet Q) ↔
      ∀ (E B C : Mat3) (U V : Mat6), ¬ QuartetEquations E B C U V := by
  constructor
  · intro hn E B C U V h
    obtain ⟨Q, hQ⟩ := exists_quartet_iff_equations.mpr ⟨E, B, C, U, V, h⟩
    exact hn Q hQ
  · intro hn Q hQ
    obtain ⟨E, B, C, U, V, h⟩ := exists_quartet_iff_equations.mp ⟨Q, hQ⟩
    exact hn E B C U V h

theorem real_bounds_of_unit (z : ℂ) (hz : Complex.normSq z = 1) :
    -1 ≤ z.re ∧ z.re ≤ 1 ∧ -1 ≤ z.im ∧ z.im ≤ 1 := by
  have hs : z.re ^ 2 + z.im ^ 2 = 1 := by simpa [Complex.normSq_apply, pow_two] using hz
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    nlinarith [sq_nonneg z.re, sq_nonneg z.im, sq_nonneg (z.re + 1),
      sq_nonneg (z.re - 1), sq_nonneg (z.im + 1), sq_nonneg (z.im - 1)]

#print axioms denominator_ne_zero
#print axioms forcedD_eq_inv_smul
#print axioms scaled_forcedD
#print axioms numerator_entry_normSq
#print axioms numerator_gram
#print axioms blockEquations_iff_admissible
#print axioms scaled_completion
#print axioms scaled_transition_normSq
#print axioms scaled_mu_iff
#print axioms candidateGauge_firstRow
#print axioms hasRawQuartet_iff_gauged
#print axioms equations_iff_admissible_quartet
#print axioms exists_quartet_iff_equations
#print axioms no_quartet_iff_no_equations
#print axioms real_bounds_of_unit
end MUB.BoundedQuartetEquations
