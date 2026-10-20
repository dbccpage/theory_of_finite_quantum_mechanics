import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.Combinatorics.Enumerative.Partition.Basic

/-! AuthorityEffect: None. Actual finite matrix path products, mass bounds,
integer characteristic-polynomial embedding and monotone work admission.
These do not extract Rust or establish categorical realizability. -/
namespace TFQM.FusionRingModel
open scoped BigOperators Matrix

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def advance (n : ι → ι → ι → Nat) (w : ι) (v : ι → Nat) (c : ι) : Nat :=
  ∑ a, v a * n a w c

theorem advance_matrix (n : ι → ι → ι → Nat) (w : ι) (v : ι → Nat) :
    advance n w v = v ᵥ* (fun a c => n a w c) := rfl

theorem matrix_word_product (n : ι → ι → ι → Nat) (words : List ι) (v : ι → Nat) :
    words.foldl (fun x w => advance n w x) v = v ᵥ* (words.map (fun w a c => n a w c)).prod := by
  induction words generalizing v with
  | nil => simp
  | cons w ws ih =>
    simp only [List.foldl_cons, List.map_cons, List.prod_cons]
    rw [ih, advance_matrix, Matrix.vecMul_vecMul]

theorem empty_word (n : ι → ι → ι → Nat) (v : ι → Nat) :
    ([] : List ι).foldl (fun x w => advance n w x) v = v := rfl

theorem word_concatenation (n : ι → ι → ι → Nat) (a b : List ι) (v : ι → Nat) :
    (a++b).foldl (fun x w => advance n w x) v =
      b.foldl (fun x w => advance n w x) (a.foldl (fun x w => advance n w x) v) := by
  rw [List.foldl_append]

theorem total_mass (n : ι → ι → ι → Nat) (w : ι) (v : ι → Nat) :
    (∑ c, advance n w v c) = ∑ a, v a * ∑ c, n a w c := by
  simp only [advance, Finset.mul_sum]
  exact Finset.sum_comm

theorem mass_bound (n : ι → ι → ι → Nat) (w : ι) (v : ι → Nat) (d : Nat)
    (hd : ∀ a, (∑ c, n a w c) ≤ d) : (∑ c, advance n w v c) ≤ (∑ a, v a)*d := by
  rw [total_mass, Finset.sum_mul]
  exact Finset.sum_le_sum (fun a _ => Nat.mul_le_mul_left (v a) (hd a))

theorem power_growth_bound (mass d g : Nat) (hd : d≤2^g) : mass*d≤mass*2^g :=
  Nat.mul_le_mul_left mass hd

theorem coefficient_square_bound (m : Nat) (hm : m≤2^64-1) : m*m<2^128 := by
  have h := Nat.mul_le_mul hm hm
  norm_num at h ⊢
  omega

theorem rank_row_bound (r : Nat) (hr : r≤32) : r*(2^64-1)<2^69 := by
  have h := Nat.mul_le_mul_right (2^64-1) hr
  norm_num at h ⊢
  omega

theorem mixed_radix_digit (digit tail modulus : Nat) (hd : digit<modulus) :
    (digit+modulus*tail)%modulus=digit := by
  simp [Nat.add_mod, Nat.mod_eq_of_lt hd]

theorem integer_charpoly_embedding (m : Matrix ι ι Int) :
    (m.map (Int.castRingHom Rat)).charpoly = m.charpoly.map (Int.castRingHom Rat) :=
  Matrix.charpoly_map m (Int.castRingHom Rat)

def charge (cells bits work : Nat) : Nat := work+cells*(bits+64)

theorem charge_monotone (cells bits work : Nat) : work≤charge cells bits work := by
  unfold charge
  omega

theorem charge_acceptance (cells bits work budget : Nat) :
    decide (charge cells bits work>budget)=false ↔ charge cells bits work≤budget := by simp

theorem prefix_failure_stays (work future budget : Nat) (h : budget<work) : budget<work+future := by omega

#print axioms advance_matrix
#print axioms matrix_word_product
#print axioms empty_word
#print axioms word_concatenation
#print axioms total_mass
#print axioms mass_bound
#print axioms power_growth_bound
#print axioms coefficient_square_bound
#print axioms rank_row_bound
#print axioms mixed_radix_digit
#print axioms integer_charpoly_embedding
#print axioms charge_monotone
#print axioms charge_acceptance
#print axioms prefix_failure_stays
end TFQM.FusionRingModel
