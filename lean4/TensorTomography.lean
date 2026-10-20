import Mathlib.Analysis.Matrix.Order
import Mathlib.LinearAlgebra.Complex.Module
import Mathlib.LinearAlgebra.BilinearForm.Properties
import Mathlib.Data.Matrix.Basis
import Mathlib.Tactic.Ring

open Matrix
open scoped Kronecker BigOperators ComplexOrder ComplexStarModule

noncomputable section

namespace TensorTomography

abbrev Herm (n : Type*) := selfAdjoint (Matrix n n ℂ)

variable {n m : Type*} [Fintype n] [Fintype m]

def val : Herm n →ₗ[ℝ] Matrix n n ℂ :=
  (selfAdjoint.submodule ℝ (Matrix n n ℂ)).subtype

instance : FiniteDimensional ℝ (Herm n) :=
  Module.Finite.of_injective val Subtype.val_injective

def product (A : Herm n) (B : Herm m) : Herm (n × m) :=
  ⟨(A : Matrix n n ℂ) ⊗ₖ (B : Matrix m m ℂ), by
    change ((A : Matrix n n ℂ) ⊗ₖ (B : Matrix m m ℂ))ᴴ = _
    rw [conjTranspose_kronecker, (show (A : Matrix n n ℂ)ᴴ = A from A.property), (show (B : Matrix m m ℂ)ᴴ = B from B.property)]⟩

@[simp] theorem product_add_left (A B : Herm n) (C : Herm m) :
    product (A + B) C = product A C + product B C :=
  Subtype.ext (add_kronecker _ _ _)

@[simp] theorem product_add_right (A : Herm n) (B C : Herm m) :
    product A (B + C) = product A B + product A C :=
  Subtype.ext (kronecker_add _ _ _)

@[simp] theorem product_smul_left (r : ℝ) (A : Herm n) (B : Herm m) :
    product (r • A) B = r • product A B :=
  Subtype.ext (smul_kronecker _ _ _)

@[simp] theorem product_smul_right (r : ℝ) (A : Herm n) (B : Herm m) :
    product A (r • B) = r • product A B :=
  Subtype.ext (kronecker_smul _ _ _)

/-- A real-linear bilinear product; its ordered cone is not specified. -/
def productMap : Herm n →ₗ[ℝ] Herm m →ₗ[ℝ] Herm (n × m) where
  toFun A := {
    toFun := product A
    map_add' := product_add_right A
    map_smul' := fun r B => product_smul_right r A B }
  map_add' A B := LinearMap.ext (product_add_left A B)
  map_smul' r A := LinearMap.ext (fun B => product_smul_left r A B)

theorem realPart_kronecker (A : Matrix n n ℂ) (B : Matrix m m ℂ) :
    ℜ (A ⊗ₖ B) = product (ℜ A) (ℜ B) - product (ℑ A) (ℑ B) := by
  apply Subtype.ext
  ext i j
  apply Complex.ext <;>
    simp [product, realPart_apply_coe, imaginaryPart_apply_coe,
      Matrix.star_apply, Complex.mul_re, Complex.mul_im, Complex.real_smul] <;> ring

/-- Products of local Hermitian matrices span every joint Hermitian matrix.
This is proved from matrix units; no composite dimension axiom is assumed. -/
theorem product_span :
    Submodule.span ℝ (Set.range (fun p : Herm n × Herm m => product p.1 p.2)) = ⊤ := by
  classical
  let S := Submodule.span ℝ (Set.range (fun p : Herm n × Herm m => product p.1 p.2))
  have hp (A : Herm n) (B : Herm m) : product A B ∈ S :=
    Submodule.subset_span ⟨(A, B), rfl⟩
  have hr (A : Matrix (n × m) (n × m) ℂ) : ℜ A ∈ S := by
    refine Matrix.induction_on' A ?_ ?_ ?_
    · simpa using S.zero_mem
    · intro X Y hX hY
      simpa only [map_add] using S.add_mem hX hY
    · intro i j z
      have hs : single i j z = single i.1 j.1 z ⊗ₖ single i.2 j.2 (1 : ℂ) := by
        simp [single_kronecker_single]
      rw [hs, realPart_kronecker]
      exact S.sub_mem (hp _ _) (hp _ _)
  apply top_unique
  intro A _
  simpa using hr (A : Matrix (n × m) (n × m) ℂ)

noncomputable def pairing : Herm n →ₗ[ℝ] Herm n →ₗ[ℝ] ℝ where
  toFun A := {
    toFun := fun B => ((A : Matrix n n ℂ) * (B : Matrix n n ℂ)).trace.re
    map_add' := by intros; simp [mul_add]
    map_smul' := by intros; simp }
  map_add' := by intros; ext; simp [add_mul]
  map_smul' := by intros; ext; simp

@[simp] theorem pairing_apply (A B : Herm n) :
    pairing A B = ((A : Matrix n n ℂ) * (B : Matrix n n ℂ)).trace.re := rfl

theorem trace_pair_im (A B : Herm n) :
    ((A : Matrix n n ℂ) * (B : Matrix n n ℂ)).trace.im = 0 := by
  apply Complex.conj_eq_iff_im.mp
  change star (((A : Matrix n n ℂ) * (B : Matrix n n ℂ)).trace) = _
  rw [← trace_conjTranspose, conjTranspose_mul, (show (A : Matrix n n ℂ)ᴴ = A from A.property), (show (B : Matrix n n ℂ)ᴴ = B from B.property), trace_mul_comm]

theorem pairing_symm : (pairing (n := n)).IsSymm := by
  constructor
  intro A B
  exact congrArg Complex.re (trace_mul_comm _ _)

theorem pairing_self_eq_zero (A : Herm n) (h : pairing A A = 0) : A = 0 := by
  apply Subtype.ext
  apply trace_conjTranspose_mul_self_eq_zero_iff.mp
  apply Complex.ext
  · simpa only [(show (A : Matrix n n ℂ)ᴴ = A from A.property), pairing_apply, Complex.zero_re] using h
  · simpa only [(show (A : Matrix n n ℂ)ᴴ = A from A.property), Complex.zero_im] using trace_pair_im A A

theorem pairing_nondegenerate : (pairing (n := n)).Nondegenerate :=
  ⟨fun A h => pairing_self_eq_zero A (h A), fun A h => pairing_self_eq_zero A (h A)⟩

theorem pairing_product (A C : Herm n) (B D : Herm m) :
    pairing (product A B) (product C D) = pairing A C * pairing B D := by
  change (((A : Matrix n n ℂ) ⊗ₖ (B : Matrix m m ℂ)) *
    ((C : Matrix n n ℂ) ⊗ₖ (D : Matrix m m ℂ))).trace.re = _
  rw [← mul_kronecker_mul, trace_kronecker, Complex.mul_re]
  simp only [trace_pair_im, mul_zero, sub_zero, pairing_apply]

#print axioms product_span
#print axioms pairing_nondegenerate

end TensorTomography
