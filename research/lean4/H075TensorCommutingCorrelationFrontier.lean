/-
  H075TensorCommutingCorrelationFrontier.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)

  Campaign C500 Block 08: Correlation Models and Computability Boundary.
  This file proves distinctions between registry labels and integer inequalities.
  It does not define correlation sets or prove their strict separation, NPA
  convergence, game optimality, or MIP*=RE. Those remain external inputs.
  Scoped checks:
  1. Labels for the cited correlation hierarchy:
       C_q(d) ⊆ C_q ⊆ C_qa ⊆ C_qc.
  2. Bounded CHSH nonlocal game certified rational bounds:
       Classical value: 3/4.
       Quantum lower bound: 17/20.
       Quantum upper bound: 43/50.
       Exact inequalities: 3/4 < 17/20 and 17/20 < 43/50.
  3. NPA hierarchy finite-level status:
       Outer relaxation vs. exact value distinction.
       Flatness certificate label; no necessity theorem.
  4. Cited guardrail against unrestricted uniform solver.
-/

namespace FableHilbertWalk20260819.H075

-- ===========================================================================
-- Section 1: Correlation Model Hierarchy
-- ===========================================================================

inductive CorrelationModelClass where
  | FixedDimensionTensor (d : Nat)
  | FiniteDimensionTensorUnion
  | ApproximateTensorClosure
  | CommutingOperatorModel
  deriving DecidableEq, Repr

/-- The two registry constructors differ. This is not a theorem separating correlation sets. -/
theorem cqa_label_ne_cqc_label :
    CorrelationModelClass.ApproximateTensorClosure ≠
    CorrelationModelClass.CommutingOperatorModel := by
  intro h
  nomatch h

/-- The registry constructors differ; this does not prove non-closure of a correlation set. -/
theorem cq_label_ne_cqa_label :
    CorrelationModelClass.FiniteDimensionTensorUnion ≠
    CorrelationModelClass.ApproximateTensorClosure := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 2: CHSH Bounded Game Certified Inequalities
-- ===========================================================================

/- CHSH classical value numerator 3, denominator 4.
   Certified lower bound numerator 17, denominator 20.
   Certified upper bound numerator 43, denominator 50. -/


def chshClassicalNum : Nat := 3
def chshClassicalDen : Nat := 4
def chshLowerNum : Nat := 17
def chshLowerDen : Nat := 20
def chshUpperNum : Nat := 43
def chshUpperDen : Nat := 50

/-- Cleared comparison of two rational bounds `n1/d1 < n2/d2`. -/
def ratBelow (n1 d1 n2 d2 : Nat) : Prop := n1 * d2 < n2 * d1

/-- Quantum lower bound 17/20 strictly exceeds the classical value 3/4. -/
theorem chsh_strictly_superclassical :
    ratBelow chshClassicalNum chshClassicalDen chshLowerNum chshLowerDen := by
  unfold ratBelow
  decide

/-- The certified interval [17/20, 43/50] is non-empty. -/
theorem chsh_interval_valid :
    ratBelow chshLowerNum chshLowerDen chshUpperNum chshUpperDen := by
  unfold ratBelow
  decide

/-- `4 * (17/20 - 1/2) = 7/5`, cleared of denominators. -/
theorem chsh_lower_shift_is_seven_fifths :
    4 * (chshLowerNum * 2 - chshLowerDen) * 5 = 7 * chshLowerDen * 2 := by
  decide


-- ===========================================================================
/-- Exact witness for 7/5 < sqrt(2), conditional on the usual nonnegative root.
    Here 7/5 = 4*(17/20 - 1/2). No game-optimality theorem is asserted. -/
theorem chsh_lower_root_squared_bound : (7 : Nat)^2 < 2 * 5^2 := by decide

/-- Exact witness for sqrt(2) < 36/25; 36/25 = 4*(43/50 - 1/2). -/
theorem chsh_upper_root_squared_bound : (2 : Nat) * 25^2 < 36^2 := by decide

-- Section 3: NPA Finite-Level Relaxation and Flatness Distinction
-- ===========================================================================

inductive NpaLevelSemantics where
  | OuterSdpRelaxation
  | ExactValueCertifiedByFlatness
  deriving DecidableEq, Repr

/-- The two status labels differ; no SDP or flatness predicate is formalized. -/
theorem npa_outer_relaxation_ne_exact :
    NpaLevelSemantics.OuterSdpRelaxation ≠
    NpaLevelSemantics.ExactValueCertifiedByFlatness := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 4: Refusal of Unrestricted Uniform Value Solver
-- ===========================================================================

inductive SolverScope where
  | BoundedDecidableScenario
  | UnrestrictedUniformQuantumSolver
  deriving DecidableEq, Repr

/-- The scope labels differ; this is not an undecidability proof. -/
theorem bounded_solver_ne_unrestricted :
    SolverScope.BoundedDecidableScenario ≠
    SolverScope.UnrestrictedUniformQuantumSolver := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 5: Axiom Census & Auditing
-- ===========================================================================

#print axioms cqa_label_ne_cqc_label
#print axioms cq_label_ne_cqa_label
#print axioms chsh_strictly_superclassical
#print axioms chsh_interval_valid
#print axioms chsh_lower_root_squared_bound
#print axioms chsh_upper_root_squared_bound
#print axioms npa_outer_relaxation_ne_exact
#print axioms bounded_solver_ne_unrestricted

end FableHilbertWalk20260819.H075
