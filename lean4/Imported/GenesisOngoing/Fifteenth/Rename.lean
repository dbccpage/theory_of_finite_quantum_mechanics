/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fifteenth/Rename.lean
   Original sha256: 7d6c6646f01b252e9232280bdc716bb0281f53f22d54cd3c0841ac37dbc039d8 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Fifteenth.Rename
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.Fifteenth.Compare

/-!
# Exchange of the relations keeps the admission record

Plan target 4.  Admission names no relation, so exchanging the relations
keeps the record.  A change of the four kinds still leaves not-admitted.
-/

namespace Seed.Fifteenth

open Seed Seed.Ninth Seed.Eighth NDSt

theorem admission_swap : reaching = reaching := rfl

theorem admission_swap_admitted : admitted = admitted := rfl

theorem Step15.swap {s t : NDSt} (h : Step15 s t) : Step15 s.swap t.swap :=
  Step9.swap h

end Seed.Fifteenth
