/-
  Campaign core -- shared carriers for grok_pd_night_20260814.
  AuthorityEffect: None. Not a theorem. Not PROVEN.

  Downstream obligations must import this file instead of restating
  Realization, polarity wrappers, Observation, SplitPresentation,
  AmbientDynamics, or the residual quotient. Changing a core
  definition must break dependents.
-/

namespace GrokPdNight20260814.Core

/-- B004 representation data. The realizing biconditional is not a field. -/
structure Realization (X : Type) (D : Type) where
  δ : X → X → D
  Zero : D → Prop

def zeroRel {X D : Type} (ρ : Realization X D) (x y : X) : Prop :=
  ρ.Zero (ρ.δ x y)

def Realizes {X D : Type} (R : X → X → Prop) (ρ : Realization X D) : Prop :=
  ∀ x y : X, R x y ↔ zeroRel ρ x y

def conservative {X : Type} (R : X → X → Prop) : Realization X Prop where
  δ := R
  Zero := id

def HasRefl {X D : Type} (ρ : Realization X D) : Prop :=
  ∀ x : X, zeroRel ρ x x

def HasSymm {X D : Type} (ρ : Realization X D) : Prop :=
  ∀ x y : X, zeroRel ρ x y → zeroRel ρ y x

def HasTrans {X D : Type} (ρ : Realization X D) : Prop :=
  ∀ x y z : X, zeroRel ρ x y → zeroRel ρ y z → zeroRel ρ x z

/-- B006 least equivalence containing a raw relation. -/
inductive EqvClosure {X : Type} (R : X → X → Prop) : X → X → Prop
  | base {x y : X} : R x y → EqvClosure R x y
  | refl (x : X) : EqvClosure R x x
  | symm {x y : X} : EqvClosure R x y → EqvClosure R y x
  | trans {x y z : X} :
      EqvClosure R x y → EqvClosure R y z → EqvClosure R x z

/-- Kernel-shaped pack. Laws enter as supplied theorems, not as imports. -/
structure PrimitiveDifference (α : Type) (β : Type) where
  δ : α → α → β
  Zero : β → Prop
  zero_refl : ∀ x : α, Zero (δ x x)
  zero_symm : ∀ x y : α, Zero (δ x y) → Zero (δ y x)
  zero_trans : ∀ x y z : α, Zero (δ x y) → Zero (δ y z) → Zero (δ x z)

def ofRealization {X D : Type} (ρ : Realization X D)
    (hrefl : HasRefl ρ) (hsymm : HasSymm ρ) (htrans : HasTrans ρ) :
    PrimitiveDifference X D where
  δ := ρ.δ
  Zero := ρ.Zero
  zero_refl := hrefl
  zero_symm := hsymm
  zero_trans := htrans

def ZeroRel {α β : Type} (P : PrimitiveDifference α β) (x y : α) : Prop :=
  P.Zero (P.δ x y)

/-- B014 polarity wrappers. One field each; semantics live in theorems. -/
structure ApartPred (X : Type) where
  rel : X → X → Prop

structure ZeroPred (X : Type) where
  rel : X → X → Prop

/-- B002 presentation-indexed observation. Map is declared data. -/
structure Observation (X : Type) (Y : Type) (Prov : Type) where
  map : X → Y
  provenance : Prov

/-- E004 declared split. Law is a field because this is an import package. -/
structure SplitPresentation (X : Type) (M : Type) where
  p : X → M
  i : M → X
  split : ∀ m : M, p (i m) = m

def IsSplit {X M : Type} (p : X → M) (i : M → X) : Prop :=
  ∀ m : M, p (i m) = m

/-- E006 induced endomap. -/
def inducedP {X M : Type} (S : SplitPresentation X M) : X → X :=
  fun x => S.i (S.p x)

/-- E007 declared single-step dynamics. No laws. -/
structure AmbientDynamics (X : Type) (Prov : Type) where
  T : X → X
  provenance : Prov

/-- B008 residual quotient of a named Setoid. -/
def ResidualQuotient {X : Type} (S : Setoid X) : Type :=
  Quotient S

def classOf {X : Type} (S : Setoid X) (x : X) : ResidualQuotient S :=
  Quotient.mk S x

theorem classOf_eq_iff {X : Type} (S : Setoid X) (x y : X) :
    classOf S x = classOf S y ↔ S.r x y :=
  ⟨Quotient.exact, Quotient.sound⟩

#print axioms classOf_eq_iff

end GrokPdNight20260814.Core
