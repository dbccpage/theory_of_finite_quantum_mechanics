/-!
# A scoped prerequisite for reflective refinement

These elementary set-level results isolate the precise obstruction to
factoring a map through a surjective refinement. They do not assert that a
minimal constructor refinement exists, preserves contextual congruence, or
defines a reflector. In particular, they do not close WDP-CH04-O01 and make
no identification with HoTT or higher categorical initiality.

The explicit section version is constructive. The surjective version uses
only Lean's standard classical choice principle. No mathematical axioms or
admitted proofs are introduced.
-/

namespace WitnessedDifference.RefinementFactorization

universe u v w

/-- A map must identify every pair identified by the proposed refinement. -/
def RespectsKernel {A : Type u} {B : Type v} {M : Type w}
    (eta : A → B) (f : A → M) : Prop :=
  ∀ x y, eta x = eta y → f x = f y

/-- Any factorization entails kernel compatibility, without surjectivity. -/
theorem factorization_requires_kernel {A : Type u} {B : Type v} {M : Type w}
    (eta : A → B) (f : A → M) (g : B → M)
    (h : ∀ x, g (eta x) = f x) : RespectsKernel eta f := by
  intro x y hxy
  calc
    f x = g (eta x) := (h x).symm
    _ = g (eta y) := congrArg g hxy
    _ = f y := h y

/-- An explicit section and kernel compatibility give a unique factor. -/
theorem section_factorization {A : Type u} {B : Type v} {M : Type w}
    (eta : A → B) (f : A → M) (sect : B → A)
    (hsection : ∀ y, eta (sect y) = y)
    (hkernel : RespectsKernel eta f) :
    ∃ g : B → M, (∀ x, g (eta x) = f x) ∧
      (∀ k : B → M, (∀ x, k (eta x) = f x) → k = g) := by
  refine ⟨fun y => f (sect y), ?_, ?_⟩
  · intro x
    exact hkernel (sect (eta x)) x (hsection (eta x))
  · intro k hk
    funext y
    calc
      k y = k (eta (sect y)) := congrArg k (hsection y).symm
      _ = f (sect y) := hk (sect y)

/-- For a surjective refinement, kernel compatibility is necessary and
sufficient for unique set-level factorization. -/
theorem surjective_factorization_iff {A : Type u} {B : Type v} {M : Type w}
    (eta : A → B) (f : A → M)
    (hsurj : ∀ y, ∃ x, eta x = y) :
    (∃ g : B → M, (∀ x, g (eta x) = f x) ∧
      (∀ k : B → M, (∀ x, k (eta x) = f x) → k = g)) ↔
      RespectsKernel eta f := by
  constructor
  · intro h
    obtain ⟨g, hg, _⟩ := h
    exact factorization_requires_kernel eta f g hg
  · intro hkernel
    exact section_factorization eta f
      (fun y => Classical.choose (hsurj y))
      (fun y => Classical.choose_spec (hsurj y)) hkernel

/-- A single separated pair in one refinement fiber refutes factorization. -/
theorem separated_fiber_refutes_factorization
    {A : Type u} {B : Type v} {M : Type w}
    (eta : A → B) (f : A → M) (x y : A)
    (hidentified : eta x = eta y) (hseparated : f x ≠ f y) :
    ¬ ∃ g : B → M, ∀ a, g (eta a) = f a := by
  intro h
  obtain ⟨g, hg⟩ := h
  exact hseparated (factorization_requires_kernel eta f g hg x y hidentified)

/-- The surjection collapsing two points has no factorization of identity. -/
theorem collapsed_bool_identity_does_not_factor :
    ¬ ∃ g : Unit → Bool, ∀ b : Bool, g () = b := by
  intro h
  obtain ⟨g, hg⟩ := h
  have hfalse := hg false
  have htrue := hg true
  have impossible : false = true := hfalse.symm.trans htrue
  cases impossible

/-- A contextual system with an explicitly declared profile relation. -/
structure ContextSystem (A : Type u) (C : Type v) where
  sameProfile : A → A → Prop
  action : C → A → A

