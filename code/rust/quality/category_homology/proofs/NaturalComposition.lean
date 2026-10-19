import Mathlib.CategoryTheory.NatTrans

/-! AuthorityEffect: None. Actual natural transformations, whiskering and
horizontal path equality/interchange. Rust raw partial diagrams require their
own typed refusals; admitted outputs are rechecked by the finite constructor.
String storage/context normalization and compiler extraction are not proved. -/
namespace TFQM.NaturalComposition
open CategoryTheory
variable {B C D E : Type} [Category B] [Category C] [Category D] [Category E]
variable {F G J P : C ⥤ D} {H K L : D ⥤ E}

theorem identity_component (F : C ⥤ D) (X : C) : (NatTrans.id F).app X = 𝟙 (F.obj X) := rfl
theorem vertical_component (α : NatTrans F G) (β : NatTrans G J) (X : C) :
    (NatTrans.vcomp α β).app X = α.app X ≫ β.app X := rfl
theorem vertical_left_identity (α : NatTrans F G) : NatTrans.vcomp (NatTrans.id F) α = α := by
  ext X
  simp [NatTrans.vcomp]
theorem vertical_right_identity (α : NatTrans F G) : NatTrans.vcomp α (NatTrans.id G) = α := by
  ext X
  simp [NatTrans.vcomp]
theorem vertical_associative (α : NatTrans F G) (β : NatTrans G J) (γ : NatTrans J P) :
    NatTrans.vcomp (NatTrans.vcomp α β) γ = NatTrans.vcomp α (NatTrans.vcomp β γ) := by
  ext X
  simp [NatTrans.vcomp,Category.assoc]

def leftWhisker (α : NatTrans F G) (H : D ⥤ E) : NatTrans (F ⋙ H) (G ⋙ H) where
  app X := H.map (α.app X)
  naturality := by
    intro X Y f
    change H.map (F.map f) ≫ H.map (α.app Y) = H.map (α.app X) ≫ H.map (G.map f)
    rw [← H.map_comp, ← H.map_comp, α.naturality f]

def rightWhisker (α : NatTrans F G) (I : B ⥤ C) : NatTrans (I ⋙ F) (I ⋙ G) where
  app X := α.app (I.obj X)
  naturality := fun {_ _} f => α.naturality (I.map f)

theorem left_component (α : NatTrans F G) (H : D ⥤ E) (X : C) :
    (leftWhisker α H).app X = H.map (α.app X) := rfl
theorem right_component (α : NatTrans F G) (I : B ⥤ C) (X : B) :
    (rightWhisker α I).app X = α.app (I.obj X) := rfl
theorem left_preserves_vertical (α : NatTrans F G) (β : NatTrans G J) (H : D ⥤ E) :
    leftWhisker (NatTrans.vcomp α β) H = NatTrans.vcomp (leftWhisker α H) (leftWhisker β H) := by
  ext X
  exact H.map_comp (α.app X) (β.app X)
theorem right_preserves_vertical (α : NatTrans F G) (β : NatTrans G J) (I : B ⥤ C) :
    rightWhisker (NatTrans.vcomp α β) I = NatTrans.vcomp (rightWhisker α I) (rightWhisker β I) := rfl

def horizontal (α : NatTrans F G) (β : NatTrans H K) : NatTrans (F ⋙ H) (G ⋙ K) :=
  NatTrans.vcomp (leftWhisker α H) (rightWhisker β G)

theorem horizontal_component (α : NatTrans F G) (β : NatTrans H K) (X : C) :
    (horizontal α β).app X = H.map (α.app X) ≫ β.app (G.obj X) := rfl
theorem horizontal_paths (α : NatTrans F G) (β : NatTrans H K) (X : C) :
    H.map (α.app X) ≫ β.app (G.obj X) = β.app (F.obj X) ≫ K.map (α.app X) :=
  β.naturality (α.app X)
theorem horizontal_other_path (α : NatTrans F G) (β : NatTrans H K) :
    horizontal α β = NatTrans.vcomp (rightWhisker β F) (leftWhisker α K) := by
  ext X
  exact β.naturality (α.app X)
theorem horizontal_naturality (α : NatTrans F G) (β : NatTrans H K) {X Y : C} (f : X ⟶ Y) :
    (F ⋙ H).map f ≫ (horizontal α β).app Y = (horizontal α β).app X ≫ (G ⋙ K).map f :=
  (horizontal α β).naturality f
theorem horizontal_identity (F : C ⥤ D) (H : D ⥤ E) :
    horizontal (NatTrans.id F) (NatTrans.id H) = NatTrans.id (F ⋙ H) := by
  ext X
  change H.map (𝟙 (F.obj X)) ≫ 𝟙 (H.obj (F.obj X)) = 𝟙 (H.obj (F.obj X))
  simp
theorem interchange (α : NatTrans F G) (α' : NatTrans G J) (β : NatTrans H K) (β' : NatTrans K L) :
    horizontal (NatTrans.vcomp α α') (NatTrans.vcomp β β') =
      NatTrans.vcomp (horizontal α β) (horizontal α' β') := by
  ext X
  change H.map (α.app X ≫ α'.app X) ≫ (β.app (J.obj X) ≫ β'.app (J.obj X)) =
    (H.map (α.app X) ≫ β.app (G.obj X)) ≫ (K.map (α'.app X) ≫ β'.app (J.obj X))
  rw [H.map_comp]
  simp only [Category.assoc]
  rw [← Category.assoc (H.map (α'.app X)), β.naturality (α'.app X)]
  simp only [Category.assoc]

end TFQM.NaturalComposition
#print axioms TFQM.NaturalComposition.identity_component
#print axioms TFQM.NaturalComposition.vertical_component
#print axioms TFQM.NaturalComposition.vertical_left_identity
#print axioms TFQM.NaturalComposition.vertical_right_identity
#print axioms TFQM.NaturalComposition.vertical_associative
#print axioms TFQM.NaturalComposition.left_component
#print axioms TFQM.NaturalComposition.right_component
#print axioms TFQM.NaturalComposition.left_preserves_vertical
#print axioms TFQM.NaturalComposition.right_preserves_vertical
#print axioms TFQM.NaturalComposition.horizontal_component
#print axioms TFQM.NaturalComposition.horizontal_paths
#print axioms TFQM.NaturalComposition.horizontal_other_path
#print axioms TFQM.NaturalComposition.horizontal_naturality
#print axioms TFQM.NaturalComposition.horizontal_identity
#print axioms TFQM.NaturalComposition.interchange
