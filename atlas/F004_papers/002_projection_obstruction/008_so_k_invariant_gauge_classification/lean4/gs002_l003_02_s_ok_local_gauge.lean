import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Tactic.Ring

/-
SO(k) local gauge theorem, simplified (PL-003-C)

Assume:
  ∀ x y, ‖x‖₂ = ‖y‖₂ → j x = j y
  j (r • x) = |r| * j x
  j u = c for all unit u

Then:
  j x = c * ‖x‖₂
-/

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

omit [NormedSpace ℝ V] in
theorem sphere_const_of_unit_transitive
    (j : V → ℝ)
    (Related : V → V → Prop)
    (unit_transitive :
      ∀ u v : V, ‖u‖ = 1 → ‖v‖ = 1 → Related u v)
    (invariant : ∀ u v : V, Related u v → j u = j v) :
    ∀ u v : V, ‖u‖ = 1 → ‖v‖ = 1 → j u = j v := by
  intro u v hu hv
  exact invariant u v (unit_transitive u v hu hv)

theorem so_k_local_gauge_simplified
    (j : V → ℝ)
    (sphere_const : ∀ u v : V, ‖u‖ = 1 → ‖v‖ = 1 → j u = j v)
    (nonneg : ∀ x : V, 0 ≤ j x)
    (homog : ∀ (r : ℝ) (x : V), j (r • x) = |r| * j x)
    (faithful : ∀ x : V, j x = 0 ↔ x = 0) :
    ∃ c : ℝ, 0 < c ∧ ∀ x : V, j x = c * ‖x‖ := by
  by_cases hV : ∃ x : V, x ≠ 0
  · rcases hV with ⟨x₀, hx₀⟩
    let u₀ := (‖x₀‖⁻¹) • x₀
    have hu₀ : ‖u₀‖ = 1 := by
      rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀]
      exact norm_ne_zero_iff.mpr hx₀
    use j u₀
    have hu₀_ne : u₀ ≠ 0 :=
      norm_ne_zero_iff.mp (by rw [hu₀]; exact one_ne_zero)
    have hj_ne : j u₀ ≠ 0 := by
      intro hzero
      exact hu₀_ne ((faithful u₀).mp hzero)
    have hc : 0 < j u₀ := lt_of_le_of_ne' (nonneg u₀) hj_ne
    refine ⟨hc, fun x => ?_⟩
    rcases eq_or_ne x 0 with rfl | hx
    · have hj0 : j (0 : V) = 0 := by
        have h := homog 0 (0 : V)
        simpa using h
      rw [hj0, norm_zero, mul_zero]
    · let u := (‖x‖⁻¹) • x
      have hu : ‖u‖ = 1 := by
        rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀]
        exact norm_ne_zero_iff.mpr hx
      have hx_eq : x = ‖x‖ • u := by
        change x = ‖x‖ • (‖x‖⁻¹ • x)
        rw [← mul_smul, mul_inv_cancel₀, one_smul]
        exact norm_ne_zero_iff.mpr hx
      have hnorm_nonneg : 0 ≤ ‖x‖ := norm_nonneg x
      calc
        j x = j (‖x‖ • u) := congr_arg j hx_eq
        _ = ‖x‖ * j u := by rw [homog, abs_of_nonneg hnorm_nonneg]
        _ = ‖x‖ * j u₀ := by rw [sphere_const u u₀ hu hu₀]
        _ = j u₀ * ‖x‖ := mul_comm ‖x‖ (j u₀)
  · use 1
    constructor
    · exact zero_lt_one
    · intro x
      have hx : x = 0 := by
        by_contra hxne
        exact hV ⟨x, hxne⟩
      subst x
      have hj0 : j (0 : V) = 0 := by
        have h := homog 0 (0 : V)
        simpa using h
      rw [hj0, norm_zero, mul_zero]

