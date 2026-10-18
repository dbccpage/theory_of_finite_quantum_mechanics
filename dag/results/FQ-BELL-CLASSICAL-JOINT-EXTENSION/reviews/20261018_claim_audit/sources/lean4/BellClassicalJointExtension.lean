import DerivationDagQMClosure

/- Exact common-denominator form of the finite rational CHSH bound.
   Origin: FQ-BELL-CLASSICAL-JOINT-EXTENSION. AuthorityEffect: None. -/
namespace QuantumMechanics.BellClassicalJointExtension

open DerivationDagQMClosure

structure Assignment where
  a0 : Bool
  a1 : Bool
  b0 : Bool
  b1 : Bool
  deriving DecidableEq, Repr

def score (a : Assignment) : Int := chshDet a.a0 a.a1 a.b0 a.b1

theorem score_eq_two_or_neg_two (a : Assignment) : score a = 2 ∨ score a = -2 := by
  rcases a with ⟨a0, a1, b0, b1⟩
  cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide

theorem score_bound (a : Assignment) : -2 ≤ score a ∧ score a ≤ 2 := by
  have h := score_eq_two_or_neg_two a
  omega

-- Each weight is bound to its actual four-response assignment, not a supplied score.
def rows (law : List (Nat × Assignment)) : List (Nat × Int) :=
  law.map fun p => (p.1, score p.2)

def mass (law : List (Nat × Assignment)) : Int := totalWeight (rows law)
def numerator (law : List (Nat × Assignment)) : Int := weightedChshSum (rows law)

def sign (b : Bool) : Int := if b then 1 else -1

def correlation (left right : Assignment → Bool) : List (Nat × Assignment) → Int
  | [] => 0
  | (w, a) :: rest => (w : Int) * (sign (left a) * sign (right a)) + correlation left right rest

def correlationChsh (law : List (Nat × Assignment)) : Int :=
  correlation Assignment.a0 Assignment.b0 law + correlation Assignment.a0 Assignment.b1 law +
  correlation Assignment.a1 Assignment.b0 law - correlation Assignment.a1 Assignment.b1 law

theorem numerator_eq_four_correlations (law : List (Nat × Assignment)) :
    numerator law = correlationChsh law := by
  induction law with
  | nil => rfl
  | cons p rest ih =>
    rcases p with ⟨w, a⟩
    have hn : numerator ((w, a) :: rest) = (w : Int) * score a + numerator rest := rfl
    rw [hn, ih]
    simp only [correlationChsh, correlation, score, chshDet, sign, Int.mul_add, Int.mul_sub]
    omega

theorem joint_scaled_bound (law : List (Nat × Assignment)) :
    -2 * mass law ≤ numerator law ∧ numerator law ≤ 2 * mass law := by
  have hb : ∀ p ∈ rows law, -2 ≤ p.2 ∧ p.2 ≤ 2 := by
    intro p hp
    obtain ⟨x, _, rfl⟩ := List.mem_map.mp hp
    exact score_bound x.2
  exact (fq_bell_classical_joint_extension_convex_bound (rows law) hb).2

-- p_i = n_i / D, D > 0, and sum n_i = D. Thus this is exactly -2 <= S <= 2.
theorem normalized_joint_bound (law : List (Nat × Assignment)) (D : Nat)
    (hD : 0 < D) (hnormalized : mass law = (D : Int)) :
    (0 : Int) < (D : Int) ∧
    (-2 * (D : Int) ≤ numerator law ∧ numerator law ≤ 2 * (D : Int)) := by
  have hb := joint_scaled_bound law
  constructor
  · omega
  · simpa [hnormalized] using hb

theorem no_joint_law_above_two (law : List (Nat × Assignment)) (D : Nat) (target : Int)
    (hnormalized : mass law = (D : Int)) (hviolation : 2 * (D : Int) < target) :
    numerator law ≠ target := by
  have hb := joint_scaled_bound law
  omega

theorem normalized_four_correlation_bound (law : List (Nat × Assignment)) (D : Nat)
    (hD : 0 < D) (hnormalized : mass law = (D : Int)) :
    (0 : Int) < (D : Int) ∧
    (-2 * (D : Int) ≤ correlationChsh law ∧ correlationChsh law ≤ 2 * (D : Int)) := by
  simpa [numerator_eq_four_correlations] using normalized_joint_bound law D hD hnormalized

def plusAssignment : Assignment := ⟨false, false, false, false⟩
def minusAssignment : Assignment := ⟨true, false, false, false⟩

theorem both_bounds_are_attained :
    mass [(1, plusAssignment)] = 1 ∧ numerator [(1, plusAssignment)] = 2 ∧
    mass [(1, minusAssignment)] = 1 ∧ numerator [(1, minusAssignment)] = -2 := by
  decide

-- Signed coefficients 3/2 and -1/2 have total 1 but give CHSH = 4.
-- They are deliberately outside List (Nat × Assignment).
theorem positivity_is_essential :
    (3 + (-1 : Int) = 2) ∧
    (3 * score plusAssignment + (-1) * score minusAssignment = 8) ∧
    (8 > 2 * (2 : Int)) := by decide

theorem all_plus_correlator_decoy :
    (1 + 1 + 1 + (1 : Int) = 4) ∧ score plusAssignment = 2 := by decide

end QuantumMechanics.BellClassicalJointExtension

#print axioms QuantumMechanics.BellClassicalJointExtension.normalized_joint_bound
#print axioms QuantumMechanics.BellClassicalJointExtension.normalized_four_correlation_bound
#print axioms QuantumMechanics.BellClassicalJointExtension.no_joint_law_above_two
#print axioms QuantumMechanics.BellClassicalJointExtension.positivity_is_essential
