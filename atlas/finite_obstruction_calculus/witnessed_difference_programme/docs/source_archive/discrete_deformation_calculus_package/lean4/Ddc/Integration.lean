/-
Letter I: integration commits a receipt and changes nothing else. AuthorityEffect: None.
-/
import Ddc.Theorems

namespace Ddc

/-- Law 5: I needs a receipt and leaves the state unchanged. -/
theorem I_needs_receipt (b a : State) (w : Witness) (h : stepLaw .I b a w = true) :
    a = b ∧ w.receipt = true := law_I.1 h

/-- DDC-I-01: appending one receipt keeps the old tape as a prefix. -/
theorem I_commit_prefix {α : Type} (tape : List α) (r : α) : tape <+: tape ++ [r] :=
  List.prefix_append tape [r]

/-- DDC-I-01 for replays: the receipts of a tape are a prefix of the receipts of any extension. -/
theorem I_receipts_prefix (t₁ t₂ : List Step) (i : Nat) (c : Control) (s : State) :
    receipts i c s t₁ <+: receipts i c s (t₁ ++ t₂) := by
  obtain ⟨rest, h⟩ := receipts_prefix t₁ t₂ i c s
  exact ⟨rest, h.symm⟩

end Ddc
