-- Campaign: FQ-GAP-STONE-CONTINUOUS-TIME. Not a default target.
-- Integer slice: 3 * 3 + 4 * 4 = 5 * 5, and 5 * a * a = 4 * b * b forces a = b = 0.
-- Continuous time, Stone, strong continuity, generator selection and causal order stay outside this module.

namespace CampaignFqGapStoneContinuousTime

theorem sqMod5 (n : Nat) :
    (n * n) % 5 = 0 ∨ (n * n) % 5 = 1 ∨ (n * n) % 5 = 4 := by
  have hmul : (n * n) % 5 = ((n % 5) * (n % 5)) % 5 := Nat.mul_mod n n 5
  have hdis : n % 5 = 0 ∨ n % 5 = 1 ∨ n % 5 = 2 ∨ n % 5 = 3 ∨ n % 5 = 4 := by
    have hlt : n % 5 < 5 := Nat.mod_lt n (by decide)
    omega
  rcases hdis with h0 | h1 | h2 | h3 | h4
  · rw [hmul, h0]; decide
  · rw [hmul, h1]; decide
  · rw [hmul, h2]; decide
  · rw [hmul, h3]; decide
  · rw [hmul, h4]; decide

theorem fourSqMod5Zero (b : Nat) (h : (4 * (b * b)) % 5 = 0) : b % 5 = 0 := by
  have hs := sqMod5 b
  have h4 : (4 * (b * b)) % 5 = (4 * ((b * b) % 5)) % 5 := by
    rw [Nat.mul_mod, Nat.mod_eq_of_lt (by decide : (4 : Nat) < 5)]
  rcases hs with h0 | h1 | h4sq
  · have hb0 : (b * b) % 5 = 0 := h0
    have hdis : b % 5 = 0 ∨ b % 5 = 1 ∨ b % 5 = 2 ∨ b % 5 = 3 ∨ b % 5 = 4 := by
      have hlt : b % 5 < 5 := Nat.mod_lt b (by decide)
      omega
    rcases hdis with hzero | hone | htwo | hthree | hfour
    · exact hzero
    · exfalso
      have honeSq : (b * b) % 5 = 1 := by rw [Nat.mul_mod, hone]
      rw [honeSq] at hb0
      cases hb0
    · exfalso
      have htwoSq : (b * b) % 5 = 4 := by rw [Nat.mul_mod, htwo]
      rw [htwoSq] at hb0
      cases hb0
    · exfalso
      have hthreeSq : (b * b) % 5 = 4 := by rw [Nat.mul_mod, hthree]
      rw [hthreeSq] at hb0
      cases hb0
    · exfalso
      have hfourSq : (b * b) % 5 = 1 := by rw [Nat.mul_mod, hfour]
      rw [hfourSq] at hb0
      cases hb0
  · exfalso
    rw [h4, h1] at h
    cases h
  · exfalso
    rw [h4, h4sq] at h
    cases h

theorem sqMod5Zero (n : Nat) (h : (n * n) % 5 = 0) : n % 5 = 0 := by
  have hs := sqMod5 n
  rcases hs with h0 | h1 | h4
  · have hdis : n % 5 = 0 ∨ n % 5 = 1 ∨ n % 5 = 2 ∨ n % 5 = 3 ∨ n % 5 = 4 := by
      have hlt : n % 5 < 5 := Nat.mod_lt n (by decide)
      omega
    rcases hdis with hzero | hone | htwo | hthree | hfour
    · exact hzero
    · exfalso
      have honeSq : (n * n) % 5 = 1 := by rw [Nat.mul_mod, hone]
      rw [honeSq] at h
      cases h
    · exfalso
      have htwoSq : (n * n) % 5 = 4 := by rw [Nat.mul_mod, htwo]
      rw [htwoSq] at h
      cases h
    · exfalso
      have hthreeSq : (n * n) % 5 = 4 := by rw [Nat.mul_mod, hthree]
      rw [hthreeSq] at h
      cases h
    · exfalso
      have hfourSq : (n * n) % 5 = 1 := by rw [Nat.mul_mod, hfour]
      rw [hfourSq] at h
      cases h
  · rw [h1] at h
    cases h
  · rw [h4] at h
    cases h

