import Mathlib.Algebra.BigOperators.Ring.Finset

/-!
# No-signalling: product behaviors have setting-independent marginals (cycle 007, QM_009)

A bounded entry into the QM_009 reconstruction. One of the five reconstruction conditions is
**no-signalling**: a distant party's *setting* must not change the local *marginal*. This file
mechanizes the finite fact that **product / local behaviors are no-signalling** — Alice's marginal of
`P(a,b|x,y) = PA(a|x)·PB(b|y)` is `PA(a|x)`, independent of Bob's setting `y` — plus a concrete
signaling witness so the condition is a genuine (non-vacuous) constraint.

Representation-transport / reconstruction routing: this is one finite ingredient of the no-signalling
condition, **not** a claim that no-signalling forces QM. No authority minted (LGGR).
-/

open scoped BigOperators

namespace QM.NoSignalling

variable {X Y A B R : Type*} [Fintype A] [Fintype B] [CommSemiring R]

/-- The A-marginal of a bipartite behavior `P(a,b | x,y)`: `P_A(a|x,y) = ∑_b P x y a b`. -/
def marginalA (P : X → Y → A → B → R) (x : X) (y : Y) (a : A) : R := ∑ b, P x y a b

/-- **No-signalling B→A:** Alice's marginal does not depend on Bob's setting `y`. -/
def NoSignallingBA (P : X → Y → A → B → R) : Prop :=
  ∀ x a y y', marginalA P x y a = marginalA P x y' a

