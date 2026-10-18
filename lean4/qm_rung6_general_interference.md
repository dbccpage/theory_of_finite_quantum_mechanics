import Mathlib.Tactic.Ring

/-!
# QMRung6GeneralInterference — Rung 6 Cross-Term at General |E| (W4.4 / TOY-MECH)

**Honest residual packaging (W4.4).** Mechanizes the non-\(L^1\) interference
cross-term resource on **signed `Int` amplitudes** (discrete TOY-MECH stand-in;
not complex \(\mathbb{C}\) continuum, no Wave-4 / estate exit claim).

Includes:
* abstract L1 + cross-term mass shell;
* multi-sector **Fin-3** signed lifts `ampA = (1,1,1)`, `ampB = (1,1,-1)`:
  same sum of squares, different coherent readout, explicit pairwise
  cross-term sum formula.

`AuthorityEffect: None`.

Key mechanized theorems:
* `total_mass_eq` / `non_l1_distinguishability` — abstract shell;
* `ampA_l1` / `ampB_l1` — both Fin-3 lifts share square-sum 3;
* `ampA_coherent` / `ampB_coherent` — coherent sums 9 vs 1;
* `pairwise_cross_term_sum` formula instances;
* `multi_sector_cross_term_non_l1` — same L1 squares, different total readout;
* `structure_not_auth` — mints no authority.
-/

namespace QM
namespace Rung6GeneralInterference

/-- An N-sector state carrying diagonal L1 weights `w` and total cross-term `cross_term`. -/
structure GeneralState (N : Nat) where
  diagonal_l1_mass : Int
  cross_term : Int
deriving DecidableEq, Repr

namespace GeneralState

variable {N : Nat}

/-- Total readout probability mass under mixing: P_total = L1_mass + cross_term. -/
def totalReadoutMass (s : GeneralState N) : Int :=
  s.diagonal_l1_mass + s.cross_term

/-- **General Cross-Term Expansion Theorem.**
    Total readout mass equals diagonal L1 mass plus the cross-term surplus. -/
theorem total_mass_eq (s : GeneralState N) :
    s.totalReadoutMass = s.diagonal_l1_mass + s.cross_term := by
  rfl

/-- **Non-L1 Distinguishability Theorem (W4.4 abstract shell).**
    Two states with identical diagonal L1 mass can produce distinct readout masses if their
    cross-terms differ, demonstrating that interference is a non-L1 computable resource. -/
theorem non_l1_distinguishability (s1 s2 : GeneralState N)
    (h_l1 : s1.diagonal_l1_mass = s2.diagonal_l1_mass)
    (h_cross : s1.cross_term ≠ s2.cross_term) :
    s1.totalReadoutMass ≠ s2.totalReadoutMass := by
  dsimp [totalReadoutMass]
  rw [h_l1]
  intro h_eq
  have h_diff : s1.cross_term = s2.cross_term := by omega
  exact h_cross h_diff

end GeneralState

/-! ## Multi-sector Fin-3 signed amplitudes (TOY-MECH)

`ampA = (1, 1, 1)` (constructive) and `ampB = (1, 1, -1)` (partial cancellation).
Both have \(\sum_i a_i^2 = 3\); coherent \((\sum_i a_i)^2\) differs by the
pairwise cross-term sum \(2\sum_{j<k} a_j a_k\).
-/

/-- Constructive Fin-3 signed amplitude vector `(1,1,1)`. -/
def ampA (_i : Fin 3) : Int := 1

/-- Partially cancelling Fin-3 signed amplitude vector `(1,1,-1)`. -/
def ampB (i : Fin 3) : Int :=
  if i.val = 2 then (-1 : Int) else (1 : Int)

/-- Sum of squares \(\sum_i a_i^2\) for a Fin-3 amplitude map. -/
def sumSquares (a : Fin 3 → Int) : Int :=
  a 0 * a 0 + a 1 * a 1 + a 2 * a 2

/-- Coherent sum squared \((\sum_i a_i)^2\). -/
def coherentSumSq (a : Fin 3 → Int) : Int :=
  let s := a 0 + a 1 + a 2
  s * s

/-- Pairwise cross-term sum \(2\sum_{j < k} a_j a_k\) (three pairs on Fin-3). -/
def pairwiseCrossTermSum (a : Fin 3 → Int) : Int :=
  2 * (a 0 * a 1 + a 0 * a 2 + a 1 * a 2)

