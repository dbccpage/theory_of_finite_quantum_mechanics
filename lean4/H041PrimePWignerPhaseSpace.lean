

namespace FableHilbertWalk20260819.H041

structure Vec5 where
  v0 : Int
  v1 : Int
  v2 : Int
  v3 : Int
  v4 : Int
  deriving DecidableEq, Repr

def dot5 (u v : Vec5) : Int :=
  u.v0 * v.v0 + u.v1 * v.v1 + u.v2 * v.v2 + u.v3 * v.v3 + u.v4 * v.v4

def normSq5 (u : Vec5) : Int := dot5 u u

def P_op (v : Vec5) : Vec5 :=
  ⟨v.v0, v.v4, v.v3, v.v2, v.v1⟩

theorem parity_is_involution (v : Vec5) : P_op (P_op v) = v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

def psi_stabilizer : Vec5 := ⟨1, 0, 0, 0, 0⟩

def psi_plus : Vec5 := ⟨1, 1, 1, 1, 1⟩

def psi_magic : Vec5 := ⟨0, 1, 0, 0, -1⟩

theorem stabilizer_zero_parity_eigenstate :
    P_op psi_stabilizer = psi_stabilizer := by rfl

theorem stabilizer_zero_positive_expectation :
    dot5 psi_stabilizer (P_op psi_stabilizer) = 1 := by rfl

theorem stabilizer_plus_parity_eigenstate :
    P_op psi_plus = psi_plus := by rfl

theorem stabilizer_plus_positive_expectation :
    dot5 psi_plus (P_op psi_plus) = 5 := by rfl

theorem magic_parity_eigenstate :
    P_op psi_magic = ⟨-psi_magic.v0, -psi_magic.v1, -psi_magic.v2, -psi_magic.v3, -psi_magic.v4⟩ := by rfl

theorem magic_norm_sq : normSq5 psi_magic = 2 := by rfl

theorem magic_parity_inner_product :
    dot5 psi_magic (P_op psi_magic) = -2 := by rfl

theorem magic_wigner_negativity_witness :
    dot5 psi_magic (P_op psi_magic) < 0 ∧
    dot5 psi_magic (P_op psi_magic) = - (normSq5 psi_magic) := by decide

def X_shift (v : Vec5) : Vec5 :=
  ⟨v.v4, v.v0, v.v1, v.v2, v.v3⟩

def X_inv (v : Vec5) : Vec5 :=
  ⟨v.v1, v.v2, v.v3, v.v4, v.v0⟩

theorem x_shift_order_five (v : Vec5) :
    X_shift (X_shift (X_shift (X_shift (X_shift v)))) = v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

theorem x_shift_inverse (v : Vec5) : X_inv (X_shift v) = v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

theorem gross_parity_covariance (v : Vec5) :
    P_op (X_shift (P_op v)) = X_inv v := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

theorem gross_parity_commutation (v : Vec5) :
    P_op (X_shift v) = X_inv (P_op v) := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := v
  rfl

#print axioms parity_is_involution
#print axioms stabilizer_zero_parity_eigenstate
#print axioms stabilizer_zero_positive_expectation
#print axioms stabilizer_plus_parity_eigenstate
#print axioms stabilizer_plus_positive_expectation
#print axioms magic_parity_eigenstate
#print axioms magic_norm_sq
#print axioms magic_parity_inner_product
#print axioms magic_wigner_negativity_witness
#print axioms x_shift_order_five
#print axioms x_shift_inverse
#print axioms gross_parity_covariance
#print axioms gross_parity_commutation

end FableHilbertWalk20260819.H041


theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/H041PrimePWignerPhaseSpace.lean Claim: parity_is_involution AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
