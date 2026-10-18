

namespace ChiralSuperconductorCore

inductive Chirality where
  | RightHanded : Chirality
  | LeftHanded  : Chirality
  deriving DecidableEq, Repr

def chirality_value : Chirality → Int
  | Chirality.RightHanded => 1
  | Chirality.LeftHanded  => -1

inductive SurfaceOrientation where
  | Top    : SurfaceOrientation
  | Bottom : SurfaceOrientation
  deriving DecidableEq, Repr

inductive TerminalRoute where
  | Repair : TerminalRoute
  | SplitBrainRefusal : TerminalRoute
  | ClosureFailure : TerminalRoute
  deriving DecidableEq, Repr

theorem nielsen_ninomiya_pair_cancellation :
    chirality_value Chirality.RightHanded + chirality_value Chirality.LeftHanded = 0 := by
  rfl

theorem net_chiral_charge_zero (charges : List Int) (h_sum : charges.sum = 0) :
    charges.sum = 0 := h_sum

def bulk_chern_difference (c_plus c_minus : Int) : Int := c_plus - c_minus

theorem weyl_pair_chern_difference :
    bulk_chern_difference (chirality_value Chirality.RightHanded) (chirality_value Chirality.LeftHanded) = 2 := by
  rfl

theorem slab_fermi_arc_count_matches_nodes (c_plus c_minus : Int) (h_plus : c_plus = 1) (h_minus : c_minus = -1) :
    (c_plus - c_minus) / 2 = 1 := by
  rw [h_plus, h_minus]
  rfl

theorem anomaly_inflow_conservation (a_bulk a_surface : Int) (h_cancel : a_bulk + a_surface = 0) :
    a_bulk + a_surface = 0 := h_cancel

structure MajoranaMode where
  energy : Int
  is_self_conjugate : Bool

def is_valid_majorana_zero_mode (m : MajoranaMode) : Prop :=
  m.energy = 0 ∧ m.is_self_conjugate = true

theorem majorana_zero_mode_energy (m : MajoranaMode) (h : is_valid_majorana_zero_mode m) :
    m.energy = 0 := h.1

def route_chiral_superconductor (net_chiral_charge : Int) (arc_discrepancy : Nat)
    (phs_valid : Bool) (inflow_anomaly : Int) : TerminalRoute :=
  if ¬phs_valid then
    TerminalRoute.ClosureFailure
  else if net_chiral_charge ≠ 0 ∨ arc_discrepancy ≠ 0 ∨ inflow_anomaly ≠ 0 then
    TerminalRoute.SplitBrainRefusal
  else
    TerminalRoute.Repair

theorem clean_chiral_superconductor_routes_to_repair :
    route_chiral_superconductor 0 0 true 0 = TerminalRoute.Repair := by
  rfl

theorem chiral_anomaly_routes_to_refusal (c : Int) (h_c : c ≠ 0) :
    route_chiral_superconductor c 0 true 0 = TerminalRoute.SplitBrainRefusal := by
  unfold route_chiral_superconductor
  split
  · contradiction
  · split
    · rfl
    · rename_i h_not
      exfalso
      apply h_not
      left
      exact h_c

theorem arc_discrepancy_routes_to_refusal (d : Nat) (h_d : d ≠ 0) :
    route_chiral_superconductor 0 d true 0 = TerminalRoute.SplitBrainRefusal := by
  unfold route_chiral_superconductor
  split
  · contradiction
  · split
    · rfl
    · rename_i h_not
      exfalso
      apply h_not
      right; left
      exact h_d

theorem inflow_anomaly_routes_to_refusal (a : Int) (h_a : a ≠ 0) :
    route_chiral_superconductor 0 0 true a = TerminalRoute.SplitBrainRefusal := by
  unfold route_chiral_superconductor
  split
  · contradiction
  · split
    · rfl
    · rename_i h_not
      exfalso
      apply h_not
      right; right
      exact h_a

theorem phs_broken_routes_to_closure_failure (c : Int) (d : Nat) (a : Int) :
    route_chiral_superconductor c d false a = TerminalRoute.ClosureFailure := by
  rfl

end ChiralSuperconductorCore
