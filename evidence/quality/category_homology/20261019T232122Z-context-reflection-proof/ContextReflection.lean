import Mathlib.CategoryTheory.NatTrans

/-! AuthorityEffect: None. Contextual objects and checked maps form an actual
Mathlib category. Equivalence/congruence saturation gives a reflector, natural
identity-carrier unit and natural Hom equivalence to congruent targets. Rust
is the finite nonempty implementation; numeric admission, canonical merge
rounds and storage refinement are separate source/native evidence. -/
namespace TFQM.ContextReflection
open CategoryTheory
universe u

structure System (I : Type u) where
  State : Type u
  action : State → I → State
  profile : Setoid State
structure Arrow {I : Type u} (S T : System I) where
  map : S.State → T.State
  preserves : ∀ {x y}, S.profile.r x y → T.profile.r (map x) (map y)
  commutes : ∀ x i, map (S.action x i) = T.action (map x) i
variable {I : Type u} {S T U V : System I}

theorem arrow_ext {f g : Arrow S T} (same : f.map = g.map) : f = g := by
  cases f
  cases g
  cases same
  rfl
def identity (S : System I) : Arrow S S where
  map := id
  preserves := fun h => h
  commutes := fun _ _ => rfl
def compose (f : Arrow S T) (g : Arrow T U) : Arrow S U where
  map := g.map ∘ f.map
  preserves := fun h => g.preserves (f.preserves h)
  commutes := fun x i => (congrArg g.map (f.commutes x i)).trans (g.commutes (f.map x) i)
instance contextCategory : Category.{u} (System I) where
  Hom := Arrow
  id := identity
  comp := compose
  id_comp := by intros; apply arrow_ext; rfl
  comp_id := by intros; apply arrow_ext; rfl
  assoc := by intros; apply arrow_ext; rfl
theorem composition_map (f : S ⟶ T) (g : T ⟶ U) (x : S.State) :
    (f ≫ g).map x = g.map (f.map x) := rfl
theorem identity_map (S : System I) (x : S.State) : (𝟙 S : Arrow S S).map x = x := rfl

def Congruent (S : System I) : Prop :=
  ∀ x y, S.profile.r x y → ∀ i, S.profile.r (S.action x i) (S.action y i)
inductive Saturated (S : System I) : S.State → S.State → Prop
  | base {x y} : S.profile.r x y → Saturated S x y
  | refl (x) : Saturated S x x
  | symm {x y} : Saturated S x y → Saturated S y x
  | trans {x y z} : Saturated S x y → Saturated S y z → Saturated S x z
  | action {x y} (i : I) : Saturated S x y → Saturated S (S.action x i) (S.action y i)
def reflect (S : System I) : System I where
  State := S.State
  action := S.action
  profile := {
    r := Saturated S
    iseqv := {
      refl := fun x => .refl x
      symm := fun h => .symm h
      trans := fun h k => .trans h k } }
theorem reflect_congruent (S : System I) : Congruent (reflect S) := by
  intro x y same i
  exact Saturated.action i same
theorem saturation_preserved (f : S ⟶ T) (stable : Congruent T) {x y : S.State}
    (h : Saturated S x y) : T.profile.r (f.map x) (f.map y) := by
  induction h with
  | base h => exact f.preserves h
  | refl x => exact T.profile.iseqv.refl _
  | symm _ ih => exact T.profile.iseqv.symm ih
  | trans _ _ ih ik => exact T.profile.iseqv.trans ih ik
  | @action x y i _ ih =>
    rw [f.commutes, f.commutes]
    exact stable _ _ ih i
def unit (S : System I) : S ⟶ reflect S where
  map := id
  preserves := fun h => .base h
  commutes := fun _ _ => rfl
def factor (f : S ⟶ T) (stable : Congruent T) : reflect S ⟶ T where
  map := f.map
  preserves := saturation_preserved f stable
  commutes := f.commutes
theorem factor_triangle (f : S ⟶ T) (stable : Congruent T) : unit S ≫ factor f stable = f := by
  apply arrow_ext
  rfl
theorem factor_unique (f : S ⟶ T) (stable : Congruent T) (g : reflect S ⟶ T)
    (triangle : unit S ≫ g = f) : g = factor f stable := by
  apply arrow_ext
  funext x
  exact congrArg (fun arrow : S ⟶ T => arrow.map x) triangle