/-- Morphisms must preserve profiles and commute with every context action. -/
structure ContextHom {A B : Type u} {C : Type v}
    (S : ContextSystem A C) (T : ContextSystem B C) where
  toFun : A → B
  preservesProfile : ∀ x y, S.sameProfile x y → T.sameProfile (toFun x) (toFun y)
  intertwines : ∀ c x, toFun (S.action c x) = T.action c (toFun x)

/-- Context congruence is preservation of the declared profile relation. -/
def ContextCongruent {A : Type u} {C : Type v} (S : ContextSystem A C) : Prop :=
  ∀ c x y, S.sameProfile x y → S.sameProfile (S.action c x) (S.action c y)

/-- A profile-reflecting morphism into a congruent system forces its source
already to be congruent. Thus profile reflection cannot be silently imposed
on the unit of a completion intended to repair a noncongruent system. -/
theorem reflecting_unit_requires_source_congruence
    {A B : Type u} {C : Type v}
    {S : ContextSystem A C} {T : ContextSystem B C}
    (eta : ContextHom S T)
    (hreflect : ∀ x y, T.sameProfile (eta.toFun x) (eta.toFun y) →
      S.sameProfile x y)
    (hcomplete : ContextCongruent T) : ContextCongruent S := by
  intro c x y hxy
  apply hreflect (S.action c x) (S.action c y)
  rw [eta.intertwines c x, eta.intertwines c y]
  exact hcomplete c (eta.toFun x) (eta.toFun y) (eta.preservesProfile x y hxy)

/-- Profile reflection together with the set-level hypotheses suffices for
unique factorization as contextual morphisms. Context intertwining follows from
the unit being a morphism; it is not a separate unverified assumption.
Uniqueness is stated on underlying maps, hence does not depend on proof fields. -/
theorem contextual_factorization
    {A B M : Type u} {C : Type v}
    {S : ContextSystem A C} {T : ContextSystem B C} {N : ContextSystem M C}
    (eta : ContextHom S T) (f : ContextHom S N)
    (hsurj : ∀ y, ∃ x, eta.toFun x = y)
    (hkernel : RespectsKernel eta.toFun f.toFun)
    (hreflect : ∀ x y, T.sameProfile (eta.toFun x) (eta.toFun y) →
      S.sameProfile x y) :
    ∃ g : ContextHom T N, (∀ x, g.toFun (eta.toFun x) = f.toFun x) ∧
      (∀ k : ContextHom T N,
        (∀ x, k.toFun (eta.toFun x) = f.toFun x) → k.toFun = g.toFun) := by
  obtain ⟨g, hg, huniq⟩ := (surjective_factorization_iff eta.toFun f.toFun hsurj).mpr hkernel
  have hprofile : ∀ x y, T.sameProfile x y → N.sameProfile (g x) (g y) := by
    intro x y hxy
    obtain ⟨a, ha⟩ := hsurj x
    obtain ⟨b, hb⟩ := hsurj y
    subst x
    subst y
    rw [hg a, hg b]
    exact f.preservesProfile a b (hreflect a b hxy)
  have haction : ∀ c y, g (T.action c y) = N.action c (g y) := by
    intro c y
    obtain ⟨x, hx⟩ := hsurj y
    subst y
    rw [← eta.intertwines c x, hg (S.action c x), hg x]
    exact f.intertwines c x
  refine ⟨⟨g, hprofile, haction⟩, hg, ?_⟩
  intro k hk
  exact huniq k.toFun hk

end WitnessedDifference.RefinementFactorization

#print axioms WitnessedDifference.RefinementFactorization.factorization_requires_kernel
#print axioms WitnessedDifference.RefinementFactorization.section_factorization
#print axioms WitnessedDifference.RefinementFactorization.surjective_factorization_iff
#print axioms WitnessedDifference.RefinementFactorization.separated_fiber_refutes_factorization
#print axioms WitnessedDifference.RefinementFactorization.collapsed_bool_identity_does_not_factor
#print axioms WitnessedDifference.RefinementFactorization.contextual_factorization
#print axioms WitnessedDifference.RefinementFactorization.reflecting_unit_requires_source_congruence
