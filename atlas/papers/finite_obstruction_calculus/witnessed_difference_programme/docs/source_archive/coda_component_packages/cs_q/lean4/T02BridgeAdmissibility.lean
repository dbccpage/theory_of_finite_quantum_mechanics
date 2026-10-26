import D01D02Records
import T01FactorizationFiberConstancy

/-!
# CODA-CS-Q T02: 14-Tuple Bridge Packet Schema & 8-Step Admission (BRIDGE-003)

Formalizes:
1. Schema field count parity: 14 fields in BridgePacket14.
2. 8-step admission projection theorems: each conjunct is recoverable.
3. Combined admission projector.
4. Admission implies fiber constancy via factorization conjunct.
5. QHeld 5-debt recovery.

AuthorityEffect: None.
-/

namespace CodaCsQ

open CodaCsQ

set_option linter.unusedVariables false

variable {α β γ : Type}

theorem BridgePacket14.field_count_eq_fourteen :
    BridgePacket14.field_count = 14 := rfl

theorem admissible_implies_finite_packet_validity
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    FinitePacketValidity.holds adm.finite_packet_validity :=
  h.1

theorem admissible_implies_tower_coherent
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    TowerCoherence.holds adm.tower_coherence :=
  h.2.1

theorem admissible_implies_completion
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    CompletionWitness.holds adm.completion :=
  h.2.2.1

theorem admissible_implies_q_held
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    QHeldDebts.paid adm.q_held :=
  h.2.2.2.1

theorem admissible_implies_profile_factorization
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    profile_factorization packet.Prof packet.q packet.q_bar :=
  h.2.2.2.2.1

theorem admissible_implies_route_independent
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    RouteIndependence.holds adm.route_independence :=
  h.2.2.2.2.2.1

theorem admissible_implies_reflection_descent
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    ReflectionDescent.holds adm.reflection_descent :=
  h.2.2.2.2.2.2.1

theorem admissible_implies_terminal_agreement
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    TerminalAgreement.holds adm.terminal_agreement :=
  h.2.2.2.2.2.2.2

theorem admissible_implies_all_eight
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    FinitePacketValidity.holds adm.finite_packet_validity ∧
    TowerCoherence.holds adm.tower_coherence ∧
    CompletionWitness.holds adm.completion ∧
    QHeldDebts.paid adm.q_held ∧
    profile_factorization packet.Prof packet.q packet.q_bar ∧
    RouteIndependence.holds adm.route_independence ∧
    ReflectionDescent.holds adm.reflection_descent ∧
    TerminalAgreement.holds adm.terminal_agreement := by
  exact ⟨
    admissible_implies_finite_packet_validity packet adm h,
    admissible_implies_tower_coherent packet adm h,
    admissible_implies_completion packet adm h,
    admissible_implies_q_held packet adm h,
    admissible_implies_profile_factorization packet adm h,
    admissible_implies_route_independent packet adm h,
    admissible_implies_reflection_descent packet adm h,
    admissible_implies_terminal_agreement packet adm h
  ⟩

theorem bridge_admissible8_implies_fiber_constancy
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet)
    (h : adm.holds) :
    fiber_constant packet.Prof packet.q :=
  factorization_implies_fiber_constancy packet.Prof packet.q packet.q_bar
    (admissible_implies_profile_factorization packet adm h)

theorem q_held_paid_implies_five_debts
    (d : QHeldDebts) (h : QHeldDebts.paid d) :
    d.shadow ∧ d.monotonicity ∧ d.topology ∧ d.formula ∧ d.trigger :=
  h

end CodaCsQ
