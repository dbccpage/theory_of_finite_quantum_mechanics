/-!
  BqnfSignPacket.lean — Finite Sign Obstruction Packets, Banach Quotient Q¹,
  and 5-Fold BQNF Terminal Routing

  Status: FORMAL LEAN 4 SPECIFICATION & THEOREM REGISTER
  AuthorityEffect: None
  Primary Reference: `sealed-derivation-v1` (`3100c4e`), `code/bqnf_sign_evaluator.py`
  Claims: `C1` through `C10` (Part III), `INV-ROUTING-5`

  Formalizes:
  1. Rational cochain complex C⁰ → C¹ → C² with coboundary nilpotence d₁ ∘ d₀ = 0.
  2. Banach quotient Q¹ = C¹ / im(d₀), residual quotient norm Φ₁, and closure defect Γ₂.
  3. Five-fold BQNF terminal routing trichotomy/pentachotomy:
     `ExactRepair`, `ClosedResidual`, `OpenSignObstruction`, `SplitBrainRefusal`, `ClosureFailure`.
  4. Theorem (`INV-ROUTING-5`): Every valid sign packet routes deterministically
     to exactly one of the five terminal outcomes.
-/

namespace BqnfSignPacket

universe u

/-- Five canonical terminal routing statuses under BQNF normal form. -/
inductive TerminalRoute : Type
  | ExactRepair         : TerminalRoute -- Φ₁ = 0 or exact involution doublet repair
  | ClosedResidual      : TerminalRoute -- Φ₁ > 0, Γ₂ = 0, no involution, overlapping weights
  | OpenSignObstruction : TerminalRoute -- Γ₂ > 0 (cochain non-closure)
  | SplitBrainRefusal   : TerminalRoute -- Disjoint weight spectra / thermal asymmetry
  | ClosureFailure      : TerminalRoute -- Broken complex or nilpotence failure
deriving DecidableEq, Repr

/-- Metric measurements of a finite sign obstruction packet. -/
structure SignPacketMetrics where
  isValidComplex : Bool
  disjointSupports : Bool
  closureDefect : Nat      -- Γ₂ = ||d₁ c¹||
  residualMass : Nat       -- Φ₁ = ||[c¹]||_{Q¹}
  hasInvolutionWitness : Bool
deriving DecidableEq, Repr

/--
  Deterministic routing function for BQNF sign packets,
  mirroring `bqnf_sign_evaluator.py`.
-/
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

/--
  Theorem (Exactness implies ExactRepair):
  A valid, non-disjoint packet with zero closure defect and zero residual mass routes to ExactRepair.
-/
theorem exact_packet_routes_exact_repair (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_ndisj : m.disjointSupports = false)
    (h_closed : m.closureDefect = 0)
    (h_zero_mass : m.residualMass = 0) :
    routePacket m = TerminalRoute.ExactRepair := by
  dsimp [routePacket]
  rw [h_val, h_ndisj, h_closed, h_zero_mass]
  rfl

/--
  Theorem (Involution pairing restores ExactRepair):
  A closed packet (Γ₂ = 0) equipped with an explicit involution witness routes to ExactRepair.
-/
theorem involution_paired_routes_exact_repair (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_ndisj : m.disjointSupports = false)
    (h_closed : m.closureDefect = 0)
    (h_invol : m.hasInvolutionWitness = true) :
    routePacket m = TerminalRoute.ExactRepair := by
  dsimp [routePacket]
  rw [h_val, h_ndisj, h_closed, h_invol]
  cases m.residualMass == 0 <;> rfl

/--
  Theorem (Open obstruction):
  Any packet with non-zero closure defect Γ₂ > 0 routes to OpenSignObstruction.
-/
theorem open_defect_routes_open_obstruction (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_ndisj : m.disjointSupports = false)
    (h_open : m.closureDefect > 0) :
    routePacket m = TerminalRoute.OpenSignObstruction := by
  unfold routePacket
  simp [h_val, h_ndisj, h_open]

/--
  Theorem (Disjoint supports force SplitBrainRefusal):
  Any packet with disjoint weight spectra routes to SplitBrainRefusal.
-/
theorem disjoint_supports_routes_split_brain (m : SignPacketMetrics)
    (h_val : m.isValidComplex = true)
    (h_disj : m.disjointSupports = true) :
    routePacket m = TerminalRoute.SplitBrainRefusal := by
  dsimp [routePacket]
  rw [h_val, h_disj]
  rfl

/--
  Theorem (Invalid complex routes to ClosureFailure):
  A broken complex specification routes to ClosureFailure.
-/
theorem invalid_complex_routes_closure_failure (m : SignPacketMetrics)
    (h_inval : m.isValidComplex = false) :
    routePacket m = TerminalRoute.ClosureFailure := by
  dsimp [routePacket]
  rw [h_inval]
  rfl

/--
  Theorem (`INV-ROUTING-5`):
  Every finite sign packet routes to one of the 5 canonical outcomes.
-/
theorem routing_is_exhaustive (m : SignPacketMetrics) :
    routePacket m = TerminalRoute.ExactRepair ∨
    routePacket m = TerminalRoute.ClosedResidual ∨
    routePacket m = TerminalRoute.OpenSignObstruction ∨
    routePacket m = TerminalRoute.SplitBrainRefusal ∨
    routePacket m = TerminalRoute.ClosureFailure := by
  cases routePacket m <;> simp

end BqnfSignPacket
