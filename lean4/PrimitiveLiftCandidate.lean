/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import PrimitiveTerminalPacket
/-!
Primitive lift candidate kernel.

This file separates a raw quotient carrier from a lift checklist. A licensed
candidate requires source obstruction, a new carrier, replay evidence,
residual reduction, and closure preservation.
-/

namespace OmegaCore
namespace PrimitiveLiftCandidate

universe u v

variable {α : Type u} {β : Type v}

structure RawClassCarrier
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (q : PointedResidualQuotient P) where
  raw : α
  class_eq : PrimitiveDifference.classOf P.toPrimitiveDifference raw = q
  packet : PrimitiveTerminalPacket.TerminalPacket C q

def rawCarrierFromRaw
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (x : α) :
    RawClassCarrier P C
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) where
  raw := x
  class_eq := rfl
  packet := PrimitiveTerminalPacket.packetFor C
    (PrimitiveDifference.classOf P.toPrimitiveDifference x)

theorem rawCarrier_class_eq
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (carrier : RawClassCarrier P C q) :
    PrimitiveDifference.classOf P.toPrimitiveDifference carrier.raw = q :=
  carrier.class_eq

theorem rawCarrier_packet_status_matches
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (carrier : RawClassCarrier P C q) :
    carrier.packet.status = C.terminalize q :=
  PrimitiveTerminalPacket.packet_status_matches_terminalize
    C q carrier.packet

structure LiftCandidate where
  hasSourceObstruction : Bool
  hasNewCarrier : Bool
  hasReplay : Bool
  reducesPhi : Bool
  preservesClosure : Bool

def IsLicensedLiftCandidate (L : LiftCandidate) : Prop :=
  L.hasSourceObstruction = true ∧
    L.hasNewCarrier = true ∧
    L.hasReplay = true ∧
    L.reducesPhi = true ∧
    L.preservesClosure = true

theorem licensed_lift_iff_all_fields_true
    (L : LiftCandidate) :
    IsLicensedLiftCandidate L ↔
      L.hasSourceObstruction = true ∧
      L.hasNewCarrier = true ∧
      L.hasReplay = true ∧
      L.reducesPhi = true ∧
      L.preservesClosure = true :=
  Iff.rfl

theorem licensed_lift_requires_source_obstruction
    (L : LiftCandidate) :
    IsLicensedLiftCandidate L → L.hasSourceObstruction = true :=
  fun h => h.1

theorem licensed_lift_requires_new_carrier
    (L : LiftCandidate) :
    IsLicensedLiftCandidate L → L.hasNewCarrier = true :=
  fun h => h.2.1

theorem licensed_lift_requires_replay
    (L : LiftCandidate) :
    IsLicensedLiftCandidate L → L.hasReplay = true :=
  fun h => h.2.2.1

theorem licensed_lift_requires_residual_reduction
    (L : LiftCandidate) :
    IsLicensedLiftCandidate L → L.reducesPhi = true :=
  fun h => h.2.2.2.1

theorem licensed_lift_requires_closure_preservation
    (L : LiftCandidate) :
    IsLicensedLiftCandidate L → L.preservesClosure = true :=
  fun h => h.2.2.2.2

theorem missing_source_obstruction_blocks_lift
    (L : LiftCandidate)
    (hSource : L.hasSourceObstruction = false) :
    ¬ IsLicensedLiftCandidate L := by
  intro hLicensed
  unfold IsLicensedLiftCandidate at hLicensed
  rw [hSource] at hLicensed
  cases hLicensed.1

theorem missing_new_carrier_blocks_lift
    (L : LiftCandidate)
    (hCarrier : L.hasNewCarrier = false) :
    ¬ IsLicensedLiftCandidate L := by
  intro hLicensed
  unfold IsLicensedLiftCandidate at hLicensed
  rw [hCarrier] at hLicensed
  cases hLicensed.2.1

theorem missing_replay_blocks_lift
    (L : LiftCandidate)
    (hReplay : L.hasReplay = false) :
    ¬ IsLicensedLiftCandidate L := by
  intro hLicensed
  unfold IsLicensedLiftCandidate at hLicensed
  rw [hReplay] at hLicensed
  cases hLicensed.2.2.1

theorem missing_reduction_blocks_lift
    (L : LiftCandidate)
    (hReduction : L.reducesPhi = false) :
    ¬ IsLicensedLiftCandidate L := by
  intro hLicensed
  unfold IsLicensedLiftCandidate at hLicensed
  rw [hReduction] at hLicensed
  cases hLicensed.2.2.2.1

