


namespace InstantonDyonGas

inductive DyonSpecies : Type where
  | M_dyon : DyonSpecies
  | L_dyon : DyonSpecies
  | M_bar  : DyonSpecies
  | L_bar  : DyonSpecies
deriving DecidableEq, Repr

def magnetic_charge : DyonSpecies → Int
  | .M_dyon => 1
  | .L_dyon => -1
  | .M_bar  => -1
  | .L_bar  => 1

def topological_charge_units (nu_units : Int) (D : Int) : DyonSpecies → Int
  | .M_dyon => nu_units
  | .L_dyon => D - nu_units
  | .M_bar  => -nu_units
  | .L_bar  => -(D - nu_units)

theorem kvbll_fractional_charge_sum (nu_units : Int) (D : Int) :
    topological_charge_units nu_units D DyonSpecies.M_dyon +
    topological_charge_units nu_units D DyonSpecies.L_dyon = D := by
  dsimp [topological_charge_units]
  omega

theorem neutral_dipole_magnetic_charge_is_zero :
    magnetic_charge DyonSpecies.M_dyon + magnetic_charge DyonSpecies.M_bar = 0 := by
  dsimp [magnetic_charge]

theorem neutral_dipole_topological_charge_is_zero (nu_units : Int) (D : Int) :
    topological_charge_units nu_units D DyonSpecies.M_dyon +
    topological_charge_units nu_units D DyonSpecies.M_bar = 0 := by
  dsimp [topological_charge_units]
  omega

theorem neutral_quartet_topological_charge_is_zero (nu_units : Int) (D : Int) :
    topological_charge_units nu_units D DyonSpecies.M_dyon +
    topological_charge_units nu_units D DyonSpecies.M_bar +
    topological_charge_units nu_units D DyonSpecies.L_dyon +
    topological_charge_units nu_units D DyonSpecies.L_bar = 0 := by
  dsimp [topological_charge_units]
  omega

def dirac_phase (lk : Int) : Int :=
  if lk % 2 = 0 then 1 else -1

theorem unlinked_dirac_phase_is_positive :
    dirac_phase 0 = 1 := by
  dsimp [dirac_phase]

theorem linked_dirac_phase_is_negative :
    dirac_phase 1 = -1 := by
  dsimp [dirac_phase]

def dyonDefectMass (phase : Int) : Nat :=
  if phase = 1 then 0 else 2

theorem molecular_cluster_nullifies_defect (h : dirac_phase 0 = 1) :
    dyonDefectMass (dirac_phase 0) = 0 := by
  dsimp [dyonDefectMass]
  rw [h]
  rfl

theorem monopole_braiding_obstructs_sign (h : dirac_phase 1 = -1) :
    dyonDefectMass (dirac_phase 1) = 2 := by
  dsimp [dyonDefectMass]
  rw [h]
  rfl

theorem dyonic_involution_pair_cancels_sign (w : Int) :
    w * 1 + w * (-1) = 0 := by
  omega

theorem plasma_action_gap_separates_weights (s_pos s_neg : Int) (h : s_neg > s_pos) :
    s_neg - s_pos > 0 := by
  omega

end InstantonDyonGas
