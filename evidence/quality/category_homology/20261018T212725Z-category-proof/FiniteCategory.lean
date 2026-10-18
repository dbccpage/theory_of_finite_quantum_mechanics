import Mathlib.CategoryTheory.Category.Basic

/-!
AuthorityEffect: None.

Finite category admission model. Object and arrow identifiers here are already
admitted finite domains. The Rust key/name, endpoint, identity-totality and
closure checks justify that representation; extra guards model their refusals.
This file proves that accepted tables realize an actual Mathlib category. It
does not establish mechanized refinement of Rust storage, binary search, MIR,
allocation behavior or the diagnostic text. Those boundaries need source review.
-/

namespace TFQM.FiniteCategory

structure Data (n m : ℕ) where
  source : Fin m → Fin n
  target : Fin m → Fin n
  identity : Fin n → Fin m
  compose : Fin m → Fin m → Option (Fin m)

def IdentityBoundary {n m} (d : Data n m) : Prop :=
  ∀ x, d.source (d.identity x) = x ∧ d.target (d.identity x) = x

def CompositionDomain {n m} (d : Data n m) : Prop :=
  ∀ f g, (∃ h, d.compose f g = some h) ↔ d.target f = d.source g

def CompositionBoundary {n m} (d : Data n m) : Prop :=
  ∀ f g h, d.compose f g = some h →
    d.source h = d.source f ∧ d.target h = d.target g

def LeftUnit {n m} (d : Data n m) : Prop :=
  ∀ f, d.compose (d.identity (d.source f)) f = some f

def RightUnit {n m} (d : Data n m) : Prop :=
  ∀ f, d.compose f (d.identity (d.target f)) = some f

def Associative {n m} (d : Data n m) : Prop :=
  ∀ f g h, d.target f = d.source g → d.target g = d.source h →
    (d.compose f g).bind (fun fg => d.compose fg h) =
      (d.compose g h).bind (fun gh => d.compose f gh)

structure Laws {n m} (d : Data n m) : Prop where
  identityBoundary : IdentityBoundary d
  compositionDomain : CompositionDomain d
  compositionBoundary : CompositionBoundary d
  leftUnit : LeftUnit d
  rightUnit : RightUnit d
  associative : Associative d

noncomputable def checks {n m} (d : Data n m) : List Bool := by
  classical
  exact [decide (IdentityBoundary d), decide (CompositionDomain d),
    decide (CompositionBoundary d), decide (LeftUnit d),
    decide (RightUnit d), decide (Associative d)]

theorem checks_true_iff {n m} (d : Data n m) :
    (checks d).all id = true ↔ Laws d := by
  classical
  constructor
  · intro h
    have parts : IdentityBoundary d ∧ CompositionDomain d ∧
        CompositionBoundary d ∧ LeftUnit d ∧ RightUnit d ∧ Associative d := by
      simpa [checks] using h
    exact ⟨parts.1, parts.2.1, parts.2.2.1, parts.2.2.2.1,
      parts.2.2.2.2.1, parts.2.2.2.2.2⟩
  · rintro ⟨h₁, h₂, h₃, h₄, h₅, h₆⟩
    simp [checks, h₁, h₂, h₃, h₄, h₅, h₆]

/-- Success returns raw data, not a type that assumes the desired laws. -/
noncomputable def admit {n m} (d : Data n m) (guards : List Bool) :
    Except Unit (Data n m) :=
  if (guards ++ checks d).all id then .ok d else .error ()

theorem admit_preserves_data {n m} (d out : Data n m) (guards : List Bool)
    (success : admit d guards = .ok out) : out = d := by
  unfold admit at success
  split at success
  · exact (Except.ok.inj success).symm
  · cases success

theorem admit_success_laws {n m} (d out : Data n m) (guards : List Bool)
    (success : admit d guards = .ok out) : Laws out := by
  have same := admit_preserves_data d out guards success
  subst out
  unfold admit at success
  split at success
  · rename_i all
    have parts : guards.all id = true ∧ (checks d).all id = true := by
      simpa using all
    exact (checks_true_iff d).mp parts.2
  · cases success

theorem failed_guard {n m} (d : Data n m) (before after : List Bool) :
    admit d (before ++ false :: after) = .error () := by
  simp [admit]

