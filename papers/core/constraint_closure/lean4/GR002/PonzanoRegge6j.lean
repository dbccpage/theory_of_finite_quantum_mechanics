



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
