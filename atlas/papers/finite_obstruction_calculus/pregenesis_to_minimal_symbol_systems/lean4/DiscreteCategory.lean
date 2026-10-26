import Paper

/-! The discrete categories used in the finite alphabet example. Homs are
lifted equality proofs, with actual identity/composition and functor laws.
An equivalence includes natural isomorphisms for both composites. -/
namespace PreMssn.DiscreteCategory
universe u v w

def Hom {A : Type u} (a b : A) := PLift (a = b)

instance {A : Type u} {a b : A} : Subsingleton (Hom a b) :=
  ⟨fun x y => by cases x; cases y; rfl⟩

def identityHom {A : Type u} (a : A) : Hom a a := ⟨rfl⟩
def composeHom {A : Type u} {a b c : A} (g : Hom b c) (f : Hom a b) : Hom a c :=
  ⟨f.down.trans g.down⟩

theorem identity_compose {A : Type u} {a b : A} (f : Hom a b) :
    composeHom (identityHom b) f = f := Subsingleton.elim _ _
theorem compose_identity {A : Type u} {a b : A} (f : Hom a b) :
    composeHom f (identityHom a) = f := Subsingleton.elim _ _
theorem compose_assoc {A : Type u} {a b c d : A}
    (h : Hom c d) (g : Hom b c) (f : Hom a b) :
    composeHom (composeHom h g) f = composeHom h (composeHom g f) :=
  Subsingleton.elim _ _

structure Functor (A : Type u) (B : Type v) where
  obj : A → B

def Functor.map {A : Type u} {B : Type v} (F : Functor A B)
    {a b : A} (f : Hom a b) : Hom (F.obj a) (F.obj b) := ⟨congrArg F.obj f.down⟩

theorem Functor.map_identity {A : Type u} {B : Type v} (F : Functor A B) (a : A) :
    F.map (identityHom a) = identityHom (F.obj a) := Subsingleton.elim _ _
theorem Functor.map_compose {A : Type u} {B : Type v} (F : Functor A B)
    {a b c : A} (g : Hom b c) (f : Hom a b) :
    F.map (composeHom g f) = composeHom (F.map g) (F.map f) := Subsingleton.elim _ _

def Functor.identity (A : Type u) : Functor A A := ⟨fun a => a⟩
def Functor.comp {A : Type u} {B : Type v} {C : Type w}
    (G : Functor B C) (F : Functor A B) : Functor A C := ⟨fun a => G.obj (F.obj a)⟩

structure NaturalIso {A : Type u} {B : Type v} (F G : Functor A B) where
  component : ∀ a, Hom (F.obj a) (G.obj a)
  naturality : ∀ a b (f : Hom a b),
    composeHom (component b) (F.map f) = composeHom (G.map f) (component a)

def NaturalIso.symm {A : Type u} {B : Type v} {F G : Functor A B}
    (e : NaturalIso F G) : NaturalIso G F where
  component a := ⟨(e.component a).down.symm⟩
  naturality _ _ _ := Subsingleton.elim _ _

theorem NaturalIso.component_left_inverse {A : Type u} {B : Type v}
    {F G : Functor A B} (e : NaturalIso F G) (a : A) :
    composeHom (e.symm.component a) (e.component a) = identityHom (F.obj a) :=
  Subsingleton.elim _ _
theorem NaturalIso.component_right_inverse {A : Type u} {B : Type v}
    {F G : Functor A B} (e : NaturalIso F G) (a : A) :
    composeHom (e.component a) (e.symm.component a) = identityHom (G.obj a) :=
  Subsingleton.elim _ _

structure Equivalence (A : Type u) (B : Type v) where
  forward : Functor A B
  backward : Functor B A
  unit : NaturalIso (Functor.identity A) (backward.comp forward)
  counit : NaturalIso (forward.comp backward) (Functor.identity B)

theorem Equivalence.left_inverse {A : Type u} {B : Type v}
    (e : Equivalence A B) (a : A) : e.backward.obj (e.forward.obj a) = a :=
  (e.unit.component a).down.symm

theorem Equivalence.right_inverse {A : Type u} {B : Type v}
    (e : Equivalence A B) (b : B) : e.forward.obj (e.backward.obj b) = b :=
  (e.counit.component b).down

theorem equivalence_object_bijection {A : Type u} {B : Type v}
    (e : Equivalence A B) :
    (∀ a a', e.forward.obj a = e.forward.obj a' → a = a') ∧
    (∀ b, ∃ a, e.forward.obj a = b) := by
  constructor
  · intro a a' h
    rw [← e.left_inverse a, ← e.left_inverse a', h]
  · intro b
    exact ⟨e.backward.obj b, e.right_inverse b⟩

theorem finite_equivalence_card_eq {n m : Nat} (e : Equivalence (Fin n) (Fin m)) :
    n = m := by
  have left := finite_injection_card_le e.forward.obj
    (equivalence_object_bijection e).1
  have right := finite_injection_card_le e.backward.obj (fun a b h => by
    rw [← e.right_inverse a, ← e.right_inverse b, h])
  omega

theorem two_and_twenty_six_not_equivalent :
    ¬Nonempty (Equivalence (Fin 2) (Fin 26)) := by
  rintro ⟨e⟩
  have h := finite_equivalence_card_eq e
  omega

end PreMssn.DiscreteCategory
