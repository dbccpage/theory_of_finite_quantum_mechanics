/- Finite relation-coarsening completion and exact reflecting-unit obstruction.
   The universal property is proved for arbitrary carriers; the native solver
   specializes its generated congruence to finite carriers. AuthorityEffect: None. -/
namespace WitnessedDifference.ContextReflection

universe u v

structure System (A : Type u) (C : Type v) where
  rel : A → A → Prop
  refl : ∀ x, rel x x
  symm : ∀ x y, rel x y → rel y x
  trans : ∀ x y z, rel x y → rel y z → rel x z
  act : C → A → A

structure Hom {A B : Type u} {C : Type v} (S : System A C) (T : System B C) where
  map : A → B
  preserve : ∀ x y, S.rel x y → T.rel (map x) (map y)
  commute : ∀ c x, map (S.act c x) = T.act c (map x)

def Congruent {A : Type u} {C : Type v} (S : System A C) : Prop :=
  ∀ c x y, S.rel x y → S.rel (S.act c x) (S.act c y)

def identity {A : Type u} {C : Type v} (S : System A C) : Hom S S :=
  ⟨id, fun _ _ h => h, fun _ _ => rfl⟩

def compose {A B D : Type u} {C : Type v}
    {S : System A C} {T : System B C} {U : System D C}
    (f : Hom S T) (g : Hom T U) : Hom S U where
  map := fun x => g.map (f.map x)
  preserve := fun x y h => g.preserve _ _ (f.preserve x y h)
  commute := by
    intro c x
    rw [f.commute, g.commute]

theorem hom_ext {A B : Type u} {C : Type v} {S : System A C} {T : System B C}
    (f g : Hom S T) (h : f.map = g.map) : f = g := by
  cases f
  cases g
  cases h
  rfl

theorem identity_left {A B : Type u} {C : Type v}
    {S : System A C} {T : System B C} (f : Hom S T) : compose (identity S) f = f := by
  apply hom_ext
  rfl

theorem identity_right {A B : Type u} {C : Type v}
    {S : System A C} {T : System B C} (f : Hom S T) : compose f (identity T) = f := by
  apply hom_ext
  rfl

theorem composition_associative {A B D E : Type u} {C : Type v}
    {S : System A C} {T : System B C} {U : System D C} {V : System E C}
    (f : Hom S T) (g : Hom T U) (h : Hom U V) :
    compose (compose f g) h = compose f (compose g h) := by
  apply hom_ext
  rfl

inductive Closure {A : Type u} {C : Type v} (S : System A C) : A → A → Prop
  | base {x y} : S.rel x y → Closure S x y
  | refl (x) : Closure S x x
  | symm {x y} : Closure S x y → Closure S y x
  | trans {x y z} : Closure S x y → Closure S y z → Closure S x z
  | action (c) {x y} : Closure S x y → Closure S (S.act c x) (S.act c y)

def reflection {A : Type u} {C : Type v} (S : System A C) : System A C where
  rel := Closure S
  refl := Closure.refl
  symm := fun _ _ => Closure.symm
  trans := fun _ _ _ => Closure.trans
  act := S.act

theorem reflection_congruent {A : Type u} {C : Type v} (S : System A C) :
    Congruent (reflection S) := fun c _ _ h => Closure.action c h

def unit {A : Type u} {C : Type v} (S : System A C) : Hom S (reflection S) :=
  ⟨id, fun _ _ h => Closure.base h, fun _ _ => rfl⟩

theorem closure_preserved {A B : Type u} {C : Type v}
    {S : System A C} {T : System B C} (f : Hom S T) (hT : Congruent T)
    {x y : A} (h : Closure S x y) : T.rel (f.map x) (f.map y) := by
  induction h with
  | base h => exact f.preserve _ _ h
  | refl x => exact T.refl (f.map x)
  | symm _ ih => exact T.symm _ _ ih
  | trans _ _ ih₁ ih₂ => exact T.trans _ _ _ ih₁ ih₂
  | action c h ih =>
      rw [f.commute, f.commute]
      exact hT c _ _ ih

