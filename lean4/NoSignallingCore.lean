

namespace NoSignallingCore

variable {X Y A B : Type}

def sumList : List Nat → Nat
  | [] => 0
  | x :: xs => x + sumList xs

theorem sumList_mul (c : Nat) (l : List Nat) :
    sumList (l.map (fun x => c * x)) = c * sumList l := by
  induction l with
  | nil => rfl
  | cons head tail ih =>
    simp only [List.map, sumList]
    rw [Nat.mul_add, ih]

theorem sumList_map_mul (c : Nat) (f : B → Nat) (l : List B) :
    sumList (l.map (fun b => c * f b)) = c * sumList (l.map f) := by
  induction l with
  | nil => rfl
  | cons head tail ih =>
    simp only [List.map, sumList]
    rw [Nat.mul_add, ih]

def marginalA (P : X → Y → A → B → Nat) (outcomesB : List B) (x : X) (y : Y) (a : A) : Nat :=
  sumList (outcomesB.map (fun b => P x y a b))

def NoSignallingBA (P : X → Y → A → B → Nat) (outcomesB : List B) : Prop :=
  ∀ x a y y', marginalA P outcomesB x y a = marginalA P outcomesB x y' a

theorem product_noSignalling (PA : X → A → Nat) (PB : Y → B → Nat)
    (outcomesB : List B)
    (hPB : ∀ y, sumList (outcomesB.map (PB y)) = 1) :
    NoSignallingBA (fun x y a b => PA x a * PB y b) outcomesB := by
  intro x a y y'
  simp only [marginalA]
  rw [sumList_map_mul (PA x a) (PB y) outcomesB]
  rw [sumList_map_mul (PA x a) (PB y') outcomesB]
  rw [hPB y, hPB y']

theorem marginalA_product (PA : X → A → Nat) (PB : Y → B → Nat)
    (outcomesB : List B) (hPB : ∀ y, sumList (outcomesB.map (PB y)) = 1)
    (x : X) (y : Y) (a : A) :
    marginalA (fun x y a b => PA x a * PB y b) outcomesB x y a = PA x a := by
  simp only [marginalA]
  rw [sumList_map_mul (PA x a) (PB y) outcomesB, hPB y, Nat.mul_one]

namespace Witness

def sig (_x : Unit) (y : Bool) (a : Bool) (_b : Unit) : Nat :=
  if a == y then 1 else 0

theorem sig_signals : ¬ NoSignallingBA sig [()] := by
  intro h
  have key := h () true true false
  revert key
  decide

end Witness

end NoSignallingCore

namespace QM.NoSignalling
export NoSignallingCore (sumList sumList_mul sumList_map_mul marginalA NoSignallingBA product_noSignalling marginalA_product)
namespace Witness
export NoSignallingCore.Witness (sig sig_signals)
end Witness
end QM.NoSignalling

#print axioms NoSignallingCore.sumList_mul
#print axioms NoSignallingCore.sumList_map_mul
#print axioms NoSignallingCore.product_noSignalling
#print axioms NoSignallingCore.marginalA_product
#print axioms NoSignallingCore.Witness.sig_signals

private def l5aProvenance : String :=
  "Origin: lean4/NoSignallingCore.lean Claim: sumList_mul AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
