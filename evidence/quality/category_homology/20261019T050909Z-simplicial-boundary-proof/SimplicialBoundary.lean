import Mathlib.Data.Matrix.Mul
import Mathlib.Algebra.Field.Rat
import Mathlib.Algebra.BigOperators.Fin

/-! AuthorityEffect: None. Signed face pairing and exact indicator matrices.
The finite-index sum bijection adapts the argument of Mathlib's
AlgebraicTopology.AlternatingFaceMapComplex.d_squared (Joël Riou, Adam Topaz,
Johan Commelin; Apache-2.0). This version needs only the two-face identities,
not a full simplicial object or a presumed zero differential square.
Concrete canonical-list/basis and Rust representation correspondence remain
separate review obligations. No Rust/MIR extraction is claimed.
-/
namespace TFQM.SimplicialBoundary

open scoped BigOperators

def swapFace {n : Nat} (pair : Fin (n + 2) × Fin (n + 3))
    (order : (pair.2 : Nat) ≤ pair.1) : Fin (n + 2) × Fin (n + 3) :=
  (Fin.castLT pair.2 (lt_of_le_of_lt order pair.1.is_lt), pair.1.succ)

def signedTerm {n : Nat} (product : Fin (n + 2) → Fin (n + 3) → ℚ)
    (pair : Fin (n + 2) × Fin (n + 3)) : ℚ :=
  (-1 : ℚ) ^ (pair.1 : Nat) * (-1 : ℚ) ^ (pair.2 : Nat) * product pair.1 pair.2

theorem paired_term {n : Nat} (product : Fin (n + 2) → Fin (n + 3) → ℚ)
    (faces : ∀ pair, ∀ order : (pair.2 : Nat) ≤ pair.1,
      product pair.1 pair.2 = product (swapFace pair order).1 (swapFace pair order).2)
    (pair : Fin (n + 2) × Fin (n + 3)) (order : (pair.2 : Nat) ≤ pair.1) :
    signedTerm product pair = -signedTerm product (swapFace pair order) := by
  unfold signedTerm
  rw [faces pair order]
  simp only [swapFace, Fin.val_castLT, Fin.val_succ, pow_add, pow_one,
    mul_neg, neg_mul, neg_neg, mul_one]
  simp only [mul_comm, mul_left_comm, mul_assoc]

theorem pair_cancellation {n : Nat} (term : Fin (n + 2) × Fin (n + 3) → ℚ)
    (paired : ∀ pair, ∀ order : (pair.2 : Nat) ≤ pair.1,
      term pair = -term (swapFace pair order)) : ∑ pair, term pair = 0 := by
  classical
  let P := Fin (n + 2) × Fin (n + 3)
  let S : Finset P := {pair : P | (pair.2 : Nat) ≤ pair.1}
  rw [← Finset.sum_add_sum_compl S, ← eq_neg_iff_add_eq_zero, ← Finset.sum_neg_distrib]
  let φ : ∀ pair : P, pair ∈ S → P := fun pair present =>
    swapFace pair (Finset.mem_filter.mp present).right
  apply Finset.sum_bij φ
  · intro pair present
    simp_rw [S, φ, swapFace, Finset.compl_filter, Finset.mem_filter_univ,
      Fin.val_succ, Fin.val_castLT] at present ⊢
    omega
  · rintro ⟨i, j⟩ present ⟨i', j'⟩ present' same
    rw [Prod.mk_inj]
    exact ⟨by simpa [φ, swapFace] using! congr_arg Prod.snd same,
      by simpa [φ, swapFace, Fin.castSucc_castLT] using!
        congr_arg Fin.castSucc (congr_arg Prod.fst same)⟩
  · rintro ⟨i', j'⟩ present'
    simp_rw [S, Finset.compl_filter, Finset.mem_filter_univ, not_le] at present'
    refine ⟨(j'.pred ?_, Fin.castSucc i'), ?_, ?_⟩
    · rintro rfl
      simp only [Fin.val_zero, not_lt_zero] at present'
    · simpa [S] using! Nat.le_sub_one_of_lt present'
    · simp only [φ, swapFace, Fin.castLT_castSucc, Fin.succ_pred]
  · intro pair present
    exact paired pair (Finset.mem_filter.mp present).right

theorem signed_faces_cancel {n : Nat} (product : Fin (n + 2) → Fin (n + 3) → ℚ)
    (faces : ∀ pair, ∀ order : (pair.2 : Nat) ≤ pair.1,
      product pair.1 pair.2 = product (swapFace pair order).1 (swapFace pair order).2) :
    ∑ pair, signedTerm product pair = 0 :=
  pair_cancellation (signedTerm product) (paired_term product faces)

def mapMatrix {a b : Nat} (map : Fin b → Fin a) : Matrix (Fin a) (Fin b) ℚ :=
  fun row column => if row = map column then 1 else 0

theorem mapMatrix_comp {a b c : Nat} (first : Fin b → Fin a) (second : Fin c → Fin b) :
    mapMatrix first * mapMatrix second = mapMatrix (first ∘ second) := by
  classical
  ext row column
  simp [Matrix.mul_apply, mapMatrix, mul_ite]

theorem mapMatrix_identity (a : Nat) : mapMatrix (id : Fin a → Fin a) = 1 := by
  classical
  ext row column
  simp [mapMatrix, Matrix.one_apply]

#print axioms paired_term
#print axioms pair_cancellation
#print axioms signed_faces_cancel
#print axioms mapMatrix_comp
#print axioms mapMatrix_identity

end TFQM.SimplicialBoundary
