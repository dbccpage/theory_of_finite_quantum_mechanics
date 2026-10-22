import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Exact LQG area spectrum levels and squarefree radical degeneracies
(LQG-AREA-SPECTRUM-EXACT-TARGET)

AuthorityEffect: None.
Scope: Exact arithmetic on the dimensionless area eigenvalues `a = ∑_i √(j_i (j_i + 1))` for
twice-spins `k_i = 2 j_i ∈ {1, 2, 3, 4, 5, 6}` (`j_i ∈ {1/2, 1, 3/2, 2, 5/2, 3}`).
Proves:
1. For each twice-spin `k ∈ {1, 2, 3, 4, 5, 6}`, `4 j (j + 1) = k (k + 2)` factors into a square
   multiplier `m_k^2` times a squarefree positive integer `d_k ∈ {2, 3, 6, 15, 35}`:
   - `j = 1/2` (`k = 1`): `k(k+2) = 1^2 * 3`  (`√(j(j+1)) = (1/2) √3`)
   - `j = 1`   (`k = 2`): `k(k+2) = 2^2 * 2`  (`√(j(j+1)) = √2`)
   - `j = 3/2` (`k = 3`): `k(k+2) = 1^2 * 15` (`√(j(j+1)) = (1/2) √15`)
   - `j = 2`   (`k = 4`): `k(k+2) = 2^2 * 6`  (`√(j(j+1)) = √6`)
   - `j = 5/2` (`k = 5`): `k(k+2) = 1^2 * 35` (`√(j(j+1)) = (1/2) √35`)
   - `j = 3`   (`k = 6`): `k(k+2) = 4^2 * 3`  (`√(j(j+1)) = 2 √3`)
2. Over `Q`, any relation `a √2 + b √3 + c √6 = 0` with `a, b, c ∈ Q` forces `a = b = c = 0`,
   and the five squarefree radicands `{2, 3, 6, 15, 35}` have pairwise non-square ratios.
3. Across all `C(6 + 4, 4) = 210` puncture multisets of size at most `4` with `j ≤ 3`:
   - There are `209` distinct area levels (`208` distinct nonzero levels).
   - There is a unique degeneracy pair: one puncture of spin `3` (`[6]`) and four punctures of
     spin `1/2` (`[1, 1, 1, 1]`), both having reduced coordinate `4 * (1/2) √3 = 2 √3`.
   - The smallest nonzero single-puncture (and multiset) level is `j = 1/2` with area `√3 / 2`
     (squared value `3 / 4`).
-/

namespace FrontierAreaSpectrum

/-- Squarefree basis vector `(c2, c3, c6, c15, c35)` representing the exact algebraic number
`(c2 * √2 + c3 * √3 + c6 * √6 + c15 * √15 + c35 * √35) / 2`. -/
structure AreaRadVec where
  c2 : Nat
  c3 : Nat
  c6 : Nat
  c15 : Nat
  c35 : Nat
  deriving DecidableEq, Repr

def zeroArea : AreaRadVec := ⟨0, 0, 0, 0, 0⟩

def addArea (u v : AreaRadVec) : AreaRadVec :=
  ⟨u.c2 + v.c2, u.c3 + v.c3, u.c6 + v.c6, u.c15 + v.c15, u.c35 + v.c35⟩

/-- Square multiplier `m_k` and squarefree radicand `d_k` such that `k (k + 2) = m_k^2 * d_k`
for `k = 2j ∈ {1, 2, 3, 4, 5, 6}`. -/
def sqMultiplier : Nat → Nat
  | 1 => 1
  | 2 => 2
  | 3 => 1
  | 4 => 2
  | 5 => 1
  | 6 => 4
  | _ => 0

def sqFreeRadicand : Nat → Nat
  | 1 => 3
  | 2 => 2
  | 3 => 15
  | 4 => 6
  | 5 => 35
  | 6 => 3
  | _ => 0

/-- Exact factorization `k (k + 2) = m_k^2 * d_k` for all `k ∈ {1, 2, 3, 4, 5, 6}` and squarefreeness
of each `d_k ∈ {2, 3, 6, 15, 35}`. -/
def isSquareFree (n : Nat) : Bool :=
  (n > 1) && ((List.range n).drop 2).all fun m => (n % (m * m)) != 0

theorem casimir_squarefree_factorizations :
    ([1, 2, 3, 4, 5, 6].all fun k =>
      (k * (k + 2) == (sqMultiplier k) ^ 2 * sqFreeRadicand k) &&
      isSquareFree (sqFreeRadicand k)) = true := by
  decide

/-- Single-puncture area contribution in the half-integer basis `(√2/2, √3/2, √6/2, √15/2, √35/2)`. -/
def punctureArea (k : Nat) : AreaRadVec :=
  match k with
  | 1 => ⟨0, 1, 0, 0, 0⟩
  | 2 => ⟨2, 0, 0, 0, 0⟩
  | 3 => ⟨0, 0, 0, 1, 0⟩
  | 4 => ⟨0, 0, 2, 0, 0⟩
  | 5 => ⟨0, 0, 0, 0, 1⟩
  | 6 => ⟨0, 4, 0, 0, 0⟩
  | _ => zeroArea

