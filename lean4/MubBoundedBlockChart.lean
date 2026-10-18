import MubMinorChart
import MubIndexTransport
import MubQuartetTransportBridge
import Mathlib.Data.Matrix.Block
import Mathlib.Logic.Equiv.Fin.Basic

/-!
# A bounded block chart for actual six-dimensional Hadamards

AuthorityEffect: None.

The selected minor is placed in the upper-right block, then the entire
matrix is dephased by an actual monomial action. No finite-fibre assertion
or nonextension statement is assumed.
-/

noncomputable section
namespace MUB.BoundedBlockChart
open MonomialTransport
open scoped BigOperators

abbrev I3 := Fin 3
abbrev I6 := Fin 3 ⊕ Fin 3
abbrev Mat3 := Matrix I3 I3 ℂ
abbrev Mat6 := Matrix I6 I6 ℂ

def blockIndex : I6 ≃ Fin 6 := finSumFinEquiv

def columnOrder (s : Fin 20) (j : Fin 6) : Fin 6 :=
  Fin.addCases (m := 3) (n := 3) (motive := fun _ => Fin 6)
    (MinorChart.columns s.rev) (MinorChart.columns s) j

theorem columnOrder_bijective (s : Fin 20) : Function.Bijective (columnOrder s) := by
  revert s
  decide

def columnPerm (s : Fin 20) : Equiv.Perm (Fin 6) :=
  Equiv.ofBijective (columnOrder s) (columnOrder_bijective s)

@[simp] theorem columnPerm_right (s : Fin 20) (j : Fin 3) :
    columnPerm s (Fin.natAdd 3 j) = MinorChart.columns s j := by
  change columnOrder s (Fin.natAdd 3 j) = _
  unfold columnOrder
  rw [Fin.addCases_right]

private theorem phase_cancel (z : ℂ) (hz : Complex.normSq z = 1) :
    star z * z = 1 := by
  simpa [Complex.star_def, Complex.normSq_eq_conj_mul_self] using
    congrArg (fun x : ℝ => (x : ℂ)) hz

def rowPhase (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6)) (i : Fin 6) : ℂ :=
  star (H i (τ 0))

def columnPhase (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6)) (j : Fin 6) : ℂ :=
  H 0 (τ 0) * star (H 0 (τ j))

def dephase (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6)) : Mat (Fin 6) :=
  action H (Equiv.refl _) τ (rowPhase H τ) (columnPhase H τ)

theorem rowPhase_unit (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6))
    (hH : ∀ i j, Complex.normSq (H i j) = 1) (i : Fin 6) :
    Complex.normSq (rowPhase H τ i) = 1 := by
  simp [rowPhase, hH]

theorem columnPhase_unit (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6))
    (hH : ∀ i j, Complex.normSq (H i j) = 1) (j : Fin 6) :
    Complex.normSq (columnPhase H τ j) = 1 := by
  simp [columnPhase, Complex.normSq_mul, hH]

theorem dephase_equivalent (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6))
    (hH : ∀ i j, Complex.normSq (H i j) = 1) : MonomialEquivalent H (dephase H τ) :=
  ⟨Equiv.refl _, τ, rowPhase H τ, columnPhase H τ,
    rowPhase_unit H τ hH, columnPhase_unit H τ hH, rfl⟩

theorem dephase_firstRow (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6))
    (hH : ∀ i j, Complex.normSq (H i j) = 1) (j : Fin 6) :
    dephase H τ 0 j = 1 := by
  change star (H 0 (τ 0)) * H 0 (τ j) * (H 0 (τ 0) * star (H 0 (τ j))) = 1
  calc
    _ = (star (H 0 (τ 0)) * H 0 (τ 0)) *
        (star (H 0 (τ j)) * H 0 (τ j)) := by ring
    _ = 1 := by rw [phase_cancel _ (hH _ _), phase_cancel _ (hH _ _)]; simp

