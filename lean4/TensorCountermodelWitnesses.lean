import TensorCountermodelCones
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-! Exact two-qubit counterexamples. Universal product-test positivity comes
from the full-cone theorems; the finite calculations certify separation and
failure of the named calibration/preservation hypotheses, not a classification. -/
open Matrix Module
open scoped BigOperators Kronecker ComplexOrder MatrixOrder
noncomputable section
namespace TensorCountermodelWitnesses
open TensorTomography TensorComposition TensorEffectOrder TensorPartialTranspose
open TensorCountermodelCones TensorConeReconstruction TensorOperationalCone TensorReachability

abbrev Q := Fin 2
abbrev J := Q × Q
def bellVector : J → ℂ := fun i => if i.1 = i.2 then 1 else 0
def antisymmetric : J → ℂ := fun i => if i = (0,1) then 1 else if i = (1,0) then -1 else 0
def bell : Herm J := (1 / 2 : ℝ) • hermRankOne bellVector
def swapWitness : Herm J := gamma bell
def plus : Herm Q := (1 / 2 : ℝ) • hermRankOne ![1, 1]
def minus : Herm Q := (1 / 2 : ℝ) • hermRankOne ![1, -1]
def zeroState : Herm Q := hermRankOne (Pi.single 0 1)
def seed : Herm J := product plus zeroState
def minusSeed : Herm J := product minus zeroState
def imaginaryEffect : Herm Q := (1 / 2 : ℝ) • hermRankOne ![1, Complex.I]
def gate : Matrix.unitaryGroup J ℂ := controlledShift (n := 2) (m := 2) (by decide)

theorem scaled_rankOne_entry {d : Type*} (r : ℝ) (v : d → ℂ) (i j : d) :
    ((r • hermRankOne v : Herm d).val i j) = (r : ℂ) * v i * star (v j) := by
  change r • (v i * star (v j)) = _
  simp [Algebra.smul_def, mul_assoc]

@[simp] theorem plus_entry (i j : Q) : plus.val i j = (1 / 2 : ℂ) := by
  rw [plus, scaled_rankOne_entry]
  fin_cases i <;> fin_cases j <;> norm_num

@[simp] theorem minus_entry (i j : Q) : minus.val i j =
    (1 / 2 : ℂ) * (![1,-1] : Q → ℂ) i * (![1,-1] : Q → ℂ) j := by
  rw [minus, scaled_rankOne_entry]
  fin_cases i <;> fin_cases j <;> norm_num

@[simp] theorem imaginary_entry (i j : Q) : imaginaryEffect.val i j =
    (1 / 2 : ℂ) * (![1,Complex.I] : Q → ℂ) i * star ((![1,Complex.I] : Q → ℂ) j) := by
  rw [imaginaryEffect, scaled_rankOne_entry]
  norm_num

