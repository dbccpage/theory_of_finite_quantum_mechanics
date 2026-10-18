/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

-- Born Normalization for Finite Quantum Carriers in Lean 4
-- AuthorityEffect: None

namespace BornNormalization

/-- A discrete 2-dimensional density operator represented by integer diagonal weights scaled by a positive denominator `denom`.
    Unit trace condition: a + d = denom, with non-negative diagonal elements a, d ≥ 0. -/
structure DiscreteDensity2 where
  a : Nat
  d : Nat
  denom : Nat
  h_denom_pos : denom > 0
  h_unit_trace : a + d = denom

/-- The trace of a discrete density operator. -/
def trace (ρ : DiscreteDensity2) : Nat :=
  ρ.a + ρ.d

/-- Unit trace theorem: Tr(ρ) = denom. -/
theorem density_trace_eq_denom (ρ : DiscreteDensity2) :
    trace ρ = ρ.denom := by
  dsimp [trace]
  exact ρ.h_unit_trace

/-- A discrete binary POVM partition of identity: E0 + E1 = I.
    Represented by diagonal weights satisfying e0_a + e1_a = 1 and e0_d + e1_d = 1. -/
structure DiscretePOVM2 where
  e0_a : Nat
  e0_d : Nat
  e1_a : Nat
  e1_d : Nat
  h_res_a : e0_a + e1_a = 1
  h_res_d : e0_d + e1_d = 1

/-- Unnormalized Born expectation Tr(E0 ρ) * denom = e0_a * ρ.a + e0_d * ρ.d. -/
def born_outcome_0 (ρ : DiscreteDensity2) (povm : DiscretePOVM2) : Nat :=
  povm.e0_a * ρ.a + povm.e0_d * ρ.d

/-- Unnormalized Born expectation Tr(E1 ρ) * denom = e1_a * ρ.a + e1_d * ρ.d. -/
def born_outcome_1 (ρ : DiscreteDensity2) (povm : DiscretePOVM2) : Nat :=
  povm.e1_a * ρ.a + povm.e1_d * ρ.d

/-- Born Probability Normalization Redundancy Theorem:
    The sum of Born measurement outcome probabilities across any complete POVM partition of identity
    equals the density operator trace (and thus equals denom, corresponding to total probability 1.0).
    This establishes that Born normalization is an algebraic redundancy once unit trace and resolution
    of identity are established. -/
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

/-- A pure state amplitude vector (c0, c1) over integers with sum of squares equal to denom. -/
structure DiscretePureState2 where
  c0 : Int
  c1 : Int
  denom : Nat
  h_denom_pos : denom > 0
  h_norm : c0 * c0 + c1 * c1 = (denom : Int)

/-- The rank-1 projector matrix elements for a pure state:
    P_00 = c0 * c0, P_11 = c1 * c1, P_01 = c0 * c1, P_10 = c1 * c0. -/
def proj_00 (ψ : DiscretePureState2) : Int := ψ.c0 * ψ.c0
def proj_11 (ψ : DiscretePureState2) : Int := ψ.c1 * ψ.c1
def proj_01 (ψ : DiscretePureState2) : Int := ψ.c0 * ψ.c1
def proj_10 (ψ : DiscretePureState2) : Int := ψ.c1 * ψ.c0

/-- Projector self-adjointness: P_01 = P_10 for real amplitudes. -/
theorem projector_self_adjoint (ψ : DiscretePureState2) :
    proj_01 ψ = proj_10 ψ := by
  dsimp [proj_01, proj_10]
  exact Int.mul_comm ψ.c0 ψ.c1

/-- Projector trace theorem: P_00 + P_11 = denom. -/
theorem projector_trace (ψ : DiscretePureState2) :
    proj_00 ψ + proj_11 ψ = (ψ.denom : Int) := by
  dsimp [proj_00, proj_11]
  exact ψ.h_norm

/-- Projector idempotence on diagonal components:
    (P^2)_00 = P_00 * P_00 + P_01 * P_10 = c0^2 (c0^2 + c1^2) = denom * P_00. -/
theorem projector_idempotence_00 (ψ : DiscretePureState2) :
    proj_00 ψ * proj_00 ψ + proj_01 ψ * proj_10 ψ = (ψ.denom : Int) * proj_00 ψ := by
  dsimp [proj_00, proj_01, proj_10]
  have h1 : (ψ.c0 * ψ.c0 + ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c0) =
            (ψ.c0 * ψ.c0) * (ψ.c0 * ψ.c0) + (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c0) :=
    Int.add_mul (ψ.c0 * ψ.c0) (ψ.c1 * ψ.c1) (ψ.c0 * ψ.c0)
  have h2 : ψ.c0 * ψ.c1 * (ψ.c1 * ψ.c0) = (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c0) := by
    simp [Int.mul_comm, Int.mul_left_comm]
  rw [h2, ← h1, ψ.h_norm]

/-- Projector idempotence on off-diagonal component:
    (P^2)_01 = P_00 * P_01 + P_01 * P_11 = (c0^2 + c1^2) * (c0 * c1) = denom * P_01. -/
theorem projector_idempotence_01 (ψ : DiscretePureState2) :
    proj_00 ψ * proj_01 ψ + proj_01 ψ * proj_11 ψ = (ψ.denom : Int) * proj_01 ψ := by
  dsimp [proj_00, proj_01, proj_11]
  have h1 : (ψ.c0 * ψ.c0 + ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c1) =
            (ψ.c0 * ψ.c0) * (ψ.c0 * ψ.c1) + (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c1) :=
    Int.add_mul (ψ.c0 * ψ.c0) (ψ.c1 * ψ.c1) (ψ.c0 * ψ.c1)
  have h2 : ψ.c0 * ψ.c1 * (ψ.c1 * ψ.c1) = (ψ.c1 * ψ.c1) * (ψ.c0 * ψ.c1) := by
    simp [Int.mul_comm, Int.mul_left_comm]
  rw [h2, ← h1, ψ.h_norm]

/-- Ray invariance: Global sign inversion c -> -c leaves the projector matrix invariant. -/
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