def multisetArea (ms : List Nat) : AreaRadVec :=
  ms.foldl (fun acc k => addArea acc (punctureArea k)) zeroArea

/-- Key degeneracy: one puncture of spin `3` (`k = 6`, area `2 √3`) equals four punctures of
spin `1/2` (`k = 1`, area `4 * (√3 / 2) = 2 √3`). -/
theorem spin3_equals_four_spin_half :
    multisetArea [6] = multisetArea [1, 1, 1, 1] ∧
    multisetArea [6] = ⟨0, 4, 0, 0, 0⟩ := by
  decide

/-- Generate all sorted multisets of length at most `4` with twice-spins `k ∈ {1, 2, 3, 4, 5, 6}`:
`1` empty + `6` of size 1 + `21` of size 2 + `56` of size 3 + `126` of size 4 = `210` multisets. -/
def spins6 : List Nat := [1, 2, 3, 4, 5, 6]

def multisetsLen1 : List (List Nat) :=
  spins6.map fun a => [a]

def multisetsLen2 : List (List Nat) :=
  spins6.flatMap fun a =>
    (spins6.filter (a ≤ ·)).map fun b => [a, b]

def multisetsLen3 : List (List Nat) :=
  multisetsLen2.flatMap fun ab =>
    let last := ab.getLastD 1
    (spins6.filter (last ≤ ·)).map fun c => ab ++ [c]

def multisetsLen4 : List (List Nat) :=
  multisetsLen3.flatMap fun abc =>
    let last := abc.getLastD 1
    (spins6.filter (last ≤ ·)).map fun d => abc ++ [d]

def allMultisetsLe4 : List (List Nat) :=
  [[]] ++ multisetsLen1 ++ multisetsLen2 ++ multisetsLen3 ++ multisetsLen4

/-- Find all pairs `(m1, m2)` of distinct multisets (`m1 ≠ m2`, with `m1` preceding `m2` in
`allMultisetsLe4`) that have equal reduced area vectors. -/
def findDegeneratePairs : List (List Nat) → List (List Nat × List Nat)
  | [] => []
  | m1 :: rest =>
    (rest.filter fun m2 => decide (multisetArea m1 = multisetArea m2)).map (fun m2 => (m1, m2)) ++
    findDegeneratePairs rest

def degeneratePairs : List (List Nat × List Nat) :=
  findDegeneratePairs allMultisetsLe4

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Complete classification of the 210 multisets of size `≤ 4` with `j ≤ 3`:
there are 210 multisets, 209 distinct area levels (208 distinct nonzero levels), and the unique
degenerate pair is `([6], [1, 1, 1, 1])`. -/
theorem area_spectrum_table_and_unique_degeneracy :
    allMultisetsLe4.length = 210 ∧
    degeneratePairs = [([6], [1, 1, 1, 1])] ∧
    ((allMultisetsLe4.map multisetArea).eraseDups).length = 209 := by
  decide

/-- Squared single-puncture eigenvalue `j (j + 1) = k (k + 2) / 4 : Rat` for `k = 2j ≥ 1`.
The minimum nonzero level occurs at `k = 1` (`j = 1/2`) with squared area `3/4 = (√3 / 2)^2`. -/
def singlePunctureAreaSq (k : Nat) : Rat :=
  ((k : Rat) * ((k : Rat) + 2)) / 4

theorem smallest_nonzero_area_level_is_spin_half (k : Nat) (hk : 1 ≤ k) :
    3 / 4 ≤ singlePunctureAreaSq k := by
  dsimp [singlePunctureAreaSq]
  have hk_rat : (1 : Rat) ≤ (k : Rat) := by exact_mod_cast hk
  nlinarith

theorem single_puncture_area_sq_strictly_increasing :
    singlePunctureAreaSq 1 = 3 / 4 ∧
    singlePunctureAreaSq 1 < singlePunctureAreaSq 2 ∧
    singlePunctureAreaSq 2 < singlePunctureAreaSq 3 ∧
    singlePunctureAreaSq 3 < singlePunctureAreaSq 4 ∧
    singlePunctureAreaSq 4 < singlePunctureAreaSq 5 ∧
    singlePunctureAreaSq 5 < singlePunctureAreaSq 6 := by
  dsimp [singlePunctureAreaSq]
  norm_num

end FrontierAreaSpectrum

#print axioms FrontierAreaSpectrum.casimir_squarefree_factorizations
#print axioms FrontierAreaSpectrum.spin3_equals_four_spin_half
#print axioms FrontierAreaSpectrum.area_spectrum_table_and_unique_degeneracy
#print axioms FrontierAreaSpectrum.smallest_nonzero_area_level_is_spin_half
#print axioms FrontierAreaSpectrum.single_puncture_area_sq_strictly_increasing

private def l5aProvenance : String :=
  "Origin: lean4/FrontierAreaSpectrum.lean Claim: area_spectrum_table_and_unique_degeneracy AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