theorem dephase_firstColumn (H : Mat (Fin 6)) (τ : Equiv.Perm (Fin 6))
    (hH : ∀ i j, Complex.normSq (H i j) = 1) (i : Fin 6) :
    dephase H τ i 0 = 1 := by
  change star (H i (τ 0)) * H i (τ 0) * (H 0 (τ 0) * star (H 0 (τ 0))) = 1
  rw [phase_cancel _ (hH _ _), mul_comm (H 0 (τ 0)), phase_cancel _ (hH _ _)]
  simp

theorem rephase_det_normSq (A : Mat3) (r c : I3 → ℂ)
    (hr : ∀ i, Complex.normSq (r i) = 1)
    (hc : ∀ j, Complex.normSq (c j) = 1) :
    Complex.normSq (Matrix.of (fun i j => r i * A i j * c j)).det =
      Complex.normSq A.det := by
  have heq : Matrix.of (fun i j => r i * A i j * c j) =
      Matrix.diagonal r * A * Matrix.diagonal c := by
    ext i j
    simp
  rw [heq, Matrix.det_mul, Matrix.det_mul, Matrix.det_diagonal, Matrix.det_diagonal]
  simp [Complex.normSq_mul, map_prod, hr, hc]

def chart (H : Mat (Fin 6)) (s : Fin 20) : Mat6 :=
  pullMatrix blockIndex (dephase H (columnPerm s))

theorem chart_upperRight_det_normSq (H : Mat (Fin 6)) (s : Fin 20)
    (hH : ∀ i j, Complex.normSq (H i j) = 1) :
    Complex.normSq (chart H s).toBlocks₁₂.det =
      Complex.normSq (MinorChart.minor (MinorChart.firstRows H) s).det := by
  have heq : (chart H s).toBlocks₁₂ = Matrix.of (fun i j =>
      rowPhase H (columnPerm s) (Fin.castAdd 3 i) *
      MinorChart.minor (MinorChart.firstRows H) s i j *
      columnPhase H (columnPerm s) (Fin.natAdd 3 j)) := by
    ext i j
    change rowPhase H (columnPerm s) (Fin.castAdd 3 i) *
      H (Fin.castAdd 3 i) (columnPerm s (Fin.natAdd 3 j)) *
      columnPhase H (columnPerm s) (Fin.natAdd 3 j) =
      rowPhase H (columnPerm s) (Fin.castAdd 3 i) *
      H (Fin.castAdd 3 i) (MinorChart.columns s j) *
      columnPhase H (columnPerm s) (Fin.natAdd 3 j)
    rw [columnPerm_right]
  rw [heq]
  exact rephase_det_normSq _ _ _ (fun i => rowPhase_unit _ _ hH _)
    (fun j => columnPhase_unit _ _ hH _)

theorem chart_hadamard (H : Mat (Fin 6)) (s : Fin 20) (hH : RawHadamard H) :
    RawHadamard (chart H s) := by
  apply pullMatrix_hadamard
  exact action_hadamard _ _ _ _ _ (rowPhase_unit _ _ hH.1)
    (columnPhase_unit _ _ hH.1) hH

theorem chart_hasRawQuartet_iff (H : Mat (Fin 6)) (s : Fin 20)
    (hH : RawHadamard H) : HasRawQuartet (chart H s) ↔ HasRawQuartet H := by
  rw [chart, hasRawQuartet_pull_iff]
  exact (hasRawQuartet_iff_of_monomialEquivalent (dephase_equivalent _ _ hH.1)).symm

theorem six_mul_comm {ι : Type*} [Fintype ι] [DecidableEq ι] (A B : Mat ι)
    (h : A * B = (6 : ℂ) • (1 : Mat ι)) :
    B * A = (6 : ℂ) • (1 : Mat ι) := by
  have hs : ((1 / 6 : ℂ) • A) * B = 1 := by
    rw [Matrix.smul_mul, h, smul_smul]
    norm_num
  have ht := mul_eq_one_comm.mp hs
  rw [Matrix.mul_smul] at ht
  calc
    B * A = (6 : ℂ) • ((1 / 6 : ℂ) • (B * A)) := by
      rw [smul_smul]
      norm_num
    _ = (6 : ℂ) • (1 : Mat ι) := by rw [ht]

