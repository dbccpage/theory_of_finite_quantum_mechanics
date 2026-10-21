import Mathlib.Analysis.InnerProductSpace.Spectrum
import Mathlib.Analysis.Normed.Module.Normalize
import Mathlib.LinearAlgebra.UnitaryGroup

open scoped ComplexConjugate InnerProductSpace
open WithLp Matrix NormedSpace

namespace TensorSchmidt

abbrev Space (n : ℕ) := EuclideanSpace ℂ (Fin n)

/-- Rectangular Schmidt bases, including the kernel and arbitrary n ≤ m. -/
theorem exists_schmidt_bases {n m : ℕ} (hnm : n ≤ m)
    (T : Space n →ₗ[ℂ] Space m) :
    ∃ (u : OrthonormalBasis (Fin n) ℂ (Space n))
      (v : OrthonormalBasis (Fin m) ℂ (Space m)) (s : Fin n → ℝ),
      (∀ i, 0 ≤ s i) ∧ ∀ i, T (u i) = (s i : ℂ) • v (Fin.castLE hnm i) := by
  classical
  have hn : Module.finrank ℂ (Space n) = n := by simp [Space]
  let u := T.isSymmetric_adjoint_comp_self.eigenvectorBasis hn
  have ho : Pairwise fun i j => ⟪T (u i), T (u j)⟫_ℂ = 0 := by
    intro i j hij
    rw [← T.adjoint_inner_right]
    change ⟪u i, (T.adjoint ∘ₗ T) (u j)⟫_ℂ = 0
    rw [T.isSymmetric_adjoint_comp_self.apply_eigenvectorBasis]
    rw [inner_smul_real_right]
    change _ • ⟪u i, u j⟫_ℂ = 0
    rw [u.inner_eq_ite, if_neg hij, smul_zero]
  let e : Fin n → Fin m := Fin.castLE hnm
  have he : Function.Injective e := Fin.castLE_injective hnm
  let f : Fin m → Space m :=
    Function.extend e (fun i => (‖T (u i)‖ : ℂ)⁻¹ • T (u i)) 0
  have hf (i : Fin n) : f (e i) = (‖T (u i)‖ : ℂ)⁻¹ • T (u i) :=
    he.extend_apply _ _ i
  let S : Set (Fin m) := e '' {i | T (u i) ≠ 0}
  have horth : Orthonormal ℂ (S.domRestrict f) := by
    constructor
    · intro i
      obtain ⟨j, hj, hji⟩ := i.property
      change ‖f i.val‖ = 1
      rw [← hji, hf]
      simp only [norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_norm]
      exact inv_mul_cancel₀ (norm_ne_zero_iff.mpr hj)
    · intro i j hij
      obtain ⟨a, ha, hai⟩ := i.property
      obtain ⟨b, hb, hbj⟩ := j.property
      have hab : a ≠ b := by
        intro h
        apply hij
        apply Subtype.ext
        rw [← hai, ← hbj, h]
      change ⟪f i.val, f j.val⟫_ℂ = 0
      rw [← hai, ← hbj, hf, hf]
      simp [inner_smul_left, inner_smul_right, ho hab]
  obtain ⟨v, hv⟩ := horth.exists_orthonormalBasis_extension_of_card_eq (by simp [Space])
  refine ⟨u, v, fun i => ‖T (u i)‖, fun _ => norm_nonneg _, ?_⟩
  intro i
  by_cases hi : T (u i) = 0
  · simp [hi]
  · have hSi : e i ∈ S := ⟨i, hi, rfl⟩
    rw [hv _ hSi, hf]
    rw [smul_smul, mul_inv_cancel₀ (by simpa using norm_ne_zero_iff.mpr hi), one_smul]

#print axioms exists_schmidt_bases

end TensorSchmidt
