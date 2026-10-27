

namespace HilbertWalk.TensorCommutingCorrelationFrontier


inductive CorrelationModelClass where
  | FixedDimensionTensor (d : Nat)
  | FiniteDimensionTensorUnion
  | ApproximateTensorClosure
  | CommutingOperatorModel
  deriving DecidableEq, Repr

theorem cqa_label_ne_cqc_label :
    CorrelationModelClass.ApproximateTensorClosure ≠
    CorrelationModelClass.CommutingOperatorModel := by
  intro h
  nomatch h

theorem cq_label_ne_cqa_label :
    CorrelationModelClass.FiniteDimensionTensorUnion ≠
    CorrelationModelClass.ApproximateTensorClosure := by
  intro h
  nomatch h





def chshClassicalNum : Nat := 3
def chshClassicalDen : Nat := 4
def chshLowerNum : Nat := 17
def chshLowerDen : Nat := 20
def chshUpperNum : Nat := 43
def chshUpperDen : Nat := 50

def ratBelow (n1 d1 n2 d2 : Nat) : Prop := n1 * d2 < n2 * d1

theorem chsh_strictly_superclassical :
    ratBelow chshClassicalNum chshClassicalDen chshLowerNum chshLowerDen := by
  unfold ratBelow
  decide

theorem chsh_interval_valid :
    ratBelow chshLowerNum chshLowerDen chshUpperNum chshUpperDen := by
  unfold ratBelow
  decide

theorem chsh_lower_shift_is_seven_fifths :
    4 * (chshLowerNum * 2 - chshLowerDen) * 5 = 7 * chshLowerDen * 2 := by
  decide


theorem chsh_lower_root_squared_bound : (7 : Nat)^2 < 2 * 5^2 := by decide

theorem chsh_upper_root_squared_bound : (2 : Nat) * 25^2 < 36^2 := by decide


inductive NpaLevelSemantics where
  | OuterSdpRelaxation
  | ExactValueCertifiedByFlatness
  deriving DecidableEq, Repr

theorem npa_outer_relaxation_ne_exact :
    NpaLevelSemantics.OuterSdpRelaxation ≠
    NpaLevelSemantics.ExactValueCertifiedByFlatness := by
  intro h
  nomatch h



inductive SolverScope where
  | BoundedDecidableScenario
  | UnrestrictedUniformQuantumSolver
  deriving DecidableEq, Repr

theorem bounded_solver_ne_unrestricted :
    SolverScope.BoundedDecidableScenario ≠
    SolverScope.UnrestrictedUniformQuantumSolver := by
  intro h
  nomatch h



#print axioms cqa_label_ne_cqc_label
#print axioms cq_label_ne_cqa_label
#print axioms chsh_strictly_superclassical
#print axioms chsh_interval_valid
#print axioms chsh_lower_root_squared_bound
#print axioms chsh_upper_root_squared_bound
#print axioms npa_outer_relaxation_ne_exact
#print axioms bounded_solver_ne_unrestricted

end HilbertWalk.TensorCommutingCorrelationFrontier

private def l5aProvenance : String :=
  "Origin: lean4/TensorCommutingCorrelationFrontier.lean Claim: cqa_label_ne_cqc_label AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