theorem chart_firstRow (H : Mat (Fin 6)) (s : Fin 20)
    (hH : ∀ i j, Complex.normSq (H i j) = 1) (j : I6) :
    chart H s (Sum.inl 0) j = 1 := by
  exact dephase_firstRow H (columnPerm s) hH (blockIndex j)

theorem chart_firstColumn (H : Mat (Fin 6)) (s : Fin 20)
    (hH : ∀ i j, Complex.normSq (H i j) = 1) (i : I6) :
    chart H s i (Sum.inl 0) = 1 := by
  exact dephase_firstColumn H (columnPerm s) hH (blockIndex i)

theorem rowGram_blocks (E B C D : Mat3)
    (h : Matrix.fromBlocks E B C D * (Matrix.fromBlocks E B C D).conjTranspose =
      (6 : ℂ) • (1 : Mat6)) :
    E * E.conjTranspose + B * B.conjTranspose = (6 : ℂ) • (1 : Mat3) ∧
    C * E.conjTranspose + D * B.conjTranspose = 0 ∧
    C * C.conjTranspose + D * D.conjTranspose = (6 : ℂ) • (1 : Mat3) := by
  have htop := congrArg Matrix.toBlocks₁₁ h
  have hcross := congrArg Matrix.toBlocks₂₁ h
  have hbottom := congrArg Matrix.toBlocks₂₂ h
  rw [Matrix.fromBlocks_conjTranspose, Matrix.fromBlocks_multiply,
    Matrix.toBlocks_fromBlocks₁₁] at htop
  rw [Matrix.fromBlocks_conjTranspose, Matrix.fromBlocks_multiply,
    Matrix.toBlocks_fromBlocks₂₁] at hcross
  rw [Matrix.fromBlocks_conjTranspose, Matrix.fromBlocks_multiply,
    Matrix.toBlocks_fromBlocks₂₂] at hbottom
  refine ⟨htop.trans ?_, hcross.trans ?_, hbottom.trans ?_⟩
  all_goals
    ext i j
    simp [Matrix.toBlocks₁₁, Matrix.toBlocks₂₁, Matrix.toBlocks₂₂,
      Matrix.smul_apply, Matrix.one_apply]

def forcedD (E B C : Mat3) : Mat3 :=
  -(C * E.conjTranspose * (B⁻¹).conjTranspose)

theorem recover_lowerRight (E B C D : Mat3) (hB : IsUnit B.det)
    (hcross : C * E.conjTranspose + D * B.conjTranspose = 0) :
    D = forcedD E B C := by
  have hinv : B.conjTranspose * (B⁻¹).conjTranspose = 1 := by
    rw [← Matrix.conjTranspose_mul, Matrix.nonsing_inv_mul B hB]
    simp
  have h := congrArg (fun M : Mat3 => M * (B⁻¹).conjTranspose) hcross
  simp only [Matrix.add_mul, Matrix.mul_assoc, hinv, Matrix.mul_one, Matrix.zero_mul] at h
  unfold forcedD
  apply eq_neg_iff_add_eq_zero.mpr
  simpa only [add_comm, Matrix.mul_assoc] using h

theorem forced_cross (E B C : Mat3) (hB : IsUnit B.det) :
    C * E.conjTranspose + forcedD E B C * B.conjTranspose = 0 := by
  have hinv : (B⁻¹).conjTranspose * B.conjTranspose = 1 := by
    rw [← Matrix.conjTranspose_mul, Matrix.mul_nonsing_inv B hB]
    simp
  simp only [forcedD, neg_mul, Matrix.mul_assoc, hinv, Matrix.mul_one, add_neg_cancel]

def completion (E B C : Mat3) : Mat6 := Matrix.fromBlocks E B C (forcedD E B C)

def UnitEntries (A : Mat3) : Prop := ∀ i j, Complex.normSq (A i j) = 1

