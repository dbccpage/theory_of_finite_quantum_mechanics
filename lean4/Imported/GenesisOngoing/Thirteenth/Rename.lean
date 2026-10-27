/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 23d369aa5dac0a17c34a3cf0c5138cdab1760d0a0ca1c6b399b85fe8e1cd7410 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Thirteenth.Rename
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.Thirteenth.Compare

/-!
# Exchange of the relations keeps the coarser writing

Plan target 4.  The coarser writing is the sum of the two multiplicities, so
exchanging the relations does not change it.  A change of the thirteenth seed
exchanges with the ninth's `Step9.swap`.
-/

namespace Seed.Thirteenth

open Seed Seed.Ninth Seed.Eighth NDSt

theorem Step13.swap {s t : NDSt} (h : Step13 s t) : Step13 s.swap t.swap :=
  Step9.swap h

theorem coarse_swap' (s : NDSt) : coarse s.swap = coarse s :=
  coarse_swap s

end Seed.Thirteenth
