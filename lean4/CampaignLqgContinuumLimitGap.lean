/-
Campaign: LQG-CONTINUUM-LIMIT-GAP.

Finite census of the level-2 admissibility predicate on labels {0, 1, 2},
together with the two quantum-dimension identities in Q(sqrt 2).
The module imports no Mathlib. AuthorityEffect: None.
The node stays OPEN: this census does not discharge a continuum limit,
a semiclassical limit, or a physical cosmological constant.
-/

namespace CampaignLqgContinuumLimitGap

structure Qsqrt2 where
  rat : Rat
  coeff : Rat

namespace Qsqrt2

def zero : Qsqrt2 := { rat := 0, coeff := 0 }
def one : Qsqrt2 := { rat := 1, coeff := 0 }
def sqrt2 : Qsqrt2 := { rat := 0, coeff := 1 }

def add (x y : Qsqrt2) : Qsqrt2 :=
  { rat := x.rat + y.rat, coeff := x.coeff + y.coeff }

def neg (x : Qsqrt2) : Qsqrt2 :=
  { rat := -x.rat, coeff := -x.coeff }

def sub (x y : Qsqrt2) : Qsqrt2 := add x (neg y)

def mul (x y : Qsqrt2) : Qsqrt2 :=
  { rat := x.rat * y.rat + (2 : Rat) * x.coeff * y.coeff
    coeff := x.rat * y.coeff + x.coeff * y.rat }

/-- Quantum dimensions of twice-spin labels 0, 1, and 2. -/
def d0 : Qsqrt2 := one
def d1 : Qsqrt2 := sqrt2
def d2 : Qsqrt2 := one

end Qsqrt2

/-- Eight comparisons matching `ising_admissible` on twice-spin labels. -/
def admissible (a b c : Nat) : Bool :=
  decide (a ≤ 2) && decide (b ≤ 2) && decide (c ≤ 2) &&
    decide (c ≤ a + b) && decide (b ≤ a + c) && decide (a ≤ b + c) &&
    decide ((a + b + c) % 2 = 0) && decide (a + b + c ≤ 4)

def labels : List Nat := [0, 1, 2]

def triples : List (Nat × Nat × Nat) :=
  labels.flatMap fun a =>
    labels.flatMap fun b =>
      labels.map fun c => (a, b, c)

def admissibleRoster : List (Nat × Nat × Nat) :=
  triples.filter fun t => admissible t.1 t.2.1 t.2.2

def admissibleCount : Nat := admissibleRoster.length

theorem level2_dimension_truncation :
    Qsqrt2.sub (Qsqrt2.mul Qsqrt2.d1 Qsqrt2.d1) Qsqrt2.d0 = Qsqrt2.d2 ∧
      Qsqrt2.sub (Qsqrt2.mul Qsqrt2.d1 Qsqrt2.d2) Qsqrt2.d1 = Qsqrt2.zero := by
  unfold Qsqrt2.sub Qsqrt2.mul Qsqrt2.add Qsqrt2.neg
    Qsqrt2.d0 Qsqrt2.d1 Qsqrt2.d2 Qsqrt2.one Qsqrt2.sqrt2 Qsqrt2.zero
  grind

theorem level2_admissible_count :
    admissibleCount = 10 ∧
      admissibleRoster =
        [(0, 0, 0), (0, 1, 1), (0, 2, 2),
         (1, 0, 1), (1, 1, 0), (1, 1, 2), (1, 2, 1),
         (2, 0, 2), (2, 1, 1), (2, 2, 0)] ∧
      admissible 0 0 1 = false := by
  decide

theorem level2_tuple_census :
    (3 : Nat) ^ 6 = 729 ∧ (3 : Nat) ^ 9 = 19683 := by
  decide

theorem level2_counts_do_not_select_a_scale :
    (3 : Rat) ≠ 729 ∧ (729 : Rat) ≠ 19683 ∧ (3 : Rat) ≠ 19683 := by
  grind

theorem level2_free_positive_scale :
    ∃ lam : Rat, 0 < lam ∧ lam ≠ 3 ∧ lam ≠ 729 ∧ lam ≠ 19683 ∧
      (3 : Nat) ^ 6 = 729 ∧ (3 : Nat) ^ 9 = 19683 := by
  refine ⟨1, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · decide
  · grind
  · grind
  · grind
  · decide
  · decide

end CampaignLqgContinuumLimitGap

#print axioms CampaignLqgContinuumLimitGap.level2_dimension_truncation
#print axioms CampaignLqgContinuumLimitGap.level2_admissible_count
#print axioms CampaignLqgContinuumLimitGap.level2_tuple_census
#print axioms CampaignLqgContinuumLimitGap.level2_counts_do_not_select_a_scale
#print axioms CampaignLqgContinuumLimitGap.level2_free_positive_scale