/-- Explicit equations and a positive determinant bound, with no finite-fibre premise. -/
structure Admissible (E B C : Mat3) : Prop where
  unitE : UnitEntries E
  unitB : UnitEntries B
  unitC : UnitEntries C
  rowE : ∀ j, E 0 j = 1
  columnE : ∀ i, E i 0 = 1
  rowB : ∀ j, B 0 j = 1
  columnC : ∀ i, C i 0 = 1
  determinant_bound : (54 / 5 : ℝ) ≤ Complex.normSq B.det
  topGram : E * E.conjTranspose + B * B.conjTranspose = (6 : ℂ) • (1 : Mat3)
  bottomGram : C * C.conjTranspose + forcedD E B C * (forcedD E B C).conjTranspose =
    (6 : ℂ) • (1 : Mat3)
  unitD : UnitEntries (forcedD E B C)

theorem Admissible.det_isUnit {E B C : Mat3} (h : Admissible E B C) : IsUnit B.det := by
  apply isUnit_iff_ne_zero.mpr
  intro hz
  have hb := h.determinant_bound
  norm_num [hz] at hb

theorem Admissible.inverse_bound {E B C : Mat3} (h : Admissible E B C) (i j : I3) :
    Complex.normSq (B⁻¹ i j) ≤ 10 / 27 :=
  MinorChart.inverse_entry_normSq_le B h.unitB h.determinant_bound i j

