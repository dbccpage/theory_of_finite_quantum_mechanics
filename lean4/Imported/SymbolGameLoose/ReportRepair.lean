/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/ReportRepair.lean
   Original sha256: 3e39d6f5189eb6e51e0508dac32c441ee0543560670ff5547a90db54ceca4e80 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.ReportRepair
   Reason         : WDP
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Std
/-! One witnessed report-class split. These three local laws do not formalize
the Rust search, resource accounting or the finite class-count termination bound.
The full-answer refinement property is already in GenesisJoint.lean. -/
namespace ReportRepair
variable {X R A : Type} [DecidableEq R]

def split (report : X → R) (answer : X → A) (selected : R) (x : X) : R × Option A :=
  (report x, if report x = selected then some (answer x) else none)

theorem retains_report (report : X → R) (answer : X → A) (selected : R)
    (x y : X) (h : split report answer selected x = split report answer selected y) :
    report x = report y := by
  exact congrArg Prod.fst h

theorem no_unnecessary_distinction (report : X → R) (answer : X → A) (selected : R)
    (x y : X) (hr : report x = report y) (ha : answer x = answer y) :
    split report answer selected x = split report answer selected y := by
  simp only [split, hr, ha]

theorem separates_witness (report : X → R) (answer : X → A) (x y : X)
    (hr : report x = report y) (ha : answer x ≠ answer y) :
    split report answer (report x) x ≠ split report answer (report x) y := by
  intro equal
  have values := congrArg Prod.snd equal
  simp [split, hr] at values
  exact ha values

#print axioms retains_report
#print axioms no_unnecessary_distinction
#print axioms separates_witness
end ReportRepair
