/-
L1-GS001-GAUGE-L1, two integer coordinates.

Signed permutations are a coordinate swap and a sign on each coordinate.
The unweighted aggregate is |x| + |y|.
Weighted aggregates use natural weights.
No general gauge presentation and no bounded-linear classification.
-/

namespace CampaignL1Gs001GaugeL1

def l1 (x y : Int) : Nat := x.natAbs + y.natAbs

def weighted (w1 w2 : Nat) (x y : Int) : Nat :=
  w1 * x.natAbs + w2 * y.natAbs

def applyGauge (swap sx sy : Bool) (x y : Int) : Int × Int :=
  let x' := if sx then -x else x
  let y' := if sy then -y else y
  if swap then (y', x') else (x', y')

theorem l1_sign_invariant (x y : Int) :
    l1 (-x) y = l1 x y ∧ l1 x (-y) = l1 x y ∧ l1 (-x) (-y) = l1 x y := by
  simp [l1, Int.natAbs_neg]

theorem l1_swap_invariant (x y : Int) : l1 y x = l1 x y := by
  simp [l1, Nat.add_comm]

theorem signed_permutation_preserves_l1 (swap sx sy : Bool) (x y : Int) :
    l1 (applyGauge swap sx sy x y).1 (applyGauge swap sx sy x y).2 = l1 x y := by
  cases swap <;> cases sx <;> cases sy <;>
    simp [applyGauge, l1, Int.natAbs_neg, Nat.add_comm]

theorem edge_additive (x y : Int) : l1 x 0 + l1 0 y = l1 x y := by
  simp [l1]

theorem absolutely_homogeneous (k x y : Int) :
    l1 (k * x) (k * y) = k.natAbs * l1 x y := by
  simp [l1, Int.natAbs_mul, Nat.mul_add]

theorem eight_images_of_one_two :
    applyGauge false false false 1 2 = (1, 2) ∧
    applyGauge false true false 1 2 = (-1, 2) ∧
    applyGauge false false true 1 2 = (1, -2) ∧
    applyGauge false true true 1 2 = (-1, -2) ∧
    applyGauge true false false 1 2 = (2, 1) ∧
    applyGauge true true false 1 2 = (2, -1) ∧
    applyGauge true false true 1 2 = (-2, 1) ∧
    applyGauge true true true 1 2 = (-2, -1) ∧
    ([(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)] :
      List (Int × Int)).Nodup := by
  decide

theorem faithful_on_one_two
    (s1 sx1 sy1 s2 sx2 sy2 : Bool)
    (h : applyGauge s1 sx1 sy1 1 2 = applyGauge s2 sx2 sy2 1 2) :
    s1 = s2 ∧ sx1 = sx2 ∧ sy1 = sy2 := by
  cases s1 <;> cases sx1 <;> cases sy1 <;> cases s2 <;> cases sx2 <;> cases sy2 <;>
    simp [applyGauge] at h <;> (try cases h) <;> exact ⟨rfl, rfl, rfl⟩

theorem swap_invariant_weighted_iff (w1 w2 : Nat) :
    (∀ x y : Int, weighted w1 w2 x y = weighted w1 w2 y x) ↔ w1 = w2 := by
  constructor
  · intro h
    have h10 : weighted w1 w2 1 0 = weighted w1 w2 0 1 := h 1 0
    have hleft : weighted w1 w2 1 0 = w1 := by
      simp [weighted]
    have hright : weighted w1 w2 0 1 = w2 := by
      simp [weighted]
    omega
  · rintro rfl x y
    simp [weighted, Nat.add_comm]

theorem equal_weight_is_scaled_l1 (w : Nat) (x y : Int) :
    weighted w w x y = w * l1 x y := by
  simp [weighted, l1, Nat.mul_add]

theorem unequal_weights_separate_axes :
    weighted 1 2 1 0 = 1 ∧ weighted 1 2 0 1 = 2 ∧ (1 : Nat) ≠ 2 := by
  decide

theorem equal_squared_length_splits_l1 :
    ((3 : Int) * 3 + 4 * 4 = 25) ∧
    ((5 : Int) * 5 + 0 * 0 = 25) ∧
    l1 3 4 = 7 ∧
    l1 5 0 = 5 ∧
    (7 : Nat) ≠ 5 := by
  decide

theorem signed_permutation_gauge_shadow :
    (∀ (x y k : Int) (swap sx sy : Bool),
      l1 (applyGauge swap sx sy x y).1 (applyGauge swap sx sy x y).2 = l1 x y ∧
      l1 x 0 + l1 0 y = l1 x y ∧
      l1 (k * x) (k * y) = k.natAbs * l1 x y) ∧
    (applyGauge false false false 1 2 = (1, 2) ∧
      applyGauge false true false 1 2 = (-1, 2) ∧
      applyGauge false false true 1 2 = (1, -2) ∧
      applyGauge false true true 1 2 = (-1, -2) ∧
      applyGauge true false false 1 2 = (2, 1) ∧
      applyGauge true true false 1 2 = (2, -1) ∧
      applyGauge true false true 1 2 = (-2, 1) ∧
      applyGauge true true true 1 2 = (-2, -1) ∧
      ([(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)] :
        List (Int × Int)).Nodup) ∧
    (∀ s1 sx1 sy1 s2 sx2 sy2 : Bool,
      applyGauge s1 sx1 sy1 1 2 = applyGauge s2 sx2 sy2 1 2 →
        s1 = s2 ∧ sx1 = sx2 ∧ sy1 = sy2) ∧
    (∀ w1 w2 : Nat,
      (∀ x y : Int, weighted w1 w2 x y = weighted w1 w2 y x) ↔ w1 = w2) ∧
    (∀ (w : Nat) (x y : Int), weighted w w x y = w * l1 x y) ∧
    (weighted 1 2 1 0 = 1 ∧ weighted 1 2 0 1 = 2 ∧ (1 : Nat) ≠ 2) ∧
    (((3 : Int) * 3 + 4 * 4 = 25) ∧ ((5 : Int) * 5 + 0 * 0 = 25) ∧
      l1 3 4 = 7 ∧ l1 5 0 = 5 ∧ (7 : Nat) ≠ 5) := by
  refine ⟨?_, eight_images_of_one_two, ?_, swap_invariant_weighted_iff,
    equal_weight_is_scaled_l1, unequal_weights_separate_axes, equal_squared_length_splits_l1⟩
  · intro x y k swap sx sy
    exact ⟨signed_permutation_preserves_l1 swap sx sy x y, edge_additive x y,
      absolutely_homogeneous k x y⟩
  · intro s1 sx1 sy1 s2 sx2 sy2 h
    exact faithful_on_one_two s1 sx1 sy1 s2 sx2 sy2 h

#print axioms l1_sign_invariant
#print axioms l1_swap_invariant
#print axioms signed_permutation_preserves_l1
#print axioms edge_additive
#print axioms absolutely_homogeneous
#print axioms eight_images_of_one_two
#print axioms faithful_on_one_two
#print axioms swap_invariant_weighted_iff
#print axioms equal_weight_is_scaled_l1
#print axioms unequal_weights_separate_axes
#print axioms equal_squared_length_splits_l1
#print axioms signed_permutation_gauge_shadow

end CampaignL1Gs001GaugeL1
