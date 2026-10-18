


namespace FoliatedFracton2Gauge

inductive FoliationPlane : Type where
  | xy : FoliationPlane
  | yz : FoliationPlane
  | zx : FoliationPlane
deriving DecidableEq, Repr

inductive Mobility : Type where
  | fracton : Mobility
  | lineon  : Mobility
  | planon  : Mobility
deriving DecidableEq, Repr

theorem planon_dipole_neutrality (q : Int) :
    q + (-q) = 0 := by
  omega

theorem planon_dipole_defect_nullification (w : Int) :
    w * 1 + w * (-1) = 0 := by
  omega

theorem subsystem_extensive_gap_positive (kappa : Nat) (R : Nat) (h_k : kappa > 0) (h_R : R > 0) :
    kappa * R > 0 := by
  exact Nat.mul_pos h_k h_R

theorem extensive_gap_separates_weights (w_plus w_minus : Int) (gap : Nat) (h_gap : gap > 0) (h_sep : w_plus - w_minus ≥ (gap : Int)) :
    w_plus ≠ w_minus := by
  omega

def hingeCommutatorTrace (is_nonabelian : Bool) : Int :=
  if is_nonabelian then -2 else 2

theorem abelian_hinge_trace_positive :
    hingeCommutatorTrace false = 2 := by
  rfl

theorem nonabelian_hinge_trace_negative :
    hingeCommutatorTrace true = -2 := by
  rfl

def fractonDefectMass (tr : Int) : Nat :=
  if tr ≥ 0 then 0 else 2

theorem abelian_hinge_defect_mass_zero :
    fractonDefectMass (hingeCommutatorTrace false) = 0 := by
  rfl

theorem nonabelian_hinge_defect_mass_two :
    fractonDefectMass (hingeCommutatorTrace true) = 2 := by
  rfl

def foliatedProjectedTrace (has_corner_lineon : Bool) (base_tr : Int) : Int :=
  if has_corner_lineon then base_tr else (base_tr.natAbs * base_tr.natAbs : Nat)

theorem decoupled_foliated_projection_nonnegative (tr : Int) :
    0 ≤ foliatedProjectedTrace false tr := by
  dsimp [foliatedProjectedTrace]
  exact Int.natCast_nonneg _

theorem corner_lineon_obstruction_persists (h : hingeCommutatorTrace true = -2) :
    foliatedProjectedTrace true (hingeCommutatorTrace true) < 0 := by
  rw [h]
  decide

end FoliatedFracton2Gauge
