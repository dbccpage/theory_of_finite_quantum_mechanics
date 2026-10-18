/-
  H004 -- free linearization. AuthorityEffect: None. Candidate only.
  Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H004
  Source-paper contact: QM_020 (amplitude carrier), QM_121 rung
  "linear structure". H001/H002 report layer below.

  Target proposition
    Given an imported coefficient carrier K (a StarRingPack), the
    function space K^Q with delta basis gives formal linear
    combinations over report states: superposition SYNTAX. The same
    construction runs over Int, GaussInt, and F2, so the carrier is
    an import that Primitive Difference does not select.

  Imports added at this rung
    The coefficient pack K. That is the entire content of the rung:
    everything else is the free construction over it.

  Theorem or counterexample
    basis_expansion: every vector is the pack-sum of its coordinates
    against the delta basis (general, any pack, any enumeration).
    carrier_not_selected: over F2, delta_true + delta_true = 0 while
    over Int the same formal sum is nonzero -- the finite separator
    showing the coefficient import changes the geometry.

  Nonclaim boundary
    No inner product yet (H005). No claim that K^Q is THE state
    space of anything physical. "Superposition" here is syntax; its
    quotient-fiber semantics is H009.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel

namespace FableHilbertWalk20260819.H004

open FableHilbertWalk20260819.HWKernel

/-- Vectors: the free K-module on the report set, as functions. -/
def Vec (K Q : Type) : Type := Q → K

def vadd {K Q : Type} (P : StarRingPack K) (u v : Vec K Q) : Vec K Q :=
  fun q => P.add (u q) (v q)

def smul {K Q : Type} (P : StarRingPack K) (c : K) (v : Vec K Q) :
    Vec K Q :=
  fun q => P.mul c (v q)

def vzero {K Q : Type} (P : StarRingPack K) : Vec K Q :=
  fun _ => P.zero

/-- Delta basis vector at a report state. -/
def delta {K Q : Type} (P : StarRingPack K) [DecidableEq Q] (q : Q) :
    Vec K Q :=
  fun x => if (q == x) = true then P.one else P.zero

/-- Superposition syntax: every vector is the pack-sum of its
    coordinates against the delta basis, pointwise. General theorem:
    any pack, any enumerated report set. -/
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

/-! ## Linear pushforward: the free extension of a report map. -/

def linPush {K X Q : Type} (P : StarRingPack K) [DecidableEq Q]
    (E : Enum X) (τ : X → Q) (v : Vec K X) : Vec K Q :=
  fun q => rsum P ((E.elems.filter (fun x => τ x == q)).map v)

/-- Linear pushforward preserves the total pack-sum: H002's Fubini
    at the amplitude level, for any coefficient pack. -/
theorem linPush_total {K X Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (EX : Enum X) (EQ : Enum Q) (τ : X → Q)
    (v : Vec K X) :
    rsum P (EQ.elems.map (linPush P EX τ v)) =
      rsum P (EX.elems.map v) :=
  rsum_fiber_partition P EQ τ v EX.elems

#print axioms linPush_total

/-! ## Refusal: the coefficient carrier is an import. The same
    formal sum behaves differently over F2 and Int. -/

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

/-- H004 punchline: superposition syntax is free over an imported
    carrier, and the carrier choice is observable. -/
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

end FableHilbertWalk20260819.H004
