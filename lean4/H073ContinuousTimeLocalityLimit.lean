

namespace FableHilbertWalk20260819.H073


theorem trotter1_denom_strictly_increasing {n1 n2 : Nat} (h : n1 < n2) :
    2 * n1 < 2 * n2 := Nat.mul_lt_mul_of_pos_left h (by decide)

theorem trotter2_denom_strictly_increasing {n1 n2 : Nat} (hn1 : n1 > 0) (h : n1 < n2) :
    12 * (n1 * n1) < 12 * (n2 * n2) := by
  have h_sq : n1 * n1 < n2 * n2 := by
    have h1 : n1 * n1 < n1 * n2 := Nat.mul_lt_mul_of_pos_left h hn1
    have h2 : n1 * n2 < n2 * n2 := Nat.mul_lt_mul_of_pos_right h (Nat.lt_trans hn1 h)
    exact Nat.lt_trans h1 h2
  exact Nat.mul_lt_mul_of_pos_left h_sq (by decide)

theorem trotter_steps_order : (10 : Nat) < 20 ∧ (20 : Nat) < 50 := by decide



def outside_declared_cone (dist : Nat) (v : Nat) (t : Nat) : Prop :=
  dist > v * t

theorem outside_cone_arithmetic_witness : outside_declared_cone 5 2 1 := by
  dsimp [outside_declared_cone]
  decide

theorem inside_cone_arithmetic_witness : ¬ outside_declared_cone 1 2 1 := by
  dsimp [outside_declared_cone]
  decide



inductive DynamicalActionType where
  | DiscreteGroupActionZ
  | ContinuousFlowActionR
  deriving DecidableEq, Repr

theorem declared_action_type_labels_differ :
    DynamicalActionType.DiscreteGroupActionZ ≠ DynamicalActionType.ContinuousFlowActionR := by
  intro h
  nomatch h



inductive DenseOrbitAuditStatus where
  | Hit
  | Miss
  | Narrowed
  | ScopedEvidence
  deriving DecidableEq, Repr

def c250_dense_orbit_audit_status : DenseOrbitAuditStatus :=
  DenseOrbitAuditStatus.Narrowed

theorem declared_dense_orbit_status_is_narrowed :
    c250_dense_orbit_audit_status = DenseOrbitAuditStatus.Narrowed := by
  rfl

theorem declared_dense_orbit_status_not_hit :
    c250_dense_orbit_audit_status ≠ DenseOrbitAuditStatus.Hit := by
  intro h
  nomatch h



structure ContinuousGeneratorHypotheses where
  topology_declared : Bool
  stone_strong_continuity : Bool
  thermodynamic_algebra_complete : Bool
  lieb_robinson_velocity_bounded : Bool

def standard_continuous_hypotheses : ContinuousGeneratorHypotheses := {
  topology_declared := true,
  stone_strong_continuity := true,
  thermodynamic_algebra_complete := true,
  lieb_robinson_velocity_bounded := false
}

theorem declared_hypotheses_leave_locality_open :
    standard_continuous_hypotheses.topology_declared = true ∧
    standard_continuous_hypotheses.stone_strong_continuity = true ∧
    standard_continuous_hypotheses.thermodynamic_algebra_complete = true ∧
    standard_continuous_hypotheses.lieb_robinson_velocity_bounded = false := by
  decide



#print axioms trotter1_denom_strictly_increasing
#print axioms trotter2_denom_strictly_increasing
#print axioms trotter_steps_order
#print axioms outside_cone_arithmetic_witness
#print axioms inside_cone_arithmetic_witness
#print axioms declared_action_type_labels_differ
#print axioms declared_dense_orbit_status_is_narrowed
#print axioms declared_dense_orbit_status_not_hit
#print axioms declared_hypotheses_leave_locality_open

end FableHilbertWalk20260819.H073

private def l5aProvenance : String :=
  "Origin: lean4/H073ContinuousTimeLocalityLimit.lean Claim: trotter1_denom_strictly_increasing AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
