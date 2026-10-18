







import HWKernel

namespace FableHilbertWalk20260819.H001

open FableHilbertWalk20260819.HWKernel

structure ScaledProb (Q : Type) (E : Enum Q) (M : Int) where
  w : Q → Int
  scale_pos : 0 < M
  nonneg : ∀ q : Q, 0 ≤ w q
  mass_eq : rsum intPack (E.elems.map w) = M

def mass {Q : Type} (E : Enum Q) (w : Q → Int) : Int :=
  rsum intPack (E.elems.map w)

def iabs (a : Int) : Int :=
  if a < 0 then -a else a

def l1dist {Q : Type} (E : Enum Q) (v w : Q → Int) : Int :=
  rsum intPack (E.elems.map (fun q => iabs (v q - w q)))

theorem iabs_zero : iabs 0 = 0 := by decide

theorem l1dist_self {Q : Type} (E : Enum Q) (v : Q → Int) :
    l1dist E v v = 0 := by
  unfold l1dist
  have h : E.elems.map (fun q => iabs (v q - v q)) =
      E.elems.map (fun _ => (0 : Int)) := by
    apply map_congr_mem
    intro q _
    rw [Int.sub_self, iabs_zero]
  rw [h]
  exact rsum_map_zero intPack E.elems

#print axioms l1dist_self


def pointW (q : Bool) : Int :=
  if q then 0 else 1

def pointMass : ScaledProb Bool enumBool 1 where
  w := pointW
  scale_pos := by decide
  nonneg := fun q => by cases q <;> decide
  mass_eq := by decide

#print axioms pointMass


def signedW (q : Bool) : Int :=
  if q then 2 else -1

theorem signed_mass_one : mass enumBool signedW = 1 := by decide

theorem signed_not_nonneg : ¬(∀ q : Bool, 0 ≤ signedW q) := by
  intro h
  exact absurd (h false) (by decide)

#print axioms signed_not_nonneg

def doubleW (_ : Bool) : Int := 1

theorem double_nonneg : ∀ q : Bool, 0 ≤ doubleW q := by decide

theorem double_mass_two : mass enumBool doubleW = 2 := by decide

theorem double_not_normalized : mass enumBool doubleW ≠ 1 := by decide

#print axioms double_not_normalized

theorem probability_simplex :
    (pointMass.w = pointW) ∧
      mass enumBool signedW = 1 ∧
      ¬(∀ q : Bool, 0 ≤ signedW q) ∧
      (∀ q : Bool, 0 ≤ doubleW q) ∧
      mass enumBool doubleW ≠ 1 :=
  ⟨rfl, signed_mass_one, signed_not_nonneg, double_nonneg,
    double_not_normalized⟩

#print axioms probability_simplex

end FableHilbertWalk20260819.H001

private def l5aProvenance : String :=
  "Origin: lean4/H001ProbabilitySimplex.lean Claim: iabs_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
