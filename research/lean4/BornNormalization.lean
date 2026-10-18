

namespace BornNormalization

structure DiscreteDensity2 where
  a : Nat
  d : Nat
  denom : Nat
  h_denom_pos : denom > 0
  h_unit_trace : a + d = denom

def trace (ρ : DiscreteDensity2) : Nat :=
  ρ.a + ρ.d

theorem density_trace_eq_denom (ρ : DiscreteDensity2) :
    trace ρ = ρ.denom := by
  dsimp [trace]
  exact ρ.h_unit_trace

structure DiscretePOVM2 where
  e0_a : Nat
  e0_d : Nat
  e1_a : Nat
  e1_d : Nat
  h_res_a : e0_a + e1_a = 1
  h_res_d : e0_d + e1_d = 1

def born_outcome_0 (ρ : DiscreteDensity2) (povm : DiscretePOVM2) : Nat :=
  povm.e0_a * ρ.a + povm.e0_d * ρ.d

def born_outcome_1 (ρ : DiscreteDensity2) (povm : DiscretePOVM2) : Nat :=
  povm.e1_a * ρ.a + povm.e1_d * ρ.d

theorem born_normalization_redundancy (ρ : DiscreteDensity2) (povm : DiscretePOVM2) :
    born_outcome_0 ρ povm + born_outcome_1 ρ povm = ρ.denom := by
  dsimp [born_outcome_0, born_outcome_1]
  have h1 : povm.e0_a * ρ.a + povm.e1_a * ρ.a = (povm.e0_a + povm.e1_a) * ρ.a := by
    rw [Nat.add_mul]
  have h2 : povm.e0_d * ρ.d + povm.e1_d * ρ.d = (povm.e0_d + povm.e1_d) * ρ.d := by
    rw [Nat.add_mul]
  have h_reorder : (povm.e0_a * ρ.a + povm.e0_d * ρ.d) + (povm.e1_a * ρ.a + povm.e1_d * ρ.d) =
                   (povm.e0_a * ρ.a + povm.e1_a * ρ.a) + (povm.e0_d * ρ.d + povm.e1_d * ρ.d) := by omega
  rw [h_reorder, h1, h2, povm.h_res_a, povm.h_res_d]
  rw [Nat.one_mul, Nat.one_mul]
  exact ρ.h_unit_trace

structure DiscretePureState2 where
  c0 : Int
  c1 : Int
  denom : Nat
  h_denom_pos : denom > 0
  h_norm : c0 * c0 + c1 * c1 = (denom : Int)

def proj_00 (ψ : DiscretePureState2) : Int := ψ.c0 * ψ.c0
def proj_11 (ψ : DiscretePureState2) : Int := ψ.c1 * ψ.c1
def proj_01 (ψ : DiscretePureState2) : Int := ψ.c0 * ψ.c1
def proj_10 (ψ : DiscretePureState2) : Int := ψ.c1 * ψ.c0

theorem projector_self_adjoint (ψ : DiscretePureState2) :
    proj_01 ψ = proj_10 ψ := by
  dsimp [proj_01, proj_10]
  exact Int.mul_comm ψ.c0 ψ.c1

theorem projector_trace (ψ : DiscretePureState2) :
    proj_00 ψ + proj_11 ψ = (ψ.denom : Int) := by
  dsimp [proj_00, proj_11]
  exact ψ.h_norm

theorem projector_idempotence_00 (ψ : DiscretePureState2) :
    proj_00 ψ * proj_00 ψ + proj_01 ψ * proj_10 ψ = (ψ.denom : Int) * proj_00 ψ := by
  dsimp [proj_00, proj_01, proj_10]
  have h1 : (ψ.c0 * ψ.c0 + ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c0) =
            (ψ.c0 * ψ.c0) * (ψ.c0 * ψ.c0) + (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c0) :=
    Int.add_mul (ψ.c0 * ψ.c0) (ψ.c1 * ψ.c1) (ψ.c0 * ψ.c0)
  have h2 : ψ.c0 * ψ.c1 * (ψ.c1 * ψ.c0) = (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c0) := by
    simp [Int.mul_comm, Int.mul_left_comm]
  rw [h2, ← h1, ψ.h_norm]

theorem projector_idempotence_01 (ψ : DiscretePureState2) :
    proj_00 ψ * proj_01 ψ + proj_01 ψ * proj_11 ψ = (ψ.denom : Int) * proj_01 ψ := by
  dsimp [proj_00, proj_01, proj_11]
  have h1 : (ψ.c0 * ψ.c0 + ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c1) =
            (ψ.c0 * ψ.c0) * (ψ.c0 * ψ.c1) + (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c1) :=
    Int.add_mul (ψ.c0 * ψ.c0) (ψ.c1 * ψ.c1) (ψ.c0 * ψ.c1)
  have h2 : ψ.c0 * ψ.c1 * (ψ.c1 * ψ.c1) = (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c1) := by
    simp [Int.mul_comm, Int.mul_left_comm]
  rw [h2, ← h1, ψ.h_norm]

theorem ray_invariance_sign_flip (ψ : DiscretePureState2) :
    (-ψ.c0) * (-ψ.c0) = proj_00 ψ ∧
    (-ψ.c1) * (-ψ.c1) = proj_11 ψ ∧
    (-ψ.c0) * (-ψ.c1) = proj_01 ψ := by
  dsimp [proj_00, proj_11, proj_01]
  have h0 : (-ψ.c0) * (-ψ.c0) = ψ.c0 * ψ.c0 := by
    simp [Int.neg_mul_neg]
  have h1 : (-ψ.c1) * (-ψ.c1) = ψ.c1 * ψ.c1 := by
    simp [Int.neg_mul_neg]
  have h01 : (-ψ.c0) * (-ψ.c1) = ψ.c0 * ψ.c1 := by
    simp [Int.neg_mul_neg]
  exact ⟨h0, h1, h01⟩

#print axioms density_trace_eq_denom
#print axioms born_normalization_redundancy
#print axioms projector_self_adjoint
#print axioms projector_trace
#print axioms projector_idempotence_00
#print axioms projector_idempotence_01
#print axioms ray_invariance_sign_flip

end BornNormalization

private def l5aProvenance : String :=
  "Origin: lean4/BornNormalization.lean Claim: density_trace_eq_denom AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
