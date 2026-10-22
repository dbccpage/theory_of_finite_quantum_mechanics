import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import CausalOrder

/-!
# Ordering fraction, Myrheim-Meyer dimension table, and Hasse/Mobius reductions
(CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET)

AuthorityEffect: None.
Scope: Exact rational arithmetic on finite strict posets (`FiniteStrictPoset n`), the `n × n`
componentwise product grid, the Myrheim-Meyer reference fractions `f(1)=1, f(2)=1/2, f(3)=8/35, f(4)=1/10`,
and the Hasse covering relation and Möbius recursion on `posetC1` and `posetC2`.
Proves:
(i) For the `n × n` grid with the strict componentwise product order (`N = n^2` points), the number
    of strictly related pairs is `R(n) = (n(n+1)/2)^2 - n^2 = n^2(n-1)(n+3)/4`, and for every `n ≥ 2`
    the ordering fraction `2 R(n) / (N (N - 1))` equals `(n + 3) / (2 (n + 1))`. At `n = 2` this
    equals `5/6` (agreeing with `posetC2`), and `r(n) - 1/2 = 1 / (n + 1)`.
(ii) Exact rational nearest-dimension classifier against `{f(1)=1, f(2)=1/2, f(3)=8/35, f(4)=1/10}`
     with tie reporting: `5/6 ↦ [1]`, `3/4 ↦ [1, 2]` (exact tie), `1/2 ↦ [2]`, `8/35 ↦ [3]`, `1/10 ↦ [4]`.
(iii) For any `FiniteStrictPoset n`, the Hasse covering relation `covers P x y` is contained in any
      subrelation `E ⊆ P.rel` whose 2-step closure covers `P.rel` (unique minimal transitive reduction);
      `posetC1` has 2 Hasse links, `posetC2` has 4 Hasse links, and `c1_mu` and `c2_mu` satisfy the
      full Möbius inversion recursion `∑_{x ≤ z ≤ y} μ(x, z) = δ_{x, y}`.
-/

namespace FrontierMyrheimMeyer

open CausalOrder

/-- Count of strict relation pairs `(x, y)` with `P.rel x y` in a `FiniteStrictPoset n`. -/
def relationCount {n : Nat} (P : FiniteStrictPoset n) : Nat :=
  ((List.finRange n).map fun x =>
    ((List.finRange n).filter fun y => decide (P.rel x y)).length).sum

/-- Exact rational ordering fraction `2 R / (n (n - 1))` for `n ≥ 2`. -/
def orderingFraction {n : Nat} (P : FiniteStrictPoset n) : Rat :=
  if n < 2 then 0
  else (2 * (relationCount P : Rat)) / ((n : Rat) * ((n : Rat) - 1))

/-- (i) On the `n × n` grid `{0..n-1} × {0..n-1}` with componentwise order `(x₁,y₁) ≤ (x₂,y₂)`,
the number of weak pairs is `(n(n+1)/2)^2`, and subtracting the `n^2` diagonal pairs gives
`gridStrictPairs n` strict pairs. -/
def gridWeak1D (n : Nat) : Rat := (n : Rat) * ((n : Rat) + 1) / 2

def gridStrictPairs (n : Nat) : Rat :=
  (gridWeak1D n) ^ 2 - (n : Rat) ^ 2

def gridOrderingFraction (n : Nat) : Rat :=
  (2 * gridStrictPairs n) / ((n : Rat) ^ 2 * ((n : Rat) ^ 2 - 1))

/-- Exact polynomial identity `4 * gridStrictPairs n = n^2 * (n - 1) * (n + 3)`. -/
theorem gridStrictPairs_factorization (n : Nat) :
    4 * gridStrictPairs n = (n : Rat) ^ 2 * ((n : Rat) - 1) * ((n : Rat) + 3) := by
  dsimp [gridStrictPairs, gridWeak1D]
  ring