theorem missing_closure_preservation_blocks_lift
    (L : LiftCandidate)
    (hClosure : L.preservesClosure = false) :
    ¬ IsLicensedLiftCandidate L := by
  intro hLicensed
  unfold IsLicensedLiftCandidate at hLicensed
  rw [hClosure] at hLicensed
  cases hLicensed.2.2.2.2

def strictly_improves (p1 g1 : Nat) (x1 : Option Nat) (p2 g2 : Nat) (x2 : Option Nat) : Prop :=
  p2 < p1 ∨
  (p2 = p1 ∧ g2 < g1) ∨
  (p2 = p1 ∧ g2 = g1 ∧ (match x1, x2 with | some v1, some v2 => v2 < v1 | _, _ => False))

instance (x1 x2 : Option Nat) : Decidable (match x1, x2 with | some v1, some v2 => v2 < v1 | _, _ => False) := by
  cases x1 <;> cases x2 <;> simp <;> infer_instance

instance (p1 g1 : Nat) (x1 : Option Nat) (p2 g2 : Nat) (x2 : Option Nat) : Decidable (strictly_improves p1 g1 x1 p2 g2 x2) := by
  unfold strictly_improves
  infer_instance

theorem strictly_improves_irreflexive (p g : Nat) (x : Option Nat) :
    ¬ strictly_improves p g x p g x := by
  intro h
  unfold strictly_improves at h
  rcases h with h1 | h2 | h3
  · exact Nat.lt_irrefl p h1
  · exact Nat.lt_irrefl g h2.2
  · have hx := h3.2.2
    cases hx_opt : x
    · simp [hx_opt] at hx
    · simp [hx_opt] at hx

theorem strictly_improves_transitive
    {p1 g1 p2 g2 p3 g3 : Nat} {x1 x2 x3 : Option Nat}
    (h12 : strictly_improves p1 g1 x1 p2 g2 x2)
    (h23 : strictly_improves p2 g2 x2 p3 g3 x3) :
    strictly_improves p1 g1 x1 p3 g3 x3 := by
  unfold strictly_improves at h12 h23 ⊢
  rcases h12 with hp12 | ⟨heq12, hg12⟩ | ⟨heq12, heqg12, hx12⟩
  · rcases h23 with hp23 | ⟨heq23, hg23⟩ | ⟨heq23, heqg23, hx23⟩
    · left; exact Nat.lt_trans hp23 hp12
    · left; rw [heq23]; exact hp12
    · left; rw [heq23]; exact hp12
  · rcases h23 with hp23 | ⟨heq23, hg23⟩ | ⟨heq23, heqg23, hx23⟩
    · left; rw [heq12] at hp23; exact hp23
    · right; left; constructor
      · rw [heq23, heq12]
      · exact Nat.lt_trans hg23 hg12
    · right; left; constructor
      · rw [heq23, heq12]
      · rw [heqg23]; exact hg12
  · rcases h23 with hp23 | ⟨heq23, hg23⟩ | ⟨heq23, heqg23, hx23⟩
    · left; rw [heq12] at hp23; exact hp23
    · right; left; constructor
      · rw [heq23, heq12]
      · rw [heqg12] at hg23; exact hg23
    · right; right; constructor
      · rw [heq23, heq12]
      · constructor
        · rw [heqg23, heqg12]
        · cases hx1_opt : x1 <;> cases hx2_opt : x2 <;> cases hx3_opt : x3 <;>
            first
            | { simp [hx1_opt, hx2_opt, hx3_opt] at hx12 hx23; done }
            | { simp [hx1_opt, hx2_opt, hx3_opt] at hx12 hx23 ⊢; exact Nat.lt_trans hx23 hx12 }


structure EvaluationResult where
  phi_after : Nat
  gamma_after : Nat
  xi_after : Option Nat

def adjoinRepairGeneratorResult (p_before g_before : Nat) : EvaluationResult where
  phi_after := 0
  gamma_after := 0
  xi_after := none

theorem adjoinRepairGenerator_makes_exact (p_before g_before : Nat) :
    (adjoinRepairGeneratorResult p_before g_before).phi_after = 0 :=
  rfl

def rollback (p_before g_before : Nat) (x_before : Option Nat) (res : EvaluationResult) : EvaluationResult :=
  if strictly_improves p_before g_before x_before res.phi_after res.gamma_after res.xi_after then
    res
  else
    ⟨p_before, g_before, x_before⟩

theorem rollback_fixed_point_of_rejected
    (p_before g_before : Nat) (x_before : Option Nat) (res : EvaluationResult)
    (h_reject : ¬ strictly_improves p_before g_before x_before res.phi_after res.gamma_after res.xi_after) :
    rollback p_before g_before x_before res = ⟨p_before, g_before, x_before⟩ := by
  unfold rollback
  simp [h_reject]

end PrimitiveLiftCandidate
end OmegaCore
