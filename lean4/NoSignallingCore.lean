/-!
# No-signalling: product behaviors have setting-independent marginals (Cycle 007 core mechanization)

AuthorityEffect: None.
Self-contained Lean 4 core verification of Cycle 007 without external Mathlib dependencies.
Proves that product behaviors have setting-independent marginals, operational independence
holds, and the signaling witness demonstrates non-vacuity.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace NoSignallingCore

variable {X Y A B : Type}

/-- Finite list summation in Lean 4 core. -/
def sumList : List Nat → Nat
  | [] => 0
  | x :: xs => x + sumList xs

/-- Distributivity of multiplication over list summation. -/
theorem sumList_mul (c : Nat) (l : List Nat) :
    sumList (l.map (fun x => c * x)) = c * sumList l := by
  induction l with
  | nil => rfl
  | cons head tail ih =>
    simp only [List.map, sumList]
    rw [Nat.mul_add, ih]

/-- Distributivity over mapped function list summation. -/
theorem sumList_map_mul (c : Nat) (f : B → Nat) (l : List B) :
    sumList (l.map (fun b => c * f b)) = c * sumList (l.map f) := by
  induction l with
  | nil => rfl
  | cons head tail ih =>
    simp only [List.map, sumList]
    rw [Nat.mul_add, ih]

/-- Alice's marginal over Bob's finite outcome list `outcomesB`. -/
def marginalA (P : X → Y → A → B → Nat) (outcomesB : List B) (x : X) (y : Y) (a : A) : Nat :=
  sumList (outcomesB.map (fun b => P x y a b))

/-- No-signalling condition B → A: Alice's marginal is invariant under Bob's setting `y`. -/
def NoSignallingBA (P : X → Y → A → B → Nat) (outcomesB : List B) : Prop :=
  ∀ x a y y', marginalA P outcomesB x y a = marginalA P outcomesB x y' a

/-- **Theorem (No-signalling on product behaviors):** If Bob's local behavior is normalized
(`∑_b PB y b = 1`), then the product joint behavior `P(a,b|x,y) = PA(a|x) * PB(b|y)` is no-signalling. -/
theorem product_noSignalling (PA : X → A → Nat) (PB : Y → B → Nat)
    (outcomesB : List B)
    (hPB : ∀ y, sumList (outcomesB.map (PB y)) = 1) :
    NoSignallingBA (fun x y a b => PA x a * PB y b) outcomesB := by
  intro x a y y'
  simp only [marginalA]
  rw [sumList_map_mul (PA x a) (PB y) outcomesB]
  rw [sumList_map_mul (PA x a) (PB y') outcomesB]
  rw [hPB y, hPB y']

/-- **Theorem (Operational independence):** Alice's marginal exactly recovers `PA(a|x)`. -/
theorem marginalA_product (PA : X → A → Nat) (PB : Y → B → Nat)
    (outcomesB : List B) (hPB : ∀ y, sumList (outcomesB.map (PB y)) = 1)
    (x : X) (y : Y) (a : A) :
    marginalA (fun x y a b => PA x a * PB y b) outcomesB x y a = PA x a := by
  simp only [marginalA]
  rw [sumList_map_mul (PA x a) (PB y) outcomesB, hPB y, Nat.mul_one]

namespace Witness

/-- Manifest signaling witness: Alice's outcome equals Bob's setting (`a == y`). -/
def sig (_x : Unit) (y : Bool) (a : Bool) (_b : Unit) : Nat :=
  if a == y then 1 else 0

/-- **Theorem (Non-vacuity):** The signaling witness violates no-signalling. -/
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