omit [Fintype A] in
/-- **Product / local behaviors are no-signalling.** If `P x y a b = PA x a * PB y b` with each
`PB y` normalized (`∑_b PB y b = 1`), then `P_A(a|x,y) = PA x a`, independent of `y`. -/
theorem product_noSignalling (PA : X → A → R) (PB : Y → B → R)
    (hPB : ∀ y, ∑ b, PB y b = 1) :
    NoSignallingBA (fun x y a b => PA x a * PB y b) := by
  intro x a y y'
  simp only [marginalA]
  rw [← Finset.mul_sum, ← Finset.mul_sum, hPB y, hPB y']

/-- Bob's marginal: `P_B(b|x,y) = ∑_a P x y a b`. -/
def marginalB (P : X → Y → A → B → R) (x : X) (y : Y) (b : B) : R := ∑ a, P x y a b

/-- **No-signalling A→B:** Bob's marginal does not depend on Alice's setting `x`. -/
def NoSignallingAB (P : X → Y → A → B → R) : Prop :=
  ∀ y b x x', marginalB P x y b = marginalB P x' y b

omit [Fintype B] in
/-- **Product behaviors are no-signalling A→B too** (symmetric to `product_noSignalling`). -/
theorem product_noSignalling_AB (PA : X → A → R) (PB : Y → B → R)
    (hPA : ∀ x, ∑ a, PA x a = 1) :
    NoSignallingAB (fun x y a b => PA x a * PB y b) := by
  intro y b x x'
  simp only [marginalB]
  rw [← Finset.sum_mul, ← Finset.sum_mul, hPA x, hPA x']

/-- The reduced A-marginal (computed at a default Bob setting). -/
def reducedMarginalA [Inhabited Y] (P : X → Y → A → B → R) (x : X) (a : A) : R :=
  marginalA P x default a

omit [Fintype A] in
/-- **Well-defined local state.** Under no-signalling, Alice's marginal at *any* Bob setting `y`
equals the reduced marginal — an unambiguous local description independent of Bob. (This is the
reconstruction consequence of no-signalling: each party has a well-defined reduced state.) -/
theorem reducedMarginalA_eq [Inhabited Y] {P : X → Y → A → B → R}
    (h : NoSignallingBA P) (x : X) (a : A) (y : Y) :
    marginalA P x y a = reducedMarginalA P x a :=
  h x a y default

omit [Fintype A] in
/-- **Operational independence (A).** The product joint recovers Alice's local behavior:
`marginalA (PA·PB) = PA` (when each `PB y` is normalized). -/
theorem marginalA_product (PA : X → A → R) (PB : Y → B → R) (hPB : ∀ y, ∑ b, PB y b = 1)
    (x : X) (y : Y) (a : A) :
    marginalA (fun x y a b => PA x a * PB y b) x y a = PA x a := by
  simp only [marginalA]; rw [← Finset.mul_sum, hPB y, mul_one]

omit [Fintype B] in
/-- **Operational independence (B).** The product joint recovers Bob's local behavior:
`marginalB (PA·PB) = PB` (when each `PA x` is normalized). -/
theorem marginalB_product (PA : X → A → R) (PB : Y → B → R) (hPA : ∀ x, ∑ a, PA x a = 1)
    (x : X) (y : Y) (b : B) :
    marginalB (fun x y a b => PA x a * PB y b) x y b = PB y b := by
  simp only [marginalB]; rw [← Finset.sum_mul, hPA x, one_mul]

omit [Fintype A] in
/-- `marginalA` is additive in the behavior. -/
theorem marginalA_add (P Q : X → Y → A → B → R) (x : X) (y : Y) (a : A) :
    marginalA (fun x y a b => P x y a b + Q x y a b) x y a
      = marginalA P x y a + marginalA Q x y a := by
  simp only [marginalA, Finset.sum_add_distrib]

omit [Fintype A] in
/-- **No-signalling is closed under addition** (hence under mixing / convex combination): if `P` and
`Q` are no-signalling B→A, so is `P + Q`. The no-signalling behaviors form a convex cone. -/
theorem noSignalling_add {P Q : X → Y → A → B → R}
    (hP : NoSignallingBA P) (hQ : NoSignallingBA Q) :
    NoSignallingBA (fun x y a b => P x y a b + Q x y a b) := by
  intro x a y y'
  rw [marginalA_add P Q x y a, marginalA_add P Q x y' a, hP x a y y', hQ x a y y']

omit [Fintype A] in
/-- `marginalA` is homogeneous in the behavior. -/
theorem marginalA_smul (c : R) (P : X → Y → A → B → R) (x : X) (y : Y) (a : A) :
    marginalA (fun x y a b => c * P x y a b) x y a = c * marginalA P x y a := by
  simp only [marginalA]; rw [← Finset.mul_sum]

omit [Fintype A] in
/-- **No-signalling is closed under scalar multiplication.** With `noSignalling_add` this makes the
no-signalling behaviors a convex cone. -/
theorem noSignalling_smul (c : R) {P : X → Y → A → B → R} (hP : NoSignallingBA P) :
    NoSignallingBA (fun x y a b => c * P x y a b) := by
  intro x a y y'
  rw [marginalA_smul c P x y a, marginalA_smul c P x y' a, hP x a y y']

end QM.NoSignalling

namespace QM.NoSignalling.Witness

/-- A behavior where Alice's outcome is forced to equal Bob's setting — manifestly signaling. -/
def sig (_x : Unit) (y : Bool) (a : Bool) (_b : Unit) : ℕ := if a = y then 1 else 0

/-- **Non-vacuity:** the signaling witness is *not* no-signalling — so no-signalling is a genuine
constraint, not vacuously true. -/
theorem sig_signals : ¬ QM.NoSignalling.NoSignallingBA sig := by
  intro h
  have key := h () true true false
  simp [QM.NoSignalling.marginalA, sig] at key

end QM.NoSignalling.Witness

#print axioms QM.NoSignalling.product_noSignalling
#print axioms QM.NoSignalling.product_noSignalling_AB
#print axioms QM.NoSignalling.reducedMarginalA_eq
#print axioms QM.NoSignalling.marginalA_product
#print axioms QM.NoSignalling.marginalB_product
#print axioms QM.NoSignalling.marginalA_add
#print axioms QM.NoSignalling.noSignalling_add
#print axioms QM.NoSignalling.marginalA_smul
#print axioms QM.NoSignalling.noSignalling_smul
#print axioms QM.NoSignalling.Witness.sig_signals
