-- Integer keep-and-scale pairs for three steps with a zero fresh addend.
-- The literature limitation is not stated here.

namespace CampaignQcvImportNoisyReversibleLimits

def u : Nat → Nat
  | 0 => 1
  | t + 1 => 3 * u t

def v : Nat → Nat
  | 0 => 1
  | t + 1 => 4 * v t

def w : Nat → Nat
  | 0 => 1
  | t + 1 => 3 * w t + 0

theorem u_zero : u 0 = 1 := rfl

theorem v_zero : v 0 = 1 := rfl

theorem w_zero : w 0 = 1 := rfl

theorem u_step (t : Nat) : u (t + 1) = 3 * u t := rfl

theorem v_step (t : Nat) : v (t + 1) = 4 * v t := rfl

theorem w_step (t : Nat) : w (t + 1) = 3 * w t + 0 := rfl

theorem u1 : u 1 = 3 := by decide

theorem v1 : v 1 = 4 := by decide

theorem u2 : u 2 = 9 := by decide

theorem v2 : v 2 = 16 := by decide

theorem u3 : u 3 = 27 := by decide

theorem v3 : v 3 = 64 := by decide

theorem below1 : u 1 < v 1 := by decide

theorem below2 : u 2 < v 2 := by decide

theorem below3 : u 3 < v 3 := by decide

theorem w0_u : w 0 = u 0 := rfl

theorem w1 : w 1 = u 1 := by decide

theorem w2 : w 2 = u 2 := by decide

theorem w3 : w 3 = u 3 := by decide

#print axioms u_zero
#print axioms v_zero
#print axioms w_zero
#print axioms u_step
#print axioms v_step
#print axioms w_step
#print axioms u1
#print axioms v1
#print axioms u2
#print axioms v2
#print axioms u3
#print axioms v3
#print axioms below1
#print axioms below2
#print axioms below3
#print axioms w0_u
#print axioms w1
#print axioms w2
#print axioms w3

end CampaignQcvImportNoisyReversibleLimits
