import MubQuadraticLiftCompatibility
import MubQuadraticLiftNarrowBox
import Mathlib.Data.Complex.BigOperators

/-!
# Quantitative separation of columns from the first two transitions

AuthorityEffect: None. The resulting regional exclusion criterion is a
necessary condition for every actual quartet, not a full-domain exclusion.
-/

noncomputable section
namespace MUB.QuadraticTransitionSeparation
open QuadraticLift QuadraticLiftCompatibility QuadraticLiftNarrowBox BoundedBlockChart
open scoped BigOperators

def columnDistance (r : Coord → ℝ) (i j : I6) : ℝ :=
  ∑ k, Complex.normSq (W r 0 k i - W r 1 k j)

theorem columnDistance_identity {r : Coord → ℝ} (h : System r) (i j : I6) :
    columnDistance r i j = 72 - 12 * (W r 2 i j).re := by
  have hc : (∑ k, star (W r 0 k i) * W r 1 k j) = (6 : ℂ) * W r 2 i j := by
    exact congrFun (congrFun (cycle_01 h) i) j
  have hr : ∑ k, (W r 0 k i * star (W r 1 k j)).re = 6 * (W r 2 i j).re := by
    calc
      _ = (∑ k, star (W r 0 k i) * W r 1 k j).re := by
        rw [Complex.re_sum]
        apply Finset.sum_congr rfl
        intro k _
        simp [Complex.mul_re, Complex.star_def]
      _ = ((6 : ℂ) * W r 2 i j).re := congrArg Complex.re hc
      _ = _ := by simp
  simp_rw [columnDistance, Complex.normSq_sub, h.overlapNorm]
  change (∑ k, (6 + 6 - 2 * (W r 0 k i * star (W r 1 k j)).re)) = _
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum, hr]
  norm_num [I6, Fintype.card_sum]
  ring

def separationLower : ℚ := 43623 / 1024

theorem separationLower_identity :
    (separationLower : ℝ) = 72 - 12 * (transitionRadius : ℝ) := by
  norm_num [separationLower, transitionRadius]

theorem separationLower_pos : 0 < (separationLower : ℝ) := by
  norm_num [separationLower]

theorem columnDistance_lower {r : Coord → ℝ} (h : System r) (i j : I6) :
    (separationLower : ℝ) ≤ columnDistance r i j := by
  rw [separationLower_identity, columnDistance_identity h]
  have hb := (components_of_norm_six (W r 2 i j) (h.overlapNorm 2 i j)).2.1
  linarith

theorem exclude_small_column_distance (r : Coord → ℝ) (i j : I6)
    (hsmall : columnDistance r i j < (separationLower : ℝ)) : ¬ System r := by
  intro h
  exact (not_lt_of_ge (columnDistance_lower h i j)) hsmall

theorem component_box_exclusion (r : Coord → ℝ) (i j : I6) (d : I6 → ℝ × ℝ)
    (hre : ∀ k, (W r 0 k i - W r 1 k j).re ^ 2 ≤ (d k).1)
    (him : ∀ k, (W r 0 k i - W r 1 k j).im ^ 2 ≤ (d k).2)
    (htotal : (∑ k, ((d k).1 + (d k).2)) < (separationLower : ℝ)) : ¬ System r := by
  apply exclude_small_column_distance r i j
  apply lt_of_le_of_lt _ htotal
  apply Finset.sum_le_sum
  intro k _
  simpa [Complex.normSq_apply, pow_two] using add_le_add (hre k) (him k)

theorem close_columns_box_excluded (r : Coord → ℝ) (i j : I6) (c : I6 → ℝ)
    (hr0 : ∀ k, (9 / 10 : ℝ) ≤ (W r 0 k i).re ∧ (W r 0 k i).re ≤ 11 / 10)
    (hr1 : ∀ k, (9 / 10 : ℝ) ≤ (W r 1 k j).re ∧ (W r 1 k j).re ≤ 11 / 10)
    (hi0 : ∀ k, c k - 1 / 20 ≤ (W r 0 k i).im ∧ (W r 0 k i).im ≤ c k + 1 / 20)
    (hi1 : ∀ k, c k - 1 / 20 ≤ (W r 1 k j).im ∧ (W r 1 k j).im ≤ c k + 1 / 20) :
    ¬ System r := by
  apply component_box_exclusion r i j (fun _ => (1 / 25, 1 / 100))
  · intro k
    have hl : -(1 / 5 : ℝ) ≤ (W r 0 k i).re - (W r 1 k j).re := by
      linarith [(hr0 k).1, (hr1 k).2]
    have hu : (W r 0 k i).re - (W r 1 k j).re ≤ (1 / 5 : ℝ) := by
      linarith [(hr0 k).2, (hr1 k).1]
    have hs := sq_le_sq' hl hu
    norm_num only [one_div, inv_pow, Nat.cast_pow, Nat.reducePow] at hs
    simpa only [Complex.sub_re] using hs
  · intro k
    have hl : -(1 / 10 : ℝ) ≤ (W r 0 k i).im - (W r 1 k j).im := by
      linarith [(hi0 k).1, (hi1 k).2]
    have hu : (W r 0 k i).im - (W r 1 k j).im ≤ (1 / 10 : ℝ) := by
      linarith [(hi0 k).2, (hi1 k).1]
    have hs := sq_le_sq' hl hu
    norm_num only [one_div, inv_pow, Nat.cast_pow, Nat.reducePow] at hs
    simpa only [Complex.sub_im] using hs
  · norm_num [I6, Fintype.card_sum, separationLower]

#print axioms columnDistance_identity
#print axioms separationLower_identity
#print axioms separationLower_pos
#print axioms columnDistance_lower
#print axioms exclude_small_column_distance
#print axioms component_box_exclusion
#print axioms close_columns_box_excluded
end MUB.QuadraticTransitionSeparation
