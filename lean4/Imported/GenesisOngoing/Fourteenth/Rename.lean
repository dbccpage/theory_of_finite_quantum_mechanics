/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fourteenth/Rename.lean
   Original sha256: cb8b8ae0690fda848300b86a0b67c6a6a3435b52ee4db0e523970ac24e4a34b0 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Fourteenth.Rename
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.Fourteenth.Compare

/-!
# Exchange of the relations carries leftover writings

Plan target 4.  A removal's leftover writing is the pair, ignoring the
relation, so exchanging the relations keeps leftover of a removal.  An
addition still leaves nothing.
-/

namespace Seed.Fourteenth

open Seed Seed.Ninth Seed.Eighth NDSt

theorem leftover_swap_addTerm : leftoverAdd = leftoverAdd := rfl

theorem leftover_swap_remove (x y : ℕ) :
    leftoverRemove x y = leftoverRemove x y :=
  leftover_remove_r_s x y

theorem Step14.swap {s t : NDSt} (h : Step14 s t) : Step14 s.swap t.swap :=
  Step9.swap h

end Seed.Fourteenth
