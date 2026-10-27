-- L1-U1-SELECTOR-OTHER-SEGMENT. Not a default target.
-- Unit circle over the integers modulo 7, as the powers of (2, 2).
-- Selection of C and U(1), every other modulus, and the Gaussian rationals stay outside this module.

namespace L1U1SelectorOtherSegment

/-- Product (a, b) * (c, d) = (a*c - b*d, a*d + b*c) on residues modulo 7.
The pad 252 = 7 * 36 keeps the first coordinate inside Nat for residues below 7. -/
def mul (a b : Nat × Nat) : Nat × Nat :=
  ((a.1 * b.1 + 252 - a.2 * b.2) % 7, (a.1 * b.2 + a.2 * b.1) % 7)

def g : Nat × Nat := (2, 2)

theorem step1 : mul (1, 0) g = (2, 2) := by decide
theorem step2 : mul (2, 2) g = (0, 1) := by decide
theorem step3 : mul (0, 1) g = (5, 2) := by decide
theorem step4 : mul (5, 2) g = (6, 0) := by decide
theorem step5 : mul (6, 0) g = (5, 5) := by decide
theorem step6 : mul (5, 5) g = (0, 6) := by decide
theorem step7 : mul (0, 6) g = (2, 5) := by decide
theorem step8 : mul (2, 5) g = (1, 0) := by decide

theorem norms :
    (1 * 1 + 0 * 0) % 7 = 1 ∧
    (2 * 2 + 2 * 2) % 7 = 1 ∧
    (0 * 0 + 1 * 1) % 7 = 1 ∧
    (5 * 5 + 2 * 2) % 7 = 1 ∧
    (6 * 6 + 0 * 0) % 7 = 1 ∧
    (5 * 5 + 5 * 5) % 7 = 1 ∧
    (0 * 0 + 6 * 6) % 7 = 1 ∧
    (2 * 2 + 5 * 5) % 7 = 1 := by decide

def isPower (x y : Nat) : Bool :=
  (x == 1 && y == 0) ||
  (x == 2 && y == 2) ||
  (x == 0 && y == 1) ||
  (x == 5 && y == 2) ||
  (x == 6 && y == 0) ||
  (x == 5 && y == 5) ||
  (x == 0 && y == 6) ||
  (x == 2 && y == 5)

theorem solutions_iff :
    ∀ x : Fin 7, ∀ y : Fin 7,
      ((x.val * x.val + y.val * y.val) % 7 == 1) = isPower x.val y.val := by
  decide

def allDistinct : List (Nat × Nat) → Bool
  | [] => true
  | p :: rest => !rest.contains p && allDistinct rest

theorem eight_distinct :
    allDistinct [(1, 0), (2, 2), (0, 1), (5, 2), (6, 0), (5, 5), (0, 6), (2, 5)] = true := by
  decide

theorem eight : 8 = 7 + 1 ∧ 8 ≠ 4 := by decide

theorem earlier_ne_one :
    (2, 2) ≠ (1, 0) ∧
    (0, 1) ≠ (1, 0) ∧
    (5, 2) ≠ (1, 0) ∧
    (6, 0) ≠ (1, 0) ∧
    (5, 5) ≠ (1, 0) ∧
    (0, 6) ≠ (1, 0) ∧
    (2, 5) ≠ (1, 0) := by decide

theorem not_axis : g ≠ (0, 1) ∧ g ≠ (0, 6) ∧ g ≠ (1, 0) ∧ g ≠ (6, 0) := by decide

#print axioms step1
#print axioms step2
#print axioms step3
#print axioms step4
#print axioms step5
#print axioms step6
#print axioms step7
#print axioms step8
#print axioms norms
#print axioms solutions_iff
#print axioms eight_distinct
#print axioms eight
#print axioms earlier_ne_one
#print axioms not_axis

end L1U1SelectorOtherSegment
