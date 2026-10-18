


namespace ChiralAnomalyInflow

universe u

structure AnomalyInflowPacket where
  q_bulk : Int
  q_surf : Int

def isConservedInflow (p : AnomalyInflowPacket) : Prop :=
  p.q_bulk + p.q_surf = 0

theorem callan_harvey_cancellation (q : Int) :
    isConservedInflow ⟨q, -q⟩ := by
  dsimp [isConservedInflow]
  rw [Int.add_right_neg]

structure ChiralSystem where
  base_energy : Nat
  mu_5 : Nat

def energy_R (s : ChiralSystem) : Nat := s.base_energy
def energy_L (s : ChiralSystem) : Nat := s.base_energy + 2 * s.mu_5

def chiralCochainCurvature (s : ChiralSystem) : Nat :=
  s.mu_5

theorem chiral_symmetric_energy_equality (s : ChiralSystem) (h_zero : s.mu_5 = 0) :
    energy_R s = energy_L s ∧ chiralCochainCurvature s = 0 := by
  dsimp [energy_R, energy_L, chiralCochainCurvature]
  rw [h_zero]
  constructor
  · omega
  · rfl

theorem chiral_symmetric_sign_cancels (w : Nat) :
    (w : Int) * 1 + (w : Int) * (-1) = 0 := by
  rw [Int.mul_one, Int.mul_neg, Int.mul_one, Int.add_right_neg]

theorem chiral_asymmetry_energy_split (s : ChiralSystem) (h_pos : s.mu_5 > 0) :
    energy_L s > energy_R s ∧ chiralCochainCurvature s > 0 := by
  dsimp [energy_R, energy_L, chiralCochainCurvature]
  constructor
  · omega
  · exact h_pos

theorem chiral_asymmetric_weights_nonzero_residual (w_R w_L : Nat) (h_split : w_R > w_L) :
    (w_R : Int) * 1 + (w_L : Int) * (-1) ≠ 0 := by
  rw [Int.mul_one, Int.mul_neg, Int.mul_one]
  intro h_zero
  have h_eq : (w_R : Int) = (w_L : Int) := by omega
  have : w_R = w_L := Int.ofNat_inj.mp h_eq
  omega

end ChiralAnomalyInflow