def reflectMap (f : S ⟶ T) : reflect S ⟶ reflect T :=
  factor (f ≫ unit T) (reflect_congruent T)
def reflectFunctor : System I ⥤ System I where
  obj := reflect
  map := reflectMap
  map_id := by intro S; apply arrow_ext; rfl
  map_comp := by intros; apply arrow_ext; rfl
def unitNatural : CategoryTheory.NatTrans (𝟭 (System I)) (reflectFunctor (I := I)) where
  app := unit
  naturality := by intros; apply arrow_ext; rfl
def factorEquiv (S T : System I) (stable : Congruent T) : (S ⟶ T) ≃ (reflect S ⟶ T) where
  toFun := fun f => factor f stable
  invFun := fun g => unit S ≫ g
  left_inv := fun f => factor_triangle f stable
  right_inv := by intro g; apply arrow_ext; rfl
theorem factor_natural_left (h : S ⟶ T) (f : T ⟶ U) (stable : Congruent U) :
    reflectMap h ≫ factor f stable = factor (h ≫ f) stable := by
  apply arrow_ext
  rfl
theorem factor_natural_right (f : S ⟶ T) (g : T ⟶ U)
    (stableT : Congruent T) (stableU : Congruent U) :
    factor f stableT ≫ g = factor (f ≫ g) stableU := by
  apply arrow_ext
  rfl
theorem saturated_iff_of_congruent (stable : Congruent S) (x y : S.State) :
    Saturated S x y ↔ S.profile.r x y :=
  ⟨fun h => saturation_preserved (𝟙 S) stable h, fun h => .base h⟩
theorem reflection_idempotent (S : System I) (x y : S.State) :
    Saturated (reflect S) x y ↔ Saturated S x y :=
  saturated_iff_of_congruent (reflect_congruent S) x y
def Reflects (f : S ⟶ T) : Prop :=
  ∀ x y, T.profile.r (f.map x) (f.map y) → S.profile.r x y
theorem reflecting_congruent (f : S ⟶ T) (stable : Congruent T) (reflection : Reflects f) :
    Congruent S := by
  intro x y same i
  apply reflection
  rw [f.commutes, f.commutes]
  exact stable _ _ (f.preserves same) i
theorem obstruction_no_reflecting (f : S ⟶ T) (stable : Congruent T)
    (x y : S.State) (i : I) (same : S.profile.r x y)
    (different : ¬S.profile.r (S.action x i) (S.action y i)) : ¬Reflects f :=
  fun reflection => different (reflecting_congruent f stable reflection x y same i)
theorem unit_reflects_iff (S : System I) : Reflects (unit S) ↔ Congruent S :=
  ⟨reflecting_congruent (unit S) (reflect_congruent S),
    fun stable x y h => (saturated_iff_of_congruent stable x y).mp h⟩
end TFQM.ContextReflection

#print axioms TFQM.ContextReflection.arrow_ext
#print axioms TFQM.ContextReflection.contextCategory
#print axioms TFQM.ContextReflection.composition_map
#print axioms TFQM.ContextReflection.identity_map
#print axioms TFQM.ContextReflection.reflect_congruent
#print axioms TFQM.ContextReflection.saturation_preserved
#print axioms TFQM.ContextReflection.unit
#print axioms TFQM.ContextReflection.factor
#print axioms TFQM.ContextReflection.factor_triangle
#print axioms TFQM.ContextReflection.factor_unique
#print axioms TFQM.ContextReflection.reflectMap
#print axioms TFQM.ContextReflection.reflectFunctor
#print axioms TFQM.ContextReflection.unitNatural
#print axioms TFQM.ContextReflection.factorEquiv
#print axioms TFQM.ContextReflection.factor_natural_left
#print axioms TFQM.ContextReflection.factor_natural_right
#print axioms TFQM.ContextReflection.saturated_iff_of_congruent
#print axioms TFQM.ContextReflection.reflection_idempotent
#print axioms TFQM.ContextReflection.reflecting_congruent
#print axioms TFQM.ContextReflection.obstruction_no_reflecting
#print axioms TFQM.ContextReflection.unit_reflects_iff