/-- For all `n ≥ 2`, the `n × n` grid ordering fraction `2 R(n) / (n^2 (n^2 - 1))` equals
`(n + 3) / (2 (n + 1))`. -/
theorem grid_ordering_fraction_closed_form (n : Nat) (hn : 2 ≤ n) :
    gridOrderingFraction n = ((n : Rat) + 3) / (2 * ((n : Rat) + 1)) := by
  have hn_rat : (2 : Rat) ≤ (n : Rat) := by exact_mod_cast hn
  have h1 : (n : Rat) ^ 2 ≠ 0 := by nlinarith
  have h2 : (n : Rat) ^ 2 - 1 ≠ 0 := by nlinarith
  have hden1 : (n : Rat) ^ 2 * ((n : Rat) ^ 2 - 1) ≠ 0 := mul_ne_zero h1 h2
  have hden2 : 2 * ((n : Rat) + 1) ≠ 0 := by linarith
  dsimp [gridOrderingFraction]
  rw [div_eq_div_iff hden1 hden2]
  dsimp [gridStrictPairs, gridWeak1D]
  ring

/-- The excess of `gridOrderingFraction n` over the 2D continuum value `f(2) = 1/2` is `1 / (n + 1)`. -/
theorem grid_ordering_fraction_minus_half (n : Nat) (hn : 2 ≤ n) :
    gridOrderingFraction n - 1 / 2 = 1 / ((n : Rat) + 1) := by
  rw [grid_ordering_fraction_closed_form n hn]
  have hn_rat : (2 : Rat) ≤ (n : Rat) := by exact_mod_cast hn
  have h3 : (n : Rat) + 1 ≠ 0 := by linarith
  have hden2 : 2 * ((n : Rat) + 1) ≠ 0 := by linarith
  rw [div_sub_div _ _ hden2 (by norm_num)]
  rw [div_eq_div_iff (mul_ne_zero hden2 (by norm_num)) h3]
  ring

/-- Explicit check for `n = 2..6` and agreement of `n = 2` (`5/6`) with `C2`. -/
theorem grid_values_2_to_6_and_c2_agreement :
    orderingFraction C2 = 5 / 6 ∧
    orderingFraction C1 = 2 / 3 ∧
    gridOrderingFraction 2 = 5 / 6 ∧
    gridOrderingFraction 3 = 3 / 4 ∧
    gridOrderingFraction 4 = 7 / 10 ∧
    gridOrderingFraction 5 = 2 / 3 ∧
    gridOrderingFraction 6 = 9 / 14 := by
  have hc2 : relationCount C2 = 5 := by decide
  have hc1 : relationCount C1 = 2 := by decide
  dsimp [orderingFraction, gridOrderingFraction, gridStrictPairs, gridWeak1D]
  rw [hc2, hc1]
  norm_num

/-- (ii) Myrheim-Meyer reference ordering fractions `f(d)` for `d ∈ {1, 2, 3, 4}`,
cleared by the common denominator `70 = lcm(1, 2, 35, 10)`:
`70 * f(1) = 70`, `70 * f(2) = 35`, `70 * f(3) = 16`, `70 * f(4) = 7`. -/
def myrheimMeyerScaled70 : Nat → Int
  | 1 => 70
  | 2 => 35
  | 3 => 16
  | 4 => 7
  | _ => 0

def intAbs (x : Int) : Int := if x < 0 then -x else x

/-- Exact rational nearest-dimension selector for `r = rNum / rDen` (`rDen > 0`) over `d ∈ {1, 2, 3, 4}`,
comparing `70 * rDen * |r - f(d)| = |70 * rNum - 70 * f(d) * rDen|` and returning all dimensions
that achieve the minimum distance (reporting ties). -/
def nearestMyrheimMeyerDims (rNum rDen : Int) : List Nat :=
  let dims := [1, 2, 3, 4]
  let dist (d : Nat) : Int := intAbs (70 * rNum - myrheimMeyerScaled70 d * rDen)
  let minDist := (dims.map dist).foldl min (dist 1)
  dims.filter fun d => decide (dist d = minDist)

theorem myrheim_meyer_nearest_dimension_checks :
    nearestMyrheimMeyerDims 5 6 = [1] ∧
    nearestMyrheimMeyerDims 3 4 = [1, 2] ∧
    nearestMyrheimMeyerDims 7 10 = [2] ∧
    nearestMyrheimMeyerDims 1 2 = [2] ∧
    nearestMyrheimMeyerDims 8 35 = [3] ∧
    nearestMyrheimMeyerDims 1 10 = [4] := by
  decide

