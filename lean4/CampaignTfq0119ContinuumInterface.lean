import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

/-!
# Campaign Formalization: `TFQ-0119` (`CONTINUUM_INTERFACE`)
## Dyadic Direct-Limit Inclusion vs. Completed Circle and Pontryagin Completion Fences

This module formalizes the exact finite/algebraic counterpart and non-equivalence scope fences for
DAG node `TFQ-0119` (`cdx2.pontryagin_completion_classification stays open. Dyadic direct limit is
not the completed circle`):

1. **Dyadic Direct-System Compatibility & Finite Haar Partition (`dyadicRatVal`)**:
   - Models the rational valuation `dyadicRatVal k m = m / 2^k` of a level-`k` dyadic representative.
   - Proves single-step compatibility `dyadicRatVal (k + 1) (2 * m) = dyadicRatVal k m`
     (`dyadic_direct_limit_step_invariant`), multi-step compatibility
     `dyadicRatVal (k + d) (2^d * m) = dyadicRatVal k m` (`dyadic_direct_limit_multi_step_invariant`),
     and unit total mass of the level-`k` uniform Haar partition
     `2^k * (1 / 2^k) = 1` (`dyadic_haar_uniform_sum_one`).

2. **Dyadic Direct Limit Is Not the Completed Circle (`1/3 ∉ Z[1/2]`)**:
   - Proves by induction on `k` that `(2 ^ k) % 3 ≠ 0` (`two_pow_mod_three_nonzero`), so no power of
     `2` is divisible by `3` (`three_mul_ne_two_pow : 3 * m ≠ 2 ^ k`).
   - Deduces that for every dyadic level `k : Nat` and numerator `m : Nat`, the dyadic fraction
     `dyadicRatVal k m = m / 2^k` never equals the rational 3-torsion circle point `1 / 3`
     (`one_third_not_dyadic_fraction`), establishing constructively that the uncompleted dyadic
     direct limit omits even rational non-dyadic points of the circle.

3. **Uncompleted Dyadic Cauchy Sequence Approximating `1/3` (`cdx2.pontryagin_completion_classification` Fence)**:
   - Proves that `(4 ^ n - 1) % 3 = 0` for all `n : Nat` (`four_pow_sub_one_mod_three_zero`), so
     `a_n = (4^n - 1) / 3` is an exact integer numerator over the dyadic denominator `4^n = 2^(2n)`.
   - Defines `dyadicOneThirdApprox n = (4^n - 1) / (3 * 4^n)` and proves that its residual to `1/3`
     is `1 / (3 * 4^n)`, which contracts by `1 / 4` at each step (`dyadic_cauchy_approx_one_third_residual`),
     remains strictly positive (`dyadicOneThirdApprox n < 1/3`) at every finite stage `n`
     (`dyadic_cauchy_approx_strictly_below_one_third`), and evaluates to `1/4, 5/16, 21/64, 85/256`
     for `n = 1, 2, 3, 4` (`dyadic_cauchy_approx_table`).
-/

namespace CampaignTfq0119ContinuumInterface

-- ============================================================================
-- 1. Dyadic Direct-System Compatibility & Finite Haar Partition
-- ============================================================================

/-- Rational valuation `m / 2^k` of a level-`k` dyadic representative `m`. -/
def dyadicRatVal (k : Nat) (m : ℚ) : ℚ :=
  m / ((2 : ℚ) ^ k)

/-- Theorem 1: Single-step dyadic direct-system transition `(k, m) ↦ (k + 1, 2 * m)` preserves
the rational valuation `dyadicRatVal`. -/
theorem dyadic_direct_limit_step_invariant (k : Nat) (m : ℚ) :
    dyadicRatVal (k + 1) (2 * m) = dyadicRatVal k m := by
  dsimp [dyadicRatVal]
  rw [pow_succ]
  have h2k : (2 : ℚ) ^ k ≠ 0 := by positivity
  field_simp [h2k]

/-- Theorem 2: Multi-step dyadic direct-system transition `(k, m) ↦ (k + d, 2^d * m)` preserves
`dyadicRatVal`. -/
theorem dyadic_direct_limit_multi_step_invariant (k d : Nat) (m : ℚ) :
    dyadicRatVal (k + d) (((2 : ℚ) ^ d) * m) = dyadicRatVal k m := by
  dsimp [dyadicRatVal]
  rw [pow_add]
  have h2k : (2 : ℚ) ^ k ≠ 0 := by positivity
  have h2d : (2 : ℚ) ^ d ≠ 0 := by positivity
  field_simp [h2k, h2d]

