/-
Prime Triad Foundations: Types and Operations.
AuthorityEffect: None.
-/

namespace Prime

/-- Stage of candidate packet processing in Prime 000. -/
inductive PacketPhase where
  | proposed : PacketPhase
  | admitted : PacketPhase
  | measured : PacketPhase
  deriving DecidableEq, Repr

/-- Packet record tracking admission and measurement state. -/
structure Packet where
  id : Nat
  admitted : Bool
  measured : Bool
  deriving DecidableEq, Repr

/-- Measurement gate: measurement is refused if packet is not admitted. -/
def canMeasure (p : Packet) : Bool :=
  p.admitted

/-- Execute measurement: only succeeds when admitted is true. -/
def measure (p : Packet) : Option Packet :=
  if p.admitted then
    some { p with measured := true }
  else
    none

/-- Prime 002: Canonical 9 continuation conjuncts. -/
structure CanContinue9 where
  has_obligation : Bool
  has_witness : Bool
  next_carrier_declared : Bool
  adapter_sound : Bool
  detector_adequate : Bool
  minimal_lift : Bool
  skeleton_preserved : Bool
  budget_remains : Bool
  not_gtla_refusal : Bool
  deriving DecidableEq, Repr

/-- Evaluation of all 9 conjuncts. -/
def CanContinue9.evaluate (c : CanContinue9) : Bool :=
  c.has_obligation &&
  c.has_witness &&
  c.next_carrier_declared &&
  c.adapter_sound &&
  c.detector_adequate &&
  c.minimal_lift &&
  c.skeleton_preserved &&
  c.budget_remains &&
  c.not_gtla_refusal

/-- Weakened 3-condition summary form. -/
structure CanContinue3 where
  structural : Bool
  budget : Bool
  no_stop : Bool
  deriving DecidableEq, Repr

/-- Evaluation of 3-condition summary form. -/
def CanContinue3.evaluate (c : CanContinue3) : Bool :=
  c.structural && c.budget && c.no_stop

/-- Canonical reduction map from 9 conjuncts to 3 conditions. -/
def cc9_to_cc3 (c : CanContinue9) : CanContinue3 :=
  { structural := c.has_obligation && c.has_witness && c.next_carrier_declared &&
                  c.adapter_sound && c.detector_adequate && c.minimal_lift &&
                  c.skeleton_preserved,
    budget := c.budget_remains,
    no_stop := c.not_gtla_refusal }

/-- Phase embedding map preserving causal partial order. -/
structure PhaseEmbedding where
  toFun : Nat → Nat
  monotone : ∀ a b, a ≤ b → toFun a ≤ toFun b

end Prime
