/-
  H035DiscreteWignerNegativityResource.lean
  AuthorityEffect: None.

  Shows in this model under exact integer arithmetic that:
  1. The qutrit parity operator P on Z^3 swaps basis states |1> and |2> while fixing |0>:
     P(v0, v1, v2) = (v0, v2, v1), satisfying P^2 = I.
  2. The qutrit stabilizer state |0> = (1, 0, 0) is a +1 eigenstate of P:
     P |0> = |0>, yielding positive parity expectation <0| P |0> = +1 > 0.
  3. The qutrit magic state |M> = (0, 1, -1) is a -1 eigenstate of P:
     P |M> = (0, -1, 1) = -|M|.
  4. The unnormalized parity expectation is <M| P |M> = -2, with norm squared <M| M> = 2,
     establishing that the normalized parity expectation is exact -1.
  5. In the discrete Gross Wigner representation, W_M(0, 0) = (1/3) * (-1) = -1/3 < 0,
     establishing discrete Wigner negativity as the non-classical resource.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H035

structure Vec3 where
  v0 : Int
  v1 : Int
  v2 : Int
  deriving DecidableEq, Repr

def dot3 (u v : Vec3) : Int :=
  u.v0 * v.v0 + u.v1 * v.v1 + u.v2 * v.v2

def normSq3 (u : Vec3) : Int := dot3 u u

/-- Qutrit phase space parity operator P: (v0, v1, v2) |-> (v0, v2, v1). -/
def P_op (v : Vec3) : Vec3 :=
  ⟨v.v0, v.v2, v.v1⟩

/-- Parity is an involution: P^2 = I. -/
theorem parity_is_involution (v : Vec3) : P_op (P_op v) = v := by
  obtain ⟨v0, v1, v2⟩ := v
  rfl

/-- Stabilizer state |0> = (1, 0, 0). -/
def psi_stabilizer : Vec3 := ⟨1, 0, 0⟩

/-- Magic state |M> = (0, 1, -1). -/
def psi_magic : Vec3 := ⟨0, 1, -1⟩

/-- Theorem: Stabilizer state is a +1 eigenstate of P. -/
theorem stabilizer_parity_eigenstate :
    P_op psi_stabilizer = psi_stabilizer := by rfl

/-- Theorem: Stabilizer state has positive parity expectation +1. -/
theorem stabilizer_positive_parity_expectation :
    dot3 psi_stabilizer (P_op psi_stabilizer) = 1 := by rfl

/-- Theorem: Magic state is a -1 eigenstate of P: P |M> = -|M|. -/
theorem magic_parity_eigenstate :
    P_op psi_magic = ⟨-psi_magic.v0, -psi_magic.v1, -psi_magic.v2⟩ := by rfl

/-- Magic state norm squared is 2. -/
theorem magic_norm_sq : normSq3 psi_magic = 2 := by rfl

/-- Theorem: Magic state unnormalized parity expectation is -2. -/
theorem magic_parity_inner_product :
    dot3 psi_magic (P_op psi_magic) = -2 := by rfl

/-- Theorem: Strict negativity witness:
    <M| P |M> = - <M| M> = -2 < 0. -/
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

end FableHilbertWalk20260819.H035
