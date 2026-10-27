/- Imported so that this repository carries its own Lean evidence.
   Original sha256: c1cca5e359a1bac06fdaf525650f8d44f460dc36cde0206a63ee0582a7212dee (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.GenesisBellCertificate
   Reason         : genesis
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
import Std
/-! Soundness of a finite weighted-inequality obstruction over integers.
Exact rational certificates can be scaled to this form by positive common
denominators. That scaling and the Rust simplex search are not formalized here. -/
namespace GenesisBellCertificate
structure Row where
  weight : Int
  lhs : Int
  rhs : Int

def leftSum : List Row → Int
  | [] => 0
  | r :: rs => r.weight * r.lhs + leftSum rs

def rightSum : List Row → Int
  | [] => 0
  | r :: rs => r.weight * r.rhs + rightSum rs

theorem weighted_inequalities (rows : List Row)
    (valid : ∀ r ∈ rows, 0 ≤ r.weight ∧ r.lhs ≤ r.rhs) :
    leftSum rows ≤ rightSum rows := by
  induction rows with
  | nil => exact Int.le_refl 0
  | cons r rs ih =>
    have hr := valid r (by simp)
    have ht := ih (fun s hs => valid s (by simp [hs]))
    exact Int.add_le_add (Int.mul_le_mul_of_nonneg_left hr.2 hr.1) ht

theorem obstruction_no_feasible_rows (rows : List Row)
    (positive : ∀ r ∈ rows, 0 ≤ r.weight)
    (cancels : leftSum rows = 0) (negative : rightSum rows < 0) :
    ¬ (∀ r ∈ rows, r.lhs ≤ r.rhs) := by
  intro feasible
  have h := weighted_inequalities rows (fun r hr => ⟨positive r hr, feasible r hr⟩)
  rw [cancels] at h
  omega
#print axioms weighted_inequalities
#print axioms obstruction_no_feasible_rows
end GenesisBellCertificate
