

namespace Entanglement

structure BipartiteState2 where
  c00 : Int
  c01 : Int
  c10 : Int
  c11 : Int

def is_product_state (ψ : BipartiteState2) : Prop :=
  ∃ (a0 a1 b0 b1 : Int),
    ψ.c00 = a0 * b0 ∧
    ψ.c01 = a0 * b1 ∧
    ψ.c10 = a1 * b0 ∧
    ψ.c11 = a1 * b1

def schmidt_minor (ψ : BipartiteState2) : Int :=
  ψ.c00 * ψ.c11 - ψ.c01 * ψ.c10

theorem product_state_minor_zero (ψ : BipartiteState2) (h : is_product_state ψ) :
    schmidt_minor ψ = 0 := by
  rcases h with ⟨a0, a1, b0, b1, h00, h01, h10, h11⟩
  dsimp [schmidt_minor]
  rw [h00, h01, h10, h11]
  have h1 : a0 * b0 * (a1 * b1) = (a0 * a1) * (b0 * b1) := by
    simp [Int.mul_comm, Int.mul_left_comm]
  have h2 : a0 * b1 * (a1 * b0) = (a0 * a1) * (b0 * b1) := by
    simp [Int.mul_comm, Int.mul_left_comm]
  rw [h1, h2]
  omega

def bell_phi_plus : BipartiteState2 :=
  { c00 := 1, c01 := 0, c10 := 0, c11 := 1 }

theorem bell_phi_plus_minor_non_zero :
    schmidt_minor bell_phi_plus = 1 := by
  rfl

theorem bell_state_is_entangled :
    ¬ is_product_state bell_phi_plus := by
  intro h_prod
  have h_zero := product_state_minor_zero bell_phi_plus h_prod
  dsimp [schmidt_minor, bell_phi_plus] at h_zero
  revert h_zero
  decide

def reduced_marginal_a (ψ : BipartiteState2) : Int × Int :=
  (ψ.c00 * ψ.c00 + ψ.c01 * ψ.c01, ψ.c10 * ψ.c10 + ψ.c11 * ψ.c11)

def local_flip_b (ψ : BipartiteState2) : BipartiteState2 :=
  { c00 := ψ.c01, c01 := ψ.c00, c10 := ψ.c11, c11 := ψ.c10 }

theorem non_signaling_under_local_b_flip (ψ : BipartiteState2) :
    reduced_marginal_a (local_flip_b ψ) = reduced_marginal_a ψ := by
  dsimp [reduced_marginal_a, local_flip_b]
  have h0 : ψ.c01 * ψ.c01 + ψ.c00 * ψ.c00 = ψ.c00 * ψ.c00 + ψ.c01 * ψ.c01 := by omega
  have h1 : ψ.c11 * ψ.c11 + ψ.c10 * ψ.c10 = ψ.c10 * ψ.c10 + ψ.c11 * ψ.c11 := by omega
  rw [h0, h1]

def local_phase_b (ψ : BipartiteState2) : BipartiteState2 :=
  { c00 := ψ.c00, c01 := -ψ.c01, c10 := ψ.c10, c11 := -ψ.c11 }

theorem non_signaling_under_local_b_phase (ψ : BipartiteState2) :
    reduced_marginal_a (local_phase_b ψ) = reduced_marginal_a ψ := by
  dsimp [reduced_marginal_a, local_phase_b]
  have h0 : (-ψ.c01) * (-ψ.c01) = ψ.c01 * ψ.c01 := by simp [Int.neg_mul_neg]
  have h1 : (-ψ.c11) * (-ψ.c11) = ψ.c11 * ψ.c11 := by simp [Int.neg_mul_neg]
  rw [h0, h1]

#print axioms product_state_minor_zero
#print axioms bell_phi_plus_minor_non_zero
#print axioms bell_state_is_entangled
#print axioms non_signaling_under_local_b_flip
#print axioms non_signaling_under_local_b_phase

end Entanglement

private def l5aProvenance : String :=
  "Origin: lean4/Entanglement.lean Claim: product_state_minor_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
