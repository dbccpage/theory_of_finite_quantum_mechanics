import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.RingTheory.Ideal.Operations
import Mathlib.Tactic.Ring

/-!
# First-row gauge balance as an explicit ideal identity

AuthorityEffect: None.

The identity holds before imposing any equations, over every commutative
star ring. Its ideal-membership corollary applies in particular to polynomial
rings carrying a star operation. It asserts no independence, rank, or global
nonextension result.
-/

namespace MUB.GaugeSyzygy
open scoped BigOperators

variable {R : Type*} [CommRing R] [StarRing R]
abbrev Mat6 (R : Type*) := Matrix (Fin 6) (Fin 6) R

def gaugeResidual (A : Mat6 R) (j : Fin 6) : R := A 0 j - 1

def rowGramResidual (B : Mat6 R) (m : Fin 6) : R :=
  (∑ k, B m k * star (B 0 k)) - if m = 0 then 6 else 0

def balanceResidual (A B : Mat6 R) (j : Fin 6) : R :=
  (∑ k, (A.conjTranspose * B) j k) - 6

def columnBalanceResidual (A B : Mat6 R) (k : Fin 6) : R :=
  (∑ j, (A.conjTranspose * B) j k) - 6

theorem row_balance_syzygy (A B : Mat6 R) (j : Fin 6) :
    balanceResidual A B j =
      (∑ m, star (A m j) * rowGramResidual B m) -
      (∑ m, ∑ k, star (A m j) * B m k * star (gaugeResidual B k)) +
      6 * star (gaugeResidual A j) := by
  have hrow (m : Fin 6) :
      star (A m j) * rowGramResidual B m -
          (∑ k, star (A m j) * B m k * star (gaugeResidual B k)) =
        (∑ k, star (A m j) * B m k) -
          star (A m j) * (if m = 0 then 6 else 0) := by
    simp only [rowGramResidual, gaugeResidual, star_sub, star_one,
      mul_sub, Finset.mul_sum, Finset.sum_sub_distrib]
    simp only [mul_assoc]
    ring_nf
  have hsum := congrArg (fun f : Fin 6 → R => ∑ m, f m) (funext hrow)
  simp only [Finset.sum_sub_distrib] at hsum
  have hdelta : (∑ m : Fin 6, star (A m j) * (if m = 0 then 6 else 0)) =
      star (A 0 j) * 6 := by simp
  rw [hdelta] at hsum
  rw [hsum]
  simp only [balanceResidual, Matrix.mul_apply, Matrix.conjTranspose_apply,
    gaugeResidual, star_sub, star_one]
  rw [Finset.sum_comm]
  ring_nf

/-- Every balance residual lies in any ideal containing the displayed generators. -/
theorem balanceResidual_mem (A B : Mat6 R) (j : Fin 6) (I : Ideal R)
    (hrow : ∀ m, rowGramResidual B m ∈ I)
    (hB : ∀ k, star (gaugeResidual B k) ∈ I)
    (hA : star (gaugeResidual A j) ∈ I) : balanceResidual A B j ∈ I := by
  rw [row_balance_syzygy]
  apply I.add_mem
  · apply I.sub_mem
    · exact I.sum_mem (fun m _ => I.mul_mem_left _ (hrow m))
    · exact I.sum_mem (fun m _ => I.sum_mem (fun k _ => I.mul_mem_left _ (hB k)))
  · exact I.mul_mem_left _ hA

theorem balanceResidual_zero (A B : Mat6 R) (j : Fin 6)
    (hrow : ∀ m, rowGramResidual B m = 0)
    (hB : ∀ k, gaugeResidual B k = 0)
    (hA : gaugeResidual A j = 0) : balanceResidual A B j = 0 := by
  rw [row_balance_syzygy]
  simp [hrow, hB, hA]

theorem columnBalanceResidual_eq_star (A B : Mat6 R) (k : Fin 6) :
    columnBalanceResidual A B k = star (balanceResidual B A k) := by
  simp [columnBalanceResidual, balanceResidual, Matrix.mul_apply,
    Matrix.conjTranspose_apply, mul_comm]

theorem column_balance_syzygy (A B : Mat6 R) (k : Fin 6) :
    columnBalanceResidual A B k =
      (∑ m, star (rowGramResidual A m) * B m k) -
      (∑ m, ∑ j, gaugeResidual A j * (star (A m j) * B m k)) +
      gaugeResidual B k * 6 := by
  rw [columnBalanceResidual_eq_star, row_balance_syzygy]
  simp only [star_add, star_sub, star_sum, star_mul, star_star, star_ofNat]

theorem columnBalanceResidual_mem (A B : Mat6 R) (k : Fin 6) (I : Ideal R)
    (hrow : ∀ m, star (rowGramResidual A m) ∈ I)
    (hA : ∀ j, gaugeResidual A j ∈ I)
    (hB : gaugeResidual B k ∈ I) : columnBalanceResidual A B k ∈ I := by
  rw [column_balance_syzygy]
  apply I.add_mem
  · apply I.sub_mem
    · exact I.sum_mem (fun m _ => I.mul_mem_right _ (hrow m))
    · exact I.sum_mem (fun m _ => I.sum_mem (fun j _ => I.mul_mem_right _ (hA j)))
  · exact I.mul_mem_right _ hB

#print axioms row_balance_syzygy
#print axioms balanceResidual_mem
#print axioms balanceResidual_zero
#print axioms columnBalanceResidual_eq_star
#print axioms column_balance_syzygy
#print axioms columnBalanceResidual_mem
end MUB.GaugeSyzygy