def factor {A B : Type u} {C : Type v}
    {S : System A C} {T : System B C} (hT : Congruent T) (f : Hom S T) :
    Hom (reflection S) T :=
  ⟨f.map, fun _ _ h => closure_preserved f hT h, f.commute⟩

/-- Initiality in the actual comma category S↓Cong: objects are congruent
    systems T with arrows f:S→T; arrows satisfy the displayed triangle.
    Uniqueness is equality of typed Hom values, not just a Boolean flag. -/
theorem reflection_initial {A B : Type u} {C : Type v}
    (S : System A C) (T : System B C) (hT : Congruent T) (f : Hom S T) :
    ∃ g : Hom (reflection S) T,
      compose (unit S) g = f ∧
      ∀ k : Hom (reflection S) T, compose (unit S) k = f → k = g := by
  refine ⟨factor hT f, ?_, ?_⟩
  · apply hom_ext
    rfl
  · intro k triangle
    apply hom_ext
    have maps := congrArg Hom.map triangle
    exact maps

def reflectHom {A B : Type u} {C : Type v}
    {S : System A C} {T : System B C} (f : Hom S T) :
    Hom (reflection S) (reflection T) :=
  factor (reflection_congruent T) (compose f (unit T))

theorem reflection_identity {A : Type u} {C : Type v} (S : System A C) :
    reflectHom (identity S) = identity (reflection S) := by
  apply hom_ext
  rfl

theorem reflection_composition {A B D : Type u} {C : Type v}
    {S : System A C} {T : System B C} {U : System D C}
    (f : Hom S T) (g : Hom T U) :
    reflectHom (compose f g) = compose (reflectHom f) (reflectHom g) := by
  apply hom_ext
  rfl

theorem unit_natural {A B : Type u} {C : Type v}
    {S : System A C} {T : System B C} (f : Hom S T) :
    compose (unit S) (reflectHom f) = compose f (unit T) := by
  apply hom_ext
  rfl

/-- Exact obstruction: a profile-reflecting arrow into Cong forces the
    source already to belong to Cong, so such units cannot repair failure. -/
theorem reflecting_unit_requires_congruence {A B : Type u} {C : Type v}
    {S : System A C} {T : System B C} (f : Hom S T) (hT : Congruent T)
    (reflects : ∀ x y, T.rel (f.map x) (f.map y) → S.rel x y) : Congruent S := by
  intro c x y hxy
  apply reflects (S.act c x) (S.act c y)
  rw [f.commute, f.commute]
  exact hT c _ _ (f.preserve x y hxy)

/-- In the profile-reflecting comma category there are no objects at all
    when S is noncongruent; hence no candidate can be an initial object. -/
theorem no_reflecting_completion {A B : Type u} {C : Type v}
    (S : System A C) (bad : ¬ Congruent S) (T : System B C) :
    ¬ ∃ f : Hom S T, Congruent T ∧
      (∀ x y, T.rel (f.map x) (f.map y) → S.rel x y) := by
  intro h
  obtain ⟨f, hT, reflects⟩ := h
  exact bad (reflecting_unit_requires_congruence f hT reflects)

inductive Three | left | middle | right

def report : Three → Bool
  | .left => false
  | .middle => false
  | .right => true

def countermodel : System Three Unit where
  rel := fun x y => report x = report y
  refl := fun _ => rfl
  symm := fun _ _ => Eq.symm
  trans := fun _ _ _ => Eq.trans
  act := fun _ x => match x with
    | .left => .left
    | .middle => .right
    | .right => .right

theorem countermodel_noncongruent : ¬ Congruent countermodel := by
  intro h
  have impossible := h () Three.left Three.middle rfl
  cases impossible

theorem countermodel_has_no_reflecting_initial_object (B : Type) (T : System B Unit) :
    ¬ ∃ f : Hom countermodel T, Congruent T ∧
      (∀ x y, T.rel (f.map x) (f.map y) → countermodel.rel x y) :=
  no_reflecting_completion countermodel countermodel_noncongruent T

#print axioms reflection_initial
#print axioms no_reflecting_completion
#print axioms countermodel_has_no_reflecting_initial_object
#print axioms reflection_identity
#print axioms reflection_composition
#print axioms unit_natural

end WitnessedDifference.ContextReflection
