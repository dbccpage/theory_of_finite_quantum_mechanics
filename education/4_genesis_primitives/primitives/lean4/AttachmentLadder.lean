/-!
# Genesis Primitives Category 10: Attachment Ladder & Skeletal Filtration (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/Attachment.lean
- lean4/Derivation/LadderGeneral.lean

Classification: Genesis Foundation Substrate.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.AttachmentLadder

/-- A policy is lawful over `rounds` if every parent selection points to an already-represented parent. -/
def LawfulPolicy (pi : Nat → Nat) (rounds : Nat) : Prop :=
  ∀ k, k ≤ rounds → pi (k + 1) ≤ k

/-- Attachment outcome: either a successfully extended state or a typed refusal. -/
inductive AttachOutcome (α : Type) where
  | attached (next : α) : AttachOutcome α
  | refusedParent (p : Nat) (bound : Nat) : AttachOutcome α

/-- Occurrence order token vs position index. -/
structure AttachmentNode where
  token : Nat
  position : Nat
  parent_position : Nat
  parent_valid : parent_position < position

/-- One-edge Up-block: attaching a single node to parent `p`. -/
structure UpBlock (α : Type) where
  parent : Nat
  child : Nat
  lawful : parent < child
  apply : α → α

end GenesisPrimitives.AttachmentLadder
