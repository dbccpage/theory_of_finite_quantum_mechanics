import Mathlib.CategoryTheory.Groupoid

/-! AuthorityEffect: None. Admitted inverse equations realize an actual Mathlib
Groupoid. Chosen connectors give reversible isotropy coordinates and composition.
Finite source partition/minimum selection/bounds/storage are separate refinements;
no complex groupoid-algebra simplicity theorem or physical interpretation. -/
namespace TFQM.FiniteGroupoid
open CategoryTheory
variable {C : Type}

section Admission
variable [Category C]

structure Data (C : Type) [Category C] where
  inv : ∀ {X Y : C}, (X ⟶ Y) → (Y ⟶ X)
structure Laws (d : Data C) : Prop where
  left : ∀ {X Y : C} (f : X ⟶ Y), f ≫ d.inv f = 𝟙 X
  right : ∀ {X Y : C} (f : X ⟶ Y), d.inv f ≫ f = 𝟙 Y

noncomputable def checks (d : Data C) : List Bool := by
  classical
  exact [decide (∀ {X Y : C} (f : X ⟶ Y), f ≫ d.inv f = 𝟙 X),
    decide (∀ {X Y : C} (f : X ⟶ Y), d.inv f ≫ f = 𝟙 Y)]

theorem checks_true_iff (d : Data C) : (checks d).all id = true ↔ Laws d := by
  classical
  constructor
  · intro h
    have parts : (∀ {X Y : C} (f : X ⟶ Y), f ≫ d.inv f = 𝟙 X) ∧
        (∀ {X Y : C} (f : X ⟶ Y), d.inv f ≫ f = 𝟙 Y) := by simpa [checks] using h
    exact ⟨parts.1, parts.2⟩
  · rintro ⟨hl, hr⟩
    simp [checks, hl, hr]

noncomputable def admit (d : Data C) (guards : List Bool) : Except Unit (Data C) :=
  if (guards ++ checks d).all id then .ok d else .error ()

theorem admit_preserves_data (d out : Data C) (guards : List Bool)
    (h : admit d guards = .ok out) : out = d := by
  unfold admit at h
  split at h
  · exact (Except.ok.inj h).symm
  · cases h

theorem admit_success_laws (d out : Data C) (guards : List Bool)
    (h : admit d guards = .ok out) : Laws out := by
  have same := admit_preserves_data d out guards h
  subst out
  unfold admit at h
  split at h
  · rename_i all
    have parts : guards.all id = true ∧ (checks d).all id = true := by simpa using all
    exact (checks_true_iff d).mp parts.2
  · cases h

theorem failed_guard (d : Data C) (before after : List Bool) :
    admit d (before ++ false :: after) = .error () := by simp [admit]

@[instance_reducible]
def groupoidOfLaws (d : Data C) (laws : Laws d) : Groupoid C where
  toCategory := inferInstance
  inv := d.inv
  inv_comp := laws.right
  comp_inv := laws.left

theorem groupoid_inverse (d : Data C) (laws : Laws d) {X Y : C} (f : X ⟶ Y) :
    (groupoidOfLaws d laws).inv f = d.inv f := rfl

@[instance_reducible]
noncomputable def groupoidOfAdmitted (d out : Data C) (guards : List Bool)
    (success : admit d guards = .ok out) : Groupoid C :=
  groupoidOfLaws out (admit_success_laws d out guards success)
end Admission

section Coordinates
variable [Groupoid C]

theorem related_refl (X : C) : Nonempty (X ⟶ X) := ⟨𝟙 X⟩
theorem related_symm {X Y : C} (h : Nonempty (X ⟶ Y)) : Nonempty (Y ⟶ X) := by
  obtain ⟨f⟩ := h
  exact ⟨inv f⟩
theorem related_trans {X Y Z : C} (h : Nonempty (X ⟶ Y)) (k : Nonempty (Y ⟶ Z)) :
    Nonempty (X ⟶ Z) := by
  obtain ⟨f⟩ := h
  obtain ⟨g⟩ := k
  exact ⟨f ≫ g⟩

noncomputable def coordinate {R X Y : C} (px : R ⟶ X) (py : R ⟶ Y) (f : X ⟶ Y) : R ⟶ R :=
  px ≫ f ≫ inv py
noncomputable def reconstruct {R X Y : C} (px : R ⟶ X) (py : R ⟶ Y) (h : R ⟶ R) : X ⟶ Y :=
  inv px ≫ h ≫ py

theorem reconstruct_coordinate {R X Y : C} (px : R ⟶ X) (py : R ⟶ Y) (f : X ⟶ Y) :
    reconstruct px py (coordinate px py f) = f := by
  simp [coordinate, reconstruct, Category.assoc]

theorem coordinate_reconstruct {R X Y : C} (px : R ⟶ X) (py : R ⟶ Y) (h : R ⟶ R) :
    coordinate px py (reconstruct px py h) = h := by
  simp [coordinate, reconstruct, Category.assoc]

noncomputable def coordinateEquiv {R X Y : C} (px : R ⟶ X) (py : R ⟶ Y) :
    (X ⟶ Y) ≃ (R ⟶ R) where
  toFun := coordinate px py
  invFun := reconstruct px py
  left_inv := reconstruct_coordinate px py
  right_inv := coordinate_reconstruct px py

theorem coordinate_identity {R X : C} (px : R ⟶ X) : coordinate px px (𝟙 X) = 𝟙 R := by
  simp [coordinate]

theorem coordinate_composition {R X Y Z : C} (px : R ⟶ X) (py : R ⟶ Y) (pz : R ⟶ Z)
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    coordinate px pz (f ≫ g) = coordinate px py f ≫ coordinate py pz g := by
  simp [coordinate, Category.assoc]

theorem thin_from_root {R X Y : C} (px : R ⟶ X) (py : R ⟶ Y)
    (unique : Subsingleton (R ⟶ R)) (f g : X ⟶ Y) : f = g := by
  exact (coordinateEquiv px py).injective (@Subsingleton.elim (R ⟶ R) unique _ _)
end Coordinates

theorem removal_progress (before after : Nat) (nonempty : 0 < before)
    (removed : after ≤ before - 1) : after < before := by omega

theorem empty_not_connected_thin (isotropy : Nat) : ¬ (0 = 1 ∧ isotropy = 1) := by omega

end TFQM.FiniteGroupoid

#print axioms TFQM.FiniteGroupoid.checks_true_iff
#print axioms TFQM.FiniteGroupoid.admit_preserves_data
#print axioms TFQM.FiniteGroupoid.admit_success_laws
#print axioms TFQM.FiniteGroupoid.failed_guard
#print axioms TFQM.FiniteGroupoid.groupoidOfLaws
#print axioms TFQM.FiniteGroupoid.groupoid_inverse
#print axioms TFQM.FiniteGroupoid.groupoidOfAdmitted
#print axioms TFQM.FiniteGroupoid.related_refl
#print axioms TFQM.FiniteGroupoid.related_symm
#print axioms TFQM.FiniteGroupoid.related_trans
#print axioms TFQM.FiniteGroupoid.reconstruct_coordinate
#print axioms TFQM.FiniteGroupoid.coordinate_reconstruct
#print axioms TFQM.FiniteGroupoid.coordinateEquiv
#print axioms TFQM.FiniteGroupoid.coordinate_identity
#print axioms TFQM.FiniteGroupoid.coordinate_composition
#print axioms TFQM.FiniteGroupoid.thin_from_root
#print axioms TFQM.FiniteGroupoid.removal_progress
#print axioms TFQM.FiniteGroupoid.empty_not_connected_thin
