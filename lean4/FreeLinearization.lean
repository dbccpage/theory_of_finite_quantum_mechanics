






import HWKernel

namespace HilbertWalk.FreeLinearization

open HilbertWalk.HWKernel

def Vec (K Q : Type) : Type := Q → K

def vadd {K Q : Type} (P : StarRingPack K) (u v : Vec K Q) : Vec K Q :=
  fun q => P.add (u q) (v q)

def smul {K Q : Type} (P : StarRingPack K) (c : K) (v : Vec K Q) :
    Vec K Q :=
  fun q => P.mul c (v q)

def vzero {K Q : Type} (P : StarRingPack K) : Vec K Q :=
  fun _ => P.zero

def delta {K Q : Type} (P : StarRingPack K) [DecidableEq Q] (q : Q) :
    Vec K Q :=
  fun x => if (q == x) = true then P.one else P.zero

theorem basis_expansion {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (E : Enum Q) (v : Vec K Q) (x : Q) :
    rsum P (E.elems.map (fun q => P.mul (v q) (delta P q x))) = v x := by
  have h : E.elems.map (fun q => P.mul (v q) (delta P q x)) =
      E.elems.map (fun q =>
        if (x == q) = true then v x else P.zero) := by
    apply map_congr_mem
    intro q _
    unfold delta
    by_cases hq : x = q
    · subst hq
      rw [if_pos (beq_self_eq_true x), if_pos (beq_self_eq_true x),
        P.mul_one]
    · rw [if_neg (fun h => hq (beq_iff_eq.mp h).symm),
        if_neg (fun h => hq (beq_iff_eq.mp h)), P.mul_zero]
  rw [h, rsum_map_delta P (v x) (E.complete x) E.nodup]

#print axioms basis_expansion


def linPush {K X Q : Type} (P : StarRingPack K) [DecidableEq Q]
    (E : Enum X) (τ : X → Q) (v : Vec K X) : Vec K Q :=
  fun q => rsum P ((E.elems.filter (fun x => τ x == q)).map v)

theorem linPush_total {K X Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (EX : Enum X) (EQ : Enum Q) (τ : X → Q)
    (v : Vec K X) :
    rsum P (EQ.elems.map (linPush P EX τ v)) =
      rsum P (EX.elems.map v) :=
  rsum_fiber_partition P EQ τ v EX.elems

#print axioms linPush_total


def deltaTrueF2 : Vec Bool Bool := delta f2Pack true

def deltaTrueInt : Vec Int Bool := delta intPack true

theorem f2_superposition_cancels :
    ∀ x : Bool, vadd f2Pack deltaTrueF2 deltaTrueF2 x = vzero f2Pack x := by
  intro x; cases x <;> rfl

theorem int_superposition_persists :
    ¬(∀ x : Bool, vadd intPack deltaTrueInt deltaTrueInt x =
      vzero intPack x) := by
  intro h
  have h1 := h true
  revert h1
  decide

#print axioms f2_superposition_cancels
#print axioms int_superposition_persists

theorem free_linearization :
    (∀ (v : Vec Int Bool) (x : Bool),
      rsum intPack (enumBool.elems.map
        (fun q => intPack.mul (v q) (delta intPack q x))) = v x) ∧
      (∀ x : Bool,
        vadd f2Pack deltaTrueF2 deltaTrueF2 x = vzero f2Pack x) ∧
      ¬(∀ x : Bool,
        vadd intPack deltaTrueInt deltaTrueInt x = vzero intPack x) :=
  ⟨fun v x => basis_expansion intPack enumBool v x,
    f2_superposition_cancels, int_superposition_persists⟩

#print axioms free_linearization

end HilbertWalk.FreeLinearization

private def l5aProvenance : String :=
  "Origin: lean4/FreeLinearization.lean Claim: basis_expansion AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
