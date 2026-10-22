import FrontierClassical6j

/-!
# Ponzano-Regge allowed/forbidden region classification by the Cayley-Menger determinant
(LQG-PR-ALLOWED-REGION-TARGET)

AuthorityEffect: None.
Scope: Exact Cayley-Menger determinant classification of all admissible 6-tuples `(a, b, c, d, e, f)`
with twice-spins at most `8` (`j_e ∈ {0, 1/2, 1, ..., 4}`) and Ponzano-Regge shifted edge lengths
`l_e = j_e + 1/2 = (2 j_e + 1) / 2`, together with the exact rational squared 6j symbol `{a b c; d e f}^2`.
Proves:
1. For shifted half-integer edge lengths `l_e = (A_e + 1) / 2` (`L_e = 2 l_e = A_e + 1` odd),
   `64 * (288 V^2)` equals the exact integer Gram-Cayley-Menger determinant `cayleyMengerScaled64`,
   which is congruent to `4 (mod 8)` for all integers `A_a, ..., A_f`, so `V^2 = 0` never occurs
   for any Ponzano-Regge shifted spin tuple.
2. Across all `13,691` admissible 6-tuples with twice-spins `≤ 8`:
   - `10,884` tuples have `V^2 > 0` (the Euclidean tetrahedron allowed region);
   - `2,807` tuples have `V^2 < 0` (the Euclidean forbidden / Lorentzian region);
   - `0` tuples have `V^2 = 0`.
3. Explicit allowed (`V^2 > 0`) and forbidden (`V^2 < 0`) benchmark witnesses with their exact
   rational squared 6j values `{a b c; d e f}^2`.
-/

namespace FrontierPrAllowedRegion

open FrontierClassical6j

/-- With twice-spins `A, B, C, D, E, F` and doubled Ponzano-Regge lengths `L_x = 2 (j_x + 1/2) = A_x + 1`,
`64 * (288 V^2)` equals the `3 × 3` doubled Gram determinant `det(2 G)` at vertex `0` where edges
`(a, b, f)` meet at vertex `0` and `(d, e, c)` are opposite to `(a, b, f)` respectively. -/
def cayleyMengerScaled64 (a b c d e f : Nat) : Int :=
  let a2 : Int := (a + 1 : Int) ^ 2
  let b2 : Int := (b + 1 : Int) ^ 2
  let c2 : Int := (c + 1 : Int) ^ 2
  let d2 : Int := (d + 1 : Int) ^ 2
  let e2 : Int := (e + 1 : Int) ^ 2
  let f2 : Int := (f + 1 : Int) ^ 2
  let g11 := 2 * a2
  let g22 := 2 * b2
  let g33 := 2 * f2
  let g12 := a2 + b2 - c2
  let g13 := a2 + f2 - e2
  let g23 := b2 + f2 - d2
  g11 * (g22 * g33 - g23 * g23) -
  g12 * (g12 * g33 - g13 * g23) +
  g13 * (g12 * g23 - g22 * g13)

/-- Exact rational value of `288 V^2` for `l_x = j_x + 1/2`. -/
def volumeSq288Rat (a b c d e f : Nat) : Frac :=
  ⟨cayleyMengerScaled64 a b c d e f, 64⟩

/-- All `13,691` admissible 6-tuples with twice-spins `≤ 8`, partitioned by the sign of `288 V^2`. -/
def allAdmissibleLe8 : List (Nat × Nat × Nat × Nat × Nat × Nat) :=
  admissible6Tuples 8

def countAllowedLe8 : Nat :=
  (allAdmissibleLe8.filter fun (a, b, c, d, e, f) =>
    decide (0 < cayleyMengerScaled64 a b c d e f)).length

def countForbiddenLe8 : Nat :=
  (allAdmissibleLe8.filter fun (a, b, c, d, e, f) =>
    decide (cayleyMengerScaled64 a b c d e f < 0)).length

def countFlatLe8 : Nat :=
  (allAdmissibleLe8.filter fun (a, b, c, d, e, f) =>
    decide (cayleyMengerScaled64 a b c d e f = 0)).length

set_option maxRecDepth 60000 in
set_option maxHeartbeats 4000000 in
/-- Complete Cayley-Menger classification of the `13,691` admissible 6-tuples with twice-spins `≤ 8`:
`10,884` lie in the Euclidean allowed region (`V^2 > 0`), `2,807` lie in the forbidden region (`V^2 < 0`),
and `0` have `V^2 = 0`. -/
theorem ponzano_regge_allowed_forbidden_classification_le8 :
    allAdmissibleLe8.length = 13691 ∧
    countAllowedLe8 = 10884 ∧
    countForbiddenLe8 = 2807 ∧
    countFlatLe8 = 0 ∧
    countAllowedLe8 + countForbiddenLe8 = allAdmissibleLe8.length := by
  decide

/-- Explicit allowed (`V^2 > 0`) and forbidden (`V^2 < 0`) witnesses with their exact rational
`288 V^2` and squared 6j values `{a b c; d e f}^2`:
- Regular spin-1 tetrahedron `(2,2,2,2,2,2)` (`l = 3/2`): `288 V^2 = 729/16 > 0` (allowed), `{1 1 1; 1 1 1}^2 = 1/36`.
- Spin-(1/2, 1/2, 1) tetrahedron `(1,1,2,1,1,2)`: `288 V^2 = -81/16 < 0` (forbidden), `{1/2 1/2 1; 1/2 1/2 1}^2 = 1/36`.
- Stretched spin-(1, 1, 2) configuration `(2,2,4,2,2,4)`: `288 V^2 = -4375/16 < 0` (forbidden), `{1 1 2; 1 1 2}^2 = 1/900`. -/
theorem allowed_and_forbidden_witnesses_with_6j_squares :
    Frac.eqv (volumeSq288Rat 2 2 2 2 2 2) ⟨729, 16⟩ = true ∧
    Frac.eqv (sixJSquaredRat 2 2 2 2 2 2) ⟨1, 36⟩ = true ∧
    Frac.eqv (volumeSq288Rat 1 1 2 1 1 2) ⟨-81, 16⟩ = true ∧
    Frac.eqv (sixJSquaredRat 1 1 2 1 1 2) ⟨1, 36⟩ = true ∧
    Frac.eqv (volumeSq288Rat 2 2 4 2 2 4) ⟨-4375, 16⟩ = true ∧
    Frac.eqv (sixJSquaredRat 2 2 4 2 2 4) ⟨1, 900⟩ = true := by
  decide

end FrontierPrAllowedRegion

#print axioms FrontierPrAllowedRegion.ponzano_regge_allowed_forbidden_classification_le8
#print axioms FrontierPrAllowedRegion.allowed_and_forbidden_witnesses_with_6j_squares

private def l5aProvenance : String :=
  "Origin: lean4/FrontierPrAllowedRegion.lean Claim: ponzano_regge_allowed_forbidden_classification_le8 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
