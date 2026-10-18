import MubMonomialTransport

/-!
# Reindexing concrete raw quartet completions

AuthorityEffect: None.

A bijection of the coordinate types preserves every Gram equation and all
completion conditions. This connects the campaign's Fin 6 convention to the
external finite-corner model on Fin 3 + Fin 3 without changing its matrices.
-/

namespace MUB.MonomialTransport

variable {ι κ : Type*} [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ]

def pullMatrix (e : κ ≃ ι) (H : Mat ι) : Mat κ := H.submatrix e e

omit [DecidableEq ι] [DecidableEq κ] in
theorem pullMatrix_gram (e : κ ≃ ι) (H U : Mat ι) :
    (pullMatrix e H).conjTranspose * pullMatrix e U =
      pullMatrix e (H.conjTranspose * U) := by
  simp only [pullMatrix, Matrix.conjTranspose_submatrix, Matrix.submatrix_mul_equiv]

theorem pullMatrix_hadamard (e : κ ≃ ι) (H : Mat ι) (hH : RawHadamard H) :
    RawHadamard (pullMatrix e H) := by
  constructor
  · intro i j
    exact hH.1 (e i) (e j)
  · rw [pullMatrix_gram, hH.2]
    ext i j
    simp [pullMatrix, Matrix.submatrix_apply, Matrix.smul_apply,
      Matrix.one_apply, Fintype.card_congr e]

omit [DecidableEq ι] [DecidableEq κ] in
theorem pullMatrix_mu (e : κ ≃ ι) (H U : Mat ι) (hHU : RawMU H U) :
    RawMU (pullMatrix e H) (pullMatrix e U) := by
  intro i j
  rw [pullMatrix_gram]
  simpa only [pullMatrix, Matrix.submatrix_apply, Fintype.card_congr e] using hHU (e i) (e j)

omit [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ] in
theorem pullMatrix_inverse (e : κ ≃ ι) (H : Mat ι) :
    pullMatrix e.symm (pullMatrix e H) = H := by
  ext i j
  simp [pullMatrix]

theorem hasRawQuartet_pull (e : κ ≃ ι) (H : Mat ι) (hH : HasRawQuartet H) :
    HasRawQuartet (pullMatrix e H) := by
  rcases hH with ⟨hH, U, V, hU, hV, hHU, hHV, hUV⟩
  exact ⟨pullMatrix_hadamard e H hH, pullMatrix e U, pullMatrix e V,
    pullMatrix_hadamard e U hU, pullMatrix_hadamard e V hV,
    pullMatrix_mu e H U hHU, pullMatrix_mu e H V hHV, pullMatrix_mu e U V hUV⟩

theorem hasRawQuartet_pull_iff (e : κ ≃ ι) (H : Mat ι) :
    HasRawQuartet (pullMatrix e H) ↔ HasRawQuartet H := by
  constructor
  · intro h
    simpa only [pullMatrix_inverse] using hasRawQuartet_pull e.symm (pullMatrix e H) h
  · exact hasRawQuartet_pull e H

theorem exists_rawQuartet_index_iff (e : κ ≃ ι) :
    (∃ H : Mat ι, HasRawQuartet H) ↔ ∃ H : Mat κ, HasRawQuartet H := by
  constructor
  · rintro ⟨H, hH⟩
    exact ⟨pullMatrix e H, hasRawQuartet_pull e H hH⟩
  · rintro ⟨H, hH⟩
    exact ⟨pullMatrix e.symm H, hasRawQuartet_pull e.symm H hH⟩

#print axioms pullMatrix_gram
#print axioms pullMatrix_hadamard
#print axioms pullMatrix_mu
#print axioms pullMatrix_inverse
#print axioms hasRawQuartet_pull
#print axioms hasRawQuartet_pull_iff
#print axioms exists_rawQuartet_index_iff
end MUB.MonomialTransport
