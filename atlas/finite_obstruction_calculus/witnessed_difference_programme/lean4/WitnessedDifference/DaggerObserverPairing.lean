import Lean.Elab.Tactic.Omega
import WitnessedDifference.AdditiveTensorCompletion

/-!
# Dagger extension and positive observer pairings

An involution on admitted generators extends uniquely to the free signed
carrier and componentwise through its algebraic tensor object.  Separately, a
declared additive observer into two integer coordinates induces a symmetric
positive-semidefinite Gram pairing.  Its self-null vectors are exactly the
observer kernel, and equal reports are exactly null observed differences.

No dagger, observer, positive form, complex structure, or probability readout
is selected by primitive difference.  This file proves preservation after the
corresponding finite data have been supplied.  Lean core plus the bundled Omega
tactic only.
-/

namespace WitnessedDifference.DaggerObserverPairing

open WitnessedDifference.AdditiveTensorCompletion

universe u

set_option linter.checkUnivs false

/-! ## Dagger on a free signed carrier -/

/-- A declared involution on admitted generators. -/
structure GeneratorDagger (X : Type u) where
  dagger : X → X
  involutive : ∀ x, dagger (dagger x) = x

def identityHom (A : AbelianGroup.{u}) : GroupHom A A where
  toFun := id
  map_zero := rfl
  map_add := fun _ _ => rfl
  map_neg := fun _ => rfl

def composeHom {A B C : AbelianGroup.{u}} (g : GroupHom B C) (f : GroupHom A B) :
    GroupHom A C where
  toFun := fun x => g.toFun (f.toFun x)
  map_zero := by rw [f.map_zero, g.map_zero]
  map_add := by intro x y; rw [f.map_add, g.map_add]
  map_neg := by intro x; rw [f.map_neg, g.map_neg]

/-- Homomorphisms from a free signed carrier agree when they agree on units. -/
theorem signedHom_ext_units {X : Type u} {G : AbelianGroup.{u}}
    (h k : GroupHom (signedGroup X) G)
    (onUnits : ∀ x, h.toFun (signedUnit x) = k.toFun (signedUnit x)) : h = k := by
  calc
    h = signedLiftHom G (fun x => h.toFun (signedUnit x)) := signedHom_eq_lift G h
    _ = signedLiftHom G (fun x => k.toFun (signedUnit x)) := by
      apply GroupHom.ext
      intro s
      apply congrArg (fun f => signedLift G f s)
      funext x
      exact onUnits x
    _ = k := (signedHom_eq_lift G k).symm

/-- The unique additive extension of the generator dagger. -/
def signedDaggerHom {X : Type u} (I : GeneratorDagger X) :
    GroupHom (signedGroup X) (signedGroup X) :=
  signedLiftHom (signedGroup X) (fun x => signedUnit (I.dagger x))

def signedDagger {X : Type u} (I : GeneratorDagger X) (a : Signed X) : Signed X :=
  (signedDaggerHom I).toFun a

theorem signedDagger_unit {X : Type u} (I : GeneratorDagger X) (x : X) :
    signedDagger I (signedUnit x) = signedUnit (I.dagger x) := by
  exact signedLift_unit (signedGroup X) (fun x => signedUnit (I.dagger x)) x

theorem signedDagger_add {X : Type u} (I : GeneratorDagger X) (a b : Signed X) :
    signedDagger I (signedAdd a b) =
      signedAdd (signedDagger I a) (signedDagger I b) :=
  (signedDaggerHom I).map_add a b

theorem signedDagger_neg {X : Type u} (I : GeneratorDagger X) (a : Signed X) :
    signedDagger I (signedNeg a) = signedNeg (signedDagger I a) :=
  (signedDaggerHom I).map_neg a

/-- The additive extension is itself involutive. -/
theorem signedDagger_involutive {X : Type u} (I : GeneratorDagger X)
    (a : Signed X) : signedDagger I (signedDagger I a) = a := by
  let twice := composeHom (signedDaggerHom I) (signedDaggerHom I)
  have h : twice = identityHom (signedGroup X) := by
    apply signedHom_ext_units
    intro x
    change signedDagger I (signedDagger I (signedUnit x)) = signedUnit x
    rw [signedDagger_unit, signedDagger_unit, I.involutive]
  exact congrArg (fun k => k.toFun a) h

/-! ## Compatibility with the algebraic tensor object -/

def pairDagger {X Y : Type u} (I : GeneratorDagger X) (J : GeneratorDagger Y) :
    GeneratorDagger (X × Y) where
  dagger := fun xy => (I.dagger xy.1, J.dagger xy.2)
  involutive := by
    intro xy
    cases xy
    simp only [I.involutive, J.involutive]

def tensorLeftHom {X Y : Type u} (b : Signed Y) :
    GroupHom (signedGroup X) (signedGroup (X × Y)) where
  toFun := fun a => tensor a b
  map_zero := tensor_zero_left b
  map_add := fun a a' => tensor_add_left a a' b
  map_neg := fun a => tensor_neg_left a b

