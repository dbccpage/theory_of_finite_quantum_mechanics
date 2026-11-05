import Mathlib.Analysis.Normed.Group.AddCircle
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Topology.Algebra.Group.CompactOpen

/-!
# A compact-open zero neighborhood on the actual dyadic circle subgroup

We use AddCircle 1 with its quotient norm in turns, not Circle's chordal metric.
The final discreteness statement explicitly assumes the integer classification.
-/

noncomputable section

namespace WitnessedDifference.DyadicCompactOpen

open Topology Filter
open ContinuousMonoidHom

abbrev Turns := AddCircle (1 : ℝ)

def dyadicCircle : AddSubgroup Turns where
  carrier := {x | ∃ n : ℕ, (2 ^ n : ℕ) • x = 0}
  zero_mem' := ⟨0, by simp⟩
  add_mem' := by
    rintro x y ⟨n, hn⟩ ⟨m, hm⟩
    refine ⟨n + m, ?_⟩
    have hx : (2 ^ (n + m) : ℕ) • x = 0 := by
      rw [Nat.add_comm, pow_add, mul_smul, hn, smul_zero]
    have hy : (2 ^ (n + m) : ℕ) • y = 0 := by
      rw [pow_add, mul_smul, hm, smul_zero]
    rw [smul_add, hx, hy, add_zero]
  neg_mem' := by
    rintro x ⟨n, hn⟩
    exact ⟨n, by rw [smul_neg, hn, neg_zero]⟩

theorem mem_dyadicCircle_iff (x : Turns) :
    x ∈ dyadicCircle ↔ ∃ n k : ℕ, k < 2 ^ n ∧
      (((k : ℝ) / (2 : ℝ) ^ n : ℝ) : Turns) = x := by
  change (∃ n : ℕ, (2 ^ n : ℕ) • x = 0) ↔ _
  simp_rw [AddCircle.nsmul_eq_zero_iff (pow_pos (by norm_num : 0 < (2 : ℕ)) _)]
  simp

def dyadicPoint (n : ℕ) : dyadicCircle :=
  ⟨((1 / (2 : ℝ) ^ (n + 1) : ℝ) : Turns), by
    refine ⟨n + 1, ?_⟩
    rw [← AddCircle.coe_nsmul, nsmul_eq_mul]
    norm_num [Nat.cast_pow, mul_one_div_cancel (pow_ne_zero _ (by norm_num : (2 : ℝ) ≠ 0))]⟩

