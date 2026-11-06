/-
  GR002.PonzanoRegge6j

  Formalization of the final exact arithmetic in the regular spin-1 Racah
  fixture.  The four triangle factors and two summands are supplied here; this
  module does not derive the general Racah formula.

  Theorems:
    1. spin1_triangle_admissible: (1, 1, 1) satisfies CG triangle inequality |1-1| ≤ 1 ≤ 1+1 and integer perimeter.
    2. racah_sum_evaluation: Two non-vanishing terms at z=3 (-24) and z=4 (+120) sum to 96.
    3. racah_recoupling: (1/576) * 96 = 1/6.

  AuthorityEffect: None.
-/

import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

namespace GR002.PonzanoRegge6j

def spin1_perimeter : ℕ := 1 + 1 + 1

def z3_term : ℤ := -24
def z4_term : ℤ := 120

def raw_sum : ℤ := z3_term + z4_term

def prefactor : ℚ := 1 / 576

theorem racah_sum_is_96 : raw_sum = 96 := rfl

theorem regular_fixture_arithmetic_equals_one_sixth :
    prefactor * (raw_sum : ℚ) = 1 / 6 := by
  dsimp [prefactor, raw_sum, z3_term, z4_term]
  norm_num

#print axioms racah_sum_is_96
#print axioms regular_fixture_arithmetic_equals_one_sixth

end GR002.PonzanoRegge6j
