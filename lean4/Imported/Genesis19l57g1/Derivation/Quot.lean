/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Quot.lean
   Original sha256: 0d1df5e6ef985f48a1689ecadfe76c3c6c54d64ee7e07950fb1abc08a4956203 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.Genesis19l57g1.Derivation.Quot
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.Genesis19l57g1.Derivation.Basic
import Imported.Genesis19l57g1.Derivation.Inertia

/-!
# The abstraction barrier

If a current abstraction identifies two cases, no operation defined only on
that abstraction can recover the distinction: every function out of the
quotient is constant on identified elements.  This answers the required
question about recovering distinctions from an identifying abstraction.
-/

namespace Derivation

/-- Operations defined only on a quotient cannot separate identified
elements. -/
theorem quotient_barrier {α : Sort u} {β : Sort v} (s : Setoid α)
    (f : Quotient s → β) {a b : α} (h : a ≈ b) :
    f (Quotient.mk s a) = f (Quotient.mk s b) :=
  congrArg f (Quotient.sound h)

/-- The same barrier for raw quotients by an arbitrary relation. -/
theorem quot_barrier {α : Sort u} {β : Sort v} (rel : α → α → Prop)
    (f : Quot rel → β) {a b : α} (h : rel a b) :
    f (Quot.mk rel a) = f (Quot.mk rel b) :=
  congrArg f (Quot.sound h)

/-- Instantiation to the derivation: identify observationally collapsed
data of a fixed regime; any operation defined on the collapse classes gives
equal outputs on `<a>` and `<ab>` in the Challenge 2/3 regime. -/
def collapseRel (r : Regime) (d d' : Nat) : Prop := collapsed r d d'

theorem barrier_R2L {β : Sort v} (f : Quot (collapseRel R2L) → β) :
    f (Quot.mk _ 0) = f (Quot.mk _ 1) :=
  quot_barrier (collapseRel R2L) f R2L_collapsed

end Derivation
