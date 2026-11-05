import WitnessedDifference.Core

/-!
# Semiring Transport Kernel

Mechanized core lemmas for the finite weighted transport calculus:
- `lsum_mul_right`: finite-sum right-distributivity: algebraic core of path-sum / transfer-matrix
  identities for coarse-graining preservation.
- `holonomy_telescope`: coboundary connections telescope along paths.
- `coboundary_trivial_holonomy`: coboundary has zero holonomy around any closed walk.
- `im_d0_subset_ker_d1`: d1 ∘ d0 = 0 implies im(d0) ⊆ ker(d1) for quotient descent.

No continuum, no inner product, and no Born rule appears.
-/

namespace WitnessedDifference

/-! ## Minimal right-distributive weight algebra (Mathlib-free) -/

class FWSemiring (R : Type _) where
  zero : R
  one  : R
  add  : R → R → R
  mul  : R → R → R
  zero_mul      : ∀ a, mul zero a = zero
  right_distrib : ∀ a b c, mul (add a b) c = add (mul a c) (mul b c)

open FWSemiring

/-- The finite weighted aggregation `Σ xs` (the path-sum over a finite fiber). -/
def lsum {R : Type _} [FWSemiring R] : List R → R
  | []      => zero
  | x :: xs => add x (lsum xs)

/-- Finite sums distribute on the right: `(Σ xs) · y = Σ (x · y)`. -/
theorem lsum_mul_right {R : Type _} [FWSemiring R] (y : R) :
    ∀ xs : List R, mul (lsum xs) y = lsum (xs.map (fun x => mul x y))
  | [] => by
      simp only [lsum, List.map_nil]
      exact zero_mul y
  | x :: xs => by
      simp only [lsum, List.map_cons]
      rw [right_distrib, lsum_mul_right y xs]

/-! ## Connection, holonomy, and coboundary triviality -/

variable {V : Type _}

/-- Last element of a non-empty walk `a :: l`. -/
def lastOf (a : V) : List V → V
  | []      => a
  | b :: rest => lastOf b rest

/-- Holonomy of the coboundary connection from a potential `φ` along a walk over Int. -/
def holonomy (φ : V → Int) : List V → Int
  | []          => 0
  | [_]         => 0
  | a :: b :: rest => (φ b - φ a) + holonomy φ (b :: rest)

/-- The coboundary telescopes: `holonomy(a::l) = φ(last) - φ(first)`. -/
theorem holonomy_telescope (φ : V → Int) :
    ∀ (a : V) (l : List V), holonomy φ (a :: l) = φ (lastOf a l) - φ a := by
  intro a l
  induction l generalizing a with
  | nil => simp only [holonomy, lastOf]; omega
  | cons b rest ih =>
      simp only [holonomy, lastOf]
      rw [ih b]; omega

/-- A walk `a :: l` is closed when its last vertex returns to the first. -/
def IsClosed (a : V) (l : List V) : Prop := lastOf a l = a

/-- A coboundary has zero holonomy around any closed walk. -/
theorem coboundary_trivial_holonomy (φ : V → Int) (a : V) (l : List V)
    (h : IsClosed a l) : holonomy φ (a :: l) = 0 := by
  rw [holonomy_telescope, show lastOf a l = a from h]; omega

/-! ## d² = 0 exact-repair closedness kernel -/

/-- If `d1 ∘ d0 = 0` then `im d0 ⊆ ker d1`. -/
theorem im_d0_subset_ker_d1
    {A B C : Type _} (d0 : A → B) (d1 : B → C) (z : C)
    (hdd : ∀ x, d1 (d0 x) = z) :
    ∀ y, (∃ x, y = d0 x) → d1 y = z := by
  intro y hy
  obtain ⟨x, rfl⟩ := hy
  exact hdd x

/-! ## Worked finite instance: ℕ as a weight semiring -/

instance : FWSemiring Nat where
  zero := 0
  one  := 1
  add  := Nat.add
  mul  := Nat.mul
  zero_mul := Nat.zero_mul
  right_distrib := Nat.add_mul

theorem nat_lsum_example : lsum (R := Nat) [1, 2, 3] = 6 := by decide

end WitnessedDifference
