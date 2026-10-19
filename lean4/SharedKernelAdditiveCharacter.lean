import Mathlib.Algebra.BigOperators.Field
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic.Ring

/-!
# SharedKernel — finite additive-character cancellation

Reusable finite-sum cancellation under translation scaling. Not MUB-specific.
Extracted from the MUB programme (2026-07-24) so other libraries can depend
without importing `MUB`.
-/

namespace SharedKernel

open scoped BigOperators

theorem finite_sum_eq_scaled_sum_from_translation
    {α R : Type*} [Fintype α] [Field R]
    (e : α ≃ α) (χ : α -> R) (c : R)
    (hshift : ∀ x, χ (e x) = c * χ x) :
    (∑ x, χ x) = c * ∑ x, χ x := by
  have hperm : (∑ x, χ (e x)) = ∑ x, χ x := by
    simpa using (Equiv.sum_comp e χ)
  have hscale : (∑ x, χ (e x)) = c * ∑ x, χ x := by
    calc
      (∑ x, χ (e x)) = ∑ x, c * χ x := by
        apply Fintype.sum_congr
        intro x
        exact hshift x
      _ = c * ∑ x, χ x := by
        simp [Finset.mul_sum]
  exact hperm.symm.trans hscale

theorem finite_character_sum_vanishes_from_nontrivial_translation
    {α R : Type*} [Fintype α] [Field R]
    (e : α ≃ α) (χ : α -> R) (c : R)
    (hshift : ∀ x, χ (e x) = c * χ x)
    (hc : c ≠ 1) :
    (∑ x, χ x) = 0 := by
  have hfixed : (∑ x, χ x) = c * ∑ x, χ x :=
    finite_sum_eq_scaled_sum_from_translation e χ c hshift
  have hzero : (1 - c) * (∑ x, χ x) = 0 := by
    calc
      (1 - c) * (∑ x, χ x) = (∑ x, χ x) - c * (∑ x, χ x) := by ring
      _ = 0 := by
        exact sub_eq_zero.mpr hfixed
  have hone : 1 - c ≠ 0 := by
    intro h
    have h1c : (1 : R) = c := sub_eq_zero.mp h
    exact hc h1c.symm
  exact (mul_eq_zero.mp hzero).resolve_left hone

end SharedKernel
