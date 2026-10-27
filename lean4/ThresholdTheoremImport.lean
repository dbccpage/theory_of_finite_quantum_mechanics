-- Integer orbit for one stated concatenation step.
-- The literature threshold theorems are not stated here.

namespace ThresholdTheoremImport

def t (n : Int) : Int := 2 * n * n

theorem t_spec (n : Int) : t n = 2 * n * n := rfl

theorem step_zero : t 0 = 0 := by decide

theorem step_one : t 1 = 2 := by decide

theorem step_two : t 2 = 8 := by decide

theorem step_eight : t 8 = 128 := by decide

theorem orbit_three : t (t (t 1)) = 128 := by decide

theorem mul_eight : 2 * 8 * 8 = 128 := by decide

theorem scale_zero : 2 * 0 = 0 := by decide

theorem scale_one : 2 * 1 = 2 := by decide

#print axioms t_spec
#print axioms step_zero
#print axioms step_one
#print axioms step_two
#print axioms step_eight
#print axioms orbit_three
#print axioms mul_eight
#print axioms scale_zero
#print axioms scale_one

end ThresholdTheoremImport