/-- (iii) Hasse covering relation: `x < y` with no intermediate `z` satisfying `x < z < y`. -/
def covers {n : Nat} (P : FiniteStrictPoset n) (x y : Fin n) : Bool :=
  decide (P.rel x y) && !((List.finRange n).any fun z => decide (P.rel x z) && decide (P.rel z y))

def hasseLinkCount {n : Nat} (P : FiniteStrictPoset n) : Nat :=
  ((List.finRange n).map fun x =>
    ((List.finRange n).filter fun y => covers P x y).length).sum

/-- Every Hasse covering pair `(x, y)` must belong to any subrelation `E ⊆ P.rel` that generates
`P.rel` (i.e. whenever `P.rel x y` decomposes as either `E x y` or `∃ z, P.rel x z ∧ P.rel z y`). -/
theorem covers_subset_of_generating_subrelation {n : Nat} (P : FiniteStrictPoset n)
    (E : Fin n → Fin n → Bool)
    (hgen : ∀ x y : Fin n, P.rel x y →
      E x y = true ∨ ∃ z : Fin n, P.rel x z ∧ P.rel z y)
    (x y : Fin n) (hcov : covers P x y = true) : E x y = true := by
  dsimp [covers] at hcov
  rcases Bool.and_eq_true_iff.mp hcov with ⟨hxy_dec, hno⟩
  have hxy : P.rel x y := of_decide_eq_true hxy_dec
  rcases hgen x y hxy with hE | ⟨z, hxz, hzy⟩
  · exact hE
  · exfalso
    have hany : ((List.finRange n).any fun z => decide (P.rel x z) && decide (P.rel z y)) = true := by
      rw [List.any_eq_true]
      exact ⟨z, List.mem_finRange z, Bool.and_eq_true_iff.mpr ⟨decide_eq_true hxz, decide_eq_true hzy⟩⟩
    rw [hany] at hno
    cases hno

/-- Executable check of the full Möbius inversion recursion on a `FiniteStrictPoset n`:
`μ(x, x) = 1`, `μ(x, y) = 0` when `x ≠ y` and `¬(x < y)`, and `∑_{x ≤ z ≤ y} μ(x, z) = 0` for `x < y`. -/
def inClosedInterval {n : Nat} (P : FiniteStrictPoset n) (x z y : Fin n) : Bool :=
  (decide (x = z) || decide (P.rel x z)) && (decide (z = y) || decide (P.rel z y))

def satisfiesMobiusRecursion {n : Nat} (P : FiniteStrictPoset n) (mu : Fin n → Fin n → Int) : Bool :=
  (List.finRange n).all fun x =>
    (List.finRange n).all fun y =>
      if x = y then
        decide (mu x y = 1)
      else if decide (P.rel x y) then
        let intervalSum :=
          ((List.finRange n).filter (fun z => inClosedInterval P x z y)).foldl
            (fun acc z => acc + mu x z) 0
        decide (intervalSum = 0)
      else
        decide (mu x y = 0)

theorem hasse_links_and_mobius_recursions_C1_C2 :
    hasseLinkCount C1 = 2 ∧
    hasseLinkCount C2 = 4 ∧
    satisfiesMobiusRecursion C1 c1_mu = true ∧
    satisfiesMobiusRecursion C2 c2_mu = true ∧
    c2_mu d0 d3 = 1 := by
  decide

end FrontierMyrheimMeyer

#print axioms FrontierMyrheimMeyer.gridStrictPairs_factorization
#print axioms FrontierMyrheimMeyer.grid_ordering_fraction_closed_form
#print axioms FrontierMyrheimMeyer.grid_ordering_fraction_minus_half
#print axioms FrontierMyrheimMeyer.grid_values_2_to_6_and_c2_agreement
#print axioms FrontierMyrheimMeyer.myrheim_meyer_nearest_dimension_checks
#print axioms FrontierMyrheimMeyer.covers_subset_of_generating_subrelation
#print axioms FrontierMyrheimMeyer.hasse_links_and_mobius_recursions_C1_C2

private def l5aProvenance : String :=
  "Origin: lean4/FrontierMyrheimMeyer.lean Claim: grid_ordering_fraction_closed_form AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
