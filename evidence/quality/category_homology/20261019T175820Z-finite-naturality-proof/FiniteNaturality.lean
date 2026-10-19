import Mathlib.CategoryTheory.NatTrans

/-! AuthorityEffect: None. Already admitted endpoint categories/functors and
typed total components model the Rust context/domain/boundary checks. Exact
naturality admission then realizes an actual Mathlib NatTrans. String storage,
finite enumeration/formatting and Rust extraction remain separate boundaries. -/
namespace TFQM.FiniteNaturality
open CategoryTheory
variable {C D : Type} [Category C] [Category D]

abbrev Components (F G : C ⥤ D) := ∀ X, F.obj X ⟶ G.obj X
structure Natural (F G : C ⥤ D) (app : Components F G) : Prop where
  square : ∀ {X Y : C} (f : X ⟶ Y), F.map f ≫ app Y = app X ≫ G.map f

noncomputable def checks (F G : C ⥤ D) (app : Components F G) : List Bool := by
  classical
  exact [decide (Natural F G app)]
theorem checks_true_iff (F G : C ⥤ D) (app : Components F G) :
    (checks F G app).all id = true ↔ Natural F G app := by
  classical
  simp [checks]

noncomputable def admit (F G : C ⥤ D) (app : Components F G) (guards : List Bool) :
    Except Unit (Components F G) :=
  if (guards ++ checks F G app).all id then .ok app else .error ()

theorem admit_preserves_data (F G : C ⥤ D) (app out : Components F G) (guards : List Bool)
    (h : admit F G app guards = .ok out) : out = app := by
  unfold admit at h
  split at h
  · exact (Except.ok.inj h).symm
  · cases h
theorem admit_success (F G : C ⥤ D) (app out : Components F G) (guards : List Bool)
    (h : admit F G app guards = .ok out) : Natural F G out := by
  have same := admit_preserves_data F G app out guards h
  subst out
  unfold admit at h
  split at h
  · rename_i all
    have parts : guards.all id = true ∧ (checks F G app).all id = true := by simpa using all
    exact (checks_true_iff F G app).mp parts.2
  · cases h
theorem failed_guard (F G : C ⥤ D) (app : Components F G) (before after : List Bool) :
    admit F G app (before ++ false :: after) = .error () := by simp [admit]

def natTransOfLaws (F G : C ⥤ D) (app : Components F G) (laws : Natural F G app) : NatTrans F G where
  app := app
  naturality := fun {_ _} f => laws.square f
theorem natTrans_app (F G : C ⥤ D) (app : Components F G) (laws : Natural F G app) (X : C) :
    (natTransOfLaws F G app laws).app X = app X := rfl
theorem natTrans_naturality (F G : C ⥤ D) (app : Components F G) (laws : Natural F G app)
    {X Y : C} (f : X ⟶ Y) :
    F.map f ≫ (natTransOfLaws F G app laws).app Y = (natTransOfLaws F G app laws).app X ≫ G.map f := laws.square f
noncomputable def natTransOfAdmitted (F G : C ⥤ D) (app out : Components F G) (guards : List Bool)
    (success : admit F G app guards = .ok out) : NatTrans F G :=
  natTransOfLaws F G out (admit_success F G app out guards success)
theorem admitted_component (F G : C ⥤ D) (app out : Components F G) (guards : List Bool)
    (success : admit F G app guards = .ok out) (X : C) :
    (natTransOfAdmitted F G app out guards success).app X = app X := by
  have same := admit_preserves_data F G app out guards success
  subst out
  rfl

end TFQM.FiniteNaturality
#print axioms TFQM.FiniteNaturality.checks_true_iff
#print axioms TFQM.FiniteNaturality.admit_preserves_data
#print axioms TFQM.FiniteNaturality.admit_success
#print axioms TFQM.FiniteNaturality.failed_guard
#print axioms TFQM.FiniteNaturality.natTrans_app
#print axioms TFQM.FiniteNaturality.natTrans_naturality
#print axioms TFQM.FiniteNaturality.natTransOfAdmitted
#print axioms TFQM.FiniteNaturality.admitted_component