theorem dyadicPoint_tendsto : Tendsto dyadicPoint atTop (nhds 0) := by
  apply tendsto_subtype_rng.mpr
  have h := (tendsto_pow_atTop_nhds_zero_of_lt_one
    (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (1 : ℝ) / 2 < 1)).mul_const (1 / 2)
  have hc := (AddCircle.continuous_mk' (1 : ℝ)).continuousAt.tendsto.comp h
  simpa [dyadicPoint, pow_succ, one_div, inv_pow, mul_comm, Function.comp_def] using hc

def compactTest : Set dyadicCircle := insert 0 (Set.range dyadicPoint)

theorem compactTest_isCompact : IsCompact compactTest :=
  dyadicPoint_tendsto.isCompact_insert_range

abbrev DyadicCharacter := ContinuousAddMonoidHom dyadicCircle Turns

def integerCharacter (j : ℤ) : DyadicCharacter where
  toFun x := j • (x : Turns)
  map_zero' := by simp
  map_add' x y := by simp [smul_add]
  continuous_toFun := continuous_subtype_val.zsmul j

@[simp] theorem integerCharacter_zero : integerCharacter 0 = 0 := by
  apply ContinuousAddMonoidHom.ext
  intro x
  change (0 : ℤ) • (x : Turns) = 0
  exact zero_zsmul _

theorem natural_character_hits_half {j : ℕ} (hj : j ≠ 0) :
    ∃ n : ℕ, dist (integerCharacter j (dyadicPoint n)) 0 = (1 : ℝ) / 2 := by
  obtain ⟨v, m, hm, hfactor⟩ := Nat.exists_eq_two_pow_mul_odd hj
  obtain ⟨k, hk⟩ := hm
  refine ⟨v, ?_⟩
  have hreal : (j : ℝ) * (1 / (2 : ℝ) ^ (v + 1)) = (k : ℝ) + 1 / 2 := by
    rw [hfactor, hk]
    push_cast
    rw [pow_succ]
    field_simp
  rw [dist_zero_right]
  change ‖(j : ℤ) • (((1 / (2 : ℝ) ^ (v + 1)) : ℝ) : Turns)‖ = (1 : ℝ) / 2
  rw [← AddCircle.coe_zsmul, zsmul_eq_mul, Int.cast_natCast, hreal, AddCircle.coe_add]
  have hkzero : (((k : ℝ) : ℝ) : Turns) = 0 := by
    calc
      (((k : ℝ) : ℝ) : Turns) = k • ((1 : ℝ) : Turns) := by
        simpa only [nsmul_eq_mul, mul_one] using
          (AddCircle.coe_nsmul (p := (1 : ℝ)) (n := k) (x := (1 : ℝ)))
      _ = 0 := by rw [AddCircle.coe_period, smul_zero]
  rw [hkzero, zero_add]
  simpa using AddCircle.norm_half_period_eq (1 : ℝ)

theorem integer_character_hits_half {j : ℤ} (hj : j ≠ 0) :
    ∃ n : ℕ, dist (integerCharacter j (dyadicPoint n)) 0 = (1 : ℝ) / 2 := by
  cases j with
  | ofNat m =>
      exact natural_character_hits_half (fun hm => hj (by simp [hm]))
  | negSucc m =>
      obtain ⟨n, hn⟩ := natural_character_hits_half (Nat.succ_ne_zero m)
      refine ⟨n, ?_⟩
      rw [dist_zero_right] at hn ⊢
      change ‖(Int.negSucc m) • ((dyadicPoint n) : Turns)‖ = (1 : ℝ) / 2
      have heq : Int.negSucc m = -((m + 1 : ℕ) : ℤ) := by omega
      rw [heq, neg_smul, norm_neg]
      exact hn

def zeroNeighborhood : Set DyadicCharacter :=
  {χ | Set.MapsTo χ compactTest (Metric.ball 0 (1 / 4))}

theorem zeroNeighborhood_isOpen : IsOpen zeroNeighborhood := by
  exact isOpen_induced (ContinuousMap.isOpen_setOfPred_mapsTo
    compactTest_isCompact Metric.isOpen_ball)

theorem zero_mem_zeroNeighborhood : (0 : DyadicCharacter) ∈ zeroNeighborhood := by
  intro x _
  norm_num

theorem nonzero_integer_not_mem {j : ℤ} (hj : j ≠ 0) :
    integerCharacter j ∉ zeroNeighborhood := by
  intro h
  obtain ⟨n, hn⟩ := integer_character_hits_half hj
  have hm := h (Set.mem_insert_of_mem 0 (Set.mem_range_self n))
  change dist (integerCharacter j (dyadicPoint n)) 0 < (1 : ℝ) / 4 at hm
  rw [hn] at hm
  norm_num at hm

theorem zeroNeighborhood_eq_singleton
    (classification : ∀ χ : DyadicCharacter, ∃ j : ℤ, χ = integerCharacter j) :
    zeroNeighborhood = {0} := by
  ext χ
  constructor
  · intro h
    obtain ⟨j, rfl⟩ := classification χ
    have hj : j = 0 := by
      by_contra hj
      exact nonzero_integer_not_mem hj h
    simp [hj]
  · intro h
    rcases Set.mem_singleton_iff.mp h with rfl
    exact zero_mem_zeroNeighborhood

theorem dual_discrete_of_integer_classification
    (classification : ∀ χ : DyadicCharacter, ∃ j : ℤ, χ = integerCharacter j) :
    DiscreteTopology DyadicCharacter := by
  apply discreteTopology_of_isOpen_singleton_zero
  rw [← zeroNeighborhood_eq_singleton classification]
  exact zeroNeighborhood_isOpen

end WitnessedDifference.DyadicCompactOpen