theorem fiveFourSquareForcesBZero (a b : Nat) (h : 5 * (a * a) = 4 * (b * b)) : b = 0 := by
  induction b using Nat.strongRecOn generalizing a with
  | ind b ih =>
    cases b with
    | zero => rfl
    | succ b' =>
      exfalso
      have hform : 5 * (a * a) = 4 * ((b' + 1) * (b' + 1)) := by
        simpa [Nat.succ_eq_add_one] using h
      have hmod : (4 * ((b' + 1) * (b' + 1))) % 5 = 0 := by
        have h5 : (5 * (a * a)) % 5 = 0 :=
          Nat.mod_eq_zero_of_dvd (Nat.dvd_mul_right 5 (a * a))
        rw [hform] at h5
        exact h5
      have hdiv : (b' + 1) % 5 = 0 := fourSqMod5Zero (b' + 1) hmod
      obtain ⟨r, hr⟩ := Nat.dvd_of_mod_eq_zero hdiv
      have hrpos : 0 < r := by
        cases r with
        | zero =>
          rw [Nat.mul_zero] at hr
          exact absurd hr (Nat.ne_of_gt (Nat.zero_lt_succ b'))
        | succ n =>
          exact Nat.succ_pos n
      have hrlt : r < b' + 1 := by
        have hmulLt : 1 * r < 5 * r :=
          Nat.mul_lt_mul_of_pos_right (by decide : (1 : Nat) < 5) hrpos
        have hr5 : r < 5 * r := by simpa [Nat.one_mul] using hmulLt
        simpa [hr] using hr5
      have h25 : (5 * r) * (5 * r) = 25 * (r * r) := by
        calc
          (5 * r) * (5 * r) = 5 * (r * (5 * r)) := Nat.mul_assoc 5 r (5 * r)
          _ = 5 * ((r * 5) * r) := by rw [← Nat.mul_assoc r 5 r]
          _ = 5 * ((5 * r) * r) := by rw [Nat.mul_comm r 5]
          _ = 5 * (5 * (r * r)) := by rw [Nat.mul_assoc 5 r r]
          _ = 25 * (r * r) := by omega
      have hmul : 5 * (a * a) = 100 * (r * r) := by
        calc
          5 * (a * a) = 4 * ((b' + 1) * (b' + 1)) := hform
          _ = 4 * ((5 * r) * (5 * r)) := by rw [hr]
          _ = 4 * (25 * (r * r)) := by rw [h25]
          _ = 100 * (r * r) := by omega
      have ha : a * a = 20 * (r * r) := by
        have hdiv5 : 5 * (a * a) = 5 * (20 * (r * r)) := by
          calc
            5 * (a * a) = 100 * (r * r) := hmul
            _ = 5 * (20 * (r * r)) := by omega
        exact Nat.mul_left_cancel (by decide : 0 < 5) hdiv5
      have hamod : (a * a) % 5 = 0 := by
        rw [ha]
        have hdvd : 5 ∣ 20 * (r * r) := by
          have h20 : 20 * (r * r) = 5 * (4 * (r * r)) := by omega
          rw [h20]
          exact Nat.dvd_mul_right 5 (4 * (r * r))
        exact Nat.mod_eq_zero_of_dvd hdvd
      have hadiv : a % 5 = 0 := sqMod5Zero a hamod
      obtain ⟨s, hs⟩ := Nat.dvd_of_mod_eq_zero hadiv
      have hdesc : 5 * (s * s) = 4 * (r * r) := by
        have hsq : (5 * s) * (5 * s) = 20 * (r * r) := by simpa [hs] using ha
        have hleft : (5 * s) * (5 * s) = 25 * (s * s) := by
          calc
            (5 * s) * (5 * s) = 5 * (s * (5 * s)) := Nat.mul_assoc 5 s (5 * s)
            _ = 5 * ((s * 5) * s) := by rw [← Nat.mul_assoc s 5 s]
            _ = 5 * ((5 * s) * s) := by rw [Nat.mul_comm s 5]
            _ = 5 * (5 * (s * s)) := by rw [Nat.mul_assoc 5 s s]
            _ = 25 * (s * s) := by omega
        have h25s : 25 * (s * s) = 20 * (r * r) := by simpa [hleft] using hsq
        have h5 : 5 * (5 * (s * s)) = 5 * (4 * (r * r)) := by
          calc
            5 * (5 * (s * s)) = 25 * (s * s) := by omega
            _ = 20 * (r * r) := h25s
            _ = 5 * (4 * (r * r)) := by omega
        exact Nat.mul_left_cancel (by decide : 0 < 5) h5
      have hr0 : r = 0 := ih r hrlt s hdesc
      exact absurd hr0 (Nat.ne_of_gt hrpos)

theorem pythagorean345 : (3 : Nat) * 3 + 4 * 4 = 5 * 5 := by
  decide

theorem fiveMulSqEqFourMulSq (a b : Nat) (h : 5 * (a * a) = 4 * (b * b)) : a = 0 ∧ b = 0 := by
  have hb : b = 0 := fiveFourSquareForcesBZero a b h
  refine ⟨?_, hb⟩
  have h5 : 5 * (a * a) = 0 := by simpa [hb] using h
  have hprod : 5 = 0 ∨ a * a = 0 := Nat.mul_eq_zero.mp h5
  cases hprod with
  | inl z => exact absurd z (by decide)
  | inr z =>
    cases Nat.mul_eq_zero.mp z with
    | inl ha => exact ha
    | inr ha => exact ha

end CampaignFqGapStoneContinuousTime

#print axioms CampaignFqGapStoneContinuousTime.pythagorean345
#print axioms CampaignFqGapStoneContinuousTime.fiveMulSqEqFourMulSq
