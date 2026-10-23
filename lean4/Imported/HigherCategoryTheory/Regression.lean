/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/Regression.lean
   Original sha256: eb10852868d314ee3143ed9cd9e7374015e59de9fd94d0a203afadc0a4c90120 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Regression
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.HigherCategoryTheory.HigherNaturalTransformation
import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

/-- One object with the two-element group as its endomorphisms. -/
def boolCategory : Category Unit where
  Hom := fun _ _ => Bool
  id := fun _ => false
  comp := Bool.xor
  comp_assoc := by intros; rename_i f g h; cases f <;> cases g <;> cases h <;> rfl
  id_comp := by intros; rename_i f; cases f <;> rfl
  comp_id := by intros; rename_i f; cases f <;> rfl

/-- Objects associate strictly, but the two unitors are nonidentity automorphisms. -/
def twistedUnitMonoidal : MonoidalCategory Unit where
  cat := boolCategory
  tensorObj := fun _ _ => ()
  unit := ()
  tensorHom := Bool.xor
  tensorHom_id := by intros; rfl
  tensorHom_comp := by
    intros; rename_i f1 f2 g1 g2
    cases f1 <;> cases f2 <;> cases g1 <;> cases g2 <;> rfl
  associator := fun _ _ _ => ⟨false, false, rfl, rfl⟩
  leftUnitor := fun _ => ⟨true, true, rfl, rfl⟩
  rightUnitor := fun _ => ⟨true, true, rfl, rfl⟩
  associator_naturality := by
    intros; rename_i f g h; cases f <;> cases g <;> cases h <;> rfl
  leftUnitor_naturality := by intros; rename_i f; cases f <;> rfl
  rightUnitor_naturality := by intros; rename_i f; cases f <;> rfl
  pentagon := by intros; rfl
  triangle := by intros; rfl

abbrev regressionBicategory := twistedUnitMonoidal.toBicategory

theorem nonidentity_unitors_are_not_strict : ¬ regressionBicategory.IsStrict := by
  intro h
  obtain ⟨p, hp⟩ := h.2.1 (A := ()) (B' := ()) ()
  have bad : (true : Bool) = false := congrArg (fun i => i.hom) hp
  cases bad

/-- The identity maps can carry nonidentity pseudofunctor comparisons. -/
def twistedComparisons : Pseudofunctor regressionBicategory regressionBicategory where
  obj := id
  map1 := id
  map2 := id
  map2_id2 := by intros; rfl
  map2_vcomp := by intros; rfl
  compositor := fun _ _ => ⟨true, true, rfl, rfl⟩
  unitor := fun _ => ⟨true, true, rfl, rfl⟩
  compositor_naturality := by intros; rename_i α β; cases α <;> cases β <;> rfl
  associator_coherence := by intros; rfl
  leftUnitor_coherence := by intros; rfl
  rightUnitor_coherence := by intros; rfl

theorem nonidentity_functor_comparisons_are_not_strict : ¬ twistedComparisons.IsStrict := by
  intro h
  obtain ⟨p, hp⟩ := h.1 (A := ()) (B := ()) (C := ()) () ()
  have bad : (true : Bool) = false := congrArg (fun i => i.hom) hp
  cases bad

def twistedTransformation : PseudoNatTrans twistedComparisons (Pseudofunctor.id regressionBicategory) where
  comp1 := fun _ => ()
  comp2 := fun _ => ⟨true, true, rfl, rfl⟩
  naturality2 := by intros; rename_i α; cases α <;> rfl
  comp_coherence := by intros; rfl
  id_coherence := by intros; rfl

theorem nonidentity_transformation_comparisons_are_not_strict : ¬ twistedTransformation.IsStrict := by
  intro h
  obtain ⟨p, hp⟩ := h (A := ()) (B := ()) ()
  have bad : (true : Bool) = false := congrArg (fun i => i.hom) hp
  cases bad

end HigherCategoryTheory
