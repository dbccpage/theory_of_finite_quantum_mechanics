import Std

/-!
Source-25's one-assertion slice and finite cost-report obstructions.

`step` is the exact natural-multiplicity add/remove rule on one fixed cell.
Embedding into a nonempty raw Source25State, with every other field fixed,
is checked in the native Rust integration test and explained in the research
note. This file does not formalize the entire source interpreter or its
Python/Rust correspondence. No claim that `<>` forces admission is made.
-/
namespace NativeHistoryCost

inductive Event where
  | add
  | remove
  deriving DecidableEq

def step : Nat → Event → Option Nat
  | n, .add => some (n + 1)
  | 0, .remove => none
  | n + 1, .remove => some n

def replay (n : Nat) : List Event → Option Nat
  | [] => some n
  | e :: es => (step n e).bind (fun m => replay m es)

def price : List Event → Nat
  | [] => 0
  | .add :: es => 1 + price es
  | .remove :: es => price es

def loops : Nat → List Event
  | 0 => []
  | k + 1 => .add :: .remove :: loops k

theorem replay_loops (n k : Nat) : replay n (loops k) = some n := by
  induction k with
  | zero => rfl
  | succ k ih => simpa [loops, replay, step] using ih

theorem price_loops (k : Nat) : price (loops k) = k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [loops, price, ih, Nat.add_comm]

theorem length_loops (k : Nat) : (loops k).length = 2 * k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [loops, ih, Nat.mul_add, Nat.add_assoc]

theorem loops_injective {j k : Nat} (h : loops j = loops k) : j = k := by
  have := congrArg price h
  simpa [price_loops] using this

theorem price_append (before after : List Event) :
    price (before ++ after) = price before + price after := by
  induction before with
  | nil => simp [price]
  | cons e es ih => cases e <;> simp [price, ih, Nat.add_assoc]

theorem positive_loop_has_no_zero_price_continuation (k : Nat) (after : List Event) :
    0 < price (loops (k + 1) ++ after) := by
  rw [price_append, price_loops]
  omega

theorem endpoint_does_not_recover_price (n : Nat) :
    ¬ ∃ decode : Option Nat → Nat,
      ∀ k, decode (replay n (loops k)) = price (loops k) := by
  rintro ⟨decode, h⟩
  have h0 := h 0
  have h1 := h 1
  simp only [replay_loops, price_loops] at h0 h1
  omega

/- A constructive finite maximum; no classical enumeration assumption. -/
def bound : (n : Nat) → (Fin n → Nat) → Nat
  | 0, _ => 0
  | n + 1, f => max (f 0) (bound n (fun i => f i.succ))

theorem le_bound {n : Nat} (f : Fin n → Nat) (i : Fin n) : f i ≤ bound n f := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    refine Fin.cases ?_ (fun j => ?_) i
    · exact Nat.le_max_left _ _
    · exact Nat.le_trans (ih (fun j => f j.succ) j) (Nat.le_max_right _ _)

/-- No finite-valued report admits an exact decoder of every loop price. -/
theorem no_finite_exact_price (labels : Nat) (report : Nat → Fin labels)
    (decode : Fin labels → Nat) : ¬ ∀ k, decode (report k) = price (loops k) := by
  intro h
  have hb := le_bound decode (report (bound labels decode + 1))
  rw [h, price_loops] at hb
  omega

/-- Any finite report with integer decoder has arbitrarily large underestimates.
This does not address infinite-valued reports in a finite-dimensional space. -/
theorem finite_price_error_unbounded (labels : Nat) (report : Nat → Fin labels)
    (decode : Fin labels → Nat) (gap : Nat) :
    ∃ k, decode (report k) + gap < price (loops k) := by
  refine ⟨bound labels decode + gap + 1, ?_⟩
  have hb := le_bound decode (report (bound labels decode + gap + 1))
  rw [price_loops]
  omega

/-- For an arrow and an inverse, additive nonnegative costs summing to the
identity cost must both vanish. `reverse` need only be a right inverse. -/
theorem reversible_nonnegative_cost_zero {G : Type} (one : G) (mul : G → G → G)
    (cost : G → Nat) (hOne : cost one = 0)
    (hAdd : ∀ a b, cost (mul a b) = cost a + cost b)
    (a reverse : G) (hInverse : mul a reverse = one) : cost a = 0 := by
  have h := hAdd a reverse
  rw [hInverse, hOne] at h
  omega

/-- A concrete nonempty reversible model satisfies the preceding hypotheses;
they are not an inconsistent axiom package. -/
theorem reversible_zero_cost_inhabitant :
    (fun _ : Bool => 0 : Bool → Nat) false = 0 ∧
    (∀ _a _b : Bool, (0 : Nat) = 0 + 0) ∧
    (∀ a : Bool, Bool.xor a a = false) := by
  constructor
  · rfl
  constructor
  · intro _ _; rfl
  · intro a; cases a <;> rfl

#print axioms replay_loops
#print axioms price_loops
#print axioms length_loops
#print axioms loops_injective
#print axioms price_append
#print axioms positive_loop_has_no_zero_price_continuation
#print axioms endpoint_does_not_recover_price
#print axioms le_bound
#print axioms no_finite_exact_price
#print axioms finite_price_error_unbounded
#print axioms reversible_nonnegative_cost_zero
#print axioms reversible_zero_cost_inhabitant

end NativeHistoryCost