def tensorRightHom {X Y : Type u} (a : Signed X) :
    GroupHom (signedGroup Y) (signedGroup (X × Y)) where
  toFun := tensor a
  map_zero := tensor_zero_right a
  map_add := tensor_add_right a
  map_neg := tensor_neg_right a

/-- Dagger acts componentwise on the universal algebraic tensor. -/
theorem signedDagger_tensor {X Y : Type u}
    (I : GeneratorDagger X) (J : GeneratorDagger Y)
    (a : Signed X) (b : Signed Y) :
    signedDagger (pairDagger I J) (tensor a b) =
      tensor (signedDagger I a) (signedDagger J b) := by
  have onLeftUnit : ∀ x : X,
      signedDagger (pairDagger I J) (tensor (signedUnit x) b) =
        tensor (signedDagger I (signedUnit x)) (signedDagger J b) := by
    intro x
    let lhs : GroupHom (signedGroup Y) (signedGroup (X × Y)) :=
      composeHom (signedDaggerHom (pairDagger I J)) (tensorRightHom (signedUnit x))
    let rhs : GroupHom (signedGroup Y) (signedGroup (X × Y)) :=
      composeHom (tensorRightHom (signedUnit (I.dagger x))) (signedDaggerHom J)
    have eq : lhs = rhs := by
      apply signedHom_ext_units
      intro y
      change signedDagger (pairDagger I J)
          (tensor (signedUnit x) (signedUnit y)) =
        tensor (signedUnit (I.dagger x))
          (signedDagger J (signedUnit y))
      rw [tensor_unit_unit, signedDagger_unit, signedDagger_unit,
        tensor_unit_unit]
      rfl
    have point := congrArg (fun k => k.toFun b) eq
    change signedDagger (pairDagger I J) (tensor (signedUnit x) b) =
      tensor (signedUnit (I.dagger x)) (signedDagger J b) at point
    rw [signedDagger_unit]
    exact point
  let lhs : GroupHom (signedGroup X) (signedGroup (X × Y)) :=
    composeHom (signedDaggerHom (pairDagger I J)) (tensorLeftHom b)
  let rhs : GroupHom (signedGroup X) (signedGroup (X × Y)) :=
    composeHom (tensorLeftHom (signedDagger J b)) (signedDaggerHom I)
  have eq : lhs = rhs := signedHom_ext_units lhs rhs onLeftUnit
  exact congrArg (fun k => k.toFun a) eq

/-! ## A concrete exact observer pairing -/

structure IVec2 where
  first : Int
  second : Int
  deriving DecidableEq

def vecZero : IVec2 := ⟨0, 0⟩
def vecAdd (u v : IVec2) : IVec2 := ⟨u.first + v.first, u.second + v.second⟩
def vecNeg (u : IVec2) : IVec2 := ⟨-u.first, -u.second⟩

abbrev ivec2Group : AbelianGroup where
  Carrier := IVec2
  zero := vecZero
  add := vecAdd
  zero_add := by intro x; cases x; simp [vecZero, vecAdd]
  add_zero := by intro x; cases x; simp [vecZero, vecAdd]
  add_assoc := by intro x y z; cases x; cases y; cases z; simp [vecAdd, Int.add_assoc]
  add_comm := by intro x y; cases x; cases y; simp [vecAdd, Int.add_comm]
  neg := vecNeg
  add_neg := by
    intro x
    cases x
    simp only [vecAdd, vecNeg, vecZero, IVec2.mk.injEq]
    constructor <;> omega
  neg_zero := by simp [vecNeg, vecZero]
  neg_add := by
    intro x y
    cases x
    cases y
    simp only [vecNeg, vecAdd, IVec2.mk.injEq]
    constructor <;> omega
  neg_neg := by intro x; cases x; simp [vecNeg]

def dot (u v : IVec2) : Int := u.first * v.first + u.second * v.second

theorem int_square_nonnegative (x : Int) : 0 ≤ x * x := by
  cases x with
  | ofNat n =>
      change (0 : Int) ≤ Int.ofNat (n * n)
      exact Int.natCast_nonneg (n * n)
  | negSucc n =>
      change (0 : Int) ≤ Int.ofNat ((n + 1) * (n + 1))
      exact Int.natCast_nonneg ((n + 1) * (n + 1))

theorem dot_self_nonnegative (u : IVec2) : 0 ≤ dot u u :=
  Int.add_nonneg (int_square_nonnegative u.first) (int_square_nonnegative u.second)

