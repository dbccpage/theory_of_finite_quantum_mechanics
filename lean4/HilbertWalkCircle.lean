



import HWKernel
import InterferenceNonDescent
import U1SelectorBoundary

namespace HilbertWalk.Circle

open HilbertWalk.HWKernel
open HilbertWalk.InterferenceNonDescent

structure PhaseCarrier (G : Type) where
  mem : G → Prop
  mul : G → G → G
  one : G
  mem_one : mem one
  mem_mul : ∀ a b, mem a → mem b → mem (mul a b)

def ConnectednessShadow {G : Type} (P : PhaseCarrier G) : Prop :=
  ∃ u, P.mem u ∧ P.mul u u ≠ P.one


def isSign (a : Int) : Prop :=
  a = 1 ∨ a = -1

theorem isSign_mul (a b : Int) (ha : isSign a) (hb : isSign b) :
    isSign (a * b) := by
  rcases ha with ha | ha <;> rcases hb with hb | hb
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr rfl
  · subst ha; subst hb; exact Or.inr rfl
  · subst ha; subst hb; exact Or.inl rfl

#print axioms isSign_mul

theorem sign_every_square_is_one (a : Int) (h : isSign a) :
    a * a = 1 := by
  rcases h with h | h <;> subst h <;> decide

#print axioms sign_every_square_is_one

def signCarrier : PhaseCarrier Int where
  mem := isSign
  mul := (· * ·)
  one := 1
  mem_one := Or.inl rfl
  mem_mul := isSign_mul

theorem sign_fails_connectedness_shadow :
    ¬ ConnectednessShadow signCarrier := by
  intro h
  rcases h with ⟨u, hu, hne⟩
  exact hne (sign_every_square_is_one u hu)

#print axioms sign_fails_connectedness_shadow

theorem sign_excluded_under_connectedness_shadow
    {G : Type} (P : PhaseCarrier G) (h : ConnectednessShadow P) :
    ¬ ∀ u, P.mem u → P.mul u u = P.one := by
  intro hall
  rcases h with ⟨u, hu, hne⟩
  exact hne (hall u hu)

#print axioms sign_excluded_under_connectedness_shadow


def isGaussUnit (z : GaussInt) : Prop :=
  z = GaussInt.gone ∨ z = GaussInt.gneg GaussInt.gone ∨
    z = GaussInt.gi ∨ z = GaussInt.gneg GaussInt.gi

theorem isGaussUnit_mul (a b : GaussInt)
    (ha : isGaussUnit a) (hb : isGaussUnit b) :
    isGaussUnit (GaussInt.gmul a b) := by
  rcases ha with ha | ha | ha | ha <;>
    rcases hb with hb | hb | hb | hb
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)

#print axioms isGaussUnit_mul

def gaussUnitCarrier : PhaseCarrier GaussInt where
  mem := isGaussUnit
  mul := GaussInt.gmul
  one := GaussInt.gone
  mem_one := Or.inl rfl
  mem_mul := isGaussUnit_mul

theorem gi_sq_ne_one :
    GaussInt.gmul GaussInt.gi GaussInt.gi ≠ GaussInt.gone := by
  intro h
  have hre :
      (GaussInt.gmul GaussInt.gi GaussInt.gi).re = GaussInt.gone.re :=
    congrArg GaussInt.re h
  simp [GaussInt.gmul, GaussInt.gi, GaussInt.gone] at hre

#print axioms gi_sq_ne_one

theorem gauss_units_meet_connectedness_shadow :
    ConnectednessShadow gaussUnitCarrier :=
  ⟨GaussInt.gi, Or.inr (Or.inr (Or.inl rfl)), gi_sq_ne_one⟩

#print axioms gauss_units_meet_connectedness_shadow


def cyc3Carrier : PhaseCarrier (Fin 3) where
  mem := fun _ => True
  mul := (· + ·)
  one := 0
  mem_one := trivial
  mem_mul := fun _ _ _ _ => trivial

theorem cyc3_one_double_ne_zero : (1 : Fin 3) + 1 ≠ 0 := by
  decide

#print axioms cyc3_one_double_ne_zero

theorem cyc3_meets_connectedness_shadow :
    ConnectednessShadow cyc3Carrier :=
  ⟨1, trivial, cyc3_one_double_ne_zero⟩

#print axioms cyc3_meets_connectedness_shadow

theorem sign_excluded_circle_still_imported :
    ¬ ConnectednessShadow signCarrier ∧
      ConnectednessShadow gaussUnitCarrier ∧
      ConnectednessShadow cyc3Carrier ∧
      (∀ q : Bool, iWeights iPsi1 q = iWeights iPsi2 q) ∧
      ¬ (∀ q : Bool, iReadout iPsi1 q = iReadout iPsi2 q) :=
  ⟨sign_fails_connectedness_shadow,
    gauss_units_meet_connectedness_shadow,
    cyc3_meets_connectedness_shadow,
    int_realization.1, int_realization.2⟩

#print axioms sign_excluded_circle_still_imported

end HilbertWalk.Circle

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkCircle.lean Claim: isSign_mul AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