def Arrow {n m} (d : Data n m) (x y : Fin n) :=
  {f : Fin m // d.source f = x ∧ d.target f = y}

noncomputable def composite {n m} (d : Data n m) (laws : Laws d)
    (f g : Fin m) (compatible : d.target f = d.source g) : Fin m :=
  Classical.choose ((laws.compositionDomain f g).mpr compatible)

theorem composite_spec {n m} (d : Data n m) (laws : Laws d)
    (f g : Fin m) (compatible : d.target f = d.source g) :
    d.compose f g = some (composite d laws f g compatible) :=
  Classical.choose_spec ((laws.compositionDomain f g).mpr compatible)

def identityArrow {n m} (d : Data n m) (laws : Laws d) (x : Fin n) : Arrow d x x :=
  ⟨d.identity x, laws.identityBoundary x⟩

noncomputable def composeArrow {n m} (d : Data n m) (laws : Laws d)
    {x y z : Fin n} (f : Arrow d x y) (g : Arrow d y z) : Arrow d x z := by
  let compatible := f.property.2.trans g.property.1.symm
  let value := composite d laws f.val g.val compatible
  have bounds := laws.compositionBoundary f.val g.val value
    (composite_spec d laws f.val g.val compatible)
  exact ⟨value, bounds.1.trans f.property.1, bounds.2.trans g.property.2⟩

theorem composeArrow_spec {n m} (d : Data n m) (laws : Laws d)
    {x y z : Fin n} (f : Arrow d x y) (g : Arrow d y z) :
    d.compose f.val g.val = some (composeArrow d laws f g).val :=
  composite_spec d laws f.val g.val (f.property.2.trans g.property.1.symm)

theorem identity_compose {n m} (d : Data n m) (laws : Laws d)
    {x y : Fin n} (f : Arrow d x y) :
    composeArrow d laws (identityArrow d laws x) f = f := by
  apply Subtype.ext
  have law := laws.leftUnit f.val
  rw [f.property.1] at law
  exact Option.some.inj ((composeArrow_spec d laws (identityArrow d laws x) f).symm.trans law)

theorem compose_identity {n m} (d : Data n m) (laws : Laws d)
    {x y : Fin n} (f : Arrow d x y) :
    composeArrow d laws f (identityArrow d laws y) = f := by
  apply Subtype.ext
  have law := laws.rightUnit f.val
  rw [f.property.2] at law
  exact Option.some.inj ((composeArrow_spec d laws f (identityArrow d laws y)).symm.trans law)

theorem compose_associative {n m} (d : Data n m) (laws : Laws d)
    {w x y z : Fin n} (f : Arrow d w x) (g : Arrow d x y) (h : Arrow d y z) :
    composeArrow d laws (composeArrow d laws f g) h =
      composeArrow d laws f (composeArrow d laws g h) := by
  apply Subtype.ext
  have law := laws.associative f.val g.val h.val
    (f.property.2.trans g.property.1.symm) (g.property.2.trans h.property.1.symm)
  rw [composeArrow_spec d laws f g, composeArrow_spec d laws g h] at law
  simp only [Option.bind_some] at law
  rw [composeArrow_spec d laws (composeArrow d laws f g) h,
    composeArrow_spec d laws f (composeArrow d laws g h)] at law
  exact Option.some.inj law

/-- The result uses Mathlib's actual category interface and its three laws. -/
@[instance_reducible] noncomputable def categoryOfLaws {n m} (d : Data n m) (laws : Laws d) :
    CategoryTheory.Category (Fin n) where
  Hom := Arrow d
  id := identityArrow d laws
  comp := composeArrow d laws
  id_comp := identity_compose d laws
  comp_id := compose_identity d laws
  assoc := compose_associative d laws

@[instance_reducible] noncomputable def categoryOfAdmitted {n m} (d out : Data n m) (guards : List Bool)
    (success : admit d guards = .ok out) : CategoryTheory.Category (Fin n) :=
  categoryOfLaws out (admit_success_laws d out guards success)

#print axioms checks_true_iff
#print axioms admit_preserves_data
#print axioms admit_success_laws
#print axioms failed_guard
#print axioms composite_spec
#print axioms composeArrow_spec
#print axioms identity_compose
#print axioms compose_identity
#print axioms compose_associative
#print axioms categoryOfAdmitted

end TFQM.FiniteCategory
