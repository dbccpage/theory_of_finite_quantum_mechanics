/-!
# Exact rational representation examples and a feedforward lookup table

AuthorityEffect: None. GenesisEffect: None.
This file calculates two squared norms and checks declared rational constants.
RatVal is an unreduced numerator/positive-denominator representation; structural
Lean equality differs from the cross-multiplication predicate RatVal.eq.
No state-transfer protocol, distillation map, entanglement witness calculation,
anyon matrices, or categorical coherence theorem is implemented here.
-/
namespace MssnQuantumTransfer

/-- Exact Rational number as a pair (num, den) with den > 0. -/
structure RatVal where
  num : Int
  den : Nat
  den_pos : den > 0
  deriving Repr, DecidableEq

def RatVal.eq (a b : RatVal) : Bool :=
  a.num * (b.den : Int) == b.num * (a.den : Int)

def RatVal.mul (a b : RatVal) : RatVal :=
  ⟨a.num * b.num, a.den * b.den, Nat.mul_pos a.den_pos b.den_pos⟩

def RatVal.add (a b : RatVal) : RatVal :=
  ⟨a.num * (b.den : Int) + b.num * (a.den : Int), a.den * b.den, Nat.mul_pos a.den_pos b.den_pos⟩

def RatVal.one : RatVal := ⟨1, 1, Nat.zero_lt_one⟩
def RatVal.zero : RatVal := ⟨0, 1, Nat.zero_lt_one⟩

/-- Exact Gaussian Rational z = a + bi with a, b in Q. -/
structure GaussianRat where
  re : RatVal
  im : RatVal
  deriving Repr, DecidableEq

/-- Complex conjugation: (a + bi)* = a - bi. -/
def GaussianRat.conj (z : GaussianRat) : GaussianRat :=
  ⟨z.re, ⟨-z.im.num, z.im.den, z.im.den_pos⟩⟩

/-- Exact squared modulus: |z|^2 = a^2 + b^2 in Q. -/
def GaussianRat.normSq (z : GaussianRat) : RatVal :=
  RatVal.add (RatVal.mul z.re z.re) (RatVal.mul z.im z.im)

/-- Level 48 Path A: Exact Pythagorean Superposition State (3/5, 4/5 i). -/
def pythagoreanStateC0 : GaussianRat :=
  ⟨⟨3, 5, by decide⟩, RatVal.zero⟩

def pythagoreanStateC1 : GaussianRat :=
  ⟨RatVal.zero, ⟨4, 5, by decide⟩⟩

/-- Theorem: Pythagorean superposition has exact unit norm in rational arithmetic without square roots.
    (3/5)^2 + (4/5)^2 = 9/25 + 16/25 = 25/25 = 1. -/
theorem pythagorean_superposition_unit_norm :
    RatVal.eq (RatVal.add (pythagoreanStateC0.normSq) (pythagoreanStateC1.normSq)) RatVal.one = true := by
  decide

/-- Level 48 Path B: Unnormalized equal superposition ray (|0> + |1>).
    Amplitudes: c0 = 1, c1 = 1.
    Norm squared: 1^2 + 1^2 = 2 in Q (no 1/sqrt(2) required). -/
def equalSuperpositionNormSq : RatVal :=
  RatVal.add (⟨1, 1, by decide⟩) (⟨1, 1, by decide⟩)

theorem equal_superposition_norm_is_two :
    RatVal.eq equalSuperpositionNormSq ⟨2, 1, by decide⟩ = true := by
  decide

/-- Supplied rational value for the intended Path B expectation:
    <X> = <psi|X|psi> / <psi|psi> = 2 / 2 = 1 in Q. -/
def equalSuperpositionXExpectation : RatVal :=
  ⟨2, 2, by decide⟩

theorem projective_ray_expectation_exact_one :
    RatVal.eq equalSuperpositionXExpectation RatVal.one = true := by
  decide

/-- A declared correction table on two bits; no fidelity claim follows from it. -/
inductive FeedforwardGate where
  | I
  | Z
  | X
  | XZ
  deriving Repr, DecidableEq

def feedforwardSchedule : Bool → Bool → FeedforwardGate
  | false, false => .I
  | true, false => .Z
  | false, true => .X
  | true, true => .XZ

theorem feedforward_table_entries :
    feedforwardSchedule false false = .I ∧
    feedforwardSchedule true false = .Z ∧
    feedforwardSchedule false true = .X ∧
    feedforwardSchedule true true = .XZ := by
  decide

/-- BBPSSW Entanglement Distillation Purification:
    F' = (F^2 + 1/9 (1-F)^2) / (F^2 + 2/3 F(1-F) + 5/9 (1-F)^2).
    Evaluated for initial noisy Bell state F0 = 3/5:
    Numerator = (3/5)^2 + 1/9 (2/5)^2 = 9/25 + 4/225 = 85/225 = 17/45.
    Denominator = (3/5)^2 + 2/3 (3/5)(2/5) + 5/9 (2/5)^2 = 81/225 + 36/225 + 20/225 = 137/225.
    F1 = 85/137. -/
def bbpsswDistillationF0 : RatVal := ⟨3, 5, by decide⟩
def bbpsswDistillationF1 : RatVal := ⟨85, 137, by decide⟩

/-- Arithmetic comparison of the two supplied fixture values:
    F1 = 85/137 > 3/5 = F0 (since 85 * 5 = 425 > 137 * 3 = 411). -/
theorem bbpssw_fixture_ratio_increases :
    (bbpsswDistillationF1.num * (bbpsswDistillationF0.den : Int) >
     bbpsswDistillationF0.num * (bbpsswDistillationF1.den : Int)) := by
  decide

/-- Supplied values of two intended GHZ witness pairings.
    No density matrices or trace operation are defined in this file:
    W_GHZ = 1/2 I_8 - |GHZ><GHZ|.
    Tr(W * rho_GHZ) = -1/2 < 0.
    Tr(W * rho_000) = 0 >= 0. -/
def ghzWitnessTraceGHZ : RatVal := ⟨-1, 2, by decide⟩
def ghzWitnessTraceSeparable : RatVal := ⟨0, 1, by decide⟩

theorem declared_ghz_value_is_negative :
    ghzWitnessTraceGHZ.num < 0 := by
  decide

theorem declared_product_value_is_nonnegative :
    ghzWitnessTraceSeparable.num ≥ 0 := by
  decide

end MssnQuantumTransfer