theorem so_k_local_gauge_from_unit_transitive
    (j : V → ℝ)
    (Related : V → V → Prop)
    (unit_transitive :
      ∀ u v : V, ‖u‖ = 1 → ‖v‖ = 1 → Related u v)
    (invariant : ∀ u v : V, Related u v → j u = j v)
    (nonneg : ∀ x : V, 0 ≤ j x)
    (homog : ∀ (r : ℝ) (x : V), j (r • x) = |r| * j x)
    (faithful : ∀ x : V, j x = 0 ↔ x = 0) :
    ∃ c : ℝ, 0 < c ∧ ∀ x : V, j x = c * ‖x‖ := by
  exact so_k_local_gauge_simplified j
    (sphere_const_of_unit_transitive j Related unit_transitive invariant)
    nonneg homog faithful

/-!
## Constructive SO(2) Rotation Transitivity on S^1

Given unit vectors u, v ∈ ℝ², we construct an explicit 2×2 rotation matrix
R = [[a, -b], [b, a]] with a² + b² = 1 such that R u = v.
The construction uses polynomial algebra:
  a = u₁ v₁ + u₂ v₂
  b = u₁ v₂ - u₂ v₁
satisfying a² + b² = (u₁² + u₂²)(v₁² + v₂²) = 1 · 1 = 1.
-/

structure SO2Matrix where
  a : ℝ
  b : ℝ
  h_det : a ^ 2 + b ^ 2 = 1

def SO2Matrix.mulVec (R : SO2Matrix) (x : ℝ × ℝ) : ℝ × ℝ :=
  (R.a * x.1 - R.b * x.2, R.b * x.1 + R.a * x.2)

def inUnitCircle (x : ℝ × ℝ) : Prop :=
  x.1 ^ 2 + x.2 ^ 2 = 1

theorem so2_transitive_on_circle (u v : ℝ × ℝ)
    (hu : inUnitCircle u) (hv : inUnitCircle v) :
    ∃ R : SO2Matrix, R.mulVec u = v := by
  let a := u.1 * v.1 + u.2 * v.2
  let b := u.1 * v.2 - u.2 * v.1
  have h_det : a ^ 2 + b ^ 2 = 1 := by
    have h_id : a ^ 2 + b ^ 2 = (u.1 ^ 2 + u.2 ^ 2) * (v.1 ^ 2 + v.2 ^ 2) := by ring
    unfold inUnitCircle at hu hv
    rw [h_id, hu, hv, mul_one]
  let R : SO2Matrix := ⟨a, b, h_det⟩
  use R
  dsimp [SO2Matrix.mulVec, R, a, b]
  ext
  · have h1_id : (u.1 * v.1 + u.2 * v.2) * u.1 - (u.1 * v.2 - u.2 * v.1) * u.2 =
        (u.1 ^ 2 + u.2 ^ 2) * v.1 := by ring
    unfold inUnitCircle at hu
    rw [h1_id, hu, one_mul]
  · have h2_id : (u.1 * v.2 - u.2 * v.1) * u.1 + (u.1 * v.1 + u.2 * v.2) * u.2 =
        (u.1 ^ 2 + u.2 ^ 2) * v.2 := by ring
    unfold inUnitCircle at hu
    rw [h2_id, hu, one_mul]

def SO2Related (u v : ℝ × ℝ) : Prop :=
  ∃ R : SO2Matrix, R.mulVec u = v

theorem so2_unit_transitive (u v : ℝ × ℝ)
    (hu : inUnitCircle u) (hv : inUnitCircle v) :
    SO2Related u v :=
  so2_transitive_on_circle u v hu hv

theorem so2_circle_const (j : (ℝ × ℝ) → ℝ)
    (h_inv : ∀ (R : SO2Matrix) (x : ℝ × ℝ), j (R.mulVec x) = j x)
    (u v : ℝ × ℝ) (hu : inUnitCircle u) (hv : inUnitCircle v) :
    j u = j v := by
  rcases so2_transitive_on_circle u v hu hv with ⟨R, hR⟩
  rw [← hR, h_inv]

#print axioms SO2Matrix
#print axioms sphere_const_of_unit_transitive
#print axioms so_k_local_gauge_simplified
#print axioms so_k_local_gauge_from_unit_transitive
#print axioms so2_transitive_on_circle
#print axioms so2_unit_transitive
#print axioms so2_circle_const
