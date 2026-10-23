/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Twelfth/Rename.lean
   Original sha256: fe2348a5f3140745650c1067000dc2709a99e82dfc129501d803d86d0eacc415 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Twelfth.Rename
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.Twelfth.Compare

/-!
# Exchange of the relations carries identification records

Plan target 4.  The terms are unchanged by the exchange (`swap9_T`), so the
2×2 block of one relation on `s` is the 2×2 block of the other relation on
`s.swap`.
-/

namespace Seed.Twelfth

open Seed Seed.Ninth Seed.Eighth NDSt

theorem recordRel_swap (s : NDSt) (q : Rel) (u v : ℕ) :
    recordRel s.swap q u v = recordRel s (!q) u v := by
  unfold recordRel NDSt.swap
  rfl

theorem recordOf_swap (s : NDSt) (u v : ℕ) :
    recordOf s.swap u v = ⟨(recordOf s u v).s, (recordOf s u v).r⟩ := by
  simp [recordOf, recordRel_swap]

theorem Step12.swap {s t : NDSt} (h : Step12 s t) : Step12 s.swap t.swap :=
  Step9.swap h

end Seed.Twelfth
