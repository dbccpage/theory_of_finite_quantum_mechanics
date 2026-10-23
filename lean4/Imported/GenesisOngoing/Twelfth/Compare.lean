/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Twelfth/Compare.lean
   Original sha256: 0593cf42697a0a74d7271cec64b89a767ef3811b5df6930ac4d23d1f47bba83f (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Twelfth.Compare
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.Twelfth.Step

/-!
# What survives a kept identification record

Under C-M1 the record is computed from the identification, not a third
multiplicity.  The ninth's results, cost and reachability survive by the
identity on states (`Step12` as `Step9`).  The unchosen recorded tag has
results the ninth has not.
-/

namespace Seed.Twelfth

open Seed Seed.Ninth Seed.Eighth Seed.Eleventh NDSt

theorem fewest_changes12 {g : NDSt} (hgw : g.WF) :
    Reach12 empty9 g g.size ∧ ∀ n, Reach12 empty9 g n → g.size ≤ n :=
  fewest_changes9 hgw

theorem reach12_iff {s g : NDSt} (hs : s.WF) (hg : g.WF) :
    (∃ n, Reach12 s g n) ↔ (s.T.Nonempty → g.T.Nonempty) :=
  reach9_iff hs hg

theorem results_pair12 {m m' : Seed.Seventh.NSt} (hm : m.WF) (hm' : m'.WF)
    (hT : m'.T = m.T) :
    ∃ n, Reach12 empty9 ⟨m.T, fun q => match q with | false => m.M | true => m'.M⟩ n :=
  results_pair9 hm hm' hT

theorem no_third_rel (s : NDSt) :
    (s.proj false).M = s.M false ∧ (s.proj true).M = s.M true :=
  record_not_assertion s

theorem no_cross_constraint :
    LoopTag.xy ∈ recordRel twoBetween false 0 1 ∧
      recordRel twoBetween true 0 1 = ∅ :=
  r_record_not_s

theorem recorded_extra : Recorded.onePlain ≠ Recorded.oneIdent := by
  intro h
  have : false = true := congrArg Recorded.tagged h
  exact Bool.false_ne_true this

theorem recorded_cost_is_size (t : Recorded) : t.size = t.state.size := rfl

theorem toNDSt (s : NDSt) : s = s := rfl

end Seed.Twelfth
