import TensorSchmidt
import Mathlib.LinearAlgebra.Matrix.Permutation
import Mathlib.LinearAlgebra.Matrix.Kronecker

open Matrix WithLp
open scoped BigOperators ComplexConjugate InnerProductSpace Kronecker

noncomputable section
namespace TensorReachability
open TensorSchmidt

def basisUnitary {n : ℕ} (b : OrthonormalBasis (Fin n) ℂ (Space n)) :
    Matrix.unitaryGroup (Fin n) ℂ :=
  ⟨(EuclideanSpace.basisFun (Fin n) ℂ).toBasis.toMatrix b,
    (EuclideanSpace.basisFun (Fin n) ℂ).toMatrix_orthonormalBasis_mem_unitary b⟩

@[simp] theorem basisUnitary_apply {n : ℕ}
    (b : OrthonormalBasis (Fin n) ℂ (Space n)) (i j : Fin n) :
    (basisUnitary b : Matrix (Fin n) (Fin n) ℂ) i j = b j i := rfl

/-- Rectangular Schmidt decomposition, with both complete local unitary matrices.
Zero Schmidt coefficients and unequal dimensions are included. -/
theorem exists_schmidt_coefficients {n m : ℕ} (hnm : n ≤ m)
    (M : Matrix (Fin n) (Fin m) ℂ) :
    ∃ (U : Matrix.unitaryGroup (Fin n) ℂ) (V : Matrix.unitaryGroup (Fin m) ℂ)
      (s : Fin n → ℝ), (∀ i, 0 ≤ s i) ∧
      ∀ a b, M a b = ∑ i, U.val a i * (s i : ℂ) * V.val b (Fin.castLE hnm i) := by
  classical
  let T : Space n →ₗ[ℂ] Space m := Matrix.toEuclideanLin M.transpose
  obtain ⟨u, v, s, hs, hT⟩ := exists_schmidt_bases hnm T
  refine ⟨Matrix.UnitaryGroup.map_star (basisUnitary u), basisUnitary v, s, hs, ?_⟩
  intro a b
  have h := congrArg (fun x : Space m => x b)
    (congrArg T (u.sum_repr' ((EuclideanSpace.basisFun (Fin n) ℂ) a)))
  simp only [map_sum, map_smul, hT, smul_smul] at h
  simpa [T, Matrix.toLpLin_apply, EuclideanSpace.basisFun_apply,
    EuclideanSpace.inner_single_right, Matrix.mulVec, dotProduct,
    Matrix.transpose_apply, basisUnitary, Matrix.UnitaryGroup.map_star,
    Module.Basis.toMatrix_apply, ← mul_assoc] using h.symm

def productVector {n m : ℕ} (a : Fin n → ℂ) (b : Fin m → ℂ) :
    Fin n × Fin m → ℂ := fun i => a i.1 * b i.2

/-- The controlled modular shift sends (a,b) to (a,b+a). -/
def shift {n m : ℕ} [NeZero m] (hnm : n ≤ m) : Equiv.Perm (Fin n × Fin m) where
  toFun p := (p.1, p.2 + Fin.castLE hnm p.1)
  invFun p := (p.1, p.2 - Fin.castLE hnm p.1)
  left_inv p := by simp
  right_inv p := by simp

def controlledShift {n m : ℕ} [NeZero m] (hnm : n ≤ m) :
    Matrix.unitaryGroup (Fin n × Fin m) ℂ :=
  ⟨((shift hnm)⁻¹).permMatrix ℂ, by
    rw [Matrix.mem_unitaryGroup_iff']
    change (((shift hnm)⁻¹).permMatrix ℂ)ᴴ * ((shift hnm)⁻¹).permMatrix ℂ = 1
    simp [← Matrix.permMatrix_mul]⟩

theorem controlledShift_seed {n m : ℕ} [NeZero m] (hnm : n ≤ m)
    (s : Fin n → ℂ) (a : Fin n) (b : Fin m) :
    ((controlledShift hnm).val *ᵥ productVector s (Pi.single 0 1)) (a,b) =
      if b = Fin.castLE hnm a then s a else 0 := by
  classical
  simp [controlledShift, Matrix.permMatrix_mulVec, productVector, shift,
    Pi.single_apply, sub_eq_zero]

theorem local_after_shift {n m : ℕ} [NeZero m] (hnm : n ≤ m)
    (U : Matrix.unitaryGroup (Fin n) ℂ) (V : Matrix.unitaryGroup (Fin m) ℂ)
    (s : Fin n → ℂ) (a : Fin n) (b : Fin m) :
    (((U.val ⊗ₖ V.val) * (controlledShift hnm).val) *ᵥ
      productVector s (Pi.single 0 1)) (a,b) =
      ∑ i, U.val a i * s i * V.val b (Fin.castLE hnm i) := by
  rw [← Matrix.mulVec_mulVec]
  change (∑ j, (U.val ⊗ₖ V.val) (a,b) j *
    ((controlledShift hnm).val *ᵥ productVector s (Pi.single 0 1)) j) = _
  simp only [Fintype.sum_prod_type, kroneckerMap_apply, controlledShift_seed]
  simp [mul_ite, mul_comm, mul_left_comm, mul_assoc]

/-- Every bipartite vector is a controlled shift of a product seed followed by
local unitaries. The smaller subsystem is the control (relabel factors if needed). -/
theorem schmidt_reachability {n m : ℕ} [NeZero m] (hnm : n ≤ m)
    (ψ : Fin n × Fin m → ℂ) :
    ∃ (U : Matrix.unitaryGroup (Fin n) ℂ) (V : Matrix.unitaryGroup (Fin m) ℂ)
      (s : Fin n → ℂ),
      ((U.val ⊗ₖ V.val) * (controlledShift hnm).val) *ᵥ
        productVector s (Pi.single 0 1) = ψ := by
  obtain ⟨U,V,s,_,h⟩ := exists_schmidt_coefficients hnm (fun a b => ψ (a,b))
  refine ⟨U,V,fun i => (s i : ℂ),?_⟩
  funext ⟨a,b⟩
  rw [local_after_shift]
  exact (h a b).symm

#print axioms schmidt_reachability
end TensorReachability
