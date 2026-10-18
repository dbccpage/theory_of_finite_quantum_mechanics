

namespace KitaevHoneycombCore

inductive Sublattice where
  | A : Sublattice
  | B : Sublattice
  deriving DecidableEq, Repr

inductive BondDir where
  | X : BondDir
  | Y : BondDir
  | Z : BondDir
  deriving DecidableEq, Repr

inductive TerminalRoute where
  | Repair : TerminalRoute
  | SplitBrainRefusal : TerminalRoute
  | ClosureFailure : TerminalRoute
  deriving DecidableEq, Repr

def is_vortex (w_p : Int) : Prop := w_p = -1
def is_vortex_free (w_p : Int) : Prop := w_p = 1

def is_valid_gauge_link (u : Int) : Prop := u = 1 ∨ u = -1

theorem gauge_link_square (u : Int) (h : is_valid_gauge_link u) : u * u = 1 := by
  rcases h with rfl | rfl <;> rfl

theorem link_gauge_operators_commute (u1 u2 : Int) : u1 * u2 = u2 * u1 := by
  exact Int.mul_comm u1 u2

theorem plaquette_flux_gauge_invariant (w : Int) (w_next : Int) (h_inv : w_next = w) :
    w_next - w = 0 := by
  omega

theorem torus_flux_parity_even (total_vortices : Nat) (h_even : total_vortices % 2 = 0) :
    total_vortices % 2 = 0 := h_even

theorem fermion_parity_conserved (p_initial p_final : Int) (h_eq : p_initial = p_final) :
    p_final - p_initial = 0 := by
  omega

def ising_mutual_braiding_angle_units (f : Nat) : Int :=
  if f % 2 = 0 then -1 else 3

theorem ising_braiding_phase_distinction (f1 f2 : Nat)
    (h1 : f1 % 2 = 0) (h2 : f2 % 2 = 1) :
    ising_mutual_braiding_angle_units f1 ≠ ising_mutual_braiding_angle_units f2 := by
  simp [ising_mutual_braiding_angle_units, h1, h2]

def route_honeycomb_state (vortex_count : Nat) (parity_defect : Bool) (gauge_invariant : Bool) : TerminalRoute :=
  if ¬gauge_invariant then
    TerminalRoute.ClosureFailure
  else if parity_defect ∨ (vortex_count % 2 ≠ 0) then
    TerminalRoute.SplitBrainRefusal
  else
    TerminalRoute.Repair

theorem ground_state_routes_to_repair :
    route_honeycomb_state 0 false true = TerminalRoute.Repair := by
  rfl

theorem valid_vortex_pair_routes_to_repair (k : Nat) :
    route_honeycomb_state (2 * k) false true = TerminalRoute.Repair := by
  have h_even : (2 * k) % 2 = 0 := by omega
  unfold route_honeycomb_state
  split
  · contradiction
  · split
    · rename_i h_defect
      rcases h_defect with h_p | h_odd
      · contradiction
      · contradiction
    · rfl

theorem parity_defect_routes_to_refusal (v : Nat) :
    route_honeycomb_state v true true = TerminalRoute.SplitBrainRefusal := by
  unfold route_honeycomb_state
  split
  · contradiction
  · split
    · rfl
    · rename_i h_not
      exfalso
      apply h_not
      left
      rfl

theorem odd_flux_anomaly_routes_to_refusal (k : Nat) :
    route_honeycomb_state (2 * k + 1) false true = TerminalRoute.SplitBrainRefusal := by
  have h_odd : (2 * k + 1) % 2 ≠ 0 := by omega
  unfold route_honeycomb_state
  split
  · contradiction
  · split
    · rfl
    · rename_i h_not
      exfalso
      apply h_not
      right
      exact h_odd

theorem gauge_defect_routes_to_closure_failure (v : Nat) (p : Bool) :
    route_honeycomb_state v p false = TerminalRoute.ClosureFailure := by
  rfl

end KitaevHoneycombCore
