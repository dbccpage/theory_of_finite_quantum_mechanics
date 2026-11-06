import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.Algebra.Module.Pi
import Mathlib.Algebra.Field.Rat

/-! Finite rational cochain presentations and observable equivariance.
These are model statements and give no Genesis extension authority. -/

namespace FiniteToContinuum

abbrev State (n : ℕ) := Fin n → ℚ

structure CochainPresentation (n0 n1 n2 : ℕ) where
  d0 : State n0 →ₗ[ℚ] State n1
  d1 : State n1 →ₗ[ℚ] State n2
  law : ∀ x, d1 (d0 x) = 0

structure CochainSymmetry {n0 n1 n2 : ℕ} (C : CochainPresentation n0 n1 n2) where
  p0 : State n0 ≃ₗ[ℚ] State n0
  p1 : State n1 ≃ₗ[ℚ] State n1
  p2 : State n2 ≃ₗ[ℚ] State n2
  commute0 : ∀ x, C.d0 (p0 x) = p1 (C.d0 x)
  commute1 : ∀ x, C.d1 (p1 x) = p2 (C.d1 x)

theorem symmetry_preserves_cocycles {n0 n1 n2 : ℕ}
    {C : CochainPresentation n0 n1 n2} (s : CochainSymmetry C)
    (x : State n1) (hx : C.d1 x = 0) : C.d1 (s.p1 x) = 0 := by
  rw [s.commute1, hx]
  exact s.p2.map_zero

theorem symmetry_preserves_coboundaries {n0 n1 n2 : ℕ}
    {C : CochainPresentation n0 n1 n2} (s : CochainSymmetry C)
    (x : State n1) (hx : ∃ y, C.d0 y = x) : ∃ y, C.d0 y = s.p1 x := by
  rcases hx with ⟨y, hy⟩
  exact ⟨s.p0 y, by rw [s.commute0, hy]⟩

theorem difference_symmetry_preserves_kernel {n : ℕ}
    (D : State n →ₗ[ℚ] State n) (P : State n ≃ₗ[ℚ] State n)
    (commute : ∀ x, D (P x) = P (D x)) (x : State n) (hx : D x = 0) :
    D (P x) = 0 := by
  rw [commute, hx]
  exact P.map_zero

end FiniteToContinuum