/-- Theorem 3: At every finite dyadic level `k : Nat`, summing `2^k` uniform point masses of weight
`1 / 2^k` yields total mass `1`. -/
theorem dyadic_haar_uniform_sum_one (k : Nat) :
    ((2 : ℚ) ^ k) * dyadicRatVal k 1 = 1 := by
  dsimp [dyadicRatVal]
  have h2k : (2 : ℚ) ^ k ≠ 0 := by positivity
  field_simp [h2k]

-- ============================================================================
-- 2. Dyadic Direct Limit Is Not the Completed Circle (`1/3 ∉ Z[1/2]`)
-- ============================================================================

/-- Theorem 4: For every `k : Nat`, `(2 ^ k) % 3` is either `1` or `2`, and is never `0`. -/
theorem two_pow_mod_three_nonzero (k : Nat) :
    ((2 ^ k) % 3 = 1 ∨ (2 ^ k) % 3 = 2) ∧ (2 ^ k) % 3 ≠ 0 := by
  have h12 : (2 ^ k) % 3 = 1 ∨ (2 ^ k) % 3 = 2 := by
    induction k with
    | zero => decide
    | succ n ih =>
      rw [Nat.pow_succ, Nat.mul_mod]
      rcases ih with h1 | h2
      · right; rw [h1]
      · left; rw [h2]
  refine ⟨h12, ?_⟩
  rcases h12 with h1 | h2 <;> omega

/-- Theorem 5: No power of `2` is a multiple of `3`: for all `k m : Nat`, `3 * m ≠ 2 ^ k`. -/
theorem three_mul_ne_two_pow (k m : Nat) :
    3 * m ≠ 2 ^ k := by
  intro h
  have hmod : (3 * m) % 3 = (2 ^ k) % 3 := congrArg (fun x => x % 3) h
  rw [Nat.mul_mod_right] at hmod
  exact (two_pow_mod_three_nonzero k).2 hmod.symm

/-- Theorem 6: The rational 3-torsion point `1 / 3` on the circle `R / Z` is never equal to any
dyadic fraction `m / 2^k` (`k m : Nat`), showing that the dyadic direct limit is a proper subset
of the completed circle. -/
theorem one_third_not_dyadic_fraction (k m : Nat) :
    dyadicRatVal k (m : ℚ) ≠ 1 / 3 := by
  dsimp [dyadicRatVal]
  intro h
  have h2k : (2 : ℚ) ^ k ≠ 0 := by positivity
  have hcross : (3 : ℚ) * (m : ℚ) = (2 : ℚ) ^ k := by
    field_simp [h2k] at h
    linarith
  have hnat : 3 * m = 2 ^ k := by exact_mod_cast hcross
  exact three_mul_ne_two_pow k m hnat

-- ============================================================================
-- 3. Dyadic Cauchy Sequence Approximating `1/3` Without In-Limit Convergence
-- ============================================================================

/-- Theorem 7: For every `n : Nat`, `4^n` is congruent to `1` modulo `3`, so `4^n - 1` is divisible
by `3` (making `(4^n - 1) / 3` an exact integer numerator over the dyadic denominator `4^n = 2^(2n)`). -/
theorem four_pow_sub_one_mod_three_zero (n : Nat) :
    (4 ^ n) % 3 = 1 ∧ (4 ^ n - 1) % 3 = 0 := by
  have h4 : (4 ^ n) % 3 = 1 := by
    induction n with
    | zero => decide
    | succ m ih =>
      rw [Nat.pow_succ, Nat.mul_mod, ih]
  have hge : 1 ≤ 4 ^ n := Nat.one_le_pow n 4 (by decide)
  refine ⟨h4, ?_⟩
  omega

/-- Stage-`n` dyadic rational approximation `((4^n - 1) / 3) / 4^n` to `1 / 3`. -/
def dyadicOneThirdApprox (n : Nat) : ℚ :=
  (((4 : ℚ) ^ n) - 1) / (3 * ((4 : ℚ) ^ n))

