import ConcreteJordanProducts

/-! Positivity is identified with squares for the two concrete real products.
The spin proof treats the zero-vector case separately, then takes square roots of t plus or minus norm(v).
It is an exact existence construction over the declared real field. -/
noncomputable section
namespace FiniteQM.JordanConeSquares
open ConcreteJordanProducts

theorem classical_positive_iff_square {r : ℕ} (a : Fin r → ℝ) :
    classicalPositive a ↔ ∃ b, classicalMul b b = a := by
  constructor
  · intro hp
    refine ⟨fun i => Real.sqrt (a i), ?_⟩
    funext i
    exact Real.mul_self_sqrt (hp i)
  · rintro ⟨b, rfl⟩
    exact classical_square_positive b

/-- The declared Lorentz cone is exactly the cone of Jordan squares, including its boundary. -/
theorem spin_positive_iff_square (a : Spin3) :
    spinPositive a ↔ ∃ b, spinMul b b = a := by
  constructor
  · intro hp
    by_cases hz : a.2 = 0
    · have ht : 0 ≤ a.1 := by simpa [spinPositive, hz] using hp
      refine ⟨(Real.sqrt a.1, 0), ?_⟩
      apply Prod.ext
      · simpa [spinMul] using Real.mul_self_sqrt ht
      · simp [spinMul, hz]
    · have hn : ‖a.2‖ ≠ 0 := norm_ne_zero_iff.mpr hz
      let r := ‖a.2‖
      let u : EuclideanSpace ℝ (Fin 3) := r⁻¹ • a.2
      have hu : ‖u‖ = 1 := by simp [u, r, norm_smul, hn]
      have hru : r • u = a.2 := by simp [u, r, smul_smul, hn]
      have hp' : r ≤ a.1 := hp
      have hr : 0 ≤ r := norm_nonneg a.2
      let α := Real.sqrt (a.1 + r)
      let β := Real.sqrt (a.1 - r)
      have hα : α^2 = a.1 + r := Real.sq_sqrt (by linarith)
      have hβ : β^2 = a.1 - r := Real.sq_sqrt (by linarith)
      let s := (α+β)/2
      let c := (α-β)/2
      have hsc : s*s+c*c = a.1 := by dsimp [s, c]; nlinarith [hα, hβ]
      have hrc : 2*s*c = r := by dsimp [s, c]; nlinarith [hα, hβ]
      refine ⟨(s, c • u), ?_⟩
      apply Prod.ext
      · change s*s + inner ℝ (c • u) (c • u) = a.1
        simpa [real_inner_smul_left, real_inner_smul_right, real_inner_self_eq_norm_sq, hu] using hsc
      · change s • (c • u) + s • (c • u) = a.2
        rw [← add_smul, smul_smul]
        have hcoef : (s+s)*c = r := by nlinarith [hrc]
        rw [hcoef]
        exact hru
  · rintro ⟨b, rfl⟩
    exact spin_square_positive b

#print axioms classical_positive_iff_square
#print axioms spin_positive_iff_square
end FiniteQM.JordanConeSquares