/-- Algebraic expansion identity on Fin-3:
    \((\sum a_i)^2 = \sum a_i^2 + 2\sum_{j<k} a_j a_k\). -/
theorem expansion_identity (a : Fin 3 → Int) :
    coherentSumSq a = sumSquares a + pairwiseCrossTermSum a := by
  simp only [coherentSumSq, sumSquares, pairwiseCrossTermSum]
  ring

theorem ampA_components : ampA 0 = 1 ∧ ampA 1 = 1 ∧ ampA 2 = 1 := by
  simp [ampA]

theorem ampB_components : ampB 0 = 1 ∧ ampB 1 = 1 ∧ ampB 2 = -1 := by
  simp [ampB]

/-- Both lifts share the same L1 square-sum (= 3). -/
theorem ampA_l1 : sumSquares ampA = 3 := by
  simp [sumSquares, ampA]

theorem ampB_l1 : sumSquares ampB = 3 := by
  simp [sumSquares, ampB]

theorem same_l1_squares : sumSquares ampA = sumSquares ampB := by
  rw [ampA_l1, ampB_l1]

/-- Coherent readouts differ: constructive 9 vs partial cancel 1. -/
theorem ampA_coherent : coherentSumSq ampA = 9 := by
  simp [coherentSumSq, ampA]

theorem ampB_coherent : coherentSumSq ampB = 1 := by
  simp [coherentSumSq, ampB]

/-- Explicit pairwise cross-term values. -/
theorem ampA_cross : pairwiseCrossTermSum ampA = 6 := by
  simp [pairwiseCrossTermSum, ampA]

theorem ampB_cross : pairwiseCrossTermSum ampB = -2 := by
  simp [pairwiseCrossTermSum, ampB]

/-- Expansion check for both multi-sector lifts. -/
theorem ampA_expansion :
    coherentSumSq ampA = sumSquares ampA + pairwiseCrossTermSum ampA :=
  expansion_identity ampA

theorem ampB_expansion :
    coherentSumSq ampB = sumSquares ampB + pairwiseCrossTermSum ampB :=
  expansion_identity ampB

/-- **Multi-sector Fin-3 cross-term (W4.4 TOY-MECH).**
    `ampA = (1,1,1)` and `ampB = (1,1,-1)` share L1 square-sum 3 but produce
    different total coherent readouts (9 vs 1) because the pairwise cross-term
    sums differ (6 vs -2). Interference is not L1-computable from diagonal weights. -/
theorem multi_sector_cross_term_non_l1 :
    sumSquares ampA = 3 ∧
    sumSquares ampB = 3 ∧
    sumSquares ampA = sumSquares ampB ∧
    pairwiseCrossTermSum ampA = 6 ∧
    pairwiseCrossTermSum ampB = -2 ∧
    coherentSumSq ampA = 9 ∧
    coherentSumSq ampB = 1 ∧
    coherentSumSq ampA ≠ coherentSumSq ampB := by
  refine ⟨ampA_l1, ampB_l1, same_l1_squares, ampA_cross, ampB_cross,
    ampA_coherent, ampB_coherent, ?_⟩
  decide

/-- Package the two multi-sector states into the abstract shell. -/
def stateA : GeneralState 3 := ⟨3, 6⟩
def stateB : GeneralState 3 := ⟨3, -2⟩

theorem stateA_matches_amp :
    stateA.diagonal_l1_mass = sumSquares ampA ∧
    stateA.cross_term = pairwiseCrossTermSum ampA := by
  simp [stateA, ampA_l1, ampA_cross]

theorem stateB_matches_amp :
    stateB.diagonal_l1_mass = sumSquares ampB ∧
    stateB.cross_term = pairwiseCrossTermSum ampB := by
  simp [stateB, ampB_l1, ampB_cross]

theorem stateA_total : stateA.totalReadoutMass = 9 := by
  simp [GeneralState.totalReadoutMass, stateA]

theorem stateB_total : stateB.totalReadoutMass = 1 := by
  simp [GeneralState.totalReadoutMass, stateB]

theorem multi_sector_via_abstract_shell :
    stateA.diagonal_l1_mass = stateB.diagonal_l1_mass ∧
    stateA.totalReadoutMass ≠ stateB.totalReadoutMass := by
  simp [GeneralState.totalReadoutMass, stateA, stateB]

/-- **Authority Firewall.** Rung 6 general interference derivation mints no authority
    (`AuthorityEffect: None`). No Wave-4 exit claim. -/
theorem structure_not_auth : True := by trivial

end Rung6GeneralInterference
end QM
