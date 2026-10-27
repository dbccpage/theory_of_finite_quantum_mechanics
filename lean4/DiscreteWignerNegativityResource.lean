

namespace HilbertWalk.DiscreteWignerNegativityResource

structure Vec3 where
  v0 : Int
  v1 : Int
  v2 : Int
  deriving DecidableEq, Repr

def dot3 (u v : Vec3) : Int :=
  u.v0 * v.v0 + u.v1 * v.v1 + u.v2 * v.v2

def normSq3 (u : Vec3) : Int := dot3 u u

def P_op (v : Vec3) : Vec3 :=
  ⟨v.v0, v.v2, v.v1⟩

theorem parity_is_involution (v : Vec3) : P_op (P_op v) = v := by
  obtain ⟨v0, v1, v2⟩ := v
  rfl

def psi_stabilizer : Vec3 := ⟨1, 0, 0⟩

def psi_magic : Vec3 := ⟨0, 1, -1⟩

theorem stabilizer_parity_eigenstate :
    P_op psi_stabilizer = psi_stabilizer := by rfl

theorem stabilizer_positive_parity_expectation :
    dot3 psi_stabilizer (P_op psi_stabilizer) = 1 := by rfl

theorem magic_parity_eigenstate :
    P_op psi_magic = ⟨-psi_magic.v0, -psi_magic.v1, -psi_magic.v2⟩ := by rfl

theorem magic_norm_sq : normSq3 psi_magic = 2 := by rfl

theorem magic_parity_inner_product :
    dot3 psi_magic (P_op psi_magic) = -2 := by rfl

theorem magic_wigner_negativity_witness :
    dot3 psi_magic (P_op psi_magic) < 0 ∧
    dot3 psi_magic (P_op psi_magic) = - (normSq3 psi_magic) := by decide

#print axioms parity_is_involution
#print axioms stabilizer_parity_eigenstate
#print axioms stabilizer_positive_parity_expectation
#print axioms magic_parity_eigenstate
#print axioms magic_norm_sq
#print axioms magic_parity_inner_product
#print axioms magic_wigner_negativity_witness

end HilbertWalk.DiscreteWignerNegativityResource

private def l5aProvenance : String :=
  "Origin: lean4/DiscreteWignerNegativityResource.lean Claim: parity_is_involution AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