/-- Residual `(1 / 3) - dyadicOneThirdApprox n` between `1 / 3` and its stage-`n` dyadic
approximation. -/
def dyadicOneThirdResidual (n : Nat) : ℚ :=
  1 / 3 - dyadicOneThirdApprox n

/-- Theorem 8: The stage-`n` dyadic residual equals `1 / (3 * 4^n)` and contracts by `1 / 4` at
every step `n ↦ n + 1`. -/
theorem dyadic_cauchy_approx_one_third_residual (n : Nat) :
    dyadicOneThirdResidual n = 1 / (3 * ((4 : ℚ) ^ n)) ∧
    dyadicOneThirdResidual (n + 1) = (1 / 4) * dyadicOneThirdResidual n := by
  have h4n : (4 : ℚ) ^ n ≠ 0 := by positivity
  refine ⟨?_, ?_⟩
  · dsimp [dyadicOneThirdResidual, dyadicOneThirdApprox]
    field_simp [h4n]
    ring
  · dsimp [dyadicOneThirdResidual, dyadicOneThirdApprox]
    rw [pow_succ]
    field_simp [h4n]
    ring

/-- Theorem 9: At every finite dyadic stage `n : Nat`, the residual `dyadicOneThirdResidual n` is
strictly positive (`> 0`), so `dyadicOneThirdApprox n < 1 / 3` and `dyadicOneThirdApprox n ≠ 1 / 3`. -/
theorem dyadic_cauchy_approx_strictly_below_one_third (n : Nat) :
    0 < dyadicOneThirdResidual n ∧
    dyadicOneThirdApprox n < 1 / 3 ∧
    dyadicOneThirdApprox n ≠ 1 / 3 := by
  rcases dyadic_cauchy_approx_one_third_residual n with ⟨hres, _⟩
  have hpos : 0 < 1 / (3 * ((4 : ℚ) ^ n)) := by positivity
  rw [hres]
  refine ⟨hpos, ?_, ?_⟩
  · dsimp [dyadicOneThirdResidual] at hres
    linarith
  · dsimp [dyadicOneThirdResidual] at hres
    linarith

/-- Theorem 10: Explicit dyadic approximations for `n ∈ {1, 2, 3, 4}` (`1/4, 5/16, 21/64, 85/256`)
and their residuals (`1/12, 1/48, 1/192, 1/768`). -/
theorem dyadic_cauchy_approx_table :
    dyadicOneThirdApprox 1 = 1 / 4 ∧
    dyadicOneThirdApprox 2 = 5 / 16 ∧
    dyadicOneThirdApprox 3 = 21 / 64 ∧
    dyadicOneThirdApprox 4 = 85 / 256 ∧
    dyadicOneThirdResidual 1 = 1 / 12 ∧
    dyadicOneThirdResidual 2 = 1 / 48 ∧
    dyadicOneThirdResidual 3 = 1 / 192 ∧
    dyadicOneThirdResidual 4 = 1 / 768 := by
  dsimp [dyadicOneThirdApprox, dyadicOneThirdResidual]
  norm_num

end CampaignTfq0119ContinuumInterface

#print axioms CampaignTfq0119ContinuumInterface.dyadic_direct_limit_step_invariant
#print axioms CampaignTfq0119ContinuumInterface.dyadic_direct_limit_multi_step_invariant
#print axioms CampaignTfq0119ContinuumInterface.dyadic_haar_uniform_sum_one
#print axioms CampaignTfq0119ContinuumInterface.two_pow_mod_three_nonzero
#print axioms CampaignTfq0119ContinuumInterface.three_mul_ne_two_pow
#print axioms CampaignTfq0119ContinuumInterface.one_third_not_dyadic_fraction
#print axioms CampaignTfq0119ContinuumInterface.four_pow_sub_one_mod_three_zero
#print axioms CampaignTfq0119ContinuumInterface.dyadic_cauchy_approx_one_third_residual
#print axioms CampaignTfq0119ContinuumInterface.dyadic_cauchy_approx_strictly_below_one_third
#print axioms CampaignTfq0119ContinuumInterface.dyadic_cauchy_approx_table

private def l5aProvenance : String :=
  "Origin: lean4/CampaignTfq0119ContinuumInterface.lean Claim: TFQ-0119 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
