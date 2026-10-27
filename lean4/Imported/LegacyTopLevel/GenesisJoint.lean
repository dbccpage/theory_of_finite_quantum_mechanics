/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 14809de9d1450d98c412b9ecdb908a292ea234e763115c86560d01e6b83aec01 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.GenesisJoint
   Reason         : genesis
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
import Std
/-! Coarsest sufficient refinement and the obstruction to joint decoding.
These generic statements do not supply a physical joint preparation relation. -/
namespace GenesisJoint
variable {X L R A B : Type}

def Refined (left : X → L) (right : X → R) (joint : X → A) (x y : X) : Prop :=
  left x = left y ∧ right x = right y ∧ joint x = joint y

theorem missing_distinction (left : X → L) (right : X → R) (joint : X → A)
    (x y : X) (hl : left x = left y) (hr : right x = right y)
    (hj : joint x ≠ joint y) :
    ¬ ∃ decode : L × R → A, ∀ z, decode (left z, right z) = joint z := by
  intro ⟨decode, h⟩
  apply hj
  calc
    joint x = decode (left x, right x) := (h x).symm
    _ = decode (left y, right y) := by rw [hl, hr]
    _ = joint y := h y

theorem coarsest_sufficient_refinement (left : X → L) (right : X → R)
    (joint : X → A) (report : X → B) (dl : B → L) (dr : B → R) (dj : B → A)
    (hl : ∀ x, dl (report x) = left x) (hr : ∀ x, dr (report x) = right x)
    (hj : ∀ x, dj (report x) = joint x) (x y : X) (h : report x = report y) :
    Refined left right joint x y := by
  exact ⟨(hl x).symm.trans ((congrArg dl h).trans (hl y)),
    (hr x).symm.trans ((congrArg dr h).trans (hr y)),
    (hj x).symm.trans ((congrArg dj h).trans (hj y))⟩

-- Local realizability has no implication of a common global alternative.
theorem local_green_global_red :
    (∃ x : Bool, x = false) ∧ (∃ x : Bool, x = true) ∧
    ¬ (∃ x : Bool, x = false ∧ x = true) := by
  refine ⟨⟨false, rfl⟩, ⟨true, rfl⟩, ?_⟩
  intro ⟨x, hx, hy⟩
  cases hx.symm.trans hy
#print axioms missing_distinction
#print axioms coarsest_sufficient_refinement
#print axioms local_green_global_red
end GenesisJoint
