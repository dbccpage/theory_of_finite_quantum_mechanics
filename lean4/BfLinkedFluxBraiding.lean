


namespace BfLinkedFluxBraiding

universe u

structure BfLevel where
  k : Nat
  h_k : k ≥ 2

abbrev LinkingNumber := Int

def monodromyNumerator (q p : Nat) (lk : LinkingNumber) : Int :=
  (q : Int) * (p : Int) * lk

theorem unlinked_loops_monodromy_zero (q p : Nat) :
    monodromyNumerator q p 0 = 0 := by
  dsimp [monodromyNumerator]
  rw [Int.mul_zero]


def level2 : BfLevel := ⟨2, by decide⟩

theorem level2_hopf_monodromy_odd :
    monodromyNumerator 1 1 1 % 2 ≠ 0 := by
  dsimp [monodromyNumerator]
  decide

theorem level2_symmetric_orientation_cancels (w : Nat) :
    (w : Int) * 1 + (w : Int) * (-1) = 0 := by
  rw [Int.mul_one, Int.mul_neg, Int.mul_one, Int.add_right_neg]


def level3 : BfLevel := ⟨3, by decide⟩

theorem level3_involution_order_clash :
    Nat.gcd 2 level3.k = 1 := rfl

theorem level3_hopf_monodromy_nontrivial :
    (monodromyNumerator 1 1 1).natAbs % level3.k ≠ 0 := by
  dsimp [monodromyNumerator, level3]
  decide


structure OrientationEnergyGap where
  delta_E : Nat
  h_asymm : delta_E > 0

theorem orientation_gap_forces_weight_split (base_w : Nat) (gap : OrientationEnergyGap) :
    base_w ≠ base_w + gap.delta_E := by
  have h := gap.h_asymm
  omega

theorem orientation_asymmetric_residual_nonzero (w_pos w_neg : Nat) (h_ne : w_pos ≠ w_neg) :
    (w_pos : Int) * 1 + (w_neg : Int) * (-1) ≠ 0 := by
  rw [Int.mul_one, Int.mul_neg, Int.mul_one]
  intro h_zero
  have : w_pos = w_neg := by omega
  exact h_ne this

end BfLinkedFluxBraiding
