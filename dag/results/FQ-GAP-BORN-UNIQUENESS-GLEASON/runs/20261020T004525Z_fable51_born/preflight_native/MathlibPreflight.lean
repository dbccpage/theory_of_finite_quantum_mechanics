import Mathlib

namespace BornEnvironmentPreflight
theorem rational_add_control (x y : Rat) : x + y = y + x := by ring
#print axioms rational_add_control
end BornEnvironmentPreflight
