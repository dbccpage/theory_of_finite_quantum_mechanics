import Mathlib.CategoryTheory.Functor.Basic

/-! AuthorityEffect: None. Admitted total reversed typed arrows over an actual
Mathlib category carry involution, identity and reversed-composition laws.
Rust finite domain/boundary enumeration, budgets and storage are separate. -/
namespace TFQM.FiniteDagger
open CategoryTheory

structure Data (C : Type) [Category C] where
  map : ∀ {X Y : C}, (X ⟶ Y) → (Y ⟶ X)

variable {C : Type} [Category C]

def Involution (d : Data C) : Prop := ∀ {X Y : C} (f : X ⟶ Y), d.map (d.map f) = f
def Identity (d : Data C) : Prop := ∀ X : C, d.map (𝟙 X) = 𝟙 X
def Composition (d : Data C) : Prop :=
  ∀ {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ Z), d.map (f ≫ g) = d.map g ≫ d.map f

structure Laws (d : Data C) : Prop where
  involution : Involution d
  identity : Identity d
  composition : Composition d

noncomputable def checks (d : Data C) : List Bool := by
  classical
  exact [decide (Involution d), decide (Identity d), decide (Composition d)]

theorem checks_true_iff (d : Data C) : (checks d).all id = true ↔ Laws d := by
  classical
  constructor
  · intro h
    have parts : Involution d ∧ Identity d ∧ Composition d := by simpa [checks] using h
    exact ⟨parts.1, parts.2.1, parts.2.2⟩
  · rintro ⟨hi, he, hc⟩
    simp [checks, hi, he, hc]

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

structure Certified (C : Type) [Category C] where
  data : Data C
  laws : Laws data

noncomputable def certifiedOfAdmitted (d out : Data C) (guards : List Bool)
    (success : admit d guards = .ok out) : Certified C :=
  ⟨out, admit_success_laws d out guards success⟩

theorem certified_arrow (d out : Data C) (guards : List Bool)
    (success : admit d guards = .ok out) {X Y : C} (f : X ⟶ Y) :
    (certifiedOfAdmitted d out guards success).data.map f = out.map f := rfl

theorem dagger_involutive (d : Data C) (laws : Laws d) {X Y : C} (f : X ⟶ Y) :
    d.map (d.map f) = f := laws.involution f

theorem dagger_injective (d : Data C) (laws : Laws d) {X Y : C} (f g : X ⟶ Y)
    (h : d.map f = d.map g) : f = g := by
  have double := congrArg (fun k : Y ⟶ X => d.map k) h
  simpa only [laws.involution] using double

theorem dagger_surjective (d : Data C) (laws : Laws d) {X Y : C} (g : Y ⟶ X) :
    ∃ f : X ⟶ Y, d.map f = g := ⟨d.map g, laws.involution g⟩

theorem dagger_identity (d : Data C) (laws : Laws d) (X : C) :
    d.map (𝟙 X) = 𝟙 X := laws.identity X

theorem dagger_composition (d : Data C) (laws : Laws d) {X Y Z : C}
    (f : X ⟶ Y) (g : Y ⟶ Z) : d.map (f ≫ g) = d.map g ≫ d.map f := laws.composition f g

def Unitary (d : Data C) {X Y : C} (f : X ⟶ Y) : Prop :=
  f ≫ d.map f = 𝟙 X ∧ d.map f ≫ f = 𝟙 Y

theorem unitary_identity (d : Data C) (laws : Laws d) (X : C) : Unitary d (𝟙 X) := by
  simp [Unitary, laws.identity X]

theorem unitary_dagger (d : Data C) (laws : Laws d) {X Y : C} (f : X ⟶ Y)
    (h : Unitary d f) : Unitary d (d.map f) := by
  dsimp [Unitary] at *
  rw [laws.involution]
  exact ⟨h.2, h.1⟩

theorem unitary_composite (d : Data C) (laws : Laws d) {X Y Z : C}
    (f : X ⟶ Y) (g : Y ⟶ Z) (hf : Unitary d f) (hg : Unitary d g) :
    Unitary d (f ≫ g) := by
  constructor
  · calc
      (f ≫ g) ≫ d.map (f ≫ g) = f ≫ (g ≫ d.map g) ≫ d.map f := by
        rw [laws.composition]; simp only [Category.assoc]
      _ = 𝟙 X := by rw [hg.1, Category.id_comp, hf.1]
  · calc
      d.map (f ≫ g) ≫ (f ≫ g) = d.map g ≫ (d.map f ≫ f) ≫ g := by
        rw [laws.composition]; simp only [Category.assoc]
      _ = 𝟙 Z := by rw [hf.2, Category.id_comp, hg.2]

noncomputable def unitaryCheck (d : Data C) {X Y : C} (f : X ⟶ Y) : Bool := by
  classical
  exact decide (Unitary d f)

theorem unitary_check_iff (d : Data C) {X Y : C} (f : X ⟶ Y) :
    unitaryCheck d f = true ↔ Unitary d f := by classical; simp [unitaryCheck]

end TFQM.FiniteDagger

#print axioms TFQM.FiniteDagger.checks_true_iff
#print axioms TFQM.FiniteDagger.admit_preserves_data
#print axioms TFQM.FiniteDagger.admit_success_laws
#print axioms TFQM.FiniteDagger.failed_guard
#print axioms TFQM.FiniteDagger.certifiedOfAdmitted
#print axioms TFQM.FiniteDagger.certified_arrow
#print axioms TFQM.FiniteDagger.dagger_involutive
#print axioms TFQM.FiniteDagger.dagger_injective
#print axioms TFQM.FiniteDagger.dagger_surjective
#print axioms TFQM.FiniteDagger.dagger_identity
#print axioms TFQM.FiniteDagger.dagger_composition
#print axioms TFQM.FiniteDagger.unitary_identity
#print axioms TFQM.FiniteDagger.unitary_dagger
#print axioms TFQM.FiniteDagger.unitary_composite
#print axioms TFQM.FiniteDagger.unitary_check_iff