theorem dot_self_eq_zero_iff (u : IVec2) : dot u u = 0 ↔ u = vecZero := by
  constructor
  · intro h
    have hfirst_nonneg := int_square_nonnegative u.first
    have hsecond_nonneg := int_square_nonnegative u.second
    have hfirst_sq : u.first * u.first = 0 := by
      dsimp [dot] at h
      omega
    have hsecond_sq : u.second * u.second = 0 := by
      dsimp [dot] at h
      omega
    have hfirst : u.first = 0 := (Int.mul_eq_zero.mp hfirst_sq).elim id id
    have hsecond : u.second = 0 := (Int.mul_eq_zero.mp hsecond_sq).elim id id
    cases u
    simp only [vecZero, IVec2.mk.injEq]
    exact ⟨hfirst, hsecond⟩
  · intro h
    rw [h]
    rfl

/-- A finite additive observation of the free signed carrier. -/
abbrev Observation (X : Type) := GroupHom (signedGroup X) ivec2Group

/-- The observer-induced Gram pairing. -/
def observerPairing {X : Type} (L : Observation X) (a b : Signed X) : Int :=
  dot (L.toFun a) (L.toFun b)

theorem observerPairing_symmetric {X : Type} (L : Observation X)
    (a b : Signed X) : observerPairing L a b = observerPairing L b a := by
  simp only [observerPairing, dot]
  rw [Int.mul_comm (L.toFun a).first (L.toFun b).first,
    Int.mul_comm (L.toFun a).second (L.toFun b).second]

theorem observerPairing_self_nonnegative {X : Type} (L : Observation X)
    (a : Signed X) : 0 ≤ observerPairing L a a :=
  dot_self_nonnegative (L.toFun a)

/-- Self-null vectors of the induced positive-semidefinite form are exactly
the differences invisible to the observer. -/
theorem observerPairing_self_zero_iff_kernel {X : Type} (L : Observation X)
    (a : Signed X) :
    observerPairing L a a = 0 ↔ L.toFun a = vecZero :=
  dot_self_eq_zero_iff (L.toFun a)

def signedSub {X : Type u} (a b : Signed X) : Signed X :=
  signedAdd a (signedNeg b)

theorem observed_sub_eq_zero_iff {X : Type} (L : Observation X)
    (a b : Signed X) : L.toFun (signedSub a b) = vecZero ↔ L.toFun a = L.toFun b := by
  change L.toFun (signedAdd a (signedNeg b)) = vecZero ↔ L.toFun a = L.toFun b
  rw [L.map_add, L.map_neg]
  cases ha : L.toFun a with
  | mk a₁ a₂ =>
    cases hb : L.toFun b with
    | mk b₁ b₂ =>
      simp only [vecAdd, vecNeg, vecZero, IVec2.mk.injEq]
      constructor
      · rintro ⟨h₁, h₂⟩
        constructor <;> omega
      · rintro ⟨h₁, h₂⟩
        constructor <;> omega

/-- Equal observer reports are exactly the differences in the Gram radical. -/
theorem same_observation_iff_null_difference {X : Type} (L : Observation X)
    (a b : Signed X) :
    L.toFun a = L.toFun b ↔
      observerPairing L (signedSub a b) (signedSub a b) = 0 := by
  rw [observerPairing_self_zero_iff_kernel, observed_sub_eq_zero_iff]

/-! ## Nonselection boundaries -/

/-- Rank one over the integers has no endomorphism squaring to minus one. -/
theorem no_rank_one_integer_complex_structure : ¬ ∃ j : Int, j * j = -1 := by
  rintro ⟨j, hj⟩
  have h := int_square_nonnegative j
  omega

/-- Positivity does not select a unique pairing even on one generator. -/
theorem positive_pairing_not_unique :
    (∀ x : Int, 0 ≤ x * x) ∧
    (∀ x : Int, 0 ≤ 2 * (x * x)) ∧
    (1 : Int) * 1 ≠ 2 * (1 * 1) := by
  refine ⟨int_square_nonnegative, ?_, by decide⟩
  intro x
  exact Int.mul_nonneg (by decide) (int_square_nonnegative x)

end WitnessedDifference.DaggerObserverPairing

#print axioms WitnessedDifference.DaggerObserverPairing.signedHom_ext_units
#print axioms WitnessedDifference.DaggerObserverPairing.signedDagger_unit
#print axioms WitnessedDifference.DaggerObserverPairing.signedDagger_involutive
#print axioms WitnessedDifference.DaggerObserverPairing.signedDagger_tensor
#print axioms WitnessedDifference.DaggerObserverPairing.dot_self_nonnegative
#print axioms WitnessedDifference.DaggerObserverPairing.dot_self_eq_zero_iff
#print axioms WitnessedDifference.DaggerObserverPairing.observerPairing_symmetric
#print axioms WitnessedDifference.DaggerObserverPairing.observerPairing_self_nonnegative
#print axioms WitnessedDifference.DaggerObserverPairing.observerPairing_self_zero_iff_kernel
#print axioms WitnessedDifference.DaggerObserverPairing.same_observation_iff_null_difference
#print axioms WitnessedDifference.DaggerObserverPairing.no_rank_one_integer_complex_structure
#print axioms WitnessedDifference.DaggerObserverPairing.positive_pairing_not_unique
