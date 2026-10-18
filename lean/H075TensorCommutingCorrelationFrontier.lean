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


/-- Theorem: Quantum lower bound 17/20 strictly exceeds classical value 3/4:
    3 * 20 < 17 * 4, i.e., 60 < 68. -/
theorem chsh_strictly_superclassical :
    (3 : Nat) * 20 < 17 * 4 := by
  decide

/-- Theorem: Certified interval [17/20, 43/50] is valid and non-empty:
    17 * 50 < 43 * 20, i.e., 850 < 860. -/
theorem chsh_interval_valid :
    (17 : Nat) * 50 < 43 * 20 := by
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