theorem Admissible.hadamard {E B C : Mat3} (h : Admissible E B C) :
    RawHadamard (completion E B C) := by
  have hcross := forced_cross E B C h.det_isUnit
  have hcross' : E * C.conjTranspose + B * (forcedD E B C).conjTranspose = 0 := by
    have ht := congrArg Matrix.conjTranspose hcross
    simpa using ht
  have hrow : completion E B C * (completion E B C).conjTranspose =
      (6 : ℂ) • (1 : Mat6) := by
    rw [completion, Matrix.fromBlocks_conjTranspose, Matrix.fromBlocks_multiply,
      h.topGram, h.bottomGram, hcross, hcross']
    ext i j
    cases i <;> cases j <;> simp [Matrix.fromBlocks, Matrix.smul_apply, Matrix.one_apply]
  constructor
  · rintro (i | i) (j | j)
    · exact h.unitE i j
    · exact h.unitB i j
    · exact h.unitC i j
    · exact h.unitD i j
  · simpa using six_mul_comm _ _ hrow

theorem exists_admissible_chart (H : Mat (Fin 6)) (hH : RawHadamard H) :
    ∃ s : Fin 20,
      Admissible (chart H s).toBlocks₁₁ (chart H s).toBlocks₁₂ (chart H s).toBlocks₂₁ ∧
      chart H s = completion (chart H s).toBlocks₁₁
        (chart H s).toBlocks₁₂ (chart H s).toBlocks₂₁ := by
  have hrow : H * H.conjTranspose = (6 : ℂ) • (1 : Mat (Fin 6)) :=
    six_mul_comm _ _ (by simpa using hH.2)
  obtain ⟨s, hs, _⟩ := MinorChart.exists_invertible_minor H hrow
  let K := chart H s
  let E := K.toBlocks₁₁
  let B := K.toBlocks₁₂
  let C := K.toBlocks₂₁
  let D := K.toBlocks₂₂
  have hK : RawHadamard K := chart_hadamard H s hH
  have hrowK : K * K.conjTranspose = (6 : ℂ) • (1 : Mat6) :=
    six_mul_comm _ _ (by simpa using hK.2)
  have hg := rowGram_blocks E B C D (by
    simpa only [E, B, C, D, Matrix.fromBlocks_toBlocks] using hrowK)
  have hb : (54 / 5 : ℝ) ≤ Complex.normSq B.det := by
    change (54 / 5 : ℝ) ≤ Complex.normSq (chart H s).toBlocks₁₂.det
    rw [chart_upperRight_det_normSq H s hH.1]
    exact hs
  have hbunit : IsUnit B.det := by
    apply isUnit_iff_ne_zero.mpr
    intro hz
    norm_num [hz] at hb
  have hD := recover_lowerRight E B C D hbunit hg.2.1
  have ha : Admissible E B C := {
    unitE := fun i j => hK.1 (Sum.inl i) (Sum.inl j)
    unitB := fun i j => hK.1 (Sum.inl i) (Sum.inr j)
    unitC := fun i j => hK.1 (Sum.inr i) (Sum.inl j)
    rowE := fun j => chart_firstRow H s hH.1 (Sum.inl j)
    columnE := fun i => chart_firstColumn H s hH.1 (Sum.inl i)
    rowB := fun j => chart_firstRow H s hH.1 (Sum.inr j)
    columnC := fun i => chart_firstColumn H s hH.1 (Sum.inr i)
    determinant_bound := hb
    topGram := hg.1
    bottomGram := by rw [← hD]; exact hg.2.2
    unitD := by rw [← hD]; exact fun i j => hK.1 (Sum.inr i) (Sum.inr j) }
  refine ⟨s, ha, ?_⟩
  calc
    K = Matrix.fromBlocks E B C D := (Matrix.fromBlocks_toBlocks K).symm
    _ = completion E B C := by rw [hD]; rfl

theorem exists_admissible_completion_of_rawQuartet
    (H : Mat (Fin 6)) (hH : HasRawQuartet H) :
    ∃ E B C : Mat3, Admissible E B C ∧ HasRawQuartet (completion E B C) := by
  obtain ⟨s, ha, hEq⟩ := exists_admissible_chart H hH.1
  refine ⟨(chart H s).toBlocks₁₁, (chart H s).toBlocks₁₂, (chart H s).toBlocks₂₁, ha, ?_⟩
  rw [← hEq]
  exact (chart_hasRawQuartet_iff H s hH.1).mpr hH

theorem exists_quartet_iff_bounded_completion :
    (∃ Q : Fin 4 → Mat (Fin 6), SzollosiQuartetSystem.Quartet Q) ↔
      ∃ E B C : Mat3, Admissible E B C ∧ HasRawQuartet (completion E B C) := by
  rw [exists_quartet_iff_exists_rawQuartet]
  constructor
  · rintro ⟨H, hH⟩
    exact exists_admissible_completion_of_rawQuartet H hH
  · rintro ⟨E, B, C, _, hQ⟩
    exact (exists_rawQuartet_index_iff blockIndex).mpr ⟨completion E B C, hQ⟩

theorem no_quartet_iff_bounded_nonextension :
    (∀ Q : Fin 4 → Mat (Fin 6), ¬ SzollosiQuartetSystem.Quartet Q) ↔
      ∀ E B C : Mat3, Admissible E B C → ¬ HasRawQuartet (completion E B C) := by
  constructor
  · intro hn E B C ha hQ
    obtain ⟨Q, hQ⟩ := exists_quartet_iff_bounded_completion.mpr ⟨E, B, C, ha, hQ⟩
    exact hn Q hQ
  · intro hn Q hQ
    obtain ⟨E, B, C, ha, hc⟩ := exists_quartet_iff_bounded_completion.mp ⟨Q, hQ⟩
    exact hn E B C ha hc

#print axioms columnOrder_bijective
#print axioms columnPerm_right
#print axioms dephase_equivalent
#print axioms dephase_firstRow
#print axioms dephase_firstColumn
#print axioms rephase_det_normSq
#print axioms chart_upperRight_det_normSq
#print axioms chart_hadamard
#print axioms chart_hasRawQuartet_iff
#print axioms rowGram_blocks
#print axioms recover_lowerRight
#print axioms forced_cross
#print axioms Admissible.det_isUnit
#print axioms Admissible.inverse_bound
#print axioms Admissible.hadamard
#print axioms exists_admissible_chart
#print axioms exists_admissible_completion_of_rawQuartet
#print axioms exists_quartet_iff_bounded_completion
#print axioms no_quartet_iff_bounded_nonextension
end MUB.BoundedBlockChart
