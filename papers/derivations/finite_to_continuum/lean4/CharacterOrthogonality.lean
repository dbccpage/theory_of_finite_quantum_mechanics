import Mathlib.Analysis.Fourier.AddCircle
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Push




namespace FiniteToContinuum

attribute [local instance] Classical.propDecidable

open scoped BigOperators

variable {R : Type*} [CommRing R]

def delta (k : ℤ) : R :=
  if k = 0 then 1 else 0

@[simp]
theorem delta_zero : (delta (0 : ℤ) : R) = 1 := by
  simp [delta]

@[simp]
theorem delta_ne_zero {k : ℤ} (hk : k ≠ 0) : (delta k : R) = 0 := by
  simp [delta, hk]

structure AdditiveChar (G : Type*) [AddCommGroup G] (R : Type*) [CommRing R] where
  toFun : G → R
  map_zero' : toFun 0 = 1
  map_add' : ∀ x y : G, toFun (x + y) = toFun x * toFun y

instance {G : Type*} [AddCommGroup G] {R : Type*} [CommRing R] :
    CoeFun (AdditiveChar G R) (fun _ => G → R) where
  coe χ := χ.toFun

theorem char_sum_translation_cancel {G R : Type*} [AddCommGroup G] [Fintype G] [Field R]
    (χ : AdditiveChar G R) (y : G) (hy : χ y ≠ 1) :
    (∑ x : G, χ x) = 0 := by
  have hshift : (∑ x : G, χ (x + y)) = (∑ x : G, χ x) := by
    let e : G ≃ G := Equiv.addRight y
    have hequiv := Equiv.sum_comp e χ.toFun
    exact hequiv
  have hmul : (∑ x : G, χ (x + y)) = χ y * (∑ x : G, χ x) := by
    calc
      (∑ x : G, χ (x + y)) = ∑ x : G, (χ x * χ y) := by
        apply Fintype.sum_congr
        intro x
        exact χ.map_add' x y
      _ = (∑ x : G, χ x) * χ y := by
        rw [Finset.sum_mul]
      _ = χ y * (∑ x : G, χ x) := by
        exact mul_comm _ _
  have heq : χ y * (∑ x : G, χ x) = (∑ x : G, χ x) := hmul.symm.trans hshift
  have hsub : (χ y - 1) * (∑ x : G, χ x) = 0 := by
    calc
      (χ y - 1) * (∑ x : G, χ x) = χ y * (∑ x : G, χ x) - (∑ x : G, χ x) := by ring
      _ = 0 := sub_eq_zero.mpr heq
  have hne : χ y - 1 ≠ 0 := sub_ne_zero.mpr hy
  exact (mul_eq_zero.mp hsub).resolve_left hne

theorem trivial_char_sum {G R : Type*} [AddCommGroup G] [Fintype G] [Field R]
    (χ : AdditiveChar G R) (htriv : ∀ x, χ x = 1) :
    (∑ x : G, χ x) = Fintype.card G := by
  calc
    (∑ x : G, χ x) = ∑ x : G, (1 : R) := by
      apply Fintype.sum_congr
      intro x
      exact htriv x
    _ = Fintype.card G := by
      simp

theorem normalized_character_sum {G R : Type*} [AddCommGroup G] [Fintype G] [Field R]
    (χ : AdditiveChar G R) (hcard_pos : (Fintype.card G : R) ≠ 0) :
    ((Fintype.card G : R)⁻¹ * (∑ x : G, χ x)) = (if (∀ x, χ x = 1) then (1 : R) else 0) := by
  by_cases htriv : ∀ x, χ x = 1
  · rw [ite_eq_left htriv, trivial_char_sum χ htriv]
    exact inv_mul_cancel₀ hcard_pos
  · simp [htriv]
    push Not at htriv
    rcases htriv with ⟨y, hy⟩
    have hzero := char_sum_translation_cancel χ y hy
    rw [hzero]
    simp

end FiniteToContinuum
