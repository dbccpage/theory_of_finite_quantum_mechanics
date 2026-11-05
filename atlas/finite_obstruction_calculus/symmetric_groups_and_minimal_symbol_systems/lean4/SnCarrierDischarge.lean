import SnCarrier
import SnSyntax

/-!
Compiled discharge of the two SnCarrier defects recorded as WDP-P001-019.
The theorems import the education module and witness the unconstrained-input failure.
-/

open SnPresentation
open SnCarrier

/-- Unconstrained section lift accepting raw presentation terms, matching the pre-repair interface. -/
def unconstrainedSectionLift (stage : Nat) (p : SnPresentation) : SnPresentation :=
  match p with
  | .ground _ =>
    .lift ⟨stage, .glyphs []⟩
  | .supplied s =>
    .lift ⟨stage, .glyphs [s.mark]⟩
  | .relation (.pair p) =>
    .lift ⟨stage, .glyphs [p.first, p.second]⟩
  | .relation (.cut c) =>
    .lift ⟨stage, .arrow c.src c.tgt⟩
  | .relation (.simplex s) =>
    .lift ⟨stage, .pair s.v0 s.v1⟩
  | _ =>
    .lift ⟨stage, .glyphs []⟩

theorem refusal_token_round_trip_changes_input :
    retractionDownMap 0 (unconstrainedSectionLift 0 (.nonDescent ⟨()⟩)) =
      RetractOutcome.accepted (.ground ⟨()⟩) := by
  rfl

theorem refusal_token_not_recovered :
    retractionDownMap 0 (unconstrainedSectionLift 0 (.nonDescent ⟨()⟩)) ≠
      RetractOutcome.accepted (.nonDescent ⟨()⟩) := by
  rw [refusal_token_round_trip_changes_input]
  intro h
  injection h with hpayload
  injection hpayload

/-- The historical unconstrained carrier with an open higher constructor. -/
inductive UnrepairedCarrier : Nat → Type where
  | stage0 : Empty → UnrepairedCarrier 0
  | higher : (n : Nat) → Nat → UnrepairedCarrier n

theorem carrier_card_table_disagrees_with_higher :
    carrierCard 0 = 0 ∧ Nonempty (UnrepairedCarrier 0) :=
  ⟨rfl, ⟨UnrepairedCarrier.higher 0 0⟩⟩
