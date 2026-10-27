/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 1efe9be44f77256fca6e71c645f232cbe859a832d80b46932e09a4a67e9f4b48 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Tenth.Rename
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.Tenth.Compare

/-!
# Exchange of the relations carries leftover

Plan target 4.  Size and the terms are unchanged by the exchange
(`size9_swap`, `NDSt.swap`), so leftover of an addition or a removal is
unchanged.  The identification case (restorability after swap) is the same
statement as `Step9.swap`; it is recorded in the paper rather than closed
here on the first attempt.
-/

namespace Seed.Tenth

open Seed Seed.Ninth Seed.Eighth NDSt

/-- The exchange keeps the size, so an addition still leaves nothing. -/
theorem leftover_swap_addTerm {s : NDSt} {u : ℕ} (hw : s.WF) (ht : u ∉ s.T) :
    leftoverOf s.swap (s.swap.addTerm u) = leftoverOf s (s.addTerm u) := by
  have hts : u ∉ s.swap.T := by simpa [NDSt.swap] using ht
  have hws : s.swap.WF := swap9_wf hw
  rw [leftover_addTerm hws hts, leftover_addTerm hw ht]

/-- The exchange keeps the terms, so a removal is still clearable. -/
theorem leftover_swap_remove {s : NDSt} (hw : s.WF) (q : Rel) (x y : ℕ)
    (hp : s.M q (x, y) ≠ 0) :
    leftoverOf s.swap (s.swap.remove (!q) x y) = leftoverOf s (s.remove q x y) := by
  have hps : s.swap.M (!q) (x, y) ≠ 0 := by
    simpa [NDSt.swap] using hp
  have hws : s.swap.WF := swap9_wf hw
  rw [leftover_remove hws (!q) x y hps, leftover_remove hw q x y hp]

end Seed.Tenth
