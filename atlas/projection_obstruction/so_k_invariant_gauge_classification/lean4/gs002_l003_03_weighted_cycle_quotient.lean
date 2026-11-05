import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Order.Bounds.Basic

open scoped BigOperators

/-
Weighted cycle quotient (PL-003-E)

For a finite directed cycle:
  quotient norm with weights w_e
  equals min_e w_e * j(sum cycle)
-/

noncomputable section

variable {E V : Type*} [Fintype E] [DecidableEq E] [NormedAddCommGroup V]

def cycleCirculation (η : E → V) : V :=
  ∑ e : E, η e

omit [DecidableEq E] in
lemma cycleCirculation_sub (η θ : E → V) :
    cycleCirculation (fun e => η e - θ e) =
      cycleCirculation η - cycleCirculation θ := by
  unfold cycleCirculation
  rw [Finset.sum_sub_distrib]

omit [DecidableEq E] in
lemma cycleCirculation_sub_eq_zero_of_eq (η θ : E → V)
    (h : cycleCirculation η = cycleCirculation θ) :
    cycleCirculation (fun e => η e - θ e) = 0 := by
  rw [cycleCirculation_sub, h, sub_self]

omit [DecidableEq E] in
lemma cycleCirculation_eq_of_sub_eq_zero (η θ : E → V)
    (h : cycleCirculation (fun e => η e - θ e) = 0) :
    cycleCirculation η = cycleCirculation θ := by
  have hsub : cycleCirculation η - cycleCirculation θ = 0 := by
    simpa [cycleCirculation_sub] using h
  exact sub_eq_zero.mp hsub

omit [DecidableEq E] in
theorem same_cycle_circulation_iff_zero_difference (η θ : E → V) :
    cycleCirculation η = cycleCirculation θ ↔
      cycleCirculation (fun e => η e - θ e) = 0 := by
  constructor
  · exact cycleCirculation_sub_eq_zero_of_eq η θ
  · exact cycleCirculation_eq_of_sub_eq_zero η θ

def weightedCycleCost (w : E → ℝ) (η : E → V) : ℝ :=
  ∑ e : E, w e * ‖η e‖

def cycleCostSet (w : E → ℝ) (S : V) : Set ℝ :=
  {q | ∃ η : E → V, cycleCirculation η = S ∧ q = weightedCycleCost w η}

def singleEdgeCochain (e₀ : E) (S : V) : E → V :=
  fun e => if e = e₀ then S else 0

lemma circulation_singleEdgeCochain (e₀ : E) (S : V) :
    cycleCirculation (singleEdgeCochain e₀ S) = S := by
  unfold cycleCirculation singleEdgeCochain
  rw [Fintype.sum_eq_single e₀]
  · simp
  · intro e he
    simp [he]

lemma cost_singleEdgeCochain (w : E → ℝ) (e₀ : E) (S : V) :
    weightedCycleCost w (singleEdgeCochain e₀ S) = w e₀ * ‖S‖ := by
  unfold weightedCycleCost singleEdgeCochain
  rw [Fintype.sum_eq_single e₀]
  · simp
  · intro e he
    simp [he]

def normalizedCycleCost (η : E → V) : ℝ :=
  ∑ e : E, ‖η e‖

def normalizedCycleCostSet (S : V) : Set ℝ :=
  {q | ∃ η : E → V, cycleCirculation η = S ∧ q = normalizedCycleCost η}

lemma cost_singleEdgeCochain_normalized (e₀ : E) (S : V) :
    normalizedCycleCost (singleEdgeCochain e₀ S) = ‖S‖ := by
  unfold normalizedCycleCost singleEdgeCochain
  rw [Fintype.sum_eq_single e₀]
  · simp
  · intro e he
    simp [he]

omit [DecidableEq E] in
lemma normalized_cycle_lower_bound (S : V) (η : E → V)
    (hη : cycleCirculation η = S) :
    ‖S‖ ≤ normalizedCycleCost η := by
  unfold normalizedCycleCost
  rw [← hη]
  exact norm_sum_le Finset.univ (fun e => η e)

theorem normalized_cycle_quotient (e₀ : E) (S : V) :
    IsGLB (normalizedCycleCostSet (E := E) S) ‖S‖ := by
  refine ⟨?lower, ?greatest⟩
  · intro q hq
    rcases hq with ⟨η, hη, rfl⟩
    exact normalized_cycle_lower_bound S η hη
  · intro y hy
    have hmem :
        normalizedCycleCost (singleEdgeCochain e₀ S) ∈
          normalizedCycleCostSet (E := E) S := by
      exact ⟨singleEdgeCochain e₀ S, circulation_singleEdgeCochain e₀ S, rfl⟩
    have hy_le : y ≤ normalizedCycleCost (singleEdgeCochain e₀ S) := hy hmem
    simpa [cost_singleEdgeCochain_normalized] using hy_le

omit [DecidableEq E] in
lemma weighted_cycle_lower_bound
    (w : E → ℝ) (eMin : E) (S : V) (η : E → V)
    (hmin_nonneg : 0 ≤ w eMin)
    (hmin : ∀ e : E, w eMin ≤ w e)
    (hη : cycleCirculation η = S) :
    w eMin * ‖S‖ ≤ weightedCycleCost w η := by
  have hnorm : ‖S‖ ≤ ∑ e : E, ‖η e‖ := by
    rw [← hη]
    exact norm_sum_le Finset.univ (fun e => η e)
  calc
    w eMin * ‖S‖ ≤ w eMin * (∑ e : E, ‖η e‖) :=
      mul_le_mul_of_nonneg_left hnorm hmin_nonneg
    _ = ∑ e : E, w eMin * ‖η e‖ := by
      rw [Finset.mul_sum]
    _ ≤ ∑ e : E, w e * ‖η e‖ := by
      exact Finset.sum_le_sum fun e _ =>
        mul_le_mul_of_nonneg_right (hmin e) (norm_nonneg (η e))

theorem weighted_cycle_quotient
    (w : E → ℝ) (eMin : E) (S : V)
    (hmin_nonneg : 0 ≤ w eMin)
    (hmin : ∀ e : E, w eMin ≤ w e) :
    IsGLB (cycleCostSet w S) (w eMin * ‖S‖) := by
  refine ⟨?lower, ?greatest⟩
  · intro q hq
    rcases hq with ⟨η, hη, rfl⟩
    exact weighted_cycle_lower_bound w eMin S η hmin_nonneg hmin hη
  · intro y hy
    have hmem : weightedCycleCost w (singleEdgeCochain eMin S) ∈ cycleCostSet w S := by
      exact ⟨singleEdgeCochain eMin S, circulation_singleEdgeCochain eMin S, rfl⟩
    have hy_le : y ≤ weightedCycleCost w (singleEdgeCochain eMin S) := hy hmem
    simpa [cost_singleEdgeCochain] using hy_le

#print axioms cycleCirculation_sub
#print axioms cycleCirculation_sub_eq_zero_of_eq
#print axioms cycleCirculation_eq_of_sub_eq_zero
#print axioms same_cycle_circulation_iff_zero_difference
#print axioms circulation_singleEdgeCochain
#print axioms cost_singleEdgeCochain
#print axioms cost_singleEdgeCochain_normalized
#print axioms normalized_cycle_lower_bound
#print axioms normalized_cycle_quotient
#print axioms weighted_cycle_lower_bound
#print axioms weighted_cycle_quotient
