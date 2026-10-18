


namespace BqnfSignPacket

universe u

inductive TerminalRoute : Type
  | ExactRepair         : TerminalRoute
  | ClosedResidual      : TerminalRoute
  | OpenSignObstruction : TerminalRoute
  | SplitBrainRefusal   : TerminalRoute
  | ClosureFailure      : TerminalRoute
deriving DecidableEq, Repr

structure SignPacketMetrics where
  isValidComplex : Bool
  disjointSupports : Bool
  closureDefect : Nat
  residualMass : Nat
  hasInvolutionWitness : Bool
deriving DecidableEq, Repr

def routePacket (m : SignPacketMetrics) : TerminalRoute :=
  if ¬m.isValidComplex then
    TerminalRoute.ClosureFailure
  else if m.disjointSupports then
    TerminalRoute.SplitBrainRefusal
  else if m.closureDefect > 0 then
    TerminalRoute.OpenSignObstruction
  else if (m.residualMass == 0 || m.hasInvolutionWitness) then
    TerminalRoute.ExactRepair
  else
    TerminalRoute.ClosedResidual

theorem exact_packet_routes_exact_repair (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_ndisj : m.disjointSupports = false)
    (h_closed : m.closureDefect = 0)
    (h_zero_mass : m.residualMass = 0) :
    routePacket m = TerminalRoute.ExactRepair := by
  dsimp [routePacket]
  rw [h_val, h_ndisj, h_closed, h_zero_mass]
  rfl

theorem involution_paired_routes_exact_repair (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_ndisj : m.disjointSupports = false)
    (h_closed : m.closureDefect = 0)
    (h_invol : m.hasInvolutionWitness = true) :
    routePacket m = TerminalRoute.ExactRepair := by
  dsimp [routePacket]
  rw [h_val, h_ndisj, h_closed, h_invol]
  cases m.residualMass == 0 <;> rfl

theorem open_defect_routes_open_obstruction (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_ndisj : m.disjointSupports = false)
    (h_open : m.closureDefect > 0) :
    routePacket m = TerminalRoute.OpenSignObstruction := by
  unfold routePacket
  simp [h_val, h_ndisj, h_open]

theorem disjoint_supports_routes_split_brain (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_disj : m.disjointSupports = true) :
    routePacket m = TerminalRoute.SplitBrainRefusal := by
  dsimp [routePacket]
  rw [h_val, h_disj]
  rfl

theorem invalid_complex_routes_closure_failure (m : SignPacketMetrics)
    (h_inval : m.isValidComplex = false) :
    routePacket m = TerminalRoute.ClosureFailure := by
  dsimp [routePacket]
  rw [h_inval]
  rfl

theorem routing_is_exhaustive (m : SignPacketMetrics) :
    routePacket m = TerminalRoute.ExactRepair ∨
    routePacket m = TerminalRoute.ClosedResidual ∨
    routePacket m = TerminalRoute.OpenSignObstruction ∨
    routePacket m = TerminalRoute.SplitBrainRefusal ∨
    routePacket m = TerminalRoute.ClosureFailure := by
  cases routePacket m <;> simp

end BqnfSignPacket
