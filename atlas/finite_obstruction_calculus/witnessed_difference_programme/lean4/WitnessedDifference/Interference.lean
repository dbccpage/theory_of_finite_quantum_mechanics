import WitnessedDifference.Core

/-!
# Interference terms of a biadditive quadratic measure

Amplitudes live in a type `α` with a binary operation `add`, and a
path-set measure is read off a pairing `B : α → α → ℚ` as `P(x) = B x x`.
When `B` is additive in each argument, the second-order interference term is
the cross pairing and the third-order Sorkin term vanishes identically:

- `I₂ = P(a + b) - P(a) - P(b) = B a b + B b a`;
- `I₃ = P(a + b + c) - P(a + b) - P(a + c) - P(b + c) + P(a) + P(b) + P(c) = 0`.

Only the orders `k = 2` and `k = 3` are stated; there is no general-`k`
statement. The empty-set term `P(∅)` is omitted from `I₃`, as in the usual
Sorkin form, so no zero amplitude and no `B 0 0 = 0` hypothesis is needed.
Neither `add` nor `B` is assumed commutative, associative, or symmetric; the
theorems use only the two additivity hypotheses. This file declares no
synthetic axioms.
-/

namespace WitnessedDifference.Interference

variable {α : Type _}

/-- Second-order interference is the cross pairing. -/
theorem sorkin_I2_cross (add : α → α → α) (B : α → α → ℚ)
    (additive_left : ∀ x y z, B (add x y) z = B x z + B y z)
    (additive_right : ∀ x y z, B x (add y z) = B x y + B x z)
    (a b : α) :
    B (add a b) (add a b) - B a a - B b b = B a b + B b a := by
  simp only [additive_left, additive_right]
  grind

/-- Third-order Sorkin interference vanishes for a biadditive pairing. The
empty-set term is not included. -/
theorem sorkin_I3_biadditive (add : α → α → α) (B : α → α → ℚ)
    (additive_left : ∀ x y z, B (add x y) z = B x z + B y z)
    (additive_right : ∀ x y z, B x (add y z) = B x y + B x z)
    (a b c : α) :
    B (add (add a b) c) (add (add a b) c)
        - B (add a b) (add a b) - B (add a c) (add a c) - B (add b c) (add b c)
        + B a a + B b b + B c c = 0 := by
  simp only [additive_left, additive_right]
  grind

end WitnessedDifference.Interference
