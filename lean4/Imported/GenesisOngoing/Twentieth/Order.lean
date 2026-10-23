/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Twentieth/Order.lean
   Original sha256: 896d39250d40cafc6981b9d2fec0bdedd51b2940906537bed73a823ea7520943 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Twentieth.Order
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.H3V7N5QF.Paths

/-!
# The round counts changes

Removing `arb` is one change and adds fewer assertions than it removes.
Reaching the one-term state takes a further identification. That state adds
still less, and it is reached later. The number of terms and assertions added
is not the round.
-/

namespace Seed.Twentieth

open Seed

/-- Terms and assertions added to what is given, as a difference of sizes. -/
def addedCount (s : St) : Int :=
  (s.T.card + s.A.card : Int) - (givenA.T.card + givenA.A.card : Int)

/-- What is given with `arb` removed. -/
def cleared : St := ⟨{0, 1}, ∅, 0, 1⟩

theorem remove_eq_cleared : givenA.remove (0, 1) = cleared := by decide

theorem cleared_step : Step givenA cleared :=
  remove_eq_cleared ▸ Step.remove givenA (0, 1) (by decide)

theorem reach_cleared : Reach givenA cleared 1 :=
  Reach.step (Reach.refl givenA) cleared_step

theorem added_oneTerm : addedCount oneTerm = -2 := by decide

theorem added_cleared : addedCount cleared = -1 := by decide

/-- Fewer additions, and more changes. -/
theorem additions_diverge :
    addedCount oneTerm < addedCount cleared ∧ Reach givenA cleared 1 ∧ Reach givenA oneTerm 2 := by
  refine ⟨?_, reach_cleared, givenA_to_oneTerm⟩
  rw [added_oneTerm, added_cleared]
  omega

end Seed.Twentieth
