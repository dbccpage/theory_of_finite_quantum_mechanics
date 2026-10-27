

namespace HilbertWalk.OctahedralDepolarizingThreshold


def bloch_numerator (a d : Int) : Int :=
  3 * (d - a) ^ 2

theorem p_42_numerator_eval : bloch_numerator 42 100 = 10092 := by rfl

theorem p_43_numerator_eval : bloch_numerator 43 100 = 9747 := by rfl

theorem p_42_strictly_exceeds_psd_ball :
    bloch_numerator 42 100 > 100 ^ 2 := by decide

theorem p_43_certified_within_psd_ball :
    bloch_numerator 43 100 ≤ 100 ^ 2 := by decide

theorem depolarizing_threshold_bracket :
    bloch_numerator 43 100 ≤ 100 ^ 2 ∧ bloch_numerator 42 100 > 100 ^ 2 :=
  ⟨p_43_certified_within_psd_ball, p_42_strictly_exceeds_psd_ball⟩


structure Vec3F2 where
  v0 : Int
  v1 : Int
  v2 : Int
  deriving DecidableEq, Repr

def r0 : Vec3F2 := ⟨0, 1, 1⟩
def r1 : Vec3F2 := ⟨1, 0, 1⟩
def r2 : Vec3F2 := ⟨1, 1, 0⟩

theorem row_linear_dependence_mod2 :
    (r0.v0 + r1.v0) % 2 = r2.v0 ∧
    (r0.v1 + r1.v1) % 2 = r2.v1 ∧
    (r0.v2 + r1.v2) % 2 = r2.v2 := by decide

theorem r0_r1_independent_mod2 :
    (r0.v0 % 2 ≠ r1.v0 % 2 ∨ r0.v1 % 2 ≠ r1.v1 % 2 ∨ r0.v2 % 2 ≠ r1.v2 % 2) := by decide

def hemisphereMinor : Int :=
  r0.v1 * r1.v2 - r0.v2 * r1.v1

def hemisphereSchmidtRank : Nat :=
  if hemisphereMinor % 2 ≠ 0 then 2 ^ 2 else 0

theorem octahedral_hemisphere_schmidt_rank :
    hemisphereMinor % 2 = 1 ∧
      (r0.v0 + r1.v0) % 2 = r2.v0 ∧
      (r0.v1 + r1.v1) % 2 = r2.v1 ∧
      (r0.v2 + r1.v2) % 2 = r2.v2 ∧
      hemisphereSchmidtRank = 4 := by
  decide

#print axioms p_42_numerator_eval
#print axioms p_43_numerator_eval
#print axioms p_42_strictly_exceeds_psd_ball
#print axioms p_43_certified_within_psd_ball
#print axioms depolarizing_threshold_bracket
#print axioms row_linear_dependence_mod2
#print axioms r0_r1_independent_mod2
#print axioms octahedral_hemisphere_schmidt_rank

end HilbertWalk.OctahedralDepolarizingThreshold

private def l5aProvenance : String :=
  "Origin: lean4/OctahedralDepolarizingThreshold.lean Claim: p_42_numerator_eval AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
