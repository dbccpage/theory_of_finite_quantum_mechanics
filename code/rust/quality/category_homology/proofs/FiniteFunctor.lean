import Mathlib.CategoryTheory.Functor.Basic

/-! AuthorityEffect: None. Already admitted endpoint categories and typed total
maps model the Rust domain/image/boundary admission. Identity and composition
checks then produce an actual Mathlib functor. This is not Rust extraction,
finite string enumeration refinement, or a theorem about unchecked traits and
legacy supplied-name diagnostics. -/
namespace TFQM.FiniteFunctor
open CategoryTheory

structure Data (C D : Type) [Category C] [Category D] where
  obj : C → D
  map : ∀ {X Y : C}, (X ⟶ Y) → (obj X ⟶ obj Y)

variable {C D : Type} [Category C] [Category D]

def Identity (d : Data C D) : Prop := ∀ X, d.map (𝟙 X) = 𝟙 (d.obj X)
def Composition (d : Data C D) : Prop :=
  ∀ {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ Z), d.map (f ≫ g) = d.map f ≫ d.map g
structure Laws (d : Data C D) : Prop where
  identity : Identity d
  composition : Composition d

noncomputable def checks (d : Data C D) : List Bool := by
  classical
  exact [decide (Identity d), decide (Composition d)]

theorem checks_true_iff (d : Data C D) : (checks d).all id = true ↔ Laws d := by
  classical
  constructor
  · intro h
    have parts : Identity d ∧ Composition d := by simpa [checks] using h
    exact ⟨parts.1,parts.2⟩
  · rintro ⟨h₁,h₂⟩
    simp [checks,h₁,h₂]

noncomputable def admit (d : Data C D) (guards : List Bool) : Except Unit (Data C D) :=
  if (guards ++ checks d).all id then .ok d else .error ()

theorem admit_preserves_data (d out : Data C D) (guards : List Bool)
    (h : admit d guards = .ok out) : out = d := by
  unfold admit at h
  split at h
  · exact (Except.ok.inj h).symm
  · cases h

theorem admit_success_laws (d out : Data C D) (guards : List Bool)
    (h : admit d guards = .ok out) : Laws out := by
  have same := admit_preserves_data d out guards h
  subst out
  unfold admit at h
  split at h
  · rename_i all
    have parts : guards.all id = true ∧ (checks d).all id = true := by simpa using all
    exact (checks_true_iff d).mp parts.2
  · cases h

theorem failed_guard (d : Data C D) (before after : List Bool) :
    admit d (before ++ false :: after) = .error () := by simp [admit]

def functorOfLaws (d : Data C D) (laws : Laws d) : C ⥤ D where
  obj := d.obj
  map := d.map
  map_id := laws.identity
  map_comp := laws.composition

theorem functor_object (d : Data C D) (laws : Laws d) (X : C) :
    (functorOfLaws d laws).obj X = d.obj X := rfl
theorem functor_arrow (d : Data C D) (laws : Laws d) {X Y : C} (f : X ⟶ Y) :
    (functorOfLaws d laws).map f = d.map f := rfl
theorem functor_identity (d : Data C D) (laws : Laws d) (X : C) :
    (functorOfLaws d laws).map (𝟙 X) = 𝟙 (d.obj X) := laws.identity X
theorem functor_composition (d : Data C D) (laws : Laws d) {X Y Z : C}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (functorOfLaws d laws).map (f ≫ g) = d.map f ≫ d.map g := laws.composition f g

noncomputable def functorOfAdmitted (d out : Data C D) (guards : List Bool)
    (success : admit d guards = .ok out) : C ⥤ D :=
  functorOfLaws out (admit_success_laws d out guards success)

theorem admitted_object (d out : Data C D) (guards : List Bool)
    (success : admit d guards = .ok out) (X : C) :
    (functorOfAdmitted d out guards success).obj X = d.obj X := by
  have same := admit_preserves_data d out guards success
  subst out
  rfl

end TFQM.FiniteFunctor

#print axioms TFQM.FiniteFunctor.checks_true_iff
#print axioms TFQM.FiniteFunctor.admit_preserves_data
#print axioms TFQM.FiniteFunctor.admit_success_laws
#print axioms TFQM.FiniteFunctor.failed_guard
#print axioms TFQM.FiniteFunctor.functor_object
#print axioms TFQM.FiniteFunctor.functor_arrow
#print axioms TFQM.FiniteFunctor.functor_identity
#print axioms TFQM.FiniteFunctor.functor_composition
#print axioms TFQM.FiniteFunctor.functorOfAdmitted
#print axioms TFQM.FiniteFunctor.admitted_object
