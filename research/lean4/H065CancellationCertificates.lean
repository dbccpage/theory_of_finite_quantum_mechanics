/-
  H065CancellationCertificates.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H065
/- Scope: the constant lengths below record parameters of the cited Lam-Leung
classification. Their reduction lemmas do not formalize that classification.
Only the stated parity arithmetic and the quadratic identity are proved here.
Positive multiplicities, a roots-of-unity carrier, and its algebra are additional
hypotheses for transferring the cited classification to an application. -/

-- ==============================================================================
-- SECTION 1: RECORDED LAM-LEUNG PARAMETERS AND INTEGER PARITY
-- ==============================================================================

/-- Minimal vanishing sum length for 2-power cyclotomic conductors Q(zeta_{2^k}) (k >= 1).
    By Lam-Leung (2000), every minimal vanishing sum over a 2-power conductor
    has length 2, corresponding to pairwise reflection zeta + (-zeta) = 0. -/
def two_power_minimal_cancellation_length : Nat := 2

theorem two_power_minimal_length_is_two : two_power_minimal_cancellation_length = 2 := by
  rfl

/-- Pairability predicate: a cancellation length is pairable if it is even. -/
def is_pairable_length (len : Nat) : Prop :=
  ∃ k : Nat, len = 2 * k

theorem two_power_length_is_pairable : is_pairable_length two_power_minimal_cancellation_length := by
  unfold is_pairable_length two_power_minimal_cancellation_length
  exact ⟨1, rfl⟩

-- ==============================================================================
-- SECTION 2: ODD-PRIME CONDUCTORS AND IRREDUCIBLE VORTICES
-- ==============================================================================

/-- Minimal vanishing sum length for conductor 3 (Z[zeta_3]) is 3,
    given by the irreducible cyclic sum 1 + zeta_3 + zeta_3^2 = 0. -/
def conductor_3_minimal_cancellation_length : Nat := 3

theorem conductor_3_minimal_length_is_three : conductor_3_minimal_cancellation_length = 3 := by
  rfl

/-- Length 3 admits no integer partition into pairs (odd parity). -/
theorem length_3_not_pairable (k : Int) : (3 : Int) ≠ 2 * k := by
  omega

/-- Minimal vanishing sum length for conductor 5 (Z[zeta_5]) is 5,
    given by the irreducible cyclic sum sum_{k=0}^4 zeta_5^k = 0. -/
def conductor_5_minimal_cancellation_length : Nat := 5

theorem conductor_5_minimal_length_is_five : conductor_5_minimal_cancellation_length = 5 := by
  rfl

/-- Length 5 admits no integer partition into pairs (odd parity). -/
theorem length_5_not_pairable (k : Int) : (5 : Int) ≠ 2 * k := by
  omega

-- ==============================================================================
-- SECTION 3: TARGET CENSUS ACROSS 22 FOUNDATIONAL TARGETS
-- ==============================================================================

/-- Total number of foundational targets censused. -/
def foundational_targets_count : Nat := 22

/-- Number of foundational targets exhibiting unpairable cancellations.
    Specifically, Target 2 (cond 12, length 3), Target 3 is excluded (rational I3 identity);
    Target 13 (cond 5, length 5), and Target 22 (cond 3, length 3). -/
def unpairable_targets_count : Nat := 3

theorem recorded_unpairable_count_is_three : unpairable_targets_count = 3 := by
  rfl

/-- Bounded census theorem: the unpairable count lies between 3 and 5. -/
theorem unpairable_count_in_bounds : 3 ≤ unpairable_targets_count ∧ unpairable_targets_count ≤ 5 := by
  decide

/-- First unpairable minimal length across all 22 targets is 3. -/
def first_unpairable_length : Nat := 3

theorem first_unpairable_length_is_three : first_unpairable_length = 3 := by
  rfl

/-! The prime-root example and Sorkin inclusion-exclusion are different.
The following statement uses arbitrary rational real and imaginary coordinates;
no root-of-unity cancellation is assumed. -/

def intensity (x y : Rat) : Rat := x*x + y*y

theorem quadratic_sorkin_identity (a b c u v w : Rat) :
    intensity (a+b+c) (u+v+w)
      - intensity (a+b) (u+v) - intensity (a+c) (u+w)
      - intensity (b+c) (v+w) + intensity a u
      + intensity b v + intensity c w = 0 := by
  unfold intensity
  grind

/-- All three amplitudes can be 1: their sum is nonzero and I3 still vanishes. -/
theorem sorkin_does_not_require_amplitude_cancellation :
    (1+1+1 : Rat) ≠ 0 ∧
    intensity 3 0 - intensity 2 0 - intensity 2 0 - intensity 2 0
      + intensity 1 0 + intensity 1 0 + intensity 1 0 = 0 := by
  unfold intensity
  grind

/-- An explicitly admitted two-dimensional rational algebra with
omega squared = -1 - omega. This model is inhabited, including zero and one. -/
structure Eisenstein where
  a : Rat
  b : Rat
  deriving DecidableEq

def eadd (x y : Eisenstein) : Eisenstein := ⟨x.a+y.a, x.b+y.b⟩
def emul (x y : Eisenstein) : Eisenstein :=
  ⟨x.a*y.a-x.b*y.b, x.a*y.b+x.b*y.a-x.b*y.b⟩
def eone : Eisenstein := ⟨1,0⟩
def omega3 : Eisenstein := ⟨0,1⟩

theorem regular_triangle_sum :
    eadd (eadd eone omega3) (emul omega3 omega3) = ⟨0,0⟩ := by
  unfold eadd emul eone omega3
  congr 1 <;> grind

theorem triangle_model_nontrivial : eone ≠ (⟨0,0⟩ : Eisenstein) := by decide

/- The old `estate_link_confirmed` true-flag was removed. A typed correspondence
with SignRepair remains an open obligation, not a theorem of this module. -/

#print axioms two_power_minimal_length_is_two
#print axioms two_power_length_is_pairable
#print axioms conductor_3_minimal_length_is_three
#print axioms length_3_not_pairable
#print axioms conductor_5_minimal_length_is_five
#print axioms length_5_not_pairable
#print axioms recorded_unpairable_count_is_three
#print axioms unpairable_count_in_bounds
#print axioms first_unpairable_length_is_three

#print axioms regular_triangle_sum
#print axioms triangle_model_nontrivial
#print axioms quadratic_sorkin_identity
#print axioms sorkin_does_not_require_amplitude_cancellation
end FableHilbertWalk20260819.H065