local macro "entry_calc" : tactic => `(tactic|
  norm_num [bell, bellVector, swapWitness, gamma_val, pt, hermRankOne, rankOne,
    antisymmetric, zeroState, seed, minusSeed,
    product, Matrix.vecMulVec_apply, Matrix.mul_apply, Matrix.mulVec, dotProduct,
    quadratic, Matrix.trace, Matrix.diag_apply, Fintype.sum_prod_type, Fin.sum_univ_two,
    Pi.single_apply, Matrix.conjTranspose_apply, Matrix.diagonal_apply,
    Matrix.smul_apply, Pi.smul_apply, Pi.star_apply])

theorem bell_positive : Positive bell :=
  (Matrix.posSemidef_vecMulVec_self_star bellVector).smul (by norm_num : (0 : ℝ) ≤ 1 / 2)

theorem swap_twisted : swapWitness ∈ twisted := by
  change Positive (gamma (gamma bell))
  simpa using bell_positive

/-- Quantifies over every complex local positive test, hence every product vector. -/
theorem swap_blockPositive : BlockPositive swapWitness := twisted_blockPositive swap_twisted

theorem swap_negative : quadratic swapWitness.val antisymmetric = -1 := by entry_calc

theorem swap_not_positive : ¬ Positive swapWitness := by
  intro h
  have hv := h.re_dotProduct_nonneg antisymmetric
  change 0 ≤ (quadratic swapWitness.val antisymmetric).re at hv
  rw [swap_negative] at hv
  norm_num at hv

theorem bell_not_separable : bell ∉ sep := fun h => swap_not_positive (sep_ppt h)

theorem seed_separable : seed ∈ sep := product_mem_sep
  ((Matrix.posSemidef_vecMulVec_self_star _).smul (by norm_num : (0 : ℝ) ≤ 1 / 2))
  (Matrix.posSemidef_vecMulVec_self_star _)

theorem gamma_seed : gamma seed = seed := by
  apply Subtype.ext
  ext ⟨i,j⟩ ⟨k,l⟩
  fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;> entry_calc

theorem gate_seed : conjMap gate.val seed = bell := by
  have hs : seed = (1 / 2 : ℝ) • hermRankOne (productVector ![1, 1] (Pi.single 0 1)) := by
    rw [seed, plus, product_smul_left, zeroState, product_rankOne]
  rw [hs, map_smul]
  apply congrArg (fun H : Herm J => (1 / 2 : ℝ) • H)
  apply Subtype.ext
  change conjugate gate.val (rankOne _) = rankOne bellVector
  rw [conjugate_rankOne]
  congr 1
  ext ⟨i,j⟩
  change ((controlledShift (by decide : 2 ≤ 2)).val *ᵥ
    productVector ![1,1] (Pi.single 0 1)) (i,j) = bellVector (i,j)
  rw [controlledShift_seed]
  fin_cases i <;> fin_cases j <;> norm_num [bellVector]

theorem sep_fails_controlled_shift : ¬ (∀ H ∈ (sep : PointedCone ℝ (Herm J)),
    conjMap gate.val H ∈ sep) := by
  intro h
  exact bell_not_separable (gate_seed ▸ h seed seed_separable)

theorem negative_product_transport :
    quadratic (conjMap gate.valᴴ swapWitness).val (productVector ![1,-1] (Pi.single 1 1)) = -1 := by
  change quadratic (conjugate gate.valᴴ swapWitness.val) _ = _
  rw [quadratic_transport]
  have hv : gate.val *ᵥ productVector ![1,-1] (Pi.single 1 1) = antisymmetric := by
    ext ⟨i,j⟩
    simp only [gate, controlledShift, Matrix.permMatrix_mulVec, Function.comp_apply]
    change productVector ![1,-1] (Pi.single 1 1)
      ((shift (by decide : 2 ≤ 2)).symm (i,j)) = antisymmetric (i,j)
    simp only [productVector, shift, Pi.single_apply, antisymmetric]
    change (![1,-1] : Q → ℂ) i * (if j - i = 1 then (1 : ℂ) else 0) =
      (if (i,j) = ((0 : Q), (1 : Q)) then (1 : ℂ)
       else if (i,j) = ((1 : Q), (0 : Q)) then (-1 : ℂ) else 0)
    fin_cases i <;> fin_cases j <;> norm_num <;> decide
  rw [hv, swap_negative]

theorem bp_fails_inverse_controlled_shift : ¬ (∀ H : Herm J, BlockPositive H →
    BlockPositive (conjMap gate.valᴴ H)) := by
  intro h
  have hp := h swapWitness swap_blockPositive (hermRankOne ![1,-1])
    (hermRankOne (Pi.single 1 1)) (Matrix.posSemidef_vecMulVec_self_star _)
    (Matrix.posSemidef_vecMulVec_self_star _)
  rw [product_rankOne, pairing_apply] at hp
  change 0 ≤ (rankOne (productVector ![1,-1] (Pi.single 1 1)) *
    (conjMap gate.valᴴ swapWitness).val).trace.re at hp
  rw [trace_rankOne] at hp
  change 0 ≤ (quadratic (conjMap gate.valᴴ swapWitness).val _).re at hp
  rw [negative_product_transport] at hp
  norm_num at hp

theorem twist_seed : twist gate.val seed = swapWitness := by
  change gamma (conjMap gate.val (gamma seed)) = gamma bell
  rw [gamma_seed, gate_seed]

theorem twisted_fails_ordinary_calibration :
    seed ∈ twisted ∧ twist gate.val seed ∈ twisted ∧ conjMap gate.val seed ∉ twisted := by
  refine ⟨sep_ppt seed_separable, twist_preserves _ (sep_ppt seed_separable), ?_⟩
  rw [gate_seed]
  exact swap_not_positive

def classical (k : J) : Herm J := hermRankOne (Pi.single k 1)

theorem gate_classical (k : J) : conjMap gate.val (classical k) =
    classical (shift (by decide : 2 ≤ 2) k) := by
  apply Subtype.ext
  change conjugate gate.val (rankOne _) = rankOne _
  rw [conjugate_rankOne]
  congr 1
  ext i
  simp only [gate, controlledShift, Matrix.permMatrix_mulVec, Function.comp_apply,
    Pi.single_apply]
  congr 1
  apply propext
  change (shift (by decide : 2 ≤ 2)).symm i = k ↔ i = shift (by decide : 2 ≤ 2) k
  exact (Equiv.symm_apply_eq (shift (by decide : 2 ≤ 2)))

theorem gamma_classical (k : J) : gamma (classical k) = classical k := by
  apply Subtype.ext
  rcases k with ⟨a,b⟩
  ext ⟨i,j⟩ ⟨r,s⟩
  fin_cases a <;> fin_cases b <;> fin_cases i <;> fin_cases j <;>
    fin_cases r <;> fin_cases s <;> norm_num [classical, gamma_val, pt,
      hermRankOne, rankOne, Matrix.vecMulVec_apply, Pi.single_apply]

theorem twisted_same_classical_table (k : J) :
    twist gate.val (classical k) = conjMap gate.val (classical k) := by
  change gamma (conjMap gate.val (gamma (classical k))) = _
  rw [gamma_classical, gate_classical, gamma_classical]

theorem imaginary_effect_binary : Binary imaginaryEffect := by
  constructor
  · exact (Matrix.posSemidef_vecMulVec_self_star _).smul (by norm_num : (0 : ℝ) ≤ 1 / 2)
  · have hc : 1 - imaginaryEffect = (1 / 2 : ℝ) • hermRankOne ![1,-Complex.I] := by
      apply Subtype.ext
      ext i j
      change (1 : Matrix Q Q ℂ) i j - imaginaryEffect.val i j =
        ((1 / 2 : ℝ) • hermRankOne (![1,-Complex.I] : Q → ℂ)).val i j
      rw [scaled_rankOne_entry, imaginary_entry]
      fin_cases i <;> fin_cases j <;> norm_num [mul_assoc]
    rw [hc]
    exact (Matrix.posSemidef_vecMulVec_self_star _).smul (by norm_num : (0 : ℝ) ≤ 1 / 2)

/-- A concrete product of local binary effects distinguishes the two gates. -/
theorem coherent_calibration_separates :
    pairing (product imaginaryEffect imaginaryEffect) (conjMap gate.val seed) = 0 ∧
    pairing (product imaginaryEffect imaginaryEffect) (twist gate.val seed) = 1 / 2 := by
  rw [gate_seed, twist_seed]
  constructor <;> simp only [pairing_apply] <;> entry_calc

def dephase {d : Type*} [Fintype d] [DecidableEq d] : Herm d →ₗ[ℝ] Herm d where
  toFun A := ⟨Matrix.diagonal A.val.diag, by
    change (Matrix.diagonal A.val.diag)ᴴ = _
    ext i j
    by_cases h : i = j
    · subst j
      simpa [Matrix.conjTranspose_apply, Matrix.diagonal_apply] using
        congrFun (congrFun A.property i) i
    · simp [Matrix.conjTranspose_apply, Matrix.diagonal_apply, h, Ne.symm h]⟩
  map_add' A B := Subtype.ext (by simp)
  map_smul' r A := Subtype.ext (by simp)

theorem dephase_positive {d : Type*} [Fintype d] [DecidableEq d]
    {A : Herm d} (hA : Positive A) : Positive (dephase A) :=
  Matrix.PosSemidef.diagonal (fun i => hA.diag_nonneg)

theorem dephase_trace {d : Type*} [Fintype d] [DecidableEq d] (A : Herm d) :
    (dephase A).val.trace = A.val.trace := by simp [dephase, Matrix.trace]

theorem dephase_classical (k : J) : dephase (classical k) = classical k := by
  apply Subtype.ext
  ext i j
  by_cases h : i = j
  · subst j; simp [dephase]
  · simp [dephase, Matrix.diagonal_apply, h, classical, hermRankOne, rankOne,
      Matrix.vecMulVec_apply, Pi.single_apply]
    aesop

theorem dephased_same_classical_table (k : J) :
    dephase (conjMap gate.val (classical k)) = conjMap gate.val (classical k) := by
  rw [gate_classical, dephase_classical]

theorem dephase_not_injective : ¬ Function.Injective (dephase (d := J)) := by
  have he : dephase bell = dephase (conjMap gate.val minusSeed) := by
    have hm : conjMap gate.val minusSeed =
        (1 / 2 : ℝ) • hermRankOne (fun i : J => if i.1 = i.2 then (![1,-1] i.1 : ℂ) else 0) := by
      rw [minusSeed, minus, product_smul_left, zeroState, product_rankOne, map_smul]
      apply congrArg (fun H : Herm J => (1 / 2 : ℝ) • H)
      apply Subtype.ext
      change conjugate gate.val (rankOne _) = rankOne _
      rw [conjugate_rankOne]
      congr 1
      ext ⟨i,j⟩
      simpa [gate, eq_comm] using controlledShift_seed (by decide : 2 ≤ 2) ![1,-1] i j
    rw [hm]
    apply Subtype.ext
    ext ⟨i,j⟩ ⟨k,l⟩
    fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
      norm_num [dephase, bell, bellVector, hermRankOne, rankOne, Matrix.vecMulVec_apply,
        Matrix.diagonal_apply, Matrix.diag_apply]
  intro hi
  have hs : conjMap gate.val seed = conjMap gate.val minusSeed := gate_seed.trans (hi he)
  have hseed : seed = minusSeed := by
    have hrev := congrArg (conjMap gate.valᴴ) hs
    simpa only [conjMap_inverse] using hrev
  have hh := congrArg (fun A : Herm J => A.val (0,0) (1,0)) hseed
  norm_num [seed, minusSeed, zeroState, product, hermRankOne, rankOne,
    Matrix.vecMulVec_apply, Pi.single_apply, Matrix.smul_apply, Pi.smul_apply, Pi.star_apply] at hh

theorem dephased_coherent_calibration_separates :
    pairing (product plus plus) (conjMap gate.val seed) = 1 / 2 ∧
    pairing (product plus plus) (dephase (conjMap gate.val seed)) = 1 / 4 := by
  rw [gate_seed]
  constructor <;> simp only [pairing_apply] <;> norm_num [dephase, Matrix.diagonal_apply,
    Matrix.diag_apply, bell, bellVector, product, hermRankOne, rankOne,
    Matrix.vecMulVec_apply, Matrix.mul_apply, Matrix.trace, Fintype.sum_prod_type, Fin.sum_univ_two,
    Matrix.smul_apply, Pi.smul_apply, Pi.star_apply]

theorem dephased_controlled_shift_not_injective :
    ¬ Function.Injective (fun H : Herm J => dephase (conjMap gate.val H)) := by
  have hr (H : Herm J) : conjMap gate.val (conjMap gate.valᴴ H) = H := by
    have h := conjMap_inverse (star gate) H
    change conjMap gate.valᴴᴴ (conjMap gate.valᴴ H) = H at h
    simpa only [Matrix.conjTranspose_conjTranspose] using h
  intro hi
  apply dephase_not_injective
  intro X Y h
  have he : conjMap gate.valᴴ X = conjMap gate.valᴴ Y :=
    hi (by simpa only [hr] using h)
  simpa only [hr] using congrArg (conjMap gate.val) he

theorem plus_binary : Binary plus := by
  constructor
  · exact (Matrix.posSemidef_vecMulVec_self_star _).smul (by norm_num : (0 : ℝ) ≤ 1 / 2)
  · have hc : 1 - plus = minus := by
      apply Subtype.ext
      ext i j
      change (1 : Matrix Q Q ℂ) i j - plus.val i j = minus.val i j
      rw [plus_entry, minus_entry]
      fin_cases i <;> fin_cases j <;> norm_num
    rw [hc]
    exact (Matrix.posSemidef_vecMulVec_self_star _).smul (by norm_num : (0 : ℝ) ≤ 1 / 2)

theorem seed_normalized : Positive seed ∧ seed.val.trace.re = 1 := by
  refine ⟨sep_positive seed_separable, ?_⟩
  norm_num [seed, zeroState, product, hermRankOne, rankOne, Matrix.trace,
    Matrix.diag_apply, Matrix.vecMulVec_apply, Pi.single_apply,
    Fintype.sum_prod_type, Fin.sum_univ_two]

#print axioms swap_blockPositive
#print axioms bell_not_separable
#print axioms sep_fails_controlled_shift
#print axioms bp_fails_inverse_controlled_shift
#print axioms twisted_fails_ordinary_calibration
#print axioms twisted_same_classical_table
#print axioms coherent_calibration_separates
#print axioms dephased_same_classical_table
#print axioms dephase_not_injective
#print axioms dephased_controlled_shift_not_injective
#print axioms imaginary_effect_binary
#print axioms plus_binary
#print axioms seed_normalized
#print axioms dephased_coherent_calibration_separates
end TensorCountermodelWitnesses
