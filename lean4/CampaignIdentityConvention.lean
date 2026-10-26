import Std

/- Observational identity depends on a declared observer family.
This is logical underdetermination, not a computability undecidability theorem. -/
namespace CampaignIdentityConvention

def Indistinguishable {I X V : Type} (obs : I → X → V) (x y : X) : Prop :=
  ∀ i, obs i x = obs i y

def IsNew {I X V : Type} (obs : I → X → V) (old supplied : X) : Prop :=
  ¬ Indistinguishable obs old supplied

theorem observational_equivalence {I X V : Type} (obs : I → X → V) :
    Equivalence (Indistinguishable obs) := by
  refine ⟨?_, ?_, ?_⟩
  · intro x i; rfl
  · intro x y h i; exact (h i).symm
  · intro x y z hxy hyz i; exact (hxy i).trans (hyz i)

theorem forgetting_preserves_indistinguishability {I J X V : Type}
    (obs : I → X → V) (keep : J → I) {x y : X}
    (h : Indistinguishable obs x y) :
    Indistinguishable (fun j => obs (keep j)) x y := fun j => h (keep j)

theorem empty_family_identifies_all {X V : Type} (obs : Empty → X → V) (x y : X) :
    Indistinguishable obs x y := by
  intro i
  cases i

def withIdentity {I X V : Type} (obs : I → X → V) : Sum I Unit → X → Sum V X
  | .inl i, x => .inl (obs i x)
  | .inr _, x => .inr x

theorem adding_identity_separates {I X V : Type} (obs : I → X → V) (x y : X) :
    Indistinguishable (withIdentity obs) x y ↔ x = y := by
  constructor
  · intro h; exact Sum.inr.inj (h (.inr ()))
  · intro h; subst y; intro i; rfl

def opaqueObserver {X : Type} : Empty → X → X := fun i => nomatch i

def exactObserver {X : Type} : Unit → X → X := fun _ => id

theorem exact_observer_sees_new : IsNew exactObserver false true := by
  intro h
  have impossible := h ()
  cases impossible

theorem opaque_observer_sees_no_new : ¬ IsNew opaqueObserver false true := by
  intro h
  exact h (empty_family_identifies_all opaqueObserver false true)

theorem exact_inscription_is_new : IsNew exactObserver "<>" "<a>" := by
  intro h
  exact (by decide : ("<>" : String) ≠ "<a>") (h ())

theorem opaque_inscription_is_not_new : ¬ IsNew opaqueObserver "<>" "<a>" := by
  intro h
  exact h (empty_family_identifies_all opaqueObserver "<>" "<a>")

theorem no_convention_independent_answer :
    ¬ ∃ answer : Prop, (answer ↔ IsNew exactObserver "<>" "<a>") ∧
      (answer ↔ IsNew opaqueObserver "<>" "<a>") := by
  rintro ⟨answer, hexact, hopaque⟩
  exact opaque_inscription_is_not_new (hopaque.mp (hexact.mpr exact_inscription_is_new))

#print axioms observational_equivalence
#print axioms forgetting_preserves_indistinguishability
#print axioms empty_family_identifies_all
#print axioms adding_identity_separates
#print axioms exact_observer_sees_new
#print axioms opaque_observer_sees_no_new
#print axioms exact_inscription_is_new
#print axioms opaque_inscription_is_not_new
#print axioms no_convention_independent_answer
end CampaignIdentityConvention
