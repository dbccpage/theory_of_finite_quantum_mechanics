import MubQuadraticLiftCompatibility
import Mathlib.Tactic.LinearCombination

/-!
# Exact affine completion of a six by six matrix with row and column sums six

AuthorityEffect: None. This removes eleven complex entries per transition
matrix without division or any additional hypothesis beyond the stated sums.
-/

namespace MUB.BalancedCompletion
open scoped BigOperators
variable {R : Type*} [CommRing R]

def restrict (A : Matrix (Fin 6) (Fin 6) R) : Matrix (Fin 5) (Fin 5) R :=
  fun i j => A i.castSucc j.castSucc

def complete (A : Matrix (Fin 5) (Fin 5) R) : Matrix (Fin 6) (Fin 6) R :=
  Fin.lastCases
    (Fin.lastCases ((∑ i, ∑ j, A i j) - 24) (fun j => 6 - ∑ i, A i j))
    (fun i => Fin.lastCases (6 - ∑ j, A i j) (fun j => A i j))

@[simp] theorem complete_core (A : Matrix (Fin 5) (Fin 5) R) (i j : Fin 5) :
    complete A i.castSucc j.castSucc = A i j := by
  simp only [complete, Fin.lastCases_castSucc]

@[simp] theorem complete_last_column (A : Matrix (Fin 5) (Fin 5) R) (i : Fin 5) :
    complete A i.castSucc (Fin.last 5) = 6 - ∑ j, A i j := by
  simp only [complete, Fin.lastCases_castSucc, Fin.lastCases_last]

@[simp] theorem complete_last_row (A : Matrix (Fin 5) (Fin 5) R) (j : Fin 5) :
    complete A (Fin.last 5) j.castSucc = 6 - ∑ i, A i j := by
  simp only [complete, Fin.lastCases_castSucc, Fin.lastCases_last]

@[simp] theorem complete_corner (A : Matrix (Fin 5) (Fin 5) R) :
    complete A (Fin.last 5) (Fin.last 5) = (∑ i, ∑ j, A i j) - 24 := by
  simp only [complete, Fin.lastCases_last]

theorem restrict_complete (A : Matrix (Fin 5) (Fin 5) R) : restrict (complete A) = A := by
  ext i j
  exact complete_core A i j

theorem complete_row_sum (A : Matrix (Fin 5) (Fin 5) R) (i : Fin 6) :
    ∑ j, complete A i j = 6 := by
  refine Fin.lastCases ?_ (fun k => ?_) i
  · rw [Fin.sum_univ_castSucc]
    simp only [complete_last_row, complete_corner, Finset.sum_sub_distrib,
      Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    rw [Finset.sum_comm]
    ring
  · rw [Fin.sum_univ_castSucc]
    simp only [complete_core, complete_last_column]
    ring

theorem complete_column_sum (A : Matrix (Fin 5) (Fin 5) R) (j : Fin 6) :
    ∑ i, complete A i j = 6 := by
  refine Fin.lastCases ?_ (fun k => ?_) j
  · rw [Fin.sum_univ_castSucc]
    simp only [complete_last_column, complete_corner, Finset.sum_sub_distrib,
      Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    ring
  · rw [Fin.sum_univ_castSucc]
    simp only [complete_core, complete_last_row]
    ring

theorem complete_restrict (A : Matrix (Fin 6) (Fin 6) R)
    (hr : ∀ i, ∑ j, A i j = 6) (hc : ∀ j, ∑ i, A i j = 6) :
    complete (restrict A) = A := by
  have hlast (j : Fin 5) : A (Fin.last 5) j.castSucc = 6 - ∑ i : Fin 5, A i.castSucc j.castSucc := by
    have h := hc j.castSucc
    rw [Fin.sum_univ_castSucc] at h
    linear_combination h
  ext i j
  refine Fin.lastCases ?_ (fun k => ?_) i
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · rw [complete_corner]
      have h := hr (Fin.last 5)
      rw [Fin.sum_univ_castSucc] at h
      simp_rw [hlast] at h
      simp only [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_fin, nsmul_eq_mul] at h
      rw [Finset.sum_comm] at h
      simp only [restrict]
      linear_combination -h
    · rw [complete_last_row, hlast]
      rfl
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · rw [complete_last_column]
      have h := hr k.castSucc
      rw [Fin.sum_univ_castSucc] at h
      simp only [restrict]
      linear_combination -h
    · exact complete_core (restrict A) k l

#print axioms restrict_complete
#print axioms complete_row_sum
#print axioms complete_column_sum
#print axioms complete_restrict
end MUB.BalancedCompletion